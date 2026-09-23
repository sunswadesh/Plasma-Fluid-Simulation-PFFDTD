"""Orchestrator for file-based coupling between pffdtd and Python PIC.

By default this script does NOT run the `pffdtd` executable (respect the user's request).
Use `--run-fdtd` to allow the script to execute the FDTD binary (not recommended without verification).

Workflow (default):
- Load fields from a provided `.fd` file using `visualization.pffdtd_loader` if available.
- Construct a small particle ensemble (or load particles from an input file).
- Call `pic.pic_driver.run_pic_single_step` to compute charge density `rho`.
- Save coupling outputs to an `.npz` file that `pffdtd` can be modified to read.
"""
import argparse
import subprocess
import sys
import numpy as np

from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description='PIC<->FDTD file-based orchestrator (no automatic pffdtd run).')
    parser.add_argument('--fd-file', type=str, default=None, help='Path to .fd file produced by pffdtd')
    parser.add_argument('--out', type=str, default='coupling_currents.npz', help='Output coupling file (.npz)')
    parser.add_argument('--run-fdtd', action='store_true', help='If set, run the pffdtd exe before coupling (disabled by default)')
    parser.add_argument('--fdtd-cmd', type=str, default='pffdtd', help='Command to run the pffdtd executable')
    args = parser.parse_args()

    if args.run_fdtd:
        print('Running FDTD executable:', args.fdtd_cmd)
        try:
            subprocess.run([args.fdtd_cmd], check=True)
        except Exception as e:
            print('Failed to run pffdtd:', e)
            print('Aborting to avoid unintended runs.')
            sys.exit(1)

    fd_data = None
    if args.fd_file:
        fd_path = Path(args.fd_file)
        if fd_path.exists():
            try:
                from visualization.pffdtd_loader import load_fd

                print('Loading .fd file via visualization.pffdtd_loader.load_fd')
                fd_data = load_fd(str(fd_path))
            except Exception as e:
                print('Could not import or use visualization.pffdtd_loader:', e)
                print('Falling back to synthetic/empty fields.')
        else:
            print('Provided .fd file does not exist:', args.fd_file)

    # For Phase-1 we use a small synthetic particle set and zero E/B fields (placeholder)
    try:
        from pic.pic_driver import run_pic_single_step
    except Exception as e:
        print('Failed to import pic driver:', e)
        sys.exit(1)

    # Build particles: center-cluster example
    N = 100
    positions = np.random.rand(N, 3) * 4.0 + 2.0
    v_half = np.zeros((N, 3))
    charges = np.ones(N) * (1.0 / N)
    masses = np.ones(N)
    dt = 0.1

    grid_shape = (64, 64, 8)
    grid_origin = (0.0, 0.0, 0.0)
    grid_spacing = (1.0, 1.0, 1.0)

    rho, positions_new, v_half_new = run_pic_single_step(positions, v_half, charges, masses, dt, grid_shape, grid_origin, grid_spacing)

    out_path = Path(args.out)
    np.savez(out_path, rho=rho, positions=positions_new, v_half=v_half_new)
    print('Wrote coupling file:', str(out_path))


if __name__ == '__main__':
    main()
