# Project Structure and Organization Guide

## Overview

This document describes the recommended folder organization for the PF-FDTD project to support collaborative development, version control, testing, and future expansion.

## Proposed Folder Structure

```
Plasma-Fluid-Simulation-PFFDTD/
│
├── README.md                          # Project overview (main entry point)
├── CHANGELOG.md                       # Version history
├── LICENSE                            # License file
├── .gitignore                         # Git ignore patterns
├── .github/                           # GitHub configuration
│   ├── workflows/                     # CI/CD workflows
│   │   ├── build.yml                  # Build testing
│   │   ├── tests.yml                  # Automated tests
│   │   └── valgrind.yml               # Memory testing
│   └── ISSUE_TEMPLATE/                # Issue templates
│
├── docs/                              # Documentation (THIS IS KEY)
│   ├── README_STRUCTURE.md            # This file
│   ├── DEVELOPERS.md                  # Development guidelines
│   ├── CONTRIBUTING.md                # Contribution guide
│   ├── ARCHITECTURE.md                # Code architecture
│   ├── PHYSICS.md                     # Physics equations
│   ├── INPUT_FORMAT.md                # Input file specifications
│   ├── PERFORMANCE.md                 # Performance tuning guide
│   ├── BUILDING.md                    # Build instructions
│   ├── TROUBLESHOOTING.md             # Common issues
│   └── figs/                          # Documentation figures/diagrams
│       ├── yee_grid.png
│       ├── data_flow.png
│       └── architecture.png
│
├── src/                               # Main source code
│   ├── pffdtd.cpp                     # Main FDTD solver
│   ├── pffdtd.h                       # Main header (future)
│   ├── constants.h                    # Physical constants
│   ├── types.h                        # Data type definitions (future)
│   │
│   ├── physics/                       # Physics modules (future organization)
│   │   ├── plasma.h                   # Base plasma model
│   │   ├── plasmaMultiSpecies.h       # Multi-species plasma
│   │   ├── magnetized.h               # Magnetized plasma effects
│   │   └── collisions.h               # Collision operators
│   │
│   ├── solvers/                       # Solver methods
│   │   ├── fdtd_solver.h              # FDTD algorithms
│   │   ├── boundary_conditions.h      # BC implementations
│   │   └── absorbing_bc.h             # Retarded time ABC
│   │
│   ├── fields/                        # Field definitions
│   │   ├── field.h                    # Field base classes
│   │   └── yee_grid.h                 # Yee grid implementation
│   │
│   ├── io/                            # Input/Output
│   │   ├── output.h                   # Output routines
│   │   ├── source.h                   # Source implementations
│   │   └── input_parser.h             # Input file parsing (future)
│   │
│   ├── utils/                         # Utility functions
│   │   ├── memallocate.h              # Memory management
│   │   ├── timing.h                   # Performance timing
│   │   └── error_handling.h           # Error management (future)
│   │
│   └── legacy/                        # Older versions (keep for reference)
│       ├── pffdtdN.cpp
│       ├── pffdtdN1.cpp
│       ├── plasmaN*.h
│       └── outputN.h
│
├── include/                           # Public headers (future)
│   └── pffdtd/
│       ├── pffdtd.h
│       └── version.h
│
├── lib/                               # Library code (future)
│   ├── libpffdtd.a                    # Static library
│   └── libpffdtd.so                   # Shared library
│
├── tests/                             # Test suite
│   ├── CMakeLists.txt                 # Test build configuration
│   ├── run_tests.sh                   # Test runner script
│   │
│   ├── unit/                          # Unit tests
│   │   ├── test_plasma.cpp            # Plasma equation tests
│   │   ├── test_fdtd.cpp              # FDTD algorithm tests
│   │   ├── test_boundaries.cpp        # BC tests
│   │   └── test_io.cpp                # I/O tests
│   │
│   ├── validation/                    # Physics validation tests
│   │   ├── test_free_space.cpp        # Free space wave test
│   │   ├── test_plasma_dispersion.cpp # Dispersion relation
│   │   ├── test_cold_plasma.cpp       # Cold plasma limits
│   │   └── test_langmuir.cpp          # Langmuir probe
│   │
│   ├── performance/                   # Performance benchmarks
│   │   ├── benchmark_grid.cpp         # Grid size scaling
│   │   ├── benchmark_species.cpp      # Species count scaling
│   │   └── benchmark_parallel.cpp     # Parallel efficiency
│   │
│   ├── regression/                    # Regression tests (against reference)
│   │   ├── dipole_reference.fd        # Reference data
│   │   └── test_dipole_regression.cpp
│   │
│   └── data/                          # Test input files
│       ├── dipole.str                 # Dipole antenna
│       ├── plasma.str                 # Plasma test case
│       ├── langmuir.str               # Langmuir probe
│       ├── free_space.str             # Free space propagation
│       └── magnetized.str             # Magnetized plasma
│
├── tools/                             # Utility scripts and tools
│   ├── build.sh                       # Build script
│   ├── clean.sh                       # Clean build
│   ├── profile.sh                     # Profiling script
│   ├── memory_check.sh                # Memory leak detection
│   │
│   ├── python/                        # Python utilities
│   │   ├── requirements.txt           # Python dependencies
│   │   ├── setup.py                   # Python package setup
│   │   └── pffdtd_utils.py            # Shared utilities
│   │
│   └── cmake/                         # CMake helpers (future)
│       ├── FindPFMPI.cmake
│       └── FindPFCUDA.cmake
│
├── visualization/                     # Visualization and analysis
│   ├── README.md                      # Visualization guide
│   ├── requirements.txt               # Python dependencies
│   │
│   ├── field_visualization/           # Field plotting
│   │   ├── FieldViz.py                # Main visualization
│   │   ├── plot_fields.py             # Field plots
│   │   ├── animate_fields.py          # Animations (future)
│   │   └── colormap_utils.py          # Colormap tools
│   │
│   ├── analysis/                      # Data analysis
│   │   ├── analysis_tools.py          # Analysis utilities
│   │   ├── compute_energy.py          # Energy computation
│   │   ├── compute_spectrum.py        # Spectral analysis
│   │   ├── langmuir_analysis.py       # Langmuir probe analysis
│   │   └── dispersion_analysis.py     # Dispersion relation
│   │
│   ├── comparison/                    # Multi-run comparison
│   │   ├── compare_runs.py            # Compare simulations
│   │   └── parameter_sweep.py         # Parameter studies
│   │
│   └── jupyter_notebooks/             # Interactive analysis
│       ├── dipole_analysis.ipynb
│       ├── plasma_validation.ipynb
│       └── performance_analysis.ipynb
│
├── examples/                          # Example simulations
│   ├── README.md                      # Examples guide
│   │
│   ├── basic/                         # Basic examples
│   │   ├── free_space_dipole/         # Dipole in free space
│   │   │   ├── input.str
│   │   │   ├── run.sh
│   │   │   └── README.md
│   │   │
│   │   └── cold_plasma/               # Cold plasma
│   │       ├── input.str
│   │       ├── run.sh
│   │       └── README.md
│   │
│   ├── intermediate/                  # Intermediate examples
│   │   ├── langmuir_probe/            # Langmuir probe simulation
│   │   ├── magnetized_plasma/         # With magnetic field
│   │   └── multi_species_ions/        # Multiple ion species
│   │
│   └── advanced/                      # Advanced examples
│       ├── parameter_sweep/           # Parameter variation
│       ├── output_analysis/           # Detailed output processing
│       └── coupled_physics/           # Multiple physics models
│
├── external/                          # External libraries (future)
│   ├── hdf5/                          # HDF5 for large outputs
│   ├── netcdf/                        # NetCDF format support
│   └── README.md                      # External lib guide
│
├── scripts/                           # Build and deployment scripts
│   ├── Makefile                       # Make build system
│   ├── CMakeLists.txt                 # CMake configuration
│   ├── build_release.sh               # Release build
│   ├── build_debug.sh                 # Debug build
│   ├── build_parallel.sh              # Parallel build (OpenMP/MPI)
│   ├── build_gpu.sh                   # GPU build (CUDA)
│   ├── install.sh                     # Installation script
│   ├── configure.sh                   # Configuration script
│   └── docker/                        # Docker support (future)
│       ├── Dockerfile
│       └── docker-compose.yml
│
├── config/                            # Configuration files
│   ├── compiler_flags.txt             # Compiler optimization flags
│   ├── physics_defaults.cfg           # Default physics parameters
│   └── system_requirements.txt        # Minimum system specs
│
└── results/                           # Simulation results (ignored by git)
    ├── .gitignore                     # Ignore all results
    ├── runs/                          # Output directory
    └── analysis/                      # Analysis output

```

