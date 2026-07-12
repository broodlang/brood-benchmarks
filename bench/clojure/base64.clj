;; Generate N bytes, base64 encode+decode (java.util.Base64). Checksum =
;; (sum enc char codes + sum decoded bytes) mod 2^31.
(import '[java.util Base64])
(let [n (Long/parseLong (or (System/getenv "BENCH_N") "50000"))
      ^bytes ba (byte-array n)]
  (loop [i 0 x 123456789]
    (when (< i n)
      (let [x (bit-and (+ (* x 1103515245) 12345) 0x7FFFFFFF)]
        (aset-byte ba i (unchecked-byte (mod x 256)))
        (recur (inc i) x))))
  (let [enc (.encodeToString (Base64/getEncoder) ba)
        ^bytes dec (.decode (Base64/getDecoder) enc)
        enc-sum (reduce (fn [a c] (mod (+ a (int c)) 2147483647)) 0 enc)
        dec-sum (areduce dec i acc 0 (mod (+ acc (bit-and (aget dec i) 0xFF)) 2147483647))]
    (println (mod (+ enc-sum dec-sum) 2147483647))))
