#!/usr/bin/env python3
"""Analyze post-fix long pulse sheath sweep with CW-compatible resonance picks."""
import glob
import os
import re
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from analyze_sheath_results import compute_impedance, robust_load_vc


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sweep = os.path.join(root, "results", "sheath_pulse_long")
    out_fig = os.path.join(root, "analysis", "figures")
    out_data = os.path.join(root, "analysis", "data")
    os.makedirs(out_fig, exist_ok=True)
    os.makedirs(out_data, exist_ok=True)

    files = sorted(
        glob.glob(os.path.join(sweep, "sd*", "data.vc")),
        key=lambda p: int(re.search(r"sd(\d+)", p).group(1)),
    )
    rows = []
    fig, (axr, axi) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    for fp in files:
        sd = int(re.search(r"sd(\d+)", fp).group(1))
        t, v, i = robust_load_vc(fp)
        freq, Z, _dt = compute_impedance(t, v, i)
        mask = (freq >= 5e5) & (freq <= 3.5e6)
        f = freq[mask]
        z = Z[mask]
        im = np.imag(z)
        axr.plot(f / 1e6, np.real(z), label=f"Sd={sd}")
        axi.plot(f / 1e6, im, label=f"Sd={sd}")

        p2m = []
        for k in range(1, len(im)):
            if im[k - 1] > 0 and im[k] <= 0:
                fc = f[k - 1] + (f[k] - f[k - 1]) * (im[k - 1]) / (im[k - 1] - im[k])
                if 1.2e6 <= fc <= 3.0e6:
                    p2m.append(fc)
        fres = p2m[0] if p2m else np.nan

        def im_at(fq):
            j = int(np.argmin(np.abs(f - fq)))
            return float(im[j])

        rows.append((sd, fres, im_at(1.7e6), im_at(1.9e6), p2m))

    axr.set_ylabel("Re{Z} (Ohm)")
    axr.set_title("Pulse long sweep Z(f) after sheath coupling fix")
    axr.legend()
    axr.grid(True, alpha=0.3)
    axi.set_xlabel("Frequency (MHz)")
    axi.set_ylabel("Im{Z} (Ohm)")
    axi.axhline(0, color="k", ls="--", lw=0.6)
    axi.legend()
    axi.grid(True, alpha=0.3)
    fig.tight_layout()
    zpath = os.path.join(out_fig, "pulse_long_impedance.png")
    fig.savefig(zpath, dpi=150)
    print("Wrote", zpath)

    sds = [r[0] for r in rows if np.isfinite(r[1])]
    fres = [r[1] / 1e6 for r in rows if np.isfinite(r[1])]
    if len(sds) >= 2:
        fig2, ax = plt.subplots(figsize=(8, 5))
        ax.plot(sds, fres, "o-", ms=8)
        ax.set_xlabel("Sd (cells)")
        ax.set_ylabel("f_res (MHz) [Im + to - in 1.2-3 MHz]")
        ax.set_title("Pulse FFT resonance (CW-compatible crossing)")
        ax.grid(True, alpha=0.3)
        fig2.tight_layout()
        rpath = os.path.join(out_fig, "pulse_long_resonance_shift.png")
        fig2.savefig(rpath, dpi=150)
        print("Wrote", rpath)

    spath = os.path.join(out_data, "pulse_long_resonance_summary.txt")
    with open(spath, "w") as sf:
        sf.write("# Post-fix long pulse FFT (MaxIter=2e5, Spar=2MHz, fp=2MHz, VcRate=50)\n")
        sf.write("# f_res = first Im{Z} +to- crossing in 1.2-3.0 MHz (CW-compatible)\n")
        sf.write("# Default analyzer -to+ picks are often spurious at lower f.\n")
        sf.write("Sd\tf_res_p2m_Hz\tIm_1.7MHz\tIm_1.9MHz\tall_p2m_in_band_kHz\n")
        for sd, fres_hz, i17, i19, p2m in rows:
            band = ",".join(f"{x/1e3:.1f}" for x in p2m) if p2m else "none"
            fres_s = f"{fres_hz:.6f}" if np.isfinite(fres_hz) else "NaN"
            sf.write(f"{sd}\t{fres_s}\t{i17:.3f}\t{i19:.3f}\t{band}\n")
            fres_m = fres_hz / 1e6 if np.isfinite(fres_hz) else float("nan")
            print(
                f"Sd={sd}: f_res(+to-)={fres_m:.3f} MHz  "
                f"Im(1.7)={i17:.0f}  Im(1.9)={i19:.0f}  crossings={band}"
            )
    print("Wrote", spath)


if __name__ == "__main__":
    main()
