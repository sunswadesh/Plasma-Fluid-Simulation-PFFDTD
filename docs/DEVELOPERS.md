# PFFDTD Developer Guide

Welcome to the PF-FDTD development team! This guide provides essential information for contributing to and developing new features for the PFFDTD codebase.

## Table of Contents

1. [Development Setup](#development-setup)
2. [Code Structure](#code-structure)
3. [Development Workflow](#development-workflow)
4. [Coding Standards](#coding-standards)
5. [Testing](#testing)
6. [Performance Considerations](#performance-considerations)
7. [Adding New Physics](#adding-new-physics)
8. [Parallel Programming](#parallel-programming)

## Development Setup

### Prerequisites

- **C++ Compiler**: GCC 4.8+ or Clang 3.3+ (C++11 or later)
- **Build Tools**: Make, CMake (recommended for future versions)
- **Version Control**: Git
- **Python 3.8+**: For visualization and testing scripts
- **IDE**: VS Code, CLion, or your preference

### Environment Setup (Linux/macOS)

```bash
# Clone the repository
git clone https://github.com/sunswadesh/Plasma-Fluid-Simulation-PFFDTD.git
cd Plasma-Fluid-Simulation-PFFDTD

# Create development branch
git checkout -b feature/your-feature-name

# Set up Python environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements-dev.txt

# Compile the code
cd src
g++ -O0 -g -std=c++11 pffdtd.cpp -o pffdtd
```

### Environment Setup (Windows)

```powershell
# Clone repository
git clone https://github.com/sunswadesh/Plasma-Fluid-Simulation-PFFDTD.git
cd Plasma-Fluid-Simulation-PFFDTD

# Create development branch
git checkout -b feature/your-feature-name

# Set up Python environment
python -m venv venv
venv\Scripts\activate
pip install -r requirements-dev.txt

# Compile using MinGW or MSVC
cd src
g++ -O0 -g -std=c++11 pffdtd.cpp -o pffdtd.exe
```

## Code Structure

### Directory Organization

```
src/
├── pffdtd.cpp              # Main FDTD solver and program entry
├── plasma.h                # Base plasma model (electrons only)
├── plasmaN0.h              # Multi-species plasma model
├── plasmaN1.h              # Variant with sheath physics
├── plasmaN2.h              # Variant with heating
├── plasmaN3.h              # Variant with advanced collisions
├── plasmaN4.h              # Variant with magnetic effects
├── plasmaNSheath.h         # Sheath-specific physics
├── output.h                # Field and source data output
├── outputN.h               # Output variants
├── source.h                # Source implementations
├── Retard.h                # Absorbing boundary conditions
├── TubeBC.h                # Tube geometry BC
└── memallocate.h           # Memory allocation (Numerical Recipes)

tests/
├── dipole/                 # Dipole antenna test case
├── plasma/                 # Plasma physics verification
└── benchmark/              # Performance benchmarks

visualization/
├── FieldViz.py            # Main visualization tool
├── plot_fields.py         # Field plotting utilities
├── analysis_tools.py      # Data analysis
└── requirements.txt       # Python dependencies
```

### Module Responsibilities

| Module | Purpose |
|--------|---------|
| `pffdtd.cpp` | Main loop, parameter parsing, memory management, I/O coordination |
| `plasma.h` | Plasma electron-ion equations, conductivity, collision frequency |
| `plasmaN*.h` | Specialized plasma models for different physics regimes |
| `output.h` | Writing `.vc` (voltage/current) and `.fd` (field data) files |
| `source.h` | Source time-stepping (sine, pulse, Gaussian, etc.) |
| `Retard.h` | Wave absorption at domain boundaries |
| `memallocate.h` | Dynamic memory allocation/deallocation |

## Development Workflow

### 1. Issue-Driven Development

Before starting work:

```bash
# Check existing issues on GitHub
# Create or assign yourself to an issue
# Reference issue in commits: "fixes #123"
```

### 2. Feature Branch Workflow

```bash
# Create feature branch from main/develop
git checkout develop
git pull origin develop
git checkout -b feature/physics-enhancement

# Work on feature
# Commit frequently with meaningful messages
git add .
git commit -m "feat: add temperature-dependent collision frequency

- Implements temperature scaling from Ward 2006 Appendix C
- Fixes issue #42
- Tests pass in validation suite"

# Push and create Pull Request
git push origin feature/physics-enhancement
```

### 3. Pull Request Process

1. **Create PR** with:
   - Clear title: `[COMPONENT] Brief description`
   - Description linking to related issues
   - Test results demonstrating new feature

2. **Code Review**:
   - At least 1 review from core maintainers
   - All tests must pass
   - Documentation must be updated

3. **Merge**:
   - Squash commits if needed
   - Delete feature branch
   - Update CHANGELOG.md

### 4. Commit Message Convention

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code restructuring (no functional change)
- `perf`: Performance improvement
- `test`: Test addition/modification
- `docs`: Documentation changes
- `chore`: Build, dependencies, tooling

**Example:**
```
feat(plasma): add multi-temperature ion support

- Extends plasmaN0.h to track per-species temperatures
- Implements temperature-dependent collision cross-sections
- Adds 3 new input parameters to input file format
- All 12 test cases pass

Fixes #45
```

## Coding Standards

### C++ Style Guide

#### Naming Conventions

```cpp
// Variables: camelCase or snake_case (be consistent)
double plasmaFrequency;
double collision_freq;
int sx, sy, sz;  // Grid dimensions

// Constants: UPPER_CASE
#define PI 3.14159265359
#define MU_0 1.25663706143591729538505735331180115367886775e-6

// Functions: camelCase
void calculateElectricField();
void update_plasma_equations();

// Classes/Structs: PascalCase (if used in future)
class PlasmaModel { };
struct GridParameters { };

// Arrays: descriptive names
double ****EX, ****EY, ****EZ;  // Electric field
double *****UX, *****UY, *****UZ; // Velocity
```

#### File Organization

```cpp
// 1. Header guards (if needed)
#ifndef PLASMA_H
#define PLASMA_H

// 2. Includes
#include "math.h"
#include "stdio.h"

// 3. Defines and constants
#define PI 3.14159265359
#define ME 9.1066e-31

// 4. Global variables (minimize these)
double FREQ_PLASMA = 5.3e6;

// 5. Function declarations
void function1();
void function2();

// 6. Function implementations
void function1() { }
void function2() { }

#endif
```

#### Memory Management

```cpp
// Always allocate with corresponding deallocation
double ***field = darray3(1, sx, 1, sy, 1, sz);
// ... use field ...
free_darray3(field, 1, sx, 1, sy, 1, sz);

// Check allocation success
if (field == NULL) {
    printf("Error: Memory allocation failed\n");
    return 2;  // MEM_ERROR
}
```

#### Comments and Documentation

```cpp
/**
 * Brief description of function
 * 
 * Longer description if needed, explaining what the function does
 * and why it exists.
 * 
 * @param param1 Description of param1
 * @param param2 Description of param2
 * @return Description of return value
 * 
 * Physics reference: Ward (2006), Eq. 3.24
 */
void exampleFunction(int param1, double param2) {
    // Regular comment for implementation details
    
    // Calculate field from Maxwell's equation
    EX[i][j][k][t] = (1/eps_0) * /* curl B */;
}
```

### Code Quality Metrics

Target metrics:
- **Cyclomatic Complexity**: < 10 per function (measure with tools)
- **Lines per Function**: < 100 (shorter is better)
- **Comment Ratio**: 20-30% of code
- **Test Coverage**: > 80% (aim for critical paths)

## Testing

### Test Structure

```
tests/
├── CMakeLists.txt           # Test build configuration
├── test_plasma.cpp          # Plasma equation tests
├── test_boundaries.cpp      # Boundary condition tests
├── test_sources.cpp         # Source implementation tests
├── test_output.cpp          # Output format tests
└── data/                    # Reference data
    ├── expected_dipole.fd   # Reference field output
    └── expected_dipole.vc   # Reference voltage/current output
```

### Running Tests

```bash
# Manual test - dipole antenna
cd src
./pffdtd ../tests/data/dipole.str ../tests/output/dipole

# Compare output (assuming reference data exists)
cd ../tests
python3 validate.py ../tests/output/dipole

# Performance benchmark
./pffdtd ../tests/data/dipole.str ../tests/output/dipole --benchmark
```

### Writing New Tests

```cpp
// tests/test_new_physics.cpp
#include <cassert>
#include "../src/plasma.h"

void test_collision_frequency() {
    // Setup
    double freq_plasma = 5.3e6;
    double freq_collision = 0.27;
    double temp = 0.0;
    
    // Execute
    double result = calculate_collision_freq(freq_plasma, freq_collision, temp);
    
    // Verify
    double expected = freq_plasma * freq_collision;
    assert(abs(result - expected) < 1e-10);
    
    printf("✓ test_collision_frequency passed\n");
}

int main() {
    test_collision_frequency();
    // ... more tests ...
    return 0;
}
```

## Performance Considerations

### Optimization Guidelines

1. **Compilation Optimization**
   ```bash
   # Development (fast compile, good debugging)
   g++ -O0 -g -std=c++11 pffdtd.cpp -o pffdtd
   
   # Production (best performance)
   g++ -O3 -march=native -std=c++11 pffdtd.cpp -o pffdtd
   ```

2. **Profiling and Bottleneck Analysis**
   ```bash
   # Compile with profiling
   g++ -O2 -g -pg -std=c++11 pffdtd.cpp -o pffdtd
   
   # Run with profiling
   ./pffdtd input.str output
   
   # Analyze results
   gprof pffdtd gmon.out
   ```

3. **Memory Efficiency**
   - Monitor array allocations: 5D arrays are memory-intensive
   - Consider single vs. double precision depending on accuracy needs
   - Implement memory pooling for repeated allocations

4. **Algorithm Hotspots**
   - Field calculations (Ecalc, Bcalc) → ~60% of runtime
   - Plasma equations → ~30% of runtime
   - I/O → ~5% of runtime
   - Other → ~5% of runtime

## Adding New Physics

### Process for Adding New Physics Module

1. **Design Phase**
   - Write physics documentation in `docs/PHYSICS.md`
   - Include relevant equations and references
   - Discuss with team before coding

2. **Implementation Phase**
   ```cpp
   // Create new header: src/plasmaNX.h
   // Include:
   // - Detailed physics comments
   // - New parameters
   // - New functions
   // - References to papers
   ```

3. **Integration Phase**
   ```cpp
   // In pffdtd.cpp, add:
   - New command-line parameters
   - New input file sections
   - Selection mechanism for physics models
   - Documentation in help text
   ```

4. **Validation Phase**
   - Create test case in `tests/`
   - Compare with analytical solutions or reference data
   - Document validation results

### Example: Adding Temperature-Dependent Physics

```cpp
// docs/PHYSICS.md - Document first
/**
 * Temperature-Dependent Collision Frequency
 * 
 * Classical plasma physics predicts collision frequency scaling:
 *   ν(T) = ν(0) * sqrt(T/T_ref)
 * 
 * Reference: Fridman & Kennedy, Plasma Discharges and Electronics (2004), Ch. 2
 */

// src/plasmaNX.h - Implement
double get_collision_freq_temperature_dependent(double T) {
    // ν(T) = ν(0) * sqrt(T/T_ref)
    double T_ref = 300.0;  // Reference temperature (K)
    return FREQ_COL * sqrt(T / T_ref);
}

// tests/test_temperature_physics.cpp - Test
void test_collision_frequency_temperature() {
    double freq_300K = get_collision_freq_temperature_dependent(300.0);
    double freq_1200K = get_collision_freq_temperature_dependent(1200.0);
    
    // Should scale as sqrt(4) = 2
    assert(abs(freq_1200K / freq_300K - 2.0) < 0.01);
}
```

## Parallel Programming

### Roadmap for Parallelization

#### Phase 1: OpenMP (Shared Memory)
```cpp
// Parallelize field calculation loops
#pragma omp parallel for collapse(3)
for (int i=1; i<sx-1; i++) {
    for (int j=1; j<sy-1; j++) {
        for (int k=1; k<sz-1; k++) {
            EX[i][j][k][t+1] = ... // Independent calculation
        }
    }
}
```

#### Phase 2: MPI (Distributed Memory)
- Domain decomposition in 3D
- Ghost cell communication
- Distributed I/O

#### Phase 3: GPU Acceleration (CUDA)
- Kernel implementation for field calculations
- Efficient memory transfers
- Multi-GPU support

### Guidelines for Parallel Code

1. **Identify Parallelizable Regions**
   - Outer loops over spatial grid
   - Independent calculations per cell
   - Reduction operations

2. **Minimize Communication**
   - Overlap computation with communication
   - Reduce data transfer frequency
   - Use efficient MPI datatypes

3. **Load Balancing**
   - Profile before optimizing
   - Use domain decomposition for even loading
   - Monitor weak and strong scaling

## Resources

- **Physics References**:
  - Ward (2006) - Original dissertation (included)
  - Fridman & Kennedy (2004) - Plasma Discharges
  - Taflove & Hagness (2005) - FDTD Methods

- **C++ Resources**:
  - C++ Reference: https://en.cppreference.com/
  - Effective Modern C++: Scott Meyers
  - Code: The Hidden Language: Charles Petzold

- **Scientific Computing**:
  - Numerical Recipes: https://numerical.recipes/
  - PETSc Documentation: https://www.mcs.anl.gov/petsc/
  - HPC Best Practices: https://ideas-productivity.org/

## Getting Help

- **GitHub Issues**: Report bugs and ask questions
- **GitHub Discussions**: General questions and ideas
- **Documentation**: Start with `docs/` folder
- **Code Comments**: Well-documented code is available reference

---

**Last Updated:** January 2026  
**Maintained By:** Swadesh Patra, Edmund Spencer
