# Sheath Impedance Models: Literature Discussion and Design Choices

**Purpose.** Compare Balmain-type antenna–plasma models (including later sheath/gap work), Liu et al.’s sheath-aware PIP formulation, Tu et al. (2008) kinetic sheath physics, and the PF-FDTD volumetric-sheath approach used in this campaign. Interpret the **downward** \(f_\mathrm{res}(S_d)\) discrepancy vs the campaign’s Tu upward-shift target (detail: [`analysis/tu_discrepancy_discussion.md`](../analysis/tu_discrepancy_discussion.md)).

**Primary external sources**

| Work | Role in this note |
|------|-------------------|
| Balmain (1964), *IEEE TAP* | Short-dipole impedance in a **homogeneous** cold magnetoplasma |
| Balmain (1969), *IEEE TAP*; related 1960s work | Admittance diagnostics (\(f_p\), \(f_{uh}\)); ion sheath / contact / bias expand–collapse |
| Later Balmain & coauthors (e.g. sheath waves; insulating / plasma jackets) | Explicit sheath-layer and sheath-wave models on antennas in magnetoplasma |
| Liu et al. (manuscript under review), *Sheath-Aware Measurement Uncertainty…* | Coaxial sheath + PIP retrieval / GUM |
| Tu, Song & Reinisch (2008), *JGR* | 1D PIC sheath around a HV transmitting dipole |
| Brooks & Paliwoda (2024), *PoP* | Related PIP uncertainty / sheath-resonance framing |
| This campaign (`projects/tu2008-sheath/`) | 3D fluid FDTD with prescribed \(S_d\) |

