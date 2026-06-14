defmodule B do
  def make(0), do: nil
  def make(d), do: {make(d - 1), make(d - 1)}
  def check(nil), do: 1
  def check({l, r}), do: 1 + check(l) + check(r)
end

n = String.to_integer(System.get_env("BENCH_N") || "200")
depth = 12
IO.puts(Enum.reduce(1..n, 0, fn _, acc -> acc + B.check(B.make(depth)) end))
