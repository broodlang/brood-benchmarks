;; N-body sim; canonical formulation shared by all 7 langs (see node/nbody.js).
;; Idiomatic-fast Clojure = primitive double-arrays. Checksum = floor(energy*1e9+0.5).
(let [n (Long/parseLong (or (System/getenv "BENCH_N") "50000"))
      pi 3.141592653589793
      sm (* 4.0 pi pi)
      dpy 365.24
      dt 0.01
      ^doubles x  (double-array [0.0 4.84143144246472090e+00 8.34336671824457987e+00 1.28943695621391310e+01 1.53796971148509165e+01])
      ^doubles y  (double-array [0.0 -1.16032004402742839e+00 4.12479856412430479e+00 -1.51111514016986312e+01 -2.59193146099879641e+01])
      ^doubles z  (double-array [0.0 -1.03622044471123109e-01 -4.03523417114321381e-01 -2.23307578892655734e-01 1.79258772950371181e-01])
      ^doubles vx (double-array [0.0 (* 1.66007664274403694e-03 dpy) (* -2.76742510726862411e-03 dpy) (* 2.96460137564761618e-03 dpy) (* 2.68067772490389322e-03 dpy)])
      ^doubles vy (double-array [0.0 (* 7.69901118419740425e-03 dpy) (* 4.99852801234917238e-03 dpy) (* 2.37847173959480950e-03 dpy) (* 1.62824170038242295e-03 dpy)])
      ^doubles vz (double-array [0.0 (* -6.90460016972063023e-05 dpy) (* 2.30417297573763929e-05 dpy) (* -2.96589568540237556e-05 dpy) (* -9.51592254519715870e-05 dpy)])
      ^doubles m  (double-array [sm (* 9.54791938424326609e-04 sm) (* 2.85885980666130812e-04 sm) (* 4.36624404335156298e-05 sm) (* 5.15138902046611451e-05 sm)])
      ^doubles nvx (double-array 5)
      ^doubles nvy (double-array 5)
      ^doubles nvz (double-array 5)]
  (loop [i 0 px 0.0 py 0.0 pz 0.0]
    (if (< i 5)
      (recur (inc i) (+ px (* (aget vx i) (aget m i))) (+ py (* (aget vy i) (aget m i))) (+ pz (* (aget vz i) (aget m i))))
      (do (aset vx 0 (/ (- px) sm)) (aset vy 0 (/ (- py) sm)) (aset vz 0 (/ (- pz) sm)))))
  (dotimes [_ n]
    (dotimes [i 5]
      (loop [j 0 ax (aget vx i) ay (aget vy i) az (aget vz i)]
        (if (< j 5)
          (if (= j i)
            (recur (inc j) ax ay az)
            (let [dx (- (aget x i) (aget x j)) dy (- (aget y i) (aget y j)) dz (- (aget z i) (aget z j))
                  dsq (+ (* dx dx) (* dy dy) (* dz dz))
                  dist (Math/sqrt dsq)
                  mag (/ dt (* dsq dist))
                  mj (aget m j)]
              (recur (inc j) (- ax (* dx mj mag)) (- ay (* dy mj mag)) (- az (* dz mj mag)))))
          (do (aset nvx i ax) (aset nvy i ay) (aset nvz i az)))))
    (dotimes [i 5]
      (aset vx i (aget nvx i)) (aset vy i (aget nvy i)) (aset vz i (aget nvz i))
      (aset x i (+ (aget x i) (* dt (aget vx i))))
      (aset y i (+ (aget y i) (* dt (aget vy i))))
      (aset z i (+ (aget z i) (* dt (aget vz i))))))
  (let [e0 (loop [i 0 e 0.0]
             (if (< i 5)
               (recur (inc i) (+ e (* 0.5 (aget m i) (+ (* (aget vx i) (aget vx i)) (* (aget vy i) (aget vy i)) (* (aget vz i) (aget vz i))))))
               e))
        e (loop [i 0 e e0]
            (if (< i 5)
              (recur (inc i)
                     (loop [j (inc i) e e]
                       (if (< j 5)
                         (let [dx (- (aget x i) (aget x j)) dy (- (aget y i) (aget y j)) dz (- (aget z i) (aget z j))
                               dist (Math/sqrt (+ (* dx dx) (* dy dy) (* dz dz)))]
                           (recur (inc j) (- e (/ (* (aget m i) (aget m j)) dist))))
                         e)))
              e))]
    (println (long (Math/floor (+ (* e 1e9) 0.5))))))
