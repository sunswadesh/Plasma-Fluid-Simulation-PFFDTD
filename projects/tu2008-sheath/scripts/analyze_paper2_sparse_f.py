"""Analyze Paper 2 sparse-frequency soft scan.

Reads results/paper2_sparse_f_soft/{static_rs0_f*,static_rsmax_f*,osc_f*}/data.vc
plus 700 kHz soft pilot for the third frequency.
Writes tables/figures under paper2_oscillating_sheath_boundary/analysis/.
"""
from __future__ import print_function

import os
import re
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from paths import pffdtd_root, project_root
from analyze_paper2_pilot import robust_load_vc, extract_phasor, rms
from analyze_paper2_soft_edge import bracket_metrics

TRIM = 0.5


def phasor_at(path, f):
    t, v, i = robust_load_vc(path)
    if len(t) < 100:
        return None
    if float(t[-1]) < 0.5 / f:
        return None
    n0 = int(len(t) * TRIM)
    V = extract_phasor(t[n0:], v[n0:], f)
    I = extract_phasor(t[n0:], i[n0:], f)
    Z = V / I if abs(I) > 0 else np.nan + 1j * np.nan
    return dict(
        Z_re=float(np.real(Z)), Z_im=float(np.imag(Z)),
        Z_mag=float(abs(Z)), Z_phase=float(np.angle(Z, deg=True)),
        I_rms=rms(i[n0:]), t_end=float(t[-1]),
    )


