import numpy as np


def _as_vector(a, name):
    a = np.asarray(a, dtype=float)
    if a.shape[-1] != 3 or a.ndim > 2:
        raise ValueError(f"{name} must have shape (3,) or (N, 3), got {a.shape}")
    return a


def boris_push(q, m, dt, v_prev_half, E_field, B_field):
    """Boris pusher ported from MATLAB boris_push0.m

    Vectorized over particles: ``v_prev_half`` may be shape (3,) or (N, 3);
    ``E_field``/``B_field`` may be (3,) or (N, 3); ``q``/``m`` may be scalars
    or (N,) arrays. Broadcasting follows numpy rules.

    Args:
        q: particle charge (float or array)
        m (float or array): particle mass (must be non-zero)
        dt (float): timestep
        v_prev_half: velocity at half step (previous)
        E_field: electric field vector(s)
        B_field: magnetic field vector(s)

    Returns:
        np.ndarray: v_next_half with shape (3,) for a single particle or
        (N, 3) for N particles.
    """
    v = _as_vector(v_prev_half, "v_prev_half")
    E = _as_vector(E_field, "E_field")
    B = _as_vector(B_field, "B_field")

    q = np.asarray(q, dtype=float)
    m = np.asarray(m, dtype=float)
    if np.any(m == 0):
        raise ValueError("particle mass must be non-zero")

    # (..., 1) so the scalar factor broadcasts against (..., 3) vectors
    factor = (q * dt / (2.0 * m))[..., None]

    v_minus = v + factor * E

    T = factor * B
    T_sq = np.einsum("...i,...i->...", T, T)
    S = 2.0 * T / (1.0 + T_sq)[..., None]

    v_prime = v_minus + np.cross(v_minus, T)
    v_plus = v_minus + np.cross(v_prime, S)

    v_next_half = v_plus + factor * E

    return v_next_half

if __name__ == "__main__":
    # quick smoke test
    q = -1.0
    m = 1.0
    dt = 0.1
    v0 = np.array([1.0, 0.0, 0.0])
    E = np.array([0.0, 0.0, 0.0])
    B = np.array([0.0, 0.0, 0.1])
    print(boris_push(q, m, dt, v0, E, B))
