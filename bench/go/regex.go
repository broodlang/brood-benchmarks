// Regex full-match count with the standard library's regexp (RE2).
package main

import (
	"fmt"
	"regexp"
	"strconv"
)

func main() {
	n := benchN(20000)
	re := regexp.MustCompile(`^[0-9]+$`)
	x, count := 123456789, 0
	for i := 0; i < n; i++ {
		x = (x*1103515245 + 12345) & 0x7FFFFFFF
		s := strconv.Itoa(x)
		if x%2 == 0 {
			s += "x"
		}
		if re.MatchString(s) {
			count++
		}
	}
	fmt.Println(count)
}
