namespace Bench;
static class Pfib
{
    // Parallel fib: compute fib(n) TASKS times at once, summed, across the
    // thread pool (sized to the cores). The idiomatic .NET data-parallel form
    // is Parallel.For with a thread-local partial sum. Checksum = TASKS*fib(n).
    const int TASKS = 100;
    static long Fib(int m) => m < 2 ? m : Fib(m - 1) + Fib(m - 2);
    public static void Run(int n)
    {
        long total = 0;
        Parallel.For(0, TASKS,
            () => 0L,
            (i, _, local) => local + Fib(n),
            local => Interlocked.Add(ref total, local));
        Console.WriteLine(total);
    }
}
