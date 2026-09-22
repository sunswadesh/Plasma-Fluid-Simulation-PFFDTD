"""Benchmark: original per-particle loop vs vectorized push + deposition."""
import time

import numpy as np

from pic.boris_push import boris_push
from pic.grid_particle import particle_to_grid_charge
from pic.pic_driver import run_pic_single_step


def loop_step(positions, v_half, charges, masses, dt, grid_shape):
    rho = np.zeros(grid_shape, dtype=float)
    pos_new = positions.copy()
    v_new = v_half.copy()
    E = np.zeros(3)
    B = np.zeros(3)
    for i in range(positions.shape[0]):
        v_h = boris_push(charges[i], masses[i], dt, v_half[i], E, B)
        p = positions[i] + v_h * dt
        xi, yj, zk = (int(np.floor(c)) for c in p)
        pi, pj, pk = p[0] - xi, p[1] - yj, p[2] - zk
        particle_to_grid_charge(rho, xi, yj, zk, pi, pj, pk, charges[i])
        pos_new[i] = p
        v_new[i] = v_h
    return rho, pos_new, v_new


def timeit(fn, repeats):
    best = float("inf")
    for _ in range(repeats):
        t0 = time.perf_counter()
        fn()
        best = min(best, time.perf_counter() - t0)
    return best


def main(n=20000, repeats=3):
    rng = np.random.default_rng(0)
    positions = rng.uniform(0.5, 62.5, size=(n, 3))
    v_half = rng.normal(0, 0.5, size=(n, 3))
    charges = rng.uniform(-1.0, 1.0, size=n)
    masses = np.ones(n)
    dt, grid_shape = 0.05, (64, 64, 64)

    run_pic_single_step(positions, v_half, charges, masses, dt, grid_shape)  # warm up

    t_loop = timeit(lambda: loop_step(positions, v_half, charges, masses, dt, grid_shape), repeats)
    t_vec = timeit(lambda: run_pic_single_step(positions, v_half, charges, masses, dt, grid_shape), repeats)
    print(f"particles : {n}")
    print(f"loop      : {t_loop:.3f} s")
    print(f"vectorized: {t_vec:.3f} s")
    print(f"speedup   : {t_loop / t_vec:.1f}x")


if __name__ == "__main__":
    main()
