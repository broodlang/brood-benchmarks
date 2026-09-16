package main

import (
	"fmt"
	"slices"
)

func main() {
	n := benchN(375000)
	const mod = 1000000007
	x := 123456789
	data := make([]int, n)
	for i := 0; i < n; i++ {
		x = (x*1103515245 + 12345) & 0x7FFFFFFF
		data[i] = x
	}
	slices.Sort(data)
	h := 0
	for _, v := range data {
		h = (h*31 + v) % mod
	}
	fmt.Println(h)
}
