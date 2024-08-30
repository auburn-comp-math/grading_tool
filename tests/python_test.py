from hw00 import *
import numpy as np
import time

def test_p1():
    hw_assert (p1(0) == 0)
    hw_assert (p1(1) == 1)
    hw_assert (p1(2) == 1)
    hw_assert (p1(3) == 2)

def test_p2():
    A = np.array([[1]])
    hw_assert (p2(A) == 1)
    A = np.array([[1, 2], [3, 4]])
    hw_assert (p2(A) == -2)

def test_p3():
    start = time.time()
    p3()
    end = time.time()
    hw_assert (abs(end - start - 1.0) < 0.5)


def hw_assert(X):
    if X:
        print('\t PASS')
    else:
        print('\t FAIL')


test_p1()
test_p2()
test_p3()