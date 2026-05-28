# Sheath Validation Implementation Plan

## Status: VALIDATION IN PROGRESS
- Branch: `PffdtdSheath`
- Started: 2026-05-05
- Current focus: complete validation of sheath resonance behavior using improved low-frequency signal conditioning and/or narrow-band excitation.
- Policy: do not execute further long broadband sheath runs until the analysis methodology is confirmed with existing data and narrow-band test planning.

---

## 1. Objectives

Reproduce the impedance shift of a dipole antenna immersed in plasma when a vacuum sheath layer surrounds the antenna structure, as described in Tu (2008). The sheath is a region of depleted plasma density adjacent to the conductor surface. Increasing sheath width should shift the antenna resonance frequency upward (toward free-space value) because the effective dielectric loading is reduced near the antenna.

**Key physics:** A conducting antenna in plasma develops a sheath (ion-rich, electron-depleted region) of width `Sd` cells. Inside the sheath the plasma density is zero (step profile) or transitions from zero to bulk (gradient profile). This changes the effective permittivity seen by the antenna and shifts its input impedance spectrum.

---

## 2. Outputs / Observables

| Observable | Source | Units |
|---|---|---|
| V(t) — antenna voltage | `.vc` file column 2 | V (FDTD normalized) |
| I(t) — antenna current | `.vc` file column 3 | A (FDTD normalized) |
| Z(f) = DFT{V(t)} / DFT{I(t)} | post-processing | Ohms |
| f_res — resonance frequency (Im{Z}=0 crossing) | from Z(f) | Hz |
| Δf_res vs Sd — resonance shift curve | sweep output | Hz vs cells |

---

## 3. Normalization Rules

1. **Time axis:** `t_n = n * dt`, where `dt` is computed from CFL condition on grid spacing.
2. **Frequency axis:** `f_k = k / (N_samples * dt)`, standard DFT bin spacing.
3. **Windowing:** Apply Hanning window to V(t) and I(t) before DFT to suppress spectral leakage.
4. **Impedance:** `Z(f) = V(f) / I(f)` directly in FDTD units. Since V and I are recorded at the same feed point with consistent FDTD normalization (V = E*dx, I from contour integral of H), Z has physical units of Ohms.
5. **Density:** `N_0 = 4π² f_p² m_e ε₀ / e²` computed from input `FREQ_PLASMA` (Hz).

---

## 4. Sweep Protocol

### Parameter: Sheath Width `Sd`
- Values: [0, 2, 4, 6, 8, 10] cells
- `Sd = 0` is the reference (no sheath, full plasma contact with antenna)

### Density Profile (sub-parameter)
- **Step profile (primary):** density = 0 for distance ≤ Sd from antenna, density = N_0 otherwise
- **Linear gradient (optional follow-up):** density ramps linearly from 0 at antenna surface to N_0 at distance Sd

### Fixed Parameters (per sweep)
| Parameter | Value | Notes |
|---|---|---|
| FREQ_PLASMA | 200000 Hz | Low-density plasma |
| FREQ_COL | 0.1 | Collision ratio |
| FREQ_CYC | 0 Hz | No magnetic field |
| T | 2000 K | Warm plasma |
| Source | 30 kHz D-Gaussian | Broadband excitation |
| Grid | 70×70×65, dx=0.04m | From sheath.str |
| Iterations | 64000 | 30 plasma cycles |

### Execution
```
for Sd in 0 2 4 6 8 10:
    pffdtd_parallel.exe sheath results/sheath_sweep/sd{Sd} 200000 0.1 0 0 0 2000 {Sd}
```

---

## 5. Implementation-Path Decision Gate

### Decision: Active path first

| Criterion | Active Path (plasma.cpp) | Legacy Path (plasmaNSheath.h) |
|---|---|---|
| Array layout | Flat 1D with IDX5 macro | 5D pointer-to-pointer |
| OpenMP ready | Yes (already parallelized) | No |
| Memory efficiency | Good (contiguous) | Poor (scattered allocations) |
| Maintenance | Single compilation unit | Header-only, no modularity |
| Integration | Already linked in CMakeLists.txt | Would require build changes |

