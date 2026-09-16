// A ring of N goroutines; a token travels around +1/hop for LAPS laps (N*LAPS hops).
// Checksum = N*LAPS.
package main

import "fmt"

func main() {
	n := benchN(200)
	const laps = 5000
	total := n * laps
	chans := make([]chan int, n)
	for i := range chans {
		chans[i] = make(chan int, 1)
	}
	done := make(chan int)
	for i := 0; i < n; i++ {
		inbox, next := chans[i], chans[(i+1)%n]
		go func() {
			for v := range inbox {
				if v >= total {
					done <- v
					return
				}
				next <- v + 1
			}
		}()
	}
	chans[0] <- 0
	fmt.Println(<-done)
}
