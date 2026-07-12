defmodule Bsieve do
  # Sieve of Eratosthenes to N. Uses :atomics — OTP's mutable fixed-size integer
  # array, the idiomatic "I need a mutable array" in Elixir. Number j -> index j+1
  # (:atomics is 1-based). Checksum = count of primes <= N.
  def main do
    n = String.to_integer(System.get_env("BENCH_N") || "1000000")
    a = :atomics.new(n + 1, [])
    sieve(a, 2, n)
    IO.puts(count(a, 2, n, 0))
  end

  defp sieve(a, p, n) when p * p > n, do: :ok
  defp sieve(a, p, n) do
    if :atomics.get(a, p + 1) == 0, do: mark(a, p, p * p, n)
    sieve(a, p + 1, n)
  end

  defp mark(_a, _p, j, n) when j > n, do: :ok
  defp mark(a, p, j, n) do
    :atomics.put(a, j + 1, 1)
    mark(a, p, j + p, n)
  end

  defp count(_a, k, n, acc) when k > n, do: acc
  defp count(a, k, n, acc) do
    count(a, k + 1, n, acc + if(:atomics.get(a, k + 1) == 0, do: 1, else: 0))
  end
end
