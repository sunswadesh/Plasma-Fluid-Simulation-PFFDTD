# Paper 2 — Science framing, outstanding issues, and forward plan

**Last updated:** 2026-09-23  
**Scope:** Stay on Paper 2. Chase **actual physics of a changing sheath vs a static sheath**.  
**Not a goal:** Numerical reproduction of Song (2007) formulas or Tu (2008) PIC reactance to a percent target.

**Related:** [`README.md`](README.md), [`PLAN.md`](PLAN.md), [`design/rs_t_spec.md`](design/rs_t_spec.md), [`analysis/hard_vs_soft.md`](analysis/hard_vs_soft.md), [`analysis/delta_r_soft_findings.md`](analysis/delta_r_soft_findings.md), program literature [`../docs/SHEATH_MODELS_LITERATURE_DISCUSSION.md`](../docs/SHEATH_MODELS_LITERATURE_DISCUSSION.md).

---

## 1. What Paper 2 is asking (physics)

In RF plasma, the near-antenna density layer is not expected to be a frozen vacuum jacket. Potential and particle response make the sheath **breathe**. Paper 1 asked whether a **fixed** prescribed jacket loads the dipole like series capacitance. Paper 2 asks the next physical question:

> If the depleted region’s outer radius **moves in time** at the drive frequency, does the feed (and field) response differ from any **static** jacket at the mean or extreme thickness?

That is a question about **consequences of time-dependent geometry** in Maxwell–fluid FDTD. A positive answer means dynamic sheath structure is a first-class loading mechanism in this engine—not that Song’s analytic \(\dot{r}_s\) current has been calibrated.

**Working hypothesis (actual physics):** A changing sheath is the more realistic RF picture than a static one; a controlled kinematic \(r_s(t)\) should produce measurable dynamic loading beyond quasi-static thickness sampling.

**Evidence so far:** At 700 kHz, hard- and soft-edge oscillating cases sit far outside static brackets; soft edge reduces impulsive current but does not remove the out-of-bracket phasor. A soft \(\Delta r\) scan keeps large offsets at several amplitudes but **not** a clean monotonic amplitude law.

---

## 2. Outstanding issues (expanded)

### 2.1 Prescribed vs caused motion

**What we do.** We choose

\[
r_s(t)=r_{s0}+\Delta r\sin(2\pi f t+\phi)
\]

and rewrite the ambient density hole to follow that law. Charge, potential, and collection do **not** determine \(r_s\).

**What real physics does.** The sheath edge is an emergent location where electron density collapses under the instantaneous potential and kinetic (or nonlinear fluid) response. Motion is *caused*; \(r_s(t)\) is an outcome.

**Why this still matters for Paper 2.** Imposing \(r_s(t)\) is a legitimate **mechanism experiment**: it asks whether the Maxwell–fluid system *cares* about boundary motion when everything else is held fixed. That is analogous to prescribing a moving dielectric interface in classical EM to isolate interface currents—useful even when the interface law is not self-consistent.

**What we must not claim.** We must not say we have simulated sheath *formation*, DC bias, or orbit-limited collection. We test **consequences of motion**, not **why the sheath moves**.

**Implication for the paper.** Methods and Discussion should state the kinematic boundary condition up front and cast Song/Tu as motivation that sheaths *do* move in nature / HV RF, not as a fitting target. Paper 3 (if ever) owns “caused” motion.

**Open sub-questions.**

- Is the observed \(\Delta Z\) mainly from time-varying series \(C(t)\), from fluid response to a moving density step, or from both?
- Would a different prescribed law (e.g. Song’s \(r_s^2(t)\) form, or rectified / asymmetric \(r_s\)) change the feed signature qualitatively?

---

### 2.2 Numerics still muddy the current

**Symptom.** Hard staircase produced large feed-current spikes at integer radius jumps. Soft edge (1-cell \(N_0\) blend, no hard \(N\) floor) improved \(I_\mathrm{rms}\) toward static levels, but late-time \(I(t)\) for oscillating runs remains jagged relative to static sinusoids ([`analysis/figures/pilot_VI_last_cycles_soft.png`](analysis/figures/pilot_VI_last_cycles_soft.png)).

