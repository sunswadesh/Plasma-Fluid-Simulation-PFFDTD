# Paper 1 — Static sheath capacitance

**Working title.** *Series sheath loading of a plasma-immersed dipole in 3D fluid FDTD: volumetric \(S_d\) versus analytic coaxial \(C_\mathrm{sh}\).*

**Status:** Prior campaign complete (Phases 0–8). Paper-task analysis open.  
**Guide:** [`../PROJECT_GUIDE.md`](../PROJECT_GUIDE.md)

---

## Science question

Does a **prescribed volumetric vacuum jacket** of width \(S_d\Delta x\) in PF-FDTD behave as a **series sheath capacitor** whose effective \(C_\mathrm{eff}(S_d)\) matches coaxial / Song-static expectations?

This is the **quasi-static bridge**: sampling different sheath thicknesses the way Song’s static \(r_s\)–voltage branch does, without claiming oscillating-boundary or PIC fidelity.

## Why this can be a paper

- First clear 3D fluid-FDTD demonstration that imposed sheath → **series** \(C_\mathrm{sh}\), with the Im-zero **decreasing** with thickness explained rather than treated as a Tu failure.  
- Quantitative bridge to **Liu/Balmain-gap** analytic sheath used in PIP work.  
- Closes the 2026 campaign with the **right observable**.

## Observables (success metrics)

| Metric | Target |
|--------|--------|
| \(C_\mathrm{eff}(S_d)\) from low-\(f\) \(\mathrm{Im}\{Z\}\approx -1/(\omega C)\) | Decreases with \(S_d\); order-of-magnitude match to coax |
| Coax comparison | \(C_\mathrm{sh}=2\pi\varepsilon_0 L/\ln(1+S_d\Delta x/r_\mathrm{eff})\) |
| Free-space \(f_\mathrm{res}\) on same dipole | Upper anchor for unloading narrative |
| Multi-marker \(Z(f)\) | Report Im-zero **and** \|Z\| / admittance extrema; do not equate them |

**Not a success metric:** Im-zero climbing with \(S_d\).

## Prior data (do not re-run blindly)

| Asset | Path |
|-------|------|
| Low-f findings | [`../analysis/cw_lowf_findings.md`](../analysis/cw_lowf_findings.md) |
| Discrepancy note | [`../analysis/tu_discrepancy_discussion.md`](../analysis/tu_discrepancy_discussion.md) |
| Coupling fix | [`../analysis/sheath_coupling_findings.md`](../analysis/sheath_coupling_findings.md) |
| Dense CW + low-f phases | [`../validation/phase_6_cw_tu/`](../validation/phase_6_cw_tu/), [`../validation/phase_8_lowf_cw/`](../validation/phase_8_lowf_cw/) |
| LaTeX report | [`../validation/phase_7_documentation/main.pdf`](../validation/phase_7_documentation/main.pdf) |

## Work plan

1. Free-space CW on the same dipole grid (open item in `STATUS.md`).  
2. Post-process existing low-\(f\) capacitive asymptotes → table of \(C_\mathrm{eff}(S_d)\).  
3. Compare to coax estimate; document \(r_\mathrm{eff}\) / staircasing assumptions.  
4. Optional: denser tones near \(S_d=2\) (~0.55–0.75 MHz).  
5. Draft paper Methods/Results from `analysis/` + this folder; cite Song static branch as related, Tu only as motivation/context.

## Folder layout (this paper)

```text
paper1_static_sheath_capacitance/
├── README.md          ← you are here
├── PLAN.md            ← detailed checklist (edit as work proceeds)
├── analysis/          ← paper-specific tables/figures (C_eff, etc.)
└── draft/             ← outlines, notes toward manuscript
```

## Depends on / feeds

- **Depends on:** Phases 4–8 (coupling + CW).  
- **Feeds:** Paper 2 (trusted static \(C(r_s)\) baseline before moving \(r_s\)).
