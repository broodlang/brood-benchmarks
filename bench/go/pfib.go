// Parallel fib: compute fib(N) in 100 goroutines at once and sum the results; the
// scheduler spreads them across every core. Checksum = 100 * fib(N).
package main

import "fmt"

func fib(n int) int {
	if n < 2 {
		return n
	}
	return fib(n-1) + fib(n-2)
}

func main() {
	n := benchN(31)
	const tasks = 100
	results := make(chan int, tasks)
	for i := 0; i < tasks; i++ {
		go func() { results <- fib(n) }()
	}
	total := 0
	for i := 0; i < tasks; i++ {
		total += <-results
	}
	fmt.Println(total)
}
