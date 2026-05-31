# Concurrent HTTP: fire N GETs at a local server (each sleeps ~20ms server-side)
# and count the 200s. Python's GIL is released during blocking I/O, so a thread
# pool overlaps the waits fine — the idiomatic stdlib way to do concurrent HTTP.
# Checksum = N.
#
# This file is named http.py, which would shadow the stdlib `http` package that
# urllib imports — so drop the script's own directory from the import path first.
import sys

sys.path.pop(0)

import os
import urllib.request
from concurrent.futures import ThreadPoolExecutor

N = int(os.environ.get("BENCH_N", "500"))
URL = "http://127.0.0.1:8089/"


def fetch(_):
    with urllib.request.urlopen(URL, timeout=30) as r:
        r.read()
        return 1 if r.status == 200 else 0


if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=N) as ex:
        total = sum(ex.map(fetch, range(N)))
    print(total)
