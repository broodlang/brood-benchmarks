;; CPU parallelism: 100 x fib(N) across cores via pmap.
(def n (long (Long/parseLong (or (System/getenv "BENCH_N") "31"))))
(def tasks 100)
(defn fib ^long [^long x] (if (< x 2) x (+ (fib (- x 1)) (fib (- x 2)))))
(println (reduce + (pmap (fn [_] (fib n)) (range tasks))))

;; Stop the agent/future thread pool so the JVM exits promptly (else it lingers ~60s).
(shutdown-agents)
