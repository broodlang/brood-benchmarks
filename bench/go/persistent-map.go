// Read-modify-write churn on a map over a large key space (50k keys).
// Checksum = sum of key*value over the map.
package main

import "fmt"

func main() {
	n := benchN(300000)
	const m = 50000
	x := 123456789
	acc := make(map[int]int)
	for i := 0; i < n; i++ {
		x = (x*1103515245 + 12345) & 0x7FFFFFFF
		key := x % m
		acc[key] += 1 + key%7
	}
	total := 0
	for k, v := range acc {
		total += k * v
	}
	fmt.Println(total)
}
