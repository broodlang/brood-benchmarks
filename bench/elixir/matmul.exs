n = String.to_integer(System.get_env("BENCH_N") || "175")
mod = 1_000_000_007

# A as rows; B stored transposed (bt[j] is column j) so a cell is a dot product
# of two lists — no O(n) list indexing.
a = for i <- 0..(n - 1), do: for(j <- 0..(n - 1), do: rem(i + j, 100))
bt = for j <- 0..(n - 1), do: for(k <- 0..(n - 1), do: rem(k * j, 100))

total =
  Enum.reduce(a, 0, fn row, acc ->
    Enum.reduce(bt, acc, fn col, acc2 ->
      s = Enum.zip(row, col) |> Enum.reduce(0, fn {p, q}, t -> t + p * q end)
      acc2 + s
    end)
  end)

IO.puts(rem(total, mod))
