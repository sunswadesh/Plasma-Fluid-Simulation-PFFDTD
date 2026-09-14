# Paper 3 — Self-consistent sheath

**Working title (fluid track).** *Nonlinear fluid charging and sheath formation around a high-voltage RF dipole in PF-FDTD.*  
**Working title (kinetic track).** *Kinetic (PIC) sheath structures for a high-voltage RF antenna: closing the loop with Song (2007) and Tu (2008).*

**Status:** Requirements only — **no implementation until Paper 1 closes** (Paper 2 recommended as go/no-go).  
**Guide:** [`../PROJECT_GUIDE.md`](../PROJECT_GUIDE.md)

---

## Science question

Can we replace the **prescribed** density hole with a **self-consistent** sheath — formed by charging and particle (or fluid nonlinear) response — so that \(C_\mathrm{sh}\), bias, and (if dynamic) \(r_s(t)\) emerge from the physics, as in Song/Tu?

Two implementation tracks are allowed; they must not be conflated in one abstract.

| Track | Engine | Closest literature | Role |
|-------|--------|--------------------|------|
| **3a** | Maxwell + **fluid nonlinear sheath/charging** (Song-encoded rules) | Song 2007 | Continuum self-consistency; same FDTD core |
| **3b** | **PIC** (or hybrid) sheath module | Tu 2008 | Kinetic fidelity; Tu reactance benchmark |

## Why this can be a paper

- Completes the fidelity ladder: static \(C\) → kinematic \(\dot{r}_s\) → **emergent** sheath.  
- 3a: novel if a Song-like charging/sheath closure is embedded in 3D fluid FDTD.  
- 3b: first-principles comparison to Tu’s PIC reactance / sheath structure (likely 1D or reduced 3D at first).

## Observables (success metrics)

| Metric | 3a | 3b |
|--------|----|----|
| Emergent \(C_\mathrm{sh}\) / \(X_s\) vs Song analytics | Primary | Primary |
| DC negative charging / electron-depleted sheath | Required | Required |
| Oscillating \(r_s(t)\) without prescription | Desired | Desired |
| Reactance within ~10–20% of Song/Tu/RPI-class numbers | Stretch | Tu’s own bar |
| Match Paper 2 kinematic signatures when drive is similar | Consistency check | Consistency check |

## Physics engine change (explicit)

Papers 1–2 keep prescribed \(N_0\to N_\min\). Paper 3 **changes the plasma/sheath module**:

- **3a:** potential/charge-based sheath edge, electron-free (or depleted) region, optional ion current balance; still fluid continuum.  
- **3b:** particle species, collection at PEC, self-consistent \(\rho\) on the grid or embedded 1D radial PIC coupled to the antenna.

Maxwell core can stay; sheath formation physics cannot stay as static `ApplySheath(Sd)`.

## Decision gate (before coding)

Answer in `design/track_choice.md` after Paper 1–2 evidence:

1. Did Paper 2 show a clear \(\dot{r}_s\) effect worth self-consistency?  
2. Is the goal PIP-relevant continuum sheath (favor 3a) or Tu kinetic benchmark (favor 3b)?  
3. Person-months and compute available?  
4. Can 3a be staged first with 3b as a follow-on letter?

Default recommendation: **3a first** unless the group explicitly prioritizes Tu-number matching.

## Work plan (post-gate)

1. Requirements & equations (Song boundary conditions vs fluid discretization).  
2. Minimal 1D radial prototype (even inside this repo’s `paper3/.../proto/`) before full 3D.  
3. Compare emergent \(C_\mathrm{sh}\) to Paper 1 coax and Song formulas.  
4. Manuscript track-specific; cite Papers 1–2 as prior rungs.

## Folder layout

```text
paper3_self_consistent_sheath/
├── README.md
├── PLAN.md
├── design/          ← track choice, equation notes
├── proto/           ← optional 1D/reduced prototypes
├── analysis/
└── draft/
```

## Depends on

- **Hard:** Paper 1 closed scoreboard (\(C_\mathrm{eff}\), series-\(C\) language).  
- **Strongly recommended:** Paper 2 go/no-go on dynamic coupling.  
- **Literature:** Song 2007, Tu 2008 PDFs in [`../docs/references/`](../docs/references/).  
- **Not a substitute for Paper 3:** voltage→current feed switch — see [`../docs/VOLTAGE_VS_CURRENT_DRIVE.md`](../docs/VOLTAGE_VS_CURRENT_DRIVE.md).
