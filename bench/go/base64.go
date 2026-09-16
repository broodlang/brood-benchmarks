// base64 encode+decode with the standard library's encoding/base64.
package main

import (
	"encoding/base64"
	"fmt"
)

func main() {
	n := benchN(50000)
	x := 123456789
	bytes := make([]byte, n)
	for i := 0; i < n; i++ {
		x = (x*1103515245 + 12345) & 0x7FFFFFFF
		bytes[i] = byte(x % 256)
	}
	enc := base64.StdEncoding.EncodeToString(bytes)
	dec, err := base64.StdEncoding.DecodeString(enc)
	if err != nil {
		panic(err)
	}
	encSum := 0
	for i := 0; i < len(enc); i++ {
		encSum = (encSum + int(enc[i])) % 2147483647
	}
	decSum := 0
	for _, b := range dec {
		decSum = (decSum + int(b)) % 2147483647
	}
	fmt.Println((encSum + decSum) % 2147483647)
}
