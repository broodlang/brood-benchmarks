(defn fib ^long [^long n] (if (< n 2) n (+ (fib (- n 1)) (fib (- n 2)))))
(println (fib (long (Long/parseLong (or (System/getenv "BENCH_N") "35")))))
