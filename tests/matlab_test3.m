hw00_worker = hw00();

for i = 1:10
    start_time = tic;
    hw00_worker.p3();
    elapsed = toc(start_time);

    hw_assert(abs(elapsed - 1.0) < 0.05);
end

function hw_assert(X)
    if X; fprintf('\t PASS\n'); else; fprintf('\t FAIL\n'); end
end