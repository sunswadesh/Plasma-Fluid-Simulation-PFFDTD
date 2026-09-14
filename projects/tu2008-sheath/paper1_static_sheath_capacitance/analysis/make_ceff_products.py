import math
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

root = Path("projects/tu2008-sheath")
summary = root / "paper0_sheath_campaign/analysis/data/cw_lowf_summary.txt"
outdir = root / "paper1_static_sheath_capacitance/analysis"
figdir = outdir / "figures"
datadir = outdir / "data"
figdir.mkdir(parents=True, exist_ok=True)
datadir.mkdir(parents=True, exist_ok=True)

eps0 = 8.854187817e-12
dx = 0.04
L = 25 * dx
r_eff = 0.23 * dx

rows = []
with open(summary) as f:
    for line in f:
        if line.startswith("#") or not line.strip() or line.startswith("Sd"):
            continue
        sd, fr, re, im, az = line.split()
        rows.append((int(float(sd)), float(fr), float(re), float(im), float(az)))

ceff_lines = [
    "# C_eff = -1/(2*pi*f*ImZ) when ImZ<0; NaN otherwise\n",
    "# Sd\tFreq_Hz\tIm_Z\tC_eff_F\tC_eff_pF\n",
]
by_sd = {2: [], 10: []}
for sd, fr, re, im, az in rows:
    if sd not in (0, 2, 10):
        continue
    if im < 0:
        C = -1.0 / (2 * math.pi * fr * im)
        ceff_lines.append(f"{sd}\t{fr:.1f}\t{im:.6f}\t{C:.6e}\t{C*1e12:.6f}\n")
        if sd in by_sd and fr <= 1.5e6:
            by_sd[sd].append((fr, C))
    else:
        ceff_lines.append(f"{sd}\t{fr:.1f}\t{im:.6f}\tnan\tnan\n")

(datadir / "ceff_vs_frequency.txt").write_text("".join(ceff_lines), encoding="utf-8")

summary_rows = [
    "# Band-averaged C_eff (0.8–1.2 MHz, ImZ<0 only)\n",
    "# Sd\tt_sh_m\tC_eff_mean_pF\tC_eff_std_pF\tn\tC_coax_pF\tratio\tr_eff_m\tL_m\n",
]
means = {}
for sd in (2, 10):
    band = [C for f, C in by_sd[sd] if 0.8e6 <= f <= 1.2e6]
    mean = sum(band) / len(band)
    var = sum((c - mean) ** 2 for c in band) / len(band)
    std = math.sqrt(var)
    t = sd * dx
    Ccoax = 2 * math.pi * eps0 * L / math.log(1 + t / r_eff)
    means[sd] = (mean, Ccoax)
    summary_rows.append(
        f"{sd}\t{t:.4f}\t{mean*1e12:.4f}\t{std*1e12:.4f}\t{len(band)}\t"
        f"{Ccoax*1e12:.4f}\t{mean/Ccoax:.4f}\t{r_eff:.6f}\t{L:.4f}\n"
    )

(datadir / "ceff_vs_coax_summary.txt").write_text("".join(summary_rows), encoding="utf-8")
(datadir / "fres_summary.txt").write_text(
    "# Sd\tf_res_MHz\tnote\n"
    "0\t1.846\tIm +to- August band\n"
    "2\t0.655\tIm +to- low-f\n"
    "10\t<=0.50\tall Im<0 in 0.5-1.5 MHz\n",
    encoding="utf-8",
)

plt.figure(figsize=(6.5, 4.2))
for sd, style in [(2, "o-"), (10, "s-")]:
    fs = [f / 1e6 for f, C in by_sd[sd]]
    Cs = [C * 1e12 for f, C in by_sd[sd]]
    plt.plot(fs, Cs, style, label=rf"$S_d={sd}$")
plt.axvspan(0.8, 1.2, color="0.85", zorder=0, label="avg. band")
plt.xlabel("Frequency (MHz)")
plt.ylabel(r"$C_{\mathrm{eff}}$ (pF)")
plt.title(r"Effective capacitance from $\mathrm{Im}\{Z\}=-1/(\omega C_{\mathrm{eff}})$")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(figdir / "ceff_vs_frequency.png", dpi=200)
plt.close()

sds = [2, 10]
ceff = [means[s][0] * 1e12 for s in sds]
ccoax = [means[s][1] * 1e12 for s in sds]
s_cont = list(range(1, 11))
c_cont = [
    2 * math.pi * eps0 * L / math.log(1 + s * dx / r_eff) * 1e12 for s in s_cont
]

plt.figure(figsize=(6.5, 4.2))
plt.plot(s_cont, c_cont, "k--", label=rf"coax $r_{{\mathrm{{eff}}}}={r_eff:.3f}\,\mathrm{{m}}$")
plt.plot(sds, ceff, "o", markersize=10, label=r"FDTD $C_{\mathrm{eff}}$ (0.8–1.2 MHz mean)")
plt.plot(sds, ccoax, "x", markersize=10, label="coax at same $S_d$")
plt.xlabel(r"Sheath width $S_d$ (cells)")
plt.ylabel("Capacitance (pF)")
plt.title(r"$C_{\mathrm{eff}}(S_d)$ versus coaxial analytic sheath")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(figdir / "ceff_vs_coax.png", dpi=200)
plt.close()

print("Wrote", datadir)
print("".join(summary_rows))
