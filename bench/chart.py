#!/usr/bin/env python3
"""Render results/positioning.svg from results/results.json — a 2-D map of where
each language sits: compute speed (x, log) vs memory footprint (y). Lower-left =
fast + light. Pure-Python SVG (no deps), so it regenerates anywhere and renders
inline on GitHub.

    python3 bench/chart.py
"""
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"

# The pure single-thread compute benchmarks (exclude startup / concurrency /
# the materialization-y outliers handled elsewhere) — this is "compute speed".
COMPUTE = ["fib", "loop", "reduce", "primes", "collatz", "mandelbrot",
           "matmul", "strings", "wordcount", "bintree", "sort"]

# Brand-ish colours, kept distinct.
COLOR = {
    "brood": "#c0392b", "elixir": "#8e44ad", "python": "#2980b9",
    "node": "#27ae60", "ruby": "#d35400", "dotnet": "#16a085",
    "clojure": "#e67e22",
}
LABEL = {"brood": "Brood", "elixir": "Elixir", "python": "Python",
         "node": "Node", "ruby": "Ruby", "dotnet": ".NET", "clojure": "Clojure"}


def collect(results):
    """For each lang: (compute slowdown vs the fastest, base memory MB).

    Compute **excludes startup** (wall − that language's own startup, per
    benchmark, summed) — otherwise a slow-booting runtime like the BEAM looks
    slow at compute when it isn't. The aggregate (sum across the compute
    benchmarks) is robust to the per-benchmark noise that bites when a fast
    runtime's compute is smaller than its startup."""
    startup = {l: d["wall_ms"]
               for l, d in results.get("startup", {}).get("langs", {}).items()
               if "wall_ms" in d and "error" not in d}
    langs = set()
    for b in COMPUTE:
        langs |= set(results.get(b, {}).get("langs", {}))
    # Aggregate compute (ms) = Σ max(0, wall − startup) over the compute benchmarks.
    agg = {}
    for l in langs:
        s, ran = 0.0, False
        for b in COMPUTE:
            d = results.get(b, {}).get("langs", {}).get(l, {})
            if "wall_ms" not in d or "error" in d:
                continue
            s += max(0.0, d["wall_ms"] - startup.get(l, 0.0))
            ran = True
        if ran:
            agg[l] = max(s, 1.0)
    fastest = min(agg.values()) if agg else 1.0
    out = {}
    for l, a in agg.items():
        srow = results.get("startup", {}).get("langs", {}).get(l, {})
        if "rss_kb" in srow:
            mem = srow["rss_kb"] / 1024
        else:
            mems = [v["rss_kb"] / 1024 for b in COMPUTE
                    for k, v in results.get(b, {}).get("langs", {}).items()
                    if k == l and "rss_kb" in v]
            mem = min(mems) if mems else 0
        out[l] = (a / fastest, mem)
    return out


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def render(points):
    W, H = 760, 480
    ml, mr, mt, mb = 70, 30, 50, 60     # margins
    pw, ph = W - ml - mr, H - mt - mb
    xs = [p[0] for p in points.values()]
    ys = [p[1] for p in points.values()]
    # x: log scale from 1 to a bit past the max slowdown.
    xmin, xmax = 1.0, max(xs) * 1.25
    lxmin, lxmax = math.log10(xmin), math.log10(xmax)
    ymin, ymax = 0.0, max(ys) * 1.15

    def X(v):
        return ml + (math.log10(v) - lxmin) / (lxmax - lxmin) * pw

    def Y(v):
        return mt + ph - (v - ymin) / (ymax - ymin) * ph

    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}" font-family="system-ui,Segoe UI,Helvetica,Arial,sans-serif">']
    s.append(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')
    s.append(f'<text x="{W/2}" y="26" text-anchor="middle" font-size="17" '
             f'font-weight="700" fill="#222">Where the languages land — compute speed vs memory</text>')
    # Axes
    s.append(f'<line x1="{ml}" y1="{mt+ph}" x2="{ml+pw}" y2="{mt+ph}" stroke="#888" stroke-width="1"/>')
    s.append(f'<line x1="{ml}" y1="{mt}" x2="{ml}" y2="{mt+ph}" stroke="#888" stroke-width="1"/>')
    # X gridlines/ticks at 1,2,5,10,20,50,100
    for tick in [1, 2, 5, 10, 20, 50, 100]:
        if tick > xmax:
            break
        x = X(tick)
        s.append(f'<line x1="{x:.1f}" y1="{mt}" x2="{x:.1f}" y2="{mt+ph}" stroke="#eee" stroke-width="1"/>')
        s.append(f'<text x="{x:.1f}" y="{mt+ph+18}" text-anchor="middle" font-size="12" fill="#555">{tick}×</text>')
    # Y gridlines/ticks
    ystep = 20 if ymax <= 120 else 40
    t = 0
    while t <= ymax:
        y = Y(t)
        s.append(f'<line x1="{ml}" y1="{y:.1f}" x2="{ml+pw}" y2="{y:.1f}" stroke="#eee" stroke-width="1"/>')
        s.append(f'<text x="{ml-10}" y="{y+4:.1f}" text-anchor="end" font-size="12" fill="#555">{t}</text>')
        t += ystep
    # Axis labels
    s.append(f'<text x="{ml+pw/2}" y="{H-16}" text-anchor="middle" font-size="13" fill="#333">'
             f'compute slowdown vs the fastest — startup excluded, log scale — left is faster</text>')
    s.append(f'<text x="18" y="{mt+ph/2}" text-anchor="middle" font-size="13" fill="#333" '
             f'transform="rotate(-90 18 {mt+ph/2})">base memory (MB) — lower is lighter</text>')
    # "ideal" hint
    s.append(f'<text x="{ml+8}" y="{mt+ph-8}" font-size="11" fill="#aaa">↙ fast &amp; light</text>')
    # Points
    for l, (gx, my) in sorted(points.items(), key=lambda kv: kv[1][1]):
        c = COLOR.get(l, "#444")
        cx, cy = X(gx), Y(my)
        s.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="7" fill="{c}" '
                 f'fill-opacity="0.85" stroke="#fff" stroke-width="1.5"/>')
        # Flip the label to the left of the dot when near the right edge.
        if cx > ml + pw * 0.7:
            tx, anchor = cx - 11, "end"
        else:
            tx, anchor = cx + 11, "start"
        s.append(f'<text x="{tx:.1f}" y="{cy+4:.1f}" text-anchor="{anchor}" font-size="13" '
                 f'font-weight="600" fill="{c}">{esc(LABEL.get(l, l))} '
                 f'<tspan font-weight="400" fill="#777">({gx:.0f}× · {my:.0f}MB)</tspan></text>')
    s.append('</svg>')
    return "\n".join(s)


def main():
    results = json.loads((RESULTS / "results.json").read_text())
    points = collect(results)
    svg = render(points)
    (RESULTS / "positioning.svg").write_text(svg)
    print(f"wrote {RESULTS/'positioning.svg'} — {len(points)} languages")
    for l, (g, m) in sorted(points.items(), key=lambda kv: kv[1][0]):
        print(f"  {l:8} {g:5.1f}× slowdown, {m:5.1f} MB")


if __name__ == "__main__":
    main()
