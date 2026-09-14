# \(C_\mathrm{eff}\) extraction notes (Paper 1)

**Date:** 2026-09-10  
**Script:** `make_ceff_products.py`  
**Inputs:** `../../paper0_sheath_campaign/analysis/data/cw_lowf_summary.txt`

## Definition

When \(\mathrm{Im}\{Z\}<0\),
\[
C_\mathrm{eff}(f)=-\frac{1}{2\pi f\,\mathrm{Im}\{Z\}}.
\]
Band average: mean over capacitive points with \(0.8\le f\le 1.2\,\mathrm{MHz}\) (avoids \(S_d=2\) inductive island near 0.60 MHz).

## Coax reference

\[
C_\mathrm{sh}=\frac{2\pi\varepsilon_0 L}{\ln(1+S_d\Delta x/r_\mathrm{eff})},
\quad L=1.00\,\mathrm{m},\ \Delta x=0.04\,\mathrm{m},\ r_\mathrm{eff}=0.23\Delta x.
\]

## Results

| \(S_d\) | \(C_\mathrm{eff}\) (pF) | \(C_\mathrm{coax}\) (pF) | ratio |
|--------:|------------------------:|-------------------------:|------:|
| 2 | \(7.35\pm 1.12\) | 24.49 | 0.30 |
| 10 | \(4.27\pm 1.83\) | 14.66 | 0.29 |

Trend with \(S_d\) matches coax; absolute scale factor ≈ 0.3 under this \(r_\mathrm{eff}\).

## Caveats

- \(C_\mathrm{eff}\) includes plasma reactance, not pure gap \(C\).
- Free-space anchor still open.
- Intermediate \(S_d\) not in low-f set.
