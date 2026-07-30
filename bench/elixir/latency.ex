defmodule Blatency do
  # Latency under a fixed arrival rate, open loop. See bench/brood/latency.blsp for the full
  # rationale: request i is scheduled at start + i*(1s/rate) whether or not the system keeps
  # up, and latency is measured from that scheduled instant, so queueing delay lands in the
  # number instead of being hidden by a closed loop. Every 20th request occupies ~500us of
  # CPU — calibrated per runtime at startup, as real work rather than a clock spin — and the
  # percentiles cover the OTHER 95%, so the question is what a busy handler does to everyone
  # else. Checksum covers only the cheap round, so the calibrated amount never enters it.
  @rate 20_000
  @gap div(1_000_000_000, @rate)
  @cheap 40
  @fat_ns 500_000

  def work(k, j, acc) when j >= k, do: acc

  def work(k, j, acc) do
    v = {j, j + 1, j + 2, j + 3}
    work(k, j + 1, acc + elem(v, 0) + elem(v, 1) + elem(v, 2) + elem(v, 3))
  end

  defp now, do: System.monotonic_time(:nanosecond)

  defp warm(0, _k), do: :ok
  defp warm(reps, k), do: (work(k, 0, 0); warm(reps - 1, k))

  defp best_work_ns(0, _k, best), do: best

  defp best_work_ns(reps, k, best) do
    t = now()
    work(k, 0, 0)
    dt = now() - t
    best_work_ns(reps - 1, k, if(best == 0 or dt < best, do: dt, else: best))
  end

  defp calibrate(k) do
    dt = best_work_ns(9, k, 0)
    if dt < 200_000, do: calibrate(k * 2), else: div(k * @fat_ns, dt)
  end

  def collector(to, 0, lats, sum), do: send(to, {:all, lats, sum})

  def collector(to, left, lats, sum) do
    receive do
      {:done, lat, r} ->
        collector(to, left - 1, if(lat < 0, do: lats, else: [lat | lats]), sum + r)
    end
  end

  defp spin_until(t), do: if(now() >= t, do: :ok, else: spin_until(t))

  defp dispatch(i, n, _start, _to, _fu) when i >= n, do: :ok

  defp dispatch(i, n, start, to, fu) do
    sched = start + i * @gap
    spin_until(sched)

    spawn(fn ->
      r = work(@cheap, 0, 0)
      fat? = rem(i, 20) == 0
      if fat?, do: work(fu, 0, 0)
      # -1 for a fat request: its own latency is >=500us by construction, so counting it would
      # fill every high percentile with fat requests and hide what they did to the ordinary
      # ones queued behind them.
      send(to, {:done, if(fat?, do: -1, else: div(now() - sched, 1000)), r})
    end)

    dispatch(i + 1, n, start, to, fu)
  end

  defp pct(v, p, n), do: elem(v, min(n - 1, div(p * n, 100)))

  def main do
    n = String.to_integer(System.get_env("BENCH_N") || "50000")
    warm(60, 5000)
    fu = calibrate(1000)
    fat_measured = div(best_work_ns(5, fu, 0), 1000)

    me = self()
    coll = spawn(fn -> collector(me, n, [], 0) end)
    t0 = now()
    dispatch(0, n, t0, coll, fu)

    {lats, sum} =
      receive do
        {:all, l, s} -> {l, s}
      after
        600_000 -> {[], 0}
      end

    elapsed = now() - t0
    v = lats |> Enum.sort() |> List.to_tuple()
    cnt = tuple_size(v)
    IO.puts("#metric fat_units=#{fu}")
    IO.puts("#metric fat_measured_us=#{fat_measured}")
    IO.puts("#metric ordinary_n=#{cnt}")
    IO.puts("#metric p50_us=#{pct(v, 50, cnt)}")
    IO.puts("#metric p99_us=#{pct(v, 99, cnt)}")
    IO.puts("#metric p999_us=#{elem(v, min(cnt - 1, div(999 * cnt, 1000)))}")
    IO.puts("#metric max_us=#{elem(v, cnt - 1)}")
    IO.puts("#metric sustained_rps=#{div(n * 1_000_000_000, elapsed)}")
    IO.puts(sum)
  end
end
