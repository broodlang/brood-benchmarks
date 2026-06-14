defmodule Q do
  def safe?(_c, [], _d), do: true

  def safe?(c, [p | rest], d) do
    cond do
      p == c -> false
      p - c == d -> false
      p - c == -d -> false
      true -> safe?(c, rest, d + 1)
    end
  end

  def solve(row, n, _placed) when row == n, do: 1

  def solve(row, n, placed) do
    Enum.reduce(0..(n - 1), 0, fn c, acc ->
      if safe?(c, placed, 1), do: acc + solve(row + 1, n, [c | placed]), else: acc
    end)
  end
end

n = String.to_integer(System.get_env("BENCH_N") || "10")
IO.puts(Q.solve(0, n, []))
