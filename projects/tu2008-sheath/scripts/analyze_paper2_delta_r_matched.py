"""Analyze Paper 2 matched soft Delta-r scan (soft = c * Delta-r).

Reads results/paper2_delta_r_matched/osc_dr* plus soft-pilot Delta-r=1,
and static brackets from soft pilot / prior soft Delta-r scan.
Writes analysis under paper2_oscillating_sheath_boundary/analysis/.
"""
from __future__ import print_function

import math
import os
import re
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from paths import pffdtd_root, project_root
from analyze_paper2_pilot import robust_load_vc, extract_phasor
from analyze_paper2_soft_edge import bracket_metrics

F_DRIVE = 700000.0
TRIM = 0.5
RS0 = 4


def phasor(path):
    t, v, i = robust_load_vc(path)
    if len(t) < 100 or float(t[-1]) < 2e-5:
        return None
    n0 = int(len(t) * TRIM)
    V = extract_phasor(t[n0:], v[n0:], F_DRIVE)
    I = extract_phasor(t[n0:], i[n0:], F_DRIVE)
    Z = V / I if abs(I) > 0 else np.nan + 1j * np.nan
    return dict(
        Z_re=float(np.real(Z)), Z_im=float(np.imag(Z)),
        Z_mag=float(abs(Z)), Z_phase=float(np.angle(Z, deg=True)),
    )


