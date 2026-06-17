#!/usr/bin/env escript
%%! -mode(compile)
%% A as rows; B stored transposed (Bt[j] is column j) so a cell is a dot product
%% of two lists — no O(n) list indexing.
main(_) ->
    N = bench_n(175), Mod = 1000000007,
    A = [[(I+J) rem 100 || J <- lists:seq(0, N-1)] || I <- lists:seq(0, N-1)],
    Bt = [[(K*J) rem 100 || K <- lists:seq(0, N-1)] || J <- lists:seq(0, N-1)],
    Total = lists:foldl(fun(Row, Acc) ->
        lists:foldl(fun(Col, Acc2) ->
            S = lists:foldl(fun({P, Q}, T) -> T + P*Q end, 0, lists:zip(Row, Col)),
            Acc2 + S
        end, Acc, Bt)
    end, 0, A),
    io:format("~w~n", [Total rem Mod]).
bench_n(D) -> case os:getenv("BENCH_N") of false -> D; V -> list_to_integer(V) end.
