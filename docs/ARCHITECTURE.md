# PF-FDTD Architecture and Design

## Overview

This document describes the overall architecture, design patterns, and relationships between components in the PF-FDTD codebase.

## System Architecture

### High-Level Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         PFFDTD.CPP                              │
│                    (Main Program Loop)                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────┐   ┌──────────────────┐                    │
│  │ Parse Arguments  │─→ │ Open Input File  │                    │
│  └──────────────────┘   └──────────────────┘                    │
│           │                      │                               │
│           └──────────┬───────────┘                               │
│                      ↓                                            │
│           ┌──────────────────────┐                               │
│           │  Read Grid Parameters│                               │
│           │ Read Source Parameters│                              │
│           │ Read Antenna Structure│                              │
│           └──────────────────────┘                               │
│                      ↓                                            │
│           ┌──────────────────────┐                               │
│           │  Allocate Memory     │                               │
│           │  (Field Arrays)      │                               │
│           │  (Plasma Arrays)     │                               │
│           └──────────────────────┘                               │
│                      ↓                                            │
│        ┌─────────────────────────────┐                           │
│        │ Time-Stepping Loop (t=0..N)│                           │
│        │                             │                           │
│        │ ┌─────────────────────────┐ │                           │
│        │ │ Update Sources (source.h)│ │                           │
│        │ └─────────────────────────┘ │                           │
│        │          ↓                   │                           │
│        │ ┌─────────────────────────┐ │                           │
│        │ │ Calculate E-field       │ │                           │
│        │ │ (Ecalc)                 │ │                           │
│        │ └─────────────────────────┘ │                           │
│        │          ↓                   │                           │
│        │ ┌─────────────────────────┐ │                           │
│        │ │ Apply Plasma Equations  │ │                           │
│        │ │ (plasma.h routines)     │ │                           │
│        │ └─────────────────────────┘ │                           │
│        │          ↓                   │                           │
│        │ ┌─────────────────────────┐ │                           │
│        │ │ Calculate B-field       │ │                           │
│        │ │ (Bcalc)                 │ │                           │
│        │ └─────────────────────────┘ │                           │
│        │          ↓                   │                           │
│        │ ┌─────────────────────────┐ │                           │
│        │ │ Apply Boundary          │ │                           │
│        │ │ Conditions (Retard.h)   │ │                           │
│        │ └─────────────────────────┘ │                           │
│        │          ↓                   │                           │
│        │ ┌─────────────────────────┐ │                           │
│        │ │ Output Fields (output.h)│ │                           │
│        │ └─────────────────────────┘ │                           │
│        └─────────────────────────────┘                           │
│                      ↓                                            │
│           ┌──────────────────────┐                               │
│           │  Free Memory         │                               │
│           │  Close Output Files  │                               │
│           └──────────────────────┘                               │
│                      ↓                                            │
│           ┌──────────────────────┐                               │
│           │    Exit Program      │                               │
│           └──────────────────────┘                               │
└─────────────────────────────────────────────────────────────────┘
```

## Component Modules

### 1. pffdtd.cpp - Main Solver

**Responsibilities:**
- Program initialization and argument parsing
- Memory allocation/deallocation
- Main time-stepping loop orchestration
- I/O file management
- Error handling and exit codes

**Key Functions:**
```cpp
int main(int argc, char *argv[])           // Program entry point
void Ecalc()                                // Calculate E-field from previous time step
void Bcalc()                                // Calculate B-field from current E-field
void ClearArrays()                          // Initialize field arrays to zero
void statfile(char filepre[81])             // Write header and metadata to output files
```

**Exit Codes:**
```
0 - Successful completion
1 - File I/O error
2 - Memory allocation failure
3 - Input file format error
4 - Aborted subroutine error
```

### 2. plasma.h - Plasma Physics Model

**Responsibilities:**
- Electron-ion dynamics
- Collision frequency calculations
- Conductivity computation
- Plasma equation time-stepping

**Key Physics:**
- Multi-fluid (electron + ions) model
- Collision operator (linear damping)
- Temperature effects (optional)
- Magnetic field coupling

**Key Functions:**
```cpp
int PLASMAallocate(int allocate)            // Allocate 5D arrays for plasma variables
void PLASMAclear()                          // Initialize plasma parameters
void UBCcalc()                              // Calculate velocity boundary conditions
void NBCcalc()                              // Calculate density boundary conditions
```

**Array Conventions:**

```cpp
// Field quantities stored in 5D arrays:
// [x][y][z][time_history][species]

double *****UX;  // x-velocity
double *****UY;  // y-velocity
double *****UZ;  // z-velocity
double *****N;   // Density

// Storage indices:
// time_history: 0 (current) or 1 (previous) or 2 (t-2)
// species: 0 (electrons), 1+ (various ions)

