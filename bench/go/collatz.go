package main

import "fmt"

func main() {
	n := benchN(250000)
	best := 0
	for start := 1; start < n; start++ {
		k, steps := start, 0
		for k != 1 {
			if k%2 == 0 {
				k /= 2
			} else {
				k = 3*k + 1
			}
			steps++
		}
		if steps > best {
			best = steps
		}
	}
	fmt.Println(best)
}
