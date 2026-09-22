"""Numba-accelerated kernels for the PIC hot spots.

These are drop-in faster equivalents of the vectorized NumPy paths in
``boris_push`` and ``grid_particle``. Each kernel fuses the whole
per-particle computation into a single loop (no (N,3)/(N,8) temporaries)
and, where race-free, runs it in parallel via ``prange``.

If numba is unavailable, the import sets ``HAS_NUMBA = False`` and callers
should fall back to the NumPy implementations.
"""

import numpy as np

try:
    from numba import njit, prange

    HAS_NUMBA = True
except ImportError:  # pragma: no cover
    HAS_NUMBA = False

    def njit(*a, **k):  # type: ignore
        def deco(f):
            return f

        return deco

    def prange(*a):  # type: ignore
        return range(*a)


# Corner offsets matching grid_particle._CORNER_OFFSETS ordering:
# (0,0,0), (0,1,0), (1,0,0), (0,0,1), (1,1,0), (1,0,1), (0,1,1), (1,1,1)
@njit(cache=True)
def _boris_push_kernel(v_out, q, m, dt, v, E, B, E_is_uniform, B_is_uniform,
                       q_is_scalar, m_is_scalar):
    """Fused Boris push over particles.

    All array args are (N,3) except q/m which are (N,) unless the
    corresponding *_is_scalar flag is set (then only element 0 is read).
    E/B are either (N,3) or (1,3) uniform fields (flag selects row 0).
    Writes v_next_half into v_out (N,3).
    """
    n = v.shape[0]
    for p in prange(n):
        qq = q[0] if q_is_scalar else q[p]
        mm = m[0] if m_is_scalar else m[p]
        ex = E[0, 0] if E_is_uniform else E[p, 0]
        ey = E[0, 1] if E_is_uniform else E[p, 1]
        ez = E[0, 2] if E_is_uniform else E[p, 2]
        bx = B[0, 0] if B_is_uniform else B[p, 0]
        by = B[0, 1] if B_is_uniform else B[p, 1]
        bz = B[0, 2] if B_is_uniform else B[p, 2]

        factor = qq * dt / (2.0 * mm)

        # v_minus = v + factor * E
        vmx = v[p, 0] + factor * ex
        vmy = v[p, 1] + factor * ey
        vmz = v[p, 2] + factor * ez

        # T = factor * B ; S = 2*T / (1 + |T|^2)
        tx = factor * bx
        ty = factor * by
        tz = factor * bz
        t_sq = tx * tx + ty * ty + tz * tz
        s_scale = 2.0 / (1.0 + t_sq)
        sx = tx * s_scale
        sy = ty * s_scale
        sz = tz * s_scale

        # v_prime = v_minus + cross(v_minus, T)
        vpx = vmx + (vmy * tz - vmz * ty)
        vpy = vmy + (vmz * tx - vmx * tz)
        vpz = vmz + (vmx * ty - vmy * tx)

        # v_plus = v_minus + cross(v_prime, S)
        vpx2 = vmx + (vpy * sz - vpz * sy)
        vpy2 = vmy + (vpz * sx - vpx * sz)
        vpz2 = vmz + (vpx * sy - vpy * sx)

        v_out[p, 0] = vpx2 + factor * ex
        v_out[p, 1] = vpy2 + factor * ey
        v_out[p, 2] = vpz2 + factor * ez


