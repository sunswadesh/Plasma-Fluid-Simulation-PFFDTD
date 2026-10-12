# Paper 1 — Plan checklist

Last updated: 2026-09-15

## Manuscript policy (editorial)

- **Do not cite or name Liu et al. in the Radio Science manuscript** while that work remains unpublished. Keep internal comparison in `docs/SHEATH_MODELS_LITERATURE_DISCUSSION.md` only.
- **Public lineage:** series coax sheath from Mlodnosky \& Garriott (1962) through Balmain-era gap/jacket models (Galejs, Adachi, …) to modern probe analyses (Brooks \& Paliwoda 2024).

## Review response (2026-09-14)

- [x] Fix coax comparison: dipole \(C_\mathrm{sh}=C_\mathrm{mono}/4\) (was falsely “scale factor 0.3”)
- [x] Critique 3 (2026-10-10): demoted C_eff '~20%' headline claim (option 3) — abstract/conclusions report factor ~1.2 as a consistency check, scatter comparable to the agreement; geometric r_eff band [0.23,0.64]dx from the staircase wire (Holland/equal-area/equal-perimeter/inscribed), shaded in fig:ceffsd; band means imply r_eff ~0.35/0.40dx inside the band (consistency, not a measurement)
- [x] Primary evidence = \(\mathrm{Im}\{Z\}(S_d)\) at fixed \(f\); report near-\(f_p\) reversal
- [x] Circuit overlay \(Z(S_d=0)+1/(j\omega C_\mathrm{dip})\); show \(\mathrm{Re}\{Z\}\) failure
- [x] Critique 4 resolved 2026-10-12: denser Sd=2 tones (0.55, 0.625 MHz, both capacitive) bracket the lone 0.60 MHz inductive sample — no crossing established; 0.655 MHz value retired from text, table, and fres figure; new tones stitched into z_lowf/z_combined
- [x] Complete methods: \(\nu\), species, \(T\), \(\Delta t\), ABC, hard \(E_z\), \(V/I\) definition, domain size
- [x] Bibliography: Brooks DOI; Mlodnosky & Garriott; Galejs; Lee (Radio Science)
- [x] Drop internal Paper 0 cite from manuscript body
- [x] Quasi-static solver anchor for $S_d=0$ (2026-10-09): $C_\mathrm{fs}=4.62$ pF from the plasma-off pilot; $Z_\mathrm{qs}=1/(j\omega C_\mathrm{fs}\varepsilon_p)$ vs simulated $S_d=0$ in `analysis/data/qs_anchor_sd0.txt`, dashed overlay in `z_combined.png`, anchor subsection in the manuscript (sign + crossing 1.99 vs 1.846 MHz; Im within ~50% at 0.5–0.8 MHz; Re excess 4–9x noted)
- [ ] Box-size convergence: 105x105x98 grid, $S_d=0,2$ at 1.70 MHz (queued overnight 2026-10-09, `run_convergence.sh`)
- [ ] Free-space CW on the same dipole (`analysis/FREE_SPACE_CONTROL.md`) — pilot 1.5 MHz done; 1.5–2.3 MHz sweep running 2026-10-09
- [ ] Low-\(f\) CW for \(S_d=4,6,8\) + denser \(S_d=2\) tones (`analysis/LOWF_INTERMEDIATE_PLAN.md`)
- [ ] Fill author list, affiliations, corresponding address
- [ ] Replace Open Research with archival DOI

## Manuscript scaffolding

- [x] Radio Science / AGU draft: `draft/paper1_radioscience.tex` (+ PDF rebuild)
- [x] Science-first wiring (2026-10-08): Song/Tu demoted to one context citation; Discussion carries a “Scope: what a prescribed jacket represents” subsection; three science questions (topology, scaling, separability) organize the paper
- [x] Series-jacket geometry + all \(S_d\) in the dense band

## Done (campaign inheritance)

- [x] PEC-seeded sheath coupling
- [x] Dense CW 1.5–2.3 MHz
- [x] Low-f CW 0.5–1.5 MHz, \(S_d=0,2,10\)
- [x] Literature reframe (Song/Tu/Liu) in `docs/SHEATH_MODELS_LITERATURE_DISCUSSION.md`
