# Paper 2 — Oscillating sheath boundary

**Working title.** *Kinematic oscillating sheath boundary in 3D plasma fluid FDTD: testing Song’s \(\dot{r}_s\) radiation mechanism without particle-in-cell.*

**Status:** Not started (design only).  
**Guide:** [`../PROJECT_GUIDE.md`](../PROJECT_GUIDE.md)  
**Prerequisite:** Paper 1 static \(C(r_s)\) baseline ideally in hand (or at least \(C_\mathrm{eff}\) extraction method frozen).

---

## Science question

If the sheath–plasma boundary radius is **prescribed** to oscillate at the drive frequency,

\[
r_s(t) = r_{s0} + \Delta r\,\sin(\omega t + \phi)
\]

(or Song’s \(r_s^2(t)\) form), does PF-FDTD show Song-like **dynamic coupling** — feed loading and/or radiated fields tied to \(\dot{r}_s\) — beyond a static jacket of thickness \(r_{s0}\)?

This is the **bridge that static \(S_d\) cannot provide**: time dependence without yet solving self-consistent charging.

## Why this can be a paper

- Isolates Song’s **moving-boundary current** \(J_s \propto -e N_0 \dot{r}_s\) in a 3D Maxwell–fluid code.  
- Novelty: most FDTD antenna–plasma work either omits sheath dynamics or jumps to PIC; a **kinematic sheath** is a controlled middle path.  
- Directly informs whether Paper 3 (self-consistent) is worth the engine cost.

## Observables (success metrics)

| Metric | Target |
|--------|--------|
| \(\Delta Z\) or radiated diagnostic: oscillating \(r_s\) vs static \(r_{s0}\) | Clear, \(\omega\)-locked difference attributable to \(\dot{r}_s\) |
| Phase of boundary motion vs feed \(V\)/\(I\) | Comparable to Song’s ~90° sheath/current relations where applicable |
| Amplitude scan \(\Delta r\) | Response scales sensibly with \(\dot{r}_s\) amplitude |
| Control: static \(S_d\) at \(r_{s0}\) and at \(r_{s0}+\Delta r\) | Bracket the kinematic case |

**Not required for Paper 2 success:** matching Tu PIC reactance to 10%, or self-consistent DC charging.

## Physics engine note

**Same Maxwell + fluid core.** Change is limited to a **time-dependent sheath mask** (density hole radius updates each step or subcycle). No PIC. No orbit-limited collection.

## Work plan

1. Requirements: discrete cylindrical (or Cartesian staircased) \(r_s(t)\); stability with \(\Delta x\), CFL.  
2. Implement time-varying `ApplySheath`-class update (branch / feature flag).  
3. Single-tone pilot at one \(f < f_p\); compare static vs oscillating.  
4. Parameter scan: \(\Delta r\), \(r_{s0}\), \(\phi\), drive amplitude.  
5. Draft: mechanism paper; cite Song 2007 as theory target, Tu as future self-consistent step.

## Risks

| Risk | Mitigation |
|------|------------|
| Staircased moving boundary is noisy | Smooth \(r_s(t)\); average diagnostics over cycles |
| Fluid response cannot support Song’s electron-free assumption | Keep \(N_\min\) inside \(r_s(t)\); document as kinematic vacuum region |
| No clear \(\dot{r}_s\) signature | Still publishable as negative/controlled result; gates Paper 3 |

## Folder layout

```text
paper2_oscillating_sheath_boundary/
├── README.md
├── PLAN.md
├── design/          ← rs(t) formulation, mask update notes
├── analysis/
└── draft/
```

## Depends on / feeds

- **Depends on:** Paper 1 methods for \(Z\) / \(C\) diagnostics; working prescribed sheath.  
- **Feeds:** Go/no-go evidence for Paper 3 investment.
