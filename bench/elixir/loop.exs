defmodule B do
  def loop(i, n, acc) when i >= n, do: acc
  def loop(i, n, acc), do: loop(i + 1, n, acc + i)
end

n = String.to_integer(System.get_env("BENCH_N") || "30000000")
IO.puts(B.loop(0, n, 0))
