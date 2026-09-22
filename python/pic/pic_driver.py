import numpy as np
from .boris_push import boris_push
from .grid_particle import scatter_charge_to_grid
from .numba_kernels import (
    HAS_NUMBA,
    boris_push_numba,
    scatter_charge_to_grid_numba,
)


def run_pic_single_step(positions, v_half, charges, masses, dt, grid_shape,
                        grid_origin=(0, 0, 0), grid_spacing=(1.0, 1.0, 1.0),
                        E_field=None, B_field=None, use_numba=HAS_NUMBA):
    """Run a simple file-coupled PIC single step (vectorized).

    - positions: (N,3) array of particle positions
    - v_half: (N,3) velocities at half-step
    - charges: (N,) particle charges
    - masses: (N,) particle masses
    - dt: timestep
    - grid_shape: (nx,ny,nz)
    - grid_origin: world coords of grid (defaults to 0)
    - grid_spacing: cell sizes (dx,dy,dz)
    - E_field: (3,) or (N,3) electric field (defaults to zero)
    - B_field: (3,) or (N,3) magnetic field (defaults to zero)

    Returns:
      rho: charge density grid (same shape as grid_shape)
      positions_new: updated positions after full step
      v_half_new: updated half-step velocities

    use_numba: if True (default when numba is installed), use the fused
      numba kernels for the Boris push and charge deposition; otherwise
      fall back to the vectorized NumPy paths.
    """
    positions = np.asarray(positions, dtype=float).reshape(-1, 3)
    v_half = np.asarray(v_half, dtype=float).reshape(-1, 3)
    charges = np.asarray(charges, dtype=float).reshape(-1)
    masses = np.asarray(masses, dtype=float).reshape(-1)
    n = positions.shape[0]
    if not (v_half.shape[0] == charges.shape[0] == masses.shape[0] == n):
        raise ValueError("positions, v_half, charges and masses must agree on N")

    if E_field is None:
        E_field = np.zeros(3)
    if B_field is None:
        B_field = np.zeros(3)

    push = boris_push_numba if use_numba else boris_push
    scatter = scatter_charge_to_grid_numba if use_numba else scatter_charge_to_grid

    # Boris push for all particles at once
    v_half_new = push(charges, masses, dt, v_half, E_field, B_field)

    # position update (full step from half-step velocity)
    positions_new = positions + v_half_new * dt

    # charge deposition
    rho = scatter(grid_shape, positions_new, charges,
                  grid_origin, grid_spacing)

    return rho, positions_new, v_half_new


if __name__ == "__main__":
    # tiny integration demo: 10 particles in a small box
    N = 10
    positions = np.random.rand(N,3) * 4.0 + 1.0
    v_half = np.zeros((N,3))
    charges = np.ones(N) * 1.0
    masses = np.ones(N) * 1.0
    dt = 0.1
    rho, pos_new, v_half_new = run_pic_single_step(positions, v_half, charges, masses, dt, (8,8,8), grid_origin=(0,0,0), grid_spacing=(1,1,1))
    print('rho sum:', rho.sum())
    np.savez('python/pic/examples/pic_step_output.npz', rho=rho, positions=pos_new, v_half=v_half_new)
    print('Wrote python/pic/examples/pic_step_output.npz')
