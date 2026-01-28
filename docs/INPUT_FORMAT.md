# Input File Format Specification

Complete specification for PF-FDTD input files (`.str` format).

## Overview

Input files control all aspects of a simulation including:
- Computational grid dimensions and spacing
- Source definitions and locations
- Material properties
- Antenna/obstacle structure
- Output parameters
- Plasma properties

## File Structure

```
<Input file format>
//Grid Parameters
sx  sy  sz              # Grid dimensions (cells)
dx  dy  dz              # Grid spacing (meters)

//Source Parameters
n_sources               # Number of sources
x  y  z  field  type  param    # Source 1 definition
x  y  z  field  type  param    # Source 2 definition
...                            # Additional sources

//Dielectric Parameters
Er1                     # Relative permittivity 1
Er2                     # Relative permittivity 2

//Antenna Structure
n_cells                 # Number of cells
x  y  z  Erx  Ery  Erz # Cell 1
x  y  z  Erx  Ery  Erz # Cell 2
...                    # Additional cells

//Output Field Info
iter  E  B  Ue  Ne  Ui  Ni    # Output configuration
lower_x  lower_y  lower_z      # Output region lower corner
upper_x  upper_y  upper_z      # Output region upper corner
```

## Parameter Descriptions

### Grid Parameters

```
sx  sy  sz
```

**Grid dimensions** in number of cells along each axis.

- **Type:** Integer
- **Range:** 10 - 2048 (limited by memory)
- **Typical:** 32 - 128
- **Example:** `64  64  64`

**Note:** Larger grids increase memory exponentially.
- 64³ → ~40 MB (with plasma)
- 128³ → ~320 MB
- 256³ → ~2.5 GB

```
dx  dy  dz
```

**Grid spacing** in meters.

- **Type:** Float (scientific notation OK)
- **Typical range:** 1e-3 to 1e-6 meters
- **Example:** `1.0e-3  1.0e-3  1.0e-3` (1 mm spacing)

**Physical constraint:** Must be small enough to resolve wave features:
$$\lambda_{min} > 10 \Delta x$$

Where $\lambda_{min}$ is the shortest wavelength of interest.

**Stability constraint:** Time step computed automatically to satisfy CFL condition.

### Source Parameters

```
n_sources
```

**Number of sources** in simulation.

- **Type:** Integer
- **Range:** 1 - 100
- **Example:** `2`

```
x  y  z  field  type  param
```

**Source location and type definition** (repeat for each source).

#### Location Parameters

```
x  y  z
```

Grid coordinates (integer) of source location.

- **Type:** Integer
- **Range:** 1 to (sx-1), 1 to (sy-1), 1 to (sz-1)
- **Note:** Avoid boundaries (field not accurate there)
- **Example:** `32  32  32`

#### Field Parameter

```
field
```

Which field component to source.

- **1** = Ex (electric field x-component)
- **2** = Ey (electric field y-component)
- **3** = Ez (electric field z-component)
- **Type:** Integer
- **Example:** `3` (drive Ez)

#### Source Type and Parameter

```
type  param
```

**Type:** Source waveform shape

| Type | Name | Parameter | Unit |
|------|------|-----------|------|
| 1 | Sinusoidal | Frequency | Hz |
| 2 | Pulse | Frequency | Hz |
| 3 | Raised Cosine | Frequency | Hz |
| 4 | Gaussian | Spread | seconds |
| 5 | Gaussian Derivative | Spread | seconds |
| 6 | DC | Value | V/m |
| 7 | Sinc | Cutoff Freq | Hz |

**Detailed definitions:**

**Type 1: Sinusoidal**
```
V(t) = sin(2π * freq * t)
param = frequency (Hz)
Example: 1  1.0e7   (10 MHz sine)
```

**Type 2: Pulse (Sine-modulated)**
```
Sine wave with smooth pulse envelope
param = center frequency (Hz)
Example: 2  5.0e6   (5 MHz modulated pulse)
```

**Type 3: Raised Cosine**
```
Smooth pulse with cosine envelope
param = frequency (Hz)
Example: 3  2.0e6   (2 MHz raised cosine)
```

**Type 4: Gaussian**
```
V(t) = exp(-(t/spread)²)
param = time spread (seconds)
Example: 4  1.0e-8  (10 ns Gaussian)
```

**Type 5: Gaussian Derivative**
```
V(t) = -(t/spread²) * exp(-(t/spread)²)
param = time spread (seconds)
Example: 5  1.0e-8  (derivative of 10 ns Gaussian)
```

