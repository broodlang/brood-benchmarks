# brood-benchmarks — guidance for Claude

A cross-language micro-benchmark suite: 31 programs across Brood, Clojure, Elixir,
Python, Node, Ruby and .NET, run under one harness. 28 are implemented in every
language.

**C is a partial column and a deliberate one** (added 2026-08-14): 16 of the 31 rows, as a
machine-floor reference so ratios mean "vs roughly what the hardware does" rather than "vs
the fastest managed runtime". A row opts in with the `"all+c"` sentinel rather than `"all"` —
C is *not* in `ALL`, so a missing C port is a loud absence rather than an empty cell. Two
consequences worth knowing before touching it:
- **Adding a partial column narrows the field-wide aggregate for everyone.** Both `chart.py`
  and `docs.py:overall_numbers` intersect the rows every column implements, so C landing took
  that set 27 → 15 and moved the reference from .NET to C. Field-wide figures are therefore
  **not comparable across that date**; the per-row tables and `trend.svg` are.
- **Watch for C numbers that are too SLOW.** The first C run lost to Brood on `reduce` and
  `strings` and to Node on `primes`; all three were self-inflicted (`sprintf` format parsing,
  64-bit `idivq` where the field uses 32-bit ints, and a `volatile` pointer defeating the
  inliner). A C row that loses is a bug report about this repo's C, not a finding — see
  `bench/c/README.md`, which also records the elision audit and why there is no asm barrier.

`spawn-live` runs in five, but only **two of those five provide the same
thing** — Brood and Elixir have isolated preemptively-scheduled processes with
copying sends; Node, .NET and Python have coroutines/tasks on a shared heap, and are
included so the `cores`/`CPU·s` columns make that difference legible rather than to
claim a like-for-like comparison. `supervisor` runs only in Brood and Elixir, the two
with a runtime supervisor at all. `latency` runs in five (Ruby and Clojure ports are simply
unwritten) and is the one row reported as **percentiles**, ranked by p99 rather than by wall —
its wall is fixed by the arrival schedule, so wall says nothing about which runtime is better. See [README.md](README.md) for the full methodology.

## Running

```sh
python3 bench/smoke.py                # does every brood row still RUN? (~7 s) — run this first
python3 bench/smoke.py --langs all    # every port + cross-language checksums (~3 min)
python3 bench/harness.py              # full suite → results/results.json + report.md
python3 bench/test_guard.py           # regression test for the corruption guard (instant)
python3 bench/harness.py --quick      # smaller sizes, smoke test
python3 bench/harness.py --only fib   # subset (comma-separated)
python3 bench/harness.py --langs brood,node
python3 bench/chart.py                # regenerate results/overview.svg from results.json
```

- **`bench/smoke.py` is the gate; run it before anything else and after any brood
  upgrade.** The rows in this repo have now died wholesale *three* times from renames
  made in the brood repo — ADR-227's `sqrt` move (KI-42, two rows, three days
  unnoticed), then the v0.9.0/v0.10.0 namespacing waves (KI-44: `getenv`→`os/getenv`,
  `now-ns`→`os/now-ns`, `(table)`→`(table/new)`, `start-supervisor`/`stop-supervisor`→
  `supervisor/start`/`gen/stop`, `http/http-get`→`http/fetch`, and `require` deleted
  outright — **30 of 31 rows dead**). Brood's own migration sweeps cover its `std/`,
  `tests/`, `examples/` and `breakage/`; they cannot see this checkout. Nothing else here
  runs these programs for *correctness*.
  - It checks **two** things, and the second is the one that matters: the process exits 0,
    **and no `unbound symbol` appears in stdout or stderr**. Exit status alone is not
    enough — brood reports an unbound name as a compile-time `warning:` and only *errors*
    when the reference is evaluated, so a rename on a branch a small run never takes exits
    0, prints the right checksum, and is still broken. Verified by sabotage: a
    `(sqrt m)` added to an untaken branch of `fib` exits 0 with the right answer and the
    gate still fails it.
  - With `--langs` naming more than one language it also **compares the rows' printed
    checksums across languages** — the harness's cross-language correctness check without
    the tens of minutes of timing. That is what catches a row that runs but computes the
    wrong thing.
  - Unlike the harness, it never writes `results/` — safe to run any time.
  - `.github/workflows/smoke.yml` runs it on push/PR **and on a daily schedule**. The
    schedule is the point: the breakage always originates in the *other* repo, so a
    push-triggered gate here would not have fired for either incident. The daily job
    builds `broodlang/brood@main` and points the check at it.

