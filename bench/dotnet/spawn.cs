// Fan out N tasks, each returning its index; WhenAll and sum.
// Task.Run schedules work on the ThreadPool — .NET's lightweight concurrent
// unit. Checksum = N*(N-1)/2.
namespace Bench;
static class Spawn
{
    public static async Task Run(int n)
    {
        var tasks = Enumerable.Range(0, n)
            .Select(i => Task.Run(() => (long)i))
            .ToArray();
        var results = await Task.WhenAll(tasks);
        Console.WriteLine(results.Sum());
    }
}
