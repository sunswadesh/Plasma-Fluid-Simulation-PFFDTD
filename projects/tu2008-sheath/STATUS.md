# Project Status Dashboard

Last updated: 2026-09-07

## Program structure

| Doc / folder | Role |
|--------------|------|
| [README.md](README.md) | Science motivation + paper map |
| [CHRONICLE.md](CHRONICLE.md) | Linear hindsight development story |
| [PROJECT_GUIDE.md](PROJECT_GUIDE.md) | Locked decisions, fidelity ladder |
| [paper0_sheath_campaign/](paper0_sheath_campaign/) | Paper 0 — campaign chronicle + analysis archive |
| [paper1_static_sheath_capacitance/](paper1_static_sheath_capacitance/) | Paper 1 — \(C_\mathrm{eff}(S_d)\) vs coax |
| [paper2_oscillating_sheath_boundary/](paper2_oscillating_sheath_boundary/) | Paper 2 — kinematic \(r_s(t)\) |
| [paper3_self_consistent_sheath/](paper3_self_consistent_sheath/) | Paper 3 — fluid charging and/or PIC |
| [analysis/](analysis/) | Redirect only → paper0 analysis |

## Paper-task status

| Paper | Status | Notes |
|-------|--------|-------|
| 0 — Campaign chronicle | **Complete (archive)** | Phases 0–8 evidence under `paper0_.../analysis/` |
| 1 — Static \(C_\mathrm{sh}\) | **Active** | Free-space + \(C_\mathrm{eff}\) extraction open |
| 2 — Oscillating boundary | Design only | After Paper 1 methods freeze (recommended) |
| 3 — Self-consistent | Gated | No implementation until Paper 1 (+ ideally 2) |

## Campaign phases (raw archive in `validation/`)

| Phase | Status | Notes |
|-------|--------|-------|
| 0 — February baseline | Complete | Free-space vs plasma dipole |
| 1 — Pulse Sd sweep | Complete | FFT method inconclusive pre-fix |
| 2 — Narrowband CW | Complete | Below \(f_p\) screen |
| 3 — fp screen | Complete | Clean resonance; Sd-independent pre-fix |
| 4 — Coupling fix | Complete | PEC-seeded sheath in `plasma.cpp` |
| 5 — Post-fix confirm | Complete | CW confirm at 1.7 / 1.9 MHz |
| 6 — CW Tu sweep | Complete | 66 cases, Aug 2026 |
| 7 — Documentation | Complete | LaTeX report (updated with low-f chapter) |
| 8 — Low-f CW | Complete | 0.5–1.5 MHz, Sd=0,2,10; Sep 2026 |

## Combined campaign conclusion (Paper 0 → Paper 1)

1. Plasma-loaded dipole impedance near \(f_p\) is measurable on this grid.
2. After the PEC-seeded fix, volumetric sheath **strongly** changes feed \(Z\).
3. With Im{Z} +→− as the metric: \(f_\mathrm{res}(0)\approx1.85\,\mathrm{MHz}\), \(f_\mathrm{res}(2)\approx0.66\,\mathrm{MHz}\), \(f_\mathrm{res}(10)\lesssim0.50\,\mathrm{MHz}\) — series-\(C\) behavior.
4. Paper 1 reframes success as \(C_\mathrm{eff}(S_d)\) vs analytic coax / Song static.

## Open items (Paper 1 first)

- [ ] Free-space \(f_\mathrm{res}\) anchor on the same dipole grid
- [ ] Map low-\(f\) capacitive asymptote → \(C_\mathrm{eff}(S_d)\) vs coax
- [ ] Optional denser tones around \(S_d=2\) ~0.55–0.75 MHz
- [ ] Paper 1 draft outline in `paper1_static_sheath_capacitance/draft/`

## PFFDtd solver (this repo)

- Branch: `PffdtdSheath` in this collab repo
- Build: `compile.bat` or `cmake --build build --target pffdtd_parallel` → `pffdtd_parallel.exe` at repo root
- Sheath implementation: `src/physics/plasma.cpp`, reference header `plasmaNSheath.h`
- **Results:** `<repo-root>/results/` (gitignored). Do not set `$env:PFFDtd_ROOT`.

## Key figures (Paper 0 archive)

| Figure | Path |
|--------|------|
| Low-f Z (zoom) | [paper0_sheath_campaign/analysis/figures/cw_lowf_impedance_zoom.png](paper0_sheath_campaign/analysis/figures/cw_lowf_impedance_zoom.png) |
| Combined 0.5–2.3 MHz | [paper0_sheath_campaign/analysis/figures/cw_lowf_impedance.png](paper0_sheath_campaign/analysis/figures/cw_lowf_impedance.png) |
| \(f_\mathrm{res}(S_d)\) | [paper0_sheath_campaign/analysis/figures/cw_lowf_resonance.png](paper0_sheath_campaign/analysis/figures/cw_lowf_resonance.png) |
| Findings note | [paper0_sheath_campaign/analysis/cw_lowf_findings.md](paper0_sheath_campaign/analysis/cw_lowf_findings.md) |
| Discrepancy note | [paper0_sheath_campaign/analysis/tu_discrepancy_discussion.md](paper0_sheath_campaign/analysis/tu_discrepancy_discussion.md) |
| Report PDF | [validation/phase_7_documentation/main.pdf](validation/phase_7_documentation/main.pdf) |

## Next actions

1. Execute Paper 1 checklist (`paper1_static_sheath_capacitance/PLAN.md`)
2. Design-only notes for Paper 2 \(r_s(t)\) when ready
3. Paper 3 remains gated
