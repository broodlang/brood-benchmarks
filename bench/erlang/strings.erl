#!/usr/bin/env escript
%%! -mode(compile)
%% Build a comma-separated string of 0..n-1, then take its length.
main(_) ->
    N = bench_n(500000),
    Parts = [integer_to_binary(I) || I <- lists:seq(0, N-1)],
    S = lists:join(<<",">>, Parts),
    Bin = iolist_to_binary(S),
    io:format("~w~n", [byte_size(Bin)]).
bench_n(D) -> case os:getenv("BENCH_N") of false -> D; V -> list_to_integer(V) end.
