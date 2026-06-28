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
import urllib.request
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

# Elixir, like .NET, is precompiled once at startup rather than run from source.
# `elixir file.exs` recompiles the program's module on every run — that ~100ms
# compile leaks into the "compute" measurement (compute = wall − startup, and the
# `startup` baseline compiles no module so the leak isn't subtracted), overstating
# Elixir's compute by ~100ms/run. Instead we `elixirc` every bench module to
# BEAM_DIR once (build_beam) and run the precompiled `.beam` with `-pa BEAM_DIR`,
# the fair analog to escript / `node app.js` — no recompile per run. Each module
# is named `B<benchname>` (alnum only) so they don't collide in one BEAM_DIR; the
# run command loads it and calls `B<name>.main()`.
ELIXIR_DIR = ROOT / "elixir"
BEAM_DIR = ELIXIR_DIR / "_build"

# Clojure runs on the JVM. To avoid per-run `clojure` CLI / dependency-resolution overhead, the
# classpath is resolved once at startup (build_clojure → `clojure -Spath`) and each run is
# `java -cp <cp> clojure.main file.clj` — the JVM + clojure.main, the fair analog of `node app.js`.
# The JVM still cold-starts every run (no warmup carries over between the harness's separate
# processes), so HotSpot under-JITs short single-shot runs — a known caveat for JVM langs in a
# single-shot suite; the docs flag it.
CLOJURE_DIR = ROOT / "clojure"
CLOJURE_CP = None  # resolved by build_clojure()


def beam_module(name):
    """The compiled module name for a benchmark — `B` + the name's alphanumerics
    (e.g. `errors-deep` -> `Berrorsdeep`). Must match the `defmodule B…` in the
    corresponding bench/elixir/<name>.ex."""
    return "B" + re.sub(r"[^a-zA-Z0-9]", "", name)


def elixir_cmd(p):
    """Run the precompiled module for bench file `p` from BEAM_DIR (no recompile)."""
    return ["elixir", "-pa", str(BEAM_DIR), "-e", f"{beam_module(Path(p).stem)}.main()"]


def clojure_cmd(p):
    """Run a Clojure bench file via `java -cp <resolved-cp> clojure.main file.clj`."""
    return ["java", "-cp", CLOJURE_CP, "clojure.main", str(p)]


LANGS = {
    "brood":  {"dir": "brood",  "ext": "blsp", "cmd": lambda p: ["brood", p], "env": {"BROOD_VM": "1"}},
    "clojure": {"dir": "clojure", "ext": "clj", "cmd": clojure_cmd},
    "elixir": {"dir": "elixir", "ext": "ex",   "cmd": elixir_cmd},
    "python": {"dir": "python", "ext": "py",   "cmd": lambda p: ["python3", p]},
    "node":   {"dir": "node",   "ext": "js",   "cmd": lambda p: ["node", p]},
    "ruby":   {"dir": "ruby",   "ext": "rb",   "cmd": lambda p: ["ruby", p]},
    "dotnet": {"dir": "dotnet", "ext": "cs",   "cmd": lambda p: [str(DOTNET_APP), Path(p).stem]},
}


def build_clojure():
    """Resolve the Clojure classpath once (`clojure -Spath` from bench/clojure/deps.edn), so each
    run is `java -cp <cp> clojure.main file.clj` with no per-run CLI / dependency resolution."""
    global CLOJURE_CP
    print("resolving Clojure classpath (clojure -Spath)…")
    r = subprocess.run(
        ["clojure", "-Spath"], cwd=str(CLOJURE_DIR), capture_output=True, text=True,
    )
    if r.returncode != 0:
        raise RuntimeError("clojure -Spath failed:\n" + r.stdout + r.stderr)
    CLOJURE_CP = r.stdout.strip()


def build_dotnet():
    """Build the .NET benchmark project once to a native apphost (Release)."""
    print("building .NET project (Release)…")
    r = subprocess.run(
        ["dotnet", "build", "-c", "Release", "-o", "publish"],
        cwd=str(DOTNET_DIR), capture_output=True, text=True,
    )
    if r.returncode != 0:
        raise RuntimeError("dotnet build failed:\n" + r.stdout + r.stderr)


