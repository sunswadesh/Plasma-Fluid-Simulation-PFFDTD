"""Round-trip tests for the lean FDTD<->PIC exchange format."""
import numpy as np

from pic.exchange import (
    read_fields,
    read_sources,
    write_fields,
    write_sources,
)


def test_fields_roundtrip(tmp_path):
    rng = np.random.default_rng(3)
    E = rng.random((3, 8, 8, 8))
    B = rng.random((3, 8, 8, 8))
    p = write_fields(tmp_path, E, B, grid_origin=(1, 2, 3),
                     grid_spacing=(0.5, 0.5, 0.5), dt=0.1, step=7)
    assert p.name == "fields.npz"
    d = read_fields(p)
    np.testing.assert_array_equal(d["E"], E)
    np.testing.assert_array_equal(d["B"], B)
    assert d["grid_shape"] == (8, 8, 8)
    assert d["step"] == 7 and d["dt"] == 0.1
    np.testing.assert_array_equal(d["grid_origin"], [1, 2, 3])


def test_sources_roundtrip(tmp_path):
    rng = np.random.default_rng(5)
    rho = rng.random((8, 8, 8))
    J = rng.random((3, 8, 8, 8))
    p = write_sources(tmp_path, rho, J, step=7)
    assert p.name == "sources.npz"
    d = read_sources(p)
    np.testing.assert_array_equal(d["rho"], rho)
    np.testing.assert_array_equal(d["J"], J)
    assert d["grid_shape"] == (8, 8, 8)
    assert d["step"] == 7
