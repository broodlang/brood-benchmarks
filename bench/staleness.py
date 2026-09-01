#!/usr/bin/env python3
"""Report how far the published Brood column has drifted from the brood being tested.

Why this exists. On 2026-09-01 a refresh of the Brood column found every compute row
4-10% slower than the published numbers. Verified with build-parity A/B (`make ab`, both
arms built by the same target, interleaved, pinned, std-image live on both, min-of-3 at
the harness level) it was real: mandelbrot +8.1% against a 0.9% floor, unpinned +6.8%,
splitting into boot +14.5% and JIT'd compute ~+5.5%. It had ridden in across **three
releases** (0.19.1 -> 0.22.0) and nobody knew, because the only thing that measures this
repo's rows is a hand-run harness and nobody had run it since.

The correctness gate next door (`smoke.py`, daily) would never have caught it: the rows
all still *ran*, and produced identical checksums. Timing is invisible to it.

**Why this is a staleness check and not a perf gate.** A CI perf gate on a shared runner
would be a flake generator, and this repo is emphatic about that: even on the dedicated
box, one harness invocation is a coin flip (the governor parks cores at 800 MHz and boosts
to ~4.2 GHz; `regex` read 119.5 vs 139.3 ms back to back on the same binary), which is why
a column refresh must be min-of-3 interleaved invocations. A gate that cannot tell a real
7% from a turbo plateau teaches people to ignore it, and an ignored gate is worse than
none. So this measures nothing. It compares two *facts* — the commit the published column
was measured at, and the commit under test — and says how far apart they are. Deterministic,
zero flake, and it fires on exactly the condition that let the regression hide: numbers
that have silently stopped describing the current runtime.

    python3 bench/staleness.py --brood ../brood/target/release/brood
    python3 bench/staleness.py --brood <path> --fail-on-version   # gate on a version bump

Exits 1 only with --fail-on-version, and only when the *version* has moved — a release
boundary is a rare, meaningful signal, where "any new commit" would nag on every push.
"""
import argparse
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

# `brood 0.22.0 (60a2f6ec)` -> ("0.22.0", "60a2f6ec")
VERSION_RE = re.compile(r"brood\s+(\S+)\s+\(([0-9a-f]+)\)")


def parse_version(text):
    m = VERSION_RE.search(text or "")
    return (m.group(1), m.group(2)) if m else (None, None)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--brood", default="brood", help="brood binary under test")
    ap.add_argument(
        "--fail-on-version",
        action="store_true",
        help="exit 1 when the published column's VERSION differs from the one under test",
    )
    ap.add_argument("--results", default=str(ROOT / "results" / "results.json"))
    args = ap.parse_args()

    meta = json.load(open(args.results)).get("_meta", {})
    pub_version, pub_commit = parse_version(meta.get("versions", {}).get("brood", ""))
    pub_commit = meta.get("brood_commit") or pub_commit

    try:
        out = subprocess.run(
            [args.brood, "--version"], capture_output=True, text=True, timeout=60
        ).stdout
    except (OSError, subprocess.SubprocessError) as e:
        print(f"staleness: cannot run {args.brood}: {e}", file=sys.stderr)
        return 2
    now_version, now_commit = parse_version(out)
    if not now_version:
        print(f"staleness: could not parse a version from {out!r}", file=sys.stderr)
        return 2

    print(f"staleness: published column  brood {pub_version} ({pub_commit})")
    print(f"staleness: binary under test brood {now_version} ({now_commit})")
    if meta.get("brood_refresh"):
        print(f"staleness: {meta['brood_refresh']}")

    if pub_commit == now_commit:
        print("staleness: up to date — the published column describes this binary.")
        return 0

    # Commit distance is a nicety: it only works from a checkout that has both commits,
    # which CI does (it checks brood out beside this repo) and a local run may not.
    for candidate in (ROOT.parent / "brood", ROOT.parent / "brood-src"):
        if not (candidate / ".git").exists():
            continue
        r = subprocess.run(
            ["git", "rev-list", "--count", f"{pub_commit}..{now_commit}"],
            cwd=candidate, capture_output=True, text=True,
        )
        if r.returncode == 0 and r.stdout.strip().isdigit():
            print(f"staleness: {r.stdout.strip()} brood commit(s) since the column was measured")
        break

    if pub_version != now_version:
        msg = (
            f"staleness: the published Brood column was measured at {pub_version} and brood is "
            f"now {now_version}. Those numbers no longer describe the runtime, and a timing "
            f"regression in between is invisible to every other gate here (the rows still run "
            f"and still checksum). Refresh it: install the LEAN build "
            f"(cd ../brood && make install INSTALL_FEATURES='$(RUN_FEATURES)'), then take the "
            f"min over 3 interleaved `bench/harness.py --langs brood` invocations — see CLAUDE.md."
        )
        print(msg, file=sys.stderr)
        return 1 if args.fail_on_version else 0

    print("staleness: same version, newer commit — a refresh is due but not overdue.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