def build_beam():
    """Precompile every Elixir bench module to BEAM_DIR once (mirrors build_dotnet).
    Each run then loads the `.beam` via `-pa BEAM_DIR` instead of recompiling the
    source — so the ~100ms module-compile no longer leaks into compute."""
    print("compiling Elixir modules (elixirc → _build)…")
    BEAM_DIR.mkdir(parents=True, exist_ok=True)
    sources = sorted(str(p) for p in ELIXIR_DIR.glob("*.ex"))
    if not sources:
        raise RuntimeError(f"no Elixir sources found in {ELIXIR_DIR}")
    r = subprocess.run(
        ["elixirc", "-o", str(BEAM_DIR)] + sources,
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        raise RuntimeError("elixirc failed:\n" + r.stdout + r.stderr)


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
# Sizes are picked so even the fastest runtime (.NET / Node) spends ~100ms+ of
# *compute* — below that, wall − startup is just startup-measurement noise — while
# the slowest (the Brood VM) still finishes in a couple of seconds. `reduce` is
# the freshest tune (it became a real higher-order fold; re-measure to settle N).
BENCHES = [
    ("startup",    0,        "all", "interpreter/VM startup + base memory"),
    ("fib",        35,       "all", "naive recursion / function-call overhead"),
    ("loop",       30000000, "all", "raw iteration (tail recursion vs for-loop)"),
    ("reduce",     5000000,  "all", "higher-order fold over a range"),
    ("primes",     150000,   "all", "integer arithmetic (trial division)"),
    ("collatz",    250000,   "all", "integer arithmetic + tight inner loop"),
    ("mandelbrot", 540,      "all", "floating-point math (escape iterations)"),
    ("matmul",     175,      "all", "nested loops + indexing (integer NxN)"),
    ("strings",    500000,   "all", "string building (join) + length"),
    ("wordcount",  750000,   "all", "hash-map build (immutable vs mutable)"),
    ("bintree",    200,      "all", "allocation / GC pressure (build+walk trees)"),
    ("sort",       375000,   "all", "sort a list of ints + checksum walk"),
    ("nqueens",    10,       "all", "backtracking recursion — count N-queens solutions"),
    ("errors",     200000,   "all", "error handling — raise + recover a value N times"),
    ("errors-deep", 50000,   "all", "error propagation — throw 50 frames deep, catch at top"),
    ("pipeline",   100000,   "all", "filter/map/reduce pipeline over a range"),
    ("spawn",      10000,    "all", "lightweight concurrent units + result collection"),
    ("pfib",       28,       "all", "parallel fib — 100 computed at once across cores"),
    ("http",       500,      "all", "concurrent HTTP — N in-flight GETs to a local server"),
]

# The concurrency benchmarks bounce 15–45% run-to-run with scheduler / CPU
# contention. Since we report the best (least-noisy) run, taking more samples
# tightens the floor — so these run more times than the steady compute benches.
NOISY = {"spawn", "pfib", "http"}
NOISY_RUNS = 7

QUICK = {  # smaller sizes for a fast smoke run
    "fib": 25, "loop": 300000, "reduce": 100000, "primes": 5000, "collatz": 5000,
    "mandelbrot": 48, "matmul": 40, "strings": 10000, "wordcount": 20000,
    "bintree": 8, "sort": 10000, "nqueens": 8, "pipeline": 50000,
    "spawn": 5000, "pfib": 24, "http": 100,
}

RSS_RE = re.compile(r"Maximum resident set size \(kbytes\):\s*(\d+)")
# Strip ANSI colour/SGR escapes from a benchmark's stdout before checksumming —
# a runtime that auto-colourises (e.g. Node when FORCE_COLOR is set in the env)
# prints the SAME integer wrapped in escapes; without this the string compare
# would spuriously flag a checksum mismatch.
ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")


def run_once(cmd, n, timeout, extra_env=None, pin=None, settle=0.0):
    """Run `cmd` under /usr/bin/time -v with BENCH_N=n. Returns (ok, wall_ms, rss_kb, out).

    `pin` (a taskset core list like "11" or "0-11") confines the process to those
    CPUs so it isn't migrated and contends less with system noise; `settle` sleeps
    that many seconds first so the previous run's teardown (freeing RSS, reaping
    threads) doesn't bleed into this measurement. Both are the isolation knobs."""
    env = dict(os.environ, BENCH_N=str(n))
    if extra_env:
        env.update(extra_env)
    full = (["taskset", "-c", pin] if pin else []) + ["/usr/bin/time", "-v"] + cmd
    if settle:
        time.sleep(settle)
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
    return (True, wall_ms, rss, ANSI_RE.sub("", p.stdout).strip())


def bench_lang(lang, name, n, runs, timeout, pin=None, settle=0.0):
    spec = LANGS[lang]
    path = str(ROOT / spec["dir"] / f"{name}.{spec['ext']}")
    if not Path(path).exists():
        return None
    cmd = spec["cmd"](path)
    extra_env = spec.get("env")
    best_wall, rss_peak, checksum, err = float("inf"), 0, None, None
    for _ in range(runs):
        ok, wall, rss, out = run_once(cmd, n, timeout, extra_env, pin, settle)
        if not ok:
            return {"error": out, "wall_ms": wall, "rss_kb": rss}
        best_wall = min(best_wall, wall)          # best = least-noisy run
        if rss:
            rss_peak = max(rss_peak, rss)
        checksum = out
    return {"wall_ms": round(best_wall, 1), "rss_kb": rss_peak, "checksum": checksum}


# Benchmarks that need a local HTTP server running while they execute. The
# server (bench/httpserver.py) is started before the benchmark's languages run
# and torn down after, so the `http` clients have something to call. The port is
# chosen fresh each time (see pick_free_port) so a process squatting on a fixed
# port can't be mistaken for our server; the clients read it from BENCH_HTTP_PORT.
SERVER_FOR = {"http"}


def pick_free_port():
    """An OS-assigned free TCP port on the loopback interface."""
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def start_http_server(port):
    """Launch the local HTTP server on `port` and wait until *our* server
    answers correctly — a GET returning 200 with the body `ok`. A bare connect
    check isn't enough: a foreign listener (or a stale server) on the port would
    satisfy it, and the benchmark would then silently measure the wrong server
    (e.g. counting zero 200s). If our process dies on bind, surface its stderr."""
    proc = subprocess.Popen(
        [sys.executable, str(ROOT / "httpserver.py"), str(port)],
        stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True,
    )
    deadline = time.perf_counter() + 10.0
    while time.perf_counter() < deadline:
        if proc.poll() is not None:                      # exited (e.g. bind failed)
            err = (proc.stderr.read() if proc.stderr else "").strip()
            raise RuntimeError(f"http server exited before serving on :{port}\n{err}")
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{port}/", timeout=0.5) as r:
                if r.status == 200 and r.read() == b"ok":
                    return proc
        except Exception:
            time.sleep(0.05)
    proc.terminate()
    raise RuntimeError(f"http server on :{port} never answered with a correct 200 — "
                       "something else may be holding the port")


def stop_http_server(proc):
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", type=int, default=3)
    ap.add_argument("--startup-runs", type=int, default=None,
                    help="override --runs for the startup benchmark only (default: same as --runs)")
    ap.add_argument("--timeout", type=int, default=300, help="per-run timeout (s)")
    ap.add_argument("--only", default="", help="comma list of benchmark names")
    ap.add_argument("--langs", default="brood,clojure,elixir,python,node,ruby,dotnet")
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--out", default="", help="directory to write result files into (default: results/)")
    ap.add_argument("--label", default="", help="filename suffix, e.g. --label whklat -> results.whklat.json")
    ap.add_argument("--focus", default="", help="only print this language's rows (ranks still reflect full field)")
    ap.add_argument("--report-from", default="", metavar="JSON",
                    help="skip running; regenerate the report from an existing results JSON")
    ap.add_argument("--isolate", dest="isolate", action="store_true", default=None,
                    help="pin each run to dedicated CPU(s) via taskset and settle between "
                         "runs, to avoid contention (default: on when taskset is present)")
    ap.add_argument("--no-isolate", dest="isolate", action="store_false",
                    help="disable CPU pinning / settle (run unpinned, back-to-back)")
    ap.add_argument("--pin-cores", type=int, default=4,
                    help="how many cores to pin compute benchmarks to (default: 4, the last "
                         "N cores). The workload stays single-threaded; a small SET (not a "
                         "single core) lets a runtime's background JIT/GC threads — the JVM's "
                         "most of all — run without contending for the work core, which a "
                         "single-core pin otherwise penalises ~2× for the JVM while leaving "
                         "genuinely single-threaded runtimes unchanged. Concurrency benchmarks "
                         "always get every core.")
    ap.add_argument("--settle", type=float, default=0.25,
                    help="seconds to idle before each measured run (default: 0.25)")
    args = ap.parse_args()

    if args.report_from:
        data = json.loads(Path(args.report_from).read_text())
        meta = data.pop("_meta", None)
        out_dir = Path(args.out) if args.out else RESULTS
        out_dir.mkdir(parents=True, exist_ok=True)
        suffix = f".{args.label}" if args.label else ""
        report_path = out_dir / f"report{suffix}.md"
        report = build_report(data, args, meta)
        report_path.write_text(report)
        print(f"Wrote {report_path}")
        print("\n" + report)
        return

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
    if "clojure" in langs and shutil.which("clojure") is None:
        print("warning: `clojure` not found on PATH — skipping the Clojure column.", file=sys.stderr)
        langs.remove("clojure")

    if "dotnet" in langs:
        build_dotnet()
    if "elixir" in langs:
        build_beam()
    if "clojure" in langs:
        build_clojure()

    # Isolation: pin each measured process to dedicated CPUs (so it isn't migrated
    # and contends less with system noise) and settle between runs. On by default
    # when taskset is available; compute benchmarks pin to a small core SET, the
    # concurrency ones (NOISY) get every core so their parallelism story holds.
    #
    # Why a set and not a single core: a single-threaded *workload* still uses
    # background threads for the runtime's own housekeeping — JIT compilation and
    # GC. The JVM leans on these hardest, so pinning it to one core (where its
    # compiler/GC threads fight the work thread) roughly DOUBLES its time, while
    # genuinely single-threaded runtimes (Brood, Python, Ruby — and, as measured,
    # Elixir and .NET at these sizes) are unchanged. A small set isolates the work
    # from system noise without penalising background-threaded runtimes; the work
    # itself is still single-threaded, so no language parallelises across the set.
    ncpu = os.cpu_count() or 1
    isolate = args.isolate
    if isolate is None:
        isolate = shutil.which("taskset") is not None
    if isolate and shutil.which("taskset") is None:
        print("warning: --isolate requested but `taskset` not found — running unpinned.", file=sys.stderr)
        isolate = False
    n_compute = max(1, min(args.pin_cores, ncpu))
    compute_cores = str(ncpu - 1) if n_compute == 1 else f"{ncpu - n_compute}-{ncpu - 1}"
    all_cores = f"0-{ncpu - 1}"
    if isolate:
        print(f"isolation: taskset pin (compute→cores {compute_cores}, concurrency→{all_cores}), "
              f"{args.settle}s settle before each run")

    startup_runs = args.startup_runs if args.startup_runs is not None else args.runs
    results = {}
    mismatched = []
    for name, default_n, where, what in BENCHES:
        if only and name not in only:
            continue
        n = QUICK.get(name, default_n) if args.quick else default_n
        if name == "startup":
            runs = startup_runs
        elif name in NOISY:
            runs = max(args.runs, NOISY_RUNS)
        else:
            runs = args.runs
        run_langs = langs if where == "all" else [l for l in langs if l in where]
        results[name] = {"n": n, "what": what, "langs": {}}
        print(f"\n## {name}  (N={n}) — {what}")
        server = None
        if name in SERVER_FOR:
            port = pick_free_port()
            server = start_http_server(port)
            os.environ["BENCH_HTTP_PORT"] = str(port)
        if isolate:
            pin = all_cores if name in NOISY else compute_cores
            settle = args.settle
        else:
            pin, settle = None, 0.0
        try:
            for lang in run_langs:
                r = bench_lang(lang, name, n, runs, args.timeout, pin, settle)
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
                os.environ.pop("BENCH_HTTP_PORT", None)
        if verify_checksums(name, results[name]):
            mismatched.append(name)

    meta = collect_meta(langs)
    meta["isolation"] = (
        f"taskset pin (compute→cores {compute_cores}, concurrency→{all_cores}); {args.settle}s settle"
        if isolate else "none (unpinned, back-to-back)")
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

    if mismatched:
        print(f"\n!! CHECKSUM MISMATCH in: {', '.join(mismatched)} — the languages "
              "did not do equivalent work, so these timings are not comparable. "
              "The affected rows are flagged in the report.", file=sys.stderr)
        sys.exit(1)


def verify_checksums(name, data):
    """Assert the languages that produced a checksum all agree. On disagreement,
    print it, record it on `data` (so the report flags the row), and return the
    {lang: checksum} map; otherwise return None. The caller fails the run if any
    benchmark mismatches — a differing checksum means the languages did NOT do
    equivalent work, so the timings are not comparable."""
    sums = {l: d.get("checksum") for l, d in data["langs"].items() if "checksum" in d}
    uniq = set(sums.values())
    if len(uniq) > 1:
        print(f"  !! CHECKSUM MISMATCH: {sums}")
        data["checksum_mismatch"] = sums
        return sums
    return None


def fmt_ms(ms):
    return f"{ms/1000:.3f}s" if ms >= 1000 else f"{ms:.1f}ms"


def build_report(results, args, meta=None):
    order = ["brood", "elixir", "python", "node", "ruby", "dotnet"]
    focus = getattr(args, "focus", "") or ""
    # Title names only the languages that actually produced a result this run.
    present = [l for l in order if any(l in d["langs"] for d in results.values())]
    title = " vs ".join(NICE[l] for l in present) + " — benchmark results"
    L = [f"# {title}", ""]
    if meta:
        vers = "; ".join(f"{NICE[l]} {v}" for l, v in meta["versions"].items() if v)
        L.append(f"> **Machine:** `{meta['host']}` ({meta['cores']} cores), "
                 f"{meta['platform']} — {meta['date']}.")
        L.append(f"> **Runtimes:** {vers}.")
        if meta.get("isolation"):
            L.append(f"> **Isolation:** {meta['isolation']}.")
        L.append("")
    mode = "quick" if args.quick else "full"
    startup_runs = getattr(args, "startup_runs", None) or args.runs
    noisy_runs = max(args.runs, NOISY_RUNS)
    bits = [f"best of {args.runs} runs"]
    if startup_runs != args.runs:
        bits.append(f"startup best of {startup_runs}")
    if noisy_runs != args.runs:
        bits.append(f"spawn/pfib/http best of {noisy_runs}")
    runs_note = "; ".join(bits) + " per program"
    L.append(f"_{runs_note}; {mode} sizes. "
             f"**compute = wall − startup** (startup is that language's own boot time "
             f"from its `startup`-row wall). Rankings and ratios are by **compute** so "
             f"a slow-booting runtime's real work speed is visible (e.g. the BEAM "
             f"boots ~400ms but computes fast). On the `startup` row itself rankings "
             f"are by wall (compute ≈ 0). RSS = peak resident memory. "
             f"`pos` = rank by compute, `mem` = rank by RSS (1 = best), out of the "
             f"languages with a port._")
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
        if "checksum_mismatch" in data:
            L.append(f"> ⚠️ **CHECKSUM MISMATCH** — the languages did not agree "
                     f"(`{data['checksum_mismatch']}`); these rows are **not** "
                     f"comparable.")
            L.append("")
        L.append("| lang | compute | vs fastest | pos | wall | startup | peak RSS | mem | checksum |")
        L.append("|------|---------|------------|-----|------|---------|----------|-----|----------|")
        oks = {l: d for l, d in langs.items() if "wall_ms" in d and "error" not in d}
        n = len(oks)
        # For the startup benchmark itself compute ≈ 0 for everyone, so rank by wall.
        # For all other benchmarks rank by compute (wall − startup) so slow-starting
        # runtimes aren't penalised for boot time in compute-heavy comparisons.
        is_startup_bench = (name == "startup")
        compute_ms = {}
        for l in oks:
            if is_startup_bench:
                compute_ms[l] = oks[l]["wall_ms"]
            elif startup.get(l) is not None:
                compute_ms[l] = max(0.0, oks[l]["wall_ms"] - startup[l])
            else:
                compute_ms[l] = oks[l]["wall_ms"]
        fastest_compute = min(compute_ms.values(), default=None)
        # Floor the denominator at 1ms: when fast runtimes have compute < 0 due to
        # startup-measurement variance (wall < startup), avoid collapsing all ratios
        # to 1× via division-by-zero. Ratios < 1× are shown as "< 1×".
        ratio_denom = max(fastest_compute, 1.0) if fastest_compute is not None else 1.0
        compute_rank = {l: i + 1 for i, l in enumerate(sorted(compute_ms, key=lambda l: compute_ms[l]))}
        mem_rank = {l: i + 1 for i, l in enumerate(sorted(oks, key=lambda l: oks[l]["rss_kb"]))}
        for l in order:
            if l not in langs:
                continue
            if focus and l != focus:
                continue
            d = langs[l]
            if "error" in d:
                L.append(f"| {l} | — | — | — | — | — | — | — | ERROR |")
                continue
            r = compute_ms[l] / ratio_denom
            ratio_str = f"< 1×" if r < 1.0 else f"{r:.1f}×"
            # Break wall into startup (the lang's `startup`-row wall) + compute.
            # No startup row (e.g. --only without it) → both show "—".
            s = startup.get(l)
            if is_startup_bench:
                # Startup benchmark: the wall time IS the useful metric; showing
                # "compute = 0" would be circular, so show wall in the compute column.
                comp_str = fmt_ms(d["wall_ms"])
                start_str = "—"
            elif s is None:
                comp_str = start_str = "—"
            else:
                start_str = fmt_ms(s)
                comp_str = fmt_ms(max(0.0, d["wall_ms"] - s))
            L.append(f"| {l} | {comp_str} | {ratio_str} | "
                     f"{compute_rank[l]}/{n} | {fmt_ms(d['wall_ms'])} | {start_str} | "
                     f"{d['rss_kb']/1024:.1f} MB | "
                     f"{mem_rank[l]}/{n} | {d['checksum']} |")
        L.append("")
    return "\n".join(L)


if __name__ == "__main__":
    main()
