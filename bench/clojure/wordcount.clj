;; immutable persistent-map build (the Clojure analog of Brood/Elixir).
(let [n (long (Long/parseLong (or (System/getenv "BENCH_N") "750000"))) k 1000]
  (loop [i 0 x 123456789 counts {}]
    (if (< i n)
      (let [x (bit-and (+ (* x 1103515245) 12345) 0x7FFFFFFF)]
        (recur (inc i) x (update counts (rem x k) (fnil inc 0))))
      (println (reduce-kv (fn [acc kk vv] (+ acc (* kk vv))) 0 counts)))))
