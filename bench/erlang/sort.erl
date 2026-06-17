#!/usr/bin/env escript
%%! -mode(compile)
main(_) ->
    N = bench_n(375000), Mod = 1000000007,
    Data = gen(123456789, [], 0, N),
    Sorted = lists:sort(Data),
    H = lists:foldl(fun(V, Acc) -> (Acc * 31 + V) rem Mod end, 0, Sorted),
    io:format("~w~n", [H]).
bench_n(D) -> case os:getenv("BENCH_N") of false -> D; V -> list_to_integer(V) end.
gen(_X, Acc, I, N) when I >= N -> Acc;
gen(X, Acc, I, N) ->
    X2 = (X * 1103515245 + 12345) band 16#7FFFFFFF,
    gen(X2, [X2 | Acc], I+1, N).
