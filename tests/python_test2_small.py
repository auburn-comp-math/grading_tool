from hw00 import p2
import numpy as np
import time

def test_p2():
    A = np.array([[1]])
    hw_assert (p2(A) == 1)
    A = np.array([[1, 2], [3, 4]])
    hw_assert (p2(A) == -2)
    A = np.array([[-1]])
    hw_assert (p2(A) == -1)
    A = np.array([[1, 3], [3, 1]])
    hw_assert (p2(A) == -8)
    A = np.array([[1, 0], [0, 1]])
    hw_assert (p2(A) == 1)

def hw_assert(X):
    if X:
        print('\t PASS')
    else:
        print('\t FAIL')

test_p2()
