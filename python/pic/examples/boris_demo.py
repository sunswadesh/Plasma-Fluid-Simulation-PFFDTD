import numpy as np
import matplotlib.pyplot as plt
from pic.boris_push import boris_push

q = -1.0
m = 1.0
dt = 0.1
steps = 200

# initial conditions
v_half = np.array([0.0, 1.0, 0.0])  # velocity at half-step
pos = np.array([0.0, 0.0, 0.0])

E = np.array([0.0, 0.0, 0.0])
B = np.array([0.0, 0.0, 0.5])

trajectory = np.zeros((steps, 3))

for i in range(steps):
    # update velocity (to next half-step)
    v_half = boris_push(q, m, dt, v_half, E, B)
    # update position by full step using v_half
    pos = pos + v_half * dt
    trajectory[i] = pos

# plot
plt.figure(figsize=(6,6))
plt.plot(trajectory[:,0], trajectory[:,1], '-o', markersize=2)
plt.title('Boris pusher trajectory demo')
plt.xlabel('x')
plt.ylabel('y')
plt.axis('equal')
plt.grid(True)
plt.tight_layout()
plt.savefig('python/pic/examples/boris_demo.png')
print('Saved plot to python/pic/examples/boris_demo.png')
