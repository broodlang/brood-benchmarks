package main

import "fmt"

func main() {
	n := benchN(540)
	const maxIter = 100
	total := 0
	for py := 0; py < n; py++ {
		y0 := (float64(py)/float64(n))*3.0 - 1.5
		for px := 0; px < n; px++ {
			x0 := (float64(px)/float64(n))*3.0 - 2.0
			x, y, xx, yy := 0.0, 0.0, 0.0, 0.0
			i := 0
			for xx+yy <= 4.0 && i < maxIter {
				y = 2.0*x*y + y0 // uses old x, old y
				x = xx - yy + x0 // uses old xx, yy
				xx = x * x
				yy = y * y
				i++
			}
			total += i
		}
	}
	fmt.Println(total)
}
