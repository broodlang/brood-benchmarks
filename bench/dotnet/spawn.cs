// Fan out N tasks; each computes fib(15) and returns the result.
// Tests thread-pool task fan-out under real CPU work per unit.
// Checksum = N * fib(15) = N * 610.
namespace Bench;
static class Spawn
{
    static long Fib(int n) => n < 2 ? n : Fib(n - 1) + Fib(n - 2);

    public static async Task Run(int n)
    {
        var tasks = Enumerable.Range(0, n)
            .Select(_ => Task.Run(() => Fib(15)))
            .ToArray();
        var results = await Task.WhenAll(tasks);
        Console.WriteLine(results.Sum());
    }
}
