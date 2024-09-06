from hw00 import p1
import numpy as np
import time

def test_p1():
    hw_assert (p1(0) == 0)
    hw_assert (p1(1) == 1)
    hw_assert (p1(2) == 1)
    hw_assert (p1(3) == 2)
    hw_assert (p1(4) == 4)
    hw_assert (p1(5) == 7)
    hw_assert (p1(6) == 13)
    hw_assert (p1(7) == 24)
    hw_assert (p1(8) == 44)
    hw_assert (p1(9) == 81)

def hw_assert(X):
    if X:
        print('\t PASS')
    else:
        print('\t FAIL')

test_p1()