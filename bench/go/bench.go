// bench.go — the one helper every Go row shares: the workload size.
//
// Each row is its own `package main` file built to its own binary
// (`go build -o build/<row> bench.go <row>.go`), so the `startup` row measures a real Go
// process — runtime init, a write, exit — the way the C and .NET columns do, and each
// file diffs side by side with its siblings in the other languages.
package main

import (
	"os"
	"strconv"
)

// benchN is BENCH_N if set, else the same default every other port bakes in.
func benchN(fallback int) int {
	if e := os.Getenv("BENCH_N"); e != "" {
		if v, err := strconv.Atoi(e); err == nil {
			return v
		}
	}
	return fallback
}
