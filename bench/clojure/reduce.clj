;; higher-order fold over a materialised range.
(let [n (long (Long/parseLong (or (System/getenv "BENCH_N") "5000000")))]
  (println (reduce + 0 (range n))))
