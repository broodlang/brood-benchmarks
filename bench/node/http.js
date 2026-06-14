// Concurrent HTTP: fire N GETs at a local server (each sleeps ~20ms server-side)
// and count the 200s. This is the event loop's home turf — all N requests are
// issued up front and complete as their responses arrive, no threads involved.
// `agent: false` gives each request its own socket so nothing queues. Checksum = N.
const http = require("http");

const N = parseInt(process.env.BENCH_N || "500", 10);
const PORT = parseInt(process.env.BENCH_HTTP_PORT || "8089", 10);
let done = 0;
let ok = 0;

function finish() {
  if (++done === N) console.log(ok);
}

for (let i = 0; i < N; i++) {
  const req = http.get(
    { host: "127.0.0.1", port: PORT, path: "/", agent: false },
    (res) => {
      if (res.statusCode === 200) ok++;
      res.resume(); // drain the body so the socket can close
      res.on("end", finish);
    }
  );
  req.on("error", finish);
}
