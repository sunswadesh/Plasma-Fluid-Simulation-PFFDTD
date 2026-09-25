# Soft phase scan findings (f=700 kHz, Delta-r=1)

**Date:** 2026-09-25  
**Protocol:** soft edge=1, $r_{s0}=4$, $\Delta r=1$; $\phi\in\{0,45,90,135,180\}$  
**Statics / $\phi=0$:** `results/paper2_rs_t_pilot_soft/`  
**Other phases:** `results/paper2_phase_scan_soft/`

| $\phi$ (deg) | Re$Z$ | Im$Z$ | arg$Z$ | rel_to_bracket |
|-------------:|------:|------:|-------:|---------------:|
| 0 | 6.648e+04 | -5.789e+04 | -41.05 | **8.371** |
| 45 | 8.196e+03 | -5.268e+04 | -81.16 | **1.791** |
| 90 | 3.116e+04 | -1.159e+04 | -20.41 | **5.922** |
| 135 | 2.394e+04 | -3.066e+04 | -52.02 | **2.583** |
| 180 | -1.990e+03 | -4.235e+04 | -92.69 | **2.709** |

## Verdict

arg$(Z)$ span across $\phi$: **72.3 deg**.

Feed phase moves systematically with boundary phase (span > 10 deg) -> coherent coupling more plausible than amplitude-only numerical agitation. All five phases remain out-of-bracket (rel > 1.7). Offset magnitude is phase-dependent (largest at $\phi=0$, smallest at $\phi=45$).

Harmonic diagnostics: see `figures/phase_scan_I_harmonics.png`.

## Figures

- `figures/phase_scan_Z_complex.png`
- `figures/phase_scan_metrics.png`
- `figures/phase_scan_I_harmonics.png`
