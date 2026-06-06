namespace Bench;
static class Http
{
    // Concurrent HTTP: fire N GETs at the local server (each sleeps ~20ms
    // server-side) and count the 200s — async/await on the thread pool, all N
    // in flight at once. MaxConnectionsPerServer = N so nothing queues (the
    // analog of node's agent:false). Checksum = N.
    public static async Task Run(int n)
    {
        var handler = new SocketsHttpHandler { MaxConnectionsPerServer = n };
        using var client = new HttpClient(handler);
        var tasks = new Task<int>[n];
        for (int i = 0; i < n; i++)
        {
            tasks[i] = Task.Run(async () =>
            {
                try
                {
                    using var resp = await client.GetAsync("http://127.0.0.1:8089/");
                    return resp.IsSuccessStatusCode ? 1 : 0;
                }
                catch { return 0; }
            });
        }
        var results = await Task.WhenAll(tasks);
        Console.WriteLine(results.Sum());
    }
}
