// filter/map/reduce over a range, as a chain of iterators (Go 1.23 range-over-func) —
// the closest Go has to a combinator pipeline, with a function value per stage.
package main

import (
	"fmt"
	"iter"
)

func rangeN(n int) iter.Seq[int] {
	return func(yield func(int) bool) {
		for i := 0; i < n; i++ {
			if !yield(i) {
				return
			}
		}
	}
}

func filter(s iter.Seq[int], p func(int) bool) iter.Seq[int] {
	return func(yield func(int) bool) {
		for v := range s {
			if p(v) && !yield(v) {
				return
			}
		}
	}
}

func mapSeq(s iter.Seq[int], f func(int) int) iter.Seq[int] {
	return func(yield func(int) bool) {
		for v := range s {
			if !yield(f(v)) {
				return
			}
		}
	}
}

func reduce(s iter.Seq[int], init int, f func(int, int) int) int {
	acc := init
	for v := range s {
		acc = f(acc, v)
	}
	return acc
}

func main() {
	n := benchN(100000)
	total := reduce(
		mapSeq(
			filter(rangeN(n), func(i int) bool { return i%3 == 0 || i%5 == 0 }),
			func(i int) int { return i * i }),
		0, func(a, b int) int { return a + b })
	fmt.Println(total)
}
