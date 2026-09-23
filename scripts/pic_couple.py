"""PIC half of the lean FDTD <-> PIC coupling loop (contract v1).

See docs/PIC_COUPLING.md.

Flow:
  1. read fields.npz from the exchange dir (E, B + grid metadata);
     fall back to zero fields when absent (demo mode)
  2. load particle state (particles.npz) or initialize a synthetic ensemble
  3. gather E/B to particle positions (numba)
  4. Boris push + position update + deposit rho and J (numba)
  5. atomically write sources.npz and the updated particle state

Chainable: run once per coupling step with --step k; particle state
persists in the exchange dir between invocations.
"""
import argparse
import os
import time
from pathlib import Path

import numpy as np

from pic.exchange import (
    FIELDS_FILE,
    default_exchange_dir,
    read_fields,
    write_sources,
)
from pic.numba_kernels import HAS_NUMBA, gather_field_to_particles
from pic.pic_driver import run_pic_single_step

PARTICLES_FILE = "particles.npz"
STOP_FILE = "stop"


def init_particles(n, grid_shape, grid_origin, grid_spacing, seed=0):
    rng = np.random.default_rng(seed)
    lo = np.asarray(grid_origin, dtype=float)
    span = np.asarray(grid_spacing, dtype=float) * (np.asarray(grid_shape, dtype=float) - 2)
    positions = lo + rng.random((n, 3)) * span
    v_half = np.zeros((n, 3))
    charges = np.full(n, 1.0 / n)
    masses = np.ones(n)
    return positions, v_half, charges, masses


def load_particles(path):
    with np.load(path) as z:
        return z["positions"], z["v_half"], z["charges"], z["masses"]


def save_particles(path, positions, v_half, charges, masses):
    tmp = path.with_name(path.name + ".tmp")
    # file handle: np.savez would otherwise append ".npz" to the tmp name
    with open(tmp, "wb") as f:
        np.savez(f, positions=positions, v_half=v_half,
                 charges=charges, masses=masses)
    tmp.replace(path)


def warm_up():
    """Trigger JIT compilation once so coupled steps never pay for it."""
    if not HAS_NUMBA:
        return
    pos = np.zeros((1, 3))
    E = np.zeros((3, 2, 2, 2))
    gather_field_to_particles(E, pos)
    run_pic_single_step(pos, np.zeros((1, 3)), np.ones(1), np.ones(1),
                        0.1, (2, 2, 2), return_current=True)


def couple_one_step(exdir, step, particles, fields=None, verbose=True):
    """Run a single coupling step. Returns (timing_dict, updated particles).

    fields: dict from read_fields(), or None for zero-field demo mode.
    particles: (positions, v_half, charges, masses) or None to initialize.
    """
    t0 = time.perf_counter()
    if fields is None:
        grid_shape = (64, 64, 8)
        origin, spacing, dt = (0.0, 0.0, 0.0), (1.0, 1.0, 1.0), 0.1
        E = np.zeros((3,) + grid_shape)
        B = np.zeros((3,) + grid_shape)
    else:
        E, B = fields["E"], fields["B"]
        grid_shape = fields["grid_shape"]
        origin, spacing, dt = (fields["grid_origin"], fields["grid_spacing"],
                              fields["dt"])

    if particles is None:
        raise ValueError("particles must be provided (call init_particles)")

    positions, v_half, charges, masses = particles
    t1 = time.perf_counter()
    E_part = gather_field_to_particles(E, positions, origin, spacing)
    B_part = gather_field_to_particles(B, positions, origin, spacing)
    t2 = time.perf_counter()

    rho, pos_new, v_new, J = run_pic_single_step(
        positions, v_half, charges, masses, dt, grid_shape,
        grid_origin=origin, grid_spacing=spacing,
        E_field=E_part, B_field=B_part, return_current=True)
    t3 = time.perf_counter()

    write_sources(exdir, rho, J, grid_origin=origin, grid_spacing=spacing,
                  dt=dt, step=step)
    save_particles(exdir / PARTICLES_FILE, pos_new, v_new, charges, masses)
    t4 = time.perf_counter()

    if verbose:
        print(f"step {step}: rho.sum()={rho.sum():.6f} "
              f"Jsum=({J[0].sum():.3e},{J[1].sum():.3e},{J[2].sum():.3e})")
        print(f"timing: setup={(t1-t0)*1e3:.1f}ms gather={(t2-t1)*1e3:.1f}ms "
              f"pic={(t3-t2)*1e3:.1f}ms write={(t4-t3)*1e3:.1f}ms")
    return {"setup": t1 - t0, "gather": t2 - t1,
            "pic": t3 - t2, "write": t4 - t3}, (pos_new, v_new, charges, masses)


