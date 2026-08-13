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
