defmodule Bpersistentmap do
  import Bitwise
  # Read-modify-write churn on a persistent Map over a 50k key space.
  # Checksum = sum of key*value over the map.
  def main do
    n = String.to_integer(System.get_env("BENCH_N") || "300000")
    m = 50000

    {_, map} =
      Enum.reduce(1..n, {123_456_789, %{}}, fn _, {x, acc} ->
        x2 = band(x * 1_103_515_245 + 12_345, 0x7FFFFFFF)
        key = rem(x2, m)
        d = 1 + rem(key, 7)
        {x2, Map.update(acc, key, d, &(&1 + d))}
      end)

    total = Enum.reduce(map, 0, fn {k, v}, acc -> acc + k * v end)
    IO.puts(total)
  end
end
