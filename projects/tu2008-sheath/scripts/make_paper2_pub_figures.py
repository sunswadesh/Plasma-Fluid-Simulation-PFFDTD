"""Regenerate Paper 2 manuscript figures in publication style.

Reads existing analysis TSV (+ pilot .vc for V/I). Writes PNGs (300 dpi)
under paper2_oscillating_sheath_boundary/analysis/figures/.
"""
from __future__ import print_function

import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.ticker import MaxNLocator, FuncFormatter

from paths import pffdtd_root, project_root
from analyze_paper2_pilot import robust_load_vc

DPI = 300
TRIM = 0.5
F_DRIVE = 700e3

# Colorblind-friendly fixed palette
C_STATIC0 = "#0072B2"   # blue
C_STATIC1 = "#E69F00"   # amber
C_OSC = "#D55E00"       # vermillion
C_BRACKET = "#444444"
C_EDGE = ["#009E73", "#D55E00", "#CC79A7"]  # green, vermillion, pink
C_PHI = ["#0072B2", "#E69F00", "#009E73", "#D55E00", "#CC79A7"]
C_FREQ = {500000: "#0072B2", 700000: "#009E73", 1200000: "#E69F00"}
C_DR = ["#0072B2", "#E69F00", "#009E73", "#D55E00"]


def apply_style():
    plt.rcParams.update({
        "font.family": "serif",
        "font.size": 10,
        "axes.labelsize": 11,
        "axes.titlesize": 11,
        "legend.fontsize": 8.5,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "axes.linewidth": 0.9,
        "lines.linewidth": 1.2,
        "figure.dpi": 120,
        "savefig.dpi": DPI,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.08,
        "axes.grid": True,
        "grid.alpha": 0.28,
        "grid.linewidth": 0.5,
        "legend.framealpha": 0.95,
        "legend.edgecolor": "0.75",
        "mathtext.fontset": "dejavuserif",
    })


def ohm_formatter(x, _pos):
    ax = abs(x)
    if ax >= 1000:
        v = x / 1000.0
        if abs(v - round(v)) < 1e-9:
            return r"$%d$" % int(round(v))
        return r"$%.1f$" % v
    return r"$%g$" % x


def style_complex_ax(ax, xlabel=True, ylabel=True):
    if xlabel:
        ax.set_xlabel(r"Re$\{Z\}$ (k$\Omega$)")
    if ylabel:
        ax.set_ylabel(r"Im$\{Z\}$ (k$\Omega$)")
    ax.xaxis.set_major_formatter(FuncFormatter(ohm_formatter))
    ax.yaxis.set_major_formatter(FuncFormatter(ohm_formatter))
    # tick labels are in kΩ numbers; rescale data? Better: keep data in Ω and
    # divide displayed values. FuncFormatter already divides by 1000 when >=1000.
    ax.xaxis.set_major_locator(MaxNLocator(6))
    ax.yaxis.set_major_locator(MaxNLocator(6))
    for spine in ax.spines.values():
        spine.set_visible(True)


def pad_limits(ax, pts, pad_frac=0.08, min_pad=800):
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)
    dx = max((xmax - xmin) * pad_frac, min_pad)
    dy = max((ymax - ymin) * pad_frac, min_pad)
    ax.set_xlim(xmin - dx, xmax + dx)
    ax.set_ylim(ymin - dy, ymax + dy)


def read_tsv(path):
    rows = []
    with open(path, "r") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            rows.append(row)
    return rows


def save(fig, path):
    fig.savefig(path, dpi=DPI)
    plt.close(fig)
    print("Wrote", path)


