import os
import glob
import re
import argparse
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
    dt = t[1] - t[0]
    phasor = np.sum(signal * np.exp(-1j * 2 * np.pi * f * t)) * dt
    return phasor

def main():
    parser = argparse.ArgumentParser(description='Analyze 2D sheath frequency sweep (.vc phasor impedance)')
    parser.add_argument('--dir', default=r"results\sheath_2d_sweep", help='Sweep results directory')
    args = parser.parse_args()
    base_dir = args.dir
    # Find all data.vc files under results\sheath_2d_sweep\sd{Sd}_f{freq}\data.vc
    files = glob.glob(os.path.join(base_dir, "sd*_f*", "data.vc"))
    
    # We want to group by Sd
    data_by_sd = {}
    
    for path in sorted(files):
        # Extract Sd and Frequency from folder name (e.g., sd0_f20000)
        match = re.search(r'sd(\d+)_f(\d+)', path)
        if not match: continue
        sd = int(match.group(1))
        f_source = float(match.group(2))
        
        print(f"Processing Sd={sd}, Freq={f_source} Hz from {path}")
        try:
            t, v, i = robust_load_vc(path)
        except Exception as e:
            print(f"  Error loading {path}: {e}")
            continue
            
        if len(t) == 0: continue
        
        # Take last 50% for steady state
        idx = len(t) // 2
        t_ss = t[idx:]
        v_ss = v[idx:]
        i_ss = i[idx:]
        
        V_phasor = extract_amplitude_phase(t_ss, v_ss, f_source)
        I_phasor = extract_amplitude_phase(t_ss, i_ss, f_source)
        
        Z = V_phasor / I_phasor
        
        if sd not in data_by_sd:
            data_by_sd[sd] = {'freqs': [], 'Z_values': []}
        
        data_by_sd[sd]['freqs'].append(f_source)
        data_by_sd[sd]['Z_values'].append(Z)
        
    fig, (ax_real, ax_imag) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    
    for sd in sorted(data_by_sd.keys()):
        freqs = np.array(data_by_sd[sd]['freqs'])
        Z_values = np.array(data_by_sd[sd]['Z_values'])
        
        # Sort by frequency
        sort_idx = np.argsort(freqs)
        freqs = freqs[sort_idx]
        Z_values = Z_values[sort_idx]
        
        ax_real.plot(freqs / 1e3, np.real(Z_values), 'o-', label=f'Sd={sd}')
        ax_imag.plot(freqs / 1e3, np.imag(Z_values), 'o-', label=f'Sd={sd}')
        
        # Write individual summary file
        txt_path = os.path.join(base_dir, f'summary_sd{sd}.txt')
        with open(txt_path, 'w') as f:
            f.write("Freq(Hz)\tRe(Z)\tIm(Z)\n")
            for freq, Z in zip(freqs, Z_values):
                f.write(f"{freq}\t{np.real(Z)}\t{np.imag(Z)}\n")
        print(f"Wrote summary for Sd={sd} to {txt_path}")
        
        # Check zero crossing (resonance)
        imag_z = np.imag(Z_values)
        f_res = None
        for i in range(1, len(imag_z)):
            if imag_z[i-1] < 0 and imag_z[i] >= 0:
                f_res = freqs[i-1] + (freqs[i] - freqs[i-1]) * (-imag_z[i-1]) / (imag_z[i] - imag_z[i-1])
                break
        if f_res:
            print(f"** Resonance frequency for Sd={sd}: {f_res/1000.0:.3f} kHz **")
        else:
            print(f"No zero-crossing resonance detected for Sd={sd}")

    ax_real.set_ylabel('Re{Z} (Ohms)')
    ax_real.set_title('Antenna Impedance vs Frequency (2D Sheath Sweep)')
    ax_real.legend()
    ax_real.grid(True)
    
    ax_imag.set_xlabel('Frequency (kHz)')
    ax_imag.set_ylabel('Im{Z} (Ohms)')
    ax_imag.axhline(0, color='k', linestyle='--', linewidth=1)
    ax_imag.legend()
    ax_imag.grid(True)
    
    plt.tight_layout()
    plot_path = os.path.join(base_dir, 'sheath_2d_sweep_impedance.png')
    plt.savefig(plot_path, dpi=150)
    print(f"Saved global plot to {plot_path}")

if __name__ == '__main__':
    main()
