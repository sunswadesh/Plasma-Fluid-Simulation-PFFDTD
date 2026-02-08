import numpy as np

def generate_test_vc(filename="test_data.vc"):
    # Generate 1000 points
    t = np.linspace(0, 1e-6, 1000) # 1 us
    freq = 5e6 # 5 MHz
    
    # Voltage: 10V sine wave
    v = 10 * np.sin(2 * np.pi * freq * t)
    
    # Current: 90 degree phase shift (Capacitive) -> I = C * dV/dt
    # V = V0 sin(wt) -> I = C * V0 * w * cos(wt) = C * V0 * w * sin(wt + pi/2)
    # Let C = 1e-12
    C_val = 1e-12
    w = 2 * np.pi * freq
    i_curr = C_val * 10 * w * np.cos(w * t)
    
    # Header line
    header = np.zeros(3) # specific values don't matter, just need a line
    
    # Data: Time, V, I (for source 1)
    data = np.column_stack((t, v, i_curr))
    
    # Combined
    full_data = np.vstack((header, data))
    
    np.savetxt(filename, full_data)
    print(f"Generated {filename}")

if __name__ == "__main__":
    generate_test_vc("visualization/test_data.vc")
