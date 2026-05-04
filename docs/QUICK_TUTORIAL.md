# Quick Tutorial: Run The Dipole Example

This tutorial walks through a full dipole simulation run and basic result plotting on Windows.

## Prerequisites

- Repository checked out
- A working C++ compiler in `PATH` (for example MinGW-w64)
- Python 3 installed for plotting

## Step 1: Build The Solver

From repository root:

```bat
compile.bat
```

Expected output executable:

- `pffdtd_parallel.exe` (preferred)

If parallel build is unavailable, the run script can also use legacy serial/parallel executables if present.

## Step 2: Run The Dipole Simulation

Use the helper script:

```bat
scripts\run_simulation.bat run_test 5.3 0.1 1.43
```

What this does:

- Uses input base name `dipole` (`dipole.str`)
- Writes simulation output to `results\run_test\`
- Captures runtime log in `results\run_test\simulation.log`
- Invokes Python plotting for voltage/current and impedance

## Step 3: Inspect Output Files

Core simulation outputs:

- `results\run_test\data.vc` (voltage/current samples)
- `results\run_test\data.fd` (field samples)
- `results\run_test\simulation.log` (run log)

Generated plots:

- `results\run_test\impedance_plot_vi.png`
- `results\run_test\impedance_plot_impedance.png`

Note: the plotting script treats `impedance_plot.png` as a prefix and emits two files.

## Step 4: Optional Manual Plot Regeneration

If you need to regenerate plots manually:

```powershell
python visualization/plot_voltage.py results/run_test/data.vc --save results/run_test/impedance_plot.png
```

## Troubleshooting

- If build fails with compiler errors, verify compiler installation and `PATH`.
- If the run script reports no executable found, build first or place a compatible executable in repo root.
- If plotting fails with Python import errors, install dependencies from `visualization/requirements.txt`.

## Next Reads

- Input file details: `docs/INPUT_FORMAT.md`
- Physics background: `docs/PHYSICS.md`
- Architecture details: `docs/ARCHITECTURE.md`
