# Plasma-Fluid-Simulation-PFFDTD

Plasma Fluid - Finite Difference Time Domain (PF-FDTD) is a 3D electromagnetic simulation code that couples FDTD field updates with plasma fluid equations.

The project originates from Jeff Ward's work at Utah State University and has been modernized with a modular source layout, OpenMP-enabled build variants, tests, and visualization tooling.

## What This Repo Does

- Solves time-domain Maxwell equations on a Yee-style grid.
- Optionally couples fields to a multi-species plasma fluid model.
- Supports multiple excitation source types (sine, pulse, Gaussian, sinc, DC).
- Applies absorbing boundary conditions and antenna/material regions from input files.
- Writes voltage/current and field outputs for post-processing.

## Current Repository Layout

```text
.
|- src/                 Core C++ solver and physics modules
|  |- pffdtd.cpp        Main simulation loop and orchestration
|  |- fields/           E/B update kernels
|  |- physics/          Plasma model and coupling
|  |- source/           Source injection and probe calculations
|  |- boundary/         Absorbing and geometry boundary conditions
|  |- io/               Input parsing and output writers
|  `- utils/            Constants, types, memory allocation helpers
|- tests/               CMake unit tests and benchmark/regression scripts
|- visualization/       Python plotting and analysis scripts
|- scripts/             Windows helper scripts for build/run/verification
|- docs/                Architecture, physics, input format, contributor docs
|- CMakeLists.txt       Cross-platform build entry
`- compile.bat          Quick Windows build helper
```

## Build

### Option 1: Windows quick build (MinGW)

```bat
compile.bat
```

### Option 2: CMake (recommended)

```powershell
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --target pffdtd_parallel
```

Available CMake targets include:

- `pffdtd_debug`
- `pffdtd_release`
- `pffdtd_profile`
- `pffdtd_parallel` (when OpenMP is found)

## Run A Simulation

### Direct executable usage

```powershell
# Serial/parallel executable name depends on your build target
.\pffdtd_parallel.exe dipole out
```

This reads `dipole.str` and writes `out.vc` and `out.fd`.

### Scripted run (Windows)

```bat
scripts\run_simulation.bat run_test 5.3 0.1 1.43
```

This creates output under `results\run_test\` and can invoke plotting scripts.

## Output Files

- `.vc`: time series of source voltage/current.
- `.fd`: field (and optional plasma-derived) output samples.

Plotting and analysis tools are in `visualization/`.

## Testing

- CMake test configuration: `tests/CMakeLists.txt`
- Unit tests: `tests/unit/`
- Regression and benchmarks: `tests/regression/`, `tests/benchmarks/`

## Branch Model

Current remote branches observed in this repository:

- `main` (primary branch)
- `develop` (historical integration branch)
- `PffdtdSheath` (sheath-focused experimental work)
- `tu2008-1d-rf-sheath-implementation` (historical branch)

Contribution default: branch from `main` unless maintainers request otherwise.

## Troubleshooting

### Compiler not found

Symptoms:

- `g++` is not recognized by shell
- `compile.bat` reports compiler missing

Fix:

- Install MinGW-w64 (Windows) or GCC/Clang (Linux/macOS).
- Ensure compiler binary path is in `PATH`.
- Re-run `compile.bat` or CMake configure/build commands.

### OpenMP target not available

Symptoms:

- `pffdtd_parallel` target is missing after CMake configure.

Fix:

- Use a compiler/toolchain with OpenMP support.
- Reconfigure CMake from a clean build directory.
- Build `pffdtd_release` if OpenMP is unavailable.

### Input file format errors

Symptoms:

- Program exits with input format/read errors.

Fix:

- Validate `.str` file structure against `docs/INPUT_FORMAT.md`.
- Start from known-good inputs such as `dipole.str`.
- Keep tab/space formatting consistent with expected parser format.

### Python plotting dependencies missing

Symptoms:

- Visualization scripts fail with import errors.

Fix:

- Create/activate a Python environment.
- Install dependencies listed in `visualization/requirements.txt`.
- Re-run plotting scripts from repository root.

## Documentation Map

- Project docs index: `docs/INDEX.md`
- Quick dipole walkthrough: `docs/QUICK_TUTORIAL.md`
- Input format and examples: `docs/INPUT_FORMAT.md`
- Physics model and equations: `docs/PHYSICS.md`
- Software architecture: `docs/ARCHITECTURE.md`
- Developer onboarding: `docs/DEVELOPERS.md`
- Contribution process: `docs/CONTRIBUTING.md`

## Status Notes

- Core simulation workflow is functional and buildable.
- Some documentation files include forward-looking plans; see `docs/DOCS_REMEDIATION_CHECKLIST.md` for active cleanup priorities.
