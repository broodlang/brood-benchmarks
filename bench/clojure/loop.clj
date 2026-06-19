;; raw iteration: tail loop with an accumulator (recur = TCO).
(let [n (Long/parseLong (or (System/getenv "BENCH_N") "30000000"))]
  (loop [i 0 acc 0]
    (if (< i n) (recur (inc i) (+ acc i)) (println acc))))
