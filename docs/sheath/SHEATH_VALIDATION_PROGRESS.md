# Sheath Validation Progress

## Current status

- Plan and analysis are documented in `docs/sheath/SHEATH_VALIDATION_IMPLEMENTATION_PLAN.md` and `docs/sheath/SHEATH_VALIDATION_ANALYSIS.md`.
- The current branch is `PffdtdSheath`.
- Existing `Sd` sweep outputs exist under `results/sheath_sweep/sd*/data.vc` and `data.fd`.
- The long-run analysis found no clean Im{Z}=0 resonance crossing in the original broadband analysis band.
- The low-frequency analyzer validation was run on existing `results/sheath_long/sd0/data.vc` with `--fmax 200000 --decimate 10 --trim_seconds 0.0001 --peak_fmax 200000`.
- Result: no zero-crossing found; fallback peak at 46.845 kHz.

## Verified constraints

- Do not run another long broadband sheath test until the analysis method is confirmed.
- Focus first on validating the low-frequency signal-processing flow with existing data.
- Use a narrow-band or low-`fmax` analysis path before committing to expensive simulations.

## Current experiment: Optimized narrow-band sweep

**Status:** Running (started May 20, ~13:40 UTC)
**Parameters:**
- Frequencies: 20, 30, 40 kHz (sequential runs)
- MaxIter per frequency: 50,000 (down from 200,000)
- T (simulated time): 100 ms (down from 2000 ms)
- VcRate: 10
- Expected duration: ~10-12 hours total (3-4 hours per frequency)

**Rationale:**
- 50k iterations sufficient for steady-state equilibration
- 100 ms gives 10 Hz frequency resolution (adequate for impedance in 20-40 kHz band)
- Reduces runtime by ~95% compared to initial 200k/2000 setup
- Enables rapid iteration and validation before committing to longer runs

## Next steps

1. ✅ Validate the analyzer with `--fmax`, `--decimate`, and `--trim_seconds` on existing `.vc` files.
2. 🔄 Run optimized narrow-band sweep for 20, 30, 40 kHz (in progress)
3. Analyze completed narrow-band `.vc` files with the verified analyzer
4. Confirm resonance behavior and compare to long-run baseline
5. Only then, if needed, run targeted follow-up frequencies or longer broadband cases

## Notes

- The goal is to preserve the current implementation plan while avoiding wasted long runs.
- `scripts/run_sheath_narrow_band.ps1` is the first implementation artifact for the next experimental phase.
- Previous 3-day run of 200k/2000 was cancelled to adopt faster turnaround parameters.
