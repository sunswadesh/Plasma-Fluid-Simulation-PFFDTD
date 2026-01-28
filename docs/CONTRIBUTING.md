# Contributing to PF-FDTD

Thank you for your interest in contributing to the Plasma Fluid - Finite Difference Time Domain model! This document provides guidelines and instructions for contributing.

## Code of Conduct

Our project is committed to providing a welcoming and inclusive environment. We expect all contributors to:
- Be respectful of different viewpoints and experiences
- Provide and accept constructive criticism gracefully
- Focus on discussions about code, not personal attacks
- Report concerning behavior to maintainers

## How to Contribute

### Reporting Bugs

Before submitting a bug report, please check existing issues to avoid duplicates.

**Submit a bug report by creating a GitHub Issue with:**

1. **Title**: Clear, descriptive title
   ```
   [Bug] Incorrect plasma density at boundary
   ```

2. **Description**: Include:
   - Brief summary of the issue
   - Expected behavior
   - Actual behavior
   - Steps to reproduce
   - Input file (attach or paste)
   - Output log or error message

3. **Environment**:
   ```
   - OS: [e.g., Linux (Ubuntu 20.04), macOS 11, Windows 10]
   - Compiler: [e.g., GCC 9.3, Clang 10.0]
   - PFFDTD Version: [v1.8.2 or commit hash]
   ```

4. **Example Issue Template**:
   ```
   ## Bug Description
   Simulation crashes with segmentation fault when using temperature > 5000K
   
   ## Steps to Reproduce
   1. Use `tests/data/plasma_high_temp.str` input file
   2. Run: `./pffdtd tests/data/plasma_high_temp.str output --temperature 5000`
   3. Simulation crashes at iteration 256
   
   ## Expected Behavior
   Simulation should complete successfully for 10000 iterations
   
   ## Actual Behavior
   ```
   Segmentation fault (core dumped)
   Memory address not mapped to object
   ```
   
   ## Environment
   - OS: Linux (Ubuntu 20.04)
   - Compiler: GCC 9.3
   - Version: v1.8.2
   ```

### Suggesting Enhancements

Create an issue with label `enhancement`:

**Template for Feature Requests:**

```
## Feature Description
Clear description of the desired feature or enhancement

## Motivation
Why is this feature needed? What problem does it solve?

## Proposed Solution
Describe how you envision this feature working

## Alternatives Considered
What other approaches might work?

## Physics Background
For physics enhancements, include:
- Relevant equations
- References to literature
- Physical justification
```

**Example:**

```
## Feature: GPU Acceleration for Field Calculations

## Motivation
Current simulations on 512x512x512 grids take ~2 hours. GPU acceleration
could reduce this to minutes, enabling parameter studies.

## Proposed Solution
Implement CUDA kernels for Ecalc() and Bcalc() functions,
focusing on the innermost loops where 90% of time is spent.

## Physics Background
No new physics - direct port of existing staggered Yee grid algorithm
to GPU architecture.

## References
- CUDA C Programming Guide
- Taflove FDTD methods book, Ch. 6
```

### Submitting Code Contributions

#### 1. Fork and Clone

```bash
# Fork on GitHub first, then:
git clone https://github.com/YOUR-USERNAME/Plasma-Fluid-Simulation-PFFDTD.git
cd Plasma-Fluid-Simulation-PFFDTD
git remote add upstream https://github.com/sunswadesh/Plasma-Fluid-Simulation-PFFDTD.git
```

#### 2. Create Feature Branch

```bash
# Always branch from develop
git fetch upstream
git checkout upstream/develop
git checkout -b feature/descriptive-name

# Naming conventions:
# feature/parallel-processing
# feature/gpu-acceleration
# fix/boundary-condition-bug
# docs/api-documentation
# test/validation-suite
```

#### 3. Make Changes

- Make logical, focused commits
- One feature/fix per branch
- Write clear commit messages (see format below)

**Commit Message Format:**

```
<type>(<scope>): <subject> (max 50 chars)

<body> (wrap at 72 chars)

<footer>
```

**Types**: `feat`, `fix`, `refactor`, `perf`, `test`, `docs`, `chore`  
**Scope**: `plasma`, `output`, `boundaries`, `parallel`, `visualization`, etc.

**Examples:**

```
feat(plasma): add temperature-dependent collisions

Implements temperature scaling based on classical plasma theory.
Collision frequency now computed as:
  ν(T) = ν(0) * sqrt(T/T_ref)

- Adds new parameter: temperature_scaling_enabled
- Updates input file format (backwards compatible)
- All validation tests pass (12/12)

Fixes #42
```

```
fix(boundaries): correct retarded time calculation

Previous implementation had off-by-one error in time index.
Changed from:
  ABC_field[n-1] = ...
To:
  ABC_field[n] = ...

Validation: compares with analytical solution for plane wave
Error decreased from 2.3% to 0.1%

Fixes #88
```

#### 4. Update Documentation

For any code changes:
- Update relevant `.md` files in `docs/`
- Add comments explaining complex physics
- Update `CHANGELOG.md`
- Include docstrings for new functions

#### 5. Test Your Changes

```bash
# Compile without optimization (faster debugging)
cd src
g++ -O0 -g -std=c++11 pffdtd.cpp -o pffdtd

# Run existing tests
cd ../tests
./run_tests.sh

# Test your specific change
../src/pffdtd data/your_test_case.str output/your_test_case
python3 validate.py ../output/your_test_case
```

#### 6. Create Pull Request

**Push your branch:**
```bash
git push origin feature/descriptive-name
```

**Go to GitHub and create Pull Request with:**

1. **Title**: `[COMPONENT] Brief description`
   ```
   [Physics] Add temperature-dependent collision frequency
   [Parallel] Implement OpenMP field calculations
   [Visualization] Create improved Python plotting
   ```

