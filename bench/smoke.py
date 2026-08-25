#!/usr/bin/env python3
"""Run every benchmark row at a tiny size and report the ones that do not run.

Why this exists. Twice now a brood stdlib rename has left rows in this repo dead for
days, because nothing here runs these programs for *correctness*: the harness runs them
for *timing*, takes tens of minutes, and is invoked by hand.

  * 2026-08-14 (KI-42) — ADR-227 moved `sqrt` to `std/math.blsp` and stage 4 dropped the
    `json-` export prefix. `nbody` died on `unbound symbol: sqrt`, `json` on
    `unbound symbol: json/json-parse`. Three days unnoticed.
  * 2026-08-25 (KI-44) — the v0.9.0 + v0.10.0 namespacing waves (core: 613 -> 337
    published names) took `getenv` -> `os/getenv`, `now-ns` -> `os/now-ns`,
    `(table)` -> `(table/new)`, `start-supervisor`/`stop-supervisor` ->
    `supervisor/start`/`gen/stop`, `http/http-get` -> `http/fetch`, and removed
    `require` outright. **30 of 31 brood rows** were dead; only `startup` still ran.

Both times the brood repo's own migration sweep covered `breakage/`, `examples/`,
`stress/`, `std/` and `crates/` — it could not see this repo at all. KI-44's writeup says
a "every bench row still runs at BENCH_N=50" check would have caught it in seconds. This
is that check.

    python3 bench/smoke.py                      # every brood row, at the harness's QUICK sizes
    python3 bench/smoke.py --only nbody,json
    python3 bench/smoke.py --brood ../brood/target/release/brood
    python3 bench/smoke.py --langs all          # every port + cross-language checksums
    python3 bench/smoke.py --langs brood,node,python

Exits 1 if any row fails, so it can gate.

TWO things are checked, and the second is the one that matters:

1. The process exits 0 within the timeout.
2. **No `unbound symbol` appears anywhere in stdout or stderr.** Exit status alone is
   not enough. Brood reports an unbound name at *compile* time as a `warning:` line and
   only *errors* when the reference is actually evaluated — so a rename inside a branch
   this size of run never takes exits 0, prints the right checksum, and is still broken
   at the size the harness uses. Grepping the output is what makes the gate honest;
   relying on the exit code is what lets the rot back in.

With `--langs` naming more than one language, the rows' printed checksums are compared
across the languages that ran them — the same cross-language correctness check the
harness does, minus the tens of minutes of timing. That is how a row that "runs" but
computes the wrong thing gets caught.
"""
import argparse
import importlib.util
import os
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
TIMEOUT = 180

# Substrings that mean "this row is broken" even when the process exits 0. See the
# module docstring: brood's unbound-symbol diagnostic is a compile-time *warning* until
# the reference is evaluated, so the only reliable signal at a tiny BENCH_N is the text.
POISON = ("unbound symbol",)


