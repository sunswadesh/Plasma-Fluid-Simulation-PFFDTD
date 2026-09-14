# Free-space CW resonance on the Paper 1 dipole (open control)

**Purpose.** Provide the free-space \(f_\mathrm{res}\) upper anchor required by the Paper 1 review.

**Status:** Script scaffold ready; **not yet run** (multi-hour CW on this workstation).

## How to run

From the repo / PF-FDTD project root that contains `sheath_sine_vc.str` and the solver:

```powershell
# Option A: reuse the dense CW driver with Sd forced to 0 and plasma off
# (requires a free-space build or FREQ_PLASMA=0 / no-plasma flag if available)

# Option B: temporary vacuum run by setting fp extremely low is NOT valid —
# use a true free-space (no fluid update) configuration.

# Dense-band free-space grid (same tones as sheath_cw_tu):
& projects/tu2008-sheath/scripts/run_sheath_cw_tu.ps1 `
  -SheathWidths @(0) `
  -FrequenciesHz @(1500000,1600000,1700000,1750000,1800000,1850000,1900000,2000000,2100000,2200000,2300000)
```

Until a dedicated free-space executable path exists, document the free-space control as **open** in the manuscript limitations.

## Success criterion

Locate the first \(\mathrm{Im}\{Z\}\) \(+\to-\) crossing on the same \(70\times70\times65\), \(\Delta x=0.04\,\mathrm{m}\) dipole with plasma off. Compare to plasma-loaded \(f_\mathrm{res}(S_d=0)=1.846\,\mathrm{MHz}\).