@njit(cache=True)
def _scatter_kernel(rho, px, py, pz, charges, ox, oy, oz, sx, sy, sz,
                    nx, ny, nz):
    """Fused charge deposition.

    Serial loop (scatter to shared grid nodes cannot run in parallel
    without atomics). Computes base indices, fractions and the 8
    trilinear weights on the fly per particle -- no (N,8) temporaries.
    Clamping matches ``grid_particle._base_indices_and_fractions``:
    base indices are clamped to [0, n-2] per axis.
    """
    n = px.shape[0]
    for p in range(n):
        # world -> grid coords
        rx = (px[p] - ox) / sx
        ry = (py[p] - oy) / sy
        rz = (pz[p] - oz) / sz
        bx = int(np.floor(rx))
        by = int(np.floor(ry))
        bz = int(np.floor(rz))
        fx = rx - bx
        fy = ry - by
        fz = rz - bz
        # clamp base so base+1 stays in-bounds
        if bx < 0:
            bx = 0
        elif bx > nx - 2:
            bx = nx - 2
        if by < 0:
            by = 0
        elif by > ny - 2:
            by = ny - 2
        if bz < 0:
            bz = 0
        elif bz > nz - 2:
            bz = nz - 2

        q = charges[p]
        # 8 trilinear weights, corner ordering matches _CORNER_OFFSETS
        w0 = (1 - fx) * (1 - fy) * (1 - fz)
        w1 = (1 - fx) * fy * (1 - fz)
        w2 = fx * (1 - fy) * (1 - fz)
        w3 = (1 - fx) * (1 - fy) * fz
        w4 = fx * fy * (1 - fz)
        w5 = fx * (1 - fy) * fz
        w6 = (1 - fx) * fy * fz
        w7 = fx * fy * fz

        rho[bx, by, bz] += q * w0
        rho[bx, by + 1, bz] += q * w1
        rho[bx + 1, by, bz] += q * w2
        rho[bx, by, bz + 1] += q * w3
        rho[bx + 1, by + 1, bz] += q * w4
        rho[bx + 1, by, bz + 1] += q * w5
        rho[bx, by + 1, bz + 1] += q * w6
        rho[bx + 1, by + 1, bz + 1] += q * w7


def boris_push_numba(q, m, dt, v_prev_half, E_field, B_field):
    """Numba version of :func:`pic.boris_push.boris_push`.

    Same broadcasting semantics and return shape. Raises the same
    ValueErrors for bad shapes / zero mass.
    """
    from .boris_push import _as_vector

    v = _as_vector(v_prev_half, "v_prev_half")
    E = _as_vector(E_field, "E_field")
    B = _as_vector(B_field, "B_field")
    q = np.asarray(q, dtype=float)
    m = np.asarray(m, dtype=float)
    if np.any(m == 0):
        raise ValueError("particle mass must be non-zero")

    single = (v.ndim == 1)
    vv = v.reshape(-1, 3)
    n = vv.shape[0]

    def expand(a, name):
        a = np.asarray(a, dtype=float)
        if a.ndim == 0:
            return np.full(n, a), True
        a = a.reshape(-1)
        if a.shape[0] == 1:
            return np.full(n, a[0]), True
        if a.shape[0] != n:
            raise ValueError(f"{name} length {a.shape[0]} != particle count {n}")
        return a, False

    qq, q_scalar = expand(q, "q")
    mm, m_scalar = expand(m, "m")

    EE = E.reshape(-1, 3)
    BB = B.reshape(-1, 3)
    E_uni = EE.shape[0] == 1
    B_uni = BB.shape[0] == 1
    if not E_uni and EE.shape[0] != n:
        raise ValueError("E_field particle count mismatch")
    if not B_uni and BB.shape[0] != n:
        raise ValueError("B_field particle count mismatch")

    out = np.empty((n, 3), dtype=float)
    _boris_push_kernel(out, qq, mm, float(dt), np.ascontiguousarray(vv),
                       np.ascontiguousarray(EE), np.ascontiguousarray(BB),
                       E_uni, B_uni, q_scalar, m_scalar)
    return out[0] if single else out


def scatter_charge_to_grid_numba(grid_shape, positions, charges,
                                 grid_origin=(0, 0, 0),
                                 grid_spacing=(1.0, 1.0, 1.0)):
    """Numba version of :func:`pic.grid_particle.scatter_charge_to_grid`.

    Identical clamping/weight semantics; much faster than ``np.add.at``.
    """
    positions = np.ascontiguousarray(positions, dtype=float).reshape(-1, 3)
    charges = np.ascontiguousarray(charges, dtype=float).reshape(-1)
    if positions.shape[0] != charges.shape[0]:
        raise ValueError("positions and charges must have the same particle count")
    origin = np.asarray(grid_origin, dtype=float).reshape(3)
    spacing = np.asarray(grid_spacing, dtype=float).reshape(3)
    if np.any(spacing == 0):
        raise ValueError("grid_spacing must be non-zero")

    nx, ny, nz = (int(n) for n in grid_shape)
    rho = np.zeros((nx, ny, nz), dtype=float)
    if positions.shape[0] == 0:
        return rho
    _scatter_kernel(rho, positions[:, 0], positions[:, 1], positions[:, 2],
                    charges, origin[0], origin[1], origin[2],
                    spacing[0], spacing[1], spacing[2], nx, ny, nz)
    return rho
