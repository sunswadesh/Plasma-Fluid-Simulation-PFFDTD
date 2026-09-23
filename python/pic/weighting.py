import numpy as np


def g2p_weight(array_in, x_i, y_j, z_k, p_i, p_j, p_k):
    """Tri-linear weighting from grid to particle (port of G2P_Weight.m)

    Returns the 8 corner contributions as a 1D array (length 8).
    """
    # Assumes array_in is a NumPy 3D array with shape (nx, ny, nz)
    # x_i, y_j, z_k are integer cell indices (1-based in MATLAB). We'll expect 0-based here.
    A1 = array_in[x_i, y_j, z_k] * (1 - p_i) * (1 - p_j) * (1 - p_k)
    A2 = array_in[x_i, y_j + 1, z_k] * (1 - p_i) * p_j * (1 - p_k)
    A3 = array_in[x_i + 1, y_j, z_k] * p_i * (1 - p_j) * (1 - p_k)
    A4 = array_in[x_i, y_j, z_k + 1] * (1 - p_i) * (1 - p_j) * p_k
    A5 = array_in[x_i + 1, y_j + 1, z_k] * p_i * p_j * (1 - p_k)
    A6 = array_in[x_i + 1, y_j, z_k + 1] * p_i * (1 - p_j) * p_k
    A7 = array_in[x_i, y_j + 1, z_k + 1] * (1 - p_i) * p_j * p_k
    A8 = array_in[x_i + 1, y_j + 1, z_k + 1] * p_i * p_j * p_k

    return np.array([A1, A2, A3, A4, A5, A6, A7, A8], dtype=float)
