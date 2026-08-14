# The C column — what it is, and what it is not

C is here to give the other columns a **machine floor** to be read against. Before this
existed, `.NET` was the `1.00` in every scoreboard table, so every ratio in this repo meant
"vs the fastest managed runtime". Now it can mean "vs roughly what the hardware will do".

It is deliberately a **partial port**: 16 of the 31 rows. Read this file before citing a
C number, because the honest caveats are per-row and some of them are large.

## Build

    gcc -O2 -march=native -std=c11 -Wall -Wextra <row>.c -o build/<row> -lm

One standalone binary per benchmark rather than a dispatcher, so the `startup` row measures
a real C process — exec, loader, one write, exit — instead of a switch inside an
already-running one. `harness.py:build_c()` does this for every `*.c` here and fails the run
on any compile error.

**`-march=native` is deliberate.** Every other runtime in this suite JITs for the host CPU at
runtime (V8, RyuJIT, BeamAsm, Brood's tier-1). Building C for baseline x86-64 would understate
it against columns that do not. The cost is that this column, like every absolute in this repo,
is specific to the machine in the report header.

## The elision audit

The obvious failure mode for a C column is that it measures the compiler rather than the
machine — an optimiser replacing an algorithm with a closed form prints the right checksum
having done none of the work.

**This was tested, and on this toolchain it does not happen.** The structural reason is that
every benchmark prints a checksum derived from its whole computation and the harness gates on
that checksum matching the other six languages; eliminated work cannot produce the checksum.

`loop` — sum 0..n-1, the row most vulnerable to being solved analytically — was checked at the
machine-code level rather than assumed:

| build | wall | reading |
|---|---|---|
| `-O0` | 60 ms | scalar loop with memory traffic |
| `-O2 -march=native` | **8 ms** | ~0.9 cycles/iteration — unrolled scalar adds, a real loop |
| a closed form would be | ~0.4 ms | bare process startup |

The `-O2` asm contains a real loop back-edge, no SIMD, and none of the `imul`/`shr` markers a
closed form leaves. It runs all 30,000,000 iterations.

An earlier version of these files carried an asm barrier to *force* iteration. **It was removed
after measuring**: it prevented no elision (there was none) and cost 50% — 12 ms against 8 ms —
by pinning the accumulator every pass. Handicapping C on a false premise is the same error as
flattering it. **Re-run this check when the compiler is upgraded**, and put the numbers back in
this table.

## Three handicaps found by asking why C was LOSING

The first full run had C behind Brood on `reduce` and `strings`, and behind Node on
`primes`. That is the failure mode worth watching for in this column: a C number that is
wrong in **C's disfavour** is exactly as misleading as one that flatters it, and far less
likely to be challenged, because "C should win" reads as the thing being tested rather
than as a bug. Each turned out to be something this port did to C, not something C does.

| row | cause | cost | fix |
|---|---|---|---|
| `strings` | `sprintf("%ld")` per element re-parses the format string every call; no other column does that — they all call a dedicated int-to-string routine | 17 ms → **7 ms** | write decimal digits directly |
| `primes` | `long` arithmetic meant x86 `idivq`, where the C#/JS ports use 32-bit ints and get `idivl`; trial division is nothing but division | 14 ms → **9 ms** | use `int`, matching the field |
| `reduce` | the reducer was hidden behind a `volatile` pointer to force a real indirect call | 7 ms → **4 ms** | leave it statically known — see below |

`reduce` is the judgement call of the three. Hiding the callback holds C to a stricter
standard than the rest of the field: **Brood specialises a passthrough reducer like `+`
into a native counted loop and resolves it once rather than per element**, and V8 inlines a
monomorphic callback the same way. Forcing C alone to defeat its own inliner would measure a
restriction this harness invented. So the row reports what each language actually does with
a known reducer — Brood, Node and C specialise it away; Python, Ruby and Clojure pay a real
call per element, and that difference is the result. **C's cost with an unspecialisable
callback is 7 ms** (~1.3 ns per indirect call), recorded here so the figure is not lost.

The `volatile` variant was also checked against a plain runtime-selected pointer: both
7 ms, so `volatile` was not itself the cost — the indirect call was.

## Rows C does not run, and why

| row(s) | why not |
|---|---|
| `spawn`, `spawn-live`, `supervisor`, `pfib`, `http`, `pingpong`, `ring`, `latency` | No honest C answer. 300k held-alive units means 300k pthread stacks (~2 GB); a supervisor would be a loop this repo wrote, which measures the harness author. Same judgement `spawn-live` and `supervisor` already make about their own columns. |
| `json`, `regex`, `base64` | C ships none of these. The row would measure whichever third-party library was picked, not the language. |
| `errors`, `errors-deep` | C has no exceptions. `setjmp`/`longjmp` is the nearest idiom but does not unwind, so it is not the same operation the other six perform. Open question, not a settled exclusion. |
| `persistent-map` | Would require hand-writing a HAMT — measuring this repo's HAMT, not C. |
| `pipeline` | **Dropped after measuring.** C's compute came out at ~0.1 ms against a ~0.4 ms process startup, i.e. essentially all noise. Because ratios on a row are computed against its fastest column, a noise-dominated C denominator would have corrupted *every other language's* ratio on that row. It is also the row where C does least comparable work — the other columns exercise lazy-seq/transducer composition, and idiomatic C is one loop with an `if`. |

## Per-row caveats that materially affect the number

- **`wordcount`** — the keys are dense in 0..999, so the fastest idiomatic C is a flat
  `long[1000]`, which is an array index and no hash map at all. That would report C as
  infinitely fast at a structure it never built, so this uses a hand-written open-addressing
  table instead. Consequence: it is simpler than the production hash maps the other runtimes
  ship, so it is fast partly because it does less. Read it as "a straightforward C hash table",
  not "the C hash map".
- **`bintree`** — C mallocs and frees each node, which is the fair analogue of
  allocate-and-collect. It deliberately does *not* bump-allocate from an arena and drop it in
  one call, which is what a C programmer optimising this would really write and would be
  several times faster. A different program from the one the other six run.
- **`nqueens`** — C pushes onto a stack array (O(1)), matching Brood's O(1) `cons`. Node's
  spread and .NET's `new List(...)` are O(n) copies, so C's margin over *those two* partly
  reflects an asymmetry that already exists between the current columns.
- **`sort`** — `qsort` takes its comparator as a function pointer and calls it indirectly per
  comparison, so C does not get the inlined-comparator advantage `std::sort` would give it.
  That is a real property of the C standard library, not a handicap applied here.
- **`reduce`** — the reducer is statically known and GCC inlines it; see the handicap table
  above for why that is the fair choice and what the unspecialised figure is.
- **`bintree` loses to Elixir, and that is a real result** — C mallocs and frees ~819k nodes
  where the BEAM bump-allocates and collects in bulk. It was checked for the same class of
  self-inflicted problem as the three above and is not one: it is GC beating malloc/free on
  an allocation-heavy workload, which is the row doing its job.
- **`matmul`** — row-of-pointers (`int **`), matching the jagged arrays the other ports use,
  not a flat contiguous block. A flat block would let C vectorise the inner product in a way
  none of the other columns can.
