;; filter -> map -> reduce, fused via a transducer (the Clojure streaming idiom).
(let [n (long (Long/parseLong (or (System/getenv "BENCH_N") "100000")))]
  (println (transduce (comp (filter (fn [i] (or (zero? (rem i 3)) (zero? (rem i 5)))))
                            (map (fn [i] (* i i))))
                      + 0 (range n))))
