(let [n (Long/parseLong (or (System/getenv "BENCH_N") "175"))
      md 1000000007
      a (object-array (for [i (range n)] (long-array (for [j (range n)] (rem (+ i j) 100)))))
      b (object-array (for [i (range n)] (long-array (for [j (range n)] (rem (* i j) 100)))))]
  (loop [i 0 total 0]
    (if (< i n)
      (let [ai ^longs (aget ^objects a i)]
        (recur (inc i)
          (loop [j 0 total total]
            (if (< j n)
              (recur (inc j)
                (+ total
                   (loop [k 0 s 0]
                     (if (< k n)
                       (recur (inc k) (+ s (* (aget ai k) (aget ^longs (aget ^objects b k) j))))
                       s))))
              total))))
      (println (rem total md)))))