Local PDF copies: `docs/references/` (Tu; Brooks/NRL). Liu review copy: `D:\Swadesh\Work\Reviews\Paper Review\PIP_Sheath\`.

---

## 1. What Balmain’s model is (including later sheath papers)

Balmain’s best-known result (1964) is an **analytical expression for the input impedance of a short dipole in a cold magnetoplasma**, written in terms of the anisotropic plasma dielectric tensor. The antenna is electrically short; that closed-form formula is usually applied to a **homogeneous** magnetoplasma.

That does **not** mean Balmain ignored the sheath. **Later Balmain papers and related work** treat ion sheaths, insulating jackets, and sheath waves as first-class antenna–plasma physics:

- **Ion sheath as bias-controllable non-uniformity (1960s context).** A conducting surface is surrounded by an ion sheath that can be **expanded or collapsed by DC bias**. Collapsing the sheath is the usual way to make the near-antenna plasma “uniform enough” to compare with the homogeneous-medium formula.
- **Contact / compressible-plasma corrections.** Mid-1960s short-dipole analyses estimate low-frequency impedance contributions from plasma–metal contact when the sheath is collapsed and electron current flows to the surface.
- **Diagnostic admittance (Balmain 1969).** Quasi-static dipole admittance in a cold collisional magnetoplasma, oriented toward identifying \(f_p\) and \(f_{uh}\) from admittance spectra.
- **Later sheath / jacket / sheath-wave models.** Subsequent Balmain and coauthor papers (insulating or plasma jackets on linear antennas; magnetoplasma **sheath-wave** propagation on tethers and structures, e.g. Laurin–Morin–Balmain and related NASA/Radio Science lines) put a depleted or dielectric layer around the conductor and study how that layer loads \(Z\) and supports guided waves. Topology is still a **series gap** between metal and exterior plasma, not a shunt across the feed.
- **Broader contemporary sheath–antenna literature.** Parallel treatments (e.g. Mlodnosky & Garriott, Shkarofsky, Baker et al., vacuum-gap / insulating-layer models) already put sheath capacitance in series with the plasma impedance. Sheath awareness in PIP/antenna theory is **not a 2020s invention**.

So the accurate split is:

| Layer | What Balmain-era models did |
|-------|-----------------------------|
| Core closed-form \(Z\) (1964) | Homogeneous cold magnetoplasma dipole (tensor \(\varepsilon\)) |
| Sheath in practice / later papers | Bias expand–collapse; contact corrections; **explicit sheath or insulating jackets**; sheath-wave propagation |
| What they generally did *not* do | Self-consistent kinetic sheath evolution (Tu-like PIC), or a full GUM retrieval budget for \(n_e\) and \(\nu\) under sheath error (Liu-like metrology) |

**Do not write “Balmain had no sheath.”** Write: **1964 Balmain is homogeneous; later Balmain (and contemporaries) include sheath/gap models** that modern PIP formulations continue.

In circuit language, Balmain-type models answer:

> Given \(\varepsilon(\omega,\mathbf{B})\) (and, when included, a prescribed sheath/contact layer), what is \(Z_\mathrm{ant}(\omega)\)?

Later PIP literature (Blackwell, Spencer, Suzuki, Gatling, Brooks, Liu, …) keeps that analytic/lumped spirit while making the sheath term **explicit, fitted, and uncertainty-budgeted** for modern probe operations.

---

## 2. What Liu’s model is (and how it relates to Balmain)

Liu et al. build a **sheath-loaded cylindrical-monopole PIP model** for low-collisionality ionosphere (~200 km). The working equation is lumped and Balmain-inspired:

\[
Z_\mathrm{PIP}(\omega)
= Z_\mathrm{sh}(t_\mathrm{sh})
+ Z_\mathrm{pl}\bigl(\varepsilon_\perp(n_e,B,\nu)\bigr).
\]

Explicitly (their coaxial sheath + transverse cold-plasma dielectric):

\[
C_\mathrm{sh}
= \frac{2\pi\varepsilon_0 L}{\ln\!\bigl(1 + t_\mathrm{sh}/r\bigr)},
\qquad
Z_\mathrm{sh} = \frac{1}{j\omega C_\mathrm{sh}},
\]

\[
\varepsilon_\perp
= 1 - \frac{\omega_p^2}{\omega^2 - \omega_c^2 + j\nu\omega},
\qquad
Z_\mathrm{pl}
= \frac{1}{j\omega\, C_\mathrm{pl}\,\varepsilon_\perp}.
\]

### Comparison to Balmain-era models

| Aspect | Balmain 1964 + later sheath papers | Liu et al. |
|--------|--------------------------------------|------------|
| Geometry | Short **dipole** (and related linear antennas / tethers) in magnetoplasma | Short **cylindrical monopole** (probe head) |
| Plasma constitutive law | Full anisotropic cold-plasma tensor | Effective **scalar** \(\varepsilon_\perp\) (transverse / weakly magnetized) |
| Sheath | 1964 often homogeneous; **later** bias expand/collapse, contact, jackets, sheath waves | **Operational** coaxial vacuum layer \(t_\mathrm{sh}\) inside the retrieval model |
| How sheath is used | Collapse for homogeneous theory–experiment; or model gap / wave on jacket | Fitted / calibrated; drives \(f_{\phi0}\) vs \(f_{uh}\) distinction |
| Purpose | Antenna / diagnostic / EMI–sheath-wave theory | **Retrieve** \(n_e\), \(\nu\), constrain \(t_\mathrm{sh}\) with **GUM** uncertainty |
| Resonance markers | \(f_p\), \(f_{uh}\) identifiable in admittance (esp. 1969 line) | Split: physical \(f_{uh}\) vs sheath-shifted phase-zero \(f_{\phi0}\) |

Liu is therefore **not inventing sheath physics that Balmain missed**. It continues the **Balmain → later Balmain sheath/gap → modern PIP** lineage: keep a Balmain-like lumped plasma term, specialize geometry to a monopole, write the sheath as an explicit coax capacitor, and quantify how sheath error biases density and collision retrieval.

Kinetic PIC (EDIPIC-2D) in Liu is only a **consistency check** (self-consistent sheath + resonance near prescribed \(f_{uh}\)), not the operational retrieval model.

---

## 3. What “coaxial analytic sheath” means

“Coaxial” refers to geometry; “analytic” refers to a closed-form capacitor formula.

Imagine the monopole as a metal cylinder of radius \(r\) and length \(L\). The sheath is approximated as a **vacuum annular shell** from \(r\) to \(r+t_\mathrm{sh}\), with bulk plasma outside. That is exactly the geometry of a **coaxial cylindrical capacitor**:

```text
          plasma (ε_⊥)
    ┌─────────────────────────┐
    │      ┌───────────┐      │
    │      │  vacuum   │      │  ← sheath thickness t_sh
    │      │  ┌─────┐  │      │
    │      │  │ metal│  │      │  ← radius r
    │      │  └─────┘  │      │
    │      └───────────┘      │
    └─────────────────────────┘
