// Throw 50 frames deep, catch at the top — panic/recover, Go's non-local exit.
package main

import "fmt"

type benchError struct{ v int }

func descend(d, i int) int {
	if d == 0 {
		panic(benchError{i % 100})
	}
	return 1 + descend(d-1, i)
}

func attempt(i int) (v int) {
	defer func() {
		if e := recover(); e != nil {
			v = e.(benchError).v
		}
	}()
	descend(50, i)
	return 0
}

func main() {
	n := benchN(50000)
	const md = 1000000007
	acc := 0
	for i := 0; i < n; i++ {
		acc += attempt(i)
	}
	fmt.Println(acc % md)
}
