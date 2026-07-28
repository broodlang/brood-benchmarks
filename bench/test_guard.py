#!/usr/bin/env python3
"""Regression test for the corruption guard — `python3 bench/test_guard.py`.

The guard exists because of 2026-07-28: `startup` is subtracted from every other row,
it was sampled best-of-3 like everything else, and a high Elixir boot sample (197ms
against a true ~182ms) exceeded Elixir's *wall* on six short rows. `max(0.0, wall -
startup)` clamped those to 0.0ms, which sorts to **1st place** and turns every ratio
against it into nonsense (Brood's `bintree` printed `103x` where it is `12x`). The run
was very nearly published.

A guard that silently stops working is worse than none, and this one cannot be exercised
on demand — whether a real run clamps depends on boot-sample luck (three `--quick`
attempts in a row failed to reproduce it). So the behaviour is pinned here with
fabricated timings instead, and the harness's measurement layer is stubbed out so the
test is instant and needs no runtimes installed.

Covers: detection, the report banner, the no-baseline and errored-cell exemptions, that a
FULL run with a clamped cell exits non-zero, and that `--quick` (whose sizes are tiny by
construction, so it clamps legitimately) warns without failing.
"""
import importlib.util
import io
import json
import sys
import tempfile
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path

HARNESS = Path(__file__).with_name("harness.py")

spec = importlib.util.spec_from_file_location("harness_under_test", HARNESS)
h = importlib.util.module_from_spec(spec)
sys.modules["harness_under_test"] = h
spec.loader.exec_module(h)

failures = []


def check(label, got, want):
    if got != want:
        failures.append(f"{label}: got {got!r}, want {want!r}")
        print(f"  FAIL {label}: got {got!r}, want {want!r}")
    else:
        print(f"  ok   {label}")


# ---- unit: the detector -----------------------------------------------------
print("verify_compute_floor")

# The real shape of the 2026-07-28 corruption.
corrupt = {
    "startup": {"langs": {"elixir": {"wall_ms": 197.0}, "brood": {"wall_ms": 13.2}}},
    "bintree": {"langs": {"elixir": {"wall_ms": 196.8}, "brood": {"wall_ms": 116.5}},
                "what": "x", "n": 1},
    "nqueens": {"langs": {"elixir": {"wall_ms": 192.0}, "brood": {"wall_ms": 95.0}},
                "what": "x", "n": 1},
}
bad = h.verify_compute_floor(corrupt)
check("detects both clamped cells", sorted((n, l) for n, l, _, _ in bad),
      [("bintree", "elixir"), ("nqueens", "elixir")])
check("flags the row for the report", corrupt["bintree"].get("compute_clamped"), ["elixir"])
check("leaves healthy rows unflagged", "compute_clamped" in corrupt["startup"], False)

healthy = {
    "startup": {"langs": {"elixir": {"wall_ms": 181.8}, "brood": {"wall_ms": 12.3}}},
    "bintree": {"langs": {"elixir": {"wall_ms": 196.8}, "brood": {"wall_ms": 116.5}},
                "what": "x", "n": 1},
}
check("healthy run is silent", h.verify_compute_floor(healthy), [])

# `--only fib` never measures a baseline; there is nothing to subtract, so nothing to check.
check("no startup baseline is skipped, not crashed",
      h.verify_compute_floor({"fib": {"langs": {"brood": {"wall_ms": 70.0}}}}), [])

# A crashed cell has no timing; it must not be mistaken for a clamped one.
check("errored cell is not a clamp", h.verify_compute_floor({
    "startup": {"langs": {"elixir": {"wall_ms": 181.8}}},
    "x": {"langs": {"elixir": {"error": "boom"}}, "what": "x", "n": 1},
}), [])

# Exactly-equal wall and startup is compute == 0, which is still not a measurement.
check("wall == startup counts as clamped", len(h.verify_compute_floor({
    "startup": {"langs": {"elixir": {"wall_ms": 180.0}}},
    "x": {"langs": {"elixir": {"wall_ms": 180.0}}, "what": "x", "n": 1},
})), 1)


# ---- end-to-end: the exit contract -----------------------------------------
# Stub the measurement layer so `main()` runs instantly against fabricated timings.
# Elixir's bintree wall lands below its own startup — the corruption, reproduced on demand.
WALL = {("brood", "startup"): 12.0, ("brood", "bintree"): 120.0,
        ("elixir", "startup"): 190.0, ("elixir", "bintree"): 185.0}

_real_collect_meta = h.collect_meta  # captured before main() gets it stubbed


def fake_bench_lang(lang, name, n, runs, timeout, pin=None, settle=0.0):
    w = WALL.get((lang, name))
    return None if w is None else {"wall_ms": w, "rss_kb": 1024, "checksum": "1"}


def run_main(argv):
    """Run the harness's main() with stubbed measurement; return its exit code."""
    h.bench_lang = fake_bench_lang
    h.warmup = lambda *a, **k: None
    # Call the REAL collect_meta with no languages rather than faking its shape: it fills
    # host/cores/platform/date exactly as the report expects, probes no runtimes (so the
    # test needs none installed), and cannot drift out of sync with build_report.
    h.collect_meta = lambda langs: _real_collect_meta([])
    with tempfile.TemporaryDirectory() as tmp:
        argv = argv + ["--out", tmp]
        old = sys.argv
        sys.argv = ["harness.py"] + argv
        code = 0
        try:
            with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()) as err:
                try:
                    h.main()
                except SystemExit as e:
                    code = e.code or 0
            report = (Path(tmp) / "report.md").read_text()
        finally:
            sys.argv = old
    return code, report, err.getvalue()


print("\nexit contract")
base = ["--only", "startup,bintree", "--langs", "brood,elixir", "--no-warmup"]

code, report, stderr = run_main(base)
check("a FULL run with a clamped cell exits non-zero", code, 1)
check("...and says so on stderr", "COMPUTE CLAMPED" in stderr, True)
check("...and bannerises the row in the report", "COMPUTE CLAMPED" in report, True)
check("...naming the offending cell", "bintree/elixir" in stderr, True)

code, report, stderr = run_main(base + ["--quick"])
check("--quick warns but does not fail", code, 0)
check("...still warning on stderr", "COMPUTE CLAMPED" in stderr, True)
check("...and saying why it is tolerated", "--quick" in stderr, True)

# A clean run must not trip the exit path at all.
WALL[("elixir", "bintree")] = 260.0
code, report, stderr = run_main(base)
check("a clean run exits zero", code, 0)
check("...with no warning anywhere", "COMPUTE CLAMPED" in stderr or "COMPUTE CLAMPED" in report, False)

print()
if failures:
    print(f"FAILED ({len(failures)}):")
    for f in failures:
        print("  " + f)
    sys.exit(1)
print("all guard tests passed")