**Type 6: DC (Constant)**
```
V(t) = constant
param = field value (V/m)
Example: 6  1.0e5   (100 kV/m DC)
```

**Type 7: Sinc**
```
V(t) = sin(π*t*f_c) / (π*t*f_c)
param = cutoff frequency (Hz)
Example: 7  5.0e6   (5 MHz sinc pulse)
```

**Multiple Source Example:**

```
//Source Parameters
3                      # 3 sources total
32  32  32  3  1  1.0e7    # Source 1: Sine 10 MHz at (32,32,32) on Ez
16  32  32  1  4  1.0e-8   # Source 2: Gaussian on Ex at (16,32,32)
48  32  32  3  6  1.0e5    # Source 3: DC 100kV/m on Ez at (48,32,32)
```

### Dielectric Parameters

```
Er1
Er2
```

**Relative permittivity** of dielectric materials (not plasma).

- **Type:** Float
- **Typical range:** 1.0 - 10.0
- **Example:** `1.0` (free space) and `4.0` (dielectric)

**Note:** Currently PF-FDTD treats these identically. Can support different materials in antenna definition.

### Antenna Structure

```
n_cells
```

**Number of cells in antenna structure**.

- **Type:** Integer
- **Range:** 1 - 100,000
- **Example:** `10`

```
x  y  z  Erx  Ery  Erz
```

**Cell definition** (repeat for each cell).

#### Material Definition

```
x  y  z  Erx  Ery  Erz
```

- **x, y, z** = Grid coordinates (integer)
- **Erx, Ery, Erz** = Relative permittivity in each direction

**Erx, Ery, Erz values:**
- **0** = Free space / Plasma
- **1** = Metal (PEC - Perfect Electrical Conductor)
- **2** = Dielectric material 1 (Er1)
- **3** = Dielectric material 2 (Er2)

**Example antenna structures:**

Dipole antenna:
```
//Antenna Structure
2                  # 2 cells for dipole
32  32  31  1  0  1    # Bottom conductor (metal, Erx varied)
32  32  33  1  0  1    # Top conductor (metal, Erx varied)
```

Monopole antenna:
```
//Antenna Structure
1
32  32  32  1  0  1
```

Patch antenna (5×5 patch):
```
//Antenna Structure
25
31  31  32  1  1  0
31  32  32  1  1  0
...
(25 cells total forming a square)
```

### Output Field Info

```
iter  E  B  Ue  Ne  Ui  Ni
```

**Output configuration parameters**.

#### Iteration Rate

```
iter
```

**Number of iterations between outputs**.

- **Type:** Integer
- **Range:** 1 - 10,000
- **Example:** `10` (output every 10 iterations)

**Effect on file size:**
- iter=1: Large file, complete time history
- iter=10: 10× smaller file
- iter=100: 100× smaller file

#### Field Output Flags

```
E  B  Ue  Ne  Ui  Ni
```

Binary flags (0 or 1) for each field type.

| Flag | Field | Description |
|------|-------|-------------|
| E | 1 or 0 | Electric field (Ex, Ey, Ez) |
| B | 1 or 0 | Magnetic field (Bx, By, Bz) |
| Ue | 1 or 0 | Electron velocity (Uex, Uey, Uez) |
| Ne | 1 or 0 | Electron density |
| Ui | 1 or 0 | Ion velocity (Uix, Uiy, Uiz) |
| Ni | 1 or 0 | Ion density |

**Example:** `1  1  0  0  0  0`
- Output: E and B fields only
- Don't output: Velocities or densities

### Output Region

```
lower_x  lower_y  lower_z
upper_x  upper_y  upper_z
```

**Rectangular region where fields are recorded**.

- **Type:** Integer (grid coordinates)
- **Constraint:** lower < upper for each dimension
- **Example:**
  ```
  1   1   1      # Lower corner
  63  63  63     # Upper corner (outputs entire 64³ domain)
  ```

**Smaller region example:**
```
30  30  30     # Output only central region
34  34  34     # 5×5×5 cube
```

## Complete Example Files

### Example 1: Free-Space Dipole

```
//Free space dipole antenna test
//Grid Parameters
64  64  64
1.0e-3  1.0e-3  1.0e-3

//Source Parameters
1
32  32  32  3  1  1.0e7

//Dielectric Parameters
1.0
1.0

//Antenna Structure
2
32  32  31  1  0  1
32  32  33  1  0  1

//Output Field Info
10  1  1  0  0  0  0
1   1   1
63  63  63
```

### Example 2: Plasma with Langmuir Probe