**Why it matters.** Phasor \(Z=V/I\) at the drive frequency folds *all* time-domain structure into one complex number. If part of \(I\) is mask-update noise, \(\mathrm{Re}\{Z\}\) and \(\arg Z\) partly report numerics.

**Physics vs artifact checklist.**

| More like physics | More like artifact |
|--------------------|--------------------|
| Smooth \(I\) at \(f\) with phase locked to \(r_s(t)\) | Spikes / bursts synchronized with radius-update events |
| Survives soft-edge width changes | Vanishes when edge → large or updates frozen |
| Harmonics consistent with nonlinear \(C(t)\) | Broadband hash without phase coherence |

**What we have.** Soft edge: out-of-bracket \(Z\) **survives** → not *only* hard staircasing. Residual roughness → cannot yet treat single-tone \(Z\) as a precision observable.

**Work needed.**

- Parameterize `SheathSoftEdge` (0.5, 1, 2 cells) at fixed \(\Delta r=1\); require qualitative stability of out-of-bracket conclusion.
- Optional: update threshold finer than 0.01 cell; or filter \(r_s(t)\) before applying \(N_0\).
- Report time-domain and spectral diagnostics alongside phasors (see §3.3).

---

### 2.3 Non-monotonic \(\Delta r\) response

**Symptom.** Soft scan ([`analysis/delta_r_soft_findings.md`](analysis/delta_r_soft_findings.md)): relative distance to the static bracket segment is large at \(\Delta r=0.5,1,1.5,2\) but **not** monotonically increasing (roughly 11 → 8 → 26 → 5). \(|Z|\) also does not grow smoothly with \(\Delta r\).

**Why a monotonic law was a reasonable prior.** If the dominant extra coupling scaled with boundary speed \(\sim\omega\Delta r\), larger \(\Delta r\) should strengthen the dynamic signature in some orderly way. Absence of that order does **not** cancel “motion ≠ static”; it blocks a simple amplitude-scaling story.

**Candidate explanations (to test, not assert).**

1. **Soft-edge vs amplitude mismatch.** Fixed `SheathSoftEdge=1` while \(\Delta r\) runs from 0.5 to 2 mixes “sharp relative to motion” and “soft relative to motion.” Try \(\mathrm{soft}\propto\Delta r\) or soft fixed as a fraction of \(\Delta r\).
2. **Bracket definition.** Bracket uses \(S_d\in\{r_{s0},\,r_{s0}+\lceil\Delta r\rceil\}\). Ceiling jumps discretely; comparing “rel_to_bracket” across \(\Delta r\) mixes different static baselines (e.g. need \(S_d=6\) once \(\Delta r>1\)).
3. **Nonlinear fluid / floor.** Density floor and fluid clipping may saturate or invert response at large hole excursions.
4. **Regime change in complex \(Z\).** At \(\Delta r=1.5\), soft data show \(\mathrm{Im}\{Z\}>0\) while neighbors are capacitive—possible diagnostic of a different operating regime, not a smooth continuation.
5. **Residual update noise** that depends on how often the soft profile refreshes as \(\dot{r}_s\) grows.

**Paper stance until resolved.** Report the scan honestly: dynamic loading is robustly out-of-bracket; amplitude scaling is **unsettled**. Do not claim \(\propto\dot{r}_s\).

---

### 2.4 One frequency only

**What we know.** Primary evidence is at \(f=700\,\mathrm{kHz}\) with \(f_p=2\,\mathrm{MHz}\) (drive well below plasma frequency, in the capacitive / series-loading–relevant band familiar from Paper 1).

**What we do not know.**

- Is dynamic loading stronger, weaker, or reversed nearer \(f_p\)?
- Does it persist deeper in the low-\(f\) asymptote (more “pure \(C(t)\)”)?
- Is the effect an accident of one electrical size / grid / collision setting?

