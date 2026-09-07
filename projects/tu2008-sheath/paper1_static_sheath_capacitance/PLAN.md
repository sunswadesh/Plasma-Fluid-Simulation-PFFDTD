# Paper 1 — Plan checklist

Last updated: 2026-09-07

## Near term

- [ ] Free-space CW resonance on the same dipole (`scripts/` + new result tag)
- [ ] Script: extract \(C_\mathrm{eff}(S_d)\) from low-\(f\) Im\(\{Z\}\) (reuse `results/sheath_cw_tu/` low-f cases)
- [ ] Table: \(C_\mathrm{eff}\) vs \(C_\mathrm{sh}^\mathrm{(coax)}\) for \(S_d=2,10\) (and 0 if defined)
- [ ] Note staircasing / \(r_\mathrm{eff}\) choice in `analysis/ceff_notes.md`
- [ ] Figures: \(C_\mathrm{eff}(S_d)\); optional overlay of Song static \(C(r_s)\) formula

## Manuscript scaffolding

- [ ] Outline in `draft/outline.md` (Intro: campaign → series C; Methods: PF-FDTD + Sd; Results; Discussion vs Liu/Song static)
- [ ] Pull key figures from `../analysis/figures/` and phase-7 report
- [ ] Explicit “not Tu dynamic fidelity” disclaimer in Discussion

## Done (campaign inheritance)

- [x] PEC-seeded sheath coupling
- [x] Dense CW 1.5–2.3 MHz
- [x] Low-f CW 0.5–1.5 MHz, \(S_d=0,2,10\)
- [x] Literature reframe (Song/Tu/Liu) in `docs/SHEATH_MODELS_LITERATURE_DISCUSSION.md`
