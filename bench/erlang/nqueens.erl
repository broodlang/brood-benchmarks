#!/usr/bin/env escript
%%! -mode(compile)
main(_) -> io:format("~w~n", [solve(0, bench_n(10), [])]).
bench_n(D) -> case os:getenv("BENCH_N") of false -> D; V -> list_to_integer(V) end.
safe(_C, [], _D) -> true;
safe(C, [P | Rest], D) ->
    if P == C -> false; P - C == D -> false; P - C == -D -> false; true -> safe(C, Rest, D+1) end.
solve(Row, N, _P) when Row == N -> 1;
solve(Row, N, Placed) ->
    lists:foldl(fun(C, Acc) ->
        case safe(C, Placed, 1) of true -> Acc + solve(Row+1, N, [C|Placed]); false -> Acc end
    end, 0, lists:seq(0, N-1)).
