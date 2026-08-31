# Project Status Dashboard

Last updated: 2026-08-30

## Phase summary

| Phase | Status | Notes |
|-------|--------|-------|
| 0 — February baseline | Complete | Free-space vs plasma dipole |
| 1 — Pulse Sd sweep | Complete | FFT method inconclusive pre-fix |
| 2 — Narrowband CW | Complete | Below \(f_p\) screen |
| 3 — fp screen | Complete | Clean resonance; Sd-independent pre-fix |
| 4 — Coupling fix | Complete | PEC-seeded sheath in `plasma.cpp` |
| 5 — Post-fix confirm | Complete | CW confirm at 1.7 / 1.9 MHz |
| 6 — CW Tu sweep | Complete | 66 cases, Aug 2026 |
| 7 — Documentation | Complete | LaTeX report in `validation/phase_7_documentation/` |

## Completed

- [x] Sheath coupling bug diagnosed and fixed
- [x] Dense CW sweep at \(f_p = 2\,\mathrm{MHz}\) (1.5–2.3 MHz, Sd = 0–10)
- [x] Campaign reorganized under `projects/tu2008-sheath/` (STORMS-style)
- [x] Analysis summaries in `analysis/data/`

## Open items

- [ ] Tu upward \(f_\mathrm{res}(S_d)\) shift not reproduced with Im\(\{Z\}\) crossing observable for \(S_d \ge 2\)
- [ ] Denser frequency search or alternate observable if shift curve is required

## PFFDtd solver

- Branch: `PffdtdSheath` at `D:\Swadesh\Work\Models\Pffdtd`
- Sheath implementation: `src/physics/plasma.cpp`, reference header `plasmaNSheath.h`

## Next actions (when resuming)

1. Review `analysis/data/cw_tu_summary.txt` and chapter 7 of the report
2. Decide whether to extend CW band or change resonance metric
3. Copy fresh figures from `analysis/figures/` to `validation/phase_7_documentation/figures/` before report updates
