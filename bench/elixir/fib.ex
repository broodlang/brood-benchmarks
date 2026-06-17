defmodule Bfib do
  def fib(n) when n < 2, do: n
  def fib(n), do: fib(n - 1) + fib(n - 2)

  def main do
    n = String.to_integer(System.get_env("BENCH_N") || "35")
    IO.puts(fib(n))
  end
end
