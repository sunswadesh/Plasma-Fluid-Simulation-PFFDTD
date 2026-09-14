"""Paper 1 figures and C_eff tables.

Run from anywhere:
    python projects/tu2008-sheath/paper1_static_sheath_capacitance/analysis/make_ceff_products.py
"""
from __future__ import annotations

import math
import shutil
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch

HERE = Path(__file__).resolve().parent
TU = HERE.parents[1]
P0 = TU / "paper0_sheath_campaign" / "analysis"
FIGDIR = HERE / "figures"
DATADIR = HERE / "data"
DRAFTFIG = HERE.parent / "draft" / "figures"

EPS0 = 8.854187817e-12
DX = 0.04
L = 25 * DX
R_EFF = 0.23 * DX
N_MIN_RATIO = 1e-6
N0_BULK = 4.96e10  # m^-3 at fp = 2 MHz (electrons)
OUTLIER = {(0, 1_500_000)}  # incomplete Sd=0 restart at 1.50 MHz

SD_COLORS = {
    0: "#1f77b4",
    2: "#ff7f0e",
    4: "#2ca02c",
    6: "#d62728",
    8: "#9467bd",
    10: "#8c564b",
}
SD_MARKERS = {0: "o", 2: "s", 4: "D", 6: "^", 8: "v", 10: "P"}


def coax_c(sd: int) -> float:
    return 2.0 * math.pi * EPS0 * L / math.log(1.0 + sd * DX / R_EFF)


def ceff_from_im(freq: float, imz: float) -> float | None:
    if imz >= 0:
        return None
    return -1.0 / (2.0 * math.pi * freq * imz)


def load_rows(path: Path, has_abs: bool) -> list[tuple[int, float, float, float, float]]:
    rows = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            if line.startswith("#") or not line.strip() or line.startswith("Sd"):
                continue
            parts = line.split()
            sd = int(float(parts[0]))
            fr = float(parts[1])
            re = float(parts[2])
            im = float(parts[3])
            az = float(parts[4]) if has_abs else math.hypot(re, im)
            if (sd, int(fr)) in OUTLIER:
                continue
            rows.append((sd, fr, re, im, az))
    return rows


def merge_unique(a, b):
    seen = set()
    out = []
    for row in a + b:
        key = (row[0], int(row[1]))
        if key in seen:
            continue
        seen.add(key)
        out.append(row)
    return sorted(out, key=lambda r: (r[0], r[1]))


def band_mean(pairs: list[tuple[float, float]], f0: float, f1: float):
    vals = [c for f, c in pairs if f0 <= f <= f1]
    if not vals:
        return None
    mean = sum(vals) / len(vals)
    var = sum((c - mean) ** 2 for c in vals) / len(vals)
    return mean, math.sqrt(var), len(vals)


def setup_style():
    plt.rcParams.update(
        {
            "font.size": 10,
            "axes.labelsize": 11,
            "legend.fontsize": 8,
            "axes.grid": True,
            "grid.alpha": 0.28,
            "savefig.bbox": "tight",
            "savefig.dpi": 300,
        }
    )


def save(fig, name: str):
    FIGDIR.mkdir(parents=True, exist_ok=True)
    DRAFTFIG.mkdir(parents=True, exist_ok=True)
    dest = FIGDIR / name
    fig.savefig(dest)
    shutil.copy2(dest, DRAFTFIG / name)
    plt.close(fig)


