n = (ENV["BENCH_N"] || "540").to_i
maxiter = 100

total = 0
(0...n).each do |py|
  y0 = py.to_f / n * 3.0 - 1.5
  (0...n).each do |px|
    x0 = px.to_f / n * 3.0 - 2.0
    x = 0.0
    y = 0.0
    i = 0
    xx = 0.0
    yy = 0.0
    while xx + yy <= 4.0 && i < maxiter
      y = 2.0 * x * y + y0   # uses old x, old y
      x = xx - yy + x0       # uses old xx, yy
      xx = x * x
      yy = y * y
      i += 1
    end
    total += i
  end
end

puts total
