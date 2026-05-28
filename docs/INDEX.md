# PF-FDTD Documentation Index

This page is the primary navigation hub for project documentation.

## Start Here

- [Repository README](../README.md): project overview, quick build/run, and docs map.
- [Quick Tutorial](QUICK_TUTORIAL.md): one-page dipole simulation walkthrough.
- [Input Format](INPUT_FORMAT.md): `.str` input structure, parameters, and examples.
- [Architecture](ARCHITECTURE.md): module responsibilities and data flow.

## By Audience

### New users

1. [Repository README](../README.md)
2. [Input Format](INPUT_FORMAT.md)
3. [Physics](PHYSICS.md)

### Developers

1. [Developers Guide](DEVELOPERS.md)
2. [Architecture](ARCHITECTURE.md)
3. [Contributing](CONTRIBUTING.md)

### Researchers

1. [Physics](PHYSICS.md)
2. [Input Format](INPUT_FORMAT.md)
3. [Architecture](ARCHITECTURE.md)

## Core Documents

- [ARCHITECTURE.md](ARCHITECTURE.md)
- [CONTRIBUTING.md](CONTRIBUTING.md)
- [DEVELOPERS.md](DEVELOPERS.md)
- [INPUT_FORMAT.md](INPUT_FORMAT.md)
- [PARALLELIZATION_STRATEGY.md](PARALLELIZATION_STRATEGY.md)
- [PHYSICS.md](PHYSICS.md)
- [QUICK_TUTORIAL.md](QUICK_TUTORIAL.md)
- [README_STRUCTURE.md](README_STRUCTURE.md)
- [SETUP_SUMMARY.md](SETUP_SUMMARY.md)
- [COMPLETION_REPORT.md](COMPLETION_REPORT.md)
- [Sheath validation plan](sheath/SHEATH_VALIDATION_IMPLEMENTATION_PLAN.md)
- [Sheath validation analysis](sheath/SHEATH_VALIDATION_ANALYSIS.md)

## Build, Test, And Run References

- [CMakeLists.txt](../CMakeLists.txt): cross-platform build targets.
- [tests/CMakeLists.txt](../tests/CMakeLists.txt): unit test configuration.
- [compile.bat](../compile.bat): Windows batch compile shortcut.
- [scripts/run_simulation.bat](../scripts/run_simulation.bat): scripted simulation runner.
- [docs-link-check workflow](../.github/workflows/docs-link-check.yml): validates markdown links on PRs.

## Current Repo Structure (High-Level)

```text
.
|- docs/
|- src/
|- tests/
|- visualization/
|- scripts/
|- CMakeLists.txt
|- Makefile
|- compile.bat
`- README.md
```

## Documentation Health Notes

- This index reflects repository state as of 2026-05-04.
- Historical planning documents may still contain outdated "to create" statements.
- Active cleanup and priorities are tracked in [DOCS_REMEDIATION_CHECKLIST.md](DOCS_REMEDIATION_CHECKLIST.md).