2. **Description**:
   ```markdown
   ## Description
   Fixes #42 - Brief description of what this PR does
   
   ## Changes Made
   - Change 1
   - Change 2
   - Change 3
   
   ## Physics Validation
   Compared against:
   - Analytical solution for plane wave in free space
   - Reference data from Ward (2006) dissertation
   - Results within 0.1% error
   
   ## Testing
   - [x] Existing tests pass (12/12)
   - [x] New test case added: tests/test_temperature.cpp
   - [x] Backwards compatibility verified
   
   ## Performance Impact
   - Field calculation: +2% overhead (temperature lookup)
   - Memory: No additional memory
   - Impact: Negligible for most applications
   
   ## Checklist
   - [x] Code follows style guide
   - [x] Comments added for complex sections
   - [x] Documentation updated
   - [x] No new compiler warnings
   - [x] Tested on multiple grid sizes
   ```

3. **Link Related Issues**:
   ```
   Fixes #42
   Related to #15, #23
   ```

#### 7. Code Review

- Maintainers will review your code
- Respond constructively to feedback
- Make requested changes
- Expect 2-7 days for review

#### 8. Merge

Once approved:
- Maintainers will merge your PR
- Your feature branch will be deleted
- You'll be recognized in CHANGELOG.md

## Style Guidelines

### C++ Code Style

See [DEVELOPERS.md](DEVELOPERS.md#coding-standards) for detailed guidelines.

Quick summary:
- Use `camelCase` for variables and functions
- Use `UPPER_CASE` for constants
- 4-space indentation
- Lines ≤ 100 characters
- Comment non-obvious logic
- No trailing whitespace

### Python Code Style

Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/):

```python
# Good
def calculate_field_magnitude(field_x, field_y, field_z):
    """Calculate magnitude of 3D field vector."""
    magnitude = np.sqrt(field_x**2 + field_y**2 + field_z**2)
    return magnitude

# Avoid
def calcFieldMag(fx, fy, fz):
    mag = np.sqrt(fx**2 + fy**2 + fz**2)
    return mag
```

### Documentation Style

Use Markdown with clear structure:

```markdown
# Section Header

Brief introduction.

## Subsection

More detailed content.

- Bullet point 1
- Bullet point 2

**Bold** for emphasis, `code` for identifiers.

```code block for longer code```
```

## Testing Requirements

### Minimum Testing Before Submission

1. **Compilation**: No errors or warnings
   ```bash
   g++ -O2 -Wall -Wextra -std=c++11 pffdtd.cpp
   ```

2. **Existing Tests Pass**
   ```bash
   ./run_tests.sh  # All tests must pass
   ```

3. **New Feature Test**: Test your specific changes
   ```bash
   ./pffdtd tests/input_for_your_feature.str output
   ```

4. **Regression Testing**: Verify previous functionality
   ```bash
   ./pffdtd tests/dipole.str output
   diff expected_output/dipole.vc output.vc
   ```

### Physics Validation

For physics enhancements:

1. **Analytical Validation**: Compare with known analytical solutions
2. **Numerical Validation**: Compare with reference simulations
3. **Physical Limits**: Test extreme but valid parameters
4. **Literature Comparison**: Verify against published results

**Example Validation Report:**

```
## Temperature-Dependent Collision Frequency Validation

### Test Case: Plasma wave propagation with varying temperature

Input parameters:
- Grid: 64x64x64, dx=dy=dz=1 mm
- Plasma frequency: 5.3 MHz
- Temperature range: 0K to 5000K

Results:
- Baseline (T=0K): matches Ward 2006 reference by 0.05%
- Intermediate (T=1000K): collision freq scaled correctly per theory
- High temperature (T=5000K): stable, no numerical artifacts

Conclusion: Implementation matches classical plasma theory within 0.1%
```

## Review Process

### What Reviewers Look For

1. **Correctness**: Does the code work as intended?
2. **Physics**: Are equations correct and well-referenced?
3. **Style**: Does it follow guidelines?
4. **Tests**: Is new functionality tested?
5. **Performance**: No significant degradation?
6. **Documentation**: Clear and complete?

### Addressing Review Comments

```
Reviewer: "The collision frequency calculation looks wrong. 
           Is this using the formula from Ward 2006?"

Response: "Good catch! I was using the formula from Fridman's book.
          I've updated it to match Ward Eq. 3.24 and added a comment.
          See commit abc123."
```

## Additional Ways to Contribute

### 1. Documentation
- Improve existing documentation
- Add physics explanations
- Create tutorials
- Fix typos

### 2. Testing
- Write test cases
- Add validation benchmarks
- Improve test infrastructure

### 3. Visualization
- Enhance Python visualization tools
- Create new plotting utilities
- Build data analysis pipelines

### 4. Performance
- Profile and optimize code
- Parallelize bottlenecks
- Improve memory efficiency

### 5. Community
- Help answer questions
- Review others' contributions
- Share results and applications

## Resources for Contributors

- **Physics**: See references in DEVELOPERS.md
- **FDTD Methods**: Taflove & Hagness (2005)
- **Plasma Physics**: Fridman & Kennedy (2004)
- **Version Control**: Pro Git - https://git-scm.com/book/

## Recognition

Contributors will be recognized in:
- CHANGELOG.md (with each release)
- GitHub contributors page
- Project documentation
- Author acknowledgments in papers using this code

## Questions?

- Check [DEVELOPERS.md](DEVELOPERS.md)
- Search existing issues
- Create a GitHub Discussion
- Contact maintainers

---

**Thank you for contributing to PFFDTD!**

We appreciate your effort to improve this scientific software and advance plasma physics research.

Last Updated: January 2026
