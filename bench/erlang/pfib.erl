#!/usr/bin/env escript
%%! -mode(compile)
%% Parallel fib: compute fib(N) in 100 independent processes at once and sum the
%% results. The scheduler runs them across all cores. Checksum = 100 * fib(N).
main(_) ->
    N = bench_n(28), Tasks = 100,
    Parent = self(),
    lists:foreach(fun(_) -> spawn(fun() -> Parent ! {r, fib(N)} end) end, lists:seq(1, Tasks)),
    Total = collect(Tasks, 0),
    io:format("~w~n", [Total]).
bench_n(D) -> case os:getenv("BENCH_N") of false -> D; V -> list_to_integer(V) end.
collect(0, Acc) -> Acc;
collect(K, Acc) -> receive {r, V} -> collect(K-1, Acc+V) end.
fib(N) when N < 2 -> N;
fib(N) -> fib(N-1) + fib(N-2).
