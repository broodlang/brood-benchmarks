# Build N records, json.dumps then json.loads, checksum sum of "v" mod 2^31.
import os, json
N = int(os.environ.get("BENCH_N", "2000"))
x = 123456789
arr = []
for i in range(N):
    x = (x * 1103515245 + 12345) & 0x7FFFFFFF
    arr.append({"id": i, "v": x, "name": "item", "ok": x % 2 == 0})
parsed = json.loads(json.dumps(arr))
acc = 0
for o in parsed:
    acc = (acc + o["v"]) % 2147483647
print(acc)
