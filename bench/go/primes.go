package main

import (
	"fmt"
	"math"
)

func isPrime(n int) bool {
	if n < 2 {
		return false
	}
	limit := int(math.Sqrt(float64(n))) // once — no d*d in the loop
	for d := 2; d <= limit; d++ {
		if n%d == 0 {
			return false
		}
	}
	return true
}

func main() {
	n := benchN(150000)
	count := 0
	for k := 2; k < n; k++ {
		if isPrime(k) {
			count++
		}
	}
	fmt.Println(count)
}
