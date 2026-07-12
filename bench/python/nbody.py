# N-body sim; canonical formulation shared by all 7 langs (see node/nbody.js).
# Checksum = floor(energy*1e9 + 0.5).
import os, math
N = int(os.environ.get("BENCH_N", "50000"))
PI = 3.141592653589793
SOLAR_MASS = 4 * PI * PI
DPY = 365.24
DT = 0.01
x  = [0.0, 4.84143144246472090e+00, 8.34336671824457987e+00, 1.28943695621391310e+01, 1.53796971148509165e+01]
y  = [0.0, -1.16032004402742839e+00, 4.12479856412430479e+00, -1.51111514016986312e+01, -2.59193146099879641e+01]
z  = [0.0, -1.03622044471123109e-01, -4.03523417114321381e-01, -2.23307578892655734e-01, 1.79258772950371181e-01]
vx = [0.0, 1.66007664274403694e-03 * DPY, -2.76742510726862411e-03 * DPY, 2.96460137564761618e-03 * DPY, 2.68067772490389322e-03 * DPY]
vy = [0.0, 7.69901118419740425e-03 * DPY, 4.99852801234917238e-03 * DPY, 2.37847173959480950e-03 * DPY, 1.62824170038242295e-03 * DPY]
vz = [0.0, -6.90460016972063023e-05 * DPY, 2.30417297573763929e-05 * DPY, -2.96589568540237556e-05 * DPY, -9.51592254519715870e-05 * DPY]
m  = [SOLAR_MASS, 9.54791938424326609e-04 * SOLAR_MASS, 2.85885980666130812e-04 * SOLAR_MASS, 4.36624404335156298e-05 * SOLAR_MASS, 5.15138902046611451e-05 * SOLAR_MASS]

px = py = pz = 0.0
for i in range(5):
    px += vx[i] * m[i]; py += vy[i] * m[i]; pz += vz[i] * m[i]
vx[0] = -px / SOLAR_MASS; vy[0] = -py / SOLAR_MASS; vz[0] = -pz / SOLAR_MASS

nvx = [0.0] * 5; nvy = [0.0] * 5; nvz = [0.0] * 5
for _ in range(N):
    for i in range(5):
        ax = vx[i]; ay = vy[i]; az = vz[i]
        for j in range(5):
            if j != i:
                dx = x[i] - x[j]; dy = y[i] - y[j]; dz = z[i] - z[j]
                dsq = dx * dx + dy * dy + dz * dz
                dist = math.sqrt(dsq)
                mag = DT / (dsq * dist)
                ax -= dx * m[j] * mag; ay -= dy * m[j] * mag; az -= dz * m[j] * mag
        nvx[i] = ax; nvy[i] = ay; nvz[i] = az
    for i in range(5):
        vx[i] = nvx[i]; vy[i] = nvy[i]; vz[i] = nvz[i]
        x[i] += DT * vx[i]; y[i] += DT * vy[i]; z[i] += DT * vz[i]

e = 0.0
for i in range(5):
    e += 0.5 * m[i] * (vx[i] * vx[i] + vy[i] * vy[i] + vz[i] * vz[i])
for i in range(5):
    for j in range(i + 1, 5):
        dx = x[i] - x[j]; dy = y[i] - y[j]; dz = z[i] - z[j]
        dist = math.sqrt(dx * dx + dy * dy + dz * dz)
        e -= m[i] * m[j] / dist
print(math.floor(e * 1e9 + 0.5))
