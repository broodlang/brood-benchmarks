(let [n (Long/parseLong (or (System/getenv "BENCH_N") "200000")) md 1000000007]
  (println (rem (loop [i 0 acc 0]
                  (if (< i n)
                    (recur (inc i)
                           (+ acc (try (throw (ex-info "" {:v (rem i 100)}))
                                       (catch clojure.lang.ExceptionInfo e (:v (ex-data e))))))
                    acc))
                md)))
