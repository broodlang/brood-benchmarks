defmodule B do
  def fib(n) when n < 2, do: n
  def fib(n), do: fib(n - 1) + fib(n - 2)
end

n = String.to_integer(System.get_env("BENCH_N") || "37")
IO.puts(B.fib(n))
