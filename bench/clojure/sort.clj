(let [n (Long/parseLong (or (System/getenv "BENCH_N") "375000"))
      md 1000000007
      data (loop [i 0 x 123456789 acc (transient [])]
             (if (< i n)
               (let [x (bit-and (+ (* x 1103515245) 12345) 0x7FFFFFFF)]
                 (recur (inc i) x (conj! acc x)))
               (persistent! acc)))]
  (println (reduce (fn [h v] (rem (+ (* h 31) v) md)) 0 (sort data))))
