;; Sieve of Eratosthenes to N. Uses a Java boolean-array (idiomatic Clojure for
;; a mutable primitive array). Checksum = count of primes <= N.
(let [n (Long/parseLong (or (System/getenv "BENCH_N") "1000000"))
      comp (boolean-array (inc n))]
  (loop [p 2]
    (when (<= (* p p) n)
      (when-not (aget comp p)
        (loop [j (* p p)] (when (<= j n) (aset comp j true) (recur (+ j p)))))
      (recur (inc p))))
  (println (loop [k 2 acc 0]
             (if (> k n) acc (recur (inc k) (if (aget comp k) acc (inc acc)))))))
