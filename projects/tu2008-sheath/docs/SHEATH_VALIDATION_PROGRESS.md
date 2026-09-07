# Sheath Validation Progress

**Superseded as a live log.** Current dashboard: [`../STATUS.md`](../STATUS.md).  
Low-f results: [`../analysis/cw_lowf_findings.md`](../analysis/cw_lowf_findings.md).  
Report: [`../validation/phase_7_documentation/main.pdf`](../validation/phase_7_documentation/main.pdf).

## Historical note (May 2026)

This file originally tracked early narrow-band / pulse-FFT analysis constraints before the coupling fix and the August–September CW campaigns. Those early constraints (do not burn wall time on broadband FFT until the method works) were correct for that phase; the campaign later moved to CW phasors near \(f_p\), fixed PEC-seeded sheath coupling, and completed dense + low-f CW grids.

## Current conclusion (2026-09-04)

| Item | Result |
|------|--------|
| Plasma resonance near \(f_p\) | Yes — \(f_\mathrm{res}(S_d=0)\approx1.85\,\mathrm{MHz}\) |
| Sheath coupling | Yes — post-fix \(Z\) strongly depends on \(S_d\) |
| Tu upward \(f_\mathrm{res}(S_d)\) | **No** — \(f_\mathrm{res}\) decreases with \(S_d\) (0.66 MHz at \(S_d=2\); ≤0.5 MHz at \(S_d=10\)) |

![Resonance trend](figures/cw_lowf_resonance.png)

*Last updated: 2026-09-04.*
