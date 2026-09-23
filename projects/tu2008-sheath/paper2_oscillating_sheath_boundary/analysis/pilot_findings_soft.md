# Paper 2 pilot findings (soft)

**Data:** `results/paper2_rs_t_pilot_soft/`  
**Drive:** $f=700$ kHz  
**Method:** phasor $Z=V/I$ on last 50%% of `.vc` traces.

## Phasor table

| Case | Re$Z$ ($\Omega$) | Im$Z$ ($\Omega$) | $|Z|$ | arg$Z$ (deg) |
|------|----------------:|----------------:|------:|-------------:|
| `static_rs0` | 1.761e+04 | -4.748e+04 | 5.064e+04 | -69.65 |
| `static_rsmax` | 1.418e+04 | -4.259e+04 | 4.489e+04 | -71.59 |
| `osc_rs_t` | 6.648e+04 | -5.789e+04 | 8.815e+04 | -41.05 |

## Bracket test

Complex-plane distance between static brackets: $|Z_5-Z_4|=5.9691e+03\,\Omega$.

Oscillating case distance to bracket segment: $4.9969e+04\,\Omega$ (fraction of bracket span: **8.371**).

Projection parameter $\tau$ along $Z_4\to Z_5$: **-6.130**.

**Verdict:** The oscillating phasor is **offset from the static bracket segment**, consistent with a kinematic/moving-boundary contribution beyond quasi-static $S_d$ alone.

## Figures

- `figures/pilot_Z_complex_soft.png`
- `figures/pilot_Z_bars_soft.png`
- `figures/pilot_VI_last_cycles_soft.png`
