import numpy as np
import matplotlib.pyplot as plt
from pic.grid_particle import particle_to_grid_charge

# 2D demo slice: we'll use a 2D (x,y) grid by fixing z index
nx, ny, nz = 50, 50, 3
grid = np.zeros((nx, ny, nz))

# single particle near center
xi, yj, zk = 24, 24, 1
pi, pj, pk = 0.4, 0.6, 0.5
q = 1.0

particle_to_grid_charge(grid, xi, yj, zk, pi, pj, pk, q)

# take z=1 slice
slice2d = grid[:, :, 1]

plt.figure(figsize=(6,5))
plt.imshow(slice2d.T, origin='lower', cmap='viridis')
plt.colorbar(label='Charge density')
plt.scatter([xi, xi+1], [yj, yj+1], color='red', s=20, label='neighbor nodes')
plt.title('Particle charge scatter (z=1 slice)')
plt.legend()
plt.tight_layout()
plt.savefig('python/pic/examples/grid_particle_demo.png')
print('Saved plot to python/pic/examples/grid_particle_demo.png')
