// Concurrent HTTP: fire N GETs at a local server (each sleeps ~20ms server-side) and
// count the 200s. One goroutine per request, all in flight at once; a transport with
// no per-host connection cap so nothing queues. Checksum = N.
package main

import (
	"fmt"
	"io"
	"net/http"
	"os"
	"sync"
	"sync/atomic"
)

func main() {
	n := benchN(500)
	port := os.Getenv("BENCH_HTTP_PORT")
	if port == "" {
		port = "8089"
	}
	url := "http://127.0.0.1:" + port + "/"
	client := &http.Client{Transport: &http.Transport{MaxConnsPerHost: 0, MaxIdleConnsPerHost: n, DisableKeepAlives: true}}
	var ok atomic.Int64
	var wg sync.WaitGroup
	for i := 0; i < n; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			resp, err := client.Get(url)
			if err != nil {
				return
			}
			io.Copy(io.Discard, resp.Body) // drain the body so the socket can close
			resp.Body.Close()
			if resp.StatusCode == 200 {
				ok.Add(1)
			}
		}()
	}
	wg.Wait()
	fmt.Println(ok.Load())
}
