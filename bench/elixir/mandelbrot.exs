defmodule B do
  # new x/y are both computed from the OLD x/y (argument evaluation order)
  def iter(x, y, x0, y0, i, maxi) do
    if x * x + y * y <= 4.0 and i < maxi do
      iter(x * x - y * y + x0, 2.0 * x * y + y0, x0, y0, i + 1, maxi)
    else
      i
    end
  end
end

n = String.to_integer(System.get_env("BENCH_N") || "128")
maxi = 100

total =
  Enum.reduce(0..(n - 1), 0, fn py, accpy ->
    y0 = py / n * 3.0 - 1.5

    Enum.reduce(0..(n - 1), accpy, fn px, acc ->
      x0 = px / n * 3.0 - 2.0
      acc + B.iter(0.0, 0.0, x0, y0, 0, maxi)
    end)
  end)

IO.puts(total)
