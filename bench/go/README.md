# The Go column

Go is a **full column**: every `all` row, plus `spawn-live` and `latency`. It is the point of
comparison the field was missing between C (no runtime) and .NET (a JIT): compiled ahead of
time, garbage collected, with a scheduler of its own — goroutines are the closest thing outside
BEAM and Brood to a lightweight process, and the row notes below say where that comparison
holds and where it does not.

## Build

    go build -o build/<row> bench.go <row>.go

One static binary per row, the way the C column is built, so the `startup` row measures a real
Go process — runtime init, one write, exit — rather than a switch inside a running one.
`harness.py:build_go()` does this for every `*.go` here and fails the run on any compile error.
Every row is its own `package main` in this one directory (so the files diff side by side with
the other columns); `bench.go` is the shared `benchN` helper each is compiled with, and the
explicit two-file build is how Go compiles one `main` out of a directory holding thirty.

Default `GOAMD64` (v1), no build tags, no `-gcflags`: the toolchain as installed. Unlike the C
column there is no `-march=native` — Go does not target the host CPU by default, and the column
reports what `go build` gives.

## What is idiomatic here, and the judgement calls

- **`errors` / `errors-deep` use `panic`/`recover`.** Go's error idiom is a returned value, but
  the row measures the non-local exit every other port makes (a throw fifty frames deep, caught
  at the top); a returned `error` would measure nothing. `panic`/`recover` is Go's throw/catch.
- **`pipeline` is a chain of `iter.Seq` stages** (range-over-func, Go 1.23): a function value per
  stage, which is what the row measures in every other language. A hand-fused `for` loop would
  be the `loop` row again.
- **`reduce` leaves the reducer statically known**, as the C port does and for the same reason
  (`bench/c/README.md`): every runtime here specialises a known reducer, and hiding it behind an
  interface would hold Go alone to a standard the field is not held to.
- **`wordcount` / `persistent-map` are `m[k] += v` on a built-in map** — the plain in-place
  read-modify-write, against Brood's immutable map (which the compiler builds in place when the
  fold is provably linear, brood ADR-360).
- **`spawn`, `pfib`, `pingpong`, `ring` are goroutines and channels.** A goroutine is not an
  isolated process — one shared heap, no mailbox, a channel send passes a reference — so
  `spawn-live` copies its payload explicitly on the way in, as `send` would, and replies through
  a channel drained one message at a time. It sits in the coroutine table with Node, .NET and
  Python for that reason, and the `cores`/`CPU·s` columns show what it spends.
- **`latency` starts a goroutine per request**, the way `net/http` serves a connection. Go
  preempts a goroutine that has run for 10 ms, not one that has run for 500 µs, so a fat
  handler holds its P for its whole occupancy; what that does to the requests queued behind it
  is the row's question, and the answer is in the percentiles rather than adjusted for here.
- **`http`** is `net/http` with one goroutine per request and keep-alives off, so every request
  has its own socket and nothing queues behind a connection cap — the same shape as the Node
  port's `agent: false`.
- **Codecs** (`json`, `regex`, `base64`) are the standard library: `encoding/json` reflecting
  over a struct, `regexp` (RE2 — linear time, no backtracking), `encoding/base64`.

## What to watch for

The same thing the C column warns about: a Go number that is **too slow** is a bug report
about this directory, not a finding. The first build of this column was checked row by row
against Brood's checksums (`bench/smoke.py --langs all` does it across the whole field), but
a row that runs correctly and slowly is invisible to that gate.
