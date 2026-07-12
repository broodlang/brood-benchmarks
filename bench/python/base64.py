# Generate N bytes, base64 encode+decode. Checksum = (sum enc char codes + sum
# decoded bytes) mod 2^31.
import os, base64
N = int(os.environ.get("BENCH_N", "50000"))
x = 123456789
b = bytearray(N)
for i in range(N):
    x = (x * 1103515245 + 12345) & 0x7FFFFFFF
    b[i] = x % 256
enc = base64.b64encode(bytes(b))
dec = base64.b64decode(enc)
enc_sum = 0
for c in enc:
    enc_sum = (enc_sum + c) % 2147483647
dec_sum = 0
for c in dec:
    dec_sum = (dec_sum + c) % 2147483647
print((enc_sum + dec_sum) % 2147483647)