**Decision:** Implement sheath in `src/physics/plasma.cpp` using a new `N0_SPATIAL` flat array (IDX3-indexed, per-species offset). The legacy `plasmaNSheath.h` serves as reference for the density-profile logic only.

**Rationale:** The active path already uses flat arrays with OpenMP parallelization. Adding a spatially-varying ambient density array is a minimal, non-breaking change that preserves all existing physics.

---

## 6. Verification Metrics

1. **Resonance shift direction:** f_res must increase monotonically with Sd (sheath removes dielectric loading → frequency moves toward free-space value).
2. **Impedance continuity:** Z(f) curves must be smooth (no discontinuities or spikes from numerical artifacts at sheath boundary).
3. **Energy conservation:** Total electromagnetic energy should not grow unbounded. Check that max(|E|) and max(|V|) remain bounded for all Sd values.
4. **Sd=0 baseline:** Must match the existing no-sheath plasma simulation (regression check).
5. **Stability:** All sweep runs complete without NaN/Inf in output.

---

## 7. Acceptance Criteria

- [x] All 6 sweep cases (Sd=0..10) run to completion without crash
- [ ] Z(f) plots show clear resonance peak for each Sd
- [ ] Resonance frequency shifts upward with increasing Sd (sheath removes dielectric loading → frequency moves toward free-space value)
- [ ] Sd=0 case matches pre-sheath baseline (no regression)
- [ ] No NaN/Inf in any `.vc` output file
- [x] Implementation uses active-path code only (no legacy header inclusion)
- [ ] Build passes on Windows with CMake (Release and Debug configs)

### 7.1 Current validation status

- Sweep execution is complete and outputs exist for Sd = 0,2,4,6,8,10.
- The current analysis found no clean Im{Z} zero-crossing in the broadband 1 MHz band.
- Reported peaks are in the multi-GHz range and are likely FFT artifacts, so the physical resonance remains unvalidated.
- The top remaining work is improved low-frequency analysis and/or a narrow-band measurement plan.

---

## 8. Implementation Path

### Files to Modify
1. `src/physics/plasma.h` — add `Sd` extern, `N0_SPATIAL` extern
2. `src/physics/plasma.cpp` — add `N0_SPATIAL` allocation, sheath profile init, update `Ucalc`/`Ncalc`/`Ecalcmod` to use spatial density
3. `src/pffdtd.cpp` — add `Sd` CLI arg (argv[9])

### Files to Create
1. `scripts/run_sheath_sweep.bat` — sweep driver
2. `scripts/run_sheath_narrow_band.ps1` — narrow-band frequency sweep driver

---

## 9. Implementation Status

This file tracks progress and findings to date. See the companion analysis document `docs/SHEATH_VALIDATION_ANALYSIS.md` for measured results and plots.

### 9.1 Work Completed
- Executables relocated into `build/` for consistent invocation on Windows.
- Sweep driver created and executed: `scripts/run_sheath_sweep.ps1` / `scripts/run_sheath_sweep.bat` produced results under `results/sheath_sweep/sd{Sd}` for Sd = 0,2,4,6,8,10.
- Robust post-processing script added: `scripts/analyze_sheath_results.py` which parses `.vc` files, computes DFTs and `Z(f)` and saves `sheath_impedance.png`, `sheath_resonance_shift.png`, and `sheath_resonance_summary.txt`.

### 9.2 Issues Encountered
- Some `.vc` outputs contained non-numeric or irregular rows which broke simple `numpy.loadtxt` parsing; analyzer now filters non-numeric lines.
- The DFT frequency axis for the current recorded traces places significant energy in very high-frequency bins (due to sampling cadence and length), so the expected physical resonance in the kHz band was not detected as an Im{Z} zero-crossing within the original analysis band (f ≤ 1 MHz).

### 9.3 Short Summary of Findings
- All sweep runs completed and produced `data.vc` and `data.fd` files for Sd = 0,2,4,6,8,10.
- No clear Im{Z} zero-crossing (series resonance) was found within f ≤ 1 MHz for any Sd using the present time-series data.
- As a fallback the analyzer reports the frequency bin of maximum |Z| (peak magnitude) for each run in `sheath_resonance_summary.txt`. These peak bins currently fall at very high-frequency bins and are likely sampling/DFT artifacts rather than the physical resonance reported by Tu (2008).

