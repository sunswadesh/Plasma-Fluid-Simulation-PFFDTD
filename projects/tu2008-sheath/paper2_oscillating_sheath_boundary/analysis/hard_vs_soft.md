# Hard vs soft-edge Paper 2 pilot

**Date:** 2026-09-22  
**Hard:** `results/paper2_rs_t_pilot/` (staircased \(S_d=\mathrm{round}[r_s]\), hard \(N\) floor)  
**Soft:** `results/paper2_rs_t_pilot_soft/` (1-cell \(N_0\) blend, no hard \(N\) floor)

Drive: \(f=700\,\mathrm{kHz}\), \(r_{s0}=4\), \(\Delta r=1\), \(\phi=0\).

## Static controls

Static \(r_{s0}=4\) and \(r=5\) **reproduce** between hard and soft campaigns to \(\sim 10^{-5}\) relative (soft path unused when \(\Delta r=0\)). Bracket span stays \(\approx 6.0\times 10^{3}\,\Omega\).

## Oscillating phasor

| Run | Re\(Z\) | Im\(Z\) | \(|Z|\) | arg\(Z\) | rel. to bracket |
|-----|--------:|--------:|--------:|---------:|----------------:|
| Hard | \(7.31\times10^{4}\) | \(-4.32\times10^{4}\) | \(8.49\times10^{4}\) | \(-30.6^\circ\) | **9.32** |
| Soft | \(6.65\times10^{4}\) | \(-5.79\times10^{4}\) | \(8.82\times10^{4}\) | \(-41.0^\circ\) | **8.37** |

Soft edge **moves** the oscillating point (more capacitive Im, slightly lower Re) but it remains **far outside** the static bracket segment. Soft \(I_\mathrm{rms}\) rises toward the static values (\(7.6\times10^{-5}\to 9.0\times10^{-5}\,\mathrm{A}\)), consistent with weaker impulsive current.

## Verdict

1. Out-of-bracket \(\Delta Z\) is **not** only a hard-staircase artifact.  
2. Soft edge is the preferred kinematic path for further \(\Delta r\) / phase scans.  
3. Quantitative Song \(\dot{r}_s\) identification still needs amplitude/phase scaling, not a single-tone magnitude alone.

Figures: `figures/pilot_*_soft.png` vs hard `figures/pilot_*.png`.
