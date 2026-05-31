# Concurrent HTTP: fire N GETs at a local server (each sleeps ~20ms server-side)
# and count the 200s. Uses Erlang's built-in :httpc client, fanned out with
# Task.async_stream across the schedulers. :httpc pools connections per host, so
# we raise max_sessions to N to let them all be in flight at once. Checksum = N.
:inets.start()

n = String.to_integer(System.get_env("BENCH_N") || "500")
:httpc.set_options(max_sessions: n, max_keep_alive_length: 0, max_pipeline_length: 0)

url = ~c"http://127.0.0.1:8089/"

total =
  1..n
  |> Task.async_stream(
    fn _ ->
      case :httpc.request(:get, {url, []}, [timeout: 30_000], []) do
        {:ok, {{_, 200, _}, _, _}} -> 1
        _ -> 0
      end
    end,
    max_concurrency: n,
    ordered: false,
    timeout: :infinity
  )
  |> Enum.reduce(0, fn {:ok, v}, acc -> acc + v end)

IO.puts(total)
