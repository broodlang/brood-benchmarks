(def n (long (Long/parseLong (or (System/getenv "BENCH_N") "10"))))
(defn safe? [^long c placed ^long d]
  (loop [placed placed d d]
    (if (empty? placed)
      true
      (let [p (first placed)]
        (if (or (= p c) (= (- p c) d) (= (- p c) (- d)))
          false
          (recur (rest placed) (inc d)))))))
(defn solve ^long [^long row placed]
  (if (= row n)
    1
    (reduce (fn [total c] (if (safe? c placed 1) (+ total (solve (inc row) (cons c placed))) total))
            0 (range n))))
(println (solve 0 nil))
