# Plasma-Fluid-Simulation-PFFDTD — Tu (2008) Sheath Collaboration

Full PF-FDTD solver workspace for the Tu (2008) sheath impedance validation campaign (PiP / Alireza collab).

**Git branch:** `PffdtdSheath`  
**Primary campaign folder:** [projects/tu2008-sheath/](projects/tu2008-sheath/) ([CHRONICLE.md](projects/tu2008-sheath/CHRONICLE.md), Papers 0–3)  
**Legacy upstream (optional, not used for results):** `D:\Swadesh\Work\Models\Pffdtd`

## Quick links

| Topic | Location |
|-------|----------|
| Build & run PFFDtd | [docs/DEVELOPERS.md](docs/DEVELOPERS.md) |
| Physics & input format | [docs/PHYSICS.md](docs/PHYSICS.md), [docs/INPUT_FORMAT.md](docs/INPUT_FORMAT.md) |
| **Tu 2008 sheath campaign** | [projects/tu2008-sheath/](projects/tu2008-sheath/) |
| Campaign status | [projects/tu2008-sheath/STATUS.md](projects/tu2008-sheath/STATUS.md) |
| Low-f findings (Sep 2026) | [projects/tu2008-sheath/analysis/cw_lowf_findings.md](projects/tu2008-sheath/analysis/cw_lowf_findings.md) |
| Progress report PDF | [projects/tu2008-sheath/validation/phase_7_documentation/main.pdf](projects/tu2008-sheath/validation/phase_7_documentation/main.pdf) |

## Repository layout (STORMS-style)

```text
├── src/                 C++ PFFDtd solver
├── tests/               Unit tests, regression, benchmarks
├── scripts/             Generic build/run helpers
├── docs/                Solver documentation
├── visualization/       Post-processing tools
└── projects/
    └── tu2008-sheath/   Campaign docs, inputs, scripts, validation phases
```

## Build (from repo root)

```powershell
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --target pffdtd_parallel
```

Or `compile.bat` on Windows.

## Working here

- **Solver changes:** edit `src/`, commit from this repo root.
- **Campaign work:** open `projects/tu2008-sheath/`; run scripts under `projects/tu2008-sheath/scripts/`.
- **Results:** `results/sheath_*` at **this repo root** (gitignored). Do not set `$env:PFFDtd_ROOT`.
- **Low-f CW sweep:** `.\projects\tu2008-sheath\scripts\run_sheath_cw_lowf.ps1`

No `$env:PFFDtd_ROOT` — campaign scripts always use this repo root for results and working directory.
