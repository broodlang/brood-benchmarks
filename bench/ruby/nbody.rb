# N-body sim; canonical formulation shared by all 7 langs (see node/nbody.js).
# Checksum = floor(energy*1e9 + 0.5).
n = (ENV["BENCH_N"] || "50000").to_i
pi = 3.141592653589793
solar_mass = 4 * pi * pi
dpy = 365.24
dt = 0.01
x  = [0.0, 4.84143144246472090e+00, 8.34336671824457987e+00, 1.28943695621391310e+01, 1.53796971148509165e+01]
y  = [0.0, -1.16032004402742839e+00, 4.12479856412430479e+00, -1.51111514016986312e+01, -2.59193146099879641e+01]
z  = [0.0, -1.03622044471123109e-01, -4.03523417114321381e-01, -2.23307578892655734e-01, 1.79258772950371181e-01]
vx = [0.0, 1.66007664274403694e-03 * dpy, -2.76742510726862411e-03 * dpy, 2.96460137564761618e-03 * dpy, 2.68067772490389322e-03 * dpy]
vy = [0.0, 7.69901118419740425e-03 * dpy, 4.99852801234917238e-03 * dpy, 2.37847173959480950e-03 * dpy, 1.62824170038242295e-03 * dpy]
vz = [0.0, -6.90460016972063023e-05 * dpy, 2.30417297573763929e-05 * dpy, -2.96589568540237556e-05 * dpy, -9.51592254519715870e-05 * dpy]
m  = [solar_mass, 9.54791938424326609e-04 * solar_mass, 2.85885980666130812e-04 * solar_mass, 4.36624404335156298e-05 * solar_mass, 5.15138902046611451e-05 * solar_mass]

px = py = pz = 0.0
(0...5).each { |i| px += vx[i] * m[i]; py += vy[i] * m[i]; pz += vz[i] * m[i] }
vx[0] = -px / solar_mass; vy[0] = -py / solar_mass; vz[0] = -pz / solar_mass

nvx = Array.new(5, 0.0); nvy = Array.new(5, 0.0); nvz = Array.new(5, 0.0)
n.times do
  (0...5).each do |i|
    ax = vx[i]; ay = vy[i]; az = vz[i]
    (0...5).each do |j|
      next if j == i
      dx = x[i] - x[j]; dy = y[i] - y[j]; dz = z[i] - z[j]
      dsq = dx * dx + dy * dy + dz * dz
      dist = Math.sqrt(dsq)
      mag = dt / (dsq * dist)
      ax -= dx * m[j] * mag; ay -= dy * m[j] * mag; az -= dz * m[j] * mag
    end
    nvx[i] = ax; nvy[i] = ay; nvz[i] = az
  end
  (0...5).each do |i|
    vx[i] = nvx[i]; vy[i] = nvy[i]; vz[i] = nvz[i]
    x[i] += dt * vx[i]; y[i] += dt * vy[i]; z[i] += dt * vz[i]
  end
end

e = 0.0
(0...5).each { |i| e += 0.5 * m[i] * (vx[i] * vx[i] + vy[i] * vy[i] + vz[i] * vz[i]) }
(0...5).each do |i|
  (i + 1...5).each do |j|
    dx = x[i] - x[j]; dy = y[i] - y[j]; dz = z[i] - z[j]
    dist = Math.sqrt(dx * dx + dy * dy + dz * dz)
    e -= m[i] * m[j] / dist
  end
end
puts (e * 1e9 + 0.5).floor
