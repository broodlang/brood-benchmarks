(def depth 50)
(defn descend ^long [^long d ^long i]
  (if (= d 0)
    (throw (ex-info "" {:v (rem i 100)}))
    (+ 1 (descend (- d 1) i))))
(let [n (long (Long/parseLong (or (System/getenv "BENCH_N") "50000"))) md 1000000007]
  (println (rem (loop [i 0 acc 0]
                  (if (< i n)
                    (recur (inc i)
                           (+ acc (try (descend depth i)
                                       (catch clojure.lang.ExceptionInfo e (:v (ex-data e))))))
                    acc))
                md)))
