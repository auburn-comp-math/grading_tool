hw00_worker = hw00();

hw_assert(hw00_worker.p1(0) == 0)
hw_assert(hw00_worker.p1(1) == 1)
hw_assert(hw00_worker.p1(2) == 1)
hw_assert(hw00_worker.p1(3) == 2)
hw_assert(hw00_worker.p1(4) == 4)
hw_assert(hw00_worker.p1(5) == 7)
hw_assert(hw00_worker.p1(6) == 13)
hw_assert(hw00_worker.p1(7) == 24)
hw_assert(hw00_worker.p1(8) == 44)
hw_assert(hw00_worker.p1(9) == 81)

function hw_assert(X)
    if X; fprintf('\t PASS\n'); else; fprintf('\t FAIL\n'); end
end