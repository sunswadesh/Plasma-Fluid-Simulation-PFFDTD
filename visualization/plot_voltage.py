import argparse
import numpy as np
import matplotlib.pyplot as plt
import os
from pffdtd_loader import load_voltage_current
from utils import compute_dtft, compute_impedance

def main():
    parser = argparse.ArgumentParser(description="Visualize PFFDTD Voltage/Current data.")
    parser.add_argument("filepath", help="Path to the .vc file")
    parser.add_argument("--source", type=int, default=1, help="Source number to extract (default: 1)")
    parser.add_argument("--save", action="store_true", help="Save plots to individual files instead of showing")
    args = parser.parse_args()

    if not os.path.exists(args.filepath):
        print(f"Error: File {args.filepath} not found.")
        return

    # 1. Load Data
    try:
        t, v, i_curr = load_voltage_current(args.filepath, args.source)
    except Exception as e:
        print(f"Error loading data: {e}")
        return

    print(f"Loaded {len(t)} samples.")

    # 2. Compute Transform (DTFT to match legacy)
    # Legacy range: 0.5 MHz to 10 MHz approx
    freqs, v_f = compute_dtft(t, v, freq_range_hz=(0.5e6, 15e6, 0.01e6))
    _, i_f = compute_dtft(t, i_curr, freq_range_hz=(0.5e6, 15e6, 0.01e6))
    
    z_f = compute_impedance(v_f, i_f)
    
    # Theoretical Capacitor Reactance for comparison (from legacy)
    # Cap = 1e-12
    # XC = -j / (w * C)
    cap_val = 1e-12
    w = 2 * np.pi * freqs
    xc_f = -1j / (w * cap_val)

    # 3. Plotting
    
    # Figure 1: Time Domain
    fig1, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    ax1.plot(t * 1e9, v) # Scale to ns
    ax1.set_ylabel("Voltage (V)")
    ax1.set_title("Time Domain Signals")
    ax1.grid(True)
    
    ax2.plot(t * 1e9, i_curr)
    ax2.set_ylabel("Current (A)")
    ax2.set_xlabel("Time (ns)")
    ax2.grid(True)
    
    # Figure 2: Frequency Domain (Magnitude)
    fig2, (ax3, ax4) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    freqs_mhz = freqs / 1e6
    
    ax3.plot(freqs_mhz, 20 * np.log10(np.abs(v_f)))
    ax3.set_ylabel("FFT V (dB)")
    ax3.set_title("Frequency Domain (Magnitude)")
    ax3.grid(True)
    
    ax4.plot(freqs_mhz, 20 * np.log10(np.abs(i_f)))
    ax4.set_ylabel("FFT I (dB)")
    ax4.set_xlabel("Frequency (MHz)")
    ax4.grid(True)
    
    # Figure 3: Impedance
    fig3, ax5 = plt.subplots(1, 1, figsize=(10, 6))
    ax5.plot(freqs_mhz, 20 * np.log10(np.abs(z_f)), label='Measured Z')
    ax5.plot(freqs_mhz, 20 * np.log10(np.abs(xc_f)), '--', label='Theoretical C (1pF)')
    ax5.set_ylabel("Impedance Magnitude (dB)")
    ax5.set_xlabel("Frequency (MHz)")
    ax5.set_title("Impedance Analysis")
    ax5.legend()
    ax5.grid(True)

    if args.save:
        base = os.path.splitext(os.path.basename(args.filepath))[0]
        fig1.savefig(f"{base}_time.png")
        fig2.savefig(f"{base}_freq.png")
        fig3.savefig(f"{base}_impedance.png")
        print(f"Plots saved as {base}_*.png")
    else:
        plt.show()

if __name__ == "__main__":
    main()
