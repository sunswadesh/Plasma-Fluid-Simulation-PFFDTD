# Project Documentation Index

All paths relative to `projects/tu2008-sheath/`.

## Start here (three-paper program)

| Goal | Document |
|------|----------|
| Program overview (science + tasks) | [../README.md](../README.md) |
| Locked decisions / fidelity ladder | [../PROJECT_GUIDE.md](../PROJECT_GUIDE.md) |
| Phase + paper status | [../STATUS.md](../STATUS.md) |
| **Paper 1** — static \(C_\mathrm{sh}\) | [../paper1_static_sheath_capacitance/](../paper1_static_sheath_capacitance/) |
| **Paper 2** — oscillating \(r_s(t)\) | [../paper2_oscillating_sheath_boundary/](../paper2_oscillating_sheath_boundary/) |
| **Paper 3** — self-consistent sheath | [../paper3_self_consistent_sheath/](../paper3_self_consistent_sheath/) |

## Campaign science & findings

| Goal | Document |
|------|----------|
| Sheath models (Balmain / Liu / Song / Tu / FDTD) | [SHEATH_MODELS_LITERATURE_DISCUSSION.md](SHEATH_MODELS_LITERATURE_DISCUSSION.md) |
| Tu discrepancy discussion (Sep 2026) | [../analysis/tu_discrepancy_discussion.md](../analysis/tu_discrepancy_discussion.md) |
| Low-f CW findings (Sep 2026) | [../analysis/cw_lowf_findings.md](../analysis/cw_lowf_findings.md) |
| Coupling bug post-mortem | [../analysis/sheath_coupling_findings.md](../analysis/sheath_coupling_findings.md) |
| Implementation plan (legacy campaign) | [SHEATH_VALIDATION_IMPLEMENTATION_PLAN.md](SHEATH_VALIDATION_IMPLEMENTATION_PLAN.md) |
| Pulse-FFT analysis | [SHEATH_VALIDATION_ANALYSIS.md](SHEATH_VALIDATION_ANALYSIS.md) |
| Progress notes | [SHEATH_VALIDATION_PROGRESS.md](SHEATH_VALIDATION_PROGRESS.md) |
| LaTeX report | [../validation/phase_7_documentation/main.pdf](../validation/phase_7_documentation/main.pdf) |

## Key figures (low-f + combined)

| Figure | Path |
|--------|------|
| Low-f Z zoom | [figures/cw_lowf_impedance_zoom.png](figures/cw_lowf_impedance_zoom.png) |
| Combined 0.5–2.3 MHz | [figures/cw_lowf_impedance.png](figures/cw_lowf_impedance.png) |
| \(f_\mathrm{res}(S_d)\) | [figures/cw_lowf_resonance.png](figures/cw_lowf_resonance.png) |
| Same files in analysis/ | [../analysis/figures/](../analysis/figures/) |

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/run_sheath_cw_lowf.ps1` | Low-f CW 0.5–1.5 MHz, Sd=0,2,10 |
| `scripts/run_sheath_sweep.ps1` | Broadband pulse Sd sweep |
| `scripts/run_sheath_cw_tu.ps1` | Dense CW Tu band sweep |
| `scripts/analyze_cw_tu_partial.py` | CW Tu plots and tables → `analysis/` |
| `scripts/analyze_sheath_results.py` | Pulse FFT impedance |
| `scripts/config.ps1` | Repo paths, inputs sync |

Results always land under **`<collab-repo-root>/results/`** (gitignored). Do not set `$env:PFFDtd_ROOT`. Optional `$env:PFFDtd_EXE_ROOT` only if the executable is outside the repo.

## Validation phases (campaign archive)

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
| 8 | [../validation/phase_8_lowf_cw/](../validation/phase_8_lowf_cw/) |

## References

PDFs in [references/](references/) (Song 2007 JGR, Tu 2008 JGR, etc.).

Solver docs: [../../../docs/](../../../docs/) at the collab repo root.