### 9.4 Next Steps (recommended)
1. Re-run analysis focusing on a lower-frequency band (e.g., `fmax = 200e3`) and/or decimate the time-series to reduce Nyquist frequency and better resolve kHz-range features.
2. Ensure V(t)/I(t) recordings contain steady-state data (extend recording duration and/or trim initial transient) before computing DFT.
3. If frequency-domain identification remains ambiguous, execute the narrow-band / long-record plan in Section 10.

## 10. Narrow-band and long-record plan

Purpose: obtain a robust, low-frequency resonance measurement for sheath validation by improving DFT frequency resolution and/or measuring impedance with a narrow-band source sweep.

### 10.1 Key requirements
- Frequency resolution: `df = 1 / T`. To target ~1 kHz resolution, record at least `T >= 1 ms` of physical simulation time.
- Nyquist frequency: `fs = 1/dt` must exceed `2 * f_max_interest`. For `f_max_interest = 200 kHz`, `fs >= 400 kHz`.
- Practical approach: reduce output frequency by recording every `vc_rate` iterations while increasing the total number of iterations.

### 10.2 Recommended execution modes

#### Option A — Broadband long-record run (preferred first pass)
- Keep broadband excitation.
- Run long enough to capture many cycles of the expected resonance.
- Record V/I less often using the new output-stride parameter.
- Trim the initial transient before FFT in the analyzer.

#### Option B — Narrow-band sweep (fallback or confirmation)
- Run a series of single-tone simulations at candidate frequencies.
- Measure steady-state input voltage/current for each frequency.
- Assemble `Z(f)` from the frequency-stepped results.
- This approach is faster for locating a resonance when the broadband DFT is ambiguous.

### 10.3 Runtime parameters
- The simulator now supports the following extra positional arguments:
  - argument 10: `vc_rate` — write V/I every `vc_rate` iterations
  - argument 11: `max_iter` — override the maximum iteration count

Example broadband long-record command:
```powershell
$p = Join-Path (Get-Location) 'build\pffdtd_parallel.exe'
& $p 'sheath' 'results\sheath_long\sd4\data' 200000 0.1 0 0 0 1000000 10 1000000 > 'results\sheath_long\sd4\simulation.log' 2>&1
```

Example narrow-band sweep loop:
```powershell
$exepath = Join-Path (Get-Location) 'build\pffdtd_parallel.exe'
$freqs = @(20000,25000,30000,35000,40000)
$Sd = 4
foreach($f in $freqs) {
  $outdir = Join-Path 'results\sheath_sweep_narrow' ("sd$Sd\f$f")
  if(-not (Test-Path $outdir)) { New-Item -ItemType Directory -Path $outdir | Out-Null }
  & $exepath 'sheath' (Join-Path $outdir 'data') $f 0.1 0 0 0 20000 $Sd 10 200000 > (Join-Path $outdir 'simulation.log') 2>&1
}
```

### 10.4 Notes
- Use `vc_rate` to limit output size while preserving total simulated time.
- Prefer trimming the initial transient before computing the FFT.
- Validate the `Sd=0` baseline explicitly during this execution phase.

Files of interest (workspace):
- [scripts/analyze_sheath_results.py](scripts/analyze_sheath_results.py#L1)
- [sheath_impedance.png](sheath_impedance.png)
- [sheath_resonance_summary.txt](sheath_resonance_summary.txt#L1-L20)
- Output directories: `results/sheath_sweep/sd*/`

This plan file will be revisited after the recommended next steps are executed.

### 9.5 Recent Changes Committed

The following artifacts were added during the current work and are now part of the branch `PffdtdSheath`:

- `scripts/analyze_sheath_results.py` — improved analyzer with CLI options `--fmax`, `--decimate`, and `--trim_seconds` for focused analysis of the impedance and steady-state trimming/decimation.
- `docs/SHEATH_VALIDATION_ANALYSIS.md` — analysis summary document with measured results and recommendations.
- `scripts/run_sheath_long_trace.ps1` — helper PowerShell script template to run long-recording simulations for a single `Sd`.

All changes have been committed to the local repository and pushed to the remote branch `PffdtdSheath` (see repository history for commit details).
