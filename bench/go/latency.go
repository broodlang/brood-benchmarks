// Latency under a fixed arrival rate, open loop. See bench/brood/latency.blsp for the full
// rationale: request i is scheduled at start + i*(1s/rate) whether or not the system keeps up,
// and latency is measured from that scheduled instant, so queueing delay lands in the number.
// Every 20th request OCCUPIES ~500us — defined in time, not work units, and calibrated at
// startup as real allocating work. A handler is a goroutine, the way a connection is served
// in Go; the runtime preempts and spreads them across cores. Checksum covers only the cheap round.
package main

import (
	"fmt"
	"slices"
	"sync"
	"time"
)

const (
	rate  = 20000
	gapNs = int64(1e9 / rate)
	cheap = 40
	fatNs = int64(500000)
)

func work(k int) int64 {
	var acc int64
	for j := 0; j < k; j++ {
		v := []int64{int64(j), int64(j + 1), int64(j + 2), int64(j + 3)}
		acc += v[0] + v[1] + v[2] + v[3]
	}
	return acc
}

var epoch = time.Now()

func nowNs() int64 { return int64(time.Since(epoch)) }

func spinUntil(t int64) {
	for nowNs() < t {
	}
}

func bestWorkNs(reps, k int) int64 {
	var best int64
	for i := 0; i < reps; i++ {
		t := nowNs()
		work(k)
		dt := nowNs() - t
		if best == 0 || dt < best {
			best = dt
		}
	}
	return best
}

// ~500us of real work in THIS runtime, warm-calibrated (best of several samples).
func calibrate() int {
	for i := 0; i < 60; i++ {
		work(5000)
	}
	k := 1000
	for {
		dt := bestWorkNs(9, k)
		if dt >= 200000 {
			return int(int64(k) * fatNs / dt)
		}
		k *= 2
	}
}

func main() {
	n := benchN(50000)
	fatUnits := calibrate()
	fatMeasured := bestWorkNs(5, fatUnits) / 1000

	lats := make([]int64, n) // -1 marks a fat request: its own latency is >=500us by construction
	rs := make([]int64, n)
	var wg sync.WaitGroup
	t0 := nowNs()
	for i := 0; i < n; i++ {
		sched := t0 + int64(i)*gapNs
		spinUntil(sched)
		wg.Add(1)
		go func(i int, sched int64) {
			defer wg.Done()
			r := work(cheap)
			fat := i%20 == 0
			if fat {
				work(fatUnits)
				lats[i] = -1
			} else {
				lats[i] = (nowNs() - sched) / 1000
			}
			rs[i] = r
		}(i, sched)
	}
	wg.Wait()
	elapsed := nowNs() - t0

	var sum int64
	for _, r := range rs {
		sum += r
	}
	ord := make([]int64, 0, n)
	for _, l := range lats {
		if l >= 0 {
			ord = append(ord, l)
		}
	}
	slices.Sort(ord)
	m := len(ord)
	pct := func(p int) int64 { return ord[min(m-1, p*m/100)] }
	fmt.Printf("#metric fat_units=%d\n", fatUnits)
	fmt.Printf("#metric fat_measured_us=%d\n", fatMeasured)
	fmt.Printf("#metric ordinary_n=%d\n", m)
	fmt.Printf("#metric p50_us=%d\n", pct(50))
	fmt.Printf("#metric p99_us=%d\n", pct(99))
	fmt.Printf("#metric p999_us=%d\n", ord[min(m-1, 999*m/1000)])
	fmt.Printf("#metric max_us=%d\n", ord[m-1])
	fmt.Printf("#metric sustained_rps=%d\n", int64(n)*1e9/elapsed)
	fmt.Println(sum)
}
