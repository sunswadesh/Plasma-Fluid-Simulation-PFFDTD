"""Analyze Paper 2 soft phase scan at fixed f=700 kHz, Delta-r=1.

Combines phi=0 from soft pilot with results/paper2_phase_scan_soft/osc_phi*.
Writes tables/figures and phase_scan_soft_findings.md.
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

F_DRIVE = 700000.0
TRIM = 0.5


def phasor_row(name, phi, path):
    t, v, i = robust_load_vc(path)
    if len(t) < 100 or float(t[-1]) < 2.0e-5:
        return None
    n0 = int(len(t) * TRIM)
    t_ss, v_ss, i_ss = t[n0:], v[n0:], i[n0:]
    V = extract_phasor(t_ss, v_ss, F_DRIVE)
    I = extract_phasor(t_ss, i_ss, F_DRIVE)
    Z = V / I if abs(I) > 0 else np.nan + 1j * np.nan
    return dict(
        name=name, phi=phi,
        Z_re=float(np.real(Z)), Z_im=float(np.imag(Z)),
        Z_mag=float(abs(Z)), Z_phase=float(np.angle(Z, deg=True)),
        I_phase=float(np.angle(I, deg=True)),
        V_phase=float(np.angle(V, deg=True)),
        I_rms=rms(i_ss),
        t_ss=t_ss, i_ss=i_ss, v_ss=v_ss,
    )


def main():
    root = pffdtd_root()
    soft_pilot = os.path.join(root, "results", "paper2_rs_t_pilot_soft")
    sens = os.path.join(root, "results", "paper2_phase_scan_soft")
    out = os.path.join(project_root(), "paper2_oscillating_sheath_boundary", "analysis")
    fig_dir = os.path.join(out, "figures")
    data_dir = os.path.join(out, "data")
    os.makedirs(fig_dir, exist_ok=True)
    os.makedirs(data_dir, exist_ok=True)

    z0 = z1 = None
    for kind, sub in (("static_rs0", "static_rs0"), ("static_rsmax", "static_rsmax")):
        vc = os.path.join(soft_pilot, sub, "data.vc")
        r = phasor_row(kind, None, vc)
        if r is None:
            print("Missing static", vc)
            sys.exit(1)
        if kind == "static_rs0":
            z0 = r["Z_re"] + 1j * r["Z_im"]
        else:
            z1 = r["Z_re"] + 1j * r["Z_im"]

    osc = []
    vc0 = os.path.join(soft_pilot, "osc_rs_t", "data.vc")
    r0 = phasor_row("osc_phi0", 0.0, vc0)
    if r0 is not None:
        osc.append(r0)

    if os.path.isdir(sens):
        for name in sorted(os.listdir(sens)):
            m = re.match(r"osc_phi(\d+)$", name)
            if not m:
                continue
            phi = float(m.group(1))
            vc = os.path.join(sens, name, "data.vc")
            if not os.path.isfile(vc):
                continue
            r = phasor_row(name, phi, vc)
            if r is None:
                print("SKIP incomplete", name)
                continue
            osc.append(r)

    osc.sort(key=lambda r: r["phi"])
    if len(osc) < 2:
        print("Need at least 2 phase points")
        sys.exit(1)

    tsv = os.path.join(data_dir, "phase_scan_soft_phasor_Z.tsv")
    with open(tsv, "w") as f:
        f.write("phi_deg\tReZ\tImZ\tAbsZ\targZ_deg\tIrms\trel_to_bracket\ttau\n")
        for r in osc:
            zo = r["Z_re"] + 1j * r["Z_im"]
            m = bracket_metrics(z0, z1, zo)
            f.write("%.1f\t%.6e\t%.6e\t%.6e\t%.3f\t%.6e\t%.6e\t%.6f\n" %
                    (r["phi"], r["Z_re"], r["Z_im"], r["Z_mag"], r["Z_phase"],
                     r["I_rms"], m["rel"], m["tau"]))
    print("Wrote", tsv)

    fig, ax = plt.subplots(figsize=(5.6, 4.4))
    ax.plot([np.real(z0), np.real(z1)], [np.imag(z0), np.imag(z1)],
            "k--", lw=1, alpha=0.5, label="static bracket")
    ax.plot(np.real(z0), np.imag(z0), "o", color="C0", markersize=8)
    ax.plot(np.real(z1), np.imag(z1), "s", color="C1", markersize=8)
    for r in osc:
        ax.plot(r["Z_re"], r["Z_im"], "*", markersize=12,
                label=r"$\phi=%g^\circ$" % r["phi"])
    ax.set_xlabel(r"Re$\{Z\}$ ($\Omega$)")
    ax.set_ylabel(r"Im$\{Z\}$ ($\Omega$)")
    ax.set_title(r"Phase scan soft ($\Delta r=1$, $f=700$ kHz)")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=7)
    fig.tight_layout()
    p1 = os.path.join(fig_dir, "phase_scan_Z_complex.png")
    fig.savefig(p1, dpi=160)
    plt.close(fig)
    print("Wrote", p1)

    phis = [r["phi"] for r in osc]
    args = [r["Z_phase"] for r in osc]
    rels = [bracket_metrics(z0, z1, r["Z_re"] + 1j * r["Z_im"])["rel"] for r in osc]
    fig, axes = plt.subplots(1, 2, figsize=(7.5, 3.4))
    axes[0].plot(phis, args, "o-", color="C3")
    axes[0].set_xlabel(r"$\phi$ (deg)")
    axes[0].set_ylabel(r"arg$(Z)$ (deg)")
    axes[0].set_title("Feed phase vs boundary phase")
    axes[0].grid(True, alpha=0.3)
    axes[1].plot(phis, rels, "o-", color="C0")
    axes[1].set_xlabel(r"$\phi$ (deg)")
    axes[1].set_ylabel("rel_to_bracket")
    axes[1].set_title("Out-of-bracket vs phase")
    axes[1].grid(True, alpha=0.3)
    fig.tight_layout()
    p2 = os.path.join(fig_dir, "phase_scan_metrics.png")
    fig.savefig(p2, dpi=160)
    plt.close(fig)
    print("Wrote", p2)

    # Harmonic content of I for each phi
    fig, ax = plt.subplots(figsize=(6.2, 3.8))
    for r in osc:
        i = r["i_ss"]
        dt = r["t_ss"][1] - r["t_ss"][0]
        n = len(i)
        freqs = np.fft.rfftfreq(n, dt)
        amp = np.abs(np.fft.rfft(i)) * 2.0 / n
        # power at f, 2f, 3f
        def band(f0):
            j = np.argmin(np.abs(freqs - f0))
            return float(amp[j])
        ax.plot([1, 2, 3], [band(F_DRIVE), band(2 * F_DRIVE), band(3 * F_DRIVE)],
                "o-", label=r"$\phi=%g$" % r["phi"])
    ax.set_xticks([1, 2, 3])
    ax.set_xticklabels(["f", "2f", "3f"])
    ax.set_ylabel(r"$|I|$ harmonic amp (A)")
    ax.set_title("Late-time current harmonics")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=7)
    fig.tight_layout()
    p3 = os.path.join(fig_dir, "phase_scan_I_harmonics.png")
    fig.savefig(p3, dpi=160)
    plt.close(fig)
    print("Wrote", p3)

    note = os.path.join(out, "phase_scan_soft_findings.md")
    with open(note, "w") as f:
        f.write("# Soft phase scan findings ($f=700$ kHz, $\\Delta r=1$)\n\n")
        f.write("| $\\phi$ (deg) | Re$Z$ | Im$Z$ | arg$Z$ | rel_to_bracket |\n")
        f.write("|-------------:|------:|------:|-------:|---------------:|\n")
        for r in osc:
            m = bracket_metrics(z0, z1, r["Z_re"] + 1j * r["Z_im"])
            f.write("| %.0f | %.3e | %.3e | %.2f | **%.3f** |\n" %
                    (r["phi"], r["Z_re"], r["Z_im"], r["Z_phase"], m["rel"]))
        arg_span = max(args) - min(args)
        f.write("\n## Verdict\n\n")
        f.write("arg$(Z)$ span across $\\phi$: **%.2f deg**.\n\n" % arg_span)
        if arg_span > 10.0:
            f.write(
                "Feed phase moves systematically with boundary phase "
                "(span > 10 deg) -> coherent coupling more plausible.\n"
            )
        else:
            f.write(
                "Feed phase barely tracks $\\phi$ "
                "(span <= 10 deg) -> caution toward amplitude-only agitation.\n"
            )
        f.write("\n## Figures\n\n")
        f.write("- `figures/phase_scan_Z_complex.png`\n")
        f.write("- `figures/phase_scan_metrics.png`\n")
        f.write("- `figures/phase_scan_I_harmonics.png`\n")
    print("Wrote", note)
    for r in osc:
        m = bracket_metrics(z0, z1, r["Z_re"] + 1j * r["Z_im"])
        print("phi=%.0f argZ=%.2f rel=%.3f" % (r["phi"], r["Z_phase"], m["rel"]))


if __name__ == "__main__":
    main()
