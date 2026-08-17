#!/usr/bin/env python3
"""Run every Brood benchmark row at a tiny size and report the ones that do not run.

Why this exists. On 2026-08-14 a brood stdlib move (ADR-227: `sqrt` -> `std/math.blsp`,
and stage 4 dropping the `json-` export prefix) left **two rows dead** — `nbody` with
`unbound symbol: sqrt`, `json` with `unbound symbol: json/json-parse`. Nobody noticed for
three days, because nothing in either repo runs these programs for *correctness*: the
harness runs them for *timing*, takes tens of minutes, and is invoked by hand. The brood
repo's own migration sweep covered `breakage/`, `examples/`, `stress/`, `std/` and
`crates/` — it could not see this repo at all.

That is the KI-42 pattern (a suite that gates nothing rots quietly), and the fix is a check
cheap enough to run on every change: each row at the harness's own quick size, exit
status only.

    python3 bench/smoke.py                 # every brood row, at the harness's QUICK sizes
    python3 bench/smoke.py --only nbody,json
    python3 bench/smoke.py --brood ../brood/target/release/brood

Exits 1 if any row fails, so it can gate. It deliberately does NOT check checksums — that
is the harness's job (it compares across languages); this answers the cheaper question
"does the program still run at all", which is what a stdlib rename breaks.
"""
import argparse
import importlib.util
import os
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
ROWS_DIR = ROOT / "bench" / "brood"
TIMEOUT = 120

# Rows that cannot run standalone because the harness supplies a fixture for them:
# `http` fires its GETs at `bench/httpserver.py`, which the harness starts first (see
# its `BLOCKING_ROWS`). Skipped with a reason rather than reported as a failure — a
# smoke check that cries wolf gets ignored, which is how the rot it exists to catch
# happens in the first place.
NEEDS_FIXTURE = {"http": "needs bench/httpserver.py, which the harness starts"}


def row_sizes() -> dict:
    """Each row's smallest known-good `BENCH_N`, taken from the harness itself.

    A single constant cannot work: `BENCH_N` is an iteration count on some rows and a
    *problem size* on others, so 50 means "trivial" for `loop` and "fib(50)" or a 50x50
    board for `pfib`/`nqueens`. Reusing the harness's own `QUICK` table (and its full `N`
    where no quick size exists) keeps this honest and keeps the two in step.
    """
    spec = importlib.util.spec_from_file_location("bench_harness", ROOT / "bench" / "harness.py")
    h = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(h)
    sizes = {name: n for name, n, _langs, _desc in h.BENCHES}
    sizes.update(h.QUICK)
    return sizes


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--brood", default=shutil.which("brood") or "brood",
                    help="brood binary to use (default: the one on PATH)")
    ap.add_argument("--only", default="", help="comma-separated row names")
    args = ap.parse_args()

    wanted = {r.strip() for r in args.only.split(",") if r.strip()}
    rows = sorted(p for p in ROWS_DIR.glob("*.blsp")
                  if not wanted or p.stem in wanted)
    if not rows:
        print(f"smoke: no rows matched in {ROWS_DIR}", file=sys.stderr)
        return 1

    sizes = row_sizes()
    failed = []
    for row in rows:
        if row.stem in NEEDS_FIXTURE:
            print(f"  skip    {row.stem} ({NEEDS_FIXTURE[row.stem]})")
            continue
        env = {**os.environ, "BENCH_N": str(sizes.get(row.stem, 50))}
        try:
            p = subprocess.run([args.brood, str(row)], env=env, timeout=TIMEOUT,
                               capture_output=True, text=True)
        except subprocess.TimeoutExpired:
            failed.append((row.stem, f"timed out after {TIMEOUT}s"))
            print(f"  TIMEOUT {row.stem}")
            continue
        if p.returncode != 0:
            # The first error line is the useful one — an unbound symbol names itself.
            detail = next((ln for ln in (p.stderr or p.stdout).splitlines() if ln.strip()),
                          f"exit {p.returncode}")
            failed.append((row.stem, detail.strip()))
            print(f"  FAIL    {row.stem}: {detail.strip()}")
        else:
            print(f"  ok      {row.stem}")

    print()
    if failed:
        print(f"smoke: {len(failed)} of {len(rows)} rows do not run:")
        for name, why in failed:
            print(f"  {name}: {why}")
        return 1
    print(f"smoke: all {len(rows)} brood rows run.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