def fig_geometry():
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.4), gridspec_kw={"width_ratios": [1.05, 1]})

    ax = axes[0]
    ax.set_aspect("equal")
    ax.set_xlim(-6.2, 6.2)
    ax.set_ylim(-6.2, 6.2)
    ax.axis("off")
    ax.set_title("(a) Radial jacket around the conductor")
    plasma = Circle((0, 0), 5.8, facecolor="#d6eaf8", edgecolor="none")
    sheath = Circle((0, 0), 3.1, facecolor="#fff4cc", edgecolor="#b8860b", linewidth=1.4)
    pec = Circle((0, 0), 0.55, facecolor="#333333", edgecolor="k")
    ax.add_patch(plasma)
    ax.add_patch(sheath)
    ax.add_patch(pec)
    ax.annotate(
        "",
        xy=(3.05, 0),
        xytext=(0.58, 0),
        arrowprops=dict(arrowstyle="<->", color="#8b4513", lw=1.6),
    )
    ax.text(1.75, 0.28, r"$S_d\Delta x$", color="#8b4513", ha="center", fontsize=10)
    ax.text(0, 0, "PEC", color="white", ha="center", va="center", fontsize=8)
    ax.text(0, 2.05, "vacuum sheath", ha="center", fontsize=9, color="#6b4f00")
    ax.text(0, 4.55, "bulk plasma", ha="center", fontsize=9, color="#1a5276")
    ax.annotate(
        r"displacement current $I_d$",
        xy=(3.6, 1.4),
        xytext=(4.4, 3.3),
        fontsize=8,
        arrowprops=dict(arrowstyle="->", color="#1a5276"),
        color="#1a5276",
    )
    ax.text(0, -5.7, "Current from metal to plasma must cross the gap.", ha="center", fontsize=8)

    ax = axes[1]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")
    ax.set_title("(b) Series, not shunt, topology")
    feed = FancyBboxPatch((0.4, 2.4), 1.3, 1.2, boxstyle="round,pad=0.08", facecolor="white", edgecolor="k")
    cbox = FancyBboxPatch((3.1, 2.4), 2.4, 1.2, boxstyle="round,pad=0.08", facecolor="#fff4cc", edgecolor="#b8860b")
    zbox = FancyBboxPatch((6.7, 2.4), 2.5, 1.2, boxstyle="round,pad=0.08", facecolor="#d6eaf8", edgecolor="#1a5276")
    ax.add_patch(feed)
    ax.add_patch(cbox)
    ax.add_patch(zbox)
    ax.text(1.05, 3.0, "feed", ha="center", va="center")
    ax.text(4.3, 3.0, r"$1/(j\omega C_{\mathrm{sh}})$", ha="center", va="center")
    ax.text(7.95, 3.0, r"$Z_{\mathrm{pl}}$", ha="center", va="center")
    ax.annotate("", xy=(3.1, 3.0), xytext=(1.7, 3.0), arrowprops=dict(arrowstyle="->", lw=1.4))
    ax.annotate("", xy=(6.7, 3.0), xytext=(5.5, 3.0), arrowprops=dict(arrowstyle="->", lw=1.4))
    ax.text(5.0, 4.55, r"$Z_{\mathrm{in}}\approx Z_{\mathrm{pl}}+1/(j\omega C_{\mathrm{sh}})$", ha="center", fontsize=11)
    ax.text(
        5.0,
        1.15,
        "A shunt capacitor would sit across the feed terminals.\n"
        "The FDTD jacket coats the wire, so the gap is in series\n"
        "with the plasma-loaded antenna.",
        ha="center",
        va="center",
        fontsize=8,
    )
    fig.tight_layout()
    save(fig, "sheath_geometry.png")


def fig_n0_profile():
    fig, ax = plt.subplots(figsize=(6.6, 3.8))
    i = list(range(71))
    n_bulk = [N0_BULK] * 71
    n_sd10 = []
    for ii in i:
        d = abs(ii - 35)
        if d == 0:
            n_sd10.append(N0_BULK)  # PEC cell
        elif 1 <= d <= 10:
            n_sd10.append(N0_BULK * N_MIN_RATIO)
        else:
            n_sd10.append(N0_BULK)
    ax.semilogy(i, n_bulk, color=SD_COLORS[0], lw=2, label=r"$S_d=0$")
    ax.semilogy(i, n_sd10, color=SD_COLORS[10], lw=2, label=r"$S_d=10$")
    ax.axvline(35, color="0.4", ls=":", lw=1, label="dipole")
    ax.set_xlabel("Grid index $i$ through the feed")
    ax.set_ylabel(r"$N_{0,e}$ (m$^{-3}$)")
    ax.set_xlim(0, 70)
    ax.legend(loc="lower right")
    ax.set_title("PEC-seeded vacuum jacket (step depletion)")
    fig.tight_layout()
    save(fig, "n0_radial_profile.png")


def plot_zi(ax_re, ax_im, by_sd, sds, fmin=None, fmax=None):
    for sd in sds:
        pts = by_sd[sd]
        fs = [p[0] / 1e6 for p in pts if (fmin is None or p[0] >= fmin) and (fmax is None or p[0] <= fmax)]
        re = [p[1] for p in pts if (fmin is None or p[0] >= fmin) and (fmax is None or p[0] <= fmax)]
        im = [p[2] for p in pts if (fmin is None or p[0] >= fmin) and (fmax is None or p[0] <= fmax)]
        kw = dict(color=SD_COLORS[sd], marker=SD_MARKERS[sd], ms=5, lw=1.4, label=rf"$S_d={sd}$")
        ax_re.plot(fs, re, **kw)
        ax_im.plot(fs, im, **kw)
    ax_im.axhline(0, color="k", ls="--", lw=0.8)
    ax_re.set_ylabel(r"Re$\{Z\}$ ($\Omega$)")
    ax_im.set_ylabel(r"Im$\{Z\}$ ($\Omega$)")
    ax_im.set_xlabel("Frequency (MHz)")
    ax_re.legend(ncol=2, loc="best")


