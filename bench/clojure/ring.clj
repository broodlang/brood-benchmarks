;; A ring of N daemon threads; a token travels around +1/hop for LAPS laps
;; (N*LAPS hops). Checksum = N*LAPS.
(import '[java.util.concurrent LinkedBlockingQueue])
(let [n (long (Long/parseLong (or (System/getenv "BENCH_N") "200")))
      laps 5000
      total (* n laps)
      inboxes (vec (repeatedly n #(LinkedBlockingQueue.)))
      done (LinkedBlockingQueue.)]
  (dotimes [i n]
    (let [^LinkedBlockingQueue inbox (nth inboxes i)
          ^LinkedBlockingQueue nxt (nth inboxes (mod (inc i) n))]
      (doto (Thread. (fn []
                       (loop []
                         (let [v (long (.take inbox))]
                           (if (>= v total)
                             (.put done v)
                             (do (.put nxt (+ v 1)) (recur)))))))
        (.setDaemon true)
        (.start))))
  (.put ^LinkedBlockingQueue (nth inboxes 0) 0)
  (println (.take done)))
