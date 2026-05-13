"""
Robust analyzer for sheath sweep .vc files.
Usage:
  python scripts/analyze_sheath_results.py results/sheath_sweep

This script reads `data.vc` files under `sd*/` folders, parses the first three numeric columns
(time, voltage, current), computes Z(f)=V(f)/I(f) with a Hanning window, finds the series
resonance (Im{Z} zero-crossing), and writes two plots:
  - `sheath_impedance.png` (Re/Im Z vs frequency)
  - `sheath_resonance_shift.png` (resonance frequency vs Sd)

Saves a summary to `sheath_resonance_summary.txt`.
"""
import sys
import os
import glob
import argparse
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def robust_load_vc(path):
    times = []
    volts = []
    currents = []
    with open(path, 'r', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Replace commas with spaces
            parts = line.replace(',', ' ').split()
            # Try to parse first three tokens as floats
            if len(parts) < 3:
                continue
            try:
                t = float(parts[0])
                v = float(parts[1])
                i = float(parts[2])
            except ValueError:
                continue
            times.append(t)
            volts.append(v)
            currents.append(i)
    if not times:
        raise ValueError(f"No numeric data parsed from {path}")
    return np.array(times), np.array(volts), np.array(currents)


def trim_and_decimate(time, voltage, current, trim_seconds=0.0, decimate=1):
    # Trim to last `trim_seconds` seconds if requested
    if trim_seconds and trim_seconds > 0.0:
        t0 = time[-1] - float(trim_seconds)
        idx = np.searchsorted(time, t0, side='left')
        time = time[idx:]
        voltage = voltage[idx:]
        current = current[idx:]
    # Decimate by integer factor using block averaging (simple anti-alias)
    M = int(decimate)
    if M <= 1:
        return time, voltage, current
    n = (len(time) // M) * M
    if n < M:
        raise ValueError('Not enough samples to decimate by factor %d' % M)
    t2 = time[:n].reshape(-1, M).mean(axis=1)
    v2 = voltage[:n].reshape(-1, M).mean(axis=1)
    i2 = current[:n].reshape(-1, M).mean(axis=1)
    return t2, v2, i2


def compute_impedance(time, voltage, current, window=True):
    N = len(time)
    # Use median delta to be robust against occasional repeated timestamps
    diffs = np.diff(time)
    if len(diffs) == 0:
        raise ValueError('Time array too short')
    dt = float(np.median(diffs))
    if window:
        w = np.hanning(N)
    else:
        w = np.ones(N)
    V_f = np.fft.rfft(voltage * w)
    I_f = np.fft.rfft(current * w)
    freq = np.fft.rfftfreq(N, d=dt)
    mask = np.abs(I_f) > np.max(np.abs(I_f)) * 1e-10
    Z = np.zeros_like(V_f, dtype=np.complex128)
    Z[mask] = V_f[mask] / I_f[mask]
    return freq, Z


def find_resonance(freq, Z, fmax=1e6):
    mask = freq <= fmax
    freq = freq[mask]
    Z = Z[mask]
    imag_z = np.imag(Z)
    crossings = []
    for i in range(1, len(imag_z)):
        if imag_z[i-1] < 0 and imag_z[i] >= 0:
            f_cross = freq[i-1] + (freq[i] - freq[i-1]) * (-imag_z[i-1]) / (imag_z[i] - imag_z[i-1])
            crossings.append(f_cross)
    return crossings


def discover_vc_files(path):
    pattern = os.path.join(path, 'sd*', 'data.vc')
    files = glob.glob(pattern)
    files = sorted(files)
    return files


def extract_sd_from_path(filepath):
    parts = filepath.replace('\\', '/').split('/')
    for part in parts:
        if part.startswith('sd') and part[2:].isdigit():
            return int(part[2:])
    return None


def main():
    parser = argparse.ArgumentParser(description='Analyze sheath sweep results')
    parser.add_argument('sweep_dir', help='Path to results/sheath_sweep')
    parser.add_argument('--fmax', type=float, default=1e6, help='Maximum frequency (Hz) to analyze')
    parser.add_argument('--decimate', type=int, default=1, help='Integer decimation factor (block-average)')
    parser.add_argument('--trim_seconds', type=float, default=0.0, help='Keep only the last N seconds of the record')
    args = parser.parse_args()
    sweep_dir = args.sweep_dir
    fmax_arg = float(args.fmax)
    decimate_arg = int(args.decimate)
    trim_seconds_arg = float(args.trim_seconds)
    files = discover_vc_files(sweep_dir)
    if not files:
        print('No .vc files found under', sweep_dir)
        sys.exit(1)
    print(f'Found {len(files)} .vc files')

    fig, axes = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    ax_real = axes[0]
    ax_imag = axes[1]
    resonances = []
    summary_lines = []

    for fp in files:
        sd = extract_sd_from_path(fp)
        label = f'Sd={sd}' if sd is not None else os.path.basename(fp)
        print('Processing', fp, label)
        try:
            t, v, i = robust_load_vc(fp)
        except Exception as e:
            print('  Error parsing', fp, e)
            continue
        # Trim and decimate if requested
        try:
            t, v, i = trim_and_decimate(t, v, i, trim_seconds=trim_seconds_arg, decimate=decimate_arg)
        except Exception as e:
            print('  Error during trim/decimate:', e)
            continue
        freq, Z = compute_impedance(t, v, i)
        f_max = fmax_arg
        mask_f = freq <= f_max
        ax_real.plot(freq[mask_f] / 1e3, np.real(Z[mask_f]), label=label)
        ax_imag.plot(freq[mask_f] / 1e3, np.imag(Z[mask_f]), label=label)
        # Find zero-crossing series resonance (Im{Z} crossing from - to +)
        res = find_resonance(freq, Z, fmax=f_max)
        if res:
            resonances.append((sd, res[0]))
            summary_lines.append(f"{sd}\t{res[0]:.6f}\tpeak:{0:.6f}")
            print(f"  Resonance at {res[0]/1e3:.3f} kHz")
        else:
            # If no Im{Z} zero crossing found, report peak magnitude frequency as approximate resonance
            magZ = np.abs(Z)
            # ignore DC bin
            if len(magZ) > 1:
                idx_peak = np.argmax(magZ[1:]) + 1
                fpeak = freq[idx_peak]
                summary_lines.append(f"{sd}\tNaN\tpeak:{fpeak:.6f}")
                print(f"  No zero-crossing; peak |Z| at {fpeak/1e3:.3f} kHz")
            else:
                summary_lines.append(f"{sd}\tNaN\tpeak:NaN")
                print('  No resonance found and no frequency bins')

    ax_real.set_ylabel('Re{Z} (Ohms)')
    ax_real.set_title('Input Impedance vs Frequency (Sheath Sweep)')
    ax_real.legend()
    ax_real.grid(True, alpha=0.3)
    ax_imag.set_xlabel('Frequency (kHz)')
    ax_imag.set_ylabel('Im{Z} (Ohms)')
    ax_imag.axhline(y=0, color='k', linestyle='--', linewidth=0.5)
    ax_imag.legend()
    ax_imag.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('sheath_impedance.png', dpi=150)
    print('Saved sheath_impedance.png')

    if len(resonances) > 1:
        resonances = [r for r in resonances if r[1] is not None]
        resonances.sort(key=lambda x: x[0])
        sds = [r[0] for r in resonances]
        fres = [r[1]/1e3 for r in resonances]
        fig2, ax2 = plt.subplots(figsize=(8,5))
        ax2.plot(sds, fres, 'o-', markersize=8)
        ax2.set_xlabel('Sheath Width Sd (cells)')
        ax2.set_ylabel('Resonance Frequency (kHz)')
        ax2.set_title('Resonance Shift vs Sheath Width')
        ax2.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('sheath_resonance_shift.png', dpi=150)
        print('Saved sheath_resonance_shift.png')

    # Write summary
    with open('sheath_resonance_summary.txt', 'w') as sf:
        sf.write('Sd\tf_res(Hz)\n')
        sf.write('\n'.join(summary_lines))
    print('Wrote sheath_resonance_summary.txt')

if __name__ == '__main__':
    main()
