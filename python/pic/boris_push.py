import numpy as np

def boris_push(q, m, dt, v_prev_half, E_field, B_field):
    """Boris pusher ported from MATLAB boris_push0.m

    Args:
        q (float): particle charge
        m (float): particle mass
        dt (float): timestep
        v_prev_half (array-like, shape (3,)): velocity at half step (previous)
        E_field (array-like, shape (3,)): electric field vector
        B_field (array-like, shape (3,)): magnetic field vector

    Returns:
        np.ndarray: v_next_half (3,)
    """
    v_prev_half = np.asarray(v_prev_half, dtype=float).reshape(3)
    E_field = np.asarray(E_field, dtype=float).reshape(3)
    B_field = np.asarray(B_field, dtype=float).reshape(3)

    v_minus = v_prev_half + (q * dt / (2.0 * m)) * E_field

    T = (q * dt / (2.0 * m)) * B_field
    T_sq = np.dot(T, T)
    S = 2 * T / (1 + T_sq)

    v_prime = v_minus + np.cross(v_minus, T)
    v_plus = v_minus + np.cross(v_prime, S)

    v_next_half = v_plus + (q * dt / (2.0 * m)) * E_field

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