```
//Langmuir probe in plasma
//Grid Parameters
128  128  128
5.0e-4  5.0e-4  5.0e-4

//Source Parameters
2
64  64  32  3  1  1.0e6
64  64  96  3  6  5.0e4

//Dielectric Parameters
1.0
1.0

//Antenna Structure
3
64  64  32  1  1  1
64  64  64  1  1  1
64  64  96  1  1  1

//Output Field Info
5  1  1  1  1  1  1
30  30  30
98  98  98
```

**Run with plasma parameters:**
```bash
./pffdtd langmuir.str output 5.3e6 0.27 18.7 22.0 0.0 300.0
```

### Example 3: Magnetized Plasma

```
//Magnetized plasma simulation
//Grid Parameters
96  96  96
1.0e-3  1.0e-3  1.0e-3

//Source Parameters
1
48  48  48  1  4  2.0e-8

//Dielectric Parameters
1.0
1.0

//Antenna Structure
1
48  48  48  1  1  1

//Output Field Info
20  1  1  1  1  0  0
10  10  10
86  86  86
```

**Run with magnetic field:**
```bash
./pffdtd magnetized.str output 5.3e6 0.27 100.0 45.0 90.0 0.0
```

## Command-Line Execution

### Free Space (No Plasma)

```bash
./pffdtd input.str output_prefix
```

### With Plasma Parameters

```bash
./pffdtd input.str output_prefix plasma_freq collision_freq gyro_freq \
  elev_angle azimuth_angle temperature
```

**Parameters (in order):**
1. `plasma_freq` - Plasma frequency (Hz) [e.g., 5.3e6]
2. `collision_freq` - Collision frequency ratio [e.g., 0.27]
3. `gyro_freq` - Cyclotron frequency (Hz) [e.g., 18.7]
4. `elev_angle` - Elevation angle of B field (degrees) [e.g., 22.0]
5. `azimuth_angle` - Azimuth angle of B field (degrees) [e.g., 0.0]
6. `temperature` - Plasma temperature (K) [e.g., 0.0]

### Output File Extensions

```
input.str              → Input file
output_prefix.vc       → Voltage/Current output
output_prefix.fd       → Field data output
```

## Validation and Constraints

### Input Validation

The program checks for:

| Check | Error | Fix |
|-------|-------|-----|
| Grid size > 0 | "Invalid grid dimensions" | Ensure sx, sy, sz ≥ 10 |
| Grid spacing > 0 | "Invalid grid spacing" | Ensure dx, dy, dz > 0 |
| n_sources valid | "Invalid source count" | Ensure 1 ≤ n_sources ≤ 100 |
| Source location in bounds | "Source outside grid" | 1 ≤ x,y,z ≤ (s-1) |
| Field type valid | "Invalid field type" | 1 ≤ field ≤ 3 |
| Source type valid | "Invalid source type" | 1 ≤ type ≤ 7 |
| Output region valid | "Invalid output region" | lower < upper |

### Physical Constraints

**CFL Stability:**
```
Δt ≤ 1/(c*√(1/dx² + 1/dy² + 1/dz²))
```
Automatically enforced by program.

**Plasma Resolution:**
```
Δt should be << 1/f_plasma
```
Recommended: at least 20 points per plasma period.

**Wave Resolution:**
```
Δx should be << λ (wavelength)
```
Recommended: at least 10 points per wavelength.

## Tips for Creating Input Files

1. **Start with example file** - Modify existing template
2. **Check grid size** - Balance between accuracy and memory
3. **Set spacing carefully** - Should resolve smallest feature
4. **Choose output rate** - Higher rate = larger files
5. **Define output region** - Can be smaller than full domain
6. **Validate before running** - Check all parameters make sense
7. **Run small test first** - Verify setup before large runs

## Common Issues

### Large Output Files

**Problem:** Output files become huge (GBs)

**Solutions:**
- Increase `iter` (output every 10 iterations instead of 1)
- Decrease output region
- Don't output unnecessary fields (set flags to 0)

### Numerical Instability (NaN in output)

**Problem:** Simulation diverges, NaNs appear in results

**Possible causes:**
- Grid spacing too coarse relative to wavelength
- Collision frequency too small
- Source amplitude too large
- Grid size too small

**Solutions:**
- Use smaller grid spacing (dx, dy, dz)
- Start with smaller simulations to test
- Increase collision frequency slightly

### Memory Errors

**Problem:** "Not enough memory" error

**Solutions:**
- Reduce grid size (sx, sy, sz)
- Increase grid spacing (dx, dy, dz)
- Reduce output region size
- Increase iteration count between outputs

---

**Last Updated:** January 2026
**Version:** 1.0
