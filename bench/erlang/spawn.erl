#!/usr/bin/env escript
%%! -mode(compile)
%% Fan out N processes; each computes fib(15) and sends the result back.
%% Tests BEAM-process spawn + messaging under real CPU work per unit.
%% Checksum = N * fib(15) = N * 610.
main(_) ->
    N = bench_n(10000),
    Parent = self(),
    lists:foreach(fun(_) -> spawn(fun() -> Parent ! {done, fib(15)} end) end, lists:seq(1, N)),
    Total = collect(N, 0),
    io:format("~w~n", [Total]).
bench_n(D) -> case os:getenv("BENCH_N") of false -> D; V -> list_to_integer(V) end.
collect(0, Acc) -> Acc;
collect(K, Acc) -> receive {done, V} -> collect(K-1, Acc+V) end.
fib(N) when N < 2 -> N;
fib(N) -> fib(N-1) + fib(N-2).
