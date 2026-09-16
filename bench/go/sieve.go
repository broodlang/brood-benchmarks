// Sieve of Eratosthenes to N, counting primes. Checksum = count of primes <= N.
package main

import "fmt"

func main() {
	n := benchN(1000000)
	comp := make([]bool, n+1)
	for p := 2; p*p <= n; p++ {
		if !comp[p] {
			for j := p * p; j <= n; j += p {
				comp[j] = true
			}
		}
	}
	count := 0
	for k := 2; k <= n; k++ {
		if !comp[k] {
			count++
		}
	}
	fmt.Println(count)
}
