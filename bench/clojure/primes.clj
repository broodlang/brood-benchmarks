(defn prime? [^long n]
  (if (< n 2)
    false
    (loop [d 2]
      (cond (> (* d d) n) true
            (zero? (rem n d)) false
            :else (recur (inc d))))))
(let [n (long (Long/parseLong (or (System/getenv "BENCH_N") "150000")))]
  (println (count (filter prime? (range 2 n)))))
