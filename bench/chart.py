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
from common import CHART_ROWS, CHART_OVERLAY_ROW, compute, geomean  # noqa: E402

# Brand-ish colours, kept distinct. C is gold: the one hue region the other seven
# leave free, and it clears the lightness/chroma checks the obvious dark-slate pick
# failed (it read as grey).
#
# KNOWN LIMITATION, deliberate: python(blue) vs elixir(purple) sit at ΔE 4.6 under
# deuteranopia — a classic blue/purple confusion. Nudging the purple does not fix it
# (4.6 -> 5.1); only moving one language out of the blue/purple region would, and
# trading away two languages' recognisable colours is the worse deal. Both charts
# therefore carry a DIRECT TEXT LABEL on every mark, so identity never depends on
# colour. Keep it that way if you restyle either chart.
COLOR = {
    "brood": "#c0392b", "elixir": "#8e44ad", "python": "#2980b9",
    "node": "#27ae60", "ruby": "#d35400", "dotnet": "#16a085",
    "clojure": "#e67e22", "c": "#b7950b",
}
LABEL = {"brood": "Brood", "elixir": "Elixir", "python": "Python",
         "node": "Node", "ruby": "Ruby", "dotnet": ".NET", "clojure": "Clojure",
         "c": "C"}


def collect(results):
    """For each lang: `(overall slowdown, base memory MB, overlay slowdown or None)`.

    **Aggregated as a geometric mean of per-row ratios, not a sum of wall times.** The sum
    this used to take is dominated by whichever row is slowest in absolute ms — with 27
    rows in play `mandelbrot` and `spawn-live` would between them decide everyone's
    position, and a 16% win on a small row could not move the picture at all. A geomean of
    per-row ratios weights every benchmark equally and is what the standings table already
    reports, so chart and table now mean the same thing.

    Compute **excludes startup** (wall − that language's own startup, per row) — otherwise
    a slow-booting runtime like the BEAM looks slow at compute when it isn't.

    The third element is the same geomean *including* `spawn-live`, for the five languages
    that implement it — reported on stdout, not plotted. It was drawn as a second marker
    briefly and removed: one row inside a 28-row geomean shifts a point by ~2 px (Brood
    4.76 -> 4.84), so the marker sat on top of the filled one and implied a significance it
    does not have. `spawn-live` belongs in the per-row tables, not in a field-wide scalar.
    """
    starts = {l: d["wall_ms"]
              for l, d in results.get("startup", {}).get("langs", {}).items()
              if "wall_ms" in d and "error" not in d}
    langs = set()
    for b in CHART_ROWS:
        langs |= set(results.get(b, {}).get("langs", {}))

    def val(b, l):
        return compute(results, starts, b, l)

    # **Compare every language over the SAME rows.** Skipping a language's missing rows
    # and aggregating what is left does not penalise a broken run, it REWARDS it. So the
    # row set is the intersection of what every plotted language completed; one
    # language's failure costs that row for everyone and cannot flatter the failer.
    ran = {l: {b for b in CHART_ROWS if val(b, l) is not None} for l in langs}
    ran = {l: rows for l, rows in ran.items() if rows}
    common = sorted(set.intersection(*ran.values())) if ran else []
    dropped = sorted(set(CHART_ROWS) - set(common))
    if dropped:
        missing = {b: sorted(l for l in ran if b not in ran[l]) for b in dropped}
        print("  aggregate excludes (not completed by every language): "
              + ", ".join(f"{b} [missing: {', '.join(missing[b])}]" for b in dropped))
    if not common:
        print("  WARNING: no row was completed by every language; plotting nothing.")
        return {}, 0
    print(f"  aggregating {len(common)} rows across {len(ran)} languages (geomean of per-row ratios)")

    def geo_over(rows, langset):
        """Per-row ratio against the fastest of `langset`, geomean'd down to one number."""
        best = {b: min(val(b, l) or float("inf") for l in langset) for b in rows}
        out = {}
        for l in langset:
            ratios = [(val(b, l) or 0.0) / best[b] for b in rows if best.get(b)]
            out[l] = geomean(ratios) or 1.0
        return out

    overall = geo_over(common, list(ran))
    # Normalise so the leader reads 1.0x. A geomean of per-row ratios is scored against the
    # best time on EACH row, so a language only reaches 1.0 by winning EVERY row — .NET wins
    # 13 of 27 and scored 2.06 raw, which left an axis labelled "vs the fastest" with nobody
    # at 1x. Dividing through by the leader restores what the label promises and what the
    # old sum-of-times aggregate gave by construction; the ordering and every ratio between
    # languages are unchanged.
    lead = min(overall.values())
    raw = dict(overall)
    overall = {l: v / lead for l, v in overall.items()}
    leader = min(raw, key=lambda l: raw[l])
    print(f"  leader {leader} raw {raw[leader]:.2f}x vs the per-row best "
          f"(nobody wins every row) -> normalised to 1.00x")

    # Overlay: re-aggregate over the languages that have the process-model row, on their
    # own shared row set plus that row. Computed within that subset — a ratio against a
    # language that never ran the row would not mean anything.
    over_langs = [l for l in ran if val(CHART_OVERLAY_ROW, l) is not None]
    overlay = {}
    if len(over_langs) >= 2:
        sub = sorted(set.intersection(*(ran[l] for l in over_langs)) | {CHART_OVERLAY_ROW})
        overlay = geo_over(sub, over_langs)
        olead = min(overlay.values())
        overlay = {l: v / olead for l, v in overlay.items()}
        print(f"  overlay: {len(sub)} rows incl. {CHART_OVERLAY_ROW} across {', '.join(sorted(over_langs))}")

    out = {}
    for l in ran:
        srow = results.get("startup", {}).get("langs", {}).get(l, {})
        if "rss_kb" in srow:
            mem = srow["rss_kb"] / 1024
        else:
            mems = [v["rss_kb"] / 1024 for b in CHART_ROWS
                    for k, v in results.get(b, {}).get("langs", {}).items()
                    if k == l and "rss_kb" in v]
            mem = min(mems) if mems else 0
        out[l] = (overall[l], mem, overlay.get(l))
    return out, len(common)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def render(points, nrows):
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
             f'font-weight="700" fill="#222">Where the languages land — overall speed vs memory</text>')
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
             f'overall slowdown vs the fastest — geomean of {nrows} rows, startup excluded, log scale — left is faster</text>')
    s.append(f'<text x="18" y="{mt+ph/2}" text-anchor="middle" font-size="13" fill="#333" '
             f'transform="rotate(-90 18 {mt+ph/2})">base memory (MB) — lower is lighter</text>')
    # "ideal" hint
    s.append(f'<text x="{ml+8}" y="{mt+ph-8}" font-size="11" fill="#aaa">↙ fast &amp; light</text>')
    # Points
    for l, (gx, my, ox) in sorted(points.items(), key=lambda kv: kv[1][1]):
        c = COLOR.get(l, "#444")
        cx, cy = X(gx), Y(my)
        s.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="7" fill="{c}" '
                 f'fill-opacity="0.85" stroke="#fff" stroke-width="1.5"/>')
        # Flip the label to the left of the dot when near the right edge, and keep it
        # clear of its own overlay marker when that sits to the right.
        if cx > ml + pw * 0.7:
            tx, anchor = cx - 11, "end"
        else:
            tx, anchor = cx + 11, "start"
        s.append(f'<text x="{tx:.1f}" y="{cy+4:.1f}" text-anchor="{anchor}" font-size="13" '
                 f'font-weight="600" fill="{c}">{esc(LABEL.get(l, l))} '
                 f'<tspan font-weight="400" fill="#777">({gx:.1f}× · {my:.0f}MB)</tspan></text>')
    s.append('</svg>')
    return "\n".join(s)


