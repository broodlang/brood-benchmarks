#!/usr/bin/env escript
%%! -mode(compile)
%% filter/map/reduce pipeline over a range: keep multiples of 3 or 5, square, sum.
main(_) ->
    N = bench_n(100000),
    Sum = pipe(0, N, 0),
    io:format("~w~n", [Sum]).
bench_n(D) -> case os:getenv("BENCH_N") of false -> D; V -> list_to_integer(V) end.
pipe(I, N, Acc) when I >= N -> Acc;
pipe(I, N, Acc) ->
    case (I rem 3 =:= 0) orelse (I rem 5 =:= 0) of
        true -> pipe(I+1, N, Acc + I*I);
        false -> pipe(I+1, N, Acc)
    end.
