"""Partial analysis of the in-progress CW Tu sweep.

Reads completed cases under results/sheath_cw_tu/ only. Writes plots and
tables to paper0_sheath_campaign/analysis/ — never into the sweep directory (jobs may still be
running).

Resonance convention: first Im{Z} +to- crossing (CW series feature).
"""
from __future__ import print_function

import glob
import os
import re
from datetime import datetime

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from paths import analysis_dir, pffdtd_root

SDS = [0, 2, 4, 6, 8, 10]
FREQS = [
    1500000, 1600000, 1700000, 1750000, 1800000, 1850000,
    1900000, 2000000, 2100000, 2200000, 2300000,
]
MIN_VC_BYTES = 300000
RECENT_WRITE_SEC = 120



def robust_load_vc(path):
    times, volts, currents = [], [], []
    with open(path, "r", errors="ignore") as f:
        for line in f:
            parts = line.strip().replace(",", " ").split()
            if len(parts) < 3:
                continue
            try:
                t, v, i = float(parts[0]), float(parts[1]), float(parts[2])
            except ValueError:
                continue
            times.append(t)
            volts.append(v)
            currents.append(i)
    return np.array(times), np.array(volts), np.array(currents)


def extract_phasor(t, signal, f):
    dt = t[1] - t[0]
    return np.sum(signal * np.exp(-1j * 2 * np.pi * f * t)) * dt


def classify_case(out_dir):
    """Return status string: pending, running, incomplete, complete."""
    vc = os.path.join(out_dir, "data.vc")
    log = os.path.join(out_dir, "simulation.log")
    if not os.path.isdir(out_dir):
        return "pending"
    log_text = ""
    if os.path.isfile(log):
        with open(log, "r", errors="ignore") as f:
            log_text = f.read()
    has_done = "DONE" in log_text
    if os.path.isfile(vc):
        size = os.path.getsize(vc)
        age = datetime.now().timestamp() - os.path.getmtime(vc)
        if size >= MIN_VC_BYTES:
            # SKIP-restarted cases may lack a DONE line; a large, idle .vc is usable.
            if has_done or age >= RECENT_WRITE_SEC:
                return "complete"
            return "running"
        if age < RECENT_WRITE_SEC:
            return "running"
        if size > 0:
            return "incomplete"
    if "START" in log_text and not has_done:
        return "running"
    return "pending"


def find_plus_to_minus(freqs, imag_z):
    for i in range(1, len(imag_z)):
        if imag_z[i - 1] > 0 and imag_z[i] <= 0:
            denom = imag_z[i] - imag_z[i - 1]
            if denom == 0:
                return freqs[i]
            return freqs[i - 1] + (freqs[i] - freqs[i - 1]) * (-imag_z[i - 1]) / denom
    return None