def fig_pilot_complex(data_dir, fig_dir, soft=False):
    tag = "_soft" if soft else ""
    path = os.path.join(data_dir, "pilot_phasor_Z%s.tsv" % tag)
    rows = {r["case"]: r for r in read_tsv(path)}
    z0 = (float(rows["static_rs0"]["ReZ_ohm"]), float(rows["static_rs0"]["ImZ_ohm"]))
    z1 = (float(rows["static_rsmax"]["ReZ_ohm"]), float(rows["static_rsmax"]["ImZ_ohm"]))
    zo = (float(rows["osc_rs_t"]["ReZ_ohm"]), float(rows["osc_rs_t"]["ImZ_ohm"]))

    fig, ax = plt.subplots(figsize=(4.6, 3.7))
    ax.plot([z0[0], z1[0]], [z0[1], z1[1]], "--", color=C_BRACKET, lw=1.2,
            zorder=1, label="Static bracket")
    ax.plot(z0[0], z0[1], "o", color=C_STATIC0, ms=8, zorder=3,
            label=r"Static $r_{s0}=4$")
    ax.plot(z1[0], z1[1], "s", color=C_STATIC1, ms=8, zorder=3,
            label=r"Static $r_{s0}+1=5$")
    ax.plot(zo[0], zo[1], "*", color=C_OSC, ms=14, zorder=4,
            markeredgecolor="k", markeredgewidth=0.4,
            label=r"Oscillating $\Delta r=1$")
    style_complex_ax(ax)
    pad_limits(ax, [z0, z1, zo])
    ax.legend(loc="best", frameon=True)
    # no title — caption carries context
    save(fig, os.path.join(fig_dir, "pilot_Z_complex%s.png" % tag))


def fig_pilot_vi(fig_dir, soft=False):
    root = pffdtd_root()
    tag = "_soft" if soft else ""
    base = os.path.join(root, "results",
                        "paper2_rs_t_pilot_soft" if soft else "paper2_rs_t_pilot")
    cases = [
        ("static_rs0", r"Static $r_{s0}=4$", C_STATIC0, "-", 1.1),
        ("static_rsmax", r"Static $r=5$", C_STATIC1, "-", 1.1),
        ("osc_rs_t", r"Oscillating $\Delta r=1$", C_OSC, "-", 1.0),
    ]
    series = {}
    for name, _, _, _, _ in cases:
        vc = os.path.join(base, name, "data.vc")
        if not os.path.isfile(vc):
            print("MISSING", vc)
            return
        t, v, i = robust_load_vc(vc)
        n0 = int(len(t) * TRIM)
        series[name] = (t[n0:], v[n0:], i[n0:])

    t_win = 5.0 / F_DRIVE
    fig, axes = plt.subplots(2, 1, figsize=(6.4, 4.4), sharex=True)
    for name, label, color, ls, lw in cases:
        t, v, i = series[name]
        t0 = t[-1] - t_win
        m = t >= t0
        # Voltage: show only one static + osc offset for clarity if soft/hard overlap
        axes[0].plot(t[m] * 1e6, v[m], color=color, ls=ls, lw=lw, label=label, alpha=0.95)
        axes[1].plot(t[m] * 1e6, i[m] * 1e6, color=color, ls=ls, lw=lw, label=label, alpha=0.95)
    axes[0].set_ylabel(r"$V$ (V)")
    axes[1].set_ylabel(r"$I$ ($\mu$A)")
    axes[1].set_xlabel(r"$t$ ($\mu$s)")
    axes[0].legend(loc="upper right", ncol=1, frameon=True)
    if not soft:
        axes[1].annotate(
            "Staircasing spikes",
            xy=(24.2, 350), xytext=(22.0, 380),
            fontsize=8, color=C_OSC,
            arrowprops=dict(arrowstyle="->", color=C_OSC, lw=0.8),
        )
    for ax in axes:
        ax.xaxis.set_major_locator(MaxNLocator(6))
        ax.yaxis.set_major_locator(MaxNLocator(5))
    fig.align_ylabels(axes)
    save(fig, os.path.join(fig_dir, "pilot_VI_last_cycles%s.png" % tag))


