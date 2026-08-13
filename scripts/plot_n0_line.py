#!/usr/bin/env python3
"""Overlay N0_SPATIAL line dumps for Sd=0 vs Sd=10 (normal to z-dipole through feed)."""

import argparse
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def load_n0_line(path):
    i, x, n0, sig, erx, ery, erz, pec = [], [], [], [], [], [], [], []
    with open(path, "r", errors="ignore") as f:
        for line in f:
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            parts = line.split()
            if len(parts) < 8:
                continue
            try:
                i.append(int(parts[0]))
                x.append(float(parts[1]))
                n0.append(float(parts[2]))
                sig.append(float(parts[3]))
                erx.append(float(parts[4]))
                ery.append(float(parts[5]))
                erz.append(float(parts[6]))
                pec.append(int(float(parts[7])))
            except ValueError:
                continue
    return {
        "i": np.array(i),
        "x": np.array(x),
        "n0": np.array(n0),
        "sig": np.array(sig),
        "pec": np.array(pec),
    }


def main():
    parser = argparse.ArgumentParser(description="Plot N0 line dumps Sd=0 vs Sd=10")
    parser.add_argument("--sd0", required=True, help="Path to Sd=0 n0_line.dat")
    parser.add_argument("--sd10", required=True, help="Path to Sd=10 n0_line.dat")
    parser.add_argument("--out", required=True, help="Output PNG path")
    parser.add_argument("--title", default="N0_SPATIAL along +x through feed (j=35, k=33)")
    args = parser.parse_args()

    d0 = load_n0_line(args.sd0)
    d10 = load_n0_line(args.sd10)
    if len(d0["i"]) == 0 or len(d10["i"]) == 0:
        raise SystemExit("Empty or unreadable N0 line dump")

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.semilogy(d0["i"], np.maximum(d0["n0"], 1e-30), "o-", label="Sd=0", markersize=3)
    ax.semilogy(d10["i"], np.maximum(d10["n0"], 1e-30), "s-", label="Sd=10", markersize=3)

    pec_i = d0["i"][d0["pec"] == 1]
    if len(pec_i) == 0:
        pec_i = d10["i"][d10["pec"] == 1]
    for pi in pec_i:
        ax.axvline(pi, color="gray", ls="--", lw=0.8, alpha=0.7)
    if len(pec_i):
        ax.axvline(pec_i[0], color="gray", ls="--", lw=0.8, alpha=0.7, label="PEC cell")

    ax.axvline(35, color="red", ls=":", lw=1.0, alpha=0.8, label="dipole i=35")
    ax.set_xlabel("i (cells)")
    ax.set_ylabel(r"$N_{0,e}$ (m$^{-3}$)")
    ax.set_title(args.title)
    ax.grid(True, which="both", alpha=0.3)
    ax.legend()
    fig.tight_layout()
    os.makedirs(os.path.dirname(os.path.abspath(args.out)) or ".", exist_ok=True)
    fig.savefig(args.out, dpi=150)
    print(f"Wrote {args.out}")

    # Quick numeric summary near the wire and domain edge
    for tag, d in (("Sd=0", d0), ("Sd=10", d10)):
        near = d["n0"][np.abs(d["i"] - 35) <= 2]
        edge = d["n0"][(d["i"] <= 8) | (d["i"] >= d["i"].max() - 8)]
        print(f"{tag}: near-wire N0 median={np.median(near):.3e}, edge median={np.median(edge):.3e}")


if __name__ == "__main__":
    main()
