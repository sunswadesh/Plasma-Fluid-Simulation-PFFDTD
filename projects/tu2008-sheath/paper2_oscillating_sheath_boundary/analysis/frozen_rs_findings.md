# Frozen-$r_s$ null findings

**Date:** 2026-10-23
**Campaign:** `results/paper2_frozen_rs/` via `run_frozen_ckpt.sh` (solver checkpoint/restart; watchdog cron relaunched after VM reboots)
**Protocol:** identical to the soft pilot — $f=700$ kHz, $f_p=2$ MHz, soft edge = 1 cell, $T=100$, 430,000 steps, phasor $Z=V/I$ on the last 50% of each `.vc` record. Frozen states hold the soft mask at constant radius $r$ via Sd+$\Delta r$, $\phi=90^\circ$, $f_\mathrm{osc}=0.001$ Hz (drift $\sim10^{-7}$ rad per run; mask never updates).

## Frozen phasors

| $r$ | Re$Z$ ($\Omega$) | Im$Z$ ($\Omega$) | $|Z|$ | arg$Z$ (deg) |
|----:|------:|------:|------:|------:|
| 3.0 | 2.302e+04 | −2.928e+04 | 3.724e+04 | −51.83 |
| 3.5 | 4.118e+04 | −3.453e+04 | 5.375e+04 | −39.98 |
| 4.0 | 3.333e+04 | −3.595e+04 | 4.903e+04 | −47.16 |
| 4.5 | 1.761e+04 | −4.748e+04 | 5.064e+04 | −69.65 |
| 5.0 | 2.513e+04 | −4.397e+04 | 5.064e+04 | −60.25 |

Consistency check: the $r=4.5$ soft point reproduces the integer $S_d=4$ static from the original campaign (17,607 − 47,481j $\Omega$) to ~4 significant figures — expected, since a 1-cell soft edge at a half-integer radius reproduces the integer mask. The frozen $Z(r)$ locus is strongly nonlinear and non-monotonic in both components.

## Quasi-static prediction vs oscillating

The oscillating case ($r_{s0}=4$, $\Delta r=1$, soft pilot) visits $r\in[3,5]$ as $r(\theta)=4+\sin\theta$. Interpolating the frozen locus over that swing and averaging uniformly in $\theta$:

| Quantity | $Z$ ($\Omega$) | arg$Z$ (deg) |
|----------|---------------:|------:|
| Quasi-static $\langle Z\rangle$ | 2.772e+04 − 3.827e+04 j | −54.1 |
| Quasi-static $1/\langle Y\rangle$ | 2.840e+04 − 3.863e+04 j | −53.7 |
| Oscillating (soft pilot) | **6.648e+04 − 5.789e+04 j** | **−41.0** |

The two averaging conventions agree to ~800 $\Omega$, so the comparison does not hinge on how the quasi-static average is formed.

## Verdict

**The oscillating phasor lies outside the frozen locus entirely — genuine dynamic loading, not nonlinear quasi-static thickness averaging.**

- Re$\{Z_\mathrm{osc}\}$ = 66,480 $\Omega$ exceeds the maximum frozen Re (41,183 $\Omega$ at $r=3.5$) by 25,300 $\Omega$ (+61%).
- Im$\{Z_\mathrm{osc}\}$ = −57,887 $\Omega$ is more capacitive than every frozen state (range −29,280 to −47,479 $\Omega$).
- Distance from the oscillating phasor to the nearest point on the frozen locus polyline: 34,428 $\Omega$ ≈ 0.39 $|Z_\mathrm{osc}|$; distance to either quasi-static prediction ≈ 43 k$\Omega$ ≈ 0.49 $|Z_\mathrm{osc}|$.

Because the frozen runs use the identical soft-mask machinery with no per-step updates, this also retires the simplest mask-update-noise explanation: static masks at every visited thickness, and any cycle average of them, fail to reproduce the oscillating feed impedance by a wide margin. A velocity/memory (dynamic) term is required.

This closes the frozen-$r_s$ item of SCIENCE.md §3.6C. The effective-radius null (§3.6B) is subsumed: no single static radius and no average of radii reproduces the oscillating phasor.

## Figures / data

- `figures/frozen_rs_Z_complex.png`
- `data/frozen_rs_phasor_Z.tsv`
