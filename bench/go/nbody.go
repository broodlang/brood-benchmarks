// N-body gravitational sim (Sun + 4 gas giants), N steps of symplectic Euler.
// Canonical formulation shared by every port: each body's new velocity summed
// over j (ascending, j!=i) from the CURRENT positions; then positions advance.
// Checksum = floor(energy*1e9 + 0.5).
package main

import (
	"fmt"
	"math"
)

func main() {
	n := benchN(50000)
	const pi = 3.141592653589793
	const solarMass = 4 * pi * pi
	const dpy = 365.24
	const dt = 0.01
	// order: sun, jupiter, saturn, uranus, neptune
	x := []float64{0, 4.84143144246472090e+00, 8.34336671824457987e+00, 1.28943695621391310e+01, 1.53796971148509165e+01}
	y := []float64{0, -1.16032004402742839e+00, 4.12479856412430479e+00, -1.51111514016986312e+01, -2.59193146099879641e+01}
	z := []float64{0, -1.03622044471123109e-01, -4.03523417114321381e-01, -2.23307578892655734e-01, 1.79258772950371181e-01}
	vx := []float64{0, 1.66007664274403694e-03 * dpy, -2.76742510726862411e-03 * dpy, 2.96460137564761618e-03 * dpy, 2.68067772490389322e-03 * dpy}
	vy := []float64{0, 7.69901118419740425e-03 * dpy, 4.99852801234917238e-03 * dpy, 2.37847173959480950e-03 * dpy, 1.62824170038242295e-03 * dpy}
	vz := []float64{0, -6.90460016972063023e-05 * dpy, 2.30417297573763929e-05 * dpy, -2.96589568540237556e-05 * dpy, -9.51592254519715870e-05 * dpy}
	m := []float64{solarMass, 9.54791938424326609e-04 * solarMass, 2.85885980666130812e-04 * solarMass, 4.36624404335156298e-05 * solarMass, 5.15138902046611451e-05 * solarMass}

	px, py, pz := 0.0, 0.0, 0.0
	for i := 0; i < 5; i++ {
		px += vx[i] * m[i]
		py += vy[i] * m[i]
		pz += vz[i] * m[i]
	}
	vx[0] = -px / solarMass
	vy[0] = -py / solarMass
	vz[0] = -pz / solarMass

	var nvx, nvy, nvz [5]float64
	for s := 0; s < n; s++ {
		for i := 0; i < 5; i++ {
			ax, ay, az := vx[i], vy[i], vz[i]
			for j := 0; j < 5; j++ {
				if j != i {
					dx, dy, dz := x[i]-x[j], y[i]-y[j], z[i]-z[j]
					dsq := dx*dx + dy*dy + dz*dz
					dist := math.Sqrt(dsq)
					mag := dt / (dsq * dist)
					ax -= dx * m[j] * mag
					ay -= dy * m[j] * mag
					az -= dz * m[j] * mag
				}
			}
			nvx[i], nvy[i], nvz[i] = ax, ay, az
		}
		for i := 0; i < 5; i++ {
			vx[i], vy[i], vz[i] = nvx[i], nvy[i], nvz[i]
			x[i] += dt * vx[i]
			y[i] += dt * vy[i]
			z[i] += dt * vz[i]
		}
	}

	e := 0.0
	for i := 0; i < 5; i++ {
		e += 0.5 * m[i] * (vx[i]*vx[i] + vy[i]*vy[i] + vz[i]*vz[i])
	}
	for i := 0; i < 5; i++ {
		for j := i + 1; j < 5; j++ {
			dx, dy, dz := x[i]-x[j], y[i]-y[j], z[i]-z[j]
			dist := math.Sqrt(dx*dx + dy*dy + dz*dz)
			e -= m[i] * m[j] / dist
		}
	}
	fmt.Println(int64(math.Floor(e*1e9 + 0.5)))
}
