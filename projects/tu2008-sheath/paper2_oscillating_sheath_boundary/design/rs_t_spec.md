# Design: kinematic \(r_s(t)\) sheath mask

**Status:** Implemented in `src/physics/plasma.cpp` (2026-09-10).  
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

Feature enable: `SheathOscEnable = (SheathDeltaR > 0)`.  
When \(\Delta r = 0\), only static `ApplySheath()` runs — **Paper 1 bit-match path**.

## Discrete update

1. **Once at init:** build PEC-seeded integer distance field out to  
   \(S_\mathrm{max} = \lceil r_{s0} + |\Delta r|\rceil\).
2. **Each time step:**  
   \(S_d(t) = \mathrm{round}\bigl(r_{s0} + \Delta r\sin(\ldots)\bigr)\), clamped to \([0, S_\mathrm{max}]\).
3. **Apply only when integer \(S_d\) changes** (staircased radial threshold — no full distance rebuild).
4. For cells with \(0 < d \le S_\mathrm{max}\):  
   - \(d \le S_d(t)\): \(N_0 \leftarrow N_\mathrm{bulk}\,N_\mathrm{min}\) (kinematic vacuum)  
   - else: \(N_0 \leftarrow N_\mathrm{bulk}\) (restore)  
5. When the sheath expands, floor dynamic \(N\) inside the new hole to the density floor (stability).

## Diagnostics (pilot)

| Quantity | Where |
|----------|--------|
| Feed \(V,I\) → \(Z\) | `.vc` as in Paper 0/1 CW |
| Integer \(S_d(t)\) changes | solver log (optional sparse) |
| Controls | static \(r_{s0}\) and static \(r_{s0}+\lceil\Delta r\rceil\) brackets |

## Non-claims

- Not self-consistent charging (Paper 3).  
- Not Song’s exact \(r_s^2(t)\) or orbit-limited collection.  
- Staircasing + fluid response may wash out a clean \(\dot{r}_s\) signature; a null result still gates Paper 3.

## API

```text
ApplySheath()                 // static (Δr=0)
InitOscillatingSheath()       // after PLASMAclear + geometry
UpdateOscillatingSheath(t,f)  // inside FDTD loop when enabled
FreeOscillatingSheath()       // on exit
```
