# PIC <-> FDTD Coupling Contract (v1)

Lean in-loop exchange between the `pffdtd` FDTD solver and the Python PIC.
`.fd` files are **not** part of the loop — they remain an offline,
field-analysis-only artifact.

## Exchange directory

- Default: `/dev/shm/pffdtd_coupling/` (RAM-backed; falls back to a system
  temp dir when `/dev/shm` is unavailable). See `pic.exchange.default_exchange_dir()`.
- Override per run via CLI (`--exchange-dir`).

## Files

### `fields.npz` — FDTD → PIC (written by `pffdtd`)

| key            | shape            | dtype   | meaning                              |
|----------------|------------------|---------|--------------------------------------|
| `E`            | `(3, nx, ny, nz)`| float64 | electric field on the Yee/grid nodes |
| `B`            | `(3, nx, ny, nz)`| float64 | magnetic field on the Yee/grid nodes |
| `grid_shape`   | `(3,)`           | int64   | `(nx, ny, nz)`                       |
| `grid_origin`  | `(3,)`           | float64 | world coords of node (0,0,0)         |
| `grid_spacing` | `(3,)`           | float64 | `(dx, dy, dz)`                       |
| `dt`           | scalar           | float64 | FDTD timestep used                   |
| `step`         | scalar           | int64   | FDTD step index this snapshot is for |

### `sources.npz` — PIC → FDTD (written by the PIC driver)

| key            | shape            | dtype   | meaning                              |
|----------------|------------------|---------|--------------------------------------|
| `rho`          | `(nx, ny, nz)`   | float64 | charge density deposited by particles|
| `J`            | `(3, nx, ny, nz)`| float64 | current density `q·v` deposited       |
| `grid_shape`   | `(3,)`           | int64   | `(nx, ny, nz)` — must match fields   |
| `grid_origin`  | `(3,)`           | float64 | must match fields                    |
| `grid_spacing` | `(3,)`           | float64 | must match fields                    |
| `dt`           | scalar           | float64 | PIC timestep used                    |
| `step`         | scalar           | int64   | FDTD step index this deposit is for  |

Conservation checks the reader may apply:

- `rho.sum() == total particle charge`
- `J[c].sum() == sum(q * v_c)` per component

## Protocol (v1, polling)

Run the PIC side as a **persistent worker** (JIT compilation happens once
at startup — about 1.7 s — instead of per step):

```
python3 scripts/pic_couple.py --serve --exchange-dir /dev/shm/pffdtd_coupling
```

The worker watches `fields.npz`; whenever it carries a step newer than
the last one processed, it gathers E/B to the particles, pushes,
deposits `rho`/`J`, and atomically writes `sources.npz`. Particle state
persists in `particles.npz` between steps. Stop with Ctrl-C or by
creating `<exchange-dir>/stop`. `PIC_PARTICLES` env var sets the ensemble
size when no saved state exists.

1. `pffdtd` finishes FDTD step `k`, writes `fields.npz` **atomically**
   (temp file + rename — see `pic.exchange._atomic_npz`), then continues or
   waits depending on the coupling mode.
2. The PIC worker picks up `fields.npz` with `step == k`, processes it,
   and atomically writes `sources.npz` with `step == k`.
3. `pffdtd` picks up `sources.npz` (`step == k`) and applies the sources
   on its next step(s).

Measured steady-state cost per coupling step (20k particles, 32³ grid,
per-particle E/B, `rho`+`J` deposition): **~9 ms**
(gather ~3 ms, PIC ~3 ms, write ~3 ms) — vs ~250 ms if run as one
process per step (numba `prange` kernels do not hit the disk cache,
so a fresh process recompiles every time).

Coupling every step is the default; coupling every K steps just means
steps 1–3 run when `k % K == 0`. Readers must always check the `step`
metadata and never consume a file twice for the same step.

## Size reference (48³ grid, float64)

- `fields.npz`: ~5.3 MB uncompressed per exchange
- `sources.npz`: ~3.5 MB uncompressed per exchange

If exchange I/O ever shows up in profiles, the planned upgrades are:
float32 snapshots, then shared-memory transport. The key names and
shapes stay the same.

## Status

- [x] Python side: `pic.exchange` read/write, numba gather (`E`/`B` →
      particles), numba `rho`/`J` deposition, `scripts/pic_couple.py`
      implements the PIC half of the protocol (single-step and `--serve`
      persistent-worker modes).
- [ ] C++ side: `pffdtd` does not yet write `fields.npz` / read
      `sources.npz`. Implementation plan scoped below.

## C++ implementation plan (scoped 2026-09-22, not yet implemented)

Three pieces, ~2 days estimated:

1. **`src/io/npz.h` / `npz.cpp`** (~300 lines, zero dependencies): minimal
   uncompressed-zip reader/writer for `.npy` blobs (CRC32, npy header
   build/parse, zip local + central directory records). Validates
   `descr == '<f8'` and shapes on read.
2. **Loop hooks in `src/pffdtd.cpp`**: after `Bcalc()` in the main
   `while (Q_flag == 0)` loop, when `i % couple_rate == 0`:
   write `fields.npz` → block-wait for `sources.npz` with matching
   `step` → load `J`. Config via env vars `PIC_EXCHANGE_DIR` /
   `PIC_COUPLE_RATE` (lockstep v1; lagged/pipelined later if needed).
   Field packing repacks `EX[IDX4(i,j,k,1)]` etc. (level 1 = current;
   on the `perf/ptr-rotation-timelevels` branch this is `tlE_cur`)
   into `(3, nx, ny, nz)` C-order with `nx=sx+1`, `ny=sy+1`, `nz=sz+1`,
   origin `(0,0,0)`, spacing `(dx,dy,dz)`.
3. **Apply PIC current in the E update**: `Ecalcmod` already applies
   `- C_MU * SIG[i][j][k] * JX` with `C_MU = dt/(2*EPSILON_0)`; the PIC
   `J` slots in as an extra term next to the fluid `J`. Non-plasma
   `Ecalc` needs the same term added (it currently has none).

Open physics decisions (needed before implementing): Yee-staggering
convention for the exchanged components (document half-cell offsets vs.
interpolate to cell centers); additive vs. replacement `J`; what `rho`
feeds (fluid density vs. diagnostics-only); coupling rate.

Test plan: synthetic uniform `J` → E should respond linearly;
round-trip `fields.npz`/`sources.npz` against the Python side.
