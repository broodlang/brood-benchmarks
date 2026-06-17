#!/usr/bin/env escript
%%! -mode(compile)
%% Concurrent HTTP: fire N GETs at a local server (each sleeps ~20ms server-side)
%% and count the 200s. Uses Erlang's built-in httpc client, fanned out one
%% process per request. httpc pools connections per host, so we raise
%% max_sessions to N to let them all be in flight at once. Checksum = N.
main(_) ->
    inets:start(),
    N = bench_n(500),
    httpc:set_options([{max_sessions, N}, {max_keep_alive_length, 0}, {max_pipeline_length, 0}]),
    Port = case os:getenv("BENCH_HTTP_PORT") of false -> "8089"; P -> P end,
    Url = "http://127.0.0.1:" ++ Port ++ "/",
    Parent = self(),
    lists:foreach(fun(_) ->
        spawn(fun() ->
            R = case httpc:request(get, {Url, []}, [{timeout, 30000}], []) of
                {ok, {{_, 200, _}, _, _}} -> 1;
                _ -> 0
            end,
            Parent ! {r, R}
        end)
    end, lists:seq(1, N)),
    Total = collect(N, 0),
    io:format("~w~n", [Total]).
bench_n(D) -> case os:getenv("BENCH_N") of false -> D; V -> list_to_integer(V) end.
collect(0, Acc) -> Acc;
collect(K, Acc) -> receive {r, V} -> collect(K-1, Acc+V) end.
