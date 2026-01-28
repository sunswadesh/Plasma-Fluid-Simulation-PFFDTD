# CHANGELOG

All notable changes to the Plasma Fluid - Finite Difference Time Domain (PF-FDTD) project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Versioning Scheme

- **MAJOR.MINOR.PATCH** (e.g., 1.8.2)
- MAJOR: Significant physics or architecture changes
- MINOR: New features, physics enhancements, backward compatible
- PATCH: Bug fixes, minor improvements

## [Unreleased]

### Planned for v2.0

- [ ] OpenMP parallelization for field calculations
- [ ] MPI distributed memory support
- [ ] GPU acceleration (CUDA kernels)
- [ ] Complete refactoring into modular architecture
- [ ] Python/C++ bindings for scripting
- [ ] Advanced collision operators
- [ ] Adaptive mesh refinement (AMR)
- [ ] 2D and 1D solver variants

### Planned for v1.9

- [ ] Comprehensive test suite
- [ ] Input file validation
- [ ] Better error messages
- [ ] Python visualization tools
- [ ] Jupyter notebook examples
- [ ] CMake build system
- [ ] GitHub Actions CI/CD

## [1.8.2] - 2005-02-14

### Fixed
- Sinc source function implementation
- Issues with source output frequency (now every iteration)
- Improved stability for long simulation runs

### Changed
- Source output timing adjusted for ion analysis
- Increased iteration limit for extended simulations

### Notes
- Last version maintained by original author
- Base version for future development

## [1.8.1] - 2005-01-26

### Changed
- Collision frequency now expressed as ratio of plasma frequency
- Improved parameter documentation

### Fixed
- Plasma charge setting for antenna boundary conditions
- Delta parameter affecting electron charging

## [1.8.0] - 2005-01-15

### Added
- Multi-species ion support (NS parameter configurable)
- Ability to simulate multiple ion species with different masses/charges
- Species-specific collision and density tracking

### Changed
- Extended plasma model from 2 species (electron + ion) to N species
- Modified array structure to support arbitrary number of species

### Physics
- Implements 2-fluid model with multiple ion species
- Each species has independent mass, charge, collision frequency

## [1.7.4] - 2005-01-10

### Changed
- Source output now recorded every iteration (instead of periodic)
- Enables accurate ion analysis over longer timescales
- Increased memory usage for source output

## [1.7.3] - 2004-12-19

### Improved
- Program exit procedures
- Resource cleanup on termination
- Error handling and reporting

## [1.7.2] - 2004-12-15

### Removed
- Higher-order plasma terms (N_1*U_1)
- Attempted improvement of numerical stability
- Simplified plasma equations while maintaining physical correctness

### Notes
- Decision to remove terms was made for stability rather than physics accuracy

## [1.7.1] - 2004-12-10

### Added
- DC sweep capability for Langmuir probe testing
- Temperature effects support (DC sweep)
- Validation of ion temperature diagnostics

## [1.7.0] - 2004-11-20

### Added
- Two-fluid (electron and ion) model
- Separate momentum conservation for each species
- Multi-species dynamics

### Physics
- Full two-fluid equations implementation
- Electron-ion coupling through electromagnetic fields
- Species-specific collision frequencies

## [1.6.0] - 2004-10-05

### Fixed
- Errors in current calculation
- Corrections to plasma current density computation

### Changed
- Improved numerical scheme for current evolution

## [1.5.0] - 2004-09-15

### Fixed
- Errors found in plasma equation implementation
- Corrected finite difference stencils
- Fixed boundary condition application

## [1.4.1] - 2003-12-19

### Improved
- Program exit procedures
- Error handling enhancements

## [1.4] - 2003-12-15

### Added
- Support for external parameter files
- Command-line argument parsing
- Laboratory-type experiment configuration

### Changed
- Flexible parameter input via files
- Supports various experimental setups

## [1.3] - 2003-09-20

### Optimized
- Reduced visual output for faster processing
- Optimized memory access patterns

### Performance
- Significant speedup for large simulations

## [1.2.1] - 2003-08-10

### Changed
- Current term absorbed into Maxwell's equations
- Improves both speed and memory efficiency
- Removed two-fluid model (reverted to cold plasma)

### Physics
- Conductivity applied directly to E-field equations
- Simpler but faster implementation

## [1.2.0] - 2003-07-15

### Changed
- Cold plasma model (electron-only)
- Current term incorporated into field equations
- Improved computational efficiency

### Performance
- ~2-3x speedup compared to v1.1
- Reduced memory requirements

## [1.1] - 2003-06-01

### Added
- Two-fluid model support
- Electron and ion species tracking
- Separate velocity and density for each species

### Physics
- Multi-species dynamics
- Collision frequency per species

## [1.0] - 2003-05-15

### Initial Release
- Working FDTD implementation for free space
- Basic plasma model with electrons
- Absorbing boundary conditions (Retarded Time ABC)
- Simple source implementations
- Output to `.vc` and `.fd` files

### Features
- 3D Yee grid FDTD solver
- Single-fluid plasma model
- Multiple source types (sine, pulse, Gaussian)
- Field output at specified locations
- Voltage/current output for antenna analysis

### Physics
- Maxwell's equations in FDTD form
- Cold plasma conductivity
- Linear collision damping
- CFL stability constraints

---

## Version Naming Conventions

- **v1.x**: Original thesis work and near-term improvements
- **v2.x**: Major refactoring with parallelization and new physics
- **v3.x+**: Future extensions with advanced features

## How to Report Issues

- Use GitHub Issues for bug reports
- Include version number (from `#define pffdtdver`)
- Provide test case input file
- Include compilation flags and compiler version
- Attach error messages and output

## How to Contribute

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines on:
- Reporting bugs
- Suggesting enhancements
- Submitting code
- Documentation updates

## Current Maintenance Status

- **v1.8.2**: Stable, no longer actively developed
- **v1.9-dev**: Active development branch for enhancements
- **v2.0-dev**: Major refactoring in progress

## Timeline

```
2003-05: v1.0 - Initial FDTD implementation
2003-12: v1.4 - File-based parameters added
2004-11: v1.7 - Two-fluid model added
2005-02: v1.8.2 - Current stable version
2024+: v1.9-2.0 - Active development
```

---

**Last Updated:** January 2026  
**Maintainers:** Swadesh Patra, Edmund Spencer
