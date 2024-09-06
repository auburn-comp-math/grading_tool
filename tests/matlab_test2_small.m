hw00_worker = hw00();

hw_assert(hw00_worker.p2(1) == 1)
hw_assert(hw00_worker.p2(-1) == -1)
hw_assert(hw00_worker.p2([[1 0];[0 1]]) == 1)
hw_assert(hw00_worker.p2([[1 1];[1 1]]) == 0)
hw_assert(hw00_worker.p2([[1 3];[3 1]]) == -8)

function hw_assert(X)
    if X; fprintf('\t PASS\n'); else; fprintf('\t FAIL\n'); end
end