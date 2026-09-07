# Why Our \(f_\mathrm{res}(S_d)\) Disagrees with Tu (2008)

**Date:** 2026-09-04  
**Status:** interpretive note (post low-f CW)  
**Data:** `analysis/cw_lowf_findings.md`, August + September `results/sheath_cw_tu/`  
**Models:** `docs/SHEATH_MODELS_LITERATURE_DISCUSSION.md`  
**Report:** `validation/phase_7_documentation/` Chapters low-f / **discrepancy** / status

---

## 1. The discrepancy

**Campaign expectation** (circuit/FDTD reading of Tu): wider vacuum sheath \(S_d\) reduces dielectric loading near the dipole, so series resonance \(f_\mathrm{res}\) (first Im\(\{Z\}\) +→− crossing) should move **upward** toward free space.

**What we measure** after the PEC-seeded coupling fix:

| \(S_d\) | \(f_\mathrm{res}\) (Im +→−) |
|--------:|----------------------------:|
| 0 | ≈ 1.846 MHz |
| 2 | ≈ 0.655 MHz |
| 10 | ≲ 0.50 MHz (all capacitive in 0.5–1.5 MHz) |

So \(f_\mathrm{res}\) **falls** with \(S_d\) under this metric — opposite to the upward-shift target. Sheath **is** coupled (\(|\Delta Z|/|Z_0|\) typically 80–350%); this is not the pre-fix “\(Z\) independent of \(S_d\)” failure.

---

## 2. Possible reasons (ranked)

### 2.1 Competing physical limits (most likely)

Thickening a vacuum jacket does two things at once:

1. **Less plasma dielectric** near the wire → resonance tends to rise toward free space (the usual campaign “Tu reading”).
2. **Series sheath capacitance** \(1/(j\omega C_\mathrm{sh})\) → phase-zero is pulled **down**, as in Liu’s \(f_{\phi0}<f_{uh}\) and in Balmain-era gap/sheath corrections.

Our Im-zero trend looks like the **series-\(C\)** limit winning. That is a coherent circuit outcome for a prescribed vacuum jacket, not necessarily a solver bug.

### 2.2 We are not simulating Tu’s problem one-to-one

Tu (2008) is **1D PIC**, self-consistent, **time-varying** sheath around a **high-voltage transmitting** dipole. We prescribe a **static step-profile** vacuum shell of width \(S_d\) cells in 3D **fluid** FDTD (campaigns so far effectively unmagnetized). So:

- no oscillating sheath radius  
- no kinetic charging / collection as the primary mechanism  
- \(S_d\) is a knob, not Tu’s physical sheath  

Expecting Tu’s \(f_\mathrm{res}(S_d)\) curve from a fixed jacket may be the wrong validation target.

### 2.3 Resonance marker mismatch

We define resonance as the first Im\(\{Z\}\) **+→−** crossing. Literature often separates phase-zero / series Im-zero from magnitude or admittance peaks (and from upper-hybrid-type features when \(B\neq 0\)). For large \(S_d\) the inductive branch is weak or gone in-band; the +→− pick can track **sheath-dominated phase-zero** rather than the “plasma-loaded antenna resonance” the upward-shift narrative implies.

### 2.4 Geometric / volumetric loading is huge on this grid

With \(\Delta x=0.04\,\mathrm{m}\), \(S_d=2\) is already an **8 cm** vacuum jacket on a thin wire. That is a strong capacitive load (small \(C_\mathrm{sh}\) → large \(|X_C|\)). Staircasing and an effective wire radius thicker than a physical thin wire amplify this relative to Tu’s geometry or a real PIP \(t_\mathrm{sh}\).

### 2.5 \(S_d=0\) baseline is not free space

“Plasma to the wire” on a Yee grid still has numerical gaps and fluid constitutive assumptions. Free-space \(f_\mathrm{res}\) on the **same** dipole remains an open anchor — needed to separate “toward vacuum” from “sheath \(C\) domination.”

### 2.6 Secondary model differences

