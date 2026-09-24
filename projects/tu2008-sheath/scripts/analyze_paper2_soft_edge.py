"""Analyze Paper 2 soft-edge width sensitivity at fixed Delta-r=1.

Combines:
  - static brackets from results/paper2_rs_t_pilot_soft/
  - osc edge=1 from soft pilot osc_rs_t
  - osc edge=0.5, 2.0 from results/paper2_soft_edge_sens/

Writes tables/figures under paper2_oscillating_sheath_boundary/analysis/
and soft_edge_sensitivity.md.
"""
from __future__ import print_function

import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from paths import pffdtd_root, project_root
from analyze_paper2_pilot import robust_load_vc, extract_phasor, rms

F_DRIVE = 700000.0
TRIM = 0.5


def phasor_row(name, edge, t, v, i, f):
    n0 = int(len(t) * TRIM)
    t_ss, v_ss, i_ss = t[n0:], v[n0:], i[n0:]
    V = extract_phasor(t_ss, v_ss, f)
    I = extract_phasor(t_ss, i_ss, f)
    Z = V / I if abs(I) > 0 else np.nan + 1j * np.nan
    return dict(
        name=name,
        edge=edge,
        Z_re=float(np.real(Z)),
        Z_im=float(np.imag(Z)),
        Z_mag=float(abs(Z)),
        Z_phase=float(np.angle(Z, deg=True)),
        I_rms=rms(i_ss),
        V_rms=rms(v_ss),
        t=t,
        v=v,
        i=i,
        t_ss=t_ss,
        v_ss=v_ss,
        i_ss=i_ss,
    )


def bracket_metrics(z0, z1, zo):
    w = z1 - z0
    d_br = abs(w)
    if d_br > 0:
        tau = float(np.real(np.conj(w) * (zo - z0)) / (abs(w) ** 2))
        tau_c = min(1.0, max(0.0, tau))
        d_seg = abs(zo - (z0 + tau_c * w))
        rel = d_seg / d_br
    else:
        tau = float("nan")
        d_seg = abs(zo - z0)
        rel = float("nan")
    return dict(d_br=d_br, d_seg=d_seg, rel=rel, tau=tau)


