# Sheath Validation — Analysis Summary

## Overview

This analysis document records the post-processing steps and measured outcomes from the sheath-width sweep (Sd = 0,2,4,6,8,10) performed on branch `PffdtdSheath`.

Scripts and outputs used:

- `scripts/run_sheath_sweep.ps1` / `scripts/run_sheath_sweep.bat` — produced per-Sd output folders under `results/sheath_sweep/sd{Sd}`.
- `scripts/analyze_sheath_results.py` — robust loader + DFT + impedance computation. Saves `sheath_impedance.png`, `sheath_resonance_shift.png`, and `sheath_resonance_summary.txt` in the repository root when run from the workspace root.

Data location:

- Time-series and simulation outputs: `results/sheath_sweep/sd*/data.vc`, `results/sheath_sweep/sd*/data.fd`, `results/sheath_sweep/sd*/simulation.log`.

## Processing Method

1. Load `data.vc` with a robust line-by-line numeric filter (extract first three numeric columns: time, V, I).
2. Compute median `dt` from consecutive time stamps to be robust to occasional repeated/irregular timestamps.
3. Apply a Hanning window to V(t) and I(t) and compute `V(f)`, `I(f)` via `rfft`.
4. Compute `Z(f) = V(f) / I(f)` where `|I(f)|` is above numerical threshold.
5. Search for series resonance as Im{Z} crossing from negative to positive (zero-crossing). If no crossing is found within analysis band, report frequency of maximum `|Z|` as fallback.

Default analysis band used in the first run: `f <= 1e6` (1 MHz).

## Results (measured)

Summary written to `sheath_resonance_summary.txt`. Table below reproduces the file contents:

| Sd (cells) | Im{Z} zero-crossing (Hz) | Fallback peak | Peak (Hz) |
|---:|---:|---:|---:|
| 0  | NaN | peak | 6607172882.332258 |
| 10 | NaN | peak | 5280934276.451150 |
| 2  | NaN | peak | 6157692738.826267 |
| 4  | NaN | peak | 5280934276.451150 |
| 6  | NaN | peak | 5280934276.451150 |
| 8  | NaN | peak | 5280934276.451150 |

Notes:

- All six runs completed and produced readable `data.vc` files.
- No Im{Z} zero-crossing was detected within the analyzed band (f ≤ 1 MHz).
- The reported peak frequencies are extremely large (GHz range) and are almost certainly an artifact of sampling cadence or FFT binning rather than the low-kHz antenna resonance discussed in Tu (2008).

## Interpretation vs Tu (2008)

Tu (2008) reports an upward shift in antenna resonance frequency as sheath width increases (resonance moves toward free-space value). With the present data and analysis:

- The current broadband DFT analysis is inconclusive; no physically meaningful resonance was identified within the analyzed band.
- The reported GHz-scale peaks are almost certainly numerical artifacts and do not represent the expected sheath resonance.
- Therefore, this dataset does not validate the Tu (2008) sheath resonance behavior.

## Possible causes for missing/ambiguous resonance

1. Sampling cadence and time-series length produce very high Nyquist frequencies and coarse DFT bins at the kHz scale; low-frequency features may be masked.
2. Time-series may contain significant transient content — steady-state portion may be too short.
3. The excitation used may not couple strongly to the resonance mode under current plasma parameters; a narrow-band sweep or different source waveform may be necessary. See Section 10 of `docs/sheath/SHEATH_VALIDATION_IMPLEMENTATION_PLAN.md` for the merged execution plan.

## Recommended next steps

1. Enhance the analyzer with:
   - a reduced kHz-band `--fmax` mode
   - trace decimation and output down-sampling support
   - steady-state trimming to exclude initial transient response
   - frequency resolution diagnostics (Nyquist, df, cycles captured)
2. Do not execute another long broadband sheath test until the analysis method is validated with existing outputs and narrow-band test planning is confirmed.
3. The analyzer was validated on existing `results/sheath_long/sd0/data.vc` using `--fmax 200000 --decimate 10 --trim_seconds 0.0001 --peak_fmax 200000` and produced a fallback peak at 46.845 kHz.
4. If broadband DFT remains inconclusive, perform a narrow-band excitation sweep to directly map input impedance versus frequency. The combined narrow-band and long-record plan is now included in Section 10 of `docs/sheath/SHEATH_VALIDATION_IMPLEMENTATION_PLAN.md`.
4. Validate the `Sd=0` baseline explicitly against the existing no-sheath plasma regression case.
5. Document the new results in this analysis summary and in the implementation plan.

## Follow-up (2026-08)

Later CW phasor screening near \(f_p\) resolved a clean resonance (~1.775 MHz) but showed **identical** \(Z(f)\) for Sd=0 and Sd=10 (~0.003% difference). That is a coupling/geometry bug (sheath seeded from the plasma-on mask before antenna PEC exists), not an FFT issue. Full post-mortem, N0 line diagnostics, and the coupling fix are documented in:

- [`analysis/sheath_coupling_findings.md`](../../analysis/sheath_coupling_findings.md)

## Conclusion

The current dataset is a useful first pass, but it is not sufficient to complete sheath validation. The next phase must focus on low-frequency signal conditioning and targeted resonance measurement before the sheath plans can be considered complete.

- `scripts/analyze_sheath_results.py` — analyzer (workspace root)
- `sheath_impedance.png` — combined plots of Re{Z} and Im{Z} vs frequency (workspace root)
- `sheath_resonance_shift.png` — Sd vs reported resonance/peak (workspace root)
- `sheath_resonance_summary.txt` — numeric table of results (workspace root)

---

If you want, I can now: (A) re-run analysis with `fmax=200e3`, (B) add decimation and steady-state trimming to the analyzer, or (C) modify and re-run the simulations to record longer steady-state traces — which would you prefer?
