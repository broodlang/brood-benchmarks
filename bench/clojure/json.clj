;; Build N records, write-str then read-str (clojure.data.json), checksum sum "v".
(require '[clojure.data.json :as json])
(let [n (long (Long/parseLong (or (System/getenv "BENCH_N") "2000")))]
  (loop [i 0 x 123456789 acc (transient [])]
    (if (< i n)
      (let [x (bit-and (+ (* x 1103515245) 12345) 0x7FFFFFFF)]
        (recur (inc i) x (conj! acc {"id" i "v" x "name" "item" "ok" (even? x)})))
      (let [parsed (json/read-str (json/write-str (persistent! acc)))]
        (println (reduce (fn [a o] (rem (+ a (get o "v")) 2147483647)) 0 parsed))))))
