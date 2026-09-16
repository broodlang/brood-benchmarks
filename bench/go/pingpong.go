// Two goroutines bounce a token N round trips over a pair of unbuffered channels.
// Checksum = N.
package main

import "fmt"

func main() {
	n := benchN(100000)
	ping := make(chan int)
	pong := make(chan int)
	go func() {
		for v := range ping {
			pong <- v
		}
	}()
	k := 0
	for k < n {
		ping <- k
		k = <-pong + 1
	}
	close(ping)
	fmt.Println(k)
}
