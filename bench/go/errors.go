// Raise + recover a value N times. Go's error idiom is a returned value, but the row
// measures the non-local exit every other port makes — so this uses panic/recover,
// which is Go's equivalent of throw/catch (an error value would measure nothing).
package main

import "fmt"

type benchError struct{ v int }

func raise(i int) {
	panic(benchError{i % 100})
}

func attempt(i int) (v int) {
	defer func() {
		if e := recover(); e != nil {
			v = e.(benchError).v
		}
	}()
	raise(i)
	return 0
}

func main() {
	n := benchN(200000)
	const md = 1000000007
	acc := 0
	for i := 0; i < n; i++ {
		acc += attempt(i)
	}
	fmt.Println(acc % md)
}
