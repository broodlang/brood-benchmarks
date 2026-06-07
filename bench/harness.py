#!/usr/bin/env python3
"""Benchmark harness: run each program in Brood / Elixir / Python / Node,
measure wall time + peak RSS, verify checksums agree, emit a report.

Usage:
    python3 bench/harness.py                 # full suite, 3 runs each
    python3 bench/harness.py --runs 5
    python3 bench/harness.py --only fib,sort,mandelbrot
    python3 bench/harness.py --langs brood,python
    python3 bench/harness.py --quick         # smaller sizes (smoke test)
    python3 bench/harness.py --label whklat  # write results.whklat.json + report.whklat.md
    python3 bench/harness.py --out /tmp/run   # write the result files into /tmp/run

A missing runtime is skipped with a warning rather than aborting the run — e.g.
without the .NET SDK installed (`sudo apt install dotnet-sdk-10.0`), the suite
still runs the other languages.
"""
import argparse
import json
import os
import platform
import re
import shutil
import socket
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent          # .../bench
RESULTS = ROOT.parent / "results"

# Display names for report headers/titles, in the canonical column order.
NICE = {"brood": "Brood", "elixir": "Elixir", "python": "Python",
        "node": "Node", "ruby": "Ruby", "dotnet": ".NET"}

# ext + how to invoke a single source file. `env` is merged on top of the
# inherited environment for that language's child process.
#   brood: pin BROOD_VM=1 so an inherited BROOD_VM=0 can't silently drop us onto
#   the (≈2× slower) tree-walker and make the numbers unreproducible.
# .NET needs compilation, so unlike the others we don't "run the source": the
# project (bench/dotnet/) is built once to a native apphost (see DOTNET_APP /
# build_dotnet), and each benchmark runs as `brood-bench <name>` — measuring the
# real runtime startup + RyuJIT, the fair analog to `node app.js`. The per-bench
# .cs files still live one-per-benchmark so they diff side by side.
DOTNET_DIR = ROOT / "dotnet"
DOTNET_APP = DOTNET_DIR / "publish" / "brood-bench"

LANGS = {
    "brood":  {"dir": "brood",  "ext": "blsp", "cmd": lambda p: ["brood", p], "env": {"BROOD_VM": "1"}},
    "elixir": {"dir": "elixir", "ext": "exs",  "cmd": lambda p: ["elixir", p]},
    "python": {"dir": "python", "ext": "py",   "cmd": lambda p: ["python3", p]},
    "node":   {"dir": "node",   "ext": "js",   "cmd": lambda p: ["node", p]},
    "ruby":   {"dir": "ruby",   "ext": "rb",   "cmd": lambda p: ["ruby", p]},
    "dotnet": {"dir": "dotnet", "ext": "cs",   "cmd": lambda p: [str(DOTNET_APP), Path(p).stem]},
}


def build_dotnet():
    """Build the .NET benchmark project once to a native apphost (Release)."""
    print("building .NET project (Release)…")
    r = subprocess.run(
        ["dotnet", "build", "-c", "Release", "-o", "publish"],
        cwd=str(DOTNET_DIR), capture_output=True, text=True,
    )
    if r.returncode != 0:
        raise RuntimeError("dotnet build failed:\n" + r.stdout + r.stderr)


def probe_version(lang):
    """The runtime's `--version` first line (for elixir, the `Elixir …` line), or
    None if the binary isn't on PATH. Stamped into the report so a result file
    says which machine + toolchain produced it."""
    cmd = {
        "brood":  ["brood", "--version"],
        "elixir": ["elixir", "--version"],
        "python": ["python3", "--version"],
        "node":   ["node", "--version"],
        "ruby":   ["ruby", "--version"],
        "dotnet": ["dotnet", "--version"],
    }.get(lang)
    if not cmd or shutil.which(cmd[0]) is None:
        return None
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
    except Exception:
        return None
    lines = [ln.strip() for ln in (r.stdout or r.stderr).splitlines() if ln.strip()]
    if not lines:
        return None
    # `elixir --version` leads with the Erlang/OTP banner; the Elixir line is what we want.
    return next((ln for ln in lines if ln.startswith("Elixir")), lines[0])


def collect_meta(langs):
    """Provenance for the report header: host, core count, OS, date, runtime versions."""
    return {
        "host": socket.gethostname(),
        "cores": os.cpu_count(),
        "platform": platform.platform(),
        "date": time.strftime("%Y-%m-%d %H:%M"),
        "versions": {l: probe_version(l) for l in langs},
    }