def main():
    root = pffdtd_root()
    out = os.path.join(project_root(), "paper2_oscillating_sheath_boundary", "analysis")
    fig_dir = os.path.join(out, "figures")
    data_dir = os.path.join(out, "data")
    os.makedirs(fig_dir, exist_ok=True)
    os.makedirs(data_dir, exist_ok=True)

    soft_pilot = os.path.join(root, "results", "paper2_rs_t_pilot_soft")
    sens = os.path.join(root, "results", "paper2_soft_edge_sens")

    sources = [
        ("static_rs0", None, os.path.join(soft_pilot, "static_rs0", "data.vc")),
        ("static_rsmax", None, os.path.join(soft_pilot, "static_rsmax", "data.vc")),
        ("osc_edge0p5", 0.5, os.path.join(sens, "osc_edge0p5", "data.vc")),
        ("osc_edge1", 1.0, os.path.join(soft_pilot, "osc_rs_t", "data.vc")),
        ("osc_edge2", 2.0, os.path.join(sens, "osc_edge2", "data.vc")),
    ]

    rows = []
    missing = []
    for name, edge, path in sources:
        if not os.path.isfile(path):
            missing.append(path)
            continue
        t, v, i = robust_load_vc(path)
        if len(t) < 100:
            missing.append(path + " (too short)")
            continue
        # Heuristic: unfinished runs have much shorter t_end than soft pilot (~28.7 us)
        if name.startswith("osc_") and float(t[-1]) < 2.0e-5:
            missing.append(path + " (incomplete t_end=%.3e)" % float(t[-1]))
            continue
        rows.append(phasor_row(name, edge, t, v, i, F_DRIVE))

    if missing:
        print("MISSING/INCOMPLETE:")
        for m in missing:
            print(" ", m)
    if len(rows) < 3:
        print("Not enough complete cases to analyze")
        sys.exit(1)

    by = {r["name"]: r for r in rows}
    if "static_rs0" not in by or "static_rsmax" not in by:
        print("Need both static brackets from soft pilot")
        sys.exit(1)

    z0 = by["static_rs0"]["Z_re"] + 1j * by["static_rs0"]["Z_im"]
    z1 = by["static_rsmax"]["Z_re"] + 1j * by["static_rsmax"]["Z_im"]

    osc_rows = [r for r in rows if r["edge"] is not None]
    osc_rows.sort(key=lambda r: r["edge"])

    tsv = os.path.join(data_dir, "soft_edge_sensitivity_Z.tsv")
    with open(tsv, "w") as f:
        f.write("case\tedge_cells\tReZ\tImZ\tAbsZ\targZ_deg\tIrms\trel_to_bracket\ttau\td_seg\n")
        for r in rows:
            if r["edge"] is None:
                f.write("%s\tNA\t%.6e\t%.6e\t%.6e\t%.3f\t%.6e\tNA\tNA\tNA\n" %
                        (r["name"], r["Z_re"], r["Z_im"], r["Z_mag"], r["Z_phase"], r["I_rms"]))
            else:
                zo = r["Z_re"] + 1j * r["Z_im"]
                m = bracket_metrics(z0, z1, zo)
                f.write("%s\t%.3f\t%.6e\t%.6e\t%.6e\t%.3f\t%.6e\t%.6e\t%.6f\t%.6e\n" %
                        (r["name"], r["edge"], r["Z_re"], r["Z_im"], r["Z_mag"],
                         r["Z_phase"], r["I_rms"], m["rel"], m["tau"], m["d_seg"]))
    print("Wrote", tsv)

    # Complex Z
    fig, ax = plt.subplots(figsize=(5.6, 4.4))
    ax.plot([by["static_rs0"]["Z_re"], by["static_rsmax"]["Z_re"]],
            [by["static_rs0"]["Z_im"], by["static_rsmax"]["Z_im"]],
            "k--", lw=1, alpha=0.5, label="static bracket")
    ax.plot(by["static_rs0"]["Z_re"], by["static_rs0"]["Z_im"], "o", color="C0",
            markersize=9, label="static rs0")
    ax.plot(by["static_rsmax"]["Z_re"], by["static_rsmax"]["Z_im"], "s", color="C1",
            markersize=9, label="static rsmax")
    cmap = {0.5: "C2", 1.0: "C3", 2.0: "C4"}
    for r in osc_rows:
        ax.plot(r["Z_re"], r["Z_im"], "*", color=cmap.get(r["edge"], "k"),
                markersize=14, label="osc edge=%.1f" % r["edge"])
    ax.set_xlabel(r"Re$\{Z\}$ ($\Omega$)")
    ax.set_ylabel(r"Im$\{Z\}$ ($\Omega$)")
    ax.set_title(r"Soft-edge sensitivity ($\Delta r=1$, $f=700$ kHz)")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8)
    fig.tight_layout()
    zpath = os.path.join(fig_dir, "soft_edge_Z_complex.png")
    fig.savefig(zpath, dpi=160)
    plt.close(fig)
    print("Wrote", zpath)

    # rel vs edge + Irms vs edge
    if osc_rows:
        fig, axes = plt.subplots(1, 2, figsize=(7.5, 3.4))
        edges = [r["edge"] for r in osc_rows]
        rels = []
        irms = [r["I_rms"] for r in osc_rows]
        for r in osc_rows:
            zo = r["Z_re"] + 1j * r["Z_im"]
            rels.append(bracket_metrics(z0, z1, zo)["rel"])
        axes[0].plot(edges, rels, "o-", color="C3")
        axes[0].set_xlabel("SheathSoftEdge (cells)")
        axes[0].set_ylabel("rel_to_bracket")
        axes[0].set_title("Out-of-bracket metric")
        axes[0].grid(True, alpha=0.3)
        axes[1].plot(edges, irms, "o-", color="C0", label="osc")
        axes[1].axhline(by["static_rs0"]["I_rms"], color="C0", ls="--", alpha=0.5, label="static rs0")
        axes[1].axhline(by["static_rsmax"]["I_rms"], color="C1", ls="--", alpha=0.5, label="static rsmax")
        axes[1].set_xlabel("SheathSoftEdge (cells)")
        axes[1].set_ylabel(r"$I_\mathrm{rms}$ (A)")
        axes[1].set_title("Feed current RMS")
        axes[1].legend(fontsize=7)
        axes[1].grid(True, alpha=0.3)
        fig.tight_layout()
        mpath = os.path.join(fig_dir, "soft_edge_metrics.png")
        fig.savefig(mpath, dpi=160)
        plt.close(fig)
        print("Wrote", mpath)

    # Late-time I overlay for osc edges
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    t_win = 5.0 / F_DRIVE
    for r in osc_rows:
        t_ss, i_ss = r["t_ss"], r["i_ss"]
        t0 = t_ss[-1] - t_win
        m = t_ss >= t0
        ax.plot(t_ss[m] * 1e6, i_ss[m] * 1e6, lw=1.1,
                color=cmap.get(r["edge"], "k"), label="edge=%.1f" % r["edge"])
    ax.set_xlabel(r"$t$ ($\mu$s)")
    ax.set_ylabel(r"$I$ ($\mu$A)")
    ax.set_title("Last ~5 cycles — soft-edge osc currents")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    ipath = os.path.join(fig_dir, "soft_edge_I_last_cycles.png")
    fig.savefig(ipath, dpi=160)
    plt.close(fig)
    print("Wrote", ipath)

    # Findings note
    note = os.path.join(out, "soft_edge_sensitivity.md")
    with open(note, "w") as f:
        f.write("# Soft-edge width sensitivity (fixed $\\Delta r=1$)\n\n")
        f.write("**Date:** auto-generated  \n")
        f.write("**Drive:** $f=700$ kHz, $r_{s0}=4$, $\\Delta r=1$, $\\phi=0$  \n")
        f.write("**Statics:** `results/paper2_rs_t_pilot_soft/`  \n")
        f.write("**Osc edge=1:** soft pilot `osc_rs_t`  \n")
        f.write("**Osc edge=0.5, 2:** `results/paper2_soft_edge_sens/`\n\n")
        f.write("## Phasor table\n\n")
        f.write("| Case | edge | Re$Z$ | Im$Z$ | $|Z|$ | arg$Z$ | $I_\\mathrm{rms}$ | rel_to_bracket |\n")
        f.write("|------|-----:|------:|------:|------:|-------:|------------------:|---------------:|\n")
        for r in rows:
            if r["edge"] is None:
                f.write("| `%s` | — | %.3e | %.3e | %.3e | %.2f | %.3e | — |\n" %
                        (r["name"], r["Z_re"], r["Z_im"], r["Z_mag"], r["Z_phase"], r["I_rms"]))
            else:
                zo = r["Z_re"] + 1j * r["Z_im"]
                m = bracket_metrics(z0, z1, zo)
                f.write("| `%s` | %.1f | %.3e | %.3e | %.3e | %.2f | %.3e | **%.3f** |\n" %
                        (r["name"], r["edge"], r["Z_re"], r["Z_im"], r["Z_mag"],
                         r["Z_phase"], r["I_rms"], m["rel"]))
        f.write("\n## Verdict criteria (SCIENCE.md §2.2)\n\n")
        f.write("- Out-of-bracket must **survive** across edge widths → more like physics.\n")
        f.write("- If offset vanishes only at large edge → more like artifact.\n\n")
        if len(osc_rows) >= 2:
            rels = [bracket_metrics(z0, z1, r["Z_re"] + 1j * r["Z_im"])["rel"] for r in osc_rows]
            all_out = all(x > 0.5 for x in rels)
            spread = max(rels) - min(rels)
            if all_out:
                f.write(
                    "**Verdict:** Out-of-bracket loading **survives** for soft edges "
                    "%s (rel = %s). Soft-edge width moves the point but does not "
                    "collapse the dynamic signature onto the static bracket.\n\n"
                    % (", ".join("%.1f" % r["edge"] for r in osc_rows),
                       ", ".join("%.2f" % x for x in rels))
                )
            else:
                f.write(
                    "**Verdict:** At least one edge width sits near/on the bracket "
                    "(rel = %s). Treat width dependence as a caution for numerics.\n\n"
                    % (", ".join("%.2f" % x for x in rels))
                )
            f.write("Rel span across edges: %.3f.\n\n" % spread)
        f.write("## Figures\n\n")
        f.write("- `figures/soft_edge_Z_complex.png`\n")
        f.write("- `figures/soft_edge_metrics.png`\n")
        f.write("- `figures/soft_edge_I_last_cycles.png`\n")
    print("Wrote", note)
    for r in osc_rows:
        zo = r["Z_re"] + 1j * r["Z_im"]
        m = bracket_metrics(z0, z1, zo)
        print("edge=%.1f Z=%.4e+j%.4e rel=%.4f Irms=%.4e" %
              (r["edge"], r["Z_re"], r["Z_im"], m["rel"], r["I_rms"]))


if __name__ == "__main__":
    main()
