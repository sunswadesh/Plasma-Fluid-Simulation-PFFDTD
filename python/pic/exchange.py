"""Lean FDTD <-> PIC exchange format (no .fd files in the loop).

Two files, exchanged through a shared directory (``/dev/shm`` by default
so nothing touches disk):

- ``fields.npz``  (FDTD -> PIC):  E, B as (3, nx, ny, nz) float64
- ``sources.npz`` (PIC -> FDTD):  rho as (nx, ny, nz), J as (3, nx, ny, nz)

Both carry grid metadata (shape, origin, spacing, dt, step) so either
side can sanity-check what it received. Writes are atomic (temp file +
``os.replace``) so a reader never sees a half-written file.

See docs/PIC_COUPLING.md for the full contract.
"""
import os
import time
from pathlib import Path

import numpy as np

FIELDS_FILE = "fields.npz"
SOURCES_FILE = "sources.npz"


def default_exchange_dir():
    """RAM-backed exchange dir when available, else the system temp dir."""
    for candidate in ("/dev/shm/pffdtd_coupling",):
        try:
            Path(candidate).mkdir(parents=True, exist_ok=True)
            return Path(candidate)
        except OSError:
            continue
    import tempfile
    d = Path(tempfile.mkdtemp(prefix="pffdtd_coupling_"))
    return d


def _atomic_npz(path, payload):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + f".tmp-{os.getpid()}")
    # file handle: np.savez would otherwise append ".npz" to the tmp name
    with open(tmp, "wb") as f:
        np.savez(f, **payload)
    os.replace(tmp, path)
    return path


def _meta(grid_shape, grid_origin, grid_spacing, dt, step):
    return {
        "grid_shape": np.asarray(grid_shape, dtype=np.int64),
        "grid_origin": np.asarray(grid_origin, dtype=float),
        "grid_spacing": np.asarray(grid_spacing, dtype=float),
        "dt": np.asarray(float(dt)),
        "step": np.asarray(int(step)),
    }


def write_fields(exchange_dir, E, B, grid_origin=(0, 0, 0),
                 grid_spacing=(1.0, 1.0, 1.0), dt=0.0, step=0):
    """Write FDTD -> PIC fields. E, B: (3, nx, ny, nz) float64."""
    E = np.ascontiguousarray(E, dtype=float)
    B = np.ascontiguousarray(B, dtype=float)
    if E.shape != B.shape or E.ndim != 4 or E.shape[0] != 3:
        raise ValueError("E and B must both have shape (3, nx, ny, nz)")
    payload = {"E": E, "B": B,
               **_meta(E.shape[1:], grid_origin, grid_spacing, dt, step)}
    return _atomic_npz(Path(exchange_dir) / FIELDS_FILE, payload)


def read_fields(path):
    """Read fields.npz -> dict(E, B, grid_shape, grid_origin, grid_spacing, dt, step)."""
    with np.load(path) as z:
        d = {k: z[k] for k in z.files}
    d["grid_shape"] = tuple(int(v) for v in d["grid_shape"])
    d["step"] = int(d["step"])
    d["dt"] = float(d["dt"])
    return d


def write_sources(exchange_dir, rho, J, grid_origin=(0, 0, 0),
                  grid_spacing=(1.0, 1.0, 1.0), dt=0.0, step=0):
    """Write PIC -> FDTD sources. rho: (nx, ny, nz), J: (3, nx, ny, nz)."""
    rho = np.ascontiguousarray(rho, dtype=float)
    J = np.ascontiguousarray(J, dtype=float)
    if rho.ndim != 3 or J.ndim != 4 or J.shape[0] != 3:
        raise ValueError("rho must be (nx, ny, nz), J must be (3, nx, ny, nz)")
    if J.shape[1:] != rho.shape:
        raise ValueError("J spatial shape must match rho shape")
    payload = {"rho": rho, "J": J,
               **_meta(rho.shape, grid_origin, grid_spacing, dt, step)}
    return _atomic_npz(Path(exchange_dir) / SOURCES_FILE, payload)


def read_sources(path):
    """Read sources.npz -> dict(rho, J, grid_shape, grid_origin, grid_spacing, dt, step)."""
    with np.load(path) as z:
        d = {k: z[k] for k in z.files}
    d["grid_shape"] = tuple(int(v) for v in d["grid_shape"])
    d["step"] = int(d["step"])
    d["dt"] = float(d["dt"])
    return d


def wait_for(path, timeout=30.0, poll=0.05):
    """Block until ``path`` exists; raise TimeoutError on expiry."""
    path = Path(path)
    deadline = time.monotonic() + timeout
    while not path.exists():
        if time.monotonic() > deadline:
            raise TimeoutError(f"timed out waiting for {path}")
        time.sleep(poll)
    return path
