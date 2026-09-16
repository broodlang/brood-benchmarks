// Ackermann ack(3,9) summed N times. Deep double-recursion (depth ~4093).
// Checksum = N * ack(3,9) = N * 4093.
package main

import "fmt"

func ack(m, k int) int {
	if m == 0 {
		return k + 1
	}
	if k == 0 {
		return ack(m-1, 1)
	}
	return ack(m-1, ack(m, k-1))
}

func main() {
	n := benchN(6)
	total := 0
	for i := 0; i < n; i++ {
		total += ack(3, 9)
	}
	fmt.Println(total)
}