# name -> (default N, [langs]). "what" is the dimension each one stresses.
BENCHES = [
    ("startup",    0,      "all", "interpreter/VM startup + base memory"),
    ("fib",        30,     "all", "naive recursion / function-call overhead"),
    ("loop",       3000000,"all", "raw iteration (tail recursion vs for-loop)"),
    ("reduce",     1000000,"all", "higher-order fold over a range"),
    ("primes",     20000,  "all", "integer arithmetic (trial division)"),
    ("collatz",    30000,  "all", "integer arithmetic + tight inner loop"),
    ("mandelbrot", 128,    "all", "floating-point math (escape iterations)"),
    ("matmul",     80,     "all", "nested loops + indexing (integer NxN)"),
    ("strings",    50000,  "all", "string building (join) + length"),
    ("wordcount",  100000, "all", "hash-map build (immutable vs mutable)"),
    ("bintree",    40,     "all", "allocation / GC pressure (build+walk trees)"),
    ("sort",       50000,  "all", "sort a list of ints + checksum walk"),
    ("spawn",      20000,  ["brood", "elixir"], "lightweight processes + messaging"),
    ("pfib",       28,     "all", "parallel fib — 100 computed at once across cores"),
    ("http",       500,    "all", "concurrent HTTP — N in-flight GETs to a local server"),
]

QUICK = {  # smaller sizes for a fast smoke run
    "fib": 25, "loop": 300000, "reduce": 100000, "primes": 5000, "collatz": 5000,
    "mandelbrot": 48, "matmul": 40, "strings": 10000, "wordcount": 20000,
    "bintree": 8, "sort": 10000, "spawn": 5000, "pfib": 24, "http": 100,
}

RSS_RE = re.compile(r"Maximum resident set size \(kbytes\):\s*(\d+)")