def fig_delta_r_soft(data_dir, fig_dir):
    path = os.path.join(data_dir, "delta_r_soft_phasor_Z.tsv")
    static, osc = {}, {}
    for r in read_tsv(path):
        p = float(r["param"])
        pt = (float(r["ReZ"]), float(r["ImZ"]), float(r["AbsZ"]))
        if r["kind"] == "static":
            static[int(p)] = pt
        else:
            osc[p] = pt

    fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.5))
    drs = sorted(osc)
    axes[0].plot(drs, [osc[d][2] / 1e3 for d in drs], "o-", color=C_OSC, ms=6,
                 label=r"$|Z|$ (osc)")
    axes[0].plot(drs, [osc[d][0] / 1e3 for d in drs], "s--", color=C_STATIC1, ms=5,
                 label=r"Re$\{Z\}$ (osc)")
    if 4 in static:
        axes[0].axhline(static[4][2] / 1e3, color=C_STATIC0, ls=":", lw=1.2,
                        label=r"$|Z|$ static $S_d=4$")
    axes[0].set_xlabel(r"$\Delta r$ (cells)")
    axes[0].set_ylabel(r"$Z$ (k$\Omega$)")
    axes[0].legend(loc="best", frameon=True)
    axes[0].set_xticks(drs)
    axes[0].text(0.02, 0.98, "(a)", transform=axes[0].transAxes,
                  va="top", ha="left", fontsize=11, fontweight="bold")

    ax = axes[1]
    pts = []
    for sd, color, mk in ((4, C_STATIC0, "o"), (5, C_STATIC1, "s"), (6, "#009E73", "D")):
        if sd not in static:
            continue
        x, y, _ = static[sd]
        ax.plot(x, y, mk, color=color, ms=7, zorder=3, label=r"Static $S_d=%d$" % sd)
        pts.append((x, y))
    if 4 in static and 5 in static:
        ax.plot([static[4][0], static[5][0]], [static[4][1], static[5][1]],
                "--", color=C_BRACKET, lw=1.0, zorder=1)
    if 5 in static and 6 in static:
        ax.plot([static[5][0], static[6][0]], [static[5][1], static[6][1]],
                "--", color=C_BRACKET, lw=1.0, zorder=1, label="Static brackets")
    for i, dr in enumerate(drs):
        x, y, _ = osc[dr]
        ax.plot(x, y, "*", color=C_DR[i % len(C_DR)], ms=12, zorder=4,
                markeredgecolor="k", markeredgewidth=0.35,
                label=r"Osc $\Delta r=%.1f$" % dr)
        pts.append((x, y))
    style_complex_ax(ax)
    pad_limits(ax, pts, pad_frac=0.1, min_pad=1500)
    ax.legend(loc="best", fontsize=7.5, frameon=True)
    ax.text(0.02, 0.98, "(b)", transform=ax.transAxes,
            va="top", ha="left", fontsize=11, fontweight="bold")
    fig.tight_layout()
    save(fig, os.path.join(fig_dir, "delta_r_soft_scan.png"))


def fig_soft_edge(data_dir, fig_dir):
    path = os.path.join(data_dir, "soft_edge_sensitivity_Z.tsv")
    rows = read_tsv(path)
    by = {r["case"]: r for r in rows}
    z0 = (float(by["static_rs0"]["ReZ"]), float(by["static_rs0"]["ImZ"]))
    z1 = (float(by["static_rsmax"]["ReZ"]), float(by["static_rsmax"]["ImZ"]))
    osc = []
    for key, edge, color in (
        ("osc_edge0p5", 0.5, C_EDGE[0]),
        ("osc_edge1", 1.0, C_EDGE[1]),
        ("osc_edge2", 2.0, C_EDGE[2]),
    ):
        r = by[key]
        osc.append((edge, float(r["ReZ"]), float(r["ImZ"]), color))

    fig, ax = plt.subplots(figsize=(4.8, 3.8))
    ax.plot([z0[0], z1[0]], [z0[1], z1[1]], "--", color=C_BRACKET, lw=1.2, label="Static bracket")
    ax.plot(z0[0], z0[1], "o", color=C_STATIC0, ms=8, label=r"Static $r_{s0}=4$")
    ax.plot(z1[0], z1[1], "s", color=C_STATIC1, ms=8, label=r"Static $r_{s0}+1=5$")
    pts = [z0, z1]
    for edge, x, y, color in osc:
        ax.plot(x, y, "*", color=color, ms=11, markeredgecolor="k", markeredgewidth=0.35,
                label=r"Osc soft $=%.1f$" % edge)
        pts.append((x, y))
    style_complex_ax(ax)
    pad_limits(ax, pts)
    ax.legend(loc="best", frameon=True)
    save(fig, os.path.join(fig_dir, "soft_edge_Z_complex.png"))