def main():
    root = pffdtd_root()
    base = os.path.join(root, "results", "paper2_sparse_f_soft")
    soft_pilot = os.path.join(root, "results", "paper2_rs_t_pilot_soft")
    out = os.path.join(project_root(), "paper2_oscillating_sheath_boundary", "analysis")
    fig_dir = os.path.join(out, "figures")
    data_dir = os.path.join(out, "data")
    os.makedirs(fig_dir, exist_ok=True)
    os.makedirs(data_dir, exist_ok=True)

    # freq_hz -> {static_rs0, static_rsmax, osc}
    by_f = {}

    if os.path.isdir(base):
        for name in sorted(os.listdir(base)):
            vc = os.path.join(base, name, "data.vc")
            if not os.path.isfile(vc):
                continue
            m = re.match(r"(static_rs0|static_rsmax|osc)_f(\d+)$", name)
            if not m:
                continue
            kind, f = m.group(1), int(m.group(2))
            row = phasor_at(vc, float(f))
            if row is None:
                print("SKIP incomplete", name)
                continue
            by_f.setdefault(f, {})[kind] = row

    # Fold in 700 kHz soft pilot
    f700 = 700000
    if f700 not in by_f:
        by_f[f700] = {}
    for kind, sub in (("static_rs0", "static_rs0"),
                      ("static_rsmax", "static_rsmax"),
                      ("osc", "osc_rs_t")):
        if kind in by_f[f700]:
            continue
        vc = os.path.join(soft_pilot, sub, "data.vc")
        if os.path.isfile(vc):
            row = phasor_at(vc, float(f700))
            if row is not None:
                by_f[f700][kind] = row

    if not by_f:
        print("No sparse-f cases found")
        sys.exit(1)

    tsv = os.path.join(data_dir, "sparse_f_soft_phasor_Z.tsv")
    metrics = []
    with open(tsv, "w") as f:
        f.write("f_Hz\tkind\tReZ\tImZ\tAbsZ\targZ_deg\tIrms\trel_to_bracket\ttau\n")
        for freq in sorted(by_f):
            block = by_f[freq]
            z0 = z1 = None
            if "static_rs0" in block and "static_rsmax" in block:
                z0 = block["static_rs0"]["Z_re"] + 1j * block["static_rs0"]["Z_im"]
                z1 = block["static_rsmax"]["Z_re"] + 1j * block["static_rsmax"]["Z_im"]
            for kind in ("static_rs0", "static_rsmax", "osc"):
                if kind not in block:
                    continue
                r = block[kind]
                rel = tau = "NA"
                if kind == "osc" and z0 is not None:
                    m = bracket_metrics(z0, z1, r["Z_re"] + 1j * r["Z_im"])
                    rel = "%.6e" % m["rel"]
                    tau = "%.6f" % m["tau"]
                    metrics.append(dict(f=freq, rel=m["rel"], tau=m["tau"],
                                        Z_re=r["Z_re"], Z_im=r["Z_im"],
                                        Z_mag=r["Z_mag"]))
                f.write("%d\t%s\t%.6e\t%.6e\t%.6e\t%.3f\t%.6e\t%s\t%s\n" %
                        (freq, kind, r["Z_re"], r["Z_im"], r["Z_mag"],
                         r["Z_phase"], r["I_rms"], rel, tau))
    print("Wrote", tsv)

    # |Z| vs f for three kinds
    fig, ax = plt.subplots(figsize=(6.2, 4.0))
    freqs = sorted(by_f)
    for kind, style, label in (
        ("static_rs0", "o-", "static rs0"),
        ("static_rsmax", "s-", "static rsmax"),
        ("osc", "*-", "osc"),
    ):
        xs, ys = [], []
        for freq in freqs:
            if kind in by_f[freq]:
                xs.append(freq / 1e3)
                ys.append(by_f[freq][kind]["Z_mag"])
        if xs:
            ax.plot(xs, ys, style, label=label, markersize=9 if kind == "osc" else 7)
    ax.set_xlabel(r"$f$ (kHz)")
    ax.set_ylabel(r"$|Z|$ ($\Omega$)")
    ax.set_title(r"Sparse-$f$ soft $\Delta r=1$")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8)
    fig.tight_layout()
    p1 = os.path.join(fig_dir, "sparse_f_Zmag.png")
    fig.savefig(p1, dpi=160)
    plt.close(fig)
    print("Wrote", p1)

    # Complex Z colored by frequency
    fig, ax = plt.subplots(figsize=(5.6, 4.4))
    cmap = plt.cm.viridis
    for i, freq in enumerate(freqs):
        block = by_f[freq]
        color = cmap(i / max(1, len(freqs) - 1))
        if "static_rs0" in block and "static_rsmax" in block:
            ax.plot([block["static_rs0"]["Z_re"], block["static_rsmax"]["Z_re"]],
                    [block["static_rs0"]["Z_im"], block["static_rsmax"]["Z_im"]],
                    "--", color=color, alpha=0.5, lw=1)
            ax.plot(block["static_rs0"]["Z_re"], block["static_rs0"]["Z_im"],
                    "o", color=color, markersize=7)
            ax.plot(block["static_rsmax"]["Z_re"], block["static_rsmax"]["Z_im"],
                    "s", color=color, markersize=7)
        if "osc" in block:
            ax.plot(block["osc"]["Z_re"], block["osc"]["Z_im"],
                    "*", color=color, markersize=14,
                    label="%g kHz" % (freq / 1e3))
    ax.set_xlabel(r"Re$\{Z\}$ ($\Omega$)")
    ax.set_ylabel(r"Im$\{Z\}$ ($\Omega$)")
    ax.set_title(r"Sparse-$f$ complex $Z$ (stars = osc)")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8)
    fig.tight_layout()
    p2 = os.path.join(fig_dir, "sparse_f_Z_complex.png")
    fig.savefig(p2, dpi=160)
    plt.close(fig)
    print("Wrote", p2)

    # rel vs f
    if metrics:
        fig, ax = plt.subplots(figsize=(5.5, 3.6))
        ax.plot([m["f"] / 1e3 for m in metrics], [m["rel"] for m in metrics], "o-", color="C3")
        ax.axhline(0.5, color="k", ls=":", alpha=0.4)
        ax.set_xlabel(r"$f$ (kHz)")
        ax.set_ylabel("rel_to_bracket")
        ax.set_title("Out-of-bracket metric vs frequency")
        ax.grid(True, alpha=0.3)
        fig.tight_layout()
        p3 = os.path.join(fig_dir, "sparse_f_rel_to_bracket.png")
        fig.savefig(p3, dpi=160)
        plt.close(fig)
        print("Wrote", p3)

    note = os.path.join(out, "sparse_f_soft_findings.md")
    with open(note, "w") as f:
        f.write("# Sparse frequency soft findings\n\n")
        f.write("**Data:** `results/paper2_sparse_f_soft/` (+ 700 kHz soft pilot)\n\n")
        f.write("| $f$ (kHz) | osc Re$Z$ | osc Im$Z$ | $|Z|$ | rel_to_bracket |\n")
        f.write("|----------:|----------:|----------:|------:|---------------:|\n")
        for m in metrics:
            f.write("| %.0f | %.3e | %.3e | %.3e | **%.3f** |\n" %
                    (m["f"] / 1e3, m["Z_re"], m["Z_im"], m["Z_mag"], m["rel"]))
        f.write("\n## Verdict\n\n")
        if metrics:
            n_out = sum(1 for m in metrics if m["rel"] > 0.5)
            f.write(
                "Out-of-bracket at **%d / %d** sparse frequencies "
                "(threshold rel > 0.5).\n\n" % (n_out, len(metrics))
            )
            if n_out >= 2:
                f.write(
                    "Dynamic loading is **not unique to 700 kHz** under this soft "
                    "$\\Delta r=1$ protocol.\n"
                )
            elif n_out == 1:
                f.write(
                    "Only one frequency sits clearly out-of-bracket; treat "
                    "frequency generality as **unsettled**.\n"
                )
            else:
                f.write(
                    "Sparse set does **not** reproduce a strong out-of-bracket "
                    "signature; revisit numerics / drive band.\n"
                )
        f.write("\n## Figures\n\n")
        f.write("- `figures/sparse_f_Zmag.png`\n")
        f.write("- `figures/sparse_f_Z_complex.png`\n")
        f.write("- `figures/sparse_f_rel_to_bracket.png`\n")
    print("Wrote", note)
    for m in metrics:
        print("f=%.0f kHz rel=%.4f |Z|=%.4e" % (m["f"] / 1e3, m["rel"], m["Z_mag"]))


if __name__ == "__main__":
    main()
