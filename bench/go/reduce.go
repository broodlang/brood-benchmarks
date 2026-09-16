// Higher-order fold over a range: a function VALUE applied per element (the row is
// deliberately distinct from `loop`, the hand-written form). The reducer is left
// statically known, as in the C port — the compiler is free to inline it, which is what
// every other runtime here does with a known reducer too.
package main

import "fmt"

func fold(f func(int, int) int, init, n int) int {
	acc := init
	for i := 0; i < n; i++ {
		acc = f(acc, i)
	}
	return acc
}

func main() {
	fmt.Println(fold(func(a, b int) int { return a + b }, 0, benchN(5000000)))
}
