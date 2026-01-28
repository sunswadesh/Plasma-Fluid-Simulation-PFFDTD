# Plasma Fluid - Finite Difference Time Domain (PF-FDTD) Model

[![GitHub](https://img.shields.io/badge/GitHub-sunswadesh%2FPlasma--Fluid--Simulation--PFFDTD-blue)](https://github.com/sunswadesh/Plasma-Fluid-Simulation-PFFDTD)
![License](https://img.shields.io/badge/License-Academic-green)
![C++](https://img.shields.io/badge/C%2B%2B-11-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)

## Overview

PF-FDTD is a scientific simulation framework for modeling electromagnetic wave propagation in hot magnetized plasma using the Finite Difference Time Domain (FDTD) method. This code implements multi-fluid plasma physics models with support for electron and ion species dynamics.

**Based on:** Jeffrey D. Ward's Master Thesis (2006)  
**Currently Maintained By:** Swadesh Patra, Edmund Spencer  
**Current Version:** 1.8.2+

## Key Features

- **Multi-Fluid Plasma Model**: Supports electrons and multiple ion species with independent dynamics
- **Magnetized Plasma**: Full 3D magnetized plasma with cyclotron frequency effects
- **FDTD Framework**: Explicit time-domain electromagnetic simulation
- **Collision Physics**: Electron-neutral and ion collision modeling
- **Absorbing Boundary Conditions**: Retarded-time ABC for wave absorption
- **Flexible Source Specification**: Multiple source types (sine, pulse, Gaussian, DC, sinc)
- **Detailed Output**: Field data, particle velocity, and density tracking

## Documentation

- **[README_STRUCTURE.md](docs/README_STRUCTURE.md)** - Project structure and organization guide
- **[DEVELOPERS.md](docs/DEVELOPERS.md)** - Development guidelines and setup instructions
- **[CONTRIBUTING.md](docs/CONTRIBUTING.md)** - Contribution guidelines
- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - Code architecture and physics implementation
- **[PHYSICS.md](docs/PHYSICS.md)** - Physics equations and model descriptions
- **[INPUT_FORMAT.md](docs/INPUT_FORMAT.md)** - Detailed input file format specification
- **[CHANGELOG.md](CHANGELOG.md)** - Version history and updates

## Quick Start

### Compilation

```bash
cd src
g++ -O3 -std=c++11 pffdtd.cpp -o pffdtd
```

### Basic Usage

```bash
./pffdtd input_file output_prefix [plasma_freq] [collision_freq] [gyro_freq] [elevation_angle] [azimuth_angle] [temperature]
```

### Example: Free Space Simulation

```bash
./pffdtd tests/dipole.str results/dipole
```

### Example: Plasma Simulation

```bash
./pffdtd tests/dipole.str results/dipole 5.3e6 0.27 18.7 22.0 0.0 0.0
```

## Build Instructions

### Prerequisites

- GCC/G++ 4.8+ or Clang 3.3+
- Make (recommended)
- Python 3.8+ (for visualization and analysis)

### Compilation Methods

**Method 1: Direct compilation**
```bash
cd src
g++ -O3 -std=c++11 -march=native pffdtd.cpp -o pffdtd
```

**Method 2: Using Make (future)**
```bash
make
make install
```

**Method 3: With parallel support (future)**
```bash
make PARALLEL=1  # OpenMP parallelization
make MPI=1       # MPI distributed computing
```

## Project Structure

```
pffdtd/
├── src/                          # Core simulation code
│   ├── pffdtd.cpp               # Main FDTD solver
│   ├── pffdtdN.cpp              # Variant implementations
│   ├── plasma.h                 # Multi-fluid plasma equations
│   ├── plasmaN*.h               # Plasma model variants
│   ├── output.h                 # Output routines
│   ├── source.h                 # Source implementations
│   ├── Retard.h                 # Absorbing boundary conditions
│   ├── memallocate.h            # Memory management
│   └── constants.h              # Physical constants (future)
├── include/                      # Header files (future)
├── lib/                          # Library code (future)
├── tests/                        # Test cases and benchmarks
│   ├── dipole/
│   ├── plasma/
│   └── performance/
├── tools/                        # Utilities and helpers
├── visualization/                # Python visualization tools
│   ├── FieldViz.py              # Main visualization
│   ├── plot_fields.py           # Field plotting
│   └── analysis_tools.py         # Analysis utilities
├── docs/                         # Documentation
├── examples/                     # Example simulations
└── scripts/                      # Build and utility scripts
```

## Physics Models

### Electromagnetic
- 3D Maxwell's equations in the FDTD formulation
- Yee grid with staggered field components

### Plasma
- Two-fluid (electron and ion) model with collisions
- Multiple ion species support
- Magnetized plasma with cyclotron frequency effects
- Temperature-dependent effects

### Boundary Conditions
- Retarded-time absorbing boundary conditions for EM waves
- Boundary conditions for plasma quantities

## Roadmap

### Short Term (v1.9)
- [ ] Code refactoring and modularization
- [ ] Comprehensive unit tests
- [ ] Python/C++ bindings for easy scripting
- [ ] Improved visualization tools

### Medium Term (v2.0)
- [ ] OpenMP parallelization
- [ ] MPI distributed memory support
- [ ] GPU acceleration (CUDA/OpenCL)
- [ ] Advanced physics modules

### Long Term
- [ ] 2D and 1D solvers
- [ ] AMR (Adaptive Mesh Refinement)
- [ ] Collision operator improvements
- [ ] Dust particle effects

## Output Formats

### `.vc` File (Voltage/Current Output)
```
Time    Source1(V)    Source1(I)    Source2(V)    Source2(I)    ...
0       <values>
1       <values>
...
```

### `.fd` File (Field Data Output)
```
Time    Field1        Field2        ...           FieldN
0       <values>
1       <values>
...
```

## Performance

Typical performance on modern hardware:
- **Small grids** (32³): ~10,000 iterations/sec
- **Medium grids** (128³): ~500 iterations/sec  
- **Large grids** (256³): ~60 iterations/sec

Performance varies with:
- CPU architecture
- Optimization level (-O3 recommended)
- Plasma presence (plasma calculations ~2-3x overhead)
- Number of species and sources

## Known Issues & Limitations

1. **Stability Constraints**: Direct relationship between stability, maximum iterations, density, and grid size
2. **Boundary Conditions**: Current ABC implementation could be improved
3. **Memory Usage**: 3D grids can consume significant memory; consider domain decomposition for large simulations
4. **Sequential Computation**: Current code is single-threaded; no parallelization yet

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

## Citing This Work

If you use PF-FDTD in your research, please cite:

```bibtex
@mastersthesis{Ward2006,
  author = {Ward, Jeffrey D.},
  title = {Plasma Frequency Probe Design and Implementation},
  school = {[University Information]},
  year = {2006}
}

@software{PFFDTD2024,
  author = {Patra, Swadesh and Spencer, Edmund},
  title = {Plasma Fluid - Finite Difference Time Domain Model},
  url = {https://github.com/sunswadesh/Plasma-Fluid-Simulation-PFFDTD},
  year = {2024}
}
```

## Support

- **Documentation**: See `docs/` folder
- **Issues**: Report bugs on GitHub Issues
- **Discussions**: Use GitHub Discussions for questions

## License

[Specify your license here - Academic/Educational use?]

## Acknowledgments

- Original code development: Jeffrey D. Ward
- Code improvements and extensions: Swadesh Patra, Edmund Spencer
- Physics consultation: [If applicable]

---

**Last Updated:** January 2026  
**Maintainers:** Swadesh Patra, Edmund Spencer
