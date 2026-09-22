"""Equivalence tests: numba kernels vs vectorized NumPy reference."""
import numpy as np
import pytest

from pic.numba_kernels import (
    HAS_NUMBA,
    boris_push_numba,
    scatter_charge_to_grid_numba,
)
from pic.boris_push import boris_push
from pic.grid_particle import scatter_charge_to_grid
from pic.pic_driver import run_pic_single_step

pytestmark = pytest.mark.skipif(not HAS_NUMBA, reason="numba not installed")


@pytest.fixture
def particles():
    rng = np.random.default_rng(1234)
    n = 2000
    return {
        "positions": rng.random((n, 3)) * 60 - 5,  # some out-of-bounds (clamp test)
        "v": rng.random((n, 3)) - 0.5,
        "q": rng.random(n) + 0.5,
        "m": rng.random(n) + 0.5,
        "E": rng.random((n, 3)) - 0.5,
        "B": rng.random(3),
        "dt": 0.1,
    }


def test_boris_push_batched_matches(particles):
    p = particles
    a = boris_push(p["q"], p["m"], p["dt"], p["v"], p["E"], p["B"])
    b = boris_push_numba(p["q"], p["m"], p["dt"], p["v"], p["E"], p["B"])
    assert a.shape == b.shape == (2000, 3)
    np.testing.assert_allclose(a, b, rtol=1e-12, atol=1e-14)


def test_boris_push_single_matches(particles):
    p = particles
    a = boris_push(-1.0, 1.0, p["dt"], p["v"][0], p["E"][0], p["B"])
    b = boris_push_numba(-1.0, 1.0, p["dt"], p["v"][0], p["E"][0], p["B"])
    assert a.shape == b.shape == (3,)
    np.testing.assert_allclose(a, b, rtol=1e-12, atol=1e-14)


def test_boris_push_scalar_qm_matches(particles):
    p = particles
    a = boris_push(-1.0, 1.0, p["dt"], p["v"], p["E"], p["B"])
    b = boris_push_numba(-1.0, 1.0, p["dt"], p["v"], p["E"], p["B"])
    np.testing.assert_allclose(a, b, rtol=1e-12, atol=1e-14)


def test_boris_push_zero_mass_raises(particles):
    p = particles
    with pytest.raises(ValueError):
        boris_push_numba(p["q"], np.zeros(2000), p["dt"], p["v"], p["E"], p["B"])


def test_scatter_matches_including_clamp(particles):
    p = particles
    a = scatter_charge_to_grid((48, 48, 48), p["positions"], p["q"])
    b = scatter_charge_to_grid_numba((48, 48, 48), p["positions"], p["q"])
    assert a.shape == b.shape == (48, 48, 48)
    np.testing.assert_array_equal(a, b)  # bit-identical
    assert a.sum() == pytest.approx(p["q"].sum())  # charge conservation


def test_scatter_empty():
    a = scatter_charge_to_grid_numba((8, 8, 8), np.zeros((0, 3)), np.zeros(0))
    assert a.shape == (8, 8, 8) and a.sum() == 0.0


def test_full_step_numba_matches_numpy(particles):
    p = particles
    kw = dict(charges=p["q"], masses=p["m"], dt=p["dt"], grid_shape=(32, 32, 32),
              E_field=p["E"], B_field=p["B"])
    r1, pos1, v1 = run_pic_single_step(p["positions"], p["v"], use_numba=False, **kw)
    r2, pos2, v2 = run_pic_single_step(p["positions"], p["v"], use_numba=True, **kw)
    np.testing.assert_array_equal(r1, r2)
    np.testing.assert_allclose(pos1, pos2, rtol=1e-12, atol=1e-14)
    np.testing.assert_allclose(v1, v2, rtol=1e-12, atol=1e-14)
