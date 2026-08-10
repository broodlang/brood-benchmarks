#!/usr/bin/env python3
"""Brood's own rows over time — the chart the positioning map cannot be.

    python3 bench/trend.py            # → results/trend.svg (+ a table on stdout)
    python3 bench/trend.py --rows spawn-live,fib

Why this exists. `positioning.svg` places seven languages by one scalar each, aggregated
over 27 rows. That is the right shape for "where does this runtime stand" and the wrong
shape for "did the thing I just optimised move": a 16% win on one row shifts a 27-row
geometric mean by well under a pixel, so real progress reads as no progress. `spawn-live`
went 5362 → 1771 ms across seven published runs — a 3× improvement completely invisible on
that map.

The data is every published `results/results.json` in git history, so this is a record of
what was actually published, not a re-measurement. One point per run date (the last commit
for that date, i.e. the state that was published), values normalised to each row's first
appearance so rows spanning 20 ms and 5 s share an axis.

Caveats it prints rather than hides: the field drifts ~10% run to run, so read shapes and
not wiggles; and `startup`'s RSS is bimodal (a cold expanded-prelude boot costs ~42 MB
against ~23 MB warm, per brood's docs/handoff.md), so that row tracks boot-cache state at
least as much as it tracks the runtime's footprint.
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"

# Rows worth trending: the concurrency story the positioning map cannot show, plus a
# couple of compute rows as controls (if everything moves together it was the machine).
DEFAULT_ROWS = ["spawn-live", "supervisor", "ring", "pingpong", "fib", "bintree"]
COLOR = ["#c0392b", "#8e44ad", "#2980b9", "#27ae60", "#d35400", "#16a085", "#e67e22"]


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True).stdout


def history(rows):
    """`[(date, {row: wall_ms})]` oldest-first — one entry per published run date."""
    commits = git("log", "--format=%h", "--", "results/results.json").split()
    seen = {}
    for c in commits:  # newest first, so the first hit for a date is that run's publish
        raw = git("show", f"{c}:results/results.json")
        if not raw.strip():
            continue
        try:
            d = json.loads(raw)
        except json.JSONDecodeError:
            continue  # a truncated results.json is in the history; skip rather than die
        date = (d.get("_meta", {}).get("date") or "").split(" ")[0]
        if not date or date in seen:
            continue
        vals = {}
        for r in rows:
            lang = d.get(r, {}).get("langs", {}).get("brood") or {}
            if lang.get("wall_ms") is not None:
                # Carry the row's N: a row whose size changed is NOT comparable across
                # that change, and normalising through one invents a regression. `fib`
                # went N=30 -> 35 and `bintree` 40 -> 200 on 2026-06-14, which read as a
                # 285% blow-up until this was handled.
                vals[r] = (lang["wall_ms"], d.get(r, {}).get("n"))
        if vals:
            seen[date] = vals
    return sorted(seen.items())


def render(series, dates, rows):
    W, H = 820, 460
    ml, mr, mt, mb = 60, 150, 54, 62
    pw, ph = W - ml - mr, H - mt - mb
    allv = [v for r in rows for v in series[r] if v is not None]
    if not allv:
        return None
    ymax = max(allv) * 1.08
    ymin = min(0.0, min(allv))
    n = len(dates)

    def X(i):
        return ml + (i / max(1, n - 1)) * pw

    def Y(v):
        return mt + ph - (v - ymin) / (ymax - ymin) * ph

    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}" font-family="system-ui,Segoe UI,Helvetica,Arial,sans-serif">',
         f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
         f'<text x="{W/2}" y="24" text-anchor="middle" font-size="17" font-weight="700" '
         f'fill="#222">Brood over time — each row vs its own first published run</text>',
         f'<text x="{W/2}" y="42" text-anchor="middle" font-size="12" fill="#777">'
         f'lower is faster; 100% = that row\'s first appearance</text>']
    # gridlines every 25%
    t = 0
    while t <= ymax:
        y = Y(t)
        s.append(f'<line x1="{ml}" y1="{y:.1f}" x2="{ml+pw}" y2="{y:.1f}" stroke="#eee"/>')
        s.append(f'<text x="{ml-8}" y="{y+4:.1f}" text-anchor="end" font-size="11" '
                 f'fill="#555">{t:.0f}%</text>')
        t += 25
    s.append(f'<line x1="{ml}" y1="{Y(100):.1f}" x2="{ml+pw}" y2="{Y(100):.1f}" '
             f'stroke="#bbb" stroke-dasharray="4,3"/>')
    for i, d in enumerate(dates):
        if n <= 12 or i % max(1, n // 10) == 0 or i == n - 1:
            s.append(f'<text x="{X(i):.1f}" y="{mt+ph+18}" text-anchor="middle" '
                     f'font-size="10" fill="#555" transform="rotate(35 {X(i):.1f} {mt+ph+18})">'
                     f'{d[5:]}</text>')
    labels = []
    for k, r in enumerate(rows):
        c = COLOR[k % len(COLOR)]
        pts = [(X(i), Y(v)) for i, v in enumerate(series[r]) if v is not None]
        if not pts:
            continue
        s.append(f'<polyline fill="none" stroke="{c}" stroke-width="2.2" stroke-opacity="0.9" '
                 f'points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}"/>')
        for x, y in pts:
            s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.6" fill="{c}"/>')
        last = [v for v in series[r] if v is not None][-1]
        labels.append([pts[-1][1], c, r, last])
    # Push the right-hand labels apart: several rows converge near the same value, and
    # stacked text is unreadable exactly where the interesting rows are.
    labels.sort()
    for i in range(1, len(labels)):
        if labels[i][0] - labels[i - 1][0] < 15:
            labels[i][0] = labels[i - 1][0] + 15
    for y, c, r, last in labels:
        s.append(f'<text x="{ml+pw+10}" y="{y+4:.1f}" font-size="12" font-weight="600" '
                 f'fill="{c}">{r} <tspan font-weight="400" fill="#777">{last:.0f}%</tspan></text>')
    s.append(f'<text x="{ml+pw/2}" y="{H-10}" text-anchor="middle" font-size="12" fill="#333">'
             f'published run date — the field drifts ~10% run to run, so read shapes not wiggles</text>')
    s.append('</svg>')
    return "\n".join(s)


def main():
    rows = DEFAULT_ROWS
    if "--rows" in sys.argv:
        rows = sys.argv[sys.argv.index("--rows") + 1].split(",")
    hist = history(rows)
    if not hist:
        print("no published results.json found in history")
        return 1
    dates = [d for d, _ in hist]
    series, first, skipped = {}, {}, {}
    for r in rows:
        # Compare only runs at the row's CURRENT size; earlier runs at a different N
        # measure different work and are dropped rather than silently rebased.
        latest_n = next((v[r][1] for _, v in reversed(hist) if r in v), None)
        vals = []
        for _, v in hist:
            got = v.get(r)
            if got is None or got[1] != latest_n:
                if got is not None:
                    skipped[r] = skipped.get(r, 0) + 1
                vals.append(None)
                continue
            first.setdefault(r, got[0])
            vals.append(got[0] / first[r] * 100.0)
        series[r] = vals
    for r, k in sorted(skipped.items()):
        print(f"  note: {r} — {k} earlier run(s) dropped (ran at a different N)")
    svg = render(series, dates, rows)
    if svg:
        (RESULTS / "trend.svg").write_text(svg)
        print(f"wrote {RESULTS/'trend.svg'} — {len(dates)} runs, {len(rows)} rows")
    print(f"\n{'row':<12}{'first':>12}{'latest':>12}{'change':>10}  (runs at the current N only)")
    for r in rows:
        pct = [v for v in series[r] if v is not None]
        if not pct:
            print(f"{r:<12}{'—':>12}")
            continue
        a = first[r]
        b = a * pct[-1] / 100.0
        print(f"{r:<12}{a:>10.0f}ms{b:>10.0f}ms{pct[-1]-100:>9.1f}%")
    return 0


if __name__ == "__main__":
    sys.exit(main())
