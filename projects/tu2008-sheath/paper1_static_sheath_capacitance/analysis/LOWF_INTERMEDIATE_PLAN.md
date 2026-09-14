# Low-frequency CW for intermediate sheath widths

**Purpose.** Close the \(f_\mathrm{res}(S_d)\) upper-bound gap for \(S_d=4,6,8\) and densify \(S_d=2\) near the inductive sample.

**Status:** Driver ready (reuses `run_sheath_cw_tu.ps1`); **not yet run**.

## Recommended campaigns

### A. Intermediate widths (priority)

```powershell
& projects/tu2008-sheath/scripts/run_sheath_cw_lowf.ps1 `
  -SheathWidths @(4, 6, 8) `
  -FrequenciesHz @(500000,600000,700000,800000,900000,1000000,1100000,1200000,1300000,1400000,1500000) `
  -SkipCompleted
```

### B. Dense tones near \(S_d=2\) inductive sample

```powershell
& projects/tu2008-sheath/scripts/run_sheath_cw_tu.ps1 `
  -SheathWidths @(2) `
  -FrequenciesHz @(550000,575000,600000,625000,650000,675000,700000) `
  -SkipCompleted
```

Wall-clock estimate: similar to the original low-\(f\) extension (~tens of hours on a 4-core workstation).

## Why required

Measured \(+\to-\) crossings exist only for \(S_d=0\) and \(S_d=2\). Intermediate widths currently contribute only dense-band upper bounds \(<1.50\,\mathrm{MHz}\). The \(S_d=2\) crossing at \(0.655\,\mathrm{MHz}\) rests on a single inductive sample at \(0.60\,\mathrm{MHz}\).
