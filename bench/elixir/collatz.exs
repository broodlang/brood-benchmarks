defmodule B do
  def steps(1, s), do: s
  def steps(n, s) when rem(n, 2) == 0, do: steps(div(n, 2), s + 1)
  def steps(n, s), do: steps(3 * n + 1, s + 1)
end

n = String.to_integer(System.get_env("BENCH_N") || "250000")
IO.puts(Enum.reduce(1..(n - 1), 0, fn start, b -> max(b, B.steps(start, 0)) end))
