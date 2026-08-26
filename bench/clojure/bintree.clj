(def depth 12)
(defn make [^long d] (if (= d 0) nil [(make (- d 1)) (make (- d 1))]))
(defn check ^long [node] (if (nil? node) 1 (+ 1 (check (nth node 0)) (check (nth node 1)))))
(let [n (long (Long/parseLong (or (System/getenv "BENCH_N") "200")))]
  (println (loop [i 0 acc 0]
             (if (< i n) (recur (inc i) (+ acc (check (make depth)))) acc))))