## Directory Organization Rationale

### src/ - Source Code Organization

**Current → Future Migration:**

**Currently** (flat structure):
```
src/
├── pffdtd.cpp
├── plasma.h
├── output.h
├── source.h
└── Retard.h
```

**Proposed** (hierarchical, future refactoring):
```
src/
├── physics/          # Physics-specific modules
├── solvers/          # Solution algorithms
├── fields/           # Field representations
├── io/              # Input/Output
└── utils/           # Utilities
```

**Benefits:**
- Better separation of concerns
- Easier to find related code
- Supports plugin architecture
- Enables selective compilation

### docs/ - Documentation

All project documentation lives in `docs/`:
- **DEVELOPERS.md** - How to contribute
- **ARCHITECTURE.md** - Code structure
- **PHYSICS.md** - Equations and models
- **INPUT_FORMAT.md** - Input specifications
- **PERFORMANCE.md** - Optimization tips
- **BUILDING.md** - Build instructions
- **TROUBLESHOOTING.md** - Common issues

### tests/ - Testing

Organized by purpose:
- **unit/** - Test individual functions
- **validation/** - Test against analytical solutions
- **performance/** - Benchmark code
- **regression/** - Compare against reference

### visualization/ - Analysis Tools

Python-based analysis and visualization:
- **field_visualization/** - Field plots and animations
- **analysis/** - Scientific analysis (energy, spectrum, etc.)
- **jupyter_notebooks/** - Interactive analysis

### examples/ - Working Examples

Progressive complexity:
- **basic/** - Simple cases for learning
- **intermediate/** - Real simulation scenarios
- **advanced/** - Complex setups and custom usage

## Version Control Strategy

### Branch Organization

```
main/develop
├── feature/parallel-processing      → PR → merge to develop
├── feature/gpu-acceleration         → PR → merge to develop
├── feature/visualization-tools      → PR → merge to develop
├── fix/boundary-condition-bug       → PR → merge to develop
├── docs/api-documentation          → PR → merge to develop
├── release/v2.0                     → merge to main after testing
└── experimental/new-physics-model   → can be long-lived
```

### Release Workflow

```
main (production releases)
  ↓ (tag: v2.0)
  
develop (development mainline)
  ↑ (merge from feature branches via PR)
  
feature/* (temporary feature branches)
```

## CI/CD Pipeline (.github/workflows/)

### Automated Checks
```
On every push/PR:
1. Build with multiple compilers (GCC, Clang)
2. Run unit tests
3. Run validation tests
4. Check for memory leaks (valgrind)
5. Generate coverage reports
6. Build documentation
```

### Example GitHub Actions
```yaml
# .github/workflows/build.yml
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        compiler: [gcc, clang]
    steps:
      - uses: actions/checkout@v2
      - name: Compile
        run: make
      - name: Run tests
        run: make test
```

## File Naming Conventions

### Source Files
- C++ source: `*.cpp`
- C++ headers: `*.h` (or future `.hpp`)
- Legacy code: `.cpp~` or in `src/legacy/`

### Input Files
- PFFDTD input: `*.str` (structure)
- Configuration: `*.cfg`
- Parameters: `*.ini`

### Output Files
- Field data: `*.fd` (field data)
- Voltage/Current: `*.vc` (voltage/current)
- Analysis: `*.dat`, `*.csv`, `*.hdf5`

### Documentation
- Markdown: `*.md`
- Figures: `*.png`, `*.svg` (in `docs/figs/`)
- References: `*.bib`, `*.pdf`

### Test Files
- Test data: `tests/data/*.str`
- Reference: `tests/data/*.fd`, `tests/data/*.vc`
- Test code: `tests/**/*.cpp`

## Scalability Considerations

### For Small Changes
Structure supports direct edits to existing files.

### For Adding Features
1. Create feature branch
2. Add code to appropriate subdirectory
3. Add tests in `tests/`
4. Add documentation in `docs/`
5. Create PR with all changes

### For Major Refactoring
1. Create long-lived branch
2. Work incrementally
3. Maintain backward compatibility
4. Add migration guide in `docs/`

### For Adding Physics Module
1. Add to `src/physics/`
2. Add unit tests
3. Add validation tests
4. Add example in `examples/`
5. Document physics in `docs/PHYSICS.md`

## Transition Plan

### Phase 1: Current Structure (v1.8-1.9)
- Keep existing flat structure in `src/`
- Add `docs/`, `tests/`, `visualization/`, `examples/`
- Establish version control workflow

### Phase 2: Organization (v1.9-2.0)
- Start refactoring code into subdirectories
- Maintain backward compatibility
- Move legacy variants to `src/legacy/`

### Phase 3: Modularization (v2.0+)
- Full hierarchical organization
- Plugin architecture for physics
- Library support

## Getting Started with New Structure

### For Contributors

1. **Clone and explore:**
   ```bash
   git clone https://github.com/sunswadesh/Plasma-Fluid-Simulation-PFFDTD.git
   cd Plasma-Fluid-Simulation-PFFDTD
   ```

2. **Read docs:**
   ```
   Start: docs/README_STRUCTURE.md (this file)
   Then: docs/DEVELOPERS.md
   Then: docs/ARCHITECTURE.md
   ```

3. **Build and test:**
   ```bash
   cd src
   g++ -O3 pffdtd.cpp -o pffdtd
   cd ../tests
   bash run_tests.sh
   ```

4. **Contribute:**
   ```bash
   git checkout -b feature/my-feature
   # Make changes
   # Add tests
   # Update docs
   git push origin feature/my-feature
   # Create PR on GitHub
   ```

---

**Last Updated:** January 2026
**Version:** 1.0
