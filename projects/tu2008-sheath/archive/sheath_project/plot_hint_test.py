import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def robust_load_vc(path):
    times, volts, currents = [], [], []
    with open(path, 'r', errors='ignore') as f:
        for line in f:
            parts = line.strip().replace(',', ' ').split()
            if len(parts) < 3:
                continue
            try:
                t_val = float(parts[0])
                v_val = float(parts[1])
                i_val = float(parts[2])
            except ValueError:
                continue
            times.append(t_val)
            volts.append(v_val)
            currents.append(i_val)
    return np.array(times), np.array(volts), np.array(currents)

def main():
    if len(sys.argv) < 2:
        print("Usage: python plot_hint_test.py <data.vc>")
        sys.exit(1)
        
    path = sys.argv[1]
    print(f"Loading {path}...")
    t, v, i = robust_load_vc(path)
    
    if len(t) == 0:
        print("Error: No data found.")
        sys.exit(1)
        
    print(f"Loaded {len(t)} samples.")
    
    # Plot the last 20% of the signal to check for steady-state
    idx = int(len(t) * 0.8)
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
    
    ax1.plot(t[idx:]*1e6, v[idx:], 'b-')
    ax1.set_ylabel('Voltage (V)')
    ax1.set_title('Hint Test: Steady-State V(t) and I(t) (Last 20%)')
    ax1.grid(True, alpha=0.3)
    
    ax2.plot(t[idx:]*1e6, i[idx:], 'r-')
    ax2.set_ylabel('Current (A)')
    ax2.set_xlabel('Time (μs)')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('sheath_project/results/hint_test_steady_state.png', dpi=150)
    print("Saved plot to sheath_project/results/hint_test_steady_state.png")

if __name__ == '__main__':
    main()
