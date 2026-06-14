using System.Linq;

namespace Bench;
static class Reduce
{
    public static void Run(int n)
    {
        // higher-order fold: Aggregate applies a delegate per element over a
        // range — not a hand-rolled for-loop (that's `loop`).
        long acc = Enumerable.Range(0, n).Aggregate(0L, (a, b) => a + b);
        Console.WriteLine(acc);
    }
}
