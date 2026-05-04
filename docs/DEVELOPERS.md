# PFFDTD Developer Guide

This guide describes how to build, run, test, and contribute to the current PF-FDTD codebase.

Last reviewed: 2026-05-04

## Development Setup

### Prerequisites

- C++ compiler with C++11 support
  - GCC/Clang on Linux/macOS
  - MinGW-w64 or MSVC-compatible toolchain on Windows
- CMake 3.10+
- Git
- Python 3.8+ (for visualization and some test utilities)

### Clone

```bash
git clone https://github.com/sunswadesh/Plasma-Fluid-Simulation-PFFDTD.git
cd Plasma-Fluid-Simulation-PFFDTD
```

### Build (Recommended: CMake)

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --target pffdtd_release
```

Useful targets from `CMakeLists.txt`:

- `pffdtd_debug`
- `pffdtd_release`
- `pffdtd_profile`
- `pffdtd_parallel` (if OpenMP is detected)

### Build (Windows Batch Shortcut)

```bat
compile.bat
```

## Code Structure (Current)

```text
src/
|- pffdtd.cpp                 Main program loop and orchestration
|- boundary/                  Absorbing and geometry boundary conditions
|- fields/                    E and B update kernels
|- io/                        Input parsing and output writers
|- physics/                   Plasma model and field coupling
|- source/                    Source waveforms and source-side metrics
`- utils/                     Constants, memory and shared definitions

tests/
|- CMakeLists.txt             Unit test build configuration
|- unit/                      Unit tests
|- regression/                Regression scripts
|- benchmarks/                Benchmark scripts
`- data/                      Input/reference test data

visualization/
`- Python plotting/analysis scripts
```

## Daily Workflow

1. Branch from `main`.
2. Make focused changes with matching docs/tests updates.
3. Run relevant build and tests.
4. Open PR with summary, risk notes, and validation evidence.

Example:

```bash
git checkout main
git pull origin main
git checkout -b feature/your-change
# edit / build / test
git add .
git commit -m "feat(scope): concise description"
git push origin feature/your-change
```

## Running Simulations

### Direct executable

```bash
./pffdtd_parallel dipole out
```

Reads `dipole.str`, writes `out.vc` and `out.fd`.

### Scripted run on Windows

```bat
scripts\run_simulation.bat run_test 5.3 0.1 1.43
```

## Testing

### CMake tests

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug
cmake --build build --target unit_tests
ctest --test-dir build --output-on-failure
```

### Script-based checks

- Regression helpers: `tests/regression/`
- Benchmark helpers: `tests/benchmarks/`

## Coding Standards

- Keep changes localized to relevant modules.
- Preserve existing naming/style in touched files.
- Add comments only where behavior is non-obvious.
- Avoid broad refactors in bug-fix PRs.
- Update docs when behavior or workflows change.

## Performance Notes

Typical hotspots:

- Field update loops (`fields/`)
- Plasma update and coupling (`physics/`)
- I/O in long runs (`io/`)

General guidance:

- Use Release builds for performance measurements.
- Use OpenMP build target when available.
- Benchmark before and after changes.

## Branch Model (Current)

Observed active remotes:

- `main` (primary branch)
- `develop` (historical integration branch)
- `PffdtdSheath` (sheath-focused experimental work)
- `tu2008-1d-rf-sheath-implementation` (historical branch aligned with main at time of audit)

Recommended contribution base: `main` unless maintainers specify otherwise.

## Documentation Responsibilities

When changing behavior, update at least:

- `README.md` for user-facing build/run changes
- `docs/INPUT_FORMAT.md` for input format changes
- `docs/PHYSICS.md` for physics model/equation changes
- `docs/ARCHITECTURE.md` for module/data-flow changes
- `CHANGELOG.md` for notable changes

For active docs cleanup priorities, see `docs/DOCS_REMEDIATION_CHECKLIST.md`.
