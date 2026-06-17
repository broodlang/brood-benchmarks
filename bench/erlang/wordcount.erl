#!/usr/bin/env escript
%%! -mode(compile)
%% LCG token stream tallied into an immutable map.
main(_) ->
    N = bench_n(750000), K = 1000,
    Counts = gen(123456789, #{}, 0, N, K),
    Total = maps:fold(fun(Key, V, Acc) -> Acc + Key * V end, 0, Counts),
    io:format("~w~n", [Total]).
bench_n(D) -> case os:getenv("BENCH_N") of false -> D; V -> list_to_integer(V) end.
gen(_X, M, I, N, _K) when I >= N -> M;
gen(X, M, I, N, K) ->
    X2 = (X * 1103515245 + 12345) band 16#7FFFFFFF,
    Key = X2 rem K,
    M2 = maps:update_with(Key, fun(C) -> C + 1 end, 1, M),
    gen(X2, M2, I+1, N, K).
