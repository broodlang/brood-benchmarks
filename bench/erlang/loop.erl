#!/usr/bin/env escript
%%! -mode(compile)
main(_) -> io:format("~w~n", [loop(0, bench_n(30000000), 0)]).
bench_n(D) -> case os:getenv("BENCH_N") of false -> D; V -> list_to_integer(V) end.
loop(I, N, Acc) when I >= N -> Acc;
loop(I, N, Acc) -> loop(I+1, N, Acc+I).
