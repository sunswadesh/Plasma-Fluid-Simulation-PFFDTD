PIC Python Migration — Phase 1

Summary
-------
This phase ports legacy MATLAB PIC utilities to Python and provides a file-based coupling orchestrator for integration with the C++ `pffdtd` solver.

What was done
-------------
- Added Python PIC package under `python/pic/`:
  - `boris_push.py` — Boris particle pusher
  - `weighting.py` — trilinear interpolation weights
  - `grid_particle.py` — scatter/gather routines
  - `pic_driver.py` — single-step PIC driver
  - tests under `python/pic/tests/`
  - example demos under `python/pic/examples/`
- Added `scripts/pic_couple.py` orchestrator for file-based coupling (does not auto-run `pffdtd`).
- Created `requirements.txt` and a GitHub Actions workflow `python-ci.yml` to run tests on `PIC_FDTD` branch.

How to run
----------
Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run unit tests:

```bash
python -m pytest -q python/pic/tests
```

Run the orchestrator (example):

```bash
python scripts/pic_couple.py --out coupling_currents.npz
```

Next steps
----------
- Implement `scripts/pic_couple.py` integration to read actual `.fd` files produced by `pffdtd` and write currents in a format read by `pffdtd`.
- Add minimal hook in `pffdtd` to read coupling `.npz`/HDF5 files.
- Archive MATLAB scripts and add more unit/integration tests.
