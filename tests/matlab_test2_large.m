hw00_worker = hw00();

hw_assert(hw00_worker.p2(5 * eye(3)) == 125)
hw_assert(hw00_worker.p2(5 * eye(6)) == 5^6)
hw_assert(hw00_worker.p2(magic(4)) == 0)
hw_assert(hw00_worker.p2(magic(6)) == 0)
hw_assert(hw00_worker.p2(magic(8)) == 0)

function hw_assert(X)
    if X; fprintf('\t PASS\n'); else; fprintf('\t FAIL\n'); end
end