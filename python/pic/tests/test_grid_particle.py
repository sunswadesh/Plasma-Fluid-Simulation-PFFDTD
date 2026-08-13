import numpy as np
from pic.grid_particle import grid_to_particle_scalar, particle_to_grid_charge


def test_grid_particle_roundtrip():
    grid = np.zeros((6,6,6))
    xi, yj, zk = 2, 2, 2
    pi, pj, pk = 0.25, 0.5, 0.75
    q = 3.14
    w = particle_to_grid_charge(grid, xi, yj, zk, pi, pj, pk, q)
    interp = grid_to_particle_scalar(grid, xi, yj, zk, pi, pj, pk)
    # after scattering with shape functions w, gathering yields q * sum(w^2)
    expected = q * (w**2).sum()
    assert np.allclose(interp, expected, atol=1e-12)


def test_charge_conservation():
    grid = np.zeros((6,6,6))
    xi, yj, zk = 1, 1, 1
    pi, pj, pk = 0.6, 0.2, 0.9
    q = -2.5
    particle_to_grid_charge(grid, xi, yj, zk, pi, pj, pk, q)
    assert np.isclose(grid.sum(), q)


if __name__ == '__main__':
    test_grid_particle_roundtrip()
    test_charge_conservation()
    print('grid_particle tests passed')
