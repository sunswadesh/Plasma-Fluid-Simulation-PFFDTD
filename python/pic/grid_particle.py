import numpy as np
from .weighting import g2p_weight


def compute_trilinear_weights(pi, pj, pk):
    """Return the 8 trilinear shape-function weights for fractional coords.

    Ordering matches `g2p_weight` and the corner list used below.
    """
    w1 = (1 - pi) * (1 - pj) * (1 - pk)
    w2 = (1 - pi) * pj * (1 - pk)
    w3 = pi * (1 - pj) * (1 - pk)
    w4 = (1 - pi) * (1 - pj) * pk
    w5 = pi * pj * (1 - pk)
    w6 = pi * (1 - pj) * pk
    w7 = (1 - pi) * pj * pk
    w8 = pi * pj * pk
    return np.array([w1, w2, w3, w4, w5, w6, w7, w8], dtype=float)


# Corner offsets matching the ordering used by g2p_weight /
# compute_trilinear_weights: (0,0,0), (0,1,0), (1,0,0), (0,0,1),
# (1,1,0), (1,0,1), (0,1,1), (1,1,1)
_CORNER_OFFSETS = np.array(
    [
        [0, 0, 0],
        [0, 1, 0],
        [1, 0, 0],
        [0, 0, 1],
        [1, 1, 0],
        [1, 0, 1],
        [0, 1, 1],
        [1, 1, 1],
    ],
    dtype=np.intp,
)


def _base_indices_and_fractions(positions, grid_shape, grid_origin, grid_spacing):
    """Map (N,3) world positions to clamped base indices and fractions.

    Base indices are clamped to [0, n-2] per axis so that base+1 stays
    in-bounds, mirroring the scalar clamping behavior below.
    """
    positions = np.asarray(positions, dtype=float).reshape(-1, 3)
    origin = np.asarray(grid_origin, dtype=float).reshape(3)
    spacing = np.asarray(grid_spacing, dtype=float).reshape(3)
    if np.any(spacing == 0):
        raise ValueError("grid_spacing must be non-zero")

    rel = (positions - origin) / spacing
    base = np.floor(rel).astype(np.intp)
    frac = rel - base
    n = np.asarray(grid_shape, dtype=np.intp).reshape(3)
    base = np.clip(base, 0, n - 2)
    return base, frac


def trilinear_weights_vec(frac):
    """Vectorized shape-function weights.

    Args:
        frac: (N, 3) fractional coords in [0, 1].

    Returns:
        (N, 8) weight array with the same corner ordering as
        `compute_trilinear_weights`.
    """
    frac = np.asarray(frac, dtype=float).reshape(-1, 3)
    fi, fj, fk = frac[:, 0], frac[:, 1], frac[:, 2]
    w = np.empty((frac.shape[0], 8), dtype=float)
    w[:, 0] = (1 - fi) * (1 - fj) * (1 - fk)
    w[:, 1] = (1 - fi) * fj * (1 - fk)
    w[:, 2] = fi * (1 - fj) * (1 - fk)
    w[:, 3] = (1 - fi) * (1 - fj) * fk
    w[:, 4] = fi * fj * (1 - fk)
    w[:, 5] = fi * (1 - fj) * fk
    w[:, 6] = (1 - fi) * fj * fk
    w[:, 7] = fi * fj * fk
    return w


def scatter_charge_to_grid(grid_shape, positions, charges,
                           grid_origin=(0, 0, 0), grid_spacing=(1.0, 1.0, 1.0)):
    """Deposit particle charges onto a grid (vectorized).

    Replaces the per-particle loop over `particle_to_grid_charge` with a
    single ``np.add.at`` scatter. Repeated node hits from different
    particles accumulate correctly.

    Args:
        grid_shape: (nx, ny, nz) tuple.
        positions: (N, 3) particle positions in world coordinates.
        charges: (N,) particle charges.
        grid_origin: world coords of grid origin.
        grid_spacing: cell sizes (dx, dy, dz).

    Returns:
        np.ndarray: charge density grid of shape `grid_shape`.
    """
    positions = np.asarray(positions, dtype=float).reshape(-1, 3)
    charges = np.asarray(charges, dtype=float).reshape(-1)
    if positions.shape[0] != charges.shape[0]:
        raise ValueError("positions and charges must have the same particle count")

    rho = np.zeros(tuple(int(n) for n in grid_shape), dtype=float)
    if positions.shape[0] == 0:
        return rho

    base, frac = _base_indices_and_fractions(positions, grid_shape,
                                             grid_origin, grid_spacing)
    w = trilinear_weights_vec(frac)  # (N, 8)
    idx = base[:, None, :] + _CORNER_OFFSETS[None, :, :]  # (N, 8, 3)
    np.add.at(rho,
              (idx[..., 0], idx[..., 1], idx[..., 2]),
              charges[:, None] * w)
    return rho


def grid_to_particle_scalar(grid, xi, yj, zk, pi, pj, pk):
    """Interpolate scalar grid value to particle using trilinear weights.

    xi, yj, zk are integer base indices (0-based) of the "lower" corner.
    pi,pj,pk are fractional distances [0,1] inside the cell.
    """
    nx, ny, nz = grid.shape
    # clamp indices to valid range for corner access
    xi = int(max(0, min(xi, nx - 2)))
    yj = int(max(0, min(yj, ny - 2)))
    zk = int(max(0, min(zk, nz - 2)))

    vals = g2p_weight(grid, xi, yj, zk, pi, pj, pk)
    return vals.sum()


def particle_to_grid_charge(grid, xi, yj, zk, pi, pj, pk, q):
    """Scatter particle charge q to the 8 surrounding grid nodes in-place.

    Arguments same as `grid_to_particle_scalar`. Mutates `grid`.
    Returns the weights used (length-8 array).
    """
    nx, ny, nz = grid.shape
    xi = int(max(0, min(xi, nx - 2)))
    yj = int(max(0, min(yj, ny - 2)))
    zk = int(max(0, min(zk, nz - 2)))

    w = compute_trilinear_weights(pi, pj, pk)
    # indices for the 8 corners (matching ordering in g2p_weight)
    corners = [
        (xi, yj, zk),
        (xi, yj + 1, zk),
        (xi + 1, yj, zk),
        (xi, yj, zk + 1),
        (xi + 1, yj + 1, zk),
        (xi + 1, yj, zk + 1),
        (xi, yj + 1, zk + 1),
        (xi + 1, yj + 1, zk + 1),
    ]
    for wt, (ix, iy, iz) in zip(w, corners):
        # guard in-bound (should be within due to clamping)
        if 0 <= ix < nx and 0 <= iy < ny and 0 <= iz < nz:
            grid[ix, iy, iz] += q * wt

    return w


if __name__ == "__main__":
    # quick smoke demo
    grid = np.zeros((10, 10, 10))
    xi, yj, zk = 4, 4, 4
    pi, pj, pk = 0.3, 0.4, 0.2
    q = 1.0
    w = particle_to_grid_charge(grid, xi, yj, zk, pi, pj, pk, q)
    interp = grid_to_particle_scalar(grid, xi, yj, zk, pi, pj, pk)
    print('weights:', w)
    print('recovered:', interp)
