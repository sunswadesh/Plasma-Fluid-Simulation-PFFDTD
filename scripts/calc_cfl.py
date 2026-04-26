import math

# Constants
c = 2.998e8
KB = 1.3806e-23
ME = 9.109e-31
QE = 1.602e-19
EPS0 = 8.854e-12
AMU = 1.66e-27

# User Parameters
freq_plasma_hz = 30e3        # 30 kHz (Note: User said f_pump = 30 kHz. Usually f_p is plasma freq. 
                             # If n_e = 5e8, let's calc f_p to see if they match or if 30kHz is something else.)
n_e = 5e8                    # 5 * 10^8 m^-3
Te_K = 2000.0                # Assumed Electron Temperature (Kelvin) for T > 0

# Grid Parameters from dipole.str
dx = 0.04
dy = 0.04
dz = 0.04

# 1. Calculate Plasma Frequency from Density
wp = math.sqrt(n_e * QE**2 / (ME * EPS0))
fp = wp / (2 * math.pi)

print(f"Target Density: {n_e:.2e} m^-3")
print(f"Calculated Plasma Frequency (fp): {fp:.2e} Hz ({fp/1e6:.4f} MHz)")
print(f"User requested 30 kHz. If this is f_pump, it might be different from f_p.")
print(f"However, pffdtd takes 'FREQ_PLASMA' as arg 3. We should verify if this is f_p or source freq.")

# 2. Thermal Velocity
v_th = math.sqrt(2 * KB * Te_K / ME)
print(f"Thermal Velocity (v_th): {v_th:.2e} m/s ({v_th/c:.4f} c)")

# 3. Debye Length
lambda_d = v_th / wp
print(f"Debye Length: {lambda_d:.4f} m")
print(f"Grid Resolution: dx = {dx} m")
if dx > lambda_d:
    print("WARNING: dx > lambda_d. Debye length is not resolved! Instabilities possible.")
else:
    print("Grid resolves Debye length (dx < lambda_d). Good.")

# 4. CFL Calculation
# EM CFL
dt_em = 1 / (c * math.sqrt(1/dx**2 + 1/dy**2 + 1/dz**2))
print(f"EM CFL Limit (dt_em): {dt_em:.2e} s")

# Thermal CFL (Fluid)
# dt < dx / v_th (approx)
dt_th = dx / v_th
print(f"Thermal CFL Limit (dt_th): {dt_th:.2e} s")

# Chosen dt
dt_final = min(dt_em, dt_th) * 0.9 # Safety factor
print(f"Recommended dt: {dt_final:.2e} s")

# 5. Iterations for one cycle of 30 kHz
freq_source = 30e3
period = 1 / freq_source
iterations_per_cycle = period / dt_final
print(f"Iterations per cycle (30 kHz): {iterations_per_cycle:.1f}")

