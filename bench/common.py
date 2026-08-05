#!/usr/bin/env python3
"""Shared vocabulary for the reporting scripts — one definition per concept.

`chart.py` and `docs.py` both need the aggregate's row set, the language-name mapping and
`compute = wall − startup`. They each had their own copy, which is how the chart and the
doc could in principle disagree about what "aggregate" means. They import from here now.

`harness.py` deliberately does **not** import this: it is the measuring half and must not
depend on the reporting half.
"""

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results" / "results.json"

# The rows the aggregate covers: single-threaded core compute, same algorithm and same
# data structures in every language. Deliberately excludes the concurrency, error-handling
# and native-library rows — folding those in would swamp the figure with library and
# representation outliers rather than core language speed.
COMPUTE = ["fib", "loop", "reduce", "primes", "collatz", "mandelbrot",
           "matmul", "strings", "wordcount", "bintree", "sort"]

# Markdown column heading -> results.json key.
LANG_COL = {".NET": "dotnet", "Elixir": "elixir", "Node": "node", "Brood": "brood",
            "Ruby": "ruby", "Python": "python", "Clojure": "clojure"}
PRETTY = {v: k for k, v in LANG_COL.items()}


def load():
    """`(results, startup_wall_by_lang)` — the two things every consumer needs."""
    res = json.load(open(RESULTS))
    starts = {l: d.get("wall_ms") for l, d in res["startup"]["langs"].items()}
    return res, starts


def compute(res, starts, row, lang):
    """`wall − startup` in ms; `None` when that language has no port or no sample.

    Clamped at 0: a row whose wall lands under that language's own boot time is a
    measurement artefact, not negative work (`harness.verify_compute_floor` fails the run
    when it happens, so a clamp here should never be load-bearing).
    """
    d = res.get(row, {}).get("langs", {}).get(lang)
    if not d or d.get("wall_ms") is None:
        return None
    if row == "startup":
        return d["wall_ms"]
    return max(0.0, d["wall_ms"] - starts.get(lang, 0))


def geomean(values):
    """The geometric mean — the right average for ratios and for times spanning orders of
    magnitude.

    Used for "vs avg" instead of the arithmetic mean, which on this field is dominated by
    whichever language is slowest: on `loop` the arithmetic mean of the other six ports is
    ~541 ms (Python alone is 2.4 s), making Brood's 43 ms read as 0.08× — flattering
    nonsense. The geometric mean of the same six is ~130 ms, so Brood reads 0.3×, which is
    a claim that survives contact with the numbers.
    """
    vals = [v for v in values if v and v > 0]
    if not vals:
        return None
    return math.exp(sum(math.log(v) for v in vals) / len(vals))
