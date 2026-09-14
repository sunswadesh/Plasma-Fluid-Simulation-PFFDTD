# Voltage vs current antenna drive in PF-FDTD

**Purpose.** Introduce the Dec 2025 collaboration idea of switching from a **voltage** feed to a **current** feed, judge whether that can produce Tu’s electron-charging bias, list pros/cons of implementing it, and separate what it *can* still buy even if it is not on the Paper 0–3 critical path.

**Context (email).** Alireza (30 Dec 2025): initial PF-FDTD runs (`collision-3_merged.pdf`) do not show the DC bias from faster electron collection onto the probe (Tu et al. 2008, Fig. 2). He suggested changing the source from voltage to current. Swadesh replied that Tu models a high-voltage potential, PF-FDTD is voltage-driven (Ward), and sheath physics is naturally voltage-driven — prefer sticking with \(V\) until clearer.

**Related:** [`references/Alireza_collaboration.pdf`](references/Alireza_collaboration.pdf), Tu 2008, Song 2007, [`SHEATH_MODELS_LITERATURE_DISCUSSION.md`](SHEATH_MODELS_LITERATURE_DISCUSSION.md), Paper 3 self-consistent sheath.

**Status of this note:** analysis / design opinion (2026-09-07). Not a commitment to implement.

---

## 1. Subject introduction

### 1.1 What “drive type” means

At the antenna feed, the simulator must impose one electrical boundary condition and measure the other:

| Drive | Imposed | Measured | Impedance |
|-------|---------|----------|-----------|
| **Voltage** (what PF-FDTD does now) | \(V(t)\) across the feed gap (hard \(E\) / voltage source) | \(I(t)\) (e.g. Ampère loop around the feed) | \(Z(\omega)=V(\omega)/I(\omega)\) |
| **Current** (proposed) | \(I(t)\) into the antenna | \(V(t)\) that develops across the gap | \(Z(\omega)=V(\omega)/I(\omega)\) (same formula) |

In a **linear** passive system, \(Z\) is a property of the antenna–plasma–sheath configuration. Ideal \(V\)-drive and \(I\)-drive should recover the **same** \(Z(\omega)\) (up to numerics). They are dual circuit excitations of the same network.

In a **nonlinear** or **charging** system, drive type can change the operating point (how large \(V\) becomes for a given \(I\), how hard the sheath is driven), but it does **not** by itself create new microphysical collection channels.

### 1.2 What Tu Fig. 2 is about

Tu et al. (2008) show antenna charging and sheath structure from **kinetic** particle dynamics:

- Electrons are lighter/faster → they reach a positively swung conductor more readily than ions reach a negative one.
- Over the first part of a cycle the antenna acquires a **net negative DC bias**.
- An ion sheath (electron-depleted region) forms; with ion dynamics included, brief electron-sheath excursions can appear.
- Sheath radius then oscillates with the RF drive.

That bias is a **charge-collection / self-consistent \(\rho\)** effect. It is **not** a statement about whether the laboratory transmitter is a stiff voltage source or a stiff current source. In Song/Tu theory the controlling state variable for sheath thickness is the **antenna potential relative to the plasma**.

### 1.3 Why the current-drive idea appeared

Their early fluid runs (`collision-3_merged.pdf`) did not exhibit Tu-like charging bias. A natural (but incomplete) troubleshooting thought is: “maybe the *excitation* is wrong.” Current drive is a real degree of freedom in antenna modeling, so it was a reasonable thing to *ask*. It is a weak explanation for *missing kinetic charging* in a fluid continuum code.

### 1.4 What PF-FDTD does today

- Soft/hard **electric** sources via `Esource` (`src/source/source.cpp`).
- Feed diagnostics: voltage and current written to `.vc` (`VOLT`, `CURRENT` in `pffdtd.cpp`).
- Campaign sheath work: prescribed density hole \(S_d\) + voltage-driven dipole → \(Z(f)\).

There is no first-class “impose \(I(t)\), float \(V\)” feed mode documented for the sheath campaign.

---

## 2. Is current drive *supposed* to work (for Tu charging)?

### Short verdict

**No.** Switching voltage → current drive is **not** expected to produce Tu Fig. 2 electron-charging bias in the present **fluid** PF-FDTD model.

### Why not (physics)

1. **Missing mechanism.** Tu’s bias requires particles (or an equivalent nonlinear collection law) to deposit charge on the conductor until electron and ion currents balance. A cold/fluid Maxwell–plasma update supplies macroscopic \(\mathbf{J}(\mathbf{E})\) in the volume; it does not implement Langmuir/orbit-limited current to a metal surface unless you **add** that physics (Paper 3).

2. **Drive type ≠ collection law.**  
   - \(V\)-drive: “hold this gap voltage; plasma and antenna currents respond.”  
   - \(I\)-drive: “force this feed current; gap voltage responds.”  
   Neither statement says “electrons stick to PEC faster than ions.”

3. **Sheath scale is set by potential.** Song’s static sheath radius grows with DC/AC voltage amplitude and plasma density. A current source that develops only a small floating \(V\) may make an even *weaker* sheath signature; a large \(I\) that drives a large \(V\) is still “voltage physics,” just reached indirectly.

4. **Linear fluid regime.** If the plasma response stays linear, \(Z_V\equiv Z_I\). Seeing no charging under \(V\)-drive almost guarantees you will see no charging under \(I\)-drive either — same equations, dual port excitation.

5. **Historical code choice.** Ward’s PF-FDTD and the Tu/Song problem framing are voltage/potential centered. That does not prove current drive is useless; it does argue it is the wrong lever for “missing Fig. 2.”

### When could drive type matter *together with* charging?

Only **after** a collection/charging module exists:

