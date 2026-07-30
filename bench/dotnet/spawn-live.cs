// Hold N concurrent units ALIVE at once, then wake each INDIVIDUALLY and collect each
// result through a queue the parent drains — mirroring a mailbox, one item at a time.
//
// TWO fairness fixes (2026-07-30); the previous version flattered .NET on both counts:
//
//  1. `TaskCompletionSource` resumes its awaiting continuation **inline on the setter's
//     thread** by default. Measured: 1000 of 1000 continuations resumed inline, none on
//     the pool — so "wake 300k concurrent units" was really 300k synchronous closure
//     calls, with no scheduling, no context switch and no concurrency at all.
//     `RunContinuationsAsynchronously` is what makes a Task behave as a unit that is
//     *scheduled* rather than a callback invoked in place.
//  2. The result path was `Task.WhenAll` over a pre-allocated array — a reference store
//     per unit. Brood and Elixir send a reply *message* the parent receives individually,
//     so they were paying for 2 copied messages per unit against .NET's 1 delivery + 0.
//     A `Channel` drained one item at a time is the idiomatic .NET analogue.
//
// It is still not an isolated process — one shared heap, and nothing stops a unit from
// handing out a reference to its own state. See BENCHMARKS.md. Checksum = N*(sum+1).
namespace Bench;

using System.Threading.Channels;

static class SpawnLive
{
    public static async Task Run(int n)
    {
        var payload = Enumerable.Range(0, 16).ToArray();
        var gates = new TaskCompletionSource<int[]>[n];
        var results = Channel.CreateUnbounded<int>();
        for (int i = 0; i < n; i++)
        {
            // RunContinuationsAsynchronously: resume on the pool, not inline on the setter.
            gates[i] = new TaskCompletionSource<int[]>(TaskCreationOptions.RunContinuationsAsynchronously);
            _ = Wait(gates[i].Task, results.Writer);
        }
        // Hand each unit a COPY, as `send` would: a reference is a different operation.
        for (int i = 0; i < n; i++) gates[i].SetResult((int[])payload.Clone());
        long total = 0;
        for (int i = 0; i < n; i++) total += await results.Reader.ReadAsync();
        Console.WriteLine(total);
    }

    static async Task Wait(Task<int[]> gate, ChannelWriter<int> reply)
    {
        var p = await gate;
        int s = 0;
        foreach (var v in p) s += v;
        await reply.WriteAsync(s + 1);   // reply as a message, not a return value
    }
}
