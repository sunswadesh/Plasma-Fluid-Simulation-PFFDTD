# Sheath validation (Tu 2008)

Branch: **`PffdtdSheath`**

Reproduce the upward shift of dipole series resonance \(f_\mathrm{res}\) with vacuum sheath width \(S_d\), per Tu et al. (2008, JGR).

## Status (August 2026)

- Coupling bug fixed: sheath now seeds from PEC after geometry setup.
- Dense CW sweep at \(f_p = 2\,\mathrm{MHz}\) complete (66 cases).
- \(f_\mathrm{res}(S_d=0) \approx 1.846\,\mathrm{MHz}\); no Im\(\{Z\}\) crossing for \(S_d \ge 2\) in the 1.5–2.3 MHz band with the current observable.

## In this repo

| Document | Purpose |
|----------|---------|
| [Implementation plan](SHEATH_VALIDATION_IMPLEMENTATION_PLAN.md) | Campaign design and acceptance criteria |
| [Pulse-FFT analysis](SHEATH_VALIDATION_ANALYSIS.md) | Early sweep post-mortem |
| [Progress notes](SHEATH_VALIDATION_PROGRESS.md) | Running status |
| [Coupling findings](../../analysis/sheath_coupling_findings.md) | Why pre-fix sweeps failed + fix summary |

Inputs: `sheath.str`, `sheath_sine.str`, `sheath_sine_vc.str` (repo root).

Run drivers and analyzers: `scripts/run_sheath_*`, `scripts/analyze_*`, `scripts/plot_sheath.py`.

Results (local, gitignored): `results/sheath_*/`.

## External (collaborator / PI report)

LaTeX progress report, reference PDFs, and archived root plots:

`D:\Swadesh\Work\Impedance Probe\PiP Alireza\2026 Collab_PFFDTD_Sheath`

- Report PDF: `report/main.pdf` (build with `report/compile.bat`)
- References: `references/Tu2008_JGR_plasma_sheath.pdf`

When updating the report after analysis, copy fresh figures from `analysis/figures/` into `report/figures/` in the collab folder, then recompile.
