import numpy as np
import matplotlib.pyplot as plt
import sys
import os

def load_vc(filepath):
    """Loads Voltage/Current data from .vc file."""
    data = []
    try:
        with open(filepath, 'r') as f:
            # Skip header if present (check first char for # or non-digit)
            for line in f:
                if not line.strip(): continue
                parts = line.split()
                try:
                    # Time, Volt, Current
                    vals = [float(p) for p in parts[:3]] 
                    data.append(vals)
                except ValueError:
                    continue # Skip header lines
    except FileNotFoundError:
        print(f"Error: File {filepath} not found.")
        return None
        
    return np.array(data)

def plot_vc(vc_data, save_path=None):
    if vc_data is None or len(vc_data) == 0:
        print("No data to plot.")
        return

    time = vc_data[:, 0]
    volt = vc_data[:, 1]
    curr = vc_data[:, 2]

    fig, ax1 = plt.subplots(figsize=(10, 6))

    color = 'tab:red'
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Voltage (V)', color=color)
    ax1.plot(time, volt, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  
    color = 'tab:blue'
    ax2.set_ylabel('Current (A)', color=color)  
    ax2.plot(time, curr, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title("Antenna Voltage and Current (Sheath Test)")
    
    if save_path:
        plt.savefig(save_path)
        print(f"Plot saved to {save_path}")
    else:
        plt.show()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python plot_sheath.py <path_to_vc_file> [output_image]")
        sys.exit(1)
        
    vc_file = sys.argv[1]
    out_file = sys.argv[2] if len(sys.argv) > 2 else "sheath_plot.png"
    
    data = load_vc(vc_file)
    plot_vc(data, out_file)
