(defn ack ^long [^long m ^long k]
  (cond
    (zero? m) (inc k)
    (zero? k) (ack (dec m) 1)
    :else     (ack (dec m) (ack m (dec k)))))
(let [n (Long/parseLong (or (System/getenv "BENCH_N") "6"))
      result (atom nil)
      body (fn [] (reset! result (reduce (fn [acc _] (+ acc (ack 3 9))) 0 (range n))))
      t (Thread. nil ^Runnable body "ack" (* 256 1024 1024))]
  (.start t)
  (.join t)
  (println @result))