- A stiff **voltage** source clamps \(V(t)\) (including any intended DC offset) and lets collected current be whatever it must be (plus displacement).
- A stiff **current** source lets \(V\) (and thus sheath radius) float until the nonlinear \(I\)–\(V\) of the sheath matches the imposed current.

That is a legitimate Paper 3 *secondary* study (“transmitter Thévenin vs Norton equivalent with self-consistent sheath”). It is not a substitute for building the sheath formation physics.

### Analogy

Missing Tu bias in fluid PF-FDTD is like a weather model that has no condensation, wondering whether to force rainfall rate or atmospheric pressure at the boundary. Changing the boundary type does not create clouds.

---

## 3. Pros and cons if we implement current drive

### Pros

| Pro | Detail |
|-----|--------|
| Closes an open collaboration question | You can report a controlled \(V\) vs \(I\) comparison instead of only arguing on email. |
| Solver completeness | Many antenna codes support both; useful for other projects (PIP, ionosphere TX, teaching). |
| Linear consistency check | In linear plasma, \(Z\) from \(I\)-drive should match \(Z\) from \(V\)-drive → strong regression test of feed / `.vc` bookkeeping. |
| Literature alignment (some theories) | Classical short-dipole theory often *assumes* a current distribution \(I(z)\); imposing \(I\) can ease comparison to those formulas (Balmain-type), holding shape fixed. |
| Nonlinear operating-point control (later) | With a future sheath module, Norton (\(I\)) vs Thévenin (\(V\)) sources probe different load lines on a nonlinear sheath \(I\)–\(V\). |
| Numerical options | Soft current sources / impressed \(\mathbf{J}\) can be gentler than hard \(E\) gaps in some FDTD setups (case-dependent). |

### Cons

| Con | Detail |
|-----|--------|
| Does not fix Tu Fig. 2 | Primary collaboration pain point remains; risk of false hope / wasted thesis calendar. |
| Implementation + validation cost | Need a stable feed formulation, dual diagnostics, docs, and a matrix of regression cases (free space, plasma, with/without \(S_d\)). |
| Narrative confusion | Easy for readers to think “we switched to current drive to get sheath charging.” Must be written carefully. |
| Wrong natural variable for Song/Tu sheath | Sheath radius ↔ potential; \(V\)-drive maps more directly onto Song’s boundary data. |
| Opportunity cost | Competes with Paper 1 \(C_\mathrm{eff}\) and Paper 3 charging — higher scientific ROI for the sheath program. |
| Possible new artifacts | Hard \(I\) sources, loop placement, and gap geometry can introduce their own phase/amplitude errors if not carefully defined. |

### Effort sketch (order-of-magnitude)

- Minimal impressed-current feed + document \(Z\) match in free space: days–couple of weeks.  
- Robust plasma + sheath campaign parity with existing \(V\)-drive CW grid: additional weeks.  
- Still **zero** Tu charging without Paper 3 physics.

---

## 4. What can still be achieved (even if unrelated to Papers 0–3 goals)

These are real deliverables that do **not** require claiming Tu fidelity:

1. **Feed duality paper / note (small).**  
   Same dipole, linear magnetoplasma or unmagnetized fluid: show \(Z_V(f)\approx Z_I(f)\). Strengthens trust in `.vc` extraction.

2. **Fixed-current transmitter mode.**  
   Useful for “constant-\(I\) HF/VLF transmitter in plasma” thought experiments; power and radiation scale as \(I^2 R_\mathrm{rad}\) with floating voltage.

3. **Comparison to current-assumed analytics.**  
   Hold \(I(z)\) (e.g. triangular) and compare input impedance to Balmain-type or transmission-line antenna formulas without inferring \(I\) from a hard \(E\) gap.

4. **Soft-source / total-field experiments.**  
   Impressed \(\mathbf{J}\) sources are a standard FDTD pattern; may help plane-wave or distributed-drive studies (adjacent to Alireza’s plasma-cloud / propagation interests).

5. **Future nonlinear sheath load-line study.**  
   Once charging exists: map how much DC bias and \(r_s(t)\) you get under clamped-\(V\) vs clamped-\(I\) RF drives — a genuine Song/Tu *systems* question.

6. **Collaboration hygiene.**  
   A short memo + one figure (“we implemented \(I\)-drive; linear \(Z\) matches; still no DC bias without collection physics”) permanently retires the Dec 2025 workaround hypothesis.

---

## 5. Recommendation for this program

| Priority | Action |
|----------|--------|
| **Do not** treat current drive as the path to Tu Fig. 2 | Paper 3 (fluid charging or PIC) owns that. |
| **Optional, low priority** after Paper 1 \(C_\mathrm{eff}\)** | Small \(V\)/\(I\) duality check if solver time is cheap. |
| **If implementing** | Frame explicitly as feed feature + linear validation, not sheath formation. |
| **Default for Song/Tu sheath work** | Keep **voltage** drive; it matches potential-controlled sheath physics. |

### One-sentence summary

**Current drive is a legitimate antenna-feed option and a useful consistency tool; it is not a workaround for missing kinetic (or nonlinear collection) charging in fluid PF-FDTD, and it is not supposed to make Tu Fig. 2 appear by itself.**

---

## 6. Pointers

| Item | Location |
|------|----------|
| Email thread | `docs/references/Alireza_collaboration.pdf` |
| Early runs without bias | `docs/references/collision-3_merged.pdf` |
| Tu 2008 | `docs/references/JGR2008_Tu_plasma_sheath.pdf` |
| Song 2007 | `docs/references/JGR2007 - Song - ….pdf` |
| Present feed | `src/source/source.cpp`, `.vc` in `src/pffdtd.cpp` |
| Self-consistent path | `paper3_self_consistent_sheath/` |

*Last updated: 2026-09-07.*
