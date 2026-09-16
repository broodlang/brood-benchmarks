// LCG token stream tallied into a map — the plain read-modify-write, `counts[key]++`.
package main

import "fmt"

func main() {
	n := benchN(750000)
	const k = 1000
	x := 123456789
	counts := make(map[int]int)
	for i := 0; i < n; i++ {
		x = (x*1103515245 + 12345) & 0x7FFFFFFF
		counts[x%k]++
	}
	total := 0
	for key, v := range counts {
		total += key * v
	}
	fmt.Println(total)
}