- **A corrupt run now fails itself; you do not have to remember anything.** `startup` is
  subtracted from all 27 other rows, so an over-estimate of it corrupts the whole table
  rather than merely blurring it — and at the old best-of-3 default it did (2026-07-28):
  a high Elixir boot sample (197 ms against a true ~182 ms) exceeded its *wall* on six
  short rows, so `compute = max(0, wall − startup)` clamped them to `0.0 ms`, which sorts
  to **1st place** and made Brood's ratios against it nonsense (`bintree` `103×` where it
  is `12×`). Two mechanisms close that off, both in `harness.py`:
  - `startup` now defaults to **best of `max(runs, 9)`** — it is the one measurement whose
    error propagates everywhere, so it is sampled hardest. `--startup-runs` still overrides.
  - `verify_compute_floor` fails the run (**exit 1**, named cells on stderr, a banner in
    `report.md`) if any cell's wall is at or below that language's own startup. `--quick`
    warns without failing, because its smoke-test sizes clamp by construction.
  Exposure scales with how close a runtime's boot variance is to a row's total work, so
  Elixir (~±6 ms boot, rows of 4–10 ms) is the one that bites; nothing about it is
  Elixir-specific though. `python3 bench/test_guard.py` pins all of this — the guard
  cannot be exercised on demand from a real run (whether one clamps is boot-sample luck),
  so it is tested against fabricated timings instead.
- The harness runs `brood` from PATH (`~/.local/bin/brood` on this machine).
  **Rebuild + reinstall it first** when benchmarking a new brood commit, and
  **always install the LEAN build** — from `../brood`:

      make install INSTALL_FEATURES='$(RUN_FEATURES)'

  `make install` alone adds `brood/dev-tools` (the REPL, `nest test`, the observer,
  the MCP server) — developer tooling that is not part of the runtime an app ships.
  The reason to install lean is **build consistency, not a measured startup cost**:
  `RUN_FEATURES` is exactly what **`make ab` measures** (see the `RUN_FEATURES`
  comment in the brood Makefile) and what `nest release` embeds, so installing lean
  puts the published cross-language numbers, the A/B numbers, and what users run on
  one build.

  Measured 2026-07-29 (same commit, best-of-9 after a boot-cache warmup, pinned):
  lean and dev-tools startup are **identical** — 10 ms / 18.8 MB each, binary 38.05
  vs 38.32 MB. The DEV_MODULES are `require`d on demand, not baked into the boot
  image, so dev-tools does *not* inflate the `startup` row or base RSS. Don't claim
  it does; the case for lean is consistency.

  This makes the installed `nest` lean too. **Verified 2026-07-30: `nest test` still runs
  fine on the lean build** — an earlier note here claimed it would not work until you
  reinstalled with the default `make install`, and that is wrong. Reinstall if you find a
  dev-tool that is genuinely absent, not on the strength of this warning.

  (Never `cargo build -p brood` — it doesn't relink the binary; see the brood
  CLAUDE.md.)
- A full run takes tens of minutes and is timing-sensitive: **don't run builds
  or other heavy work concurrently.**
