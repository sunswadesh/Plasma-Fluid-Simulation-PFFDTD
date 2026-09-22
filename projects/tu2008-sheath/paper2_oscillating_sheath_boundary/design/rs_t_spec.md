# Design: kinematic \(r_s(t)\) sheath mask

**Status:** Soft-edge update added 2026-09-22 (default). Hard staircase retained via `soft_edge=0`.  
**Paper:** Paper 2 — oscillating sheath boundary.

---

## Law (chosen)

Simple sinusoid locked to the RF drive (Song \(r_s^2\) form deferred):

\[
r_s(t) = r_{s0} + \Delta r\,\sin(2\pi f_\mathrm{osc} t + \phi)
\]

| Symbol | CLI / code | Meaning |
|--------|------------|---------|
| \(r_{s0}\) | `argv[9]` → `Sd` | Mean sheath width (cells) |
| \(\Delta r\) | `argv[12]` → `SheathDeltaR` | Oscillation amplitude (cells, float OK) |
| \(\phi\) | `argv[13]` → `SheathPhaseDeg` | Phase (degrees → radians internally) |
| \(f_\mathrm{osc}\) | `argv[14]` → `SheathFosc` | Oscillation frequency (Hz); **0 = use drive `Spar[1]`** |
| soft edge | `argv[15]` → `SheathSoftEdge` | Transition width (cells); **0 = hard staircase**; default **1** |

Feature enable: `SheathOscEnable = (SheathDeltaR > 0)`.  
When \(\Delta r = 0\), only static `ApplySheath()` runs — **Paper 1 bit-match path**.

## Discrete update

### Soft edge (default, `SheathSoftEdge > 0`)

1. **Once at init:** PEC-seeded integer distance field out to \(S_\mathrm{max}=\lceil r_{s0}+|\Delta r|+\mathrm{soft}\rceil\).
2. **Each step** (when \(r_s\) moves by \(\ge 0.01\) cell): set
   \[
   N_0 = N_\mathrm{bulk}\bigl[N_\min + (1-N_\min)\,w\bigr],\quad
   w=\mathrm{clamp}\bigl(\tfrac{d-r_s}{\mathrm{soft}}+0.5,\,0,\,1\bigr).
   \]
3. **No hard floor of dynamic \(N\)** on update (avoids impulsive feed-current spikes from staircasing).

### Hard staircase (`SheathSoftEdge = 0`, original pilot)

1. \(S_d(t)=\mathrm{round}[r_s(t)]\); apply only when integer changes.
2. Step profile + floor \(N\) inside newly covered cells.

## Diagnostics (pilot)

| Quantity | Where |
|----------|--------|
| Feed \(V,I\) → \(Z\) | `.vc` as in Paper 0/1 CW |
| Controls | static \(r_{s0}\) and static \(r_{s0}+\lceil\Delta r\rceil\) brackets |
| Soft re-test | `results/paper2_rs_t_pilot_soft/` via `-OutTag soft -SoftEdge 1` |

## Non-claims

- Not self-consistent charging (Paper 3).  
- Not Song’s exact \(r_s^2(t)\) or orbit-limited collection.  
- Soft edge reduces staircasing artifacts; surviving out-of-bracket \(\Delta Z\) is stronger evidence for kinematic coupling.

## API

```text
ApplySheath()                 // static (Δr=0)
InitOscillatingSheath()       // after PLASMAclear + geometry
UpdateOscillatingSheath(t,f)  // inside FDTD loop when enabled
FreeOscillatingSheath()       // on exit
```
