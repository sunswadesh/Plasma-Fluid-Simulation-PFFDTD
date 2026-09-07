# Chronology — Antenna–Sheath PF-FDTD program

Linear development story with hindsight. For paper boundaries and locked decisions see [`PROJECT_GUIDE.md`](PROJECT_GUIDE.md). For phase-by-phase lab notes see [`validation/`](validation/) and [`paper0_sheath_campaign/`](paper0_sheath_campaign/).

---

## 1. Motivation (early 2026)

Validate PF-FDTD dipole impedance with a **prescribed vacuum sheath** of width \(S_d\) cells. Campaign target (circuit reading of Tu 2008): wider sheath → less dielectric loading → series resonance \(f_\mathrm{res}\) (Im\(\{Z\}\) +→−) moves **up** toward free space.

## 2. February–May: baselines and null sheath sweeps

| Step | What happened |
|------|----------------|
| Feb baseline | Free-space vs plasma dipole impedance measurable |
| Pulse / narrowband CW \(S_d\) sweeps | Inconclusive or **no** \(S_d\) dependence |
| \(f_p\) screen | Clean resonance, but \(Z(S_d=0)\equiv Z(S_d=10)\) |

**Lesson (found later):** sheath density hole was seeded from the plasma-on mask **before** antenna geometry existed → hole at domain edge, not around the wire.

## 3. Coupling fix (Phase 4)

PEC-seeded distance field in `ApplySheath` (`src/physics/plasma.cpp`). Post-fix CW: feed \(Z\) **strongly** depends on \(S_d\).

Detail: [`paper0_sheath_campaign/analysis/sheath_coupling_findings.md`](paper0_sheath_campaign/analysis/sheath_coupling_findings.md)

## 4. August dense CW (Phase 6)

\(f_p=2\,\mathrm{MHz}\), 1.50–2.30 MHz, \(S_d=0\ldots10\):

- \(S_d=0\): \(f_\mathrm{res}\approx 1.846\,\mathrm{MHz}\)
- \(S_d\ge 2\): Im\(\{Z\}<0\) everywhere in-band — no upward crossing

## 5. September low-f CW (Phase 8)

Extended to 0.50–1.50 MHz (\(S_d=0,2,10\)):

| \(S_d\) | \(f_\mathrm{res}\) (Im +→−) |
|--------:|----------------------------:|
| 0 | ≈ 1.85 MHz (from Aug band) |
| 2 | ≈ 0.66 MHz |
| 10 | ≲ 0.50 MHz |

**Hindsight:** series sheath capacitance dominates; the Tu “upward \(f_\mathrm{res}\)” scoreboard was the wrong exam question.

Detail: [`paper0_sheath_campaign/analysis/cw_lowf_findings.md`](paper0_sheath_campaign/analysis/cw_lowf_findings.md), [`tu_discrepancy_discussion.md`](paper0_sheath_campaign/analysis/tu_discrepancy_discussion.md)

## 6. Literature realignment

Song (2007) / Tu (2008) quantify **sheath reactance / \(C_\mathrm{sh}\)** and (Song) **oscillating** \(r_s(t)\). Liu/Balmain-gap models treat sheath as **series \(C\)**. Shared essay: [`docs/SHEATH_MODELS_LITERATURE_DISCUSSION.md`](docs/SHEATH_MODELS_LITERATURE_DISCUSSION.md).

## 7. Program split (Sep 2026)

```text
Paper 0  campaign & discovery (this chronology’s evidence)
Paper 1  static Sd → C_eff vs coax / Song static
Paper 2  kinematic rs(t) → Song ṙs mechanism
Paper 3  self-consistent sheath (fluid charging and/or PIC)
```

---

*Last updated: 2026-09-07.*
