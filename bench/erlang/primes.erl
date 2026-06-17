#!/usr/bin/env escript
%%! -mode(compile)
main(_) ->
    N = bench_n(150000),
    Count = length([K || K <- lists:seq(2, N-1), is_prime(K)]),
    io:format("~w~n", [Count]).
bench_n(D) -> case os:getenv("BENCH_N") of false -> D; V -> list_to_integer(V) end.
is_prime(N) when N < 2 -> false;
is_prime(N) -> check(N, 2, trunc(math:sqrt(N))).
check(_N, D, Limit) when D > Limit -> true;
check(N, D, Limit) -> case N rem D of 0 -> false; _ -> check(N, D+1, Limit) end.
