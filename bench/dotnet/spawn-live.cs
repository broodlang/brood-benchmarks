// Hold N concurrent units ALIVE at once, then wake each INDIVIDUALLY.
//
// .NET's unit that reaches this scale is an async Task awaiting its own completion
// source: a heap object on the SHARED heap, resumed on the thread pool. It is not an
// isolated process — there is no separate heap, no mailbox, and nothing is copied — so
// read this row's `isolated?` note in BENCHMARKS.md before comparing it to the BEAM.
// .NET's isolated alternative is an OS thread (~1 MB of stack each), which does not
// reach 300k; that cost is measured small and projected in the same note.
//
// Checksum = N.
namespace Bench;

static class SpawnLive
{
    public static async Task Run(int n)
    {
        var payload = Enumerable.Range(0, 16).ToArray();
        var gates = new TaskCompletionSource<int[]>[n];
        var units = new Task<int>[n];
        for (int i = 0; i < n; i++)
        {
            gates[i] = new TaskCompletionSource<int[]>();
            units[i] = Wait(gates[i].Task);
        }
        // Hand each unit a COPY, as `send` would: a reference is a different operation.
        for (int i = 0; i < n; i++) gates[i].SetResult((int[])payload.Clone());
        var results = await Task.WhenAll(units);
        long total = 0;
        foreach (var v in results) total += v;
        Console.WriteLine(total);
    }

    static async Task<int> Wait(Task<int[]> gate)
    {
        var p = await gate;
        int s = 0;
        foreach (var v in p) s += v;
        return s + 1;
    }
}