def fig_z_lowf(by_sd):
    fig, axes = plt.subplots(2, 1, figsize=(7.2, 6.2), sharex=True)
    plot_zi(axes[0], axes[1], by_sd, [0, 2, 10], fmin=0.5e6, fmax=1.4e6)
    axes[0].set_title(r"Low-frequency CW ($S_d=0,2,10$)")
    fig.tight_layout()
    save(fig, "z_lowf.png")


def fig_z_dense(by_sd):
    fig, axes = plt.subplots(2, 1, figsize=(7.2, 6.4), sharex=True)
    plot_zi(axes[0], axes[1], by_sd, [0, 2, 4, 6, 8, 10], fmin=1.5e6, fmax=2.3e6)
    axes[0].set_title(r"Dense CW band, all $S_d$ ($f_p=2$ MHz)")
    fig.tight_layout()
    save(fig, "z_dense.png")


def fig_z_combined(by_sd):
    fig, axes = plt.subplots(2, 1, figsize=(7.2, 6.4), sharex=True)
    plot_zi(axes[0], axes[1], by_sd, [0, 2, 10], fmin=0.5e6, fmax=2.3e6)
    for ax in axes:
        ax.axvspan(0.5, 1.5, color="0.88", zorder=0)
    axes[0].set_title(r"Combined $0.50$–$2.30$ MHz ($S_d=0,2,10$)")
    axes[1].text(1.0, axes[1].get_ylim()[0] * 0.15, "low-$f$ extension", ha="center", fontsize=8, color="0.3")
    fig.tight_layout()
    save(fig, "z_combined.png")


def fig_zabs_dense(by_sd):
    fig, ax = plt.subplots(figsize=(7.0, 3.8))
    for sd in [0, 2, 4, 6, 8, 10]:
        pts = [p for p in by_sd[sd] if 1.5e6 <= p[0] <= 2.3e6]
        ax.plot(
            [p[0] / 1e6 for p in pts],
            [p[3] for p in pts],
            color=SD_COLORS[sd],
            marker=SD_MARKERS[sd],
            ms=5,
            lw=1.4,
            label=rf"$S_d={sd}$",
        )
    ax.set_xlabel("Frequency (MHz)")
    ax.set_ylabel(r"$|Z|$ ($\Omega$)")
    ax.set_title(r"Magnitude marker, dense band")
    ax.legend(ncol=3)
    fig.tight_layout()
    save(fig, "zabs_dense.png")


def fig_fres():
    fig, ax = plt.subplots(figsize=(6.6, 3.9))
    ax.plot([0], [1.846], "o", color=SD_COLORS[0], ms=10, label=r"$S_d=0$: $1.846$ MHz")
    ax.plot([2], [0.655], "s", color=SD_COLORS[2], ms=10, label=r"$S_d=2$: $0.655$ MHz")
    ax.errorbar(
        [4, 6, 8],
        [1.50, 1.50, 1.50],
        yerr=0.12,
        uplims=True,
        fmt="none",
        ecolor="0.25",
        capsize=0,
        label=r"$S_d=4,6,8$: $<1.50$ MHz",
    )
    ax.errorbar(
        [10],
        [0.50],
        yerr=0.08,
        uplims=True,
        fmt="none",
        ecolor=SD_COLORS[10],
        capsize=0,
        label=r"$S_d=10$: $\leq 0.50$ MHz",
    )
    ax.plot([4, 6, 8], [1.50, 1.50, 1.50], "D", color="0.25", ms=7)
    ax.plot([10], [0.50], "P", color=SD_COLORS[10], ms=9)
    ax.set_xlim(-0.5, 10.8)
    ax.set_ylim(0.2, 2.15)
    ax.set_xlabel(r"Sheath width $S_d$ (cells)")
    ax.set_ylabel(r"$f_{\mathrm{res}}$ (MHz)")
    ax.set_title(r"Im$\{Z\}$ $+\to-$ crossing versus $S_d$")
    ax.legend(loc="upper right")
    fig.tight_layout()
    save(fig, "fres_vs_sd.png")


