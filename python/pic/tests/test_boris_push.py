import numpy as np
from pic.boris_push import boris_push


def test_boris_basic():
    q = -1.0
    m = 1.0
    dt = 0.1
    v0 = np.array([1.0, 0.0, 0.0])
    E = np.array([0.0, 0.0, 0.0])
    B = np.array([0.0, 0.0, 0.1])

    v_next = boris_push(q, m, dt, v0, E, B)
    # basic sanity checks
    assert v_next.shape == (3,)
    assert np.isfinite(v_next).all()


if __name__ == '__main__':
    test_boris_basic()
    print('test passed')
