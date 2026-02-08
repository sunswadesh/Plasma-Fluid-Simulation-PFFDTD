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
    parser.add_argument("--save", help="Path to save the impedance plot")
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
    z_mag = np.abs(z_f)
    
    # Normalized Impedance (if needed, otherwise just |Z|)
    # User's image shows normalized |Z/Z0|.  Z0 ~ 1000? 
    # Or maybe it's normalized to free space? 
    # For now, let's plot Magnitude.
    
    # Theoretical Capacitor Reactance for comparison (from legacy)
    # Cap = 1e-12
    # XC = -j / (w * C)
    cap_val = 1e-12
    w = 2 * np.pi * freqs
    xc_f = -1j / (w * cap_val)

    # 3. Plotting
    
    # Figure 1: Voltage and Current (Time Domain)
    fig1, ax1 = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    
    ax1[0].plot(t * 1e9, v) # Scale to ns
    ax1[0].set_ylabel("Voltage (V)")
    ax1[0].set_title("Time Domain Signals")
    ax1[0].grid(True)
    
    ax1[1].plot(t * 1e9, i_curr)
    ax1[1].set_ylabel("Current (A)")
    ax1[1].set_xlabel("Time (ns)")
    ax1[1].grid(True)

    # Figure 2: Impedance (Magnitude and Phase)
    fig2, ax2 = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    
    # Magnitude
    ax2[0].plot(freqs / 1e6, np.abs(z_f), label='|Z|')
    ax2[0].set_ylabel("|Z| (Ohms)")
    ax2[0].set_title("Impedance Analysis")
    ax2[0].grid(True)
    ax2[0].legend()
    
    # Phase
    ax2[1].plot(freqs / 1e6, np.angle(z_f, deg=True), label='Phase(Z)', color='orange')
    ax2[1].set_ylabel("Phase (Degrees)")
    ax2[1].set_xlabel("Frequency (MHz)")
    ax2[1].grid(True)
    ax2[1].legend()

    if args.save:
        # If save path is a directory/prefix, adapt. 
        # But args.save is likely a filename like "impedance_plot.png".
        # We need to split it to save two files.
        dir_name = os.path.dirname(args.save)
        base_name = os.path.splitext(os.path.basename(args.save))[0]
        
        save_path_vi = os.path.join(dir_name, f"{base_name}_vi.png")
        save_path_z = os.path.join(dir_name, f"{base_name}_impedance.png")
        
        fig1.savefig(save_path_vi)
        fig2.savefig(save_path_z)
        print(f"Plots saved to:\n  {save_path_vi}\n  {save_path_z}")
    else:
        plt.show()

if __name__ == "__main__":
    main()