- **Every harness invocation rewrites `results/results.json` + `results/report.md` — including
  `--quick` and `--only`.** So a one-row smoke test clobbers the published numbers; they are
  committed, so `git diff results/` shows it and restoring is easy, but check before you
  commit. (Walked into on 2026-08-05: a `--quick --only fib --langs brood` sanity check
  replaced a full seven-language run's results.) Use `--label X` for a run you want to keep
  separately — `results/{results,report}.<label>.*` is gitignored.
- The harness does one discarded warmup run per language before measuring. Don't
  remove it: wall is a best-of but RSS a worst-of, so without it Brood's
  build-id-keyed boot cache populates during run 1 after every rebuild and that
  cold boot (~28.5 MB vs ~19 MB warm) is published as the base-memory figure.
  `--no-warmup` reproduces the old behaviour; the report header records which.
- The run fails (non-zero) on any cross-language checksum mismatch — that means
  an implementation diverged, not a flaky run.

## After a run — the publish guide

`results/results.json` + `results/report.md` are regenerated by the harness and committed as
the canonical numbers. Then, in this order:

```sh
python3 bench/chart.py     # 1. the README's overall-speed chart (results/overview.svg)
python3 bench/docs.py      # 2. every derivable number in BENCHMARKS.md + README.md
python3 bench/docs.py --check   # 3. must exit 0 before you commit
```

**Then write the prose by hand — and only the prose.** `docs.py` owns the machine/date/commit
line, the **Overall rating** block, the `latency` percentile table, both `spawn-live` tables,
README's standings table and environment sentence, and all six ordered per-row tables
(times, `Brood rank`, `vs best`). Anything inside a `<!-- BEGIN NAME -->` / `<!-- END NAME -->`
pair is generated: edit it and the next run overwrites you.

**`FRONTIER.md` is hand-written**, and only needs touching when a gap materially moved or
closed. Same for the analysis paragraphs in `BENCHMARKS.md`/`README.md`.

**When you do cite a number in prose, prefer pointing at a table to restating one.** Every
figure typed into a sentence is a figure that is wrong after the next run. This is not
hypothetical: on 2026-08-05 the hand-publish left **six per-row tables, the run date and the
brood commit** describing the previous run while the prose around them described the new one,
and a hand-converted `1613 MB → 1.61 GB` was wrong in four places because this repo's GB is
binary (`kB/1048576`, which is what the generator does).

**Publish at the harness defaults — `python3 bench/harness.py`, no `--runs` flag.**
That is **best of 3** for the ordinary rows, and the defaults already sample the two
error-prone cases harder on their own: `startup` at best of `max(runs, 9)` (its error
propagates into every other row via `compute = wall − startup`) and `spawn`/`pfib`/`http`
at best of 7. Higher `--runs` costs tens of minutes for movement well inside the field's
±10% run-to-run drift. If you do override it, make `BENCHMARKS.md`'s methodology line say
what you actually ran.

**A movement on `spawn-live` is not a result until a fixed-baseline A/B agrees.** That row has
drifted ~20% between whole harness invocations three times; the rule has since rejected two
apparent swings and confirmed one real one (2026-08-05, −16%). Measure it as **CPU time over a
fixed unit count with the two binaries interleaved** — that gives a <2% spread where wall on a
3.3-core row gives 20%.

**A confirmed regression does not imply a culprit commit exists. Check the shape before
bisecting.** (Learned 2026-08-14 on `primes`, ~+6% across 0.3.9 → 0.3.11, reproducible on demand
against a 1.4% floor.) The A/B gate rejects anything under 5% or twice a row's floor, so a change
worth +2–3% passes as noise on its own evidence — correctly. Several of those sum to a real
regression that **no individual gate ever saw and no bisect can localise**, because no single step
crosses the threshold. `git bisect` must return something, so it returns whichever commit sits on
the far side of your cutoff: on `primes` it named a commit touching one `.blsp` *test file*, which
A/Bs against its parent at nothing.

So before spending ~20 minutes of builds on a bisect, **sample three or four points across the
range and look at the curve**. A step means bisect. A ramp (`primes`: 69 → 68 → 70 → 74 ms) means
there is nothing to find, and the tools that fit are a per-commit sweep recording *absolutes for
trend* rather than pass/fail verdicts, or profiling the two ends directly. And always sanity-check
a bisect result against what the commit actually touches — a test-only diff cannot move a runtime
row, and that check is what exposed this.

## Editing benchmark programs

- **Same algorithm, same inputs, same printed checksum** across every column that
  runs it — the harness gates on it. Idiomatic per language, not adversarial;
  the fairness rules live in the README.
- Files are named identically per benchmark (`fib.blsp`/`fib.clj`/`fib.ex`/`fib.c`/…)
  so they diff side by side. A new benchmark needs all seven ports plus a
  `BENCHES` entry in `bench/harness.py` (and a C port if the row is compute and you
  want the floor — use `"all+c"`).
- For Brood idioms read `docs/brood-for-claude.md` before writing `.blsp`.

## Analysis docs

`FRONTIER.md` interprets the data for contributors (what's slow, why, what
would move it); its upstream twin is the brood repo's `docs/compute-frontier.md`.
Historical run data lives in `results/archive/` and git history — don't keep
stale analysis snapshots in `docs/`.
