#!/usr/bin/env python3
"""Tiny concurrent HTTP server for the `http` benchmark.

Every request sleeps a fixed time, then returns a 2-byte "ok". The fixed sleep
is the whole point: it turns each request into a known, identical unit of
*waiting*, so the benchmark measures how well a client OVERLAPS in-flight
requests (its I/O-concurrency model) rather than network speed or server compute.
A client that fires all N requests concurrently finishes in ~SLEEP; one that
serialises them takes ~N*SLEEP.

Threaded so the server itself is never the bottleneck — it can hold thousands of
sleeping requests at once. Usage: `python3 httpserver.py [PORT]`.
"""
import sys
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

SLEEP_MS = 20
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8089


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def do_GET(self):
        time.sleep(SLEEP_MS / 1000.0)
        body = b"ok"
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):  # silence per-request logging
        pass


class Server(ThreadingHTTPServer):
    daemon_threads = True
    request_queue_size = 1024  # large listen backlog for bursts of N connections


if __name__ == "__main__":
    Server(("127.0.0.1", PORT), Handler).serve_forever()
