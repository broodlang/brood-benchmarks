#!/usr/bin/env escript
%%! -mode(compile)
%% error propagation: throw `depth` non-tail frames down, catch at the top, N times.
main(_) ->
    N = bench_n(50000), Md = 1000000007, Depth = 50,
    Acc = lists:foldl(fun(I, Acc) ->
        try descend(Depth, I)
        catch throw:{bench_error, V} -> Acc + V end
    end, 0, lists:seq(0, N-1)),
    io:format("~w~n", [Acc rem Md]).
bench_n(D) -> case os:getenv("BENCH_N") of false -> D; V -> list_to_integer(V) end.
descend(0, I) -> throw({bench_error, I rem 100});
descend(D, I) -> 1 + descend(D-1, I).