// Memory layout example:
UX[i][j][k][0][0] = electron_x_velocity_current_time
UX[i][j][k][0][1] = oxygen_ion_x_velocity_current_time
UX[i][j][k][1][0] = electron_x_velocity_previous_time
```

### 3. output.h - Data Output

**Responsibilities:**
- Writing field data (`.fd` files)
- Writing voltage/current data (`.vc` files)
- Formatting output for post-processing
- Data compression/decimation

**Output File Formats:**

#### `.vc` File (Voltage/Current)
```
Time    V1      I1      V2      I2      ...
0       <float> <float> <float> <float> ...
1       ...
```

#### `.fd` File (Field Data)
```
Metadata lines:
<field_type_and_axis>  (e.g., "1X" = Ex, "2Z" = Bz, "3Y" = Uy)
<x_location>
<y_location>
<z_location>

Data:
Time    Value1  Value2  ...
0       <float> <float> ...
1       ...
```

### 4. source.h - Source Implementations

**Responsibilities:**
- Time-dependent source calculation
- Multiple source type support
- Source placement and field assignment

**Supported Source Types:**
```
1 - Sinusoidal: V(t) = sin(2π*freq*t)
2 - Pulse: Sine envelope pulse
3 - Raised Cosine: Smooth pulse
4 - Gaussian: Gaussian envelope
5 - Gaussian Derivative: dG/dt
6 - DC: Constant value
7 - Sinc: sinc(t) = sin(πt)/(πt)
```

### 5. Retard.h - Absorbing Boundary Conditions

**Responsibilities:**
- Wave absorption at domain boundaries
- Reduction of reflections
- Implementation of retarded-time ABC (RTABC)

**Physics:**
- Based on Mur's boundary condition
- Implemented on electric field
- Reduces reflections by ~95% (tunable)

**Application:**
```cpp
// Applied to E-field at boundaries
// Effectively reads-in wavefront without reflection
```

### 6. memallocate.h - Memory Management

**Responsibilities:**
- Dynamic array allocation
- Memory deallocation
- Memory leak prevention

**Key Functions:**
```cpp
double *darray1(long nl, long nh)           // 1D double array
double **darray2(long nrl, long nrh, 
                 long ncl, long nch)        // 2D array
double ****darray4(...)                     // 4D array
double *****darray5(...)                    // 5D array

void free_darray1(double *v, long nl)
void free_darray2(double **m, ...)
void free_darray4(double ****t, ...)
void free_darray5(double *****p, ...)
```

**From Numerical Recipes** - Provides Fortran-style 1-indexed arrays

## Data Flow

### Spatial Grid Structure (Yee Grid)

```
Standard FDTD Yee staggered grid arrangement:

      E-field (edges)              B-field (faces)
      
      y ∧
        │   
        │   ┌─────Ey─────┐
        │   │      By    │
        │   Ez           Ex
        │   │      Bx    │
        │   └────────────┘
        ├─────────────────→ x
        │
        ├─ z (out of page)

Grid spacing: dx, dy, dz (meters)
Time step: dt (seconds)
```

**CFL Stability Condition:**
```
dt ≤ 1 / (c * sqrt(1/dx² + 1/dy² + 1/dz²))
```

### Time Stepping

```
t=0:   Initialize fields to zero
t=1:   E¹ = f(B⁰)
       U¹, N¹ = plasma equations
       B¹ = g(E¹)
       Apply BC
       Output if needed
       
t=2:   E² = f(B¹)
       U², N² = plasma equations
       B² = g(E²)
       ...
       
t=N:   Final time step
```

## Code Organization Patterns

### Memory Management Pattern

```cpp
// Allocate
double ****field = darray4(1, sx, 1, sy, 1, sz, 0, 1);

// Use
for (i=1; i<sx; i++) {
    for (j=1; j<sy; j++) {
        for (k=1; k<sz; k++) {
            field[i][j][k][0] = /* calculation */;
        }
    }
}

// Free
free_darray4(field, 1, sx, 1, sy, 1, sz, 0, 1);
```

### Field Update Pattern

```cpp
// Calculation performed on interior points only
// Boundary points handled separately (BC functions)
#pragma omp parallel for collapse(3)
for (i=2; i<sx-1; i++) {
    for (j=2; j<sy-1; j++) {
        for (k=2; k<sz-1; k++) {
            // Finite difference stencil
            E_new[i][j][k] = coeffs[0]*E_old[i][j][k] +
                             coeffs[1]*(B[i+1][j][k] - B[i][j][k])/dx +
                             ...;
        }
    }
}
```

### Plasma Physics Pattern

```cpp
// Update velocity (momentum conservation)
// U^{n+1} = (U^n - (e/m)*E^n*dt - ν*U^n*dt) / (1 + ν*dt)

