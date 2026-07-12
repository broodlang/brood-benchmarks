namespace Bench;
using System.Threading.Channels;
static class Ring
{
    // A ring of N tasks; a token travels around +1/hop for LAPS laps (N*LAPS hops).
    // Checksum = N*LAPS.
    public static async Task Run(int n)
    {
        const int LAPS = 5000;
        long total = (long)n * LAPS;
        var chans = new Channel<long>[n];
        for (int i = 0; i < n; i++) chans[i] = Channel.CreateUnbounded<long>();
        var done = new TaskCompletionSource<long>();
        for (int i = 0; i < n; i++)
        {
            var inbox = chans[i];
            var next = chans[(i + 1) % n];
            _ = Task.Run(async () =>
            {
                while (true)
                {
                    var v = await inbox.Reader.ReadAsync();
                    if (v >= total) { done.TrySetResult(v); break; }
                    await next.Writer.WriteAsync(v + 1);
                }
            });
        }
        await chans[0].Writer.WriteAsync(0);
        Console.WriteLine(await done.Task);
    }
}