def fig_sparse_f(data_dir, fig_dir):
    path = os.path.join(data_dir, "sparse_f_soft_phasor_Z.tsv")
    by_f = {}
    for r in read_tsv(path):
        f = int(r["f_Hz"])
        by_f.setdefault(f, {})[r["kind"]] = (float(r["ReZ"]), float(r["ImZ"]))

    fig, ax = plt.subplots(figsize=(5.0, 4.0))
    pts = []
    handles = [
        Line2D([0], [0], marker="o", color="w", markerfacecolor="0.35",
               markeredgecolor="0.35", markersize=7, label=r"Static $r_{s0}$"),
        Line2D([0], [0], marker="s", color="w", markerfacecolor="0.35",
               markeredgecolor="0.35", markersize=7, label=r"Static $r_{s0}+1$"),
        Line2D([0], [0], linestyle="--", color="0.4", label="Static bracket"),
    ]
    for f in sorted(by_f):
        block = by_f[f]
        color = C_FREQ.get(f, "k")
        z0 = block.get("static_rs0")
        z1 = block.get("static_rsmax")
        zo = block.get("osc")
        if z0 and z1:
            ax.plot([z0[0], z1[0]], [z0[1], z1[1]], "--", color=color, lw=1.0, alpha=0.75)
            ax.plot(z0[0], z0[1], "o", color=color, ms=7)
            ax.plot(z1[0], z1[1], "s", color=color, ms=7)
            pts.extend([z0, z1])
        if zo:
            h = ax.plot(zo[0], zo[1], "*", color=color, ms=12,
                        markeredgecolor="k", markeredgewidth=0.35,
                        label="%g kHz (osc)" % (f / 1e3))[0]
            handles.append(h)
            pts.append(zo)
    style_complex_ax(ax)
    pad_limits(ax, pts, pad_frac=0.1, min_pad=1500)
    ax.legend(handles=handles, loc="best", fontsize=7.5, frameon=True)
    save(fig, os.path.join(fig_dir, "sparse_f_Z_complex.png"))


def fig_phase_scan(data_dir, fig_dir):
    path = os.path.join(data_dir, "phase_scan_soft_phasor_Z.tsv")
    # static from soft pilot
    soft = os.path.join(data_dir, "pilot_phasor_Z_soft.tsv")
    srows = {r["case"]: r for r in read_tsv(soft)}
    z0 = (float(srows["static_rs0"]["ReZ_ohm"]), float(srows["static_rs0"]["ImZ_ohm"]))
    z1 = (float(srows["static_rsmax"]["ReZ_ohm"]), float(srows["static_rsmax"]["ImZ_ohm"]))

    osc = []
    for r in read_tsv(path):
        osc.append((float(r["phi_deg"]), float(r["ReZ"]), float(r["ImZ"])))
    osc.sort(key=lambda x: x[0])

    fig, ax = plt.subplots(figsize=(5.0, 4.0))
    ax.plot([z0[0], z1[0]], [z0[1], z1[1]], "--", color=C_BRACKET, lw=1.2, label="Static bracket")
    ax.plot(z0[0], z0[1], "o", color="0.25", ms=7, label=r"Static $r_{s0}=4$")
    ax.plot(z1[0], z1[1], "s", color="0.45", ms=7, label=r"Static $r_{s0}+1=5$")
    pts = [z0, z1]
    for i, (phi, x, y) in enumerate(osc):
        ax.plot(x, y, "*", color=C_PHI[i % len(C_PHI)], ms=11,
                markeredgecolor="k", markeredgewidth=0.35,
                label=r"Osc $\phi=%g^\circ$" % phi)
        pts.append((x, y))
    # guide polyline through phases in order
    ax.plot([p[1] for p in osc], [p[2] for p in osc], "-", color="0.55", lw=1.0,
            alpha=0.85, zorder=1)
    style_complex_ax(ax)
    pad_limits(ax, pts, pad_frac=0.12, min_pad=2000)
    ax.legend(loc="best", fontsize=7.5, frameon=True, ncol=1)
    save(fig, os.path.join(fig_dir, "phase_scan_Z_complex.png"))


