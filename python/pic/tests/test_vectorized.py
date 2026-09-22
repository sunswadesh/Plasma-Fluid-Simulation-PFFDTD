"""Equivalence tests: vectorized routines must match the scalar loop versions."""
import numpy as np

from pic.boris_push import boris_push
from pic.grid_particle import (
    particle_to_grid_charge,
    scatter_charge_to_grid,
)
from pic.pic_driver import run_pic_single_step


def _loop_reference_step(positions, v_half, charges, masses, dt, grid_shape):
    """Faithful re-implementation of the original per-particle loop driver."""
    rho = np.zeros(grid_shape, dtype=float)
    pos_new = positions.copy()
    v_new = v_half.copy()
    E = np.zeros(3)
    B = np.zeros(3)
    for i in range(positions.shape[0]):
        v_h = boris_push(charges[i], masses[i], dt, v_half[i], E, B)
        p = positions[i] + v_h * dt
        xi, yj, zk = int(np.floor(p[0])), int(np.floor(p[1])), int(np.floor(p[2]))
        pi, pj, pk = p[0] - xi, p[1] - yj, p[2] - zk
        particle_to_grid_charge(rho, xi, yj, zk, pi, pj, pk, charges[i])
        pos_new[i] = p
        v_new[i] = v_h
    return rho, pos_new, v_new


def _make_ensemble(seed=0, n=50):
    rng = np.random.default_rng(seed)
    positions = rng.uniform(0.5, 6.5, size=(n, 3))
    v_half = rng.normal(0, 0.5, size=(n, 3))
    charges = rng.uniform(-1.0, 1.0, size=n)
    masses = rng.uniform(0.5, 2.0, size=n)
    return positions, v_half, charges, masses


def test_boris_batched_matches_scalar():
    positions, v_half, charges, masses = _make_ensemble()
    dt = 0.05
    E = np.array([0.1, -0.2, 0.05])
    B = np.array([0.0, 0.0, 0.5])
    v_batch = boris_push(charges, masses, dt, v_half, E, B)
    for i in range(len(charges)):
        v_single = boris_push(charges[i], masses[i], dt, v_half[i], E, B)
        assert np.allclose(v_batch[i], v_single, atol=1e-12)


def test_scatter_matches_loop():
    positions, _, charges, _ = _make_ensemble()
    grid_shape = (8, 8, 8)
    rho_vec = scatter_charge_to_grid(grid_shape, positions, charges)
    rho_loop = np.zeros(grid_shape)
    for i in range(len(positions)):
        p = positions[i]
        xi, yj, zk = int(np.floor(p[0])), int(np.floor(p[1])), int(np.floor(p[2]))
        pi, pj, pk = p[0] - xi, p[1] - yj, p[2] - zk
        particle_to_grid_charge(rho_loop, xi, yj, zk, pi, pj, pk, charges[i])
    assert np.allclose(rho_vec, rho_loop, atol=1e-12)
    assert np.isclose(rho_vec.sum(), charges.sum())


def test_driver_matches_loop_reference():
    positions, v_half, charges, masses = _make_ensemble()
    dt, grid_shape = 0.05, (8, 8, 8)
    rho_v, pos_v, vel_v = run_pic_single_step(
        positions, v_half, charges, masses, dt, grid_shape)
    rho_l, pos_l, vel_l = _loop_reference_step(
        positions, v_half, charges, masses, dt, grid_shape)
    assert np.allclose(rho_v, rho_l, atol=1e-12)
    assert np.allclose(pos_v, pos_l, atol=1e-12)
    assert np.allclose(vel_v, vel_l, atol=1e-12)


def test_driver_with_fields_matches_loop():
    # per-particle E/B fields exercise the (N,3) field path
    positions, v_half, charges, masses = _make_ensemble(n=20)
    rng = np.random.default_rng(1)
    E = rng.normal(0, 0.1, size=(20, 3))
    B = rng.normal(0, 0.2, size=(20, 3))
    dt, grid_shape = 0.05, (8, 8, 8)
    rho_v, pos_v, vel_v = run_pic_single_step(
        positions, v_half, charges, masses, dt, grid_shape,
        E_field=E, B_field=B)
    v_ref = np.stack([boris_push(charges[i], masses[i], dt, v_half[i],
                                 E[i], B[i]) for i in range(20)])
    assert np.allclose(vel_v, v_ref, atol=1e-12)
    assert np.isclose(rho_v.sum(), charges.sum())
