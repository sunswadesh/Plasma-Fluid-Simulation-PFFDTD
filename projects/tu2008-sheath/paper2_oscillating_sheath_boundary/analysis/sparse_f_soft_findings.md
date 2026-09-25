# Sparse frequency soft findings

**Date:** 2026-09-24  
**Data:** `results/paper2_sparse_f_soft/` (+ 700 kHz soft pilot from `paper2_rs_t_pilot_soft`)  
**Protocol:** soft edge=1, $\Delta r=1$, $\phi=0$, $r_{s0}=4$; static brackets at each $f$.

| $f$ (kHz) | osc Re$Z$ | osc Im$Z$ | $|Z|$ | rel_to_bracket |
|----------:|----------:|----------:|------:|---------------:|
| 500 | 1.797e+04 | -2.168e+04 | 2.816e+04 | **1.221** |
| 700 | 6.648e+04 | -5.789e+04 | 8.815e+04 | **8.371** |
| 1200 | -3.498e+03 | -2.748e+04 | 2.770e+04 | **3.069** |

## Verdict

Out-of-bracket at **3 / 3** sparse frequencies (threshold rel > 0.5).

Dynamic loading is **not unique to 700 kHz** under this soft $\Delta r=1$ protocol. The offset is largest at 700 kHz; 500 kHz is milder but still outside the bracket; 1.2 MHz remains clearly out-of-bracket with a more inductive/less capacitive arg shift (osc arg $\approx -97^\circ$ vs static $\sim -75^\circ$).

## Figures

- `figures/sparse_f_Zmag.png`
- `figures/sparse_f_Z_complex.png`
- `figures/sparse_f_rel_to_bracket.png`
