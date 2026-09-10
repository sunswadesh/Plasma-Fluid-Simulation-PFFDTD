# Paper 2 pilot findings

**Date:** 2026-09-10  
**Data:** `results/paper2_rs_t_pilot/`  
**Drive:** $f=700$ kHz, $f_p=2$ MHz, $r_{s0}=4$, $\Delta r=1$, $\phi=0$  
**Method:** phasor $Z=V/I$ on last 50% of `.vc` traces.

## Phasor table

| Case | Re$Z$ ($\Omega$) | Im$Z$ ($\Omega$) | $|Z|$ | arg$Z$ (deg) |
|------|----------------:|----------------:|------:|-------------:|
| `static_rs0` | 1.761e+04 | -4.748e+04 | 5.064e+04 | -69.65 |
| `static_rsmax` | 1.418e+04 | -4.259e+04 | 4.489e+04 | -71.59 |
| `osc_rs_t` | 7.306e+04 | -4.316e+04 | 8.485e+04 | -30.57 |

## Bracket test

Complex-plane distance between static brackets: $|Z_5-Z_4|=5.9689e+03\,\Omega$.

Oscillating case distance to bracket segment: $5.5621e+04\,\Omega$ (fraction of bracket span: **9.319**).

Projection parameter $\tau$ along $Z_4\to Z_5$ (0 at $r_{s0}$, 1 at $r_{s\max}$): **-4.743**.

**Verdict:** The oscillating phasor is **offset from the static bracket segment**, consistent with a possible kinematic/moving-boundary contribution beyond quasi-static $S_d$ alone. Confirm with $\Delta r$ scan and phase controls.

## Figures

- `figures/pilot_Z_complex.png`
- `figures/pilot_Z_bars.png`
- `figures/pilot_VI_last_cycles.png`
