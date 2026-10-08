# Antenna–Sheath PF-FDTD Program

Three-paper program (plus a campaign chronicle) on **how a plasma sheath loads a radio-frequency dipole** in the Plasma Fluid FDTD (PF-FDTD) solver — from a prescribed vacuum jacket, through a prescribed oscillating boundary, toward self-consistent charging.

**Start here:**

1. [`CHRONICLE.md`](CHRONICLE.md) — linear development story (hindsight)  
2. [`PROJECT_GUIDE.md`](PROJECT_GUIDE.md) — science overview, locked decisions, paper map  
3. [`docs/SHEATH_MODELS_LITERATURE_DISCUSSION.md`](docs/SHEATH_MODELS_LITERATURE_DISCUSSION.md) — Balmain / Liu / Song / Tu / this solver  
4. [`STATUS.md`](STATUS.md) — dashboard

---

## What led to this study

A 2026 validation campaign set out to reproduce a common **circuit reading of Tu et al. (2008)**: thicken a vacuum sheath around a dipole and watch series resonance \(f_\mathrm{res}\) (Im\(\{Z\}\) +→−) move **up** toward free space.

Early runs showed no \(S_d\) dependence because sheath depletion was seeded from the wrong mask (domain-edge hole, not wire-adjacent). After a **PEC-seeded coupling fix**, feed impedance depended strongly on sheath width — but under the Im-zero metric \(f_\mathrm{res}\) **fell** with \(S_d\) (≈1.85 → 0.66 → ≲0.50 MHz). That is the signature of **series sheath capacitance**, not dielectric unloading toward vacuum.

Reading Song et al. (2007) and Tu et al. (2008) carefully showed the campaign target was misaligned with those papers: Song/Tu quantify **sheath reactance / \(C_\mathrm{sh}\)** and (for Song) radiation via an **oscillating sheath boundary**, not an upward \(f_\mathrm{res}(S_d)\) curve for a static jacket. Liu-style PIP models and Balmain-era gap corrections already treat the sheath as series \(C\).

This program therefore **keeps the working PF-FDTD sheath machinery** and splits the science into a campaign chronicle plus three forward papers.

---

## Science picture (one paragraph)

A bare or vacuum-jacketed antenna in plasma does not see a homogeneous dielectric. Near the conductor, density is depleted (sheath). In circuit language that region acts as a **series capacitor** between the metal and the bulk plasma impedance. For driven (high-voltage) antennas the sheath is largely electron-free and **reactive**, and a sheath boundary oscillating at the drive frequency can itself supply radiation current — the dynamic regime treated kinetically in the literature. Separately, plasma impedance probe (PIP) retrieval uses an analytic coaxial \(C_\mathrm{sh}(t_\mathrm{sh})\). Our solver can impose a volumetric density hole of width \(S_d\) and measure feed \(Z(f)\). The open questions are: (0) what did the campaign establish? (1) does that imposed gap reproduce analytic series \(C_\mathrm{sh}\)? (2) does a *moving* prescribed boundary load and radiate beyond the static brackets in 3D FDTD? (3) can fluid charging or PIC make the sheath self-consistent?

```text
Campaign Phases 0–8          Prescribed static Sd          Prescribed rs(t)           Self-consistent sheath
(discovery / methods)  →   (quasi-static C(rs))     →   (moving-boundary coupling)      →  (fluid charging / PIC)
     Paper 0                        Paper 1                      Paper 2                      Paper 3
```

---

## Papers / tasks

| # | Folder | Focus | Potential paper claim |
|---|--------|--------|------------------------|
| 0 | [`paper0_sheath_campaign`](paper0_sheath_campaign/) | Phases 0–8 chronicle; coupling fix; low-f discovery | Volumetric sheath in PF-FDTD: seed bug → series-\(C\) loading |
| 1 | [`paper1_static_sheath_capacitance`](paper1_static_sheath_capacitance/) | Prescribed \(S_d\); \(C_\mathrm{eff}\) vs dipole coax | 3D fluid FDTD volumetric sheath behaves as series \(C_\mathrm{sh}(r_s)\) |
| 2 | [`paper2_oscillating_sheath_boundary`](paper2_oscillating_sheath_boundary/) | Kinematic \(r_s(t)\); test \(\dot{r}_s\) coupling | Oscillating sheath boundary in 3D PF-FDTD (dynamic loading without PIC) |
| 3 | [`paper3_self_consistent_sheath`](paper3_self_consistent_sheath/) | Fluid nonlinear charging and/or PIC | Self-consistent sheath formation, structure, and reactance |

**Writing rule:** shared background in `PROJECT_GUIDE.md`, `CHRONICLE.md`, and `docs/SHEATH_MODELS_LITERATURE_DISCUSSION.md`. Each `paper*/` folder adds only paper-specific plans, methods, and results.

- Campaign evidence: [`paper0_sheath_campaign/analysis/`](paper0_sheath_campaign/analysis/)  
- Raw phase runbooks: [`validation/`](validation/)  
- Solver: repo-root `src/` → `pffdtd_parallel.exe`  
- Results: `<repo-root>/results/` (gitignored)

## Related local paths

- Collab solver repo: this tree (`2026 Collab_PFFDTD_Sheath`, branch `PffdtdSheath`)
- References: [`docs/references/`](docs/references/) (Song 2007 JGR, Tu 2008 JGR, …)
- Pattern sibling: `D:\Swadesh\Work\IonOutflowWINDMI`
