defmodule B do
  def prime?(n) when n < 2, do: false
  def prime?(n), do: check(n, 2)
  defp check(n, d) when d * d > n, do: true
  defp check(n, d), do: if(rem(n, d) == 0, do: false, else: check(n, d + 1))
end

n = String.to_integer(System.get_env("BENCH_N") || "20000")
IO.puts(Enum.count(2..(n - 1), &B.prime?/1))
