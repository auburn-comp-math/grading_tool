from hw00 import p3
import numpy as np
import time

def test_p3():
    for i in range(10):
        start = time.time()
        p3()
        end = time.time()
        hw_assert (abs(end - start - 1.0) < 0.05)

def hw_assert(X):
    if X:
        print('\t PASS')
    else:
        print('\t FAIL')

test_p3()
