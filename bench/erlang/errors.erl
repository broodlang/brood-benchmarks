#!/usr/bin/env escript
%%! -mode(compile)
%% error handling: raise + recover a value N times.
main(_) ->
    N = bench_n(200000), Md = 1000000007,
    Acc = lists:foldl(fun(I, Acc) ->
        try throw({bench_error, I rem 100})
        catch throw:{bench_error, V} -> Acc + V end
    end, 0, lists:seq(0, N-1)),
    io:format("~w~n", [Acc rem Md]).
bench_n(D) -> case os:getenv("BENCH_N") of false -> D; V -> list_to_integer(V) end.
