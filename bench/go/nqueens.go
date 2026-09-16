package main

import "fmt"

var n = benchN(10)

func safe(c int, placed []int) bool {
	d := 1
	for _, p := range placed {
		if p == c || p-c == d || p-c == -d {
			return false
		}
		d++
	}
	return true
}

func solve(row int, placed []int) int {
	if row == n {
		return 1
	}
	total := 0
	for c := 0; c < n; c++ {
		if safe(c, placed) {
			// a fresh list with c in front, as every other port builds
			next := make([]int, 0, len(placed)+1)
			next = append(next, c)
			next = append(next, placed...)
			total += solve(row+1, next)
		}
	}
	return total
}

func main() {
	fmt.Println(solve(0, nil))
}
