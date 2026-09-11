#!/usr/bin/env python3
"""Merge N brood-only harness invocations into the published field results.

CLAUDE.md: a Brood-column refresh is the MIN over >=3 interleaved invocations —
one invocation lands on a turbo plateau and stays there, so best-of-N inside one
invocation hides nothing while two invocations minutes apart read the same row 17%
apart. This picks, per row, the whole record from the invocation with the best
ranking figure (so wall/rss/cpu stay internally consistent rather than being
mixed from different runs).

`latency` is ranked by p99 rather than wall: its wall is fixed by the arrival
schedule, so a min-wall pick there would be a coin flip on a number that says
nothing.
"""
import json, sys, datetime
from pathlib import Path

RESULTS = Path("results")


def rank(row_name, rec):
    if row_name == "latency":
        return rec.get("metrics", {}).get("p99_us", float("inf"))
    return rec["wall_ms"]


def main(labels, commit, version, out=RESULTS / "results.json"):
    field = json.loads((RESULTS / "results.json").read_text())
    runs = {l: json.loads((RESULTS / f"results.{l}.json").read_text()) for l in labels}

    rows, problems = [], []
    for name, row in field.items():
        if name == "_meta":
            continue
        cands = []
        for label, r in runs.items():
            rec = r.get(name, {}).get("langs", {}).get("brood")
            if rec:
                cands.append((label, rec))
        if not cands:
            problems.append(f"{name}: no brood record in any run")
            continue
        # A checksum that moved means the program computes something else now; that is
        # a correctness finding, not a timing one, and must not be published quietly.
        sums = {rec.get("checksum") for _, rec in cands}
        old = row["langs"].get("brood", {})
        if len(sums) > 1:
            problems.append(f"{name}: checksums disagree across runs: {sums}")
        elif old.get("checksum") and sums != {old["checksum"]}:
            problems.append(
                f"{name}: checksum moved vs the published column: "
                f"{old['checksum']} -> {sums.pop()}")
        label, best = min(cands, key=lambda c: rank(name, c[1]))
        spread = ""
        vals = sorted(rank(name, rec) for _, rec in cands)
        if vals[0]:
            spread = f"{(vals[-1] - vals[0]) / vals[0] * 100:.1f}%"
        delta = ""
        if old.get("wall_ms"):
            delta = f"{(best['wall_ms'] - old['wall_ms']) / old['wall_ms'] * 100:+.1f}%"
        rows.append((name, old.get("wall_ms"), best["wall_ms"], delta, spread, label))
        row["langs"]["brood"] = best

    if problems:
        print("REFUSING to merge:", file=sys.stderr)
        for p in problems:
            print("  " + p, file=sys.stderr)
        return 1

    today = datetime.date.today().isoformat()
    meta = field["_meta"]
    field_date = meta["date"].split(" ")[0]
    meta["brood_commit"] = commit
    meta["versions"]["brood"] = version
    meta["brood_refresh"] = (
        f"brood column re-measured {today} at {version} (brood-only, min of "
        f"{len(labels)} interleaved harness invocations; other columns {field_date})")

    print(f"{'row':16} {'published':>10} {'new':>10} {'delta':>8} {'spread':>8}  from")
    for name, o, n, d, s, label in rows:
        print(f"{name:16} {o if o is not None else '-':>10} {n:>10} {d:>8} {s:>8}  {label}")

    Path(out).write_text(json.dumps(field, indent=2))
    print(f"\nwrote {out}  ({len(rows)} brood rows from {len(labels)} invocations)")
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 4:
        sys.exit("usage: merge_brood.py <commit> <version-string> <label> [label ...]")
    sys.exit(main(sys.argv[3:], sys.argv[1], sys.argv[2]))