def run_once(cmd, n, timeout, extra_env=None):
    """Run `cmd` under /usr/bin/time -v with BENCH_N=n. Returns (ok, wall_ms, rss_kb, out)."""
    env = dict(os.environ, BENCH_N=str(n))
    if extra_env:
        env.update(extra_env)
    full = ["/usr/bin/time", "-v"] + cmd
    t0 = time.perf_counter()
    try:
        p = subprocess.run(full, env=env, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return (False, timeout * 1000.0, None, "TIMEOUT")
    wall_ms = (time.perf_counter() - t0) * 1000.0
    m = RSS_RE.search(p.stderr)
    rss = int(m.group(1)) if m else None
    if p.returncode != 0:
        return (False, wall_ms, rss, f"EXIT {p.returncode}: {p.stderr.strip().splitlines()[-1:]}" )
    return (True, wall_ms, rss, p.stdout.strip())


def bench_lang(lang, name, n, runs, timeout):
    spec = LANGS[lang]
    path = str(ROOT / spec["dir"] / f"{name}.{spec['ext']}")
    if not Path(path).exists():
        return None
    cmd = spec["cmd"](path)
    extra_env = spec.get("env")
    best_wall, rss_peak, checksum, err = float("inf"), 0, None, None
    for _ in range(runs):
        ok, wall, rss, out = run_once(cmd, n, timeout, extra_env)
        if not ok:
            return {"error": out, "wall_ms": wall, "rss_kb": rss}
        best_wall = min(best_wall, wall)          # best = least-noisy run
        if rss:
            rss_peak = max(rss_peak, rss)
        checksum = out
    return {"wall_ms": round(best_wall, 1), "rss_kb": rss_peak, "checksum": checksum}


# Benchmarks that need a local HTTP server running while they execute. The
# server (bench/httpserver.py) is started before the benchmark's languages run
# and torn down after, so the `http` clients have something to call.
HTTP_PORT = 8089
SERVER_FOR = {"http"}


def start_http_server():
    """Launch the local HTTP server and wait until it accepts connections."""
    import socket
    proc = subprocess.Popen(
        [sys.executable, str(ROOT / "httpserver.py"), str(HTTP_PORT)],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    deadline = time.perf_counter() + 10.0
    while time.perf_counter() < deadline:
        try:
            with socket.create_connection(("127.0.0.1", HTTP_PORT), timeout=0.5):
                return proc
        except OSError:
            time.sleep(0.05)
    proc.terminate()
    raise RuntimeError("http server failed to start on :%d" % HTTP_PORT)


def stop_http_server(proc):
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--timeout", type=int, default=300, help="per-run timeout (s)")
    ap.add_argument("--only", default="", help="comma list of benchmark names")
    ap.add_argument("--langs", default="brood,elixir,python,node,ruby,dotnet")
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--out", default="", help="directory to write result files into (default: results/)")
    ap.add_argument("--label", default="", help="filename suffix, e.g. --label whklat -> results.whklat.json")
    args = ap.parse_args()

    only = set(filter(None, args.only.split(",")))
    langs = [l for l in args.langs.split(",") if l in LANGS]

    # A missing runtime is skipped (with a warning), not fatal — so the default
    # invocation works on a machine that lacks one of the toolchains.
    for l in list(langs):
        binary = LANGS[l]["cmd"]("x")[0]
        if l != "dotnet" and shutil.which(binary) is None:
            print(f"warning: `{binary}` not found on PATH — skipping {l}.", file=sys.stderr)
            langs.remove(l)
    if "dotnet" in langs and shutil.which("dotnet") is None:
        print("warning: `dotnet` not found on PATH — skipping the .NET column. "
              "Install it with `sudo apt install dotnet-sdk-10.0`.", file=sys.stderr)
        langs.remove("dotnet")

    if "dotnet" in langs:
        build_dotnet()

    results = {}
    for name, default_n, where, what in BENCHES:
        if only and name not in only:
            continue
        n = QUICK.get(name, default_n) if args.quick else default_n
        run_langs = langs if where == "all" else [l for l in langs if l in where]
        results[name] = {"n": n, "what": what, "langs": {}}
        print(f"\n## {name}  (N={n}) — {what}")
        server = start_http_server() if name in SERVER_FOR else None
        try:
            for lang in run_langs:
                r = bench_lang(lang, name, n, args.runs, args.timeout)
                if r is None:
                    continue
                results[name]["langs"][lang] = r
                if "error" in r:
                    print(f"  {lang:8} ERROR  {r['error']}")
                else:
                    print(f"  {lang:8} {r['wall_ms']:9.1f} ms   {r['rss_kb']:>8} KB   = {r['checksum']}")
        finally:
            if server:
                stop_http_server(server)
        verify_checksums(name, results[name])

    meta = collect_meta(langs)
    out_dir = Path(args.out) if args.out else RESULTS
    out_dir.mkdir(parents=True, exist_ok=True)
    suffix = f".{args.label}" if args.label else ""
    json_path = out_dir / f"results{suffix}.json"
    report_path = out_dir / f"report{suffix}.md"

    json_path.write_text(json.dumps({**results, "_meta": meta}, indent=2))
    report = build_report(results, args, meta)
    report_path.write_text(report)
    print(f"\nWrote {json_path} and {report_path}")
    print("\n" + report)


def verify_checksums(name, data):
    sums = {l: d.get("checksum") for l, d in data["langs"].items() if "checksum" in d}
    uniq = set(sums.values())
    if len(uniq) > 1:
        print(f"  !! CHECKSUM MISMATCH: {sums}")


def fmt_ms(ms):
    return f"{ms/1000:.3f}s" if ms >= 1000 else f"{ms:.1f}ms"


def build_report(results, args, meta=None):
    order = ["brood", "elixir", "python", "node", "ruby", "dotnet"]
    # Title names only the languages that actually produced a result this run.
    present = [l for l in order if any(l in d["langs"] for d in results.values())]
    title = " vs ".join(NICE[l] for l in present) + " — benchmark results"
    L = [f"# {title}", ""]
    if meta:
        vers = "; ".join(f"{NICE[l]} {v}" for l, v in meta["versions"].items() if v)
        L.append(f"> **Machine:** `{meta['host']}` ({meta['cores']} cores), "
                 f"{meta['platform']} — {meta['date']}.")
        L.append(f"> **Runtimes:** {vers}.")
        L.append("")
    mode = "quick" if args.quick else "full"
    L.append(f"_Best of {args.runs} runs per program; {mode} sizes. "
             f"Wall = total process time (startup + compute). `compute` ≈ "
             f"wall − that language's own `startup` (so a slow-booting runtime's "
             f"real compute speed is visible — e.g. the BEAM). RSS = peak resident "
             f"memory. `pos` = rank by wall, `mem` = rank by RSS (1 = best), out of "
             f"the languages with a port._")
    L.append("")
    # Per-language startup wall (from the `startup` row, if it ran) for the
    # `compute` column = wall − startup. Absent → the column shows "—".
    startup = {l: d["wall_ms"]
               for l, d in results.get("startup", {}).get("langs", {}).items()
               if "wall_ms" in d and "error" not in d}
    for name, data in results.items():
        langs = data["langs"]
        if not langs:
            continue
        L.append(f"## {name} — {data['what']}  (N={data['n']})")
        L.append("")
        L.append("| lang | wall | compute | vs fastest | pos | peak RSS | mem | checksum |")
        L.append("|------|------|---------|-----------|-----|----------|-----|----------|")
        oks = {l: d for l, d in langs.items() if "wall_ms" in d and "error" not in d}
        fastest = min((d["wall_ms"] for d in oks.values()), default=None)
        n = len(oks)
        # Rank by wall time and by peak RSS (1 = best/lowest); only the langs that
        # actually ran this benchmark are ranked, so `k/n` reflects the real field.
        wall_rank = {l: i + 1 for i, l in enumerate(sorted(oks, key=lambda l: oks[l]["wall_ms"]))}
        mem_rank = {l: i + 1 for i, l in enumerate(sorted(oks, key=lambda l: oks[l]["rss_kb"]))}
        for l in order:
            if l not in langs:
                continue
            d = langs[l]
            if "error" in d:
                L.append(f"| {l} | — | — | — | — | — | — | ERROR |")
                continue
            ratio = d["wall_ms"] / fastest if fastest else 1
            # compute ≈ wall − startup (only meaningful off the startup row).
            if name == "startup" or l not in startup:
                comp = "—"
            else:
                comp = fmt_ms(max(0.0, d["wall_ms"] - startup[l]))
            L.append(f"| {l} | {fmt_ms(d['wall_ms'])} | {comp} | {ratio:.1f}× | "
                     f"{wall_rank[l]}/{n} | {d['rss_kb']/1024:.1f} MB | "
                     f"{mem_rank[l]}/{n} | {d['checksum']} |")
        L.append("")
    return "\n".join(L)


if __name__ == "__main__":
    main()
