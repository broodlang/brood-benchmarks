# Fan out N processes; each computes fib(15) and sends the result back.
# Tests BEAM-process spawn + messaging under real CPU work per unit.
# Checksum = N * fib(15) = N * 610.
defmodule B do
  def fib(n) when n < 2, do: n
  def fib(n), do: fib(n - 1) + fib(n - 2)
end

n = String.to_integer(System.get_env("BENCH_N") || "20000")
parent = self()

Enum.each(1..n, fn _ -> spawn(fn -> send(parent, {:done, B.fib(15)}) end) end)

total = Enum.reduce(1..n, 0, fn _, acc -> receive do {:done, v} -> acc + v end end)
IO.puts(total)
