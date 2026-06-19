;; fan out N concurrent units, each computing fib(15); sum the results.
;; Clojure's idiomatic lightweight concurrency = futures (JVM thread pool).
(def n (Long/parseLong (or (System/getenv "BENCH_N") "5000")))
(defn fib [x] (if (< x 2) x (+ (fib (- x 1)) (fib (- x 2)))))
(println (reduce + (map deref (doall (map (fn [_] (future (fib 15))) (range n))))))

;; Stop the agent/future thread pool so the JVM exits promptly (else it lingers ~60s).
(shutdown-agents)
