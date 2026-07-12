namespace Bench;
using System.Threading.Channels;
static class Pingpong
{
    // Two tasks bounce a token N round trips via channels. Checksum = N.
    public static async Task Run(int n)
    {
        var toW = Channel.CreateUnbounded<int>();
        var fromW = Channel.CreateUnbounded<int>();
        var worker = Task.Run(async () =>
        {
            while (true)
            {
                var m = await toW.Reader.ReadAsync();
                if (m < 0) break;
                await fromW.Writer.WriteAsync(m);
            }
        });
        int k = 0;
        while (k < n)
        {
            await toW.Writer.WriteAsync(k);
            await fromW.Reader.ReadAsync();
            k++;
        }
        await toW.Writer.WriteAsync(-1);
        await worker;
        Console.WriteLine(k);
    }
}
