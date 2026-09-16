// Fan out N goroutines; each computes fib(15) and sends the result back on a channel.
// Checksum = N * fib(15) = N * 610.
package main

import "fmt"

func fib(n int) int {
	if n < 2 {
		return n
	}
	return fib(n-1) + fib(n-2)
}

func main() {
	n := benchN(10000)
	results := make(chan int, n)
	for i := 0; i < n; i++ {
		go func() { results <- fib(15) }()
	}
	total := 0
	for i := 0; i < n; i++ {
		total += <-results
	}
	fmt.Println(total)
}
