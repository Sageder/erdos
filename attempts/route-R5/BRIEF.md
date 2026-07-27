# Route R5 brief — large-scale data mining

Read /home/user/erdos/PROBLEM.md first; it is binding. You may also read
/home/user/erdos/experiments/erdos727.py (validated membership checkers; calibration gate
already passed) and reuse it.

Task: industrial-scale computation + pattern mining. Everything in
/home/user/erdos/attempts/route-R5/ (scripts, outputs, findings).

1. Build a SCALABLE sieve for S_2 and S_3 membership up to N = 10^8 (do NOT loop primes per
   n). Architecture: segmented sieve over blocks; for each n in a block, (a) compute the
   largest prime factor of each window element n+1..n+k via a smallest-prime-factor/rough
   sieve on the block, reject if any exceeds sqrt(2n) (large-prime criterion, valid for
   n > 2k^2); (b) for survivors only, run digit checks at all p <= sqrt(2n). Survivor density
   is ~rho(2)^k so step (b) is cheap. Target: S_2 complete to 10^8 (should be feasible in
   ~1-2 hours; checkpoint each block to disk, resumable), S_3 to 10^8, S_4/S_5/S_6 as far as
   feasible. Validate the sieve against the PROBLEM.md tables and against in_Sk_fast on a
   random sample before the long run. Save results as sorted lists (one file per k).
2. Mining on the results:
   - Congruence structure: distribution of n mod small prime powers; of n+k mod p^2 for
     small p; any forbidden/enriched classes?
   - Algebraic hits: how many n are of the form x^2-2, z^4-2, x^2-c (small c),
     2y^2-something; how many have n+k a perfect square/power; window factorization shapes.
   - Digit motifs: base-p digit statistics of n+k at small p for members vs non-members.
   - Nearest-member gaps vs n (is the density stabilizing? fit |S_k cap [1,X]| ~ c_k X?).
   - Adjacent pairs (n, n+1 both in S_k) statistics.
   - For S_3/S_4 members: factorize all window elements; classify the largest prime factors
     (how close to sqrt(2n) do they get?); is there structure in which window slot carries
     the biggest factor?
3. Deliverables: FINDINGS.md (quantitative, tables), data files, all scripts deterministic
   and resumable.
Return: structured summary — sieve status (ranges completed, counts per k), top 5 mined
patterns with exact statistics, files written.
