defmodule Bspawnlive do
  # Hold N units alive, then send each a message it must COPY. See the Brood port for
  # why the payload matters: without it the coroutine runtimes score by doing nothing.
  # On the BEAM the copy is what `send` already does. Checksum = N * (sum(payload) + 1).
  #
  # The payload is a TUPLE, not a list — the BEAM's contiguous fixed-size container, the
  # faithful equivalent of the vector/array every other port uses. Same mapping `nbody`
  # documents. The row's subject is the copy, and a 16-cell cons list is 16 pointer-chased
  # cells where the array ports copy 16 contiguous words, so a list charged Brood and Elixir
  # strictly more work for the same 16 integers.
  #
  # Summed with an `elem/2` walk rather than `Tuple.to_list |> Enum.sum`, which would
  # allocate the very list this avoids — once per unit, 300k times.
  def main do
    n = String.to_integer(System.get_env("BENCH_N") || "300000")
    payload = List.to_tuple(Enum.to_list(0..15))
    parent = self()
    pids = for id <- 1..n, do: spawn(fn -> unit(parent, id) end)
    Enum.each(pids, fn p -> send(p, {:go, payload}) end)
    total = Enum.reduce(1..n, 0, fn _, acc -> receive do {:r, v} -> acc + v end end)
    IO.puts(total)
  end

  defp unit(parent, _id) do
    receive do
      {:go, p} -> send(parent, {:r, tsum(p, 0, tuple_size(p), 0) + 1})
    end
  end

  defp tsum(_t, i, n, acc) when i >= n, do: acc
  defp tsum(t, i, n, acc), do: tsum(t, i + 1, n, acc + elem(t, i))
end
