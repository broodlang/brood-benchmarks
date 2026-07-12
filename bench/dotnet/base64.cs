namespace Bench;
static class Base64
{
    // Generate N bytes, base64 encode+decode. Checksum = (sum enc char codes +
    // sum decoded bytes) mod 2^31.
    public static void Run(int n)
    {
        long x = 123456789;
        var b = new byte[n];
        for (int i = 0; i < n; i++) { x = (x * 1103515245 + 12345) & 0x7FFFFFFF; b[i] = (byte)(x % 256); }
        string enc = Convert.ToBase64String(b);
        byte[] dec = Convert.FromBase64String(enc);
        long encSum = 0;
        foreach (char c in enc) encSum = (encSum + c) % 2147483647;
        long decSum = 0;
        foreach (byte bb in dec) decSum = (decSum + bb) % 2147483647;
        Console.WriteLine((encSum + decSum) % 2147483647);
    }
}