def fig_ceff_freq(ceff_by_sd):
    fig, ax = plt.subplots(figsize=(6.8, 4.0))
    ax.axvspan(0.8, 1.2, color="0.88", zorder=0, label="low-$f$ average window")
    for sd in (2, 10):
        pts = [(f, c) for f, c in ceff_by_sd[sd] if f <= 1.5e6]
        ax.plot(
            [f / 1e6 for f, c in pts],
            [c * 1e12 for f, c in pts],
            marker=SD_MARKERS[sd],
            color=SD_COLORS[sd],
            lw=1.5,
            label=rf"$S_d={sd}$",
        )
    ax.axvline(0.60, color=SD_COLORS[2], ls=":", lw=1)
    ax.text(0.62, 32, r"$S_d=2$ inductive island", fontsize=8, color=SD_COLORS[2])
    ax.set_xlabel("Frequency (MHz)")
    ax.set_ylabel(r"$C_{\mathrm{eff}}$ (pF)")
    ax.set_ylim(0, 40)
    ax.legend()
    fig.tight_layout()
    save(fig, "ceff_vs_frequency.png")


def fig_ceff_sd(lowf_means, high_means):
    fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.0))

    ax = axes[0]
    sds = [2, 4, 6, 8, 10]
    im16 = high_means["im16"]
    ax.plot(sds, [im16[s] for s in sds], "o-", color="#1a5276", ms=8)
    ax.axhline(0, color="k", ls="--", lw=0.8)
    ax.set_xlabel(r"$S_d$ (cells)")
    ax.set_ylabel(r"Im$\{Z\}$ at $1.60$ MHz ($\Omega$)")
    ax.set_title("(a) All dense-band widths")

    ax = axes[1]
    s_cont = list(range(1, 11))
    ax.plot(
        s_cont,
        [coax_c(s) * 1e12 for s in s_cont],
        "k--",
        label=rf"coax $r_{{\mathrm{{eff}}}}=0.23\Delta x$",
    )
    ax.errorbar(
        [2, 10],
        [lowf_means[s][0] * 1e12 for s in (2, 10)],
        yerr=[lowf_means[s][1] * 1e12 for s in (2, 10)],
        fmt="o",
        ms=9,
        color=SD_COLORS[2],
        capsize=3,
        label=r"low-$f$ mean ($0.8$–$1.2$ MHz)",
    )
    ax.plot(
        [4, 6, 8, 10],
        [high_means["ceff17"][s] * 1e12 for s in (4, 6, 8, 10)],
        "D",
        ms=8,
        color=SD_COLORS[4],
        label=r"dense-band mean ($1.50$–$1.70$ MHz)",
    )
    ax.set_xlabel(r"$S_d$ (cells)")
    ax.set_ylabel("Capacitance (pF)")
    ax.set_title(r"(b) $C_{\mathrm{eff}}$ versus coaxial $C_{\mathrm{sh}}$")
    ax.legend(fontsize=7)
    fig.tight_layout()
    save(fig, "ceff_vs_sd.png")
    # Keep the old filename used by the previous draft as an alias.
    shutil.copy2(FIGDIR / "ceff_vs_sd.png", FIGDIR / "ceff_vs_coax.png")
    shutil.copy2(FIGDIR / "ceff_vs_sd.png", DRAFTFIG / "ceff_vs_coax.png")


