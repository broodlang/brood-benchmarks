package main

import "fmt"

func main() {
	n := benchN(30000000)
	acc := 0
	for i := 0; i < n; i++ {
		acc += i
	}
	fmt.Println(acc)
}
