# Tu (2008) Sheath Validation

Validate PF-FDTD dipole sheath impedance against Tu et al. (2008, JGR).

**Git repo root:** `D:\Swadesh\Work\Impedance Probe\PiP Alireza\2026 Collab_PFFDTD_Sheath` (branch `PffdtdSheath`)  
**This folder:** campaign project (`projects/tu2008-sheath/`)

## Status

See [STATUS.md](STATUS.md).

## Layout

```text
tu2008-sheath/
├── docs/              Plans, DOCUMENTATION_INDEX.md
├── analysis/          Findings, figures, summaries
├── inputs/            sheath*.str
├── scripts/           Campaign run/analyze drivers
├── data/references/   PDF papers
├── validation/        Phases 0–7 (LaTeX report in phase_7)
└── archive/           Legacy snapshots
```

Solver source: `../../src/` (repo root). Build `pffdtd_parallel.exe` at repo root before running campaign scripts.

## Quick links

| Document | Path |
|----------|------|
| Index | [docs/DOCUMENTATION_INDEX.md](docs/DOCUMENTATION_INDEX.md) |
| Coupling fix | [analysis/sheath_coupling_findings.md](analysis/sheath_coupling_findings.md) |
| Report PDF | [validation/phase_7_documentation/main.pdf](validation/phase_7_documentation/main.pdf) |