def write_tables(rows, ceff_by_sd, lowf_means, high_means):
    DATADIR.mkdir(parents=True, exist_ok=True)
    lines = ["# Sd\tFreq_Hz\tRe_Z\tIm_Z\tAbs_Z\tC_eff_pF\n"]
    for sd, fr, re, im, az in rows:
        c = ceff_from_im(fr, im)
        cstr = f"{c*1e12:.6f}" if c is not None else "nan"
        lines.append(f"{sd}\t{fr:.1f}\t{re:.6f}\t{im:.6f}\t{az:.6f}\t{cstr}\n")
    (DATADIR / "ceff_vs_frequency.txt").write_text("".join(lines), encoding="utf-8")

    summary = [
        "# C_eff vs coax. Low-f window 0.8-1.2 MHz (Sd=2,10). Dense window 1.50-1.70 MHz (Sd>=2).\n",
        "# Sd\tt_sh_m\tC_lowf_pF\tC_lowf_std\tn_lowf\tC_dense_pF\tC_dense_std\tn_dense\tC_coax_pF\tratio_lowf\tratio_dense\n",
    ]
    for sd in (2, 4, 6, 8, 10):
        t = sd * DX
        cc = coax_c(sd) * 1e12
        if sd in lowf_means:
            m, s, n = lowf_means[sd]
            low = f"{m*1e12:.4f}\t{s*1e12:.4f}\t{n}"
            rlow = f"{m*1e12/cc:.4f}"
        else:
            low = "nan\tnan\t0"
            rlow = "nan"
        if sd in high_means["ceff17_full"]:
            m, s, n = high_means["ceff17_full"][sd]
            dense = f"{m*1e12:.4f}\t{s*1e12:.4f}\t{n}"
            rden = f"{m*1e12/cc:.4f}"
        else:
            dense = "nan\tnan\t0"
            rden = "nan"
        summary.append(f"{sd}\t{t:.4f}\t{low}\t{dense}\t{cc:.4f}\t{rlow}\t{rden}\n")
    (DATADIR / "ceff_vs_coax_summary.txt").write_text("".join(summary), encoding="utf-8")

    (DATADIR / "fres_summary.txt").write_text(
        "# Sd\tf_res_MHz\tnote\n"
        "0\t1.846\tIm +to- in dense band\n"
        "2\t0.655\tIm +to- in low-f band\n"
        "4\t<1.50\tall Im<0 in dense band; no low-f run\n"
        "6\t<1.50\tall Im<0 in dense band; no low-f run\n"
        "8\t<1.50\tall Im<0 in dense band; no low-f run\n"
        "10\t<=0.50\tall Im<0 in 0.50-2.30 MHz\n",
        encoding="utf-8",
    )


def main():
    setup_style()
    lowf = load_rows(P0 / "data" / "cw_lowf_summary.txt", has_abs=True)
    dense = load_rows(P0 / "data" / "cw_tu_summary.txt", has_abs=False)
    rows = merge_unique(lowf, dense)

    by_sd = {sd: [] for sd in (0, 2, 4, 6, 8, 10)}
    ceff_by_sd = {sd: [] for sd in (0, 2, 4, 6, 8, 10)}
    for sd, fr, re, im, az in rows:
        by_sd[sd].append((fr, re, im, az))
        c = ceff_from_im(fr, im)
        if c is not None:
            ceff_by_sd[sd].append((fr, c))

    lowf_means = {}
    for sd in (2, 10):
        stats = band_mean(ceff_by_sd[sd], 0.8e6, 1.2e6)
        if stats:
            lowf_means[sd] = stats

    high_means = {"im16": {}, "ceff17": {}, "ceff17_full": {}}
    for sd in (2, 4, 6, 8, 10):
        im16 = [im for f, re, im, az in by_sd[sd] if abs(f - 1.6e6) < 1]
        if im16:
            high_means["im16"][sd] = im16[0]
        stats = band_mean(ceff_by_sd[sd], 1.5e6, 1.7e6)
        if stats:
            high_means["ceff17_full"][sd] = stats
            if sd != 2:
                high_means["ceff17"][sd] = stats[0]
            else:
                # Sd=2 dense-band C_eff is inflated (Im Z approaching 0); omit from overlay.
                pass
        if sd == 10 and stats:
            high_means["ceff17"][sd] = stats[0]

    fig_geometry()
    fig_n0_profile()
    fig_z_lowf(by_sd)
    fig_z_dense(by_sd)
    fig_z_combined(by_sd)
    fig_zabs_dense(by_sd)
    fig_fres()
    fig_ceff_freq(ceff_by_sd)
    fig_ceff_sd(lowf_means, high_means)
    write_tables(rows, ceff_by_sd, lowf_means, high_means)

    print("Low-f C_eff (0.8-1.2 MHz):")
    for sd, (m, s, n) in lowf_means.items():
        print(f"  Sd={sd}: {m*1e12:.2f} +/- {s*1e12:.2f} pF (n={n}); coax={coax_c(sd)*1e12:.2f}")
    print("Dense-band C_eff (1.50-1.70 MHz):")
    for sd, (m, s, n) in high_means["ceff17_full"].items():
        note = "  [near Im~0]" if sd == 2 else ""
        print(f"  Sd={sd}: {m*1e12:.2f} +/- {s*1e12:.2f} pF (n={n}); coax={coax_c(sd)*1e12:.2f}{note}")
    print("Wrote", FIGDIR)
    print("Copied to", DRAFTFIG)


if __name__ == "__main__":
    main()
