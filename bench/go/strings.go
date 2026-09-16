package main

import (
	"fmt"
	"strconv"
	"strings"
)

func main() {
	n := benchN(500000)
	parts := make([]string, n)
	for i := 0; i < n; i++ {
		parts[i] = strconv.Itoa(i)
	}
	s := strings.Join(parts, ",")
	fmt.Println(len(s))
}
