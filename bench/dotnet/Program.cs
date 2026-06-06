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
    case "fib":        Bench.Fib.Run(N(30)); break;
    case "loop":       Bench.Loop.Run(N(3000000)); break;
    case "reduce":     Bench.Reduce.Run(N(1000000)); break;
    case "primes":     Bench.Primes.Run(N(20000)); break;
    case "collatz":    Bench.Collatz.Run(N(30000)); break;
    case "mandelbrot": Bench.Mandelbrot.Run(N(128)); break;
    case "matmul":     Bench.Matmul.Run(N(80)); break;
    case "strings":    Bench.Strings.Run(N(50000)); break;
    case "wordcount":  Bench.Wordcount.Run(N(100000)); break;
    case "bintree":    Bench.Bintree.Run(N(40)); break;
    case "sort":       Bench.Sort.Run(N(50000)); break;
    case "pfib":       Bench.Pfib.Run(N(28)); break;
    case "http":       await Bench.Http.Run(N(500)); break;
    default:
        Console.Error.WriteLine($"unknown benchmark: {name}");
        Environment.Exit(1);
        break;
}