Unmagnetized fluid Maxwell–plasma vs Tu’s kinetic setup; hard \(E_z\) feed and Ampère-loop \(I\); collisions, drive amplitude, and electrical length. These can change numbers; they are less likely than §§2.1–2.4 to flip the **sign** of \(df_\mathrm{res}/dS_d\).

---

## 3. Why the model behaves as *series* (not parallel) \(C_\mathrm{sh}\)

The vacuum shell sits **between** the conductor and the bulk plasma, in the radial current path:

```text
Series (what the volumetric jacket does)     Parallel (not what Sd does)

  V ── C_sh ── Z_plasma                      V ──┬── Z_ant+plasma
            (to return)                           │
                                                  C_sh (shunt across feed)
                                                  │
                                                 return
```

1. PEC carries conduction current.  
2. For \(S_d>0\), depleted cells have \(J\approx 0\) (vacuum).  
3. Bulk plasma starts only **outside** the jacket.  
4. Coupling to plasma is therefore **displacement current across the gap** — a capacitor between metal and plasma edge.

That is the same **topology** as Liu’s coax sheath and as Balmain-era insulating/sheath gap models:  
\(Z_\mathrm{in}\approx Z_\mathrm{pl}+1/(j\omega C_\mathrm{sh})\).

A **parallel** (shunt) sheath \(C\) would be a path **across the feed terminals that bypasses** the antenna–plasma chain (e.g. a lumped feed capacitor). Arm-to-arm fringing always exists for a dipole, but the **\(S_d\)-dependent** change is the radial jacket — series loading.

**Do not confuse** the pedagogical parallel-plate estimate \(C\sim\varepsilon_0 A/(S_d\Delta x)\) with parallel *topology*. That formula only estimates the **series** gap capacitor; for a thin wire the emergent \(C_\mathrm{sh}\) is closer to cylindrical/coaxial (log in gap radius).

---

## 4. Which model is closer to ionospheric PIP truth?

For **ionospheric impedance probes** (small-signal diagnostic, magnetized plasma, quasi-steady sheath):

| Model | Role for PIP |
|--------|----------------|
| **Liu-type** (Balmain-like \(Z_\mathrm{pl}\) + **series** coax \(C_\mathrm{sh}\), markers \(f_{uh}\) vs \(f_{\phi0}\), GUM) | Best **operational** match |
| **Balmain 1964** (homogeneous magnetoplasma) | Core plasma \(Z\); sheath not first-class in the closed form |
| **Later Balmain / 1960s–90s sheath work** | Ion sheath, bias expand/collapse, contact, insulating jackets, sheath waves — **same series-gap lineage** as Liu |
| **Self-consistent kinetic / PIC (low drive, with \(B\))** | Closest absolute physics; often a consistency check |
| **Tu (2008)** | Physically rich **HV transmitter** problem — different regime |
| **This campaign’s prescribed FDTD \(S_d\)** | Correct **series** topology; not PIP truth as run (fixed step sheath, often unmagnetized, \(S_d\Delta x\) can dwarf real \(t_\mathrm{sh}\)) |

**Corrected lineage (do not say “Balmain had no sheath”):**

> Balmain plasma impedance → later Balmain / contemporary sheath–gap models → modern PIP (Liu, Brooks, PCEM, …).

Liu does not invent sheath physics Balmain missed; it makes the sheath an **operational, fitted, uncertainty-budgeted** coax term for retrieval.

---

## 5. Bottom line

- Coupling works; the discrepancy is **model / metric / loading**, not “sheath missing from the feed.”  
- Under a prescribed vacuum jacket, **series \(C_\mathrm{sh}\)** naturally pulls Im-zero **down** — consistent with Liu-style phase-zero, not with an upward Tu-shift target for this setup.  
- Next checks: free-space \(f_\mathrm{res}\) on this dipole; \(C_\mathrm{eff}(S_d)\) from low-\(f\) Im\(\{Z\}\); alternate markers (\(|Z|\) / admittance); decide whether Tu upward \(f_\mathrm{res}(S_d)\) remains the right FDTD validation target.

---

*Last updated: 2026-09-04.*
