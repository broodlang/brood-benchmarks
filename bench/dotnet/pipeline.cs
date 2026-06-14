using System.Linq;

namespace Bench;
static class Pipeline
{
    public static void Run(int n)
    {
        // map / filter / reduce pipeline: square the multiples of 3 or 5, sum them.
        // Cast to long before squaring — i*i exceeds int32 for i past ~46k.
        long total = Enumerable.Range(0, n)
            .Where(i => i % 3 == 0 || i % 5 == 0)
            .Select(i => (long)i * i)
            .Aggregate(0L, (a, b) => a + b);
        Console.WriteLine(total);
    }
}
