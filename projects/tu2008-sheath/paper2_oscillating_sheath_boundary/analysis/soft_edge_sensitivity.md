# Soft-edge width sensitivity (fixed $\Delta r=1$)

**Date:** 2026-09-24  
**Drive:** $f=700$ kHz, $r_{s0}=4$, $\Delta r=1$, $\phi=0$  
**Statics:** `results/paper2_rs_t_pilot_soft/`  
**Osc edge=1:** soft pilot `osc_rs_t`  
**Osc edge=0.5, 2:** `results/paper2_soft_edge_sens/`

## Phasor table

| Case | edge | Re$Z$ | Im$Z$ | $|Z|$ | arg$Z$ | $I_\mathrm{rms}$ | rel_to_bracket |
|------|-----:|------:|------:|------:|-------:|------------------:|---------------:|
| `static_rs0` | -- | 1.761e+04 | -4.748e+04 | 5.064e+04 | -69.65 | 9.485e-05 | -- |
| `static_rsmax` | -- | 1.418e+04 | -4.259e+04 | 4.489e+04 | -71.59 | 9.150e-05 | -- |
| `osc_edge0p5` | 0.5 | 3.436e+04 | -5.446e+04 | 6.440e+04 | -57.75 | 1.731e-04 | **3.041** |
| `osc_edge1` | 1.0 | 6.648e+04 | -5.789e+04 | 8.815e+04 | -41.05 | 9.047e-05 | **8.371** |
| `osc_edge2` | 2.0 | 4.338e+04 | -5.894e+04 | 7.318e+04 | -53.65 | 1.034e-04 | **4.725** |

## Verdict criteria (SCIENCE.md section 2.2)

- Out-of-bracket must **survive** across edge widths -> more like physics.
- If offset vanishes only at large edge -> more like artifact.

**Verdict:** Out-of-bracket loading **survives** for soft edges 0.5, 1.0, 2.0 (rel = 3.04, 8.37, 4.72). Soft-edge width moves the point but does not collapse the dynamic signature onto the static bracket.

Rel span across edges: 5.331. Edge width changes the complex location and $I_\mathrm{rms}$ (sharper edge=0.5 elevates $I_\mathrm{rms}$), but all three remain far outside the static segment. Prefer edge=1 as the default for subsequent scans (lowest osc $I_\mathrm{rms}$ among the three).

## Figures

- `figures/soft_edge_Z_complex.png`
- `figures/soft_edge_metrics.png`
- `figures/soft_edge_I_last_cycles.png`
