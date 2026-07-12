// A ring of N async nodes; a token travels around +1/hop for LAPS laps
// (N*LAPS hops). Node's single-threaded event loop is its concurrency model.
// Checksum = N*LAPS.
const N = parseInt(process.env.BENCH_N || "200", 10);
const LAPS = 5000;
const total = N * LAPS;

class Chan {
  constructor() { this.q = []; this.w = []; }
  send(v) { const r = this.w.shift(); if (r) r(v); else this.q.push(v); }
  recv() { return new Promise((res) => { if (this.q.length) res(this.q.shift()); else this.w.push(res); }); }
}

const chans = Array.from({ length: N }, () => new Chan());
let resolveDone;
const donePromise = new Promise((r) => (resolveDone = r));
for (let i = 0; i < N; i++) {
  const inbox = chans[i], next = chans[(i + 1) % N];
  (async () => {
    while (true) {
      const v = await inbox.recv();
      if (v >= total) { resolveDone(v); break; }
      next.send(v + 1);
    }
  })();
}
chans[0].send(0);
donePromise.then((v) => console.log(v));
