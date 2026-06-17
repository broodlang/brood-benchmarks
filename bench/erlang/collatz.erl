#!/usr/bin/env escript
%%! -mode(compile)
main(_) ->
    N = bench_n(250000),
    io:format("~w~n", [lists:foldl(fun(Start, B) -> max(B, steps(Start, 0)) end, 0, lists:seq(1, N-1))]).
bench_n(D) -> case os:getenv("BENCH_N") of false -> D; V -> list_to_integer(V) end.
steps(1, S) -> S;
steps(N, S) when N rem 2 =:= 0 -> steps(N div 2, S+1);
steps(N, S) -> steps(3*N+1, S+1).
