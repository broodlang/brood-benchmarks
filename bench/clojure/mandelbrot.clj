(let [n (long (Long/parseLong (or (System/getenv "BENCH_N") "540"))) maxiter 100]
  (println
    (loop [py 0 total 0]
      (if (< py n)
        (let [y0 (- (* (/ (double py) n) 3.0) 1.5)]
          (recur (inc py)
            (loop [px 0 total total]
              (if (< px n)
                (let [x0 (- (* (/ (double px) n) 3.0) 2.0)]
                  (recur (inc px)
                    (loop [x 0.0 y 0.0 xx 0.0 yy 0.0 i 0]
                      (if (and (<= (+ xx yy) 4.0) (< i maxiter))
                        (let [ny (+ (* 2.0 x y) y0) nx (+ (- xx yy) x0)]
                          (recur nx ny (* nx nx) (* ny ny) (inc i)))
                        (+ total i)))))
                total))))
        total))))