def serve(exdir, poll_interval=0.02, max_steps=None):
    """Persistent worker: JIT once, then serve coupling steps until stopped.

    Watches fields.npz; whenever it carries a step newer than the last
    one processed, runs the coupling iteration and writes sources.npz.
    Stop by creating <exdir>/stop or with Ctrl-C.
    """
    print(f"PIC worker serving {exdir} (numba={'on' if HAS_NUMBA else 'off'})")
    t0 = time.perf_counter()
    warm_up()
    print(f"JIT warm-up: {(time.perf_counter()-t0)*1e3:.0f}ms (one-time cost)")

    exdir = Path(exdir)
    fields_path = exdir / FIELDS_FILE
    particles_path = exdir / PARTICLES_FILE
    particles = load_particles(particles_path) if particles_path.exists() else None
    last_step = -1
    steps_done = 0
    while True:
        if (exdir / STOP_FILE).exists():
            print("stop file seen; exiting")
            return
        if max_steps is not None and steps_done >= max_steps:
            return
        if not fields_path.exists():
            time.sleep(poll_interval)
            continue
        try:
            fields = read_fields(fields_path)
        except Exception:
            time.sleep(poll_interval)  # half-written file; retry
            continue
        step = fields["step"]
        if step <= last_step:
            time.sleep(poll_interval)
            continue
        if particles is None:
            n = int(os.environ.get("PIC_PARTICLES", "1000"))
            particles = init_particles(n, fields["grid_shape"],
                                       fields["grid_origin"],
                                       fields["grid_spacing"])
            print(f"initialized {n} particles")
        timing, particles = couple_one_step(exdir, step, particles,
                                            fields, verbose=True)
        last_step = step
        steps_done += 1


def main():
    ap = argparse.ArgumentParser(description="PIC side of the lean coupling loop")
    ap.add_argument("--exchange-dir", default=str(default_exchange_dir()))
    ap.add_argument("--step", type=int, default=0)
    ap.add_argument("--particles", type=int, default=1000)
    ap.add_argument("--grid-shape", type=int, nargs=3, default=(64, 64, 8))
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--serve", action="store_true",
                    help="run as a persistent worker instead of a single step")
    ap.add_argument("--poll-interval", type=float, default=0.02)
    ap.add_argument("--max-steps", type=int, default=None)
    args = ap.parse_args()

    exdir = Path(args.exchange_dir)
    exdir.mkdir(parents=True, exist_ok=True)

    if args.serve:
        serve(exdir, args.poll_interval, args.max_steps)
        return

    warm_up()
    fields_path = exdir / FIELDS_FILE
    fields = None
    if fields_path.exists():
        fields = read_fields(fields_path)
        if fields["step"] != args.step:
            print(f"warning: fields.npz step={fields['step']} != requested "
                  f"step={args.step}; using it anyway")
        print(f"read {FIELDS_FILE} step={fields['step']} grid={fields['grid_shape']}")
    else:
        print(f"no {FIELDS_FILE}; demo mode with zero fields")

    ppath = exdir / PARTICLES_FILE
    if ppath.exists():
        particles = load_particles(ppath)
        print(f"resumed {particles[0].shape[0]} particles from {PARTICLES_FILE}")
    else:
        gs = fields["grid_shape"] if fields else tuple(args.grid_shape)
        go = fields["grid_origin"] if fields else (0.0, 0.0, 0.0)
        sp = fields["grid_spacing"] if fields else (1.0, 1.0, 1.0)
        particles = init_particles(args.particles, gs, go, sp, seed=args.seed)
        print(f"initialized {args.particles} particles")

    couple_one_step(exdir, args.step, particles, fields)
    print("wrote sources.npz +", PARTICLES_FILE)


if __name__ == "__main__":
    main()
