package main

import "fmt"

func main() {
	n := benchN(175)
	const mod = 1000000007
	a := make([][]int, n)
	b := make([][]int, n)
	for i := 0; i < n; i++ {
		a[i] = make([]int, n)
		b[i] = make([]int, n)
		for j := 0; j < n; j++ {
			a[i][j] = (i + j) % 100
			b[i][j] = (i * j) % 100
		}
	}
	total := 0
	for i := 0; i < n; i++ {
		ai := a[i]
		for j := 0; j < n; j++ {
			s := 0
			for k := 0; k < n; k++ {
				s += ai[k] * b[k][j]
			}
			total += s
		}
	}
	fmt.Println(total % mod)
}
