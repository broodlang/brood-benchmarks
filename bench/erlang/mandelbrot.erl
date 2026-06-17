#!/usr/bin/env escript
%%! -mode(compile)
%% carry xx=x*x and yy=y*y so each is computed once per iteration, not ~5x
main(_) ->
    N = bench_n(540), Maxi = 100,
    Total = lists:foldl(fun(Py, AccPy) ->
        Y0 = Py / N * 3.0 - 1.5,
        lists:foldl(fun(Px, Acc) ->
            X0 = Px / N * 3.0 - 2.0,
            Acc + iter(0.0, 0.0, 0.0, 0.0, X0, Y0, 0, Maxi)
        end, AccPy, lists:seq(0, N-1))
    end, 0, lists:seq(0, N-1)),
    io:format("~w~n", [Total]).
bench_n(D) -> case os:getenv("BENCH_N") of false -> D; V -> list_to_integer(V) end.
iter(X, Y, XX, YY, X0, Y0, I, Maxi) ->
    case (XX + YY =< 4.0) andalso (I < Maxi) of
        true ->
            NY = 2.0 * X * Y + Y0,
            NX = XX - YY + X0,
            iter(NX, NY, NX*NX, NY*NY, X0, Y0, I+1, Maxi);
        false -> I
    end.
