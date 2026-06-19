(defn steps [m]
  (loop [m m s 0]
    (cond (= m 1) s
          (even? m) (recur (quot m 2) (inc s))
          :else (recur (+ (* 3 m) 1) (inc s)))))
(let [n (Long/parseLong (or (System/getenv "BENCH_N") "250000"))]
  (println (loop [k 1 best 0]
             (if (< k n) (recur (inc k) (max best (steps k))) best))))
