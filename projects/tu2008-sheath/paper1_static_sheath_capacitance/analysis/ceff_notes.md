# \(C_\mathrm{eff}\) and coax notes (Paper 1, review revision)

**Date:** 2026-09-14  
**Script:** `make_ceff_products.py`  
**Primary inputs:** self-contained `data/ceff_vs_frequency.txt` (falls back from paper0 summaries when present)

## Correct analytic object

Liu-style **monopole** coax
\[
C_\mathrm{sh}^\mathrm{(mono)}=\frac{2\pi\varepsilon_0 L}{\ln(1+S_d\Delta x/r_\mathrm{eff})}
\]
is **not** the feed capacitance of a center-fed dipole of total length \(L\).

Dipole correction (two arms of length \(L/2\) in series):
\[
C_\mathrm{sh}^\mathrm{(dip)}=\frac{C_\mathrm{sh}^\mathrm{(mono)}}{4}.
\]

With \(r_\mathrm{eff}=0.23\Delta x\):

| \(S_d\) | \(C_\mathrm{eff}\) (0.8–1.2 MHz) | \(C_\mathrm{mono}\) | \(C_\mathrm{dip}\) | ratio mono | ratio dip |
|--------:|--------------------------------:|--------------------:|-------------------:|-----------:|----------:|
| 2 | \(7.35\pm 1.12\) pF | 24.49 | 6.12 | 0.30 | **1.20** |
| 10 | \(4.27\pm 1.83\) pF | 14.66 | 3.66 | 0.29 | **1.17** |

The old “scale factor ≈ 0.3” was a monopole/dipole geometry error, not a physical discrepancy.

## Primary claim (not \(C_\mathrm{eff}\))

Dense-band \(\mathrm{Im}\{Z\}(S_d)\) at 1.60–1.80 MHz is monotonic (thicker → more capacitive). Near \(f_p\) that ordering **reverses**. See `figures/imz_vs_sd.png` and `data/imz_vs_sd.txt`.

## Circuit overlay

`Z(S_d=0)+1/(jω C_dip)` fails for \(\mathrm{Re}\{Z\}\): lossless series \(C\) cannot explain the measured resistive drop. See `figures/circuit_overlay.png`.

## Open controls

- Free-space CW: `FREE_SPACE_CONTROL.md`
- Low-f for \(S_d=4,6,8\) and denser \(S_d=2\): `LOWF_INTERMEDIATE_PLAN.md`

## Caveats

- \(C_\mathrm{eff}\) is frequency-dependent (mixed sheath+plasma+box).
- \(S_d=2\) crossing rests on one inductive sample at 0.60 MHz.
- Electrically small domain; absolute \(Z\) may include ABC/box contributions.
