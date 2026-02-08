# Strategic Roadmap: PF-FDTD Codebase Evolution

**Version:** 1.0  
**Last Updated:** January 28, 2026  
**Status:** Phase 4 - Visualization (Completed) / Phase 3 - Testing (Partial)  
**Target Timeline:** 6-10 weeks to v2.0

---

## Table of Contents

1. [Immediate Next Steps (This Week)](#immediate-next-steps-this-week)
2. [Phase 1: Foundation (Weeks 1-2)](#phase-1-foundation-weeks-1-2)
3. [Phase 2: Modular Structure (Weeks 2-4)](#phase-2-modular-structure-weeks-2-4)
4. [Phase 3: Testing & Examples (Weeks 3-5)](#phase-3-testing--examples-weeks-3-5)
5. [Phase 4: Python Visualization (Weeks 4-6)](#phase-4-python-visualization-weeks-4-6)
6. [Phase 5: Parallelization (Weeks 6-8)](#phase-5-parallelization-weeks-6-8)
7. [Phase 6: GPU Support (Weeks 8-10)](#phase-6-gpu-support-weeks-8-10)
8. [Parallel Development Strategy](#parallel-development-strategy-v20)
9. [Code Organization Best Practices](#code-organization-best-practices)
10. [Implementation Timeline](#implementation-timeline)
11. [Success Metrics](#success-metrics)
12. [Risk Mitigation](#risk-mitigation)

---

## Immediate Next Steps (This Week)

### 1. Set Up GitHub Repository ✅ COMPLETE
- [x] Initialize local git repository
- [x] Configure user identity
- [x] Stage and commit documentation framework
- [x] Create main and develop branches
- [x] Configure GitHub remote
- [x] Push to GitHub
- [x] Repository live: https://github.com/sunswadesh/Plasma-Fluid-Simulation-PFFDTD

**Status:** Ready for Phase 1 Foundation work

### 2. Test the Build System (1 day)
- [ ] Run Makefile with all targets (debug, release, profile, parallel, gpu)
- [ ] Verify compilation on Windows (PowerShell)
- [ ] Test with example input files (dipole.str)
- [ ] Verify output files (.vc, .fd) generation
- [ ] Document any platform-specific issues

**Acceptance Criteria:**
- Executable compiles without warnings
- Test case runs to completion
- Output files generated correctly

### 3. Create Test Infrastructure (1-2 days)
- [ ] Create `tests/` directory structure
- [ ] Set up test data files (dipole, plasma, edge cases)
- [ ] Create test runner script
- [ ] Document how to run tests
- [ ] Create CI/CD stub (GitHub Actions workflow)

**Deliverable:** `tests/README.md` with testing guidelines

---

## Phase 1: Foundation (Weeks 1-2)

**Goal:** Establish solid foundation for future development with organized structure and documented legacy code

### Tasks

#### 1.1 Organize Source Code Structure
```
src/
  ├── CMakeLists.txt (new)
  ├── pffdtd.cpp (main solver)
  ├── legacy/
  │   ├── pffdtdN.cpp
  │   ├── pffdtdN1.cpp
  │   └── README.md
  ├── physics/
  │   ├── plasma.h
  │   ├── plasmaN0.h (variants)
  │   ├── plasmaN1.h
  │   ├── plasmaN2.h
  │   ├── plasmaN3.h
  │   ├── plasmaN4.h
  │   ├── plasmaNSheath.h
  │   └── README.md
  ├── fields/
  │   └── (will be created in Phase 2)
  └── utils/
      ├── memallocate.h
      ├── constants.h (new)
      └── types.h (new)
```

#### 1.2 Create Constants and Types Headers
- **constants.h**: Numerical constants, physical constants, default values
- **types.h**: Type definitions, struct definitions, array type aliases

**Example contents:**
```cpp
// constants.h
#ifndef CONSTANTS_H
#define CONSTANTS_H

// Physical Constants (SI units)
const double PI = 3.14159265358979323846;
const double C = 299792458.0;  // Speed of light (m/s)
const double MU0 = 4.0 * PI * 1e-7;  // Permeability (H/m)
const double EPS0 = 8.85418781762e-12;  // Permittivity (F/m)

// Stability Thresholds
const double CFL_MAX = 0.5;  // Courant-Friedrichs-Lewy limit
const double STABILITY_MARGIN = 1.1;  // Safety factor

#endif
```

#### 1.3 Update Include Paths
- Replace relative includes with module-based includes
- Update `pffdtd.cpp` to reference new locations
- Create include guards for all headers
- Document include hierarchy

#### 1.4 Create Module Documentation
Each folder gets a `README.md` explaining:
- Module purpose
- Dependencies (internal and external)
- Key functions/classes
- Usage examples
- Version history

**Example: src/physics/README.md**
```markdown
# Physics Module

## Purpose
Multi-fluid plasma physics equations and models.

## Models Supported
- plasma.h: Multi-species plasma (electrons + 3 ion species)
- plasmaN0.h: Current default model
- plasmaN1-4.h: Variant implementations
- plasmaNSheath.h: Sheath boundary conditions

## Key Functions
- PLASMAallocate(): Memory allocation
- PLASMAclear(): Array clearing
- UBCcalc(): Upper boundary conditions
- NBCcalc(): Normal boundary conditions

## Dependencies
- memallocate.h: Memory allocation

## Physics Equations
See PHYSICS.md in docs/ for detailed equations.
```

#### 1.5 Create Module Dependencies Document
**File:** `src/MODULE_DEPENDENCIES.txt`

```
Module Dependency Graph
========================

pffdtd.cpp
  ├─→ physics/plasma.h
  │    ├─→ utils/memallocate.h
  │    └─→ constants.h
  ├─→ fields/output.h
  │    └─→ utils/memallocate.h
  ├─→ source.h
  │    └─→ constants.h
  └─→ boundary/Retard.h

(Fields in Phase 2 will be separately modularized)

Dependency Rules:
1. No circular dependencies
2. Leaf modules (utils, constants) depend on nothing
3. Physics/Fields/IO depend only on utils/constants
4. Main solver depends on all modules
```

#### 1.6 Update Build System
- [ ] Update Makefile to use new directory structure
- [ ] Create CMakeLists.txt for cross-platform builds
- [ ] Add compiler flags documentation
- [ ] Test all build targets

**Makefile updates:**
```makefile
# New structure
SRC_DIR = src
PHYSICS_DIR = $(SRC_DIR)/physics
UTILS_DIR = $(SRC_DIR)/utils
BUILD_DIR = build

CPPFLAGS += -I$(SRC_DIR) -I$(PHYSICS_DIR) -I$(UTILS_DIR)
```

### Deliverables
- ✅ Organized src/ directory
- ✅ constants.h and types.h
- ✅ Updated include paths
- ✅ Module documentation (README.md files)
- ✅ Module dependency map
- ✅ Updated build system
- ✅ Verified compilation

### Success Criteria
- All includes updated without breaking compilation
- Executable functions identically to v1.8.2
- Build system generates correct output
- Documentation complete and accurate

---

## Phase 2: Modular Structure (Weeks 2-4)

**Goal:** Reorganize code into logical, independently testable modules

### Tasks

#### 2.1 Create IO Module
```
src/io/
  ├── output.h (rename to field_output.h)
  ├── outputN.h (rename to voltage_output.h)
  ├── file_handler.h (new)
  └── README.md
```

**file_handler.h functions:**
- `read_input_file()`: Parse .str files
- `write_field_data()`: Write .fd files
- `write_voltage_data()`: Write .vc files
- `validate_input()`

#### 2.2 Create Fields Module
```
src/fields/
  ├── field_arrays.h
  ├── field_calculator.h
  ├── grid.h
  └── README.md
```

**field_arrays.h:**
- E-field array management
- B-field array management
- Array initialization/cleanup

**field_calculator.h:**
- Ecalc(): E-field calculation
- Bcalc(): B-field calculation

#### 2.3 Create Boundary Module
```
src/boundary/
  ├── absorbing_bc.h (Retard.h refactored)
  ├── periodic_bc.h (new)
  ├── pml_bc.h (future)
  └── README.md
```

#### 2.4 Create Source Module
```
src/source/
  ├── source_types.h
  ├── source_calculator.h
  └── README.md
```

**source_types.h:**
Enums and structs for source configurations
- SINE_WAVE
- PULSE
- GAUSSIAN
- DC
- SINC

#### 2.5 Refactor Main Solver
**pffdtd.cpp becomes:**
```cpp
#include "fields/field_calculator.h"
#include "physics/plasma.h"
#include "boundary/absorbing_bc.h"
#include "source/source_calculator.h"
#include "io/file_handler.h"

int main(int argc, char* argv[]) {
    // Read input
    InputFile input = read_input_file(argv[1]);
    
    // Initialize
    FieldArrays fields = initialize_fields(input);
    PlasmaState plasma = initialize_plasma(input);
    
    // Time-stepping loop
    for (int t = 0; t < input.max_time; t++) {
        Ecalc(fields, plasma);
        apply_boundary_conditions(fields, input.boundary_type);
        Bcalc(fields);
        
        apply_source(fields, input.source, t);
        update_plasma(plasma, fields, input);
        
        if (t % input.output_interval == 0) {
            write_output(fields, plasma, t);
        }
    }
    
    cleanup(fields, plasma);
    return 0;
}
```

#### 2.6 Implement Physics Module Selector
Create runtime selection for plasma models instead of compile-time:

```cpp
// physics/model_factory.h
enum PlasmaModelType {
    MODEL_N0,  // Multi-species
    MODEL_N1,  // Variant 1
    MODEL_N2,  // Variant 2
    MODEL_SHEATH
};

PlasmaModel* create_plasma_model(PlasmaModelType type);
```

### Deliverables
- ✅ Five sub-modules (io, fields, boundary, source, physics)
- ✅ Refactored main solver
- ✅ Module README files
- ✅ Runtime model selection
- ✅ No compilation warnings
- ✅ Identical functionality to Phase 1

### Success Criteria
- All modules compile independently
- All modules link correctly
- Executable behavior identical to v1.8.2
- Each module ≤ 500 lines of code
- Module coupling analysis shows improvements

---

## Phase 3: Testing & Examples (Weeks 3-5)

**Goal:** Comprehensive test suite ensuring code correctness and preventing regressions

### Tasks

#### 3.1 Unit Tests
Create `tests/unit/`:
- test_memory.cpp: Memory allocation functions
- test_constants.cpp: Physical constants validation
- test_field_arrays.cpp: Array initialization
- test_plasma_models.cpp: Each plasma model
- test_source_types.cpp: Source calculations

**Framework:** Google Test (gtest) or Catch2

#### 3.2 Validation Tests
Create `tests/validation/`:
- test_free_space.cpp: Empty domain stability
- test_dispersion.cpp: Wave dispersion relation
- test_stability.cpp: CFL conditions
- test_energy_conservation.cpp: Energy balance
- test_boundary_conditions.cpp: Reflection coefficients

#### 3.3 Regression Tests
Create `tests/regression/`:
- test_dipole_free_space.cpp: Original dipole test case
- test_plasma_wave.cpp: Plasma wave test
- test_collision_damping.cpp: Collision effects

#### 3.4 Performance Benchmarks
Create `tests/benchmarks/`:
- benchmark_field_calculations.cpp: Timing Ecalc/Bcalc
- benchmark_memory_access.cpp: Cache efficiency
- benchmark_full_simulation.cpp: End-to-end timing

**Tools:** Google Benchmark

#### 3.5 Test Data Files
Create `tests/data/`:
- dipole_free_space.str: Simple test case
- plasma_wave.str: Plasma wave test
- collision_test.str: Collision damping
- edge_cases.str: Boundary conditions
- large_domain.str: Performance test

#### 3.6 Test Infrastructure
Create `tests/`:
- CMakeLists.txt: Build test targets
- run_tests.sh: Linux/Mac test runner
- run_tests.bat: Windows test runner
- test_config.h: Common test constants
- regression/compare_results.py: Golden file comparator

### Deliverables
- [ ] 20+ unit tests (Skipped)
- [ ] 10+ validation tests (Skipped)
- [x] Regression test framework
- [ ] 5+ performance benchmarks
- ✅ Comprehensive test data
- ✅ Automated test runner
- ✅ Coverage report (≥80%)

### Success Criteria
- All tests pass on Windows, Linux, macOS
- Code coverage ≥80%
- Performance baselines established
- No regressions detected

---

## Phase 4: Python Visualization (Weeks 4-6)

**Goal:** Replace MATLAB visualization with modern Python tools

### Tasks

#### 4.1 Python Analysis Tools
Create `visualization/`:
```
visualization/
  ├── requirements.txt
  ├── plot_fields.py
  ├── animate_fields.py
  ├── analyze_simulation.py
  ├── spectrum_analyzer.py
  └── README.md
```

**plot_fields.py:** (Completed)
- Load .fd files
- Plot E, B, and density fields
- Support 1D/2D slices
- Publication-quality figures

**plot_voltage.py:** (Completed)
- Load .vc files
- Time domain voltage/current
- Frequency domain analysis (FFT/DTFT)
- Impedance calculation

**animate_fields.py:**
- Create animations from field data
- Multiple simultaneous fields
- Adjustable speed/resolution

**analyze_simulation.py:**
- Energy calculation
- Power spectral density
- Field statistics

#### 4.2 Jupyter Notebooks
Create `notebooks/`:
```
notebooks/
  ├── 01_Getting_Started.ipynb
  ├── 02_Free_Space_Simulation.ipynb
  ├── 03_Plasma_Waves.ipynb
  ├── 04_Collision_Effects.ipynb
  ├── 05_Parameter_Study.ipynb
  └── 06_Results_Analysis.ipynb
```

Each notebook includes:
- Problem description
- Input file creation
- Running simulation (subprocess)
- Results analysis
- Visualization
- Interpretation

#### 4.3 Data Loader
**visualization/pffdtd_loader.py:**
```python
class SimulationData:
    def __init__(self, output_prefix):
        self.E_field = load_field_data(f'{output_prefix}.fd')
        self.voltage = load_voltage_data(f'{output_prefix}.vc')
        self.metadata = load_metadata(f'{output_prefix}.meta')
    
    def get_slice(self, field_name, time_idx, axis='z'):
        pass
    
    def get_time_series(self, field_name, x, y, z):
        pass
    
    def get_energy(self, time_range=None):
        pass
```

#### 4.4 Installation Guide
Create `visualization/INSTALL.md`:
- Python version requirements
- Dependency installation
- Virtual environment setup
- Conda environment file

### Deliverables
- [x] 3 core analysis tools (pffdtd_loader, utils, plot_voltage)
- [ ] 6 Jupyter notebooks
- [x] Data loader class
- [x] Installation requirements
- [x] Example plots

### Success Criteria
- All tools run without errors
- Notebooks execute end-to-end
- Visualizations match MATLAB quality
- Documentation complete

---

## Phase 5: Parallelization (Weeks 6-8)

**Goal:** Enable multi-threaded and distributed computing

### Tasks

#### 5.1 OpenMP Integration
**Compiler flags:**
```bash
g++ -O3 -fopenmp -std=c++11 src/*.cpp
```

**Parallelizable loops:**
```cpp
// Field calculation
#pragma omp parallel for collapse(3)
for (int i = ...) {
    for (int j = ...) {
        for (int k = ...) {
            // E-field update
        }
    }
}
```

#### 5.2 Performance Profiling
- Identify hotspots with gprof
- Measure parallel speedup
- Document thread scaling
- Create performance report

#### 5.3 MPI Support (Optional)
- Domain decomposition strategy
- Ghost cell communication
- Load balancing
- Example: 2-process distributed simulation

#### 5.4 Parallel Build Targets
Update Makefile:
```makefile
# Serial version
g++ -O3 -std=c++11 src/pffdtd.cpp -o pffdtd_serial

# OpenMP version
g++ -O3 -fopenmp -std=c++11 src/pffdtd.cpp -o pffdtd_parallel

# MPI version (if available)
mpicxx -O3 -std=c++11 src/pffdtd_mpi.cpp -o pffdtd_mpi
```

### Deliverables
- ✅ OpenMP parallelized field calculations
- ✅ Performance benchmarks (speedup curves)
- ✅ Parallel build targets
- ✅ Documentation for parallel usage

### Success Criteria
- 4x speedup on 4-core system
- Bitwise identical results
- All tests pass (parallel mode)

---

## Phase 6: GPU Support (Weeks 8-10)

**Goal:** Accelerate performance-critical calculations on GPU

### Tasks

#### 6.1 CUDA Integration
- Move field calculations to GPU
- GPU memory management
- CPU-GPU data transfer

**CUDA kernels:**
```cuda
__global__ void ecalc_kernel(...) {
    // E-field update on GPU
}

__global__ void bcalc_kernel(...) {
    // B-field update on GPU
}
```

#### 6.2 Build System
```makefile
# GPU version
nvcc -O3 -std=c++11 --gpu-architecture=sm_70 src/pffdtd_gpu.cu
```

#### 6.3 Performance Comparison
- GPU vs CPU benchmarks
- Memory bandwidth analysis
- PCIe transfer overhead
- Optimization recommendations

#### 6.4 HIP Support (Optional)
AMD GPU support using HIP for portability

### Deliverables
- ✅ CUDA kernels for field calculations
- ✅ GPU memory management
- ✅ CPU-GPU communication
- ✅ Performance benchmarks (10-50x speedup expected)

### Success Criteria
- 10x+ speedup on modern GPU
- Bitwise identical results
- All tests pass (GPU mode)

---

## Parallel Development Strategy (v2.0+)

**While Phase 1 is under way, the team can work in parallel on:**

### Option A: Physics Enhancement (Weeks 2-4)
- [ ] Add new plasma models (e.g., Maxwellian distributions)
- [ ] Implement adaptive time-stepping
- [ ] Add collisional heating models
- [ ] Document new physics on `develop` branch

**Branch:** `feature/new-physics`

### Option B: Documentation (Weeks 2-3)
- [ ] Expand theory documentation
- [ ] Create physics tutorial notebook
- [ ] Add troubleshooting guide
- [ ] Create benchmark comparison document

**Branch:** `feature/documentation`

### Option C: Infrastructure (Weeks 2-4)
- [ ] Set up GitHub Actions CI/CD
- [ ] Create Docker containers
- [ ] Set up automated documentation build
- [ ] Create project management board

**Branch:** `feature/infrastructure`

**Integration Schedule:**
- Week 2: Merge A/B/C proof-of-concepts into `develop`
- Week 3: Feature refinement
- Week 4: Consolidate into Phase 2
- Week 5: Merge to main as v1.9

---

## Code Organization Best Practices

### 1. Update Include Statements

**Current (BAD):**
```cpp
#include "plasma.h"  // Where is this?
#include "Retard.h"  // Ambiguous
```

**Future (GOOD):**
```cpp
#include "physics/plasma.h"
#include "boundary/absorbing_bc.h"
#include "utils/constants.h"
```

### 2. Add README.md to Each Folder

**Example: src/physics/README.md**
```markdown
# Physics Module

## Module Purpose
Implements multi-fluid plasma equations and boundary conditions.

## Files
- plasma.h: Base multi-species model
- plasmaN0-4.h: Variant implementations
- model_factory.h: Runtime model selection

## Key Equations
∂ρ/∂t + ∇·(ρv) = 0  (continuity)
ρ(∂v/∂t + v·∇v) = q(E + v×B) - ∇p - νρv  (momentum)

## Usage
```cpp
#include "physics/plasma.h"
PlasmaModel* model = create_plasma_model(MODEL_N0);
```

## Dependencies
- utils/memallocate.h
- utils/constants.h

## Status
✅ Stable | Version 1.8.2
```

### 3. Document Module Dependencies

**File: src/MODULE_DEPENDENCIES.txt**
```
pffdtd (main)
├─ physics/plasma.h
│  ├─ utils/memallocate.h
│  └─ utils/constants.h
├─ fields/field_calculator.h
│  ├─ utils/constants.h
│  └─ fields/field_arrays.h
├─ boundary/absorbing_bc.h
├─ source/source_calculator.h
│  └─ utils/constants.h
└─ io/file_handler.h

Dependency Analysis:
- Leaf modules: utils, constants (no dependencies)
- Physics modules: Depend only on utils
- Solver modules: Can depend on physics
- No circular dependencies

Update this file when adding/removing dependencies.
```

### 4. Coding Standards

**Header File Template:**
```cpp
#ifndef MODULE_NAME_H
#define MODULE_NAME_H

#include <necessary headers>
#include "utils/constants.h"

/**
 * @brief Module description
 * 
 * Detailed explanation of functionality and physics.
 * 
 * Dependencies: physics/plasma.h, utils/memallocate.h
 * Version: 1.8.2
 */

// Code here

#endif  // MODULE_NAME_H
```

**Function Documentation:**
```cpp
/**
 * @brief Calculate E-field using FDTD method
 * 
 * @param fields Field arrays (updated in-place)
 * @param plasma Plasma state
 * @param dt Time step (s)
 * @param dx Grid spacing (m)
 * 
 * @return Status code (0=success, <0=error)
 * 
 * @note Vectorized for SIMD performance
 * @warning Must call Bcalc() after this function
 */
void Ecalc(FieldArrays& fields, const PlasmaState& plasma,
           double dt, double dx);
```

### 5. Version Control Practices

**Branch Strategy:**
```
main (production)
  └─ develop (integration)
      ├─ feature/phase-2-modules
      ├─ feature/new-physics
      ├─ bugfix/boundary-condition
      └─ experimental/gpu-support
```

**Commit Message Format:**
```
feat: Add new feature
fix: Fix specific bug
docs: Update documentation
test: Add test coverage
perf: Improve performance
refactor: Reorganize code

Example:
feat(physics): Add adaptive timestep scheme
- Implements Courant number tracking
- Adjusts dt dynamically
- Improves stability near material boundaries

Closes #42
```

---

## Implementation Timeline

| Phase | Duration | Focus | Key Deliverable |
|-------|----------|-------|-----------------|
| **Immediate** | 2-3 days | GitHub Setup | Repository live ✅ |
| **Phase 1** | 1-2 weeks | Foundation | Organized src/, updated includes |
| **Phase 2** | 2-4 weeks | Modularization | Five sub-modules, runtime selection |
| **Phase 3** | 3-5 weeks | Testing | 80%+ code coverage, regression tests |
| **Phase 4** | 4-6 weeks | Visualization | Python tools, 6 notebooks |
| **Phase 5** | 6-8 weeks | Parallelization | OpenMP enabled, 4x speedup |
| **Phase 6** | 8-10 weeks | GPU Support | CUDA kernels, 10x+ speedup |
| **v2.0 Release** | Week 10 | Integration | Public release with all features |

**Overlap Strategy:**
- Phases 2, 3, 4 can proceed in parallel (different teams)
- Phase 5-6 depends on Phase 2 completion
- Phase 3 (testing) should start early and run continuously

---

## Success Metrics

### Phase 1 Completion
- [x] GitHub repository initialized and configured
- [ ] src/ organized with 5+ subdirectories
- [ ] All includes updated and compiling
- [ ] Module dependency document complete
- [ ] Build system tested on Windows/Linux

### Phase 2 Completion
- [ ] Five sub-modules created (io, fields, boundary, source, physics)
- [ ] Main solver refactored to ≤500 lines
- [ ] Runtime physics model selection working
- [ ] All modules independently compilable
- [ ] Zero compilation warnings

### Phase 3 Completion
- [ ] 25+ unit tests (all passing)
- [ ] 10+ validation tests (all passing)
- [ ] 5+ regression tests (all passing)
- [ ] Code coverage ≥80%
- [ ] Performance baselines established

### Phase 4 Completion
- [ ] 3 core Python tools working
- [ ] 6 Jupyter notebooks executing end-to-end
- [ ] Data loader class fully functional
- [ ] Visualizations match/exceed MATLAB quality
- [ ] Installation guide verified on multiple systems

### Phase 5 Completion
- [ ] OpenMP parallelization complete
- [ ] 4x+ speedup on 4-core system
- [ ] Performance profiling documented
- [ ] MPI prototype complete (optional)
- [ ] Parallel build targets working

### Phase 6 Completion
- [ ] CUDA kernels for field calculations
- [ ] GPU memory management robust
- [ ] 10x+ speedup on modern GPU
- [ ] Bitwise identical CPU/GPU results
- [ ] Performance analysis documented

### Overall v2.0 Release
- [ ] All phases complete
- [ ] Code coverage ≥85%
- [ ] Documentation complete (20+ pages)
- [ ] Performance optimized (serial/parallel/GPU)
- [ ] Open-source release ready

---

## Risk Mitigation

### Technical Risks

**Risk 1: Modularization breaks code**
- **Mitigation:** Extensive testing at each phase
- **Contingency:** Version control allows rollback

**Risk 2: Performance regression from refactoring**
- **Mitigation:** Establish baselines in Phase 3
- **Contingency:** Profile and optimize in Phase 5

**Risk 3: GPU implementation incompatible**
- **Mitigation:** Start with simple CUDA kernels
- **Contingency:** Keep CPU version as fallback

### Schedule Risks

**Risk 1: Phase 1 takes longer than expected**
- **Mitigation:** Run Phases 2-4 in parallel
- **Contingency:** Compress Phase 5-6 timeline

**Risk 2: Testing infrastructure delays Phase 3**
- **Mitigation:** Use simple test framework initially
- **Contingency:** Add sophisticated testing in v2.1

### Team Risks

**Risk 1: Limited resources**
- **Mitigation:** Parallel development strategy
- **Contingency:** Prioritize phases (1 > 2 > 3 > 4 > 5 > 6)

**Risk 2: Knowledge transfer for GPU/parallel**
- **Mitigation:** Document extensively
- **Contingency:** External consultant for Phase 5-6

---

## Decision Points

### Week 2 Review
**Questions:**
1. Is Phase 1 on schedule?
2. Should Phase 2-4 start in parallel?
3. Are any critical issues blocking progress?

**Actions:**
- Adjust timeline if needed
- Authorize parallel development
- Escalate blockers

### Week 4 Review
**Questions:**
1. Is modularization complete?
2. Are tests comprehensive?
3. Should Phase 5 (parallel) begin?

**Actions:**
- Merge Phase 2 to main (v1.9)
- Start Phase 5 planning
- Begin GPU feasibility study

### Week 6 Review
**Questions:**
1. Is visualization working?
2. Are performance targets met?
3. Can Phase 6 (GPU) proceed?

**Actions:**
- Finalize visualization tools
- Begin GPU implementation
- Plan v2.0 release roadmap

---

## References

**Related Documentation:**
- [DEVELOPERS.md](docs/DEVELOPERS.md) - Development setup
- [ARCHITECTURE.md](docs/ARCHITECTURE.md) - System design
- [PHYSICS.md](docs/PHYSICS.md) - Physics equations
- [INPUT_FORMAT.md](docs/INPUT_FORMAT.md) - Input specification
- [CONTRIBUTING.md](docs/CONTRIBUTING.md) - Contribution guidelines

**External Resources:**
- CMake Documentation: https://cmake.org/documentation/
- Google Test: https://github.com/google/googletest
- Jupyter Notebooks: https://jupyter.org/
- OpenMP: https://www.openmp.org/
- CUDA: https://developer.nvidia.com/cuda-toolkit

---

**Last Updated:** January 28, 2026  
**Next Review:** February 11, 2026  
**Status:** ACTIVE - Phase 1 in progress
