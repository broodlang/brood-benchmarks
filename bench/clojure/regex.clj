;; Generate N decimal strings; count full matches of [0-9]+ (re-matches is
;; anchored). Checksum = count.
(let [n (long (Long/parseLong (or (System/getenv "BENCH_N") "20000")))
      re #"[0-9]+"]
  (loop [i 0 x 123456789 count 0]
    (if (< i n)
      (let [x (bit-and (+ (* x 1103515245) 12345) 0x7FFFFFFF)
            s0 (str x)
            s (if (even? x) (str s0 "x") s0)]
        (recur (inc i) x (if (re-matches re s) (inc count) count)))
      (println count))))