def main():
    root = pffdtd_root()
    base_dir = os.path.join(root, "results", "sheath_cw_tu")
    fig_dir = os.path.join(analysis_dir(), "figures")
    data_dir = os.path.join(analysis_dir(), "data")
    os.makedirs(fig_dir, exist_ok=True)
    os.makedirs(data_dir, exist_ok=True)

    status = {}
    data_by_sd = {}
    skipped_running = []

    for sd in SDS:
        for f in FREQS:
            out_dir = os.path.join(base_dir, "sd%d_f%d" % (sd, f))
            st = classify_case(out_dir)
            status[(sd, f)] = st
            if st != "complete":
                if st == "running":
                    skipped_running.append((sd, f))
                continue
            vc = os.path.join(out_dir, "data.vc")
            print("Processing Sd=%d, Freq=%d Hz" % (sd, f))
            t, v, i = robust_load_vc(vc)
            if len(t) < 4:
                status[(sd, f)] = "incomplete"
                continue
            idx = len(t) // 2
            V = extract_phasor(t[idx:], v[idx:], float(f))
            I = extract_phasor(t[idx:], i[idx:], float(f))
            if abs(I) == 0:
                continue
            Z = V / I
            data_by_sd.setdefault(sd, {"freqs": [], "Z": []})
            data_by_sd[sd]["freqs"].append(float(f))
            data_by_sd[sd]["Z"].append(Z)

    n_complete = sum(1 for s in status.values() if s == "complete")
    n_running = sum(1 for s in status.values() if s == "running")
    n_pending = sum(1 for s in status.values() if s == "pending")
    n_incomplete = sum(1 for s in status.values() if s == "incomplete")
    print("Status: complete=%d running=%d pending=%d incomplete=%d / 66" % (
        n_complete, n_running, n_pending, n_incomplete))
    if skipped_running:
        print("Skipped running cases:", skipped_running)

    summary_path = os.path.join(data_dir, "cw_tu_summary.txt")
    with open(summary_path, "w") as out:
        out.write("# Partial CW Tu sweep (completed cases only)\n")
        out.write("# Analyzed: %s\n" % datetime.now().strftime("%Y-%m-%d %H:%M"))
        out.write("# Method: phasor Z on last 50%% of V/I; +to- Im{Z} crossing\n")
        out.write("# complete=%d running=%d pending=%d incomplete=%d / 66\n" % (
            n_complete, n_running, n_pending, n_incomplete))
        out.write("Sd\tFreq_Hz\tRe_Z\tIm_Z\n")
        for sd in sorted(data_by_sd):
            freqs = np.array(data_by_sd[sd]["freqs"])
            Zs = np.array(data_by_sd[sd]["Z"])
            order = np.argsort(freqs)
            for freq, Z in zip(freqs[order], Zs[order]):
                out.write("%d\t%.0f\t%.6f\t%.6f\n" % (sd, freq, Z.real, Z.imag))
    print("Wrote", summary_path)

    res_path = os.path.join(data_dir, "cw_tu_resonance.txt")
    resonances = {}
    with open(res_path, "w") as out:
        out.write("# Provisional f_res from completed points only (Im +to-)\n")
        out.write("Sd\tf_res_Hz\tnote\n")
        for sd in sorted(data_by_sd):
            freqs = np.array(data_by_sd[sd]["freqs"])
            Zs = np.array(data_by_sd[sd]["Z"])
            order = np.argsort(freqs)
            freqs = freqs[order]
            imag = np.imag(Zs[order])
            f_res = find_plus_to_minus(freqs, imag)
            if f_res is None:
                if len(imag) and np.all(imag < 0):
                    note = "all Im<0 in completed band (crossing at or below %.2f MHz)" % (freqs[0] / 1e6)
                elif len(imag) and np.all(imag > 0):
                    note = "all Im>0 in completed band (crossing above %.2f MHz or pending)" % (freqs[-1] / 1e6)
                else:
                    note = "no +to- crossing in completed points"
                out.write("%d\t\t%s\n" % (sd, note))
                resonances[sd] = (None, note)
            else:
                out.write("%d\t%.1f\tcrossing in completed band\n" % (sd, f_res))
                resonances[sd] = (f_res, "crossing in completed band")
                print("** Sd=%d f_res=%.3f MHz **" % (sd, f_res / 1e6))
    print("Wrote", res_path)

    status_path = os.path.join(data_dir, "cw_tu_status.txt")
    with open(status_path, "w") as out:
        header = "Sd\\" + "\t".join("%.2f" % (f / 1e6) for f in FREQS)
        out.write("# Case status grid (MHz). complete / running / pending / incomplete\n")
        out.write("Sd\t" + "\t".join("%.2f" % (f / 1e6) for f in FREQS) + "\n")
        for sd in SDS:
            row = [str(sd)]
            for f in FREQS:
                row.append(status[(sd, f)])
            out.write("\t".join(row) + "\n")
    print("Wrote", status_path)

    if data_by_sd:
        fig, (ax_real, ax_imag) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
        for sd in sorted(data_by_sd):
            freqs = np.array(data_by_sd[sd]["freqs"])
            Zs = np.array(data_by_sd[sd]["Z"])
            order = np.argsort(freqs)
            freqs = freqs[order] / 1e6
            Zs = Zs[order]
            ax_real.plot(freqs, np.real(Zs), "o-", label="Sd=%d" % sd)
            ax_imag.plot(freqs, np.imag(Zs), "o-", label="Sd=%d" % sd)
        ax_real.set_ylabel(r"Re$\{Z\}$ ($\Omega$)")
        ax_real.set_title("CW Tu sweep (all completed cases)")
        ax_real.legend()
        ax_real.grid(True)
        ax_imag.set_xlabel("Frequency (MHz)")
        ax_imag.set_ylabel(r"Im$\{Z\}$ ($\Omega$)")
        ax_imag.axhline(0, color="k", linestyle="--", linewidth=1)
        ax_imag.legend()
        ax_imag.grid(True)
        plt.tight_layout()
        plot_path = os.path.join(fig_dir, "cw_tu_impedance.png")
        plt.savefig(plot_path, dpi=150)
        print("Saved", plot_path)

        fig2, ax = plt.subplots(figsize=(8, 4.5))
        sds_plot, fres_plot = [], []
        for sd, (f_res, _note) in resonances.items():
            if f_res is not None:
                sds_plot.append(sd)
                fres_plot.append(f_res / 1e6)
        if sds_plot:
            ax.plot(sds_plot, fres_plot, "o-", color="C0", label=r"$f_\mathrm{res}$")
        ax.set_xlabel(r"Sheath width $S_d$ (cells)")
        ax.set_ylabel(r"$f_\mathrm{res}$ (MHz)")
        ax.set_title(r"$f_\mathrm{res}(S_d)$ from CW grid ($\Im Z$ +to- crossing)")
        ax.grid(True)
        ax.legend()
        plt.tight_layout()
        res_plot = os.path.join(fig_dir, "cw_tu_resonance.png")
        plt.savefig(res_plot, dpi=150)
        print("Saved", res_plot)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