def fig_delta_r_matched(data_dir, fig_dir):
    path = os.path.join(data_dir, "delta_r_matched_phasor_Z.tsv")
    soft = os.path.join(data_dir, "pilot_phasor_Z_soft.tsv")
    # also need sd6 from soft delta scan for brackets
    delta = os.path.join(data_dir, "delta_r_soft_phasor_Z.tsv")
    static = {}
    for r in read_tsv(soft):
        if r["case"] == "static_rs0":
            static[4] = (float(r["ReZ_ohm"]), float(r["ImZ_ohm"]))
        elif r["case"] == "static_rsmax":
            static[5] = (float(r["ReZ_ohm"]), float(r["ImZ_ohm"]))
    for r in read_tsv(delta):
        if r["kind"] == "static":
            static[int(float(r["param"]))] = (float(r["ReZ"]), float(r["ImZ"]))

    osc = []
    for r in read_tsv(path):
        osc.append((float(r["dr"]), float(r["ReZ"]), float(r["ImZ"])))
    osc.sort(key=lambda x: x[0])

    fig, ax = plt.subplots(figsize=(5.0, 4.0))
    pts = []
    # draw relevant brackets
    if 4 in static and 5 in static:
        ax.plot([static[4][0], static[5][0]], [static[4][1], static[5][1]],
                "--", color=C_BRACKET, lw=1.0, label="Static brackets")
        ax.plot(static[4][0], static[4][1], "o", color="0.25", ms=6)
        ax.plot(static[5][0], static[5][1], "s", color="0.45", ms=6)
        pts.extend([static[4], static[5]])
    if 5 in static and 6 in static:
        ax.plot([static[5][0], static[6][0]], [static[5][1], static[6][1]],
                "--", color=C_BRACKET, lw=1.0)
        ax.plot(static[6][0], static[6][1], "D", color="0.55", ms=6,
                label=r"Static $S_d=6$")
        pts.append(static[6])
    for i, (dr, x, y) in enumerate(osc):
        ax.plot(x, y, "*", color=C_DR[i % len(C_DR)], ms=12,
                markeredgecolor="k", markeredgewidth=0.35,
                label=r"Osc $\Delta r=%.1f$" % dr)
        pts.append((x, y))
    style_complex_ax(ax)
    pad_limits(ax, pts, pad_frac=0.12, min_pad=2000)
    ax.legend(loc="best", fontsize=7.5, frameon=True)
    save(fig, os.path.join(fig_dir, "delta_r_matched_Z_complex.png"))


def main():
    apply_style()
    out = os.path.join(project_root(), "paper2_oscillating_sheath_boundary", "analysis")
    data_dir = os.path.join(out, "data")
    fig_dir = os.path.join(out, "figures")
    os.makedirs(fig_dir, exist_ok=True)

    fig_pilot_complex(data_dir, fig_dir, soft=False)
    fig_pilot_complex(data_dir, fig_dir, soft=True)
    fig_pilot_vi(fig_dir, soft=False)
    fig_pilot_vi(fig_dir, soft=True)
    fig_delta_r_soft(data_dir, fig_dir)
    fig_soft_edge(data_dir, fig_dir)
    fig_sparse_f(data_dir, fig_dir)
    fig_phase_scan(data_dir, fig_dir)
    fig_delta_r_matched(data_dir, fig_dir)
    print("Done.")


if __name__ == "__main__":
    main()
