package main

import "fmt"

type node struct{ l, r *node }

func mk(d int) *node {
	if d == 0 {
		return nil
	}
	return &node{mk(d - 1), mk(d - 1)}
}

func check(t *node) int {
	if t == nil {
		return 1
	}
	return 1 + check(t.l) + check(t.r)
}

func main() {
	n := benchN(200) // repetitions
	const depth = 12
	total := 0
	for i := 0; i < n; i++ {
		total += check(mk(depth))
	}
	fmt.Println(total)
}