// Update density (continuity equation)
// n^{n+1} = n^n - ∇·(n*U)

// Each species tracked separately
for (int sp=0; sp<NS; sp++) {
    for (i=2; i<sx-1; i++) {
        for (j=2; j<sy-1; j++) {
            for (k=2; k<sz-1; k++) {
                // Update momentum
                U[sp] = ...;
                
                // Update density
                N[sp] = ...;
            }
        }
    }
}
```

## Performance Characteristics

### Computational Complexity

| Operation | Cost | % of Total |
|-----------|------|-----------|
| E-field calc | O(N) | ~40% |
| B-field calc | O(N) | ~35% |
| Plasma equations | O(N·NS) | ~20% |
| Boundaries | O(N²/3) | ~3% |
| I/O | O(N_out) | ~2% |

Where N = sx·sy·sz·iterations, NS = number of species

### Memory Usage

```
Field arrays:     3 × 4D (Ex, Ey, Ez) × 2 timesteps
                = 6 × sx×sy×sz × 8 bytes
                
Plasma arrays:    3 × 5D (Ux, Uy, Uz) × 3 timesteps × NS
                + 1 × 5D (N) × 3 timesteps × NS
                + auxiliary
                ≈ 4 × sx×sy×sz × 3 × NS × 8 bytes
                
Auxiliary:        Various utility arrays
                ≈ 2 × sx×sy×sz × 8 bytes

Total ≈ 40 MiB for 64³ grid with 2 species
        320 MiB for 128³ grid with 2 species
        2.5 GiB for 256³ grid with 2 species
```

## Dependencies and Coupling

### External Dependencies
```
Standard C Libraries:
├── math.h         - Mathematical functions
├── stdio.h        - File I/O
├── stdlib.h       - Memory allocation
├── string.h       - String operations
├── time.h         - Timing
└── signal.h       - Signal handling
```

### Internal Module Dependencies
```
pffdtd.cpp
├── memallocate.h  (allocate/free functions)
├── source.h       (source calculations)
├── output.h       (output routines)
├── plasma.h       (plasma equations)
└── Retard.h       (boundary conditions)

plasma.h
└── memallocate.h  (allocate/free arrays)

output.h
└── (standalone)

source.h
└── (standalone)

Retard.h
└── (mostly standalone, reads E-field)
```

## Version Variants

### Current Variants

| File | Purpose | Physics |
|------|---------|---------|
| pffdtd.cpp | Standard single-fluid model | Electrons only |
| pffdtdN.cpp | Early multi-fluid attempt | Basic multi-species |
| pffdtdN1.cpp | Variant with sheath physics | Sheath-specific |
| plasma.h | Base multi-fluid model | 2-3 species |
| plasmaN0.h | Current multi-species | N arbitrary species |
| plasmaN1.h | With heating terms | Temperature evolution |
| plasmaN2.h | Advanced collisions | Velocity-dependent ν |
| plasmaN3.h | Magnetic effects | Full magnetization |
| plasmaN4.h | Complex geometries | Sheath/tube models |

### Selection Mechanism

Currently selected at compile-time via `#include` directives.

**Future:** Runtime selection via input file or command-line flags.

## Proposed Architecture Improvements

### For v2.0

1. **Modularization**
   - Separate physics modules from solver
   - Plugin architecture for different models
   - Cleaner interfaces between components

2. **Abstraction Layers**
   - Grid interface (support 1D, 2D, 3D)
   - Physics interface (hot-swap models)
   - Output interface (multiple formats)

3. **Parallelization**
   - OpenMP shared-memory directives
   - MPI domain decomposition
   - GPU kernels via CUDA/HIP

4. **Testing Infrastructure**
   - Unit test framework
   - Physics validation suite
   - Performance benchmarks

5. **Better Memory Management**
   - Modern C++ (smart pointers)
   - Reduced fragmentation
   - Better cache locality

## Design Patterns Used

### 1. Procedural Arrays
All calculations operate on global arrays rather than objects. This is typical for scientific computing due to performance requirements.

### 2. Time Stepping Pattern
Explicit time-stepping with leapfrog-like structure for field calculations.

### 3. Stencil Pattern
Finite-difference calculations use local stencils (±1 neighbor indices).

### 4. Separator Pattern
Plasma equations and field equations cleanly separated via header includes.

## Physics Validation Strategy

### Level 1: Analytical Solutions
```
Test against known solutions:
- Plane wave in free space
- Plasma dispersion relation
- Cold plasma limits
```

### Level 2: Numerical Benchmarks
```
Compare with:
- Published FDTD results
- Other simulation codes
- Experimental data
```

### Level 3: Stability Analysis
```
Verify:
- CFL condition satisfaction
- Dispersion relation accuracy
- Long-time stability
```

---

**Last Updated:** January 2026
**Document Version:** 1.0
