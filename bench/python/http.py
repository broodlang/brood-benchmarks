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
PORT = os.environ.get("BENCH_HTTP_PORT", "8089")
URL = f"http://127.0.0.1:{PORT}/"


def fetch(_):
    # Count only 200s; swallow per-request failures (count 0) so one bad request
    # doesn't abort the whole run — matches the other languages' clients.
    try:
        with urllib.request.urlopen(URL, timeout=30) as r:
            r.read()
            return 1 if r.status == 200 else 0
    except Exception:
        return 0


if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=N) as ex:
        total = sum(ex.map(fetch, range(N)))
    print(total)
