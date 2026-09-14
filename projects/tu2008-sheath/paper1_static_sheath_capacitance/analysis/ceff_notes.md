# \(C_\mathrm{eff}\) extraction notes (Paper 1)

**Date:** 2026-09-13
**Script:** `make_ceff_products.py`
**Inputs:** `paper0_sheath_campaign/analysis/data/cw_lowf_summary.txt` and `cw_tu_summary.txt`

## Why \(S_d=4,6,8\) were missing from the first table

They were **not** dropped for physics reasons. The dense CW grid already ran \(S_d=0,2,4,6,8,10\) at \(1.50\)--\(2.30\,\mathrm{MHz}\). After that survey, every \(S_d\ge 2\) was capacitive in-band, so the low-frequency extension (\(0.50\)--\(1.50\,\mathrm{MHz}\)) was run only for \(S_d=0,2,10\) to locate the \(\mathrm{Im}\{Z\}\) crossings. The quasi-static \(C_\mathrm{eff}\) window \(0.8\)--\(1.2\,\mathrm{MHz}\) therefore exists only for \(S_d=2,10\). Intermediate widths re-enter as:

- dense-band \(Z(f)\) and \(\lvert Z\rvert\) at all six \(S_d\);
- \(\mathrm{Im}\{Z\}(S_d)\) at \(1.60\,\mathrm{MHz}\);
- \(C_\mathrm{eff}\) averaged over \(1.50\)--\(1.70\,\mathrm{MHz}\) for \(S_d=4,6,8,10\).

Dense-band \(C_\mathrm{eff}(S_d=2)\) is omitted: \(\mathrm{Im}\{Z\}\) is approaching zero there, so \(-1/(\omega\mathrm{Im}Z)\) is not a quasi-static capacitor.

## Definition

When \(\mathrm{Im}\{Z\}<0\),
\[
C_\mathrm{eff}(f)=-\frac{1}{2\pi f\,\mathrm{Im}\{Z\}}.
\]

## Coax reference

\[
C_\mathrm{sh}=\frac{2\pi\varepsilon_0 L}{\ln(1+S_d\Delta x/r_\mathrm{eff})},
\quad L=1.00\,\mathrm{m},\ \Delta x=0.04\,\mathrm{m},\ r_\mathrm{eff}=0.23\Delta x.
\]

## Results (script output)

| \(S_d\) | \(C_\mathrm{eff}\) low-\(f\) (pF) | \(C_\mathrm{eff}\) dense (pF) | \(C_\mathrm{coax}\) (pF) | ratio |
|--------:|----------------------------------:|------------------------------:|-------------------------:|------:|
| 2 | \(7.35\pm 1.12\) | (omit) | 24.49 | 0.30 |
| 4 | --- | \(7.06\pm 0.63\) | 19.11 | 0.37 |
| 6 | --- | \(5.39\pm 0.24\) | 16.86 | 0.32 |
| 8 | --- | \(4.76\pm 0.13\) | 15.55 | 0.31 |
| 10 | \(4.27\pm 1.83\) | \(4.43\pm 0.08\) | 14.66 | 0.29 |

## Caveats

- \(C_\mathrm{eff}\) includes plasma reactance, not pure gap \(C\).
- Free-space anchor still open.
- \(S_d=0\), \(1.50\,\mathrm{MHz}\) restart file is omitted.
