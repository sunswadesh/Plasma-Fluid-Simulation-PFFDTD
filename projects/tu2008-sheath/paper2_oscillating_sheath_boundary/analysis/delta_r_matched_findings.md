# Matched soft $\Delta r$ findings

**Date:** 2026-09-25  
**Policy:** $\mathrm{SheathSoftEdge}=\Delta r$ (SoftFrac=1)  
**Drive:** $f=700$ kHz, $r_{s0}=4$, $\phi=0$  
**Data:** `results/paper2_delta_r_matched/` (+ soft pilot $\Delta r=1$)

| $\Delta r$ | soft | Re$Z$ | Im$Z$ | $|Z|$ | rel_to_bracket | $|Z-Z_\mathrm{mid}|$ |
|----------:|-----:|------:|------:|------:|---------------:|---------------------:|
| 0.5 | 0.5 | 2.024e+04 | 1.070e+04 | 2.289e+04 | **8.985** | 5.590e+04 |
| 1.0 | 1.0 | 6.648e+04 | -5.789e+04 | 8.815e+04 | **8.371** | 5.219e+04 |
| 1.5 | 1.5 | -7.155e+03 | -3.796e+04 | 3.863e+04 | **6.308** | 2.473e+04 |
| 2.0 | 2.0 | 2.435e+04 | -6.014e+03 | 2.508e+04 | **11.237** | 4.140e+04 |

## Verdict

Out-of-bracket at **4 / 4** matched amplitudes (rel > 0.5).

Even with soft$\propto\Delta r$, rel / $|Z|$ remain **non-monotonic**. Treat amplitude scaling as unsettled; report as a finding, not a failure.

## Figures

- `figures/delta_r_matched_Z_complex.png`
- `figures/delta_r_matched_metrics.png`
