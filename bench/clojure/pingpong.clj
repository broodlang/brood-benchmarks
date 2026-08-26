;; Two threads bounce a token N round trips via blocking queues. Checksum = N.
(import '[java.util.concurrent LinkedBlockingQueue])
(let [n (long (Long/parseLong (or (System/getenv "BENCH_N") "100000")))
      q-to (LinkedBlockingQueue.)
      q-from (LinkedBlockingQueue.)
      worker (Thread. (fn [] (loop [] (let [m (.take q-to)] (when (>= (long m) 0) (.put q-from m) (recur))))))]
  (.start worker)
  (loop [k 0]
    (if (< k n)
      (do (.put q-to k) (.take q-from) (recur (inc k)))
      (do (.put q-to -1) (.join worker) (println k)))))
