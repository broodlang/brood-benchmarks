defmodule Bnbody do
  # N-body sim; canonical formulation shared by all 7 langs (see node/nbody.js).
  # Immutable/functional (bodies = a tuple of 5 body-tuples {x,y,z,vx,vy,vz,m}).
  # Checksum = floor(energy*1e9 + 0.5).
  @dt 0.01

  def main do
    n = String.to_integer(System.get_env("BENCH_N") || "50000")
    pi = 3.141592653589793
    sm = 4 * pi * pi
    dpy = 365.24

    bodies = {
      {0.0, 0.0, 0.0, 0.0, 0.0, 0.0, sm},
      {4.84143144246472090e+00, -1.16032004402742839e+00, -1.03622044471123109e-01,
       1.66007664274403694e-03 * dpy, 7.69901118419740425e-03 * dpy, -6.90460016972063023e-05 * dpy,
       9.54791938424326609e-04 * sm},
      {8.34336671824457987e+00, 4.12479856412430479e+00, -4.03523417114321381e-01,
       -2.76742510726862411e-03 * dpy, 4.99852801234917238e-03 * dpy, 2.30417297573763929e-05 * dpy,
       2.85885980666130812e-04 * sm},
      {1.28943695621391310e+01, -1.51111514016986312e+01, -2.23307578892655734e-01,
       2.96460137564761618e-03 * dpy, 2.37847173959480950e-03 * dpy, -2.96589568540237556e-05 * dpy,
       4.36624404335156298e-05 * sm},
      {1.53796971148509165e+01, -2.59193146099879641e+01, 1.79258772950371181e-01,
       2.68067772490389322e-03 * dpy, 1.62824170038242295e-03 * dpy, -9.51592254519715870e-05 * dpy,
       5.15138902046611451e-05 * sm}
    }

    bodies = offset(bodies, sm)
    bodies = advance_n(bodies, n)
    e = energy(bodies)
    IO.puts(floor(e * 1.0e9 + 0.5))
  end

  defp offset(b, sm) do
    {px, py, pz} =
      Enum.reduce(0..4, {0.0, 0.0, 0.0}, fn i, {px, py, pz} ->
        bi = elem(b, i)
        m = elem(bi, 6)
        {px + elem(bi, 3) * m, py + elem(bi, 4) * m, pz + elem(bi, 5) * m}
      end)

    sun = elem(b, 0) |> put_elem(3, -px / sm) |> put_elem(4, -py / sm) |> put_elem(5, -pz / sm)
    put_elem(b, 0, sun)
  end

  defp advance_n(b, 0), do: b
  defp advance_n(b, n), do: advance_n(advance(b), n - 1)

  defp advance(b) do
    nb =
      Enum.reduce(0..4, b, fn i, acc ->
        bi = elem(b, i)
        {nvx, nvy, nvz} = newvel(b, i, 0, elem(bi, 3), elem(bi, 4), elem(bi, 5))
        put_elem(acc, i, bi |> put_elem(3, nvx) |> put_elem(4, nvy) |> put_elem(5, nvz))
      end)

    Enum.reduce(0..4, nb, fn i, acc ->
      bi = elem(nb, i)
      x = elem(bi, 0) + @dt * elem(bi, 3)
      y = elem(bi, 1) + @dt * elem(bi, 4)
      z = elem(bi, 2) + @dt * elem(bi, 5)
      put_elem(acc, i, bi |> put_elem(0, x) |> put_elem(1, y) |> put_elem(2, z))
    end)
  end

  defp newvel(_b, _i, 5, vx, vy, vz), do: {vx, vy, vz}
  defp newvel(b, i, i, vx, vy, vz), do: newvel(b, i, i + 1, vx, vy, vz)

  defp newvel(b, i, j, vx, vy, vz) do
    bi = elem(b, i)
    bj = elem(b, j)
    dx = elem(bi, 0) - elem(bj, 0)
    dy = elem(bi, 1) - elem(bj, 1)
    dz = elem(bi, 2) - elem(bj, 2)
    dsq = dx * dx + dy * dy + dz * dz
    dist = :math.sqrt(dsq)
    mag = @dt / (dsq * dist)
    mj = elem(bj, 6)
    newvel(b, i, j + 1, vx - dx * mj * mag, vy - dy * mj * mag, vz - dz * mj * mag)
  end

  defp energy(b) do
    ke =
      Enum.reduce(0..4, 0.0, fn i, e ->
        bi = elem(b, i)
        vx = elem(bi, 3)
        vy = elem(bi, 4)
        vz = elem(bi, 5)
        e + 0.5 * elem(bi, 6) * (vx * vx + vy * vy + vz * vz)
      end)

    potential(b, 0, 1, ke)
  end

  defp potential(_b, 5, _j, e), do: e
  defp potential(b, i, j, e) when j > 4, do: potential(b, i + 1, i + 2, e)

  defp potential(b, i, j, e) do
    bi = elem(b, i)
    bj = elem(b, j)
    dx = elem(bi, 0) - elem(bj, 0)
    dy = elem(bi, 1) - elem(bj, 1)
    dz = elem(bi, 2) - elem(bj, 2)
    dist = :math.sqrt(dx * dx + dy * dy + dz * dz)
    potential(b, i, j + 1, e - elem(bi, 6) * elem(bj, 6) / dist)
  end
end
