# Narrow-band Excitation & Long-recording Plan

Purpose: obtain clean, high-resolution measurements of antenna resonance vs sheath width by (a) lengthening recorded time-series to improve DFT frequency resolution, and (b) optionally using narrow-band excitation (frequency sweep) to map resonance directly.

Key requirements

- Frequency resolution df = 1 / T where T is total recorded time. To achieve df ~ 1 kHz, record T >= 1 ms.
- Sampling interval dt must satisfy Nyquist: fs = 1/dt >= 2 * f_max_interest. For f_max_interest = 200 kHz, fs >= 400 kHz.
- Practical approach: reduce sampling rate (record every Nth time-step) while extending total iterations to reach desired T. This keeps file size manageable.

Recommended steps

1. Increase simulation iterations to reach T >= 1 ms of physical time. Compute required iterations: iterations_needed = T / dt_sim where dt_sim is simulation timestep (CFL-based). Example: if dt_sim = 1e-9 s, iterations = 1e-3 / 1e-9 = 1e6 iterations.

2. Reduce output sampling frequency by recording every `write_stride` steps (modify code or use runtime option if available). Example: write_stride = 1000 reduces output size by 1000 while keeping T the same.

3. Option A — Broadband, long-recording (preferred): keep broadband excitation but run long enough to capture many cycles; then trim transient and compute DFT on steady-state portion.

4. Option B — Narrow-band sweep (fast, high SNR): run a sequence of short steady-state runs where the source is a continuous-tone at frequency f_i (grid of frequencies), measure steady-state amplitude/phase, and assemble Z(f). This converges faster to resonance but requires scripting multiple runs.

Example invocation templates (PowerShell)

Broadband long run (example):
```powershell
$exepath = Join-Path (Get-Location) 'build\pffdtd_parallel.exe'
$Sd = 4
$outdir = Join-Path 'results\sheath_long' ("sd$Sd")
if(-not (Test-Path $outdir)){ New-Item -ItemType Directory -Path $outdir | Out-Null }
# Increase iterations to 1,000,000 and request data sampling stride if supported (here shown as conceptual 'iterations' arg)
& $exepath 'sheath' (Join-Path $outdir 'data') 200000 0.1 0 0 0 1000000 $Sd > (Join-Path $outdir 'simulation.log') 2>&1
```

Frequency-stepped narrow-band plan (example loop):
```powershell
$exepath = Join-Path (Get-Location) 'build\pffdtd_parallel.exe'
$freqs = @(20000,25000,30000,35000,40000) # frequencies to probe (Hz)
$Sd = 4
foreach($f in $freqs){
  $outdir = Join-Path 'results\sheath_sweep_narrow' ("sd$Sd\f$f")
  if(-not (Test-Path $outdir)){ New-Item -ItemType Directory -Path $outdir -Force | Out-Null }
  # Use a short run long enough to reach steady-state at frequency f
  & $exepath 'sheath' (Join-Path $outdir 'data') $f 0.1 0 0 0 20000 $Sd > (Join-Path $outdir 'simulation.log') 2>&1
}
```

Notes

- Verify whether `pffdtd_parallel.exe` supports a `write_stride` or output-sampling argument; if not, consider adding a small CLI arg or recompiling to support `--output_step` to reduce file sizes.
- For broadband long runs prefer to (a) run longer, (b) write less often, (c) trim initial transient before DFT.
- For narrow-band sweeps, choose frequency step spacing smaller than expected resonance width (e.g., 100–500 Hz if you expect sharp resonances).

Next actions I can take for you

- Edit `scripts/run_sheath_sweep.ps1` to include an `--iterations` value and / or create `scripts/run_sheath_long_trace.ps1` using the examples above.
- Modify `src/pffdtd.cpp` to add a user-visible `--output_step` CLI parameter if needed (requires a small code change and rebuild).
- Orchestrate a narrow-band sweep run and aggregate results into a single impedance-vs-frequency file.
