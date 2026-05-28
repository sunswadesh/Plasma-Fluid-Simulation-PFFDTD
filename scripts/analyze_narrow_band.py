import os
import glob
import re
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def robust_load_vc(path):
    times, volts, currents = [], [], []
    with open(path, 'r', errors='ignore') as f:
        for line in f:
            parts = line.strip().replace(',', ' ').split()
            if len(parts) < 3: continue
            try:
                t, v, i = float(parts[0]), float(parts[1]), float(parts[2])
            except ValueError:
                continue
            times.append(t)
            volts.append(v)
            currents.append(i)
    return np.array(times), np.array(volts), np.array(currents)

def extract_amplitude_phase(t, signal, f):
    # Use DFT at exactly frequency f
    # F(f) = sum( signal * exp(-j * 2 * pi * f * t) ) * dt
    dt = t[1] - t[0]
    phasor = np.sum(signal * np.exp(-1j * 2 * np.pi * f * t)) * dt
    return phasor

def main():
    base_dir = r"results\sheath_narrow_band"
    files = glob.glob(os.path.join(base_dir, "sd*", "data.vc"))
    
    freqs = []
    Z_values = []
    
    for path in sorted(files):
        # Extract frequency from folder name (e.g., sd200000)
        match = re.search(r'sd(\d+)', path)
        if not match: continue
        f_source = float(match.group(1))
        
        print(f"Processing {f_source} Hz from {path}")
        t, v, i = robust_load_vc(path)
        
        if len(t) == 0: continue
        
        # Take last 50% for steady state
        idx = len(t) // 2
        t_ss = t[idx:]
        v_ss = v[idx:]
        i_ss = i[idx:]
        
        V_phasor = extract_amplitude_phase(t_ss, v_ss, f_source)
        I_phasor = extract_amplitude_phase(t_ss, i_ss, f_source)
        
        Z = V_phasor / I_phasor
        freqs.append(f_source)
        Z_values.append(Z)
        
    freqs = np.array(freqs)
    Z_values = np.array(Z_values)
    
    # Sort by frequency just in case
    sort_idx = np.argsort(freqs)
    freqs = freqs[sort_idx]
    Z_values = Z_values[sort_idx]
    
    fig, (ax_real, ax_imag) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    ax_real.plot(freqs / 1e3, np.real(Z_values), 'o-', color='blue')
    ax_real.set_ylabel('Re{Z} (Ohms)')
    ax_real.set_title('Antenna Impedance vs Frequency (Narrow-Band Sweep)')
    ax_real.grid(True)
    
    ax_imag.plot(freqs / 1e3, np.imag(Z_values), 'o-', color='red')
    ax_imag.set_xlabel('Frequency (kHz)')
    ax_imag.set_ylabel('Im{Z} (Ohms)')
    ax_imag.axhline(0, color='k', linestyle='--', linewidth=1)
    ax_imag.grid(True)
    
    plt.tight_layout()
    plot_path = os.path.join(base_dir, 'narrow_band_impedance.png')
    plt.savefig(plot_path, dpi=150)
    print(f"Saved plot to {plot_path}")

    # Write summary
    txt_path = os.path.join(base_dir, 'narrow_band_summary.txt')
    with open(txt_path, 'w') as f:
        f.write("Freq(Hz)\tRe(Z)\tIm(Z)\n")
        for freq, Z in zip(freqs, Z_values):
            f.write(f"{freq}\t{np.real(Z)}\t{np.imag(Z)}\n")

if __name__ == '__main__':
    main()
