defmodule Bsupervisor do
  # Supervision at scale: start N supervised children under a DynamicSupervisor, then
  # retire a quarter of them and let the supervisor restart every one.
  #
  # See bench/brood/supervisor.blsp for the full rationale. In short: this measures the
  # supervisor's own bookkeeping (add a child, find it when its exit arrives, replace
  # it), not process spawn cost. The retired children exit :normal and are :permanent,
  # so they are restarted without either runtime logging N crash reports. Children
  # announce to a REGISTERED name rather than closing over the collector pid, and the
  # collector is a SEPARATE process so the driver's mailbox stays empty while it fills
  # the supervisor (otherwise the row measures mailbox-backlog scanning, not supervision).
  #
  # Checksum = N + N/4.

  def child do
    case Process.whereis(:bench_collector) do
      nil -> :ok
      c -> send(c, {:up, self()})
    end

    receive do
      :retire -> :ok
    end
  end

  def collector(pids, k) do
    receive do
      {:up, p} ->
        collector([p | pids], k + 1)

      {:take, want, from} ->
        send(from, {:pids, Enum.take(pids, want), k})
        collector(pids, k)

      {:count_at_least, want, from} ->
        if k >= want do
          send(from, {:reached, k})
          collector(pids, k)
        else
          send(self(), {:count_at_least, want, from})
          collector(pids, k)
        end
    end
  end

  def main do
    n = String.to_integer(System.get_env("BENCH_N") || "20000")
    retire = div(n, 4)
    Process.register(spawn(fn -> collector([], 0) end), :bench_collector)

    {:ok, sup} =
      DynamicSupervisor.start_link(
        strategy: :one_for_one,
        max_restarts: 100_000_000,
        max_seconds: 60
      )

    spec = %{id: :child, start: {Task, :start_link, [&Bsupervisor.child/0]}, restart: :permanent}
    Enum.each(1..n, fn _ -> {:ok, _} = DynamicSupervisor.start_child(sup, spec) end)

    await_count(n)
    victims(retire) |> Enum.each(fn p -> send(p, :retire) end)
    total = await_count(n + retire)

    IO.puts(total)
  end

  defp await_count(want) do
    send(Process.whereis(:bench_collector), {:count_at_least, want, self()})

    receive do
      {:reached, k} -> k
    end
  end

  defp victims(want) do
    send(Process.whereis(:bench_collector), {:take, want, self()})

    receive do
      {:pids, ps, _} -> ps
    end
  end
end
