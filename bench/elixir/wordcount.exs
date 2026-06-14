import Bitwise
n = String.to_integer(System.get_env("BENCH_N") || "750000")
k = 1000

{_, counts} =
  Enum.reduce(1..n, {123_456_789, %{}}, fn _, {x, m} ->
    x2 = band(x * 1_103_515_245 + 12_345, 0x7FFFFFFF)
    key = rem(x2, k)
    {x2, Map.update(m, key, 1, &(&1 + 1))}
  end)

total = Enum.reduce(counts, 0, fn {key, v}, acc -> acc + key * v end)
IO.puts(total)
