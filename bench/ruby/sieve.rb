# Sieve of Eratosthenes to N, counting primes. Checksum = count of primes <= N.
n = (ENV["BENCH_N"] || "1000000").to_i
comp = Array.new(n + 1, false)
p = 2
while p * p <= n
  unless comp[p]
    j = p * p
    while j <= n
      comp[j] = true
      j += p
    end
  end
  p += 1
end
count = 0
(2..n).each { |k| count += 1 unless comp[k] }
puts count
