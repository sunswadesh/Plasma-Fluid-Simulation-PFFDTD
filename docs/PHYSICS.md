# Physics Models and Equations

## Overview

This document describes the physics models implemented in PF-FDTD and the fundamental equations governing the simulations.

## Table of Contents

1. [Electromagnetic Theory](#electromagnetic-theory)
2. [Plasma Physics Models](#plasma-physics-models)
3. [Multi-Fluid Model](#multi-fluid-model)
4. [Collision Physics](#collision-physics)
5. [Boundary Conditions](#boundary-conditions)
6. [Numerical Implementation](#numerical-implementation)

## Electromagnetic Theory

### Maxwell's Equations (SI Units)

The core of FDTD is solving Maxwell's equations in the presence of a plasma:

$$\nabla \times \mathbf{E} = -\frac{\partial \mathbf{B}}{\partial t}$$

$$\nabla \times \mathbf{B} = \mu_0 \epsilon_0 \frac{\partial \mathbf{E}}{\partial t} + \mu_0 \mathbf{J}$$

$$\nabla \cdot \mathbf{E} = \frac{\rho}{\epsilon_0}$$

$$\nabla \cdot \mathbf{B} = 0$$

Where:
- $\mathbf{E}$ = Electric field (V/m)
- $\mathbf{B}$ = Magnetic field (T)
- $\mathbf{J}$ = Current density (A/m²)
- $\rho$ = Charge density (C/m³)
- $\mu_0 = 4\pi \times 10^{-7}$ H/m (permeability of free space)
- $\epsilon_0 = 8.854 \times 10^{-12}$ F/m (permittivity of free space)

### Constitutive Relations

For a linear, isotropic medium:
$$\mathbf{D} = \epsilon_0 \epsilon_r \mathbf{E}$$

$$\mathbf{B} = \mu_0 \mathbf{H}$$

In current implementation:
- $\epsilon_r = 1$ (plasma effects absorbed into J term)
- $\mu_r = 1$ (non-magnetic media)

### Finite Difference Time Domain (FDTD)

The differential equations are discretized on a **Yee grid** with staggered field components:

```
Position: Grid point (i, j, k)
Time: t^n or t^{n+1}

E-fields located at cell edges
B-fields located at cell faces

Example staggered arrangement:
Ez, Ex at (i+1/2, j, k)
Ey at (i, j+1/2, k)
Bx at (i, j+1/2, k+1/2)
etc.
```

### Update Equations (3D)

**Electric Field Updates:**

$$E_x^{n+1}_{i,j,k} = E_x^n_{i,j,k} + \frac{\Delta t}{\epsilon_0 \Delta y}(H_z^{n+1/2}_{i,j,k} - H_z^{n+1/2}_{i,j-1,k})$$
$$- \frac{\Delta t}{\epsilon_0 \Delta z}(H_y^{n+1/2}_{i,j,k} - H_y^{n+1/2}_{i,j,k-1}) - \frac{\Delta t}{\epsilon_0} J_x^n_{i,j,k}$$

With similar expressions for $E_y$ and $E_z$.

**Magnetic Field Updates:**

$$H_x^{n+1/2}_{i,j,k} = H_x^{n-1/2}_{i,j,k} + \frac{\Delta t}{\mu_0 \Delta z}(E_y^n_{i,j,k+1} - E_y^n_{i,j,k})$$
$$- \frac{\Delta t}{\mu_0 \Delta y}(E_z^n_{i,j+1,k} - E_z^n_{i,j,k})$$

With similar expressions for $H_y$ and $H_z$.

### CFL Stability Condition

For guaranteed stability:

$$\Delta t \leq \frac{1}{c\sqrt{\frac{1}{(\Delta x)^2} + \frac{1}{(\Delta y)^2} + \frac{1}{(\Delta z)^2}}}$$

Where $c = 3 \times 10^8$ m/s (speed of light).

In 3D with uniform grid spacing $\Delta = \Delta x = \Delta y = \Delta z$:

$$\Delta t \leq \frac{\Delta}{c\sqrt{3}}$$

## Plasma Physics Models

### Cold Plasma Model (Default)

The simplest plasma model treats plasma as a cold (zero temperature) fluid with collisions.

**Current density from Ohm's law:**

$$\mathbf{J} = \sigma \mathbf{E} = n_e e \mu_e \mathbf{E}$$

Where:
- $\sigma$ = Conductivity (S/m)
- $n_e$ = Electron density (m⁻³)
- $e = 1.602 \times 10^{-19}$ C (elementary charge)
- $\mu_e$ = Electron mobility = $\frac{e}{\nu_m m_e}$
- $\nu_m$ = Collision frequency (Hz)
- $m_e = 9.109 \times 10^{-31}$ kg (electron mass)

### Plasma Frequency

The fundamental timescale of plasma dynamics:

$$\omega_p = \sqrt{\frac{n_e e^2}{\epsilon_0 m_e}}$$

$$f_p = \frac{\omega_p}{2\pi}$$

Typical values:
- Low pressure plasma: $f_p \sim 1-10$ GHz
- Laboratory plasma: $f_p \sim 1-100$ MHz
- Ionosphere: $f_p \sim 1-10$ MHz

### Collisional Damping

Collision frequency (parametrized):

$$\nu_c = \nu_0 f_p$$

Where $\nu_0$ is the collision frequency as a fraction of plasma frequency (typically 0.1 - 1.0).

**Temperature dependent:** (optional, in plasmaN1-N3)

$$\nu(T) = \nu_0 \sqrt{\frac{T}{T_{ref}}}$$

Based on classical plasma collision cross-section: $\sigma \propto T^{-1/2}$

## Multi-Fluid Model

### Two-Fluid Description

The plasma is modeled as two interpenetrating fluids:
1. **Electron fluid** (species 0)
2. **Ion fluid(s)** (species 1, 2, ...)

### Conservation Laws

**Continuity equation** (mass conservation):

$$\frac{\partial n_s}{\partial t} + \nabla \cdot (n_s \mathbf{u}_s) = 0$$

**Momentum equation** (Newton's 2nd law):

$$m_s n_s \frac{D\mathbf{u}_s}{Dt} = q_s n_s \mathbf{E} + q_s n_s \mathbf{u}_s \times \mathbf{B} - m_s n_s \nu_s \mathbf{u}_s + \mathbf{F}_{external}$$

Where:
- $n_s$ = Number density of species $s$
- $\mathbf{u}_s$ = Velocity of species $s$
- $m_s$ = Mass of species $s$
- $q_s$ = Charge of species $s$
- $\nu_s$ = Collision frequency of species $s$
- $\frac{D}{Dt}$ = Material (Lagrangian) derivative

### Implementation in FDTD

**Discretized momentum conservation:**

$$\mathbf{u}_s^{n+1} = \frac{1}{1+\nu_s \Delta t}\left[\mathbf{u}_s^n + \frac{\Delta t}{m_s}\left(q_s \mathbf{E}^n + q_s \mathbf{u}_s^n \times \mathbf{B}^n - m_s n_s \nu_s \mathbf{u}_s^n\right)\right]$$

**Discretized continuity:**

$$n_s^{n+1} = n_s^n - \Delta t \nabla \cdot (n_s^n \mathbf{u}_s^{n+1})$$

Using upwind finite differences to maintain stability.

### Current Density Contribution

Total current from all species:

$$\mathbf{J} = \sum_s q_s n_s \mathbf{u}_s$$

This replaces the cold plasma conductivity in the FDTD equations.

## Collision Physics

### Linear Collision Operator

The simplest collision model uses a damping term proportional to velocity:

$$-m_s n_s \nu_s \mathbf{u}_s$$

This represents collisions through a relaxation time approximation:

$$\tau_c = \frac{1}{\nu_s}$$

### Coulomb Collisions (Advanced)

Full Fokker-Planck collision operator (not currently implemented):

$$\left(\frac{\partial f}{\partial t}\right)_{coll} = \frac{e^4 n \ln\Lambda}{12\pi^{3/2} \epsilon_0^2 m v^3} \frac{\partial}{\partial v}\left(v \frac{\partial f}{\partial v}\right)$$

Where:
- $f$ = velocity distribution function
- $\ln\Lambda$ = Coulomb logarithm (~10 for typical plasmas)
- $n$ = electron density

### Temperature Dependence

The collision cross-section scales as:

$$\sigma(T) \propto T^{-1/2}$$

Leading to collision frequency:

$$\nu(T) = \nu_0 \sqrt{\frac{T}{T_0}}$$

**Reference temperature:** $T_0 = 300$ K (room temperature)

## Magnetized Plasma

### Cyclotron Motion

In a magnetic field, particles undergo cyclotron motion with angular frequency:

$$\omega_c = \frac{|q| B}{m}$$

**Cyclotron frequency (Hz):**

$$f_c = \frac{\omega_c}{2\pi}$$

### Gyroradius

Characteristic radius of cyclotron orbit:

$$r_g = \frac{m v_\perp}{|q| B}$$

Where $v_\perp$ is velocity perpendicular to B.

### Lorentz Force

Magnetic force on particle:

$$\mathbf{F}_{mag} = q(\mathbf{v} \times \mathbf{B})$$

This is included in momentum conservation:

$$m_s n_s \frac{\partial \mathbf{u}_s}{\partial t} = q_s n_s (\mathbf{E} + \mathbf{u}_s \times \mathbf{B}) - m_s n_s \nu_s \mathbf{u}_s$$

## Boundary Conditions

### Absorbing Boundary Conditions (ABC)

To prevent artificial reflections from domain boundaries, retarded-time ABC is used:

**Mur's Boundary Condition (1st order):**

$$E_{boundary}^{n+1} = E_{interior}^n + \frac{c\Delta t - \Delta x}{c\Delta t + \Delta x}(E_{boundary}^n - E_{interior}^{n+1})$$

Where:
- $c$ = speed of light
- $\Delta t$ = time step
- $\Delta x$ = spatial step

**Advantages:**
- Reduces reflections by ~95%
- Low computational cost
- Applicable to general non-uniform grids

### Antenna Boundary Conditions

On antenna surfaces (conductors):

$$\mathbf{E}_{tangential} = 0$$

$$\mathbf{B}_{normal} = 0$$

Implemented by zeroing field components at antenna locations before time-stepping.

### Plasma Boundary Conditions

Particle velocity and density at boundaries:

$$\mathbf{u}_s|_{boundary} = 0$$ (particles reflect or absorb)

$$\frac{\partial n_s}{\partial t}|_{boundary} = 0$$ (particle conservation)

## Numerical Implementation

### Time Stepping Algorithm

```
For each time step n:

1. Update E-field from B^n and J^n
   E^{n+1} = f(E^n, B^n, J^n)

2. Update plasma velocities from E^{n+1}
   U^{n+1} = g(U^n, E^{n+1}, B^n)

3. Update plasma density from U^{n+1}
   N^{n+1} = h(N^n, U^{n+1})

4. Calculate new current from N^{n+1} and U^{n+1}
   J^{n+1} = sum_s q_s n_s u_s

5. Update B-field from E^{n+1}
   B^{n+1} = f(B^n, E^{n+1})

6. Apply boundary conditions
   E_ABC = apply_retarded_ABC(E)
   Set antenna fields to zero

7. Output if needed
   Write to output files
```

### Stability and Accuracy

**Stability criteria:**
1. CFL condition for EM wave (required)
2. Plasma frequency resolution: $\Delta t < 0.1 / f_p$ (recommended)
3. Collision damping: $\Delta t < 1 / \nu$ (for explicit integration)

**Accuracy:**
- Spatial: 2nd order (central differences)
- Temporal: 2nd order (leapfrog structure)
- Relative error per step: $O(\Delta x^2 + \Delta t^2)$

## Physical Parameters

### Default Values (from plasma.h)

| Parameter | Default | Units | Range |
|-----------|---------|-------|-------|
| Plasma frequency | 5.3e6 | Hz | 1e6 - 1e9 |
| Collision frequency (ratio) | 0.27 | fraction of $f_p$ | 0.01 - 2.0 |
| Cyclotron frequency | 18.7 | Hz | 0 - 1e9 |
| Elevation angle | 22.0 | degrees | 0 - 90 |
| Azimuth angle | 0.0 | degrees | 0 - 360 |
| Temperature | 0.0 | K | 0 - 100,000 |
| Electron mass | 9.1066e-31 | kg | (fixed) |
| Elementary charge | -1.6022e-19 | C | (fixed) |
| Boltzmann constant | 1.3806e-23 | J/K | (fixed) |

### Reference Values

**Plasma frequency relation:**
$$f_p [\text{Hz}] = 8.98 \sqrt{n_e [\text{cm}^{-3}]}$$

**Example densities:**
- Upper ionosphere: $n_e = 10^4$ cm⁻³ → $f_p \approx 3$ MHz
- Lower ionosphere: $n_e = 10^5$ cm⁻³ → $f_p \approx 9$ MHz
- Laboratory plasma: $n_e = 10^{10}-10^{15}$ cm⁻³ → $f_p \approx 90$ MHz - 9 GHz

## References

### Primary References

1. **Taflove, A. & Hagness, S. C. (2005).** Computational Electrodynamics: The Finite-Difference Time-Domain Method, 3rd Edition. Artech House.

2. **Fridman, A. & Kennedy, L. A. (2004).** Plasma Discharges and Electronics. Taylor & Francis.

3. **Ward, J. D. (2006).** Plasma Frequency Probe Design and Implementation. [Master's Thesis]

### Additional References

4. **Goldston, R. J. & Rutherford, P. H. (1995).** Introduction to Plasma Physics. Institute of Physics Publishing.

5. **Kundu, P. K., Cohen, I. M., & Dowling, D. R. (2015).** Fluid Mechanics, 6th Edition. Academic Press.

6. **Jackson, J. D. (1998).** Classical Electrodynamics, 3rd Edition. Wiley.

---

**Last Updated:** January 2026
**Version:** 1.0
