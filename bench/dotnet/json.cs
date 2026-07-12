namespace Bench;
using System.Text.Json;
static class Json
{
    // Build N records, serialize then deserialize (System.Text.Json), checksum sum "v".
    class Rec { public long id { get; set; } public long v { get; set; } public string name { get; set; } public bool ok { get; set; } }

    public static void Run(int n)
    {
        long x = 123456789;
        var arr = new List<Rec>(n);
        for (int i = 0; i < n; i++)
        {
            x = (x * 1103515245 + 12345) & 0x7FFFFFFF;
            arr.Add(new Rec { id = i, v = x, name = "item", ok = x % 2 == 0 });
        }
        var text = JsonSerializer.Serialize(arr);
        var parsed = JsonSerializer.Deserialize<List<Rec>>(text);
        long acc = 0;
        foreach (var o in parsed) acc = (acc + o.v) % 2147483647;
        Console.WriteLine(acc);
    }
}
