;; Read-modify-write churn on a persistent map over a 50k key space.
;; Checksum = sum of key*value over the map.
(let [n (Long/parseLong (or (System/getenv "BENCH_N") "300000")) m 50000]
  (loop [i 0 x 123456789 acc {}]
    (if (< i n)
      (let [x (bit-and (+ (* x 1103515245) 12345) 0x7FFFFFFF)
            key (rem x m)
            acc (update acc key (fnil + 0) (+ 1 (rem key 7)))]
        (recur (inc i) x acc))
      (println (reduce-kv (fn [a k v] (+ a (* k v))) 0 acc)))))
