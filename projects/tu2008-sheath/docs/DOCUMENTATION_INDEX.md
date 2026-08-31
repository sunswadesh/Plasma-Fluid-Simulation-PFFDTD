# Project Documentation Index

All paths relative to `projects/tu2008-sheath/`.

## Start here

| Goal | Document |
|------|----------|
| Project overview | [../README.md](../README.md) |
| Phase status | [../STATUS.md](../STATUS.md) |
| Coupling bug post-mortem | [../analysis/sheath_coupling_findings.md](../analysis/sheath_coupling_findings.md) |
| Implementation plan | [SHEATH_VALIDATION_IMPLEMENTATION_PLAN.md](SHEATH_VALIDATION_IMPLEMENTATION_PLAN.md) |
| Pulse-FFT analysis | [SHEATH_VALIDATION_ANALYSIS.md](SHEATH_VALIDATION_ANALYSIS.md) |
| Progress notes | [SHEATH_VALIDATION_PROGRESS.md](SHEATH_VALIDATION_PROGRESS.md) |
| LaTeX report | [../validation/phase_7_documentation/main.pdf](../validation/phase_7_documentation/main.pdf) |

## Scripts (no runs from this index — edit/run manually when ready)

| Script | Purpose |
|--------|---------|
| `scripts/run_sheath_sweep.ps1` | Broadband pulse Sd sweep |
| `scripts/run_sheath_cw_tu.ps1` | Dense CW Tu band sweep |
| `scripts/analyze_cw_tu_partial.py` | CW Tu plots and tables → `analysis/` |
| `scripts/analyze_sheath_results.py` | Pulse FFT impedance |
| `scripts/config.ps1` | `$PFFDtd_ROOT`, inputs sync |

Set `$env:PFFDtd_ROOT` only if the repo root is not the default (two levels above `scripts/`). Results land under `<repo-root>/results/`.

## Validation phases

| Phase | Folder |
|-------|--------|
| 0 | [../validation/phase_0_february_baseline/](../validation/phase_0_february_baseline/) |
| 1 | [../validation/phase_1_pulse_sd_sweep/](../validation/phase_1_pulse_sd_sweep/) |
| 2 | [../validation/phase_2_narrowband_cw/](../validation/phase_2_narrowband_cw/) |
| 3 | [../validation/phase_3_fp_screen/](../validation/phase_3_fp_screen/) |
| 4 | [../validation/phase_4_coupling_fix/](../validation/phase_4_coupling_fix/) |
| 5 | [../validation/phase_5_postfix_confirm/](../validation/phase_5_postfix_confirm/) |
| 6 | [../validation/phase_6_cw_tu/](../validation/phase_6_cw_tu/) |
| 7 | [../validation/phase_7_documentation/](../validation/phase_7_documentation/) |

## References

PDFs in [../data/references/](../data/references/) (Tu 2008 JGR, etc.).

PFFDtd solver docs remain at `D:\Swadesh\Work\Models\Pffdtd\docs\`.
