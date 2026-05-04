# Project Structure Guide

This document describes the repository structure as it exists now, plus optional future organization ideas.

Last reviewed: 2026-05-04

## Current Structure (Authoritative)

```text
Plasma-Fluid-Simulation-PFFDTD/
|- README.md
|- CHANGELOG.md
|- LICENSE
|- .gitignore
|- CMakeLists.txt
|- Makefile
|- compile.bat
|- compile_manual.bat
|- scripts/
|- docs/
|- src/
|- tests/
|- visualization/
`- archive/
```

### Source Tree

```text
src/
|- pffdtd.cpp
|- boundary/
|- fields/
|- io/
|- physics/
|- source/
`- utils/
```

### Test Tree

```text
tests/
|- CMakeLists.txt
|- unit/
|- regression/
|- benchmarks/
`- data/
```

### Scripts and Tooling

- `scripts/` contains helper scripts for build/run/verification workflows.
- `visualization/` contains Python utilities for plotting and analysis.
- `archive/` contains legacy and historical material.

## Why This Structure Works

- Separates simulation core (`src/`) from verification (`tests/`) and analysis (`visualization/`).
- Keeps reproducibility helpers in `scripts/`.
- Is compatible with both CMake and script-driven workflows.

## Planned Evolution (Non-Authoritative Roadmap)

These are optional improvements, not current guarantees:

1. Add an `examples/` directory with small reproducible scenarios.
2. Add docs CI checks (link validation and markdown linting).
3. Further split `physics/` into model-specific modules if code grows.
4. Introduce standardized result folders and metadata manifests for benchmarks.

## Branch and Release Notes

- `main` is currently the primary branch.
- Additional remote branches exist for historical and experimental work.
- Keep structure changes incremental and accompanied by docs updates.

## Structure Update Policy

When the repository layout changes:

1. Update this file.
2. Update `docs/INDEX.md` if navigation paths changed.
3. Update `README.md` if user entrypoints changed.
4. Record notable changes in `CHANGELOG.md`.

## Related Docs

- `docs/INDEX.md`
- `docs/DEVELOPERS.md`
- `docs/ARCHITECTURE.md`
- `docs/DOCS_REMEDIATION_CHECKLIST.md`
