# Project Documentation Index

All paths relative to `projects/tu2008-sheath/`.

## Start here (paper program)

| Goal | Document |
|------|----------|
| Program overview | [../README.md](../README.md) |
| **Linear chronology (hindsight)** | [../CHRONICLE.md](../CHRONICLE.md) |
| Locked decisions / fidelity ladder | [../PROJECT_GUIDE.md](../PROJECT_GUIDE.md) |
| Dashboard | [../STATUS.md](../STATUS.md) |
| **Paper 0** — campaign chronicle | [../paper0_sheath_campaign/](../paper0_sheath_campaign/) |
| **Paper 1** — static \(C_\mathrm{sh}\) | [../paper1_static_sheath_capacitance/](../paper1_static_sheath_capacitance/) |
| **Paper 2** — oscillating \(r_s(t)\) | [../paper2_oscillating_sheath_boundary/](../paper2_oscillating_sheath_boundary/) · [SCIENCE.md](../paper2_oscillating_sheath_boundary/SCIENCE.md) |
| **Paper 3** — self-consistent sheath | [../paper3_self_consistent_sheath/](../paper3_self_consistent_sheath/) |

## Paper 0 campaign findings

| Goal | Document |
|------|----------|
| Coupling bug post-mortem | [../paper0_sheath_campaign/analysis/sheath_coupling_findings.md](../paper0_sheath_campaign/analysis/sheath_coupling_findings.md) |
| Low-f CW findings (Sep 2026) | [../paper0_sheath_campaign/analysis/cw_lowf_findings.md](../paper0_sheath_campaign/analysis/cw_lowf_findings.md) |
| Tu discrepancy / series-\(C\) | [../paper0_sheath_campaign/analysis/tu_discrepancy_discussion.md](../paper0_sheath_campaign/analysis/tu_discrepancy_discussion.md) |
| Figures | [../paper0_sheath_campaign/analysis/figures/](../paper0_sheath_campaign/analysis/figures/) |
| Data tables | [../paper0_sheath_campaign/analysis/data/](../paper0_sheath_campaign/analysis/data/) |

Root [`../analysis/`](../analysis/) is a **redirect** only.

## Shared science docs

| Goal | Document |
|------|----------|
| Sheath models (Balmain / Liu / Song / Tu / FDTD) | [SHEATH_MODELS_LITERATURE_DISCUSSION.md](SHEATH_MODELS_LITERATURE_DISCUSSION.md) |
| **Voltage vs current drive (Tu charging workaround?)** | [VOLTAGE_VS_CURRENT_DRIVE.md](VOLTAGE_VS_CURRENT_DRIVE.md) |
| Implementation plan (legacy campaign) | [SHEATH_VALIDATION_IMPLEMENTATION_PLAN.md](SHEATH_VALIDATION_IMPLEMENTATION_PLAN.md) |
| Pulse-FFT analysis | [SHEATH_VALIDATION_ANALYSIS.md](SHEATH_VALIDATION_ANALYSIS.md) |
| Progress notes | [SHEATH_VALIDATION_PROGRESS.md](SHEATH_VALIDATION_PROGRESS.md) |
| LaTeX report | [../validation/phase_7_documentation/main.pdf](../validation/phase_7_documentation/main.pdf) |

## Key figures (copies also under `docs/figures/` for lit note)

| Figure | Canonical (Paper 0) |
|--------|---------------------|
| Low-f Z zoom | [../paper0_sheath_campaign/analysis/figures/cw_lowf_impedance_zoom.png](../paper0_sheath_campaign/analysis/figures/cw_lowf_impedance_zoom.png) |
| Combined 0.5–2.3 MHz | [../paper0_sheath_campaign/analysis/figures/cw_lowf_impedance.png](../paper0_sheath_campaign/analysis/figures/cw_lowf_impedance.png) |
| \(f_\mathrm{res}(S_d)\) | [../paper0_sheath_campaign/analysis/figures/cw_lowf_resonance.png](../paper0_sheath_campaign/analysis/figures/cw_lowf_resonance.png) |

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/run_paper2_rs_t_pilot.ps1` | Paper 2: static vs oscillating \(r_s(t)\) single-tone pilot |
| `scripts/analyze_paper2_pilot.py` | Paper 2: phasor \(Z\) + bracket metrics → `paper2_.../analysis/` |
| `scripts/analyze_paper2_soft_edge.py` | Paper 2: soft-edge width sensitivity (0.5/1/2) vs soft-pilot brackets |
| `scripts/run_paper2_soft_edge_sens.ps1` | Paper 2: osc soft-edge=0.5,2 at fixed \(\Delta r=1\) |
| `scripts/run_paper2_sparse_f.ps1` | Paper 2: sparse-\(f\) soft pilot (500 kHz, 1.2 MHz) |
| `scripts/analyze_paper2_sparse_f.py` | Paper 2: sparse-\(f\) bracket metrics + figures |
| `scripts/run_paper2_phase_scan.ps1` | Paper 2: soft phase scan \(\phi\) at 700 kHz |
| `scripts/analyze_paper2_phase.py` | Paper 2: phase + harmonic diagnostics |
| `scripts/run_paper2_delta_r_matched.ps1` | Paper 2: \(\Delta r\) with \(\mathrm{soft}=c\Delta r\) |
| `scripts/analyze_paper2_delta_r_matched.py` | Paper 2: matched soft \(\Delta r\) metrics + figures |
| `scripts/make_paper2_pub_figures.py` | Paper 2: regenerate manuscript figures (publication style, 300 dpi) |
| `scripts/run_sheath_cw_lowf.ps1` | Low-f CW 0.5–1.5 MHz, Sd=0,2,10 |
| `scripts/run_sheath_sweep.ps1` | Broadband pulse Sd sweep |
| `scripts/run_sheath_cw_tu.ps1` | Dense CW Tu band sweep |
| `scripts/analyze_cw_tu_partial.py` | CW plots/tables → `paper0_sheath_campaign/analysis/` (update paths if re-run) |
| `scripts/analyze_sheath_results.py` | Pulse FFT impedance |
| `scripts/config.ps1` | Repo paths, inputs sync |

Results always land under **`<collab-repo-root>/results/`** (gitignored). Do not set `$env:PFFDtd_ROOT`.

## Validation phases (raw archive)

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
