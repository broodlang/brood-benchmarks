// JSON encode+parse round-trip with the standard library's encoding/json.
package main

import (
	"encoding/json"
	"fmt"
)

type item struct {
	ID   int    `json:"id"`
	V    int    `json:"v"`
	Name string `json:"name"`
	OK   bool   `json:"ok"`
}

func main() {
	n := benchN(2000)
	x := 123456789
	arr := make([]item, 0, n)
	for i := 0; i < n; i++ {
		x = (x*1103515245 + 12345) & 0x7FFFFFFF
		arr = append(arr, item{i, x, "item", x%2 == 0})
	}
	enc, err := json.Marshal(arr)
	if err != nil {
		panic(err)
	}
	var parsed []item
	if err := json.Unmarshal(enc, &parsed); err != nil {
		panic(err)
	}
	acc := 0
	for _, o := range parsed {
		acc = (acc + o.V) % 2147483647
	}
	fmt.Println(acc)
}
