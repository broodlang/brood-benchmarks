// Dispatcher: `brood-bench <name>` runs one benchmark. BENCH_N (env) sets the
// workload size, mirroring the other languages; each benchmark has the same
// default baked in. One project, one file per benchmark, so they diff side by
// side with the .blsp/.exs/.py/.js/.rb versions.
static int N(int def) =>
    int.TryParse(Environment.GetEnvironmentVariable("BENCH_N"), out var v) ? v : def;

var name = args.Length > 0 ? args[0] : "";
switch (name)
{
    case "startup":    Bench.Startup.Run(); break;
    case "fib":        Bench.Fib.Run(N(35)); break;
    case "loop":       Bench.Loop.Run(N(30000000)); break;
    case "reduce":     Bench.Reduce.Run(N(5000000)); break;
    case "primes":     Bench.Primes.Run(N(150000)); break;
    case "collatz":    Bench.Collatz.Run(N(250000)); break;
    case "mandelbrot": Bench.Mandelbrot.Run(N(540)); break;
    case "matmul":     Bench.Matmul.Run(N(175)); break;
    case "strings":    Bench.Strings.Run(N(500000)); break;
    case "wordcount":  Bench.Wordcount.Run(N(750000)); break;
    case "bintree":    Bench.Bintree.Run(N(200)); break;
    case "sort":       Bench.Sort.Run(N(375000)); break;
    case "latency":    Bench.Latency.Run(N(50000)); break;
    case "nqueens":    Bench.Nqueens.Run(N(10)); break;
    case "errors":     Bench.Errors.Run(N(200000)); break;
    case "errors-deep": Bench.ErrorsDeep.Run(N(50000)); break;
    case "pipeline":   Bench.Pipeline.Run(N(100000)); break;
    case "ackermann":  Bench.Ackermann.Run(N(6)); break;
    case "sieve":      Bench.Sieve.Run(N(1000000)); break;
    case "persistent-map": Bench.PersistentMap.Run(N(300000)); break;
    case "nbody":      Bench.Nbody.Run(N(50000)); break;
    case "json":       Bench.Json.Run(N(2000)); break;
    case "regex":      Bench.RegexBench.Run(N(20000)); break;
    case "base64":     Bench.Base64.Run(N(50000)); break;
    case "pfib":       Bench.Pfib.Run(N(31)); break;
    case "spawn":      await Bench.Spawn.Run(N(10000)); break;
    case "spawn-live": await Bench.SpawnLive.Run(N(300000)); break;
    case "http":       await Bench.Http.Run(N(500)); break;
    case "pingpong":   await Bench.Pingpong.Run(N(100000)); break;
    case "ring":       await Bench.Ring.Run(N(200)); break;
    default:
        Console.Error.WriteLine($"unknown benchmark: {name}");
        Environment.Exit(1);
        break;
}
