import numpy as np
from pic.pic_driver import run_pic_single_step


def test_pic_single_step_conservation():
    N = 5
    positions = np.array([[1.2,1.3,1.4],[2.1,2.2,2.3],[3.5,1.1,0.9],[0.2,4.7,2.2],[1.9,1.9,1.9]])
    v_half = np.zeros((N,3))
    # give one particle a small initial half-step velocity so positions move
    v_half[0] = np.array([0.1, 0.0, 0.0])
    charges = np.array([1.0, -1.0, 2.0, 0.5, -0.5])
    masses = np.ones(N)
    dt = 0.05
    grid_shape = (8,8,8)

    rho, pos_new, v_half_new = run_pic_single_step(positions, v_half, charges, masses, dt, grid_shape)

    # total charge should be conserved
    assert np.isclose(rho.sum(), charges.sum())
    # positions updated
    assert not np.allclose(pos_new, positions)
    # velocities may be unchanged when E/B are zero; no assertion


if __name__ == '__main__':
    test_pic_single_step_conservation()
    print('pic_driver tests passed')