def harness():
    """Import bench/harness.py as a module — the single source of truth for row sizes,
    per-language run commands, which languages each row runs in, and the build steps the
    compiled ports need. Duplicating any of it here would let the two drift, which is the
    same failure mode this script exists to catch."""
    spec = importlib.util.spec_from_file_location("bench_harness", ROOT / "bench" / "harness.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def row_sizes(h) -> dict:
    """Each row's smallest known-good `BENCH_N`, taken from the harness itself.

    A single constant cannot work: `BENCH_N` is an iteration count on some rows and a
    *problem size* on others, so 50 means "trivial" for `loop` and "fib(50)" or a 50x50
    board for `pfib`/`nqueens`. Reusing the harness's own `QUICK` table (and its full `N`
    where no quick size exists) keeps this honest and keeps the two in step."""
    sizes = {name: n for name, n, _langs, _desc in h.BENCHES}
    sizes.update(h.QUICK)
    return sizes


def row_langs(h) -> dict:
    """row -> the languages that row is expected to run in (resolving "all"/"all+c")."""
    return {name: (h.WHERE[where] if isinstance(where, str) else where)
            for name, _n, where, _desc in h.BENCHES}


def available(h, langs):
    """Drop languages whose runtime isn't installed, and run the build steps the
    compiled ports need. A missing runtime is a skip, not a failure — the gate's job is
    to catch rot in the rows, and crying wolf about an absent .NET SDK gets it ignored."""
    probes = {"brood": None, "python": "python3", "node": "node", "ruby": "ruby",
              "elixir": "elixirc", "clojure": "clojure", "dotnet": "dotnet", "c": "gcc"}
    keep = []
    for l in langs:
        probe = probes.get(l)
        if probe and shutil.which(probe) is None:
            print(f"  skip lang {l} (no {probe} on PATH)")
            continue
        keep.append(l)
    try:
        if "clojure" in keep:
            h.build_clojure()
        if "dotnet" in keep:
            h.build_dotnet()
        if "elixir" in keep:
            h.build_beam()
        if "c" in keep:
            h.build_c()
    except Exception as e:                                   # a build failure IS a failure
        print(f"smoke: build step failed: {e}", file=sys.stderr)
        raise
    return keep


def run_row(h, lang, row, n, brood_bin, extra_env):
    """(ok, detail, checksum) for one row in one language."""
    spec = h.LANGS[lang]
    path = ROOT / "bench" / spec["dir"] / f"{row}.{spec['ext']}"
    if not path.exists():
        return (None, "no port", None)
    cmd = spec["cmd"](str(path))
    if lang == "brood":
        cmd = [brood_bin] + list(cmd[1:])
    env = {**os.environ, "BENCH_N": str(n), **(spec.get("env") or {}), **extra_env}
    try:
        p = subprocess.run(cmd, env=env, timeout=TIMEOUT, capture_output=True, text=True)
    except FileNotFoundError as e:
        return (False, f"cannot run: {e}", None)
    except subprocess.TimeoutExpired:
        return (False, f"timed out after {TIMEOUT}s", None)
    blob = (p.stdout or "") + (p.stderr or "")
    for bad in POISON:
        if bad in blob:
            line = next((ln.strip() for ln in blob.splitlines() if bad in ln), bad)
            return (False, line, None)
    if p.returncode != 0:
        # The last stderr line is the useful one — brood's error text names the symbol.
        detail = next((ln for ln in reversed((p.stderr or p.stdout).splitlines()) if ln.strip()),
                      f"exit {p.returncode}")
        return (False, detail.strip(), None)
    _metrics, checksum = h.split_metrics(h.ANSI_RE.sub("", p.stdout).strip())
    return (True, "", checksum)


def main() -> int:
    global TIMEOUT
    ap = argparse.ArgumentParser()
    ap.add_argument("--brood", default=shutil.which("brood") or "brood",
                    help="brood binary to use (default: the one on PATH)")
    ap.add_argument("--only", default="", help="comma-separated row names")
    ap.add_argument("--langs", default="brood",
                    help="comma-separated languages, or 'all' (default: brood)")
    ap.add_argument("--timeout", type=int, default=TIMEOUT, help="per-row timeout (s)")
    args = ap.parse_args()

    TIMEOUT = args.timeout
    h = harness()
    sizes, langs_for = row_sizes(h), row_langs(h)

    langs = h.ALL_C if args.langs == "all" else [l.strip() for l in args.langs.split(",") if l.strip()]
    unknown = [l for l in langs if l not in h.LANGS]
    if unknown:
        print(f"smoke: unknown language(s): {', '.join(unknown)}", file=sys.stderr)
        return 1
    langs = available(h, langs)

    wanted = {r.strip() for r in args.only.split(",") if r.strip()}
    rows = [name for name, _n, _w, _d in h.BENCHES if not wanted or name in wanted]
    unmatched = wanted - set(rows)
    if unmatched:
        print(f"smoke: no such row(s): {', '.join(sorted(unmatched))}", file=sys.stderr)
        return 1
    if not rows:
        print("smoke: no rows selected", file=sys.stderr)
        return 1

    failed, mismatched, ran = [], [], 0
    for row in rows:
        n = sizes.get(row, 50)
        # The `http` row needs a server to call; the harness starts one, so do we,
        # rather than declaring the row unrunnable and leaving it unguarded.
        server, extra_env = None, {}
        if row in h.SERVER_FOR:
            try:
                port = h.pick_free_port()
                server = h.start_http_server(port)
                extra_env["BENCH_HTTP_PORT"] = str(port)
            except Exception as e:
                print(f"  skip    {row} (http fixture would not start: {e})")
                continue
        try:
            sums = {}
            for lang in langs:
                if lang not in langs_for.get(row, []):
                    continue
                ok, detail, checksum = run_row(h, lang, row, n, args.brood, extra_env)
                tag = f"{row}/{lang}" if len(langs) > 1 else row
                if ok is None:
                    print(f"  skip    {tag} ({detail})")
                elif ok:
                    ran += 1
                    sums[lang] = checksum
                    print(f"  ok      {tag}" + (f"  = {checksum}" if len(langs) > 1 else ""))
                else:
                    failed.append((tag, detail))
                    print(f"  FAIL    {tag}: {detail}")
        finally:
            if server is not None:
                h.stop_http_server(server)
        if len(sums) > 1 and len(set(sums.values())) > 1:
            mismatched.append((row, sums))
            print(f"  MISMATCH {row}: {sums}")

    print()
    if failed or mismatched:
        if failed:
            print(f"smoke: {len(failed)} row(s) do not run:")
            for name, why in failed:
                print(f"  {name}: {why}")
        if mismatched:
            print(f"smoke: {len(mismatched)} row(s) disagree across languages:")
            for name, sums in mismatched:
                print(f"  {name}: {sums}")
        return 1
    print(f"smoke: all {ran} row/language combinations run"
          + (" and agree on their checksums." if len(langs) > 1 else "."))
    return 0


if __name__ == "__main__":
    sys.exit(main())