def render_bars(points):
    """results/overview.svg — the one-glance ranking, for the top of the README.

    The positioning map answers "fast AND light, in two dimensions"; that is the right
    picture but it takes a paragraph to read. This answers the blunter question a reader
    actually opens with — *how far off the pace is Brood?* — as a sorted bar chart, which
    is what magnitude-across-categories should be.

    EMPHASIS, not categorical: Brood is the subject of this repo and the rest are context,
    so Brood carries its own colour, C carries its own as the floor the chart is scaled
    against, and everyone else is one neutral grey. That is the documented form for "one
    series is the point" — and it sidesteps the palette's blue/purple CVD clash entirely,
    since three well-separated colours replace eight.

    Single measure, so no legend: every bar carries its own name and number, so identity
    never rests on colour at all.

    The scale is linear and starts at zero, because bar LENGTH is the encoding — a log
    axis here would make Python's 53x look like a near neighbour of Brood's 9.6x. The
    price is that the fast end is compressed; the per-bar numbers carry the detail the
    lengths cannot.
    """
    GREY = "#b3bac1"
    order = sorted(points, key=lambda l: points[l][0])
    W, rowh, top, left, right = 760, 34, 58, 92, 96
    H = top + rowh * len(order) + 34
    worst = max(points[l][0] for l in order)
    pw = W - left - right

    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
         f'viewBox="0 0 {W} {H}" font-family="system-ui,Segoe UI,Helvetica,Arial,sans-serif">',
         f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
         f'<text x="{left}" y="26" font-size="17" font-weight="700" fill="#222">'
         f'Overall speed — geomean across the rows every language runs</text>',
         f'<text x="{left}" y="44" font-size="12" fill="#777">'
         f'lower is faster · 1.0× = the leader on this set · C is a machine-floor reference, '
         f'not a peer</text>']

    for i, l in enumerate(order):
        g = points[l][0]
        y = top + i * rowh
        bw = max(2.0, pw * (g / worst))
        brood = l == "brood"
        c = COLOR["brood"] if brood else COLOR["c"] if l == "c" else GREY
        # 4px rounded data-end, anchored to the baseline at x=left.
        s.append(f'<rect x="{left}" y="{y}" width="{bw:.1f}" height="{rowh-12}" rx="4" '
                 f'fill="{c}"/>')
        s.append(f'<text x="{left-10}" y="{y+16}" text-anchor="end" font-size="13" '
                 f'font-weight="{"700" if brood else "500"}" '
                 f'fill="{"#222" if brood else "#555"}">{esc(LABEL.get(l, l))}</text>')
        s.append(f'<text x="{left+bw+8:.1f}" y="{y+16}" font-size="13" '
                 f'font-weight="{"700" if brood else "400"}" fill="#444">{g:.1f}×</text>')

    s.append('</svg>')
    return "\n".join(s)


def main():
    results = json.loads((RESULTS / "results.json").read_text())
    points, nrows = collect(results)
    svg = render(points, nrows)
    (RESULTS / "positioning.svg").write_text(svg)
    (RESULTS / "overview.svg").write_text(render_bars(points))
    print(f"wrote {RESULTS/'positioning.svg'} and {RESULTS/'overview.svg'} "
          f"— {len(points)} languages")
    for l, (g, m, o) in sorted(points.items(), key=lambda kv: kv[1][0]):
        tail = f", {o:5.2f}× incl. spawn-live" if o else ""
        print(f"  {l:8} {g:5.2f}× slowdown, {m:5.1f} MB{tail}")


if __name__ == "__main__":
    main()
