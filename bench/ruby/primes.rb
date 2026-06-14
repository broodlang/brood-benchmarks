n = (ENV["BENCH_N"] || "150000").to_i

def prime?(n)
  return false if n < 2
  limit = Integer.sqrt(n)   # exact integer sqrt, once — no d*d in the loop
  d = 2
  while d <= limit
    return false if n % d == 0
    d += 1
  end
  true
end

count = 0
(2...n).each { |k| count += 1 if prime?(k) }

puts count
