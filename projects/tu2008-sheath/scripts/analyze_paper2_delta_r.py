"""Analyze Paper 2 soft Delta-r scan under results/paper2_delta_r_soft/."""
from __future__ import print_function

import os
import re
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from paths import pffdtd_root, project_root
from analyze_paper2_pilot import robust_load_vc, extract_phasor

F_DRIVE = 700000.0
TRIM = 0.5


def main():
    root = pffdtd_root()
    base = os.path.join(root, "results", "paper2_delta_r_soft")
    out = os.path.join(project_root(), "paper2_oscillating_sheath_boundary", "analysis")
    fig_dir = os.path.join(out, "figures")
    data_dir = os.path.join(out, "data")
    os.makedirs(fig_dir, exist_ok=True)
    os.makedirs(data_dir, exist_ok=True)

    static = {}
    osc = {}
    for name in sorted(os.listdir(base)):
        vc = os.path.join(base, name, "data.vc")
        if not os.path.isfile(vc):
            continue
        t, v, i = robust_load_vc(vc)
        if len(t) < 100:
            continue
        n0 = int(len(t) * TRIM)
        V = extract_phasor(t[n0:], v[n0:], F_DRIVE)
        I = extract_phasor(t[n0:], i[n0:], F_DRIVE)
        Z = V / I
        row = dict(name=name, Z_re=float(np.real(Z)), Z_im=float(np.imag(Z)),
                   Z_mag=float(abs(Z)), Z_phase=float(np.angle(Z, deg=True)))
        m = re.match(r"static_sd(\d+)$", name)
        if m:
            static[int(m.group(1))] = row
            continue
        m = re.match(r"osc_dr(.+)$", name)
        if m:
            tag = m.group(1).replace("p", ".")
            osc[float(tag)] = row

    # Also fold in soft pilot Delta-r=1 if present
    soft_pilot = os.path.join(root, "results", "paper2_rs_t_pilot_soft", "osc_rs_t", "data.vc")
    if os.path.isfile(soft_pilot) and 1.0 not in osc:
        t, v, i = robust_load_vc(soft_pilot)
        n0 = int(len(t) * TRIM)
        V = extract_phasor(t[n0:], v[n0:], F_DRIVE)
        I = extract_phasor(t[n0:], i[n0:], F_DRIVE)
        Z = V / I
        osc[1.0] = dict(name="osc_dr1 (soft pilot)", Z_re=float(np.real(Z)),
                        Z_im=float(np.imag(Z)), Z_mag=float(abs(Z)),
                        Z_phase=float(np.angle(Z, deg=True)))

    tsv = os.path.join(data_dir, "delta_r_soft_phasor_Z.tsv")
    with open(tsv, "w") as f:
        f.write("kind\tparam\tReZ\tImZ\tAbsZ\targZ_deg\n")
        for sd in sorted(static):
            r = static[sd]
            f.write("static\t%d\t%.6e\t%.6e\t%.6e\t%.3f\n" %
                    (sd, r["Z_re"], r["Z_im"], r["Z_mag"], r["Z_phase"]))
        for dr in sorted(osc):
            r = osc[dr]
            f.write("osc\t%.3f\t%.6e\t%.6e\t%.6e\t%.3f\n" %
                    (dr, r["Z_re"], r["Z_im"], r["Z_mag"], r["Z_phase"]))
    print("Wrote", tsv)

    # Distance to nearest static bracket segment for each Delta-r
    # Bracket for Delta-r: static Sd=rs0=4 to Sd=4+ceil(dr)
    metrics = []
    for dr in sorted(osc):
        sd_hi = 4 + int(np.ceil(dr))
        if 4 not in static or sd_hi not in static:
            print("Missing static bracket for dr=", dr, "need", 4, sd_hi)
            continue
        z0 = static[4]["Z_re"] + 1j * static[4]["Z_im"]
        z1 = static[sd_hi]["Z_re"] + 1j * static[sd_hi]["Z_im"]
        zo = osc[dr]["Z_re"] + 1j * osc[dr]["Z_im"]
        w = z1 - z0
        d_br = abs(w)
        if d_br > 0:
            tau = np.real(np.conj(w) * (zo - z0)) / (abs(w) ** 2)
            tau_c = min(1.0, max(0.0, float(tau)))
            d_seg = abs(zo - (z0 + tau_c * w))
            rel = d_seg / d_br
        else:
            tau = float("nan")
            d_seg = abs(zo - z0)
            rel = float("nan")
        metrics.append(dict(dr=dr, d_br=d_br, d_seg=d_seg, rel=rel, tau=float(tau),
                            Z_re=osc[dr]["Z_re"], Z_im=osc[dr]["Z_im"],
                            Z_mag=osc[dr]["Z_mag"]))
        print("dr=%.2f |Z|=%.3e Re=%.3e Im=%.3e rel_bracket=%.3f" %
              (dr, osc[dr]["Z_mag"], osc[dr]["Z_re"], osc[dr]["Z_im"], rel))

    mpath = os.path.join(data_dir, "delta_r_soft_metrics.tsv")
    with open(mpath, "w") as f:
        f.write("delta_r\td_brackets\td_to_segment\trel_to_bracket\ttau\tReZ\tImZ\tAbsZ\n")
        for m in metrics:
            f.write("%.3f\t%.6e\t%.6e\t%.6e\t%.6f\t%.6e\t%.6e\t%.6e\n" %
                    (m["dr"], m["d_br"], m["d_seg"], m["rel"], m["tau"],
                     m["Z_re"], m["Z_im"], m["Z_mag"]))
    print("Wrote", mpath)

    # Plot |Z| and ReZ vs Delta-r; complex plane
    fig, axes = plt.subplots(1, 2, figsize=(9.5, 4.0))
    drs = [m["dr"] for m in metrics]
    axes[0].plot(drs, [m["Z_mag"] for m in metrics], "o-", label="|Z| osc")
    axes[0].plot(drs, [m["Z_re"] for m in metrics], "s-", label="Re Z osc")
    if 4 in static:
        axes[0].axhline(static[4]["Z_mag"], color="C0", ls="--", alpha=0.5, label="|Z| static sd4")
    axes[0].set_xlabel(r"$\Delta r$ (cells)")
    axes[0].set_ylabel(r"$Z$ ($\Omega$)")
    axes[0].set_title(r"Soft $\Delta r$ scan at 700 kHz")
    axes[0].grid(True, alpha=0.3)
    axes[0].legend(fontsize=8)

    for sd, r in sorted(static.items()):
        axes[1].plot(r["Z_re"], r["Z_im"], "o", label="static sd%d" % sd)
    for m in metrics:
        axes[1].plot(m["Z_re"], m["Z_im"], "*", markersize=12, label="osc dr=%.1f" % m["dr"])
    axes[1].set_xlabel(r"Re$\{Z\}$")
    axes[1].set_ylabel(r"Im$\{Z\}$")
    axes[1].set_title("Complex Z")
    axes[1].grid(True, alpha=0.3)
    axes[1].legend(fontsize=7)
    fig.tight_layout()
    fpath = os.path.join(fig_dir, "delta_r_soft_scan.png")
    fig.savefig(fpath, dpi=160)
    plt.close(fig)
    print("Wrote", fpath)

    note = os.path.join(out, "delta_r_soft_findings.md")
    with open(note, "w") as f:
        f.write("# Soft $\\Delta r$ scan findings\n\n")
        f.write("**Data:** `results/paper2_delta_r_soft/` (+ soft pilot $\\Delta r=1$)\n\n")
        f.write("| $\\Delta r$ | Re$Z$ | Im$Z$ | $|Z|$ | rel. to bracket |\n")
        f.write("|----------:|------:|------:|------:|----------------:|\n")
        for m in metrics:
            f.write("| %.1f | %.3e | %.3e | %.3e | **%.2f** |\n" %
                    (m["dr"], m["Z_re"], m["Z_im"], m["Z_mag"], m["rel"]))
        f.write("\n")
        if len(metrics) >= 2:
            # Check monotonic growth of |offset| or |Z| with dr
            rels = [m["rel"] for m in metrics]
            mags = [m["Z_mag"] for m in metrics]
            f.write("rel_to_bracket sequence: %s\n\n" % ", ".join("%.2f" % x for x in rels))
            f.write("|Z| sequence: %s\n\n" % ", ".join("%.3e" % x for x in mags))
            increasing = all(rels[i] <= rels[i+1] * 1.05 for i in range(len(rels)-1))
            if increasing:
                f.write("**Verdict:** Offset from static brackets **grows with** $\\Delta r$ "
                        "(Song-like amplitude trend, at least qualitatively).\n")
            else:
                f.write("**Verdict:** Out-of-bracket offsets remain large for all $\\Delta r$, "
                        "but do **not** increase monotonically — amplitude scaling is mixed; "
                        "interpret with care before claiming clean $\\dot{r}_s$ proportionality.\n")
    print("Wrote", note)


if __name__ == "__main__":
    # allow importing analyze_paper2_pilot helpers
    sys.path.insert(0, os.path.dirname(__file__))
    main()
