# Paper 2 — Oscillating sheath boundary

**Working title.** *Kinematic oscillating sheath boundary in 3D plasma fluid FDTD: testing Song’s \(\dot{r}_s\) radiation mechanism without particle-in-cell.*

**Status:** Soft + \(\Delta r\) evidence that motion loads beyond static brackets; amplitude scaling unsettled.  
**Science / outstanding issues / forward plan:** [`SCIENCE.md`](SCIENCE.md)  
**Guide:** [`../PROJECT_GUIDE.md`](../PROJECT_GUIDE.md)  
**Design:** [`design/rs_t_spec.md`](design/rs_t_spec.md)  
**Manuscript:** [`draft/manuscript.tex`](draft/manuscript.tex) (*Radio Science* / AGU format — **reframe pending**)  
**Pilot findings:** [`analysis/pilot_findings.md`](analysis/pilot_findings.md), [`analysis/hard_vs_soft.md`](analysis/hard_vs_soft.md), [`analysis/delta_r_soft_findings.md`](analysis/delta_r_soft_findings.md)  
**Prerequisite:** Paper 1 static \(C(r_s)\) baseline ideally in hand (or at least \(C_\mathrm{eff}\) extraction method frozen).

---

## Science question

If the sheath–plasma boundary radius is **prescribed** to oscillate at the drive frequency,

\[
r_s(t) = r_{s0} + \Delta r\,\sin(\omega t + \phi)
\]

does PF-FDTD show **dynamic loading** — feed and/or field response beyond a static jacket at \(r_{s0}\) or \(r_{s0}+\Delta r\)?

This is the **bridge that static \(S_d\) cannot provide**: time dependence without yet solving self-consistent charging.  
**Scoreboard:** changing vs static sheath physics — **not** Song/Tu numerical reproduction. Detail: [`SCIENCE.md`](SCIENCE.md).

## Why this can be a paper

- Isolates **consequences of a moving density hole** in a 3D Maxwell–fluid code.  
- Novelty: most FDTD antenna–plasma work either omits sheath dynamics or jumps to PIC; a **kinematic sheath** is a controlled middle path.  
- Motivated by Song/Tu (RF sheaths move) without requiring their analytics/PIC as a fit target.

## Observables (success metrics)

| Metric | Target |
|--------|--------|
| \(\Delta Z\) or radiated diagnostic: oscillating \(r_s\) vs static \(r_{s0}\) | Clear difference beyond thickness brackets |
| Sparse frequency / phase checks | Not a fluke of one \(f\) or \(\phi=0\) |
| Amplitude scan \(\Delta r\) | Document trend or honest non-monotonic regimes |
| Control: static \(S_d\) at \(r_{s0}\) and at \(r_{s0}+\Delta r\) | Bracket the kinematic case |

**Not required for Paper 2 success:** matching Tu PIC reactance to 10%, Song formula fits, or self-consistent DC charging.

## Physics engine note

**Same Maxwell + fluid core.** Change is limited to a **time-dependent sheath mask** (density hole radius updates each step or subcycle). No PIC. No orbit-limited collection.

### Solver CLI (Paper 2 extras)

```text
pffdtd_parallel <in> <out> fp col cyc el az T Sd vc_rate MaxIter [Δr] [phase_deg] [fosc_Hz]
```

- \(\Delta r=0\) (default): static `ApplySheath(Sd)` — Paper 1 path.  
- \(\Delta r>0\): kinematic \(r_s(t)\); `fosc_Hz=0` locks to drive `Spar[1]`.

Pilot: [`../scripts/run_paper2_rs_t_pilot.ps1`](../scripts/run_paper2_rs_t_pilot.ps1) → `results/paper2_rs_t_pilot/`.

## Work plan

See [`PLAN.md`](PLAN.md) and [`SCIENCE.md`](SCIENCE.md) §5. Short version:

1. ~~Kinematic \(r_s(t)\) + soft edge + hard/soft pilots + \(\Delta r\) scan.~~  
2. Reframe manuscript (changing vs static; Song/Tu as motivation only).  
3. Soft-edge sensitivity; sparse frequencies; phase + harmonics.  
4. Matched-\(\Delta r\) / stronger nulls as needed.

## Risks

| Risk | Mitigation |
|------|------------|
| Staircased / soft-update noise in \(I(t)\) | Soft edge; edge sensitivity; spectral diagnostics ([`SCIENCE.md`](SCIENCE.md) §2.2) |
| Density hole ≠ kinetic sheath | Precise language; kinematic claims only (§2.6) |
| Non-monotonic \(\Delta r\) | Matched soft policy; report regimes (§2.3, §3.4) |
| Overclaiming Song/Tu | Explicit non-goals in PLAN; manuscript reframe (§3.5) |

## Folder layout

```text
paper2_oscillating_sheath_boundary/
├── README.md
├── PLAN.md          ← checklist
├── SCIENCE.md       ← outstanding issues + forward science plan
├── design/          ← rs(t) formulation, mask update notes
├── analysis/
└── draft/           ← Radio Science manuscript + outline
```

## Depends on / feeds

- **Depends on:** Paper 1 methods for \(Z\) / \(C\) diagnostics; working prescribed sheath.  
- **Feeds:** Evidence that prescribed sheath *motion* is electromagnetically consequential (informs, but does not require, Paper 3).
