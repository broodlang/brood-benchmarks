(require 'clojure.string)
(let [n (long (Long/parseLong (or (System/getenv "BENCH_N") "500000")))]
  (println (count (clojure.string/join "," (range n)))))