def main():
    root = pffdtd_root()
    matched = os.path.join(root, "results", "paper2_delta_r_matched")
    soft_pilot = os.path.join(root, "results", "paper2_rs_t_pilot_soft")
    old_delta = os.path.join(root, "results", "paper2_delta_r_soft")
    out = os.path.join(project_root(), "paper2_oscillating_sheath_boundary", "analysis")
    fig_dir = os.path.join(out, "figures")
    data_dir = os.path.join(out, "data")
    os.makedirs(fig_dir, exist_ok=True)
    os.makedirs(data_dir, exist_ok=True)

    static = {}
    for base in (soft_pilot, old_delta):
        if not os.path.isdir(base):
            continue
        for name in os.listdir(base):
            m = re.match(r"static_(?:rs0|rsmax|sd)(\d*)$", name)
            vc = os.path.join(base, name, "data.vc")
            if not os.path.isfile(vc):
                continue
            if name == "static_rs0":
                sd = RS0
            elif name == "static_rsmax":
                sd = RS0 + 1
            elif name.startswith("static_sd"):
                sd = int(name.replace("static_sd", ""))
            else:
                continue
            if sd in static:
                continue
            row = phasor(vc)
            if row:
                static[sd] = row

    osc = {}
    if os.path.isdir(matched):
        for name in sorted(os.listdir(matched)):
            m = re.match(r"osc_dr(.+)$", name)
            if not m:
                continue
            tag = m.group(1).replace("p", ".")
            vc = os.path.join(matched, name, "data.vc")
            row = phasor(vc)
            if row:
                osc[float(tag)] = row
                osc[float(tag)]["soft"] = float(tag)  # SoftFrac=1

    # Delta-r=1 soft=1 from soft pilot
    vc1 = os.path.join(soft_pilot, "osc_rs_t", "data.vc")
    if os.path.isfile(vc1) and 1.0 not in osc:
        row = phasor(vc1)
        if row:
            osc[1.0] = row
            osc[1.0]["soft"] = 1.0

    if not osc:
        print("No matched osc cases found")
        sys.exit(1)

    tsv = os.path.join(data_dir, "delta_r_matched_phasor_Z.tsv")
    metrics = []
    with open(tsv, "w") as f:
        f.write("dr\tsoft\tReZ\tImZ\tAbsZ\targZ_deg\trel_to_bracket\ttau\tdZ_abs\n")
        for dr in sorted(osc):
            r = osc[dr]
            soft = r.get("soft", dr)
            sd_hi = RS0 + int(math.ceil(dr - 1e-12))
            if RS0 not in static or sd_hi not in static:
                print("Missing static bracket for dr=", dr, "need", RS0, sd_hi)
                f.write("%.3f\t%.3f\t%.6e\t%.6e\t%.6e\t%.3f\tNA\tNA\tNA\n" %
                        (dr, soft, r["Z_re"], r["Z_im"], r["Z_mag"], r["Z_phase"]))
                continue
            z0 = static[RS0]["Z_re"] + 1j * static[RS0]["Z_im"]
            z1 = static[sd_hi]["Z_re"] + 1j * static[sd_hi]["Z_im"]
            zo = r["Z_re"] + 1j * r["Z_im"]
            m = bracket_metrics(z0, z1, zo)
            d_abs = abs(zo - 0.5 * (z0 + z1))
            f.write("%.3f\t%.3f\t%.6e\t%.6e\t%.6e\t%.3f\t%.6e\t%.6f\t%.6e\n" %
                    (dr, soft, r["Z_re"], r["Z_im"], r["Z_mag"], r["Z_phase"],
                     m["rel"], m["tau"], d_abs))
            metrics.append(dict(dr=dr, soft=soft, rel=m["rel"], tau=m["tau"],
                                d_abs=d_abs, Z_re=r["Z_re"], Z_im=r["Z_im"],
                                Z_mag=r["Z_mag"], Z_phase=r["Z_phase"],
                                z0=z0, z1=z1, zo=zo))
    print("Wrote", tsv)

    # Complex plane
    fig, ax = plt.subplots(figsize=(5.8, 4.6))
    for m in metrics:
        ax.plot([np.real(m["z0"]), np.real(m["z1"])],
                [np.imag(m["z0"]), np.imag(m["z1"])],
                "--", color="0.6", lw=1, alpha=0.5)
        ax.plot(m["Z_re"], m["Z_im"], "*", markersize=14,
                label=r"$\Delta r=%.1f$ (soft=%.1f)" % (m["dr"], m["soft"]))
    ax.set_xlabel(r"Re$\{Z\}$ ($\Omega$)")
    ax.set_ylabel(r"Im$\{Z\}$ ($\Omega$)")
    ax.set_title(r"Matched soft $\Delta r$ ($f=700$ kHz)")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=7)
    fig.tight_layout()
    p1 = os.path.join(fig_dir, "delta_r_matched_Z_complex.png")
    fig.savefig(p1, dpi=160)
    plt.close(fig)
    print("Wrote", p1)

    if metrics:
        fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.5))
        drs = [m["dr"] for m in metrics]
        axes[0].plot(drs, [m["rel"] for m in metrics], "o-", color="C3")
        axes[0].set_xlabel(r"$\Delta r$ (cells)")
        axes[0].set_ylabel("rel_to_bracket")
        axes[0].set_title("Out-of-bracket (matched soft)")
        axes[0].grid(True, alpha=0.3)
        axes[1].plot(drs, [m["d_abs"] for m in metrics], "o-", color="C0", label=r"$|Z-Z_\mathrm{mid}|$")
        axes[1].plot(drs, [m["Z_mag"] for m in metrics], "s--", color="C1", label=r"$|Z|$")
        axes[1].set_xlabel(r"$\Delta r$ (cells)")
        axes[1].set_ylabel(r"$\Omega$")
        axes[1].set_title("Absolute offsets")
        axes[1].legend(fontsize=7)
        axes[1].grid(True, alpha=0.3)
        fig.tight_layout()
        p2 = os.path.join(fig_dir, "delta_r_matched_metrics.png")
        fig.savefig(p2, dpi=160)
        plt.close(fig)
        print("Wrote", p2)

    note = os.path.join(out, "delta_r_matched_findings.md")
    with open(note, "w") as f:
        f.write("# Matched soft $\\Delta r$ findings\n\n")
        f.write("**Date:** 2026-09-25  \n")
        f.write("**Policy:** $\\mathrm{SheathSoftEdge}=\\Delta r$ (SoftFrac=1)  \n")
        f.write("**Drive:** $f=700$ kHz, $r_{s0}=4$, $\\phi=0$  \n")
        f.write("**Data:** `results/paper2_delta_r_matched/` (+ soft pilot $\\Delta r=1$)\n\n")
        f.write("| $\\Delta r$ | soft | Re$Z$ | Im$Z$ | $|Z|$ | rel_to_bracket | $|Z-Z_\\mathrm{mid}|$ |\n")
        f.write("|----------:|-----:|------:|------:|------:|---------------:|---------------------:|\n")
        for m in metrics:
            f.write("| %.1f | %.1f | %.3e | %.3e | %.3e | **%.3f** | %.3e |\n" %
                    (m["dr"], m["soft"], m["Z_re"], m["Z_im"], m["Z_mag"],
                     m["rel"], m["d_abs"]))
        f.write("\n## Verdict\n\n")
        if metrics:
            rels = [m["rel"] for m in metrics]
            mags = [m["Z_mag"] for m in metrics]
            mono_rel = all(rels[i] <= rels[i + 1] + 1e-9 for i in range(len(rels) - 1))
            mono_mag = all(mags[i] <= mags[i + 1] + 1e-9 for i in range(len(mags) - 1))
            n_out = sum(1 for x in rels if x > 0.5)
            f.write("Out-of-bracket at **%d / %d** matched amplitudes (rel > 0.5).\n\n" %
                    (n_out, len(metrics)))
            if mono_rel or mono_mag:
                f.write(
                    "Under matched soft policy, amplitude response looks "
                    "**more orderly** (rel monotonic=%s, |Z| monotonic=%s).\n"
                    % (mono_rel, mono_mag)
                )
            else:
                f.write(
                    "Even with soft$\\propto\\Delta r$, rel / $|Z|$ remain "
                    "**non-monotonic**. Treat amplitude scaling as unsettled; "
                    "report as a finding, not a failure.\n"
                )
        f.write("\n## Figures\n\n")
        f.write("- `figures/delta_r_matched_Z_complex.png`\n")
        f.write("- `figures/delta_r_matched_metrics.png`\n")
    print("Wrote", note)
    for m in metrics:
        print("dr=%.1f soft=%.1f rel=%.3f |Z|=%.3e d_abs=%.3e" %
              (m["dr"], m["soft"], m["rel"], m["Z_mag"], m["d_abs"]))


if __name__ == "__main__":
    main()