```

The capacitance per length of an infinite coax is \(\propto 1/\ln(b/a)\). With \(a=r\) and \(b=r+t_\mathrm{sh}\),

\[
C_\mathrm{sh}
= \frac{2\pi\varepsilon_0 L}{\ln(1 + t_\mathrm{sh}/r)}.
\]

That is the **coaxial analytic sheath**: sheath impedance enters \(Z\) as \(1/(j\omega C_\mathrm{sh})\) with \(C_\mathrm{sh}\) from electrostatics of concentric cylinders—not from a particle simulation and not from a 3D FDTD density field.

**Implications**

- \(t_\mathrm{sh}\) is a **scalar parameter** (fitted or calibrated from low-frequency capacitive response).
- Series sheath capacitance forces \(\mathrm{Im}\{Z\}=0\) (**phase-zero** \(f_{\phi0}\)) **below** the bulk upper-hybrid feature \(f_{uh}\).
- Liu’s metrological point: do **not** insert \(f_{\phi0}\) into the upper-hybrid density formula; correct with the sheath model or track \(f_{uh}\) directly. Sheath-thickness error can devastate \(\nu\) retrieval even when \(n_e\) looks fine.

---

## 4. Tu et al. (2008): a different sheath problem

Tu’s PIC study addresses a **high-voltage transmitting dipole** in (unmagnetized) plasma:

- Sheath forms by **electron charging**; radius **oscillates** with the drive.
- Focus: kinetic structure, particle collection, reactance vs Song-type analytics (~10% improvement).
- Not a PIP density-retrieval instrument model; not a fixed \(t_\mathrm{sh}\) knob.

This campaign cites Tu as motivation for “sheath changes antenna impedance,” and maps that idea onto a **prescribed vacuum gap** \(S_d\) and an upward \(f_\mathrm{res}(S_d)\) expectation. That is a **circuit/FDTD reading** of sheath loading; it is not a one-to-one reproduction of Tu’s kinetic oscillating sheath.

---

## 5. Our comparable approach (PF-FDTD)

### Design choice

We do **not** insert a coaxial \(C_\mathrm{sh}\) into the feed. We deplete ambient density in a shell of width \(S_d\) cells around PEC:

\[
d \le S_d
\quad\Rightarrow\quad
N_0 \rightarrow N_0\cdot N_\mathrm{min}
\quad\Rightarrow\quad
\mathbf{J}\approx 0
\quad\Rightarrow\quad
\text{cells behave as vacuum}.
\]

Implementation: `ApplySheath()` in `src/physics/plasma.cpp` (PEC-seeded distance field; step profile). Feed observable remains

\[
Z(f)=\frac{V(f)}{I(f)}
\]

from `.vc` phasors. The series capacitance is **emergent** from the volumetric gap, not prescribed analytically.

### Mapping between models

| Concept | Liu / Balmain-PIP | This project |
|---------|-------------------|--------------|
| Sheath thickness | \(t_\mathrm{sh}\) (meters, fitted) | \(S_d\,\Delta x\) (cells × grid) |
| Sheath impedance | Analytic coax \(1/(j\omega C_\mathrm{sh})\) | Emergent from depleted Yee cells |
| Plasma response | \(\varepsilon_\perp(\omega)\) in a lumped \(Z_\mathrm{pl}\) | Fluid Maxwell–plasma on the full 3D grid |
| Antenna | Cylindrical monopole (analytic) | Thin-wire dipole on Yee lattice |
| Magnetization | Weak \(B\), upper-hybrid | Campaigns so far effectively unmagnetized |
| Goal | Correct \(n_e,\nu\) + uncertainty | Validate solver coupling / \(f_\mathrm{res}(S_d)\) |

**Rough circuit analogue** (what we *expect* the volumetric gap to mimic):

\[
Z_\mathrm{in}(f)
\approx
Z_\mathrm{ant+plasma}(f)
+ \frac{1}{j\omega C_\mathrm{sh}(S_d)},
\qquad
C_\mathrm{sh}
\sim
\frac{\varepsilon_0 A}{S_d\,\Delta x}.
\]

For a thin wire the true emergent \(C_\mathrm{sh}\) is closer to a **cylindrical** (logarithmic) dependence on gap radius than to a parallel-plate \(A/d\) form—the parallel-plate estimate is only a pedagogical limit. Liu’s coax formula is the analytic version of that cylindrical idea for a monopole.

### Why we chose volumetric depletion over coaxial \(C_\mathrm{sh}\)

1. **Solver fidelity.** PF-FDTD’s claim is 3D EM + fluid plasma. A hand-placed feed capacitor would validate a circuit, not the plasma–Maxwell coupling.
2. **Geometry.** Our sensor is a dipole on a Cartesian grid, not a cylindrical coax; a coax formula would be an extra approximation on top of the grid.
3. **Campaign goal.** Sweep \(S_d\) and see whether feed \(Z(f)\) responds as expected—an end-to-end test of sheath attachment after the SIG-seed bug.

Trade-off: we inherit **grid staircasing**, finite \(\Delta x\), and a **non-self-consistent** (prescribed) sheath, so \(S_d\) is not Tu’s oscillating kinetic radius and not Liu’s fitted \(t_\mathrm{sh}\).

---

## 6. Resolved measurement issue: \(S_d\ge 2\) capacitive / downward \(f_\mathrm{res}\)

### What the data say

**August dense CW** (`results/sheath_cw_tu/`, 66 cases, \(f_p=2\,\mathrm{MHz}\), 1.50–2.30 MHz):

- \(S_d=0\): \(\mathrm{Im}\{Z\}=0\) (+→−) at \(f_\mathrm{res}\approx 1.846\,\mathrm{MHz}\).
- \(S_d=2,4,6,8,10\): \(\mathrm{Im}\{Z\}<0\) at **every** frequency in that band—no in-band series crossing.

**September low-f CW** (same folder, 0.50–1.50 MHz, \(S_d=0,2,10\); ~53 h):

| \(S_d\) | Low-f Im{Z} | \(f_\mathrm{res}\) (Im +→−) |
|--------:|-------------|-----------------------------|
| 0 | All inductive | 1.846 MHz (August) |
| 2 | Cap→ind@0.60→cap for \(f\ge0.70\) | **0.655 MHz** |
| 10 | All capacitive | **≤ 0.50 MHz** |

![Low-f impedance (0.5–1.5 MHz)](figures/cw_lowf_impedance_zoom.png)

![Combined 0.5–2.3 MHz](figures/cw_lowf_impedance.png)

![Resonance vs Sd](figures/cw_lowf_resonance.png)

After the coupling fix, sheath **does** enter the feed, and the low-f extension shows the **opposite of Tu’s upward shift** under the +→− metric:

\[
f_\mathrm{res}(0)\approx 1.85\,\mathrm{MHz}
\;>\;
f_\mathrm{res}(2)\approx 0.66\,\mathrm{MHz}
\;>\;
f_\mathrm{res}(10)\lesssim 0.50\,\mathrm{MHz}.
\]

### Two different problem types

**A. GUM / retrieval problem (Liu’s world)**  
You already have a measured spectrum. Questions: Which marker is \(f_{uh}\)? How much does sheath bias \(f_{\phi0}\)? How do calibration, \(B\), and \(t_\mathrm{sh}\) errors propagate into \(n_e\) and \(\nu\)?  
Success = uncertainty budget + corrected density.  
**This is not our open issue.** We are not retrieving ionospheric \(n_e\) from a VNA; we are testing whether a numerical sheath shifts a simulated resonance the way a validation target claims.

**B. Volumetric-loading / resonance-definition problem (our world)**  
We prescribe a vacuum shell and measure feed \(Z\). Questions:

1. **Volumetric loading.** For \(\Delta x=0.04\,\mathrm{m}\), \(S_d=2\) is already an \(8\,\mathrm{cm}\) vacuum jacket around a thin wire. That is a large series capacitance (small \(C_\mathrm{sh}\) in the \(1/(j\omega C)\) sense means *large* \(|X_C|\) contribution, or equivalently a strong capacitive branch in \(Z_\mathrm{in}\)). The feed can sit on the capacitive side of resonance across the whole scanned band.
2. **Direction of the shift under a series-\(C\) picture.** Adding series capacitance does **not** automatically push an LC series crossing *up* toward free space. In a simple series model, sheath capacitance can move the reactance-zero **down** in frequency relative to the plasma-loaded antenna—exactly Liu’s \(f_{\phi0}<f_{uh}\) statement. Our campaign narrative often phrases Tu as “wider sheath → less dielectric loading → \(f_\mathrm{res}\) up toward free space.” That picture mixes two limits:
   - *Removing plasma dielectric* near the antenna (less \(\varepsilon>1\) loading) tends to raise resonance toward vacuum.
   - *Inserting a vacuum gap as series \(C_\mathrm{sh}\)* tends to pull the **phase-zero** below the bulk plasma feature.
   Which effect wins depends on geometry, how \(S_d=0\) is defined (plasma to the wire vs already a numerical gap), and which marker is called “resonance.”
3. **Resonance definition.** We use the first \(\mathrm{Im}\{Z\}\) +→− crossing as series resonance. Liu insists that phase-zero and upper-hybrid magnitude peak are **different markers**. If wide \(S_d\) kills the inductive branch in-band, the crossing may exist only at lower \(f\), or the useful marker may be a magnitude extremum / admittance feature rather than \(\mathrm{Im}\{Z\}=0\).
4. **Band truncation (now closed).** Absence of a crossing in 1.50–2.30 MHz for \(S_d\ge 2\) was answered by low-\(f\) CW: the crossing for \(S_d=2\) sits near **0.655 MHz**; \(S_d=10\) remains capacitive to **0.50 MHz**. Remaining work is free-space anchor and marker/model choice—not more of the same 100 kHz grid.

### Design-choice implications

| If we believed the problem was… | We would… |
|---------------------------------|-----------|
| Liu-style retrieval bias | Fit \(t_\mathrm{sh}\), correct \(f_{\phi0}\to f_{uh}\), publish GUM tables |
| Missing kinetic sheath physics | Replace step \(N_0\) with PIC/fluid sheath formation (Tu-like) |
| **Volumetric loading / marker choice (current best reading)** | (i) ~~low-\(f\) CW for \(S_d\ge 2\)~~ **done**; (ii) free-space baseline on same dipole; (iii) report both phase-zero and \(\lvert Z\rvert\) / admittance peaks; (iv) map \(S_d\Delta x\) to an equivalent coax \(C_\mathrm{sh}\) *a posteriori* to compare with Liu’s analytic sheath; (v) re-examine whether “Tu upward shift” is the right FDTD target for a **prescribed vacuum jacket** |

Item (iv) is the natural bridge: extract effective \(C_\mathrm{sh}(S_d)\) from the low-frequency capacitive asymptote of simulated \(Z\), compare to

\[
C_\mathrm{sh}^\mathrm{(coax)}
= \frac{2\pi\varepsilon_0 L}{\ln(1 + S_d\Delta x / r_\mathrm{eff})},
\]

and ask whether FDTD and Liu’s analytic sheath agree on **loading**, even if they disagree on which spectral marker validates the campaign.

---

## 7. Summary of design choices

1. **Balmain (1964)** → homogeneous magnetoplasma dipole \(Z\); **later Balmain / contemporaries** → ion sheath, jackets, sheath waves (series-gap lineage).
2. **Liu** → same lineage, but sheath is an **operational coax \(C_\mathrm{sh}\)** inside retrieval + **GUM**; markers split (\(f_{uh}\) vs \(f_{\phi0}\)).
3. **Tu** → kinetic, self-consistent, time-varying sheath around a HV transmitter (physics, not retrieval).
4. **This project** → 3D fluid FDTD with **prescribed volumetric vacuum gap** \(S_d\); emergent **series** capacitance; validation via feed \(Z(f)\).

Sheath coupling works. Low-f CW shows \(f_\mathrm{res}\) **falling** with \(S_d\) under the Im +→− metric. Full discrepancy discussion (reasons, series vs parallel, PIP ranking): [`analysis/tu_discrepancy_discussion.md`](../analysis/tu_discrepancy_discussion.md). Remaining issue: **validation observable** and competing limits of “less plasma dielectric” vs “more series \(C_\mathrm{sh}\)”—not a GUM retrieval problem, and no longer a missing-frequency-band problem.

---

## 8. Suggested next documentation / analysis steps

1. ~~Run / complete low-frequency CW (`scripts/run_sheath_cw_lowf.ps1`) for \(S_d=0,2,10\).~~ **Done 2026-09-04** (`analysis/cw_lowf_findings.md`; LaTeX Ch.~low-f).
2. ~~Save discrepancy discussion.~~ **Done** (`analysis/tu_discrepancy_discussion.md`; reflected in LaTeX Ch.~goals / low-f / status).
3. Add free-space CW on the same dipole for an upper anchor on \(f_\mathrm{res}\).
4. Post-process low-\(f\) \(\mathrm{Im}\{Z\}\sim -1/(\omega C_\mathrm{eff})\) to tabulate \(C_\mathrm{eff}(S_d)\) vs coax estimate.
5. Keep report wording aligned with this note and the discrepancy discussion (no “Balmain had no sheath”; Tu upward shift = campaign *target*, not guaranteed FDTD outcome for a prescribed jacket).

---

*Last updated: 2026-09-04.*
