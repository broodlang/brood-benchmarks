#!/usr/bin/env escript
%%! -mode(compile)
main(_) ->
    N = bench_n(5000000),
    io:format("~w~n", [lists:foldl(fun(X, Acc) -> Acc + X end, 0, lists:seq(0, N-1))]).
bench_n(D) -> case os:getenv("BENCH_N") of false -> D; V -> list_to_integer(V) end.