**Why not a full Paper 1 frequency grid yet.** Paper 1 maps **static** \(Z(f)\) because series \(C\) is a spectral concept. Paper 2’s first question is an A/B test at drive-locked \(r_s(t)\). Each CW frequency is a long run; oscillation cannot be replaced by a single pulse FFT without a new analysis design. A **sparse** frequency set answers “fluke or not”; a dense grid is a later campaign if the sparse set stays interesting.

**Proposed sparse set (see §3.1):** e.g. \(\sim 0.4\,f_p\), \(0.35\,f_p\) (700 kHz done), \(\sim 0.75\,f_p\)—same soft \(\Delta r=1\) + brackets.

---

### 2.5 Phase and harmonics barely explored

**Physics expectation.** A moving boundary phased relative to the drive should rotate the relationship between \(V\) and \(I\). Nonlinear \(C(t)\) or moving-interface coupling can generate harmonics at \(2f\), \(3f\), etc.

**What we have.** Default \(\phi=0\) only. Diagnostics have centered on fundamental phasor \(Z\).

**What to measure.**

- Sweep \(\phi\) over \(\{0,45,90,135,180^\circ\}\) at fixed \(f\), \(r_{s0}\), \(\Delta r\).
- Track \(\arg(Z)\), \(\arg(I)-\arg(V)\), and correlation of \(I\) with \(\sin(\omega t+\phi)\) vs \(\cos(\omega t+\phi)\).
- FFT of late-time \(I\): power at \(f\) vs \(2f\), \(3f\); compare osc vs static brackets (static should be nearly sinusoidal).

**Falsifiable pattern.** If changing \(\phi\) does not systematically move feed phase / harmonic content, the present \(\Delta Z\) looks less like coherent boundary-driven coupling and more like amplitude-dependent numerical agitation.

---

### 2.6 What “sheath” means in this fluid FDTD

**Implementation reality.**

- Depletion is a prescribed floor on \(N_0\) (and soft blend) inside a PEC-distance neighborhood.
- No Poisson charging BC that sets floating potential.
- No orbit-limited ion/electron collection.
- Interior is not a true electron-free ion sheath; it is a **kinematic density hole**.

**Language rules for Paper 2.**

| Prefer | Avoid |
|--------|--------|
| Prescribed / kinematic density hole or vacuum jacket | “Self-consistent sheath” |
| Dynamic loading from time-varying depletion | “Song \(\dot{r}_s\) current verified” |
| Motivation from Song/Tu that RF sheaths move | “Reproduction of Song/Tu” |

**Why this is still physics.** Even a density hole is a real electromagnetic object: it changes the path from metal to plasma and, when moved, changes that path in time. The limitation is **model class**, not “no physics.”

---

## 3. What more to do to advance Paper 2 (expanded)

Priority order below is recommended; reorder if machine time or manuscript deadlines force it.

### 3.1 Sparse frequency set (2–3 tones)

**Goal.** Show the 700 kHz result is not unique.

**Design.** Soft edge on; \(\Delta r=1\); \(r_{s0}=4\); \(\phi=0\); for each \(f\): static \(r_{s0}\), static \(r_{s0}+1\), osc. Candidate frequencies: one lower (e.g. 500 kHz) and one higher but still \(<f_p\) (e.g. 1.2–1.5 MHz).

**Success.** Out-of-bracket behavior at ≥2 frequencies, or an honest map of where it fails.

**Cost.** ~3 cases × ~2 new frequencies ≈ 6 long runs (plus reuse 700 kHz). Not a Paper 1–scale grid.

### 3.2 Phase scan \(\phi\)

**Goal.** Test coherent coupling to boundary phase.

**Design.** Fix \(f=700\,\mathrm{kHz}\), soft, \(\Delta r=1\); sweep \(\phi\); static brackets once.

**Success.** Systematic movement of \(\arg(Z)\) / harmonic pattern with \(\phi\); not random scatter.

### 3.3 Cleaner diagnostics (beyond one phasor \(Z\))

**Goal.** Make the paper’s evidence multi-messenger so numerics are harder to hide in a single complex number.

**Add to analysis pipeline.**

