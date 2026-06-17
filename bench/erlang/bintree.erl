#!/usr/bin/env escript
%%! -mode(compile)
main(_) ->
    N = bench_n(200), Depth = 12,
    io:format("~w~n", [lists:foldl(fun(_, Acc) -> Acc + check(make(Depth)) end, 0, lists:seq(1, N))]).
bench_n(D) -> case os:getenv("BENCH_N") of false -> D; V -> list_to_integer(V) end.
make(0) -> nil;
make(D) -> {make(D-1), make(D-1)}.
check(nil) -> 1;
check({L, R}) -> 1 + check(L) + check(R).
