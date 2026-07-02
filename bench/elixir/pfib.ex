defmodule Bpfib do
  # Parallel fib: compute fib(N) in 100 tasks at once, summed. Task.async_stream
  # fans the work across the BEAM's schedulers (one per core). Checksum = 100*fib(N).
  def fib(n) when n < 2, do: n
  def fib(n), do: fib(n - 1) + fib(n - 2)

  def main do
    n = String.to_integer(System.get_env("BENCH_N") || "31")
    tasks = 100

    total =
      1..tasks
      |> Task.async_stream(fn _ -> fib(n) end,
        max_concurrency: tasks,
        ordered: false,
        timeout: :infinity
      )
      |> Enum.reduce(0, fn {:ok, v}, acc -> acc + v end)

    IO.puts(total)
  end
end
