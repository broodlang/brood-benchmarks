// Hold N units alive, then hand each a message it must COPY, and collect each result
// through a channel the parent drains one at a time — mirroring a mailbox.
//
// A goroutine is the closest thing outside BEAM/Brood to a lightweight process — its own
// growable stack, preemptively scheduled across cores — but it is NOT an isolated process:
// one shared heap, no mailbox, and a channel send passes a reference. So the payload is
// copied explicitly on the way in, as `send` would, and the reply travels as a message.
// Checksum = N * (sum(payload) + 1).
package main

import "fmt"

func main() {
	n := benchN(300000)
	payload := make([]int, 16)
	for i := range payload {
		payload[i] = i
	}
	wake := make([]chan []int, n)
	box := make(chan int, 1024)
	for i := 0; i < n; i++ {
		ch := make(chan []int, 1)
		wake[i] = ch
		go func() {
			p := <-ch
			s := 0
			for _, v := range p {
				s += v
			}
			box <- s + 1 // reply as a message, not a return value
		}()
	}
	for i := 0; i < n; i++ {
		wake[i] <- append([]int(nil), payload...) // copy, as `send` would
	}
	total := 0
	for i := 0; i < n; i++ {
		total += <-box
	}
	fmt.Println(total)
}
