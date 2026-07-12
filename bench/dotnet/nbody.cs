namespace Bench;
static class Nbody
{
    // N-body sim; canonical formulation shared by all 7 langs (see node/nbody.js).
    // Checksum = floor(energy*1e9 + 0.5).
    public static void Run(int n)
    {
        const double PI = 3.141592653589793, SOLAR_MASS = 4 * PI * PI, DPY = 365.24, DT = 0.01;
        double[] x  = { 0, 4.84143144246472090e+00, 8.34336671824457987e+00, 1.28943695621391310e+01, 1.53796971148509165e+01 };
        double[] y  = { 0, -1.16032004402742839e+00, 4.12479856412430479e+00, -1.51111514016986312e+01, -2.59193146099879641e+01 };
        double[] z  = { 0, -1.03622044471123109e-01, -4.03523417114321381e-01, -2.23307578892655734e-01, 1.79258772950371181e-01 };
        double[] vx = { 0, 1.66007664274403694e-03 * DPY, -2.76742510726862411e-03 * DPY, 2.96460137564761618e-03 * DPY, 2.68067772490389322e-03 * DPY };
        double[] vy = { 0, 7.69901118419740425e-03 * DPY, 4.99852801234917238e-03 * DPY, 2.37847173959480950e-03 * DPY, 1.62824170038242295e-03 * DPY };
        double[] vz = { 0, -6.90460016972063023e-05 * DPY, 2.30417297573763929e-05 * DPY, -2.96589568540237556e-05 * DPY, -9.51592254519715870e-05 * DPY };
        double[] m  = { SOLAR_MASS, 9.54791938424326609e-04 * SOLAR_MASS, 2.85885980666130812e-04 * SOLAR_MASS, 4.36624404335156298e-05 * SOLAR_MASS, 5.15138902046611451e-05 * SOLAR_MASS };

        double px = 0, py = 0, pz = 0;
        for (int i = 0; i < 5; i++) { px += vx[i] * m[i]; py += vy[i] * m[i]; pz += vz[i] * m[i]; }
        vx[0] = -px / SOLAR_MASS; vy[0] = -py / SOLAR_MASS; vz[0] = -pz / SOLAR_MASS;

        double[] nvx = new double[5], nvy = new double[5], nvz = new double[5];
        for (int s = 0; s < n; s++)
        {
            for (int i = 0; i < 5; i++)
            {
                double ax = vx[i], ay = vy[i], az = vz[i];
                for (int j = 0; j < 5; j++)
                {
                    if (j != i)
                    {
                        double dx = x[i] - x[j], dy = y[i] - y[j], dz = z[i] - z[j];
                        double dsq = dx * dx + dy * dy + dz * dz;
                        double dist = Math.Sqrt(dsq);
                        double mag = DT / (dsq * dist);
                        ax -= dx * m[j] * mag; ay -= dy * m[j] * mag; az -= dz * m[j] * mag;
                    }
                }
                nvx[i] = ax; nvy[i] = ay; nvz[i] = az;
            }
            for (int i = 0; i < 5; i++)
            {
                vx[i] = nvx[i]; vy[i] = nvy[i]; vz[i] = nvz[i];
                x[i] += DT * vx[i]; y[i] += DT * vy[i]; z[i] += DT * vz[i];
            }
        }

        double e = 0;
        for (int i = 0; i < 5; i++) e += 0.5 * m[i] * (vx[i] * vx[i] + vy[i] * vy[i] + vz[i] * vz[i]);
        for (int i = 0; i < 5; i++)
            for (int j = i + 1; j < 5; j++)
            {
                double dx = x[i] - x[j], dy = y[i] - y[j], dz = z[i] - z[j];
                double dist = Math.Sqrt(dx * dx + dy * dy + dz * dz);
                e -= m[i] * m[j] / dist;
            }
        Console.WriteLine((long)Math.Floor(e * 1e9 + 0.5));
    }
}
