defmodule B do
  def prime?(n) when n < 2, do: false
  def prime?(n), do: check(n, 2, trunc(:math.sqrt(n)))
  defp check(_n, d, limit) when d > limit, do: true
  defp check(n, d, limit), do: if(rem(n, d) == 0, do: false, else: check(n, d + 1, limit))
end

n = String.to_integer(System.get_env("BENCH_N") || "20000")
IO.puts(Enum.count(2..(n - 1), &B.prime?/1))
