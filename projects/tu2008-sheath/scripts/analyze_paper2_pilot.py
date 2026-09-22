"""Analyze Paper 2 rs(t) pilot: static brackets vs oscillating sheath.

Reads results/paper2_rs_t_pilot/{static_rs0,static_rsmax,osc_rs_t}/data.vc
Writes tables/figures under paper2_oscillating_sheath_boundary/analysis/
and a short findings note for the manuscript.
"""
from __future__ import print_function

import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from paths import pffdtd_root, project_root

CASES = [
    ("static_rs0", "static $r_{s0}=4$"),
    ("static_rsmax", "static $r_{s0}+1=5$"),
    ("osc_rs_t", "oscillating $\\Delta r=1$"),
]
F_DRIVE = 700000.0
TRIM_FRAC = 0.5  # use last half for phasors


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
    return np.asarray(times), np.asarray(volts), np.asarray(currents)


def extract_phasor(t, signal, f):
    dt = t[1] - t[0]
    return np.sum(signal * np.exp(-1j * 2 * np.pi * f * t)) * dt


def rms(x):
    return float(np.sqrt(np.mean(x * x)))


def main():
    import argparse
    ap = argparse.ArgumentParser(description="Analyze Paper 2 rs(t) pilot")
    ap.add_argument("--results", default="paper2_rs_t_pilot",
                    help="subdir under results/ (default paper2_rs_t_pilot)")
    ap.add_argument("--tag", default="",
                    help="suffix for output files (e.g. soft)")
    ap.add_argument("--freq", type=float, default=F_DRIVE)
    args = ap.parse_args()
    f_drive = args.freq
    tag = ("_" + args.tag) if args.tag else ""

    root = pffdtd_root()
    base = os.path.join(root, "results", args.results)
    out_dir = os.path.join(project_root(), "paper2_oscillating_sheath_boundary", "analysis")
    fig_dir = os.path.join(out_dir, "figures")
    data_dir = os.path.join(out_dir, "data")
    os.makedirs(fig_dir, exist_ok=True)
    os.makedirs(data_dir, exist_ok=True)

    rows = []
    series = {}

    for name, label in CASES:
        vc = os.path.join(base, name, "data.vc")
        if not os.path.isfile(vc):
            print("MISSING", vc)
            continue
        t, v, i = robust_load_vc(vc)
        if len(t) < 100:
            print("TOO SHORT", name, len(t))
            continue
        n0 = int(len(t) * TRIM_FRAC)
        t_ss, v_ss, i_ss = t[n0:], v[n0:], i[n0:]
        V = extract_phasor(t_ss, v_ss, f_drive)
        I = extract_phasor(t_ss, i_ss, f_drive)
        Z = V / I if abs(I) > 0 else np.nan + 1j * np.nan
        rows.append({
            "name": name,
            "label": label,
            "n": len(t),
            "t_end": float(t[-1]),
            "V_amp": abs(V),
            "I_amp": abs(I),
            "V_phase_deg": float(np.angle(V, deg=True)),
            "I_phase_deg": float(np.angle(I, deg=True)),
            "Z_re": float(np.real(Z)),
            "Z_im": float(np.imag(Z)),
            "Z_mag": float(abs(Z)),
            "Z_phase_deg": float(np.angle(Z, deg=True)),
            "V_rms": rms(v_ss),
            "I_rms": rms(i_ss),
        })
        series[name] = (t, v, i, t_ss, v_ss, i_ss)

    if not rows:
        print("No usable cases")
        sys.exit(1)

    # Table
    table_path = os.path.join(data_dir, "pilot_phasor_Z%s.tsv" % tag)
    with open(table_path, "w") as f:
        f.write("case\tReZ_ohm\tImZ_ohm\t|Z|_ohm\targZ_deg\t|V|\t|I|\tVrms\tIrms\tt_end_s\tn\n")
        for r in rows:
            f.write(
                "{name}\t{Z_re:.6e}\t{Z_im:.6e}\t{Z_mag:.6e}\t{Z_phase_deg:.3f}\t"
                "{V_amp:.6e}\t{I_amp:.6e}\t{V_rms:.6e}\t{I_rms:.6e}\t{t_end:.6e}\t{n}\n".format(**r)
            )
    print("Wrote", table_path)

    by = {r["name"]: r for r in rows}
    findings = []
    if all(k in by for k in ("static_rs0", "static_rsmax", "osc_rs_t")):
        z0 = by["static_rs0"]["Z_re"] + 1j * by["static_rs0"]["Z_im"]
        z1 = by["static_rsmax"]["Z_re"] + 1j * by["static_rsmax"]["Z_im"]
        zo = by["osc_rs_t"]["Z_re"] + 1j * by["osc_rs_t"]["Z_im"]
        z_mid = 0.5 * (z0 + z1)
        d_brackets = abs(z1 - z0)
        d_osc_mid = abs(zo - z_mid)
        d_osc_0 = abs(zo - z0)
        d_osc_1 = abs(zo - z1)
        w = z1 - z0
        if abs(w) > 0:
            tau = np.real(np.conj(w) * (zo - z0)) / (abs(w) ** 2)
            tau_c = min(1.0, max(0.0, tau))
            z_proj = z0 + tau_c * w
            d_to_seg = abs(zo - z_proj)
        else:
            tau = float("nan")
            d_to_seg = abs(zo - z0)
        findings.append(
            {
                "d_brackets": d_brackets,
                "d_osc_mid": d_osc_mid,
                "d_osc_0": d_osc_0,
                "d_osc_1": d_osc_1,
                "d_to_seg": d_to_seg,
                "tau": tau,
                "rel_to_bracket": d_to_seg / d_brackets if d_brackets > 0 else float("nan"),
            }
        )
        metric_path = os.path.join(data_dir, "pilot_deltaZ_metrics%s.tsv" % tag)
        with open(metric_path, "w") as f:
            f.write("d_brackets\td_osc_to_mid\td_osc_to_rs0\td_osc_to_rsmax\td_osc_to_segment\ttau_proj\trel_to_bracket\n")
            m = findings[0]
            f.write(
                "{d_brackets:.6e}\t{d_osc_mid:.6e}\t{d_osc_0:.6e}\t{d_osc_1:.6e}\t"
                "{d_to_seg:.6e}\t{tau:.6f}\t{rel_to_bracket:.6e}\n".format(**m)
            )
        print("Wrote", metric_path)

    # Complex Z scatter
    fig, ax = plt.subplots(figsize=(5.2, 4.2))
    colors = {"static_rs0": "C0", "static_rsmax": "C1", "osc_rs_t": "C3"}
    markers = {"static_rs0": "o", "static_rsmax": "s", "osc_rs_t": "*"}
    for r in rows:
        ax.plot(
            r["Z_re"], r["Z_im"],
            markers[r["name"]], color=colors[r["name"]],
            markersize=12 if r["name"] == "osc_rs_t" else 9,
            label=r["name"],
        )
    if all(k in by for k in ("static_rs0", "static_rsmax")):
        ax.plot(
            [by["static_rs0"]["Z_re"], by["static_rsmax"]["Z_re"]],
            [by["static_rs0"]["Z_im"], by["static_rsmax"]["Z_im"]],
            "k--", lw=1, alpha=0.5, label="static bracket",
        )
    ax.set_xlabel(r"Re$\{Z\}$ ($\Omega$)")
    ax.set_ylabel(r"Im$\{Z\}$ ($\Omega$)")
    title = r"Paper 2 phasor $Z$ at $f=%.0f$ kHz" % (f_drive / 1e3)
    if args.tag:
        title += " [%s]" % args.tag
    ax.set_title(title)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8)
    fig.tight_layout()
    zpath = os.path.join(fig_dir, "pilot_Z_complex%s.png" % tag)
    fig.savefig(zpath, dpi=160)
    plt.close(fig)
    print("Wrote", zpath)

    # Late-time V/I overlay (last few cycles)
    fig, axes = plt.subplots(2, 1, figsize=(7.2, 5.0), sharex=True)
    t_win = 5.0 / f_drive
    for name, label in CASES:
        if name not in series:
            continue
        t, v, i, t_ss, v_ss, i_ss = series[name]
        t0 = t_ss[-1] - t_win
        m = t_ss >= t0
        axes[0].plot(t_ss[m] * 1e6, v_ss[m], label=name, color=colors[name], lw=1.1)
        axes[1].plot(t_ss[m] * 1e6, i_ss[m] * 1e6, label=name, color=colors[name], lw=1.1)
    axes[0].set_ylabel("$V$ (V)")
    axes[1].set_ylabel("$I$ ($\\mu$A)")
    axes[1].set_xlabel("$t$ ($\\mu$s)")
    axes[0].set_title("Last ~5 drive cycles" + ((" [%s]" % args.tag) if args.tag else ""))
    axes[0].legend(fontsize=8, loc="upper right")
    axes[0].grid(True, alpha=0.3)
    axes[1].grid(True, alpha=0.3)
    fig.tight_layout()
    tpath = os.path.join(fig_dir, "pilot_VI_last_cycles%s.png" % tag)
    fig.savefig(tpath, dpi=160)
    plt.close(fig)
    print("Wrote", tpath)

    # Bar chart |Z|, Re, Im
    fig, ax = plt.subplots(figsize=(6.0, 3.8))
    names = [r["name"] for r in rows]
    x = np.arange(len(names))
    wbar = 0.25
    ax.bar(x - wbar, [r["Z_re"] for r in rows], wbar, label="Re Z")
    ax.bar(x, [r["Z_im"] for r in rows], wbar, label="Im Z")
    ax.bar(x + wbar, [r["Z_mag"] for r in rows], wbar, label="|Z|")
    ax.set_xticks(x)
    ax.set_xticklabels(names, rotation=15)
    ax.set_ylabel(r"$Z$ ($\Omega$)")
    ax.set_title(r"Phasor components" + ((" [%s]" % args.tag) if args.tag else ""))
    ax.legend(fontsize=8)
    ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    bpath = os.path.join(fig_dir, "pilot_Z_bars%s.png" % tag)
    fig.savefig(bpath, dpi=160)
    plt.close(fig)
    print("Wrote", bpath)

    # Findings markdown
    note = os.path.join(out_dir, "pilot_findings%s.md" % tag)
    with open(note, "w") as f:
        f.write("# Paper 2 pilot findings%s\n\n" % ((" (%s)" % args.tag) if args.tag else ""))
        f.write("**Data:** `results/%s/`  \n" % args.results)
        f.write("**Drive:** $f=%.0f$ kHz  \n" % (f_drive / 1e3))
        f.write("**Method:** phasor $Z=V/I$ on last 50%% of `.vc` traces.\n\n")
        f.write("## Phasor table\n\n")
        f.write("| Case | Re$Z$ ($\\Omega$) | Im$Z$ ($\\Omega$) | $|Z|$ | arg$Z$ (deg) |\n")
        f.write("|------|----------------:|----------------:|------:|-------------:|\n")
        for r in rows:
            f.write(
                "| `{name}` | {Z_re:.3e} | {Z_im:.3e} | {Z_mag:.3e} | {Z_phase_deg:.2f} |\n".format(**r)
            )
        f.write("\n## Bracket test\n\n")
        if findings:
            m = findings[0]
            f.write(
                "Complex-plane distance between static brackets: "
                "$|Z_5-Z_4|=%.4e\\,\\Omega$.\n\n" % m["d_brackets"]
            )
            f.write(
                "Oscillating case distance to bracket segment: "
                "$%.4e\\,\\Omega$ (fraction of bracket span: **%.3f**).\n\n"
                % (m["d_to_seg"], m["rel_to_bracket"])
            )
            f.write(
                "Projection parameter $\\tau$ along $Z_4\\to Z_5$: **%.3f**.\n\n" % m["tau"]
            )
            if m["rel_to_bracket"] < 0.05 and 0.0 <= m["tau"] <= 1.0:
                verdict = (
                    "The oscillating phasor lies **on/near the static bracket segment** "
                    "(quasi-static thickness sampling)."
                )
            elif m["rel_to_bracket"] < 0.15 and 0.0 <= m["tau"] <= 1.0:
                verdict = (
                    "The oscillating phasor is **close to the static bracket line** "
                    "with modest residual."
                )
            else:
                verdict = (
                    "The oscillating phasor is **offset from the static bracket segment**, "
                    "consistent with a kinematic/moving-boundary contribution beyond "
                    "quasi-static $S_d$ alone."
                )
            f.write("**Verdict:** " + verdict + "\n\n")
        f.write("## Figures\n\n")
        f.write("- `figures/pilot_Z_complex%s.png`\n" % tag)
        f.write("- `figures/pilot_Z_bars%s.png`\n" % tag)
        f.write("- `figures/pilot_VI_last_cycles%s.png`\n" % tag)
    print("Wrote", note)
    for r in rows:
        print(
            "{name}: Z={Z_re:.4e}+j{Z_im:.4e} |Z|={Z_mag:.4e} arg={Z_phase_deg:.2f} deg".format(**r)
        )
    if findings:
        print("rel_to_bracket=%.4f tau=%.4f" % (findings[0]["rel_to_bracket"], findings[0]["tau"]))


if __name__ == "__main__":
    main()
