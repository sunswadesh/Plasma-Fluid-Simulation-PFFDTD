"""
Impedance computation and plotting for sheath sweep results.
Computes Z(f) = DFT{V(t)} / DFT{I(t)} from .vc files.

Usage:
    python scripts/plot_impedance.py results/sheath_sweep/sd0/data.vc results/sheath_sweep/sd2/data.vc ...
    python scripts/plot_impedance.py results/sheath_sweep/      (auto-discovers all sd*/data.vc)
"""

import sys
import os
import glob
import numpy as np
import matplotlib.pyplot as plt


def load_vc(filepath):
    """Load a .vc file. Format: time V1 I1 [V2 I2 ...]"""
    data = np.loadtxt(filepath, skiprows=1)
    return data


def compute_impedance(time, voltage, current, window=True):
    """
    Compute impedance Z(f) = V(f) / I(f).
    
    Parameters:
        time: 1D array of time values
        voltage: 1D array of voltage values
        current: 1D array of current values
        window: apply Hanning window before DFT
    
    Returns:
        freq: frequency array (Hz)
        Z: complex impedance array
    """
    N = len(time)
    dt = time[1] - time[0]
    
    # Apply Hanning window to reduce spectral leakage
    if window:
        w = np.hanning(N)
    else:
        w = np.ones(N)
    
    V_f = np.fft.rfft(voltage * w)
    I_f = np.fft.rfft(current * w)
    freq = np.fft.rfftfreq(N, d=dt)
    
    # Avoid division by zero
    mask = np.abs(I_f) > np.max(np.abs(I_f)) * 1e-10
    Z = np.zeros_like(V_f)
    Z[mask] = V_f[mask] / I_f[mask]
    
    return freq, Z


def find_resonance(freq, Z):
    """Find resonance frequency where Im{Z} crosses zero (series resonance)."""
    imag_z = np.imag(Z)
    # Look for zero crossings (negative to positive = series resonance)
    crossings = []
    for i in range(1, len(imag_z)):
        if imag_z[i-1] < 0 and imag_z[i] >= 0:
            # Linear interpolation for precise crossing
            f_cross = freq[i-1] + (freq[i] - freq[i-1]) * (-imag_z[i-1]) / (imag_z[i] - imag_z[i-1])
            crossings.append(f_cross)
    return crossings


def discover_vc_files(path):
    """Auto-discover .vc files in a sweep directory."""
    if os.path.isfile(path):
        return [path]
    
    # Look for sd*/data.vc pattern
    pattern = os.path.join(path, "sd*", "data.vc")
    files = sorted(glob.glob(pattern))
    if not files:
        # Try direct *.vc
        files = sorted(glob.glob(os.path.join(path, "*.vc")))
    return files


def extract_sd_from_path(filepath):
    """Extract Sd value from path like .../sd4/data.vc"""
    parts = filepath.replace("\\", "/").split("/")
    for part in parts:
        if part.startswith("sd") and part[2:].isdigit():
            return int(part[2:])
    return None


def main():
    if len(sys.argv) < 2:
        print("Usage: python plot_impedance.py <path_or_files>")
        print("  path_or_files: directory with sd*/data.vc or individual .vc files")
        sys.exit(1)
    
    # Collect files
    files = []
    for arg in sys.argv[1:]:
        files.extend(discover_vc_files(arg))
    
    if not files:
        print("No .vc files found!")
        sys.exit(1)
    
    print(f"Found {len(files)} .vc file(s)")
    
    # Plot setup
    fig, axes = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    ax_real = axes[0]
    ax_imag = axes[1]
    
    resonances = []
    
    for filepath in files:
        sd = extract_sd_from_path(filepath)
        label = f"Sd={sd}" if sd is not None else os.path.basename(filepath)
        
        print(f"  Processing: {filepath} ({label})")
        
        data = load_vc(filepath)
        time = data[:, 0]
        voltage = data[:, 1]
        current = data[:, 2]
        
        freq, Z = compute_impedance(time, voltage, current)
        
        # Limit frequency range to meaningful region
        f_max = 1e6  # 1 MHz upper limit
        mask_f = freq <= f_max
        
        ax_real.plot(freq[mask_f] / 1e3, np.real(Z[mask_f]), label=label)
        ax_imag.plot(freq[mask_f] / 1e3, np.imag(Z[mask_f]), label=label)
        
        # Find resonance
        res = find_resonance(freq[mask_f], Z[mask_f])
        if res:
            resonances.append((sd, res[0]))
            print(f"    Resonance: {res[0]/1e3:.2f} kHz")
        else:
            print(f"    No resonance found in range")
    
    ax_real.set_ylabel("Re{Z} (Ohms)")
    ax_real.set_title("Input Impedance vs Frequency (Sheath Sweep)")
    ax_real.legend()
    ax_real.grid(True, alpha=0.3)
    
    ax_imag.set_xlabel("Frequency (kHz)")
    ax_imag.set_ylabel("Im{Z} (Ohms)")
    ax_imag.axhline(y=0, color='k', linestyle='--', linewidth=0.5)
    ax_imag.legend()
    ax_imag.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig("sheath_impedance.png", dpi=150)
    print(f"\nPlot saved to sheath_impedance.png")
    
    # If we have multiple Sd values, plot resonance shift
    if len(resonances) > 1:
        resonances.sort(key=lambda x: x[0])
        sds = [r[0] for r in resonances]
        fres = [r[1] / 1e3 for r in resonances]
        
        fig2, ax2 = plt.subplots(figsize=(8, 5))
        ax2.plot(sds, fres, 'o-', markersize=8)
        ax2.set_xlabel("Sheath Width Sd (cells)")
        ax2.set_ylabel("Resonance Frequency (kHz)")
        ax2.set_title("Resonance Shift vs Sheath Width")
        ax2.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig("sheath_resonance_shift.png", dpi=150)
        print(f"Resonance shift plot saved to sheath_resonance_shift.png")
    
    plt.show()


if __name__ == "__main__":
    main()
