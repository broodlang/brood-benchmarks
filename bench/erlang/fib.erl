#!/usr/bin/env escript
%%! -mode(compile)
main(_) -> io:format("~w~n", [fib(bench_n(35))]).
bench_n(D) -> case os:getenv("BENCH_N") of false -> D; V -> list_to_integer(V) end.
fib(N) when N < 2 -> N;
fib(N) -> fib(N-1) + fib(N-2).
