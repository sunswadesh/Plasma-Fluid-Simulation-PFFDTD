import numpy as np
from .boris_push import boris_push
from .grid_particle import particle_to_grid_charge


def run_pic_single_step(positions, v_half, charges, masses, dt, grid_shape, grid_origin=(0,0,0), grid_spacing=(1.0,1.0,1.0)):
    """Run a simple file-coupled PIC single step.

    - positions: (N,3) array of particle positions
    - v_half: (N,3) velocities at half-step
    - charges: (N,) particle charges
    - masses: (N,) particle masses
    - dt: timestep
    - grid_shape: (nx,ny,nz)
    - grid_origin: world coords of grid (defaults to 0)
    - grid_spacing: cell sizes (dx,dy,dz)

    Returns:
      rho: charge density grid (same shape as grid_shape)
      positions_new: updated positions after full step
      v_half_new: updated half-step velocities
    """
    positions = np.asarray(positions, dtype=float)
    v_half = np.asarray(v_half, dtype=float)
    charges = np.asarray(charges, dtype=float)
    masses = np.asarray(masses, dtype=float)

    nx, ny, nz = grid_shape
    dx, dy, dz = grid_spacing
    ox, oy, oz = grid_origin

    rho = np.zeros(grid_shape, dtype=float)

    positions_new = positions.copy()
    v_half_new = v_half.copy()

    N = positions.shape[0]
    for i in range(N):
        pos = positions[i]
        v_h = v_half[i]
        q = charges[i]
        m = masses[i]

        # push velocity one step (Boris pusher requires E & B; we use zero E/B here placeholder)
        E = np.zeros(3)
        B = np.zeros(3)
        v_h_new = boris_push(q, m, dt, v_h, E, B)

        # update position using v_h_new (full step)
        pos_new = pos + v_h_new * dt

        # convert world position to grid indices and fractional coords
        x_rel = (pos_new[0] - ox) / dx
        y_rel = (pos_new[1] - oy) / dy
        z_rel = (pos_new[2] - oz) / dz

        # base index (lower corner)
        xi = int(np.floor(x_rel))
        yj = int(np.floor(y_rel))
        zk = int(np.floor(z_rel))

        pi = x_rel - xi
        pj = y_rel - yj
        pk = z_rel - zk

        # scatter charge to grid
        particle_to_grid_charge(rho, xi, yj, zk, pi, pj, pk, q)

        positions_new[i] = pos_new
        v_half_new[i] = v_h_new

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
