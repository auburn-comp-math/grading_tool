hw00_worker = hw00();

hw_assert(hw00_worker.p1(0) == 0)
hw_assert(hw00_worker.p1(1) == 1)
hw_assert(hw00_worker.p1(2) == 1)
hw_assert(hw00_worker.p1(3) == 2)

hw_assert(hw00_worker.p2(1) == 1)
hw_assert(hw00_worker.p2(-1) == -1)
hw_assert(hw00_worker.p2([[1 0];[0 1]]) == 1)
hw_assert(hw00_worker.p2([[1 1];[1 1]]) == 0)

start_time = tic;
hw00_worker.p3();
elapsed = toc(start_time);

hw_assert(abs(elapsed - 1.0) < 0.5);

function hw_assert(X)
    if X; fprintf('\t PASS\n'); else; fprintf('\t FAIL\n'); end
end