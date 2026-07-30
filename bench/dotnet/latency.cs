// Latency under a fixed arrival rate, open loop. See bench/brood/latency.blsp for the full
// rationale: request i is scheduled at start + i*(1s/rate) whether or not the system keeps up,
// and latency is measured from that scheduled instant, so queueing delay lands in the number.
// Every 20th request OCCUPIES 500us — defined in time, not work units, so the row asks what a
// busy handler does to the ~10 requests behind it rather than re-measuring arithmetic speed.
// Handlers go to the thread pool, which is how a .NET server serves concurrent requests.
namespace Bench;

static class Latency
{
    const int Rate = 20000;
    const long GapNs = 1_000_000_000L / Rate;
    const int Cheap = 40;
    const long FatNs = 500_000;

    static long Work(int k)
    {
        long acc = 0;
        for (int j = 0; j < k; j++)
        {
            var v = new int[] { j, j + 1, j + 2, j + 3 };
            acc += v[0] + v[1] + v[2] + v[3];
        }
        return acc;
    }

    static long NowNs() => (long)(System.Diagnostics.Stopwatch.GetTimestamp()
                                  * (1_000_000_000.0 / System.Diagnostics.Stopwatch.Frequency));

    static void SpinUntil(long t) { while (NowNs() < t) { } }

    static long BestWorkNs(int reps, int k)
    {
        long best = 0;
        for (int i = 0; i < reps; i++)
        {
            long t = NowNs(); Work(k); long dt = NowNs() - t;
            if (best == 0 || dt < best) best = dt;
        }
        return best;
    }

    // ~500us of real work in THIS runtime, warm-calibrated. Real work rather than a clock
    // spin for two reasons: it allocates, so the GC participates the way a handler's would;
    // and spinning on many pool threads crashed the runtime outright here — `Internal CLR
    // error (0x80131506)` in roughly 3 runs of 10, reproducible with both Task.Run and
    // ThreadPool.UnsafeQueueUserWorkItem. Reported below so a mis-calibration is visible.
    static int Calibrate()
    {
        for (int i = 0; i < 60; i++) Work(5000);
        int k = 1000;
        for (;;)
        {
            long dt = BestWorkNs(9, k);
            if (dt >= 200_000) return (int)((long)k * FatNs / dt);
            k *= 2;
        }
    }

    public static void Run(int n)
    {
        // Task.Run + WhenAll, the same shape as the other .NET ports here. (An earlier version
        // used ThreadPool.UnsafeQueueUserWorkItem and hit an intermittent
        // "Internal CLR error (0x80131506)" roughly one run in seven with spinning callbacks.)
        int fatUnits = Calibrate();
        long fatMeasured = BestWorkNs(5, fatUnits) / 1000;

        var tasks = new Task<(long lat, long r)>[n];
        long t0 = NowNs();

        for (int i = 0; i < n; i++)
        {
            long sched = t0 + i * GapNs;
            SpinUntil(sched);
            int idx = i;
            tasks[i] = Task.Run(() =>
            {
                long r = Work(Cheap);
                bool fat = idx % 20 == 0;
                if (fat) Work(fatUnits);
                // -1 marks a fat request: its own latency is >=500us by construction, so counting
                // it would fill every high percentile with fat requests and hide what they did to
                // the ordinary ones queued behind them.
                return (fat ? -1L : (NowNs() - sched) / 1000, r);
            });
        }

        Task.WaitAll(tasks);
        long elapsed = NowNs() - t0;
        long sum = 0;
        foreach (var t in tasks) sum += t.Result.r;

        var ord = tasks.Select(t => t.Result.lat).Where(l => l >= 0).OrderBy(l => l).ToArray();
        int m = ord.Length;
        long Pct(int p) => ord[Math.Min(m - 1, (int)((long)p * m / 100))];
        Console.WriteLine($"#metric fat_units={fatUnits}");
        Console.WriteLine($"#metric fat_measured_us={fatMeasured}");
        Console.WriteLine($"#metric ordinary_n={m}");
        Console.WriteLine($"#metric p50_us={Pct(50)}");
        Console.WriteLine($"#metric p99_us={Pct(99)}");
        Console.WriteLine($"#metric p999_us={ord[Math.Min(m - 1, (int)(999L * m / 1000))]}");
        Console.WriteLine($"#metric max_us={ord[m - 1]}");
        Console.WriteLine($"#metric sustained_rps={n * 1_000_000_000L / elapsed}");
        Console.WriteLine(sum);
    }
}
