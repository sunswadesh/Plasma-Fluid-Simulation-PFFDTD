# Antenna–Sheath PF-FDTD — Project Guide

Authoritative program guide. Update when paper boundaries or success metrics change. Read [`CHRONICLE.md`](CHRONICLE.md), this guide, and [`docs/SHEATH_MODELS_LITERATURE_DISCUSSION.md`](docs/SHEATH_MODELS_LITERATURE_DISCUSSION.md) before opening a paper folder.

## How to use this guide

| Section | Audience |
|---------|----------|
| [Science overview](#science-overview) | Everyone |
| [What the 2026 campaign established](#what-the-2026-campaign-established) | Everyone |
| [Fidelity ladder](#fidelity-ladder) | Papers 0–3 |
| [Locked decisions](#locked-decisions) | Do not reopen without discussion |
| [Paper map](#paper-map) | Implementation entry points |

---

## Science overview

### Program goal

Build a **clear, publishable path** from the existing PF-FDTD prescribed-sheath capability to Song/Tu-class antenna–sheath physics, without forcing one misaligned observable to carry the whole story.

### Physical picture

1. **Series sheath.** A vacuum (or depleted) layer between conductor and bulk plasma inserts \(Z_\mathrm{sh}\approx 1/(j\omega C_\mathrm{sh})\) in series with the plasma-loaded antenna impedance. Phase-zero can move **down** relative to bulk plasma features (Liu \(f_{\phi0}\) intuition).  
2. **Song (2007).** HV bare dipole; electron-free ion sheath; net charge antenna+sheath ≈ 0; \(r_s(t)\) oscillates; \(\dot{r}_s\) supplies radiation current; system predominantly reactive; analytic \(C_\mathrm{sh}\) ~20% low vs IMAGE/RPI.  
3. **Tu (2008).** 1D PIC of Song’s problem; self-consistent charging; reactance ~10% better than Song analytics.  
4. **This solver.** 3D Maxwell + **fluid** plasma; optional prescribed density hole of width \(S_d\) cells (`ApplySheath` in `src/physics/plasma.cpp`).

### End-to-end chain

```text
Paper 0 — campaign Phases 0–8 (coupling, CW, low-f, discrepancy)
        │
        ▼
Paper 1 — static Sd → C_eff(Sd) vs coax / Song static
        │
        ▼
Paper 2 — prescribe rs(t) → test Song ṙs mechanism in 3D FDTD
        │
        ▼
Paper 3 — self-consistent sheath
          (3a fluid+charging  and/or  3b PIC)
```

---

## What the 2026 campaign established

| Result | Implication |
|--------|-------------|
| Pre-fix: \(Z\) independent of \(S_d\) | Sheath never entered the feed (seed bug) |
| Post-fix: \(\lvert\Delta Z\rvert/\lvert Z_0\rvert\) large | Volumetric sheath **works** in PF-FDTD |
| \(f_\mathrm{res}(0)\approx1.85\,\mathrm{MHz}\), \(f_\mathrm{res}(2)\approx0.66\,\mathrm{MHz}\), \(f_\mathrm{res}(10)\lesssim0.5\,\mathrm{MHz}\) | Im-zero tracks **series \(C\)**, not “Tu upward shift” |
| Song/Tu read carefully | Wrong scoreboard was \(f_\mathrm{res}\uparrow\); right Song quantities are \(C_\mathrm{sh}\), \(X_s\), \(\dot{r}_s\) |

Evidence: [`CHRONICLE.md`](CHRONICLE.md), [`paper0_sheath_campaign/`](paper0_sheath_campaign/), [`validation/`](validation/).

---

## Fidelity ladder

| Stage | Sheath model | Observable | Engine change? |
|-------|--------------|------------|----------------|
| Paper 0 | Campaign / methods | Coupling proof; discovery of series-\(C\) trend | Done |
| Paper 1 | Static prescribed \(S_d\) | \(C_\mathrm{eff}(S_d)\), multi-marker \(Z(f)\) | No |
| Paper 2 | Kinematic \(r_s(t)\) | Feed \(Z\), radiated fields vs \(\dot{r}_s\) | Small (time-varying mask) |
| Paper 3a | Fluid + nonlinear charging (Song-encoded) | \(C_\mathrm{sh}\), bias, sheath structure | Yes — plasma/sheath module |
| Paper 3b | PIC (Tu-like) | Reactance vs Song/Tu | Yes — kinetic engine |

Varying static \(S_d\) **partially** simulates a changing sheath (quasi-static thickness samples). It does **not** replace \(\dot{r}_s\) dynamics or self-consistent charging.

---

## Locked decisions

1. **Do not** use “Im\(\{Z\}\) +→− climbs with \(S_d\)” as the Song/Tu success metric.  
2. **Paper 0** owns the campaign chronicle; **Paper 1** owns \(C_\mathrm{eff}\) science — do not merge them in one abstract.  
3. **Paper 1 success** = quantitative \(C_\mathrm{eff}(S_d)\) vs coax (and optionally Song static \(C(r_s)\)), plus free-space / multi-marker reporting.  
4. **Paper 2** keeps Maxwell + fluid core; sheath motion is **prescribed**, not charged self-consistently.  
5. **Paper 3** chooses 3a and/or 3b explicitly; do not blur “fluid charging” with “PIC” in titles or abstracts.  
6. Shared literature narrative stays in `docs/SHEATH_MODELS_LITERATURE_DISCUSSION.md`; paper folders do not fork a second Balmain/Liu/Tu essay.  
7. Campaign products live under `paper0_sheath_campaign/analysis/`; root `analysis/` is a redirect only.  
8. Results remain under `<collab-repo-root>/results/` (gitignored). Do not set `$env:PFFDtd_ROOT`.

---

## Paper map

| Paper | README | First concrete work |
|-------|--------|---------------------|
| 0 | [`paper0_sheath_campaign/`](paper0_sheath_campaign/) | Keep chronicle current; optional methods draft |
| 1 | [`paper1_static_sheath_capacitance/`](paper1_static_sheath_capacitance/) | Free-space CW; \(C_\mathrm{eff}\) from Paper 0 low-f data |
| 2 | [`paper2_oscillating_sheath_boundary/`](paper2_oscillating_sheath_boundary/) | Pilot static vs \(r_s(t)\); fill Radio Science draft results |
| 3 | [`paper3_self_consistent_sheath/`](paper3_self_consistent_sheath/) | Requirements; gated on Paper 1 (+ ideally 2) |

### Solver pointers

- Sheath implementation: `src/physics/plasma.cpp`, `plasmaNSheath.h`  
- Build: `compile.bat` or `cmake --build build --target pffdtd_parallel`  
- Campaign scripts: [`scripts/`](scripts/)  
- Docs index: [`docs/DOCUMENTATION_INDEX.md`](docs/DOCUMENTATION_INDEX.md)
