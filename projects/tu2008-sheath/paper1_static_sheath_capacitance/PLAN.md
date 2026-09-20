# Paper 1 — Plan checklist

Last updated: 2026-09-15

## Manuscript policy (editorial)

- **Do not cite or name Liu et al. in the Radio Science manuscript** while that work remains unpublished. Keep internal comparison in `docs/SHEATH_MODELS_LITERATURE_DISCUSSION.md` only.
- **Public lineage:** series coax sheath from Mlodnosky \& Garriott (1962) through Balmain-era gap/jacket models (Galejs, Adachi, …) to modern probe analyses (Brooks \& Paliwoda 2024).

## Review response (2026-09-14)

- [x] Fix coax comparison: dipole \(C_\mathrm{sh}=C_\mathrm{mono}/4\) (was falsely “scale factor 0.3”)
- [x] Primary evidence = \(\mathrm{Im}\{Z\}(S_d)\) at fixed \(f\); report near-\(f_p\) reversal
- [x] Circuit overlay \(Z(S_d=0)+1/(j\omega C_\mathrm{dip})\); show \(\mathrm{Re}\{Z\}\) failure
- [x] Tone down \(f_\mathrm{res}(S_d)\) claims (bounds only for \(S_d=4,6,8\); provisional \(S_d=2\))
- [x] Complete methods: \(\nu\), species, \(T\), \(\Delta t\), ABC, hard \(E_z\), \(V/I\) definition, domain size
- [x] Bibliography: Brooks DOI; Mlodnosky & Garriott; Galejs; Lee (Radio Science)
- [x] Drop internal Paper 0 cite from manuscript body
- [ ] Free-space CW on the same dipole (`analysis/FREE_SPACE_CONTROL.md`)
- [ ] Low-\(f\) CW for \(S_d=4,6,8\) + denser \(S_d=2\) tones (`analysis/LOWF_INTERMEDIATE_PLAN.md`)
- [ ] Fill author list, affiliations, corresponding address
- [ ] Replace Open Research with archival DOI

## Manuscript scaffolding

- [x] Radio Science / AGU draft: `draft/paper1_radioscience.tex` (+ PDF rebuild)
- [x] Explicit “not Tu dynamic fidelity” disclaimer in Discussion
- [x] Series-jacket geometry + all \(S_d\) in the dense band

## Done (campaign inheritance)

- [x] PEC-seeded sheath coupling
- [x] Dense CW 1.5–2.3 MHz
- [x] Low-f CW 0.5–1.5 MHz, \(S_d=0,2,10\)
- [x] Literature reframe (Song/Tu/Liu) in `docs/SHEATH_MODELS_LITERATURE_DISCUSSION.md`
