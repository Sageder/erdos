"""Discovery 3 test: Pell-based smooth-window supply for k=3.

Claims tested:
 (P1) solutions of y^2 - 2u^2 = -1 give x = 2u with x^2 - 2 = 2y^2, so the window
      {x^2-2, x^2-1, x^2} of n = x^2-3 is sqrt(2n)-smooth (verified directly);
 (P2) which Pell members actually land in S_3 (digit conditions uncontrolled — expect
      sporadic hits); failing primes reported for the misses.
"""
import sys, math
sys.path.insert(0, '.')
from erdos727 import in_Sk_fast, failing_primes, largest_prime_factor

# Pell: y^2 - 2u^2 = -1; fundamental (y,u)=(1,1); recurrence (y,u) -> (3y+4u, 2y+3u)
sols = []
y, u = 1, 1
while u < 6 * 10 ** 6:
    sols.append((y, u))
    y, u = 3 * y + 4 * u, 2 * y + 3 * u

for y, u in sols:
    x = 2 * u
    n = x * x - 3
    if n < 10:
        continue
    assert x * x - 2 == 2 * y * y
    win = [n + 1, n + 2, n + 3]
    lim = math.isqrt(2 * n)
    smooth = all(largest_prime_factor(w) <= lim for w in win)
    member = in_Sk_fast(n, 3)
    fp = [] if member else failing_primes(n, 3)[:8]
    print(f"x={x} n={n} window-smooth(sqrt(2n)={lim}): {smooth} in_S3: {member} "
          f"failing_primes: {fp}", flush=True)
