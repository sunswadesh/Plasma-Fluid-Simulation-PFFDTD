"""Paper 1 figures and tables (review revision).

Primary observables:
  - dense-band Z(f) ordering with Sd
  - Im{Z}(Sd) at fixed frequencies (including near-fp reversal)
  - dipole coaxial C_sh (two arms in series), not Liu monopole
  - circuit overlay Z_pl(Sd=0) + 1/(j omega C_dipole)
  - optional C_eff as a mixed diagnostic only

Run from repo root:
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
L = 25 * DX  # total dipole length (m)
R_EFF = 0.23 * DX
R_STAIR = 0.5 * DX
N_MIN_RATIO = 1e-6
N0_BULK = 4.0 * math.pi**2 * (2e6) ** 2 * 9.1066e-31 * EPS0 / (1.6021917e-19) ** 2
OUTLIER = {(0, 1_500_000)}

SD_COLORS = {
    0: "#1f77b4",
    2: "#ff7f0e",
    4: "#2ca02c",
    6: "#d62728",
    8: "#9467bd",
    10: "#8c564b",
}
SD_MARKERS = {0: "o", 2: "s", 4: "D", 6: "^", 8: "v", 10: "P"}


def coax_monopole(sd: int, r_eff: float = R_EFF) -> float:
    """Liu-style monopole coax (wrong object for this center-fed dipole)."""
    return 2.0 * math.pi * EPS0 * L / math.log(1.0 + sd * DX / r_eff)


def coax_dipole(sd: int, r_eff: float = R_EFF) -> float:
    """Two arms of length L/2 in series: C_feed = C_arm/2 = C_monopole/4."""
    return coax_monopole(sd, r_eff) / 4.0


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


def load_from_paper1_table(path: Path) -> list[tuple[int, float, float, float, float]]:
    """Self-contained fallback: Sd, Freq, Re, Im, Abs[, C_eff]."""
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
            az = float(parts[4])
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
        "Pedagogical series circuit only.\n"
        "Measured Re{Z}(Sd) shows Z_pl also changes\n"
        "when the jacket removes near-wire plasma.",
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
            n_sd10.append(float("nan"))  # PEC cell: no plasma density
        elif 1 <= d <= 10:
            n_sd10.append(N0_BULK * N_MIN_RATIO)
        else:
            n_sd10.append(N0_BULK)
    ax.semilogy(i, n_bulk, color=SD_COLORS[0], lw=2, label=r"$S_d=0$")
    ax.semilogy(i, n_sd10, color=SD_COLORS[10], lw=2, label=r"$S_d=10$ (schematic)")
    ax.axvline(35, color="0.4", ls=":", lw=1, label="dipole")
    ax.set_xlabel("Grid index $i$ through the feed")
    ax.set_ylabel(r"$N_{0,e}$ (m$^{-3}$)")
    ax.set_xlim(0, 70)
    ax.legend(loc="lower right")
    ax.set_title("Schematic PEC-seeded vacuum jacket (not a dumped field)")
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
    axes[1].axvspan(1.5, 1.8, color="#e8f5e9", zorder=0, alpha=0.7)
    axes[1].text(1.65, axes[1].get_ylim()[0] * 0.08, "series-C ordering", ha="center", fontsize=8, color="#1b5e20")
    axes[1].text(2.1, axes[1].get_ylim()[0] * 0.08, "plasma-feature reversal", ha="center", fontsize=8, color="#b71c1c")
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
    fig, ax = plt.subplots(figsize=(6.8, 4.0))
    ax.plot([0], [1.846], "o", color=SD_COLORS[0], ms=10, label=r"$S_d=0$: $1.846$ MHz (plasma-loaded)")
    ax.plot([2], [0.655], "s", color=SD_COLORS[2], ms=10, label=r"$S_d=2$: $0.655$ MHz (single inductive sample)")
    # Upper limits plotted at the bound with downward arrows; do not invent values below.
    ax.errorbar(
        [4, 6, 8],
        [1.50, 1.50, 1.50],
        yerr=[[0.55, 0.55, 0.55], [0, 0, 0]],
        uplims=True,
        fmt="D",
        color="0.35",
        ms=7,
        ecolor="0.35",
        capsize=0,
        label=r"$S_d=4,6,8$: upper bound $<1.50$ MHz only",
    )
    ax.errorbar(
        [10],
        [0.50],
        yerr=[[0.18], [0]],
        uplims=True,
        fmt="P",
        color=SD_COLORS[10],
        ms=9,
        ecolor=SD_COLORS[10],
        capsize=0,
        label=r"$S_d=10$: upper bound $\leq 0.50$ MHz",
    )
    ax.axhline(1.50, color="0.7", ls=":", lw=1)
    ax.set_xlim(-0.5, 10.8)
    ax.set_ylim(0.15, 2.15)
    ax.set_xlabel(r"Sheath width $S_d$ (cells)")
    ax.set_ylabel(r"$f_{\mathrm{res}}$ (MHz)")
    ax.set_title(r"Im$\{Z\}$ $+\to-$ crossings (bounds are not slope points)")
    ax.legend(loc="upper right", fontsize=7)
    fig.tight_layout()
    save(fig, "fres_vs_sd.png")


def fig_im_vs_sd(by_sd):
    """Primary loading evidence: Im{Z}(Sd) at fixed frequencies."""
    fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.0))
    sds = [2, 4, 6, 8, 10]

    ax = axes[0]
    for f_mhz, ls in ((1.60, "-"), (1.70, "--"), (1.80, ":")):
        ims = []
        for sd in sds:
            pts = [p for p in by_sd[sd] if abs(p[0] - f_mhz * 1e6) < 1]
            ims.append(pts[0][2] if pts else float("nan"))
        ax.plot(sds, ims, marker="o", ls=ls, ms=7, label=rf"{f_mhz:.2f} MHz")
    ax.axhline(0, color="k", ls="--", lw=0.8)
    ax.set_xlabel(r"$S_d$ (cells)")
    ax.set_ylabel(r"Im$\{Z\}$ ($\Omega$)")
    ax.set_title(r"(a) Low dense band: thicker $\Rightarrow$ more capacitive")
    ax.legend()

    ax = axes[1]
    for f_mhz, ls in ((2.00, "-"), (2.10, "--"), (2.20, ":")):
        ims = []
        for sd in [0] + sds:
            pts = [p for p in by_sd[sd] if abs(p[0] - f_mhz * 1e6) < 1]
            ims.append(pts[0][2] if pts else float("nan"))
        ax.plot([0] + sds, ims, marker="o", ls=ls, ms=6, label=rf"{f_mhz:.2f} MHz")
    ax.axhline(0, color="k", ls="--", lw=0.8)
    ax.set_xlabel(r"$S_d$ (cells)")
    ax.set_ylabel(r"Im$\{Z\}$ ($\Omega$)")
    ax.set_title(r"(b) Near $f_p$: ordering reverses (plasma feature)")
    ax.legend()
    fig.tight_layout()
    save(fig, "imz_vs_sd.png")


def fig_ceff_freq(ceff_by_sd):
    fig, ax = plt.subplots(figsize=(6.8, 4.0))
    ax.axvspan(0.8, 1.2, color="0.88", zorder=0, label="diagnostic window (not flat)")
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
    ax.text(0.62, 32, r"$S_d=2$ inductive sample", fontsize=8, color=SD_COLORS[2])
    ax.set_xlabel("Frequency (MHz)")
    ax.set_ylabel(r"$C_{\mathrm{eff}}=-1/(\omega\mathrm{Im}\{Z\})$ (pF)")
    ax.set_ylim(0, 40)
    ax.set_title(r"$C_{\mathrm{eff}}(f)$ is mixed and frequency-dependent")
    ax.legend()
    fig.tight_layout()
    save(fig, "ceff_vs_frequency.png")


def fig_ceff_sd(lowf_means):
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.1))

    ax = axes[0]
    s_cont = list(range(1, 11))
    ax.plot(
        s_cont,
        [coax_monopole(s) * 1e12 for s in s_cont],
        "k--",
        lw=1.2,
        label=r"monopole $C_{\mathrm{sh}}$ (Liu form)",
    )
    ax.plot(
        s_cont,
        [coax_dipole(s) * 1e12 for s in s_cont],
        "k-",
        lw=1.8,
        label=r"dipole $C_{\mathrm{sh}}=C_{\mathrm{mono}}/4$",
    )
    ax.plot(
        s_cont,
        [coax_dipole(s, R_STAIR) * 1e12 for s in s_cont],
        color="0.45",
        ls=":",
        lw=1.4,
        label=r"dipole, $r_{\mathrm{eff}}=0.5\Delta x$",
    )
    if lowf_means:
        ax.errorbar(
            [2, 10],
            [lowf_means[s][0] * 1e12 for s in (2, 10)],
            yerr=[lowf_means[s][1] * 1e12 for s in (2, 10)],
            fmt="o",
            ms=9,
            color=SD_COLORS[2],
            capsize=3,
            label=r"band $C_{\mathrm{eff}}$ $0.8$–$1.2$ MHz (diagnostic)",
        )
    ax.set_xlabel(r"$S_d$ (cells)")
    ax.set_ylabel("Capacitance (pF)")
    ax.set_title(r"(a) Analytic coax: monopole vs dipole")
    ax.legend(fontsize=7)

    ax = axes[1]
    # Ratio to dipole coax in the diagnostic window
    if lowf_means:
        for sd in (2, 10):
            m, s, _ = lowf_means[sd]
            cd = coax_dipole(sd)
            ax.errorbar(
                [sd],
                [m / cd],
                yerr=[s / cd],
                fmt=SD_MARKERS[sd],
                color=SD_COLORS[sd],
                ms=10,
                capsize=3,
                label=rf"$S_d={sd}$: $C_{{\mathrm{{eff}}}}/C_{{\mathrm{{dip}}}}$",
            )
        ax.axhline(1.0, color="k", ls="--", lw=1, label="unity (dipole formula)")
        ax.axhline(0.25, color="0.5", ls=":", lw=1, label="monopole would look like ~0.25")
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 1.6)
    ax.set_xlabel(r"$S_d$ (cells)")
    ax.set_ylabel(r"$C_{\mathrm{eff}}/C_{\mathrm{sh}}^{\mathrm{(dipole)}}$")
    ax.set_title(r"(b) Diagnostic ratio after dipole correction")
    ax.legend(fontsize=7)
    fig.tight_layout()
    save(fig, "ceff_vs_sd.png")
    shutil.copy2(FIGDIR / "ceff_vs_sd.png", FIGDIR / "ceff_vs_coax.png")
    shutil.copy2(FIGDIR / "ceff_vs_sd.png", DRAFTFIG / "ceff_vs_coax.png")


def fig_circuit_overlay(by_sd):
    """Test Zin ≈ Z(Sd=0) + 1/(j ω C_dipole) against measured sheathed Z."""
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.1))
    freqs = [1.6e6, 1.7e6, 1.8e6]
    sds = [2, 4, 6, 8, 10]

    z0 = {}
    for f in freqs:
        pts = [p for p in by_sd[0] if abs(p[0] - f) < 1]
        if pts:
            z0[f] = complex(pts[0][1], pts[0][2])

    ax = axes[0]
    for f in freqs:
        if f not in z0:
            continue
        meas, model = [], []
        for sd in sds:
            pts = [p for p in by_sd[sd] if abs(p[0] - f) < 1]
            if not pts:
                continue
            c = coax_dipole(sd)
            z_m = z0[f] + 1.0 / (1j * 2 * math.pi * f * c)
            meas.append(pts[0][2])
            model.append(z_m.imag)
        ax.plot(sds, meas, "o-", ms=7, label=rf"meas {f/1e6:.2f} MHz")
        ax.plot(sds, model, "s--", ms=5, alpha=0.75, label=rf"model {f/1e6:.2f} MHz")
    ax.axhline(0, color="k", ls="--", lw=0.8)
    ax.set_xlabel(r"$S_d$ (cells)")
    ax.set_ylabel(r"Im$\{Z\}$ ($\Omega$)")
    ax.set_title(r"(a) Im$\{Z\}$: measured vs $Z(S_d{=}0)+1/(j\omega C_{\mathrm{dip}})$")
    ax.legend(fontsize=6, ncol=2)

    ax = axes[1]
    for f in freqs:
        if f not in z0:
            continue
        meas, model = [], []
        for sd in sds:
            pts = [p for p in by_sd[sd] if abs(p[0] - f) < 1]
            if not pts:
                continue
            c = coax_dipole(sd)
            z_m = z0[f] + 1.0 / (1j * 2 * math.pi * f * c)
            meas.append(pts[0][1])
            model.append(z_m.real)
        ax.plot(sds, meas, "o-", ms=7, label=rf"meas {f/1e6:.2f} MHz")
        ax.plot(sds, model, "s--", ms=5, alpha=0.75, label=rf"model {f/1e6:.2f} MHz")
    ax.set_xlabel(r"$S_d$ (cells)")
    ax.set_ylabel(r"Re$\{Z\}$ ($\Omega$)")
    ax.set_title(r"(b) Re$\{Z\}$: lossless series $C$ cannot explain drop")
    ax.legend(fontsize=6, ncol=2)
    fig.tight_layout()
    save(fig, "circuit_overlay.png")


def write_tables(rows, ceff_by_sd, lowf_means, by_sd):
    DATADIR.mkdir(parents=True, exist_ok=True)
    lines = ["# Sd\tFreq_Hz\tRe_Z\tIm_Z\tAbs_Z\tC_eff_pF\n"]
    for sd, fr, re, im, az in rows:
        c = ceff_from_im(fr, im)
        cstr = f"{c*1e12:.6f}" if c is not None else "nan"
        lines.append(f"{sd}\t{fr:.1f}\t{re:.6f}\t{im:.6f}\t{az:.6f}\t{cstr}\n")
    (DATADIR / "ceff_vs_frequency.txt").write_text("".join(lines), encoding="utf-8")

    summary = [
        "# C_eff diagnostic vs coax. Low-f window 0.8-1.2 MHz only (Sd=2,10).\n",
        "# Dipole C_sh = monopole/4 (two arms in series). Monopole kept for legacy comparison.\n",
        "# Sd\tt_sh_m\tC_eff_pF\tC_eff_std\tn\tC_mono_pF\tC_dip_pF\tratio_mono\tratio_dip\n",
    ]
    for sd in (2, 4, 6, 8, 10):
        t = sd * DX
        cm = coax_monopole(sd) * 1e12
        cd = coax_dipole(sd) * 1e12
        if sd in lowf_means:
            m, s, n = lowf_means[sd]
            summary.append(
                f"{sd}\t{t:.4f}\t{m*1e12:.4f}\t{s*1e12:.4f}\t{n}\t"
                f"{cm:.4f}\t{cd:.4f}\t{m*1e12/cm:.4f}\t{m*1e12/cd:.4f}\n"
            )
        else:
            summary.append(f"{sd}\t{t:.4f}\tnan\tnan\t0\t{cm:.4f}\t{cd:.4f}\tnan\tnan\n")
    (DATADIR / "ceff_vs_coax_summary.txt").write_text("".join(summary), encoding="utf-8")

    (DATADIR / "fres_summary.txt").write_text(
        "# Sd\tf_res_MHz\tnote\n"
        "0\t1.846\tIm +to- in dense band (plasma-loaded resonance; not a sheath marker)\n"
        "2\t0.655\tIm +to- in low-f band; rests on single inductive sample at 0.60 MHz\n"
        "4\t<1.50\tupper bound only; all Im<0 in dense band; no low-f run\n"
        "6\t<1.50\tupper bound only; all Im<0 in dense band; no low-f run\n"
        "8\t<1.50\tupper bound only; all Im<0 in dense band; no low-f run\n"
        "10\t<=0.50\tupper bound; all Im<0 in 0.50-2.30 MHz\n",
        encoding="utf-8",
    )

    # Fixed-frequency Im{Z} table — primary loading evidence
    im_lines = ["# Sd\tf_MHz\tIm_Z\n"]
    for f_mhz in (1.60, 1.70, 1.80, 2.00, 2.10, 2.20):
        for sd in (0, 2, 4, 6, 8, 10):
            pts = [p for p in by_sd[sd] if abs(p[0] - f_mhz * 1e6) < 1]
            if pts:
                im_lines.append(f"{sd}\t{f_mhz:.2f}\t{pts[0][2]:.6f}\n")
    (DATADIR / "imz_vs_sd.txt").write_text("".join(im_lines), encoding="utf-8")

    # Circuit overlay residuals at 1.60 MHz
    circ = ["# Sd\tf_Hz\tIm_meas\tIm_model\tRe_meas\tRe_model\tC_dip_pF\n"]
    f = 1.6e6
    pts0 = [p for p in by_sd[0] if abs(p[0] - f) < 1]
    if pts0:
        z0 = complex(pts0[0][1], pts0[0][2])
        for sd in (2, 4, 6, 8, 10):
            pts = [p for p in by_sd[sd] if abs(p[0] - f) < 1]
            if not pts:
                continue
            c = coax_dipole(sd)
            zm = z0 + 1.0 / (1j * 2 * math.pi * f * c)
            circ.append(
                f"{sd}\t{f:.1f}\t{pts[0][2]:.6f}\t{zm.imag:.6f}\t"
                f"{pts[0][1]:.6f}\t{zm.real:.6f}\t{c*1e12:.4f}\n"
            )
    (DATADIR / "circuit_overlay_1600kHz.txt").write_text("".join(circ), encoding="utf-8")


def load_all_rows():
    paper1 = DATADIR / "ceff_vs_frequency.txt"
    lowf_path = P0 / "data" / "cw_lowf_summary.txt"
    dense_path = P0 / "data" / "cw_tu_summary.txt"
    if lowf_path.exists() and dense_path.exists():
        return merge_unique(load_rows(lowf_path, True), load_rows(dense_path, False))
    if paper1.exists():
        print("WARNING: paper0 summaries missing; using paper1/analysis/data/ceff_vs_frequency.txt")
        return load_from_paper1_table(paper1)
    raise FileNotFoundError("No CW phasor tables found under paper0 or paper1 analysis/data")


def main():
    setup_style()
    rows = load_all_rows()

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

    fig_geometry()
    fig_n0_profile()
    fig_z_lowf(by_sd)
    fig_z_dense(by_sd)
    fig_z_combined(by_sd)
    fig_zabs_dense(by_sd)
    fig_fres()
    fig_im_vs_sd(by_sd)
    fig_ceff_freq(ceff_by_sd)
    fig_ceff_sd(lowf_means)
    fig_circuit_overlay(by_sd)
    write_tables(rows, ceff_by_sd, lowf_means, by_sd)

    print("Low-f C_eff diagnostic (0.8-1.2 MHz):")
    for sd, (m, s, n) in lowf_means.items():
        print(
            f"  Sd={sd}: {m*1e12:.2f} +/- {s*1e12:.2f} pF (n={n}); "
            f"C_mono={coax_monopole(sd)*1e12:.2f}; C_dip={coax_dipole(sd)*1e12:.2f}; "
            f"ratio_dip={m/coax_dipole(sd):.2f}"
        )
    print("Wrote", FIGDIR)
    print("Copied to", DRAFTFIG)


if __name__ == "__main__":
    main()
