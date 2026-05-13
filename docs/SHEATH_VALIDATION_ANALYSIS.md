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

- We cannot confirm or refute Tu (2008) quantitatively because the physical resonance was not identified as a clean Im{Z} zero-crossing within the analyzed band.
- Qualitatively, no clear monotonic shift of an identifiable resonance was observed in the extracted peak bins.

## Possible causes for missing/ambiguous resonance

1. Sampling cadence and time-series length produce very high Nyquist frequencies and coarse DFT bins at the kHz scale; low-frequency features may be masked.
2. Time-series may contain significant transient content — steady-state portion may be too short.
3. The excitation used may not couple strongly to the resonance mode under current plasma parameters; a narrow-band sweep or different source waveform may be necessary.

## Recommended next steps

1. Re-run `scripts/analyze_sheath_results.py` with a reduced `fmax` (e.g., 200e3) to force inspection of kHz band and/or decimate the time-series by integer factor before FFT.
2. Trim the initial transient from the V(t)/I(t) traces and analyze only steady-state windows (e.g., last N seconds of the record).
3. If resonance remains ambiguous, modify simulation source to perform a controlled frequency sweep (narrowband excitation) to directly measure input impedance vs. frequency.
4. Add automated checks in `scripts/analyze_sheath_results.py` to report sampling rate, Nyquist frequency and number of cycles captured to help tune future runs.

## Artifacts & Files produced by current work

- `scripts/analyze_sheath_results.py` — analyzer (workspace root)
- `sheath_impedance.png` — combined plots of Re{Z} and Im{Z} vs frequency (workspace root)
- `sheath_resonance_shift.png` — Sd vs reported resonance/peak (workspace root)
- `sheath_resonance_summary.txt` — numeric table of results (workspace root)

---

If you want, I can now: (A) re-run analysis with `fmax=200e3`, (B) add decimation and steady-state trimming to the analyzer, or (C) modify and re-run the simulations to record longer steady-state traces — which would you prefer?
