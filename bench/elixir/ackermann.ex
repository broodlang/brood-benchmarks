defmodule Backermann do
  # Ackermann ack(3,9) summed N times. Deep double-recursion (depth ~4093).
  # Checksum = N * ack(3,9) = N * 4093.
  def ack(0, k), do: k + 1
  def ack(m, 0), do: ack(m - 1, 1)
  def ack(m, k), do: ack(m - 1, ack(m, k - 1))

  def main do
    n = String.to_integer(System.get_env("BENCH_N") || "6")
    total = Enum.reduce(1..n, 0, fn _, acc -> acc + ack(3, 9) end)
    IO.puts(total)
  end
end
