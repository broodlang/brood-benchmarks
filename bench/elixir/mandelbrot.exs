defmodule B do
  # carry xx=x*x and yy=y*y so each is computed once per iteration, not ~5×
  def iter(x, y, xx, yy, x0, y0, i, maxi) do
    if xx + yy <= 4.0 and i < maxi do
      ny = 2.0 * x * y + y0   # uses old x, old y
      nx = xx - yy + x0       # uses old xx, yy
      iter(nx, ny, nx * nx, ny * ny, x0, y0, i + 1, maxi)
    else
      i
    end
  end
end

n = String.to_integer(System.get_env("BENCH_N") || "540")
maxi = 100

total =
  Enum.reduce(0..(n - 1), 0, fn py, accpy ->
    y0 = py / n * 3.0 - 1.5

    Enum.reduce(0..(n - 1), accpy, fn px, acc ->
      x0 = px / n * 3.0 - 2.0
      acc + B.iter(0.0, 0.0, 0.0, 0.0, x0, y0, 0, maxi)
    end)
  end)

IO.puts(total)