1. Late-time \(V(t)\), \(I(t)\) overlays (already started).  
2. Cycle-averaged \(\langle VI\rangle\) or net power into the feed.  
3. Harmonic spectrum of \(I\) (and \(V\) check).  
4. Optional: probe \(E\) (or \(B\)) outside \(r_{s0}+|\Delta r|\) soft max—radiated / near-field difference osc vs static.

**Manuscript effect.** Results section becomes “dynamic loading signatures,” not only Table of \(Z\).

### 3.4 Resolve or map the \(\Delta r\) mess

**Goal.** Either restore a clear amplitude trend under matched numerics, or document regimes.

**Actions.**

- Re-run \(\Delta r\in\{0.5,1,1.5,2\}\) with \(\mathrm{SheathSoftEdge}=c\Delta r\) (e.g. \(c=1\)) or fixed fraction.  
- Always plot absolute \(Z_\mathrm{osc}-Z_\mathrm{static}\) in the complex plane, not only “rel_to_bracket” (which renormalizes by changing bracket span).  
- If non-monotonicity persists under matched soft parameters, dedicate a Results subsection to “non-monotonic amplitude response” as a finding, not a failure.

### 3.5 Reframe the manuscript

**Goal.** Align title, abstract, keypoints, and Discussion with the actual-physics program.

**Do.**

- Title/abstract: prescribed **dynamic** sheath vs **static** jacket; measurable dynamic feed loading in 3D PF-FDTD.  
- Cite Song/Tu as **evidence that RF sheaths move** and as contrast (analytic / PIC), not as the scoreboard.  
- Explicit limitations §2.1 and §2.6.  
- Report hard vs soft and \(\Delta r\) scan with the non-monotonic caveat.

**Don’t.**

- Lead with “testing Song’s \(\dot{r}_s\) radiation mechanism” as the sole purpose.  
- Claim kinetic sheath fidelity.

**Checklist item:** rewrite [`draft/manuscript.tex`](draft/manuscript.tex) framing in a dedicated editing pass after sparse-\(f\) or phase data land (or sooner if drafting ahead of runs).

### 3.6 Optional stronger nulls

**A. Matched soft parameters while locking \(r_{s0}\).** Vary only \(\Delta r\); keep soft-edge policy consistent (§3.4).

**B. Time-averaged effective radius null.** Define a static run at \(S_d\) equal to round(\(\langle r_s\rangle\)) or to an effective radius from \(\langle C\rangle\) intuition; require osc ≠ that static, not only ≠ min/max brackets. Stronger statement: dynamics ≠ quasi-static equivalent thickness.

**C. Frozen-\(r_s\) control.** Hold \(r_s=r_{s0}+\Delta r\sin\phi_0\) fixed in time (various \(\phi_0\)) vs true osc—separates “instantaneous thickness samples” from “motion through thickness.”

---

## 4. Paper 1 vs Paper 2 (reminder)

| | Paper 1 | Paper 2 |
|--|---------|---------|
| Sheath | Static \(S_d\) | Kinematic \(r_s(t)\) |
| Core question | Series loading / \(C_\mathrm{eff}\) | Dynamic loading beyond thickness |
| Natural data | Dense \(Z(f)\) | Drive-locked A/B + sparse \(f\), \(\Delta r\), \(\phi\) |
| Feeds | Trusted static baseline | Whether motion is electromagnetically consequential |

Paper 2 does **not** replace Paper 1’s frequency map; it answers a different physical question with different experimental design.

---

## 5. Suggested near-term sequence

1. ~~Reframe draft language (§3.5).~~  
2. Soft-edge sensitivity at \(\Delta r=1\) (§2.2 / §3.4) — in progress.  
3. Sparse frequency set (§3.1).  
4. Phase scan (§3.2) + harmonic diagnostics (§3.3).  
5. Revisit \(\Delta r\) with matched soft policy (§3.4).  
6. Optional stronger nulls (§3.6) before calling Paper 2 “complete.”

Update [`PLAN.md`](PLAN.md) checkboxes as each item closes; keep this document as the science rationale.
