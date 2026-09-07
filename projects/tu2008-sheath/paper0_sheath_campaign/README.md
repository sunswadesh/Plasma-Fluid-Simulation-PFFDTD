# Paper 0 — Sheath campaign chronicle

**Working title.** *Volumetric sheath coupling in PF-FDTD: from a seed bug to series-capacitance loading.*

**Status:** Campaign complete (Phases 0–8). Folder holds the distilled discovery record.  
**Guide:** [`../PROJECT_GUIDE.md`](../PROJECT_GUIDE.md)  
**Program chronology:** [`../CHRONICLE.md`](../CHRONICLE.md)

---

## Science question

How did a prescribed volumetric sheath \(S_d\) in PF-FDTD go from “no effect on feed \(Z\)” to “strong series-\(C\) loading with downward Im-zero shift,” and what does that imply for validating against Song/Tu?

This paper (or companion methods note) owns the **path**: coupling bug, wrong Tu upward-\(f_\mathrm{res}\) scoreboard, low-f closure, and the series-\(C\) reinterpretation. **Paper 1** owns the clean \(C_\mathrm{eff}(S_d)\) vs analytic result.

## Why this can be a paper / SI

- End-to-end validation story for a new sheath feature in a 3D fluid FDTD code.  
- Documents a false negative (mask seed order) that others will hit.  
- Separates **method discovery** from **Paper 1 physics claim**.

## Contents (moved from root `analysis/`)

| Asset | Path |
|-------|------|
| Coupling fix write-up | [`analysis/sheath_coupling_findings.md`](analysis/sheath_coupling_findings.md) |
| Low-f CW findings | [`analysis/cw_lowf_findings.md`](analysis/cw_lowf_findings.md) |
| Tu discrepancy / series-\(C\) reading | [`analysis/tu_discrepancy_discussion.md`](analysis/tu_discrepancy_discussion.md) |
| Figures | [`analysis/figures/`](analysis/figures/) |
| Numeric tables | [`analysis/data/`](analysis/data/) |

Raw phase runbooks remain under [`../validation/`](../validation/) (Phases 0–8). LaTeX report: [`../validation/phase_7_documentation/main.pdf`](../validation/phase_7_documentation/main.pdf).

## Linear arc (hindsight)

```text
Feb baseline → pulse/CW Sd sweeps (null) → N0 dump shows edge hole
  → PEC-seeded ApplySheath fix → Z depends on Sd
  → dense CW: Sd≥2 capacitive in 1.5–2.3 MHz
  → low-f CW: fres falls with Sd (1.85 → 0.66 → ≲0.5 MHz)
  → Song/Tu ≠ upward fres; series C_sh is the right reading
  → Paper 1: quantify C_eff vs coax
```

## Folder layout

```text
paper0_sheath_campaign/
├── README.md
├── PLAN.md
├── analysis/          ← campaign findings, data, figures
└── draft/             ← outline toward methods paper / SI
```

## Feeds

- **Paper 1** — prior data + discrepancy framing  
- **Papers 2–3** — evidence that prescribed sheath works and what static \(S_d\) cannot do
