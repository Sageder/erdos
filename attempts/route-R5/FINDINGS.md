# Route R5 FINDINGS — large-scale computation and pattern mining (Erdős 727)

All results computed 2026-07-28 with exact integer arithmetic (numpy int64, values < 2^31;
digit criterion per PROBLEM.md). Everything here is DESCRIPTIVE STATISTICS on exact member
lists — no claim below is a proof about infinitude; all "expectations/enrichments" are
heuristic baselines and are marked as such.

## 1. Sieve status

Segmented sieve (`sievelib.py` + `driver.py`), architecture per brief: per block
(a) rough remainder sieve dividing out all prime powers p^e <= mhi with p <= isqrt(mhi);
the residual of each window element is 1 or a single prime (proved by a size argument,
asserted at runtime); n survives iff max residual over window <= isqrt(2n);
(b) exact vectorized digit check 2*s_p(n+k) - s_p(2n) >= 2k for all p <= isqrt(2(R-1))
on survivors (checking a superset of p <= isqrt(2n) is exact: the digit criterion is the
true condition at every prime). n <= 200 handled by direct per-prime digit check
(large-prime rejection needs n > 2k^2; 2*6^2 = 72 < 200).

Validation (calibrate_sieve.py, all PASS):
- C1: PROBLEM.md tables reproduced exactly (S_2 first 20 and |S_2 cap [1,2e5]| = 1981;
  S_3 first 8 and |S_3 cap [1,6e4]| = 41; S_4 cap [1,6e4] = {8174, 51984}).
- C2: full agreement with experiments/erdos727.in_Sk_fast on block [1e6, 1e6+1e4)
  (all members + 300 random n, k = 2 and 3).
- C3: scan-order independence of the digit stage verified.
- Post-run: 30 members + 30 non-members near 1e8 re-verified against in_Sk_fast for
  k = 2, 3, 5 (all agree).

**Completed range: [1, 10^8) for k = 2,3,4,5,6 simultaneously** (250 s wall on 4 cores;
50 resumable block checkpoints in data/blocks/). Counts:

| k | |S_k cap [1,1e8)| | step-(a) survivors (smooth windows) | member/survivor ratio | min S_k |
|---|-------------------|-------------------------------------|-----------------------|---------|
| 2 | 1,364,676 | 9,450,927 | 0.1444 | 208 |
| 3 | 139,975   | 2,775,573 | 0.0504 | 3,475 |
| 4 | 13,188    | 801,939   | 0.0164 | 8,174 |
| 5 | 1,012     | 231,487   | 0.0044 | 252,965 |
| 6 | 63        | 67,015    | 0.00094 | 3,648,835 |

Member lists: data/S{2..6}_run1.txt (sorted, exact). First S_5 elements: 252965,
347849, 681546, 844964, 1371365. All 63 S_6 elements are in data/S6_run1.txt.

## 2. Top mined patterns

### P1. Density is slowly INCREASING; counting function mildly superlinear
Per-decade densities of S_k (mine_density.out):
- k=2: 0.0058 (decade to 1e4) -> 0.0095 -> 0.0114 -> 0.0128 (decade to 1e8);
  log-log slope of the counting function over [1e6,1e8] = 1.040.
- k=3: 0.00033 -> 0.00071 -> 0.00093 -> 0.00122; slope 1.092.
- k=4: slope 1.124; k=5: slope 1.236; k=6: slope 1.447 (small counts).
Interpretation (heuristic): local density tracks rho(u_n)^k * (digit-pass probability)
with u_n = log n / log sqrt(2n) -> 2 from below, so density tends to a constant
c_k ~ rho(2)^k * q_k and count ~ c_k X; the increase toward it is the u_n -> 2 transient.
At X = 1e8: count/X = 1.36e-2 (k=2), 1.40e-3 (k=3), 1.32e-4 (k=4), 1.01e-5 (k=5),
6.3e-7 (k=6). Successive ratios ~ 0.103, 0.094, 0.077, 0.062: consistent with a
roughly constant factor ~ 0.1 per increment of k. NO sign of the density dying at any
k <= 6; max nearest-member gap for k=2 in the last decade is 1030 (mean gap 78),
stable per decade.

### P2. Digit-stage pass probability and where the kills happen
Member/survivor ratio 0.144, 0.050, 0.016, 0.0044, 0.00094 for k=2..6 at 1e8 —
declining ~geometrically (~1/3 per k step). The per-prime kill is spread thinly across
ALL primes p <= sqrt(2n): among k=2 survivors in [1e6,2e6], the top killing primes are
tiny (p=3 kills 5.9%, p=2 3.3%, p=7 3.1% of survivors) and 203 distinct primes are
needed to account for 99% of kills. Mean digit margins D_p = 2 s_p(n+k) - s_p(2n) - 2k
for members at 1e8 scale (k=2): 8.9 (p=2), 11.9 (p=3), 17.1 (p=5) — the condition is
typically loose; P(D_p = 0 exactly) <= 5% per prime. No single "hard prime" dominates:
the obstruction is genuinely multiplicative over many primes.

### P3. No congruence obstruction; all congruence bias = window divisibility
(mine_congruence.out) Zero forbidden residue classes mod every tested modulus
(2,4,8,16,3,9,27,5,25,7,49,11,13 and p^2 for p <= 7) for k=2,3,4. The enrichment
pattern is exactly: (n+j) ≡ 0 (mod p) for some window slot j is over-represented
(e.g. k=2: n+2 ≡ 0 or 1 mod 49 at ratio 1.80/1.79; n ≡ p-1, p-2 mod p enriched ~1.5x
for p = 11, 13), and residues making the window coprime to p are uniformly mildly
depleted (~0.85). Slot-shifted ratios (G2b) are near-exact translates of one another —
the bias lives on the window, not on n itself. chi2/dof for n mod p decays smoothly
(5332 at p=17 down to 725 at p=71 for k=2). Consequence: no CRT/covering-style
finiteness obstruction is visible in the data.

### P4. NO algebraic family carries S_k
(mine_algebraic.out) Enrichment scan of n = y^2-c, 2y^2-c, 3y^2-c, y^3-c, y^4-c,
|c| <= 30:
- The only enriched c are c = a*m^2 + 1 and a*m^2 + 2 for the form a*y^2 - c (for
  y^2: c = 5,6,10,11,17,18,26,27 = m^2+{1,2}; for 2y^2: c = 9,10,19,20 = 2m^2+{1,2};
  for 3y^2: c = 4,5,13,14,28,29 = 3m^2+{1,2}), at modest ratios 2.0-2.7x, never more.
  These are exactly the c for which n+1 or n+2 = a(y-m)(y+m), i.e. a window element
  with a balanced 2-factor split — a smoothness boost, not an algebraic family.
- The natural candidate family n = x^2 - 2 (n+2 square) is NOT enriched for k=2:
  120 hits vs 136.5 expected. n+k a perfect square for k=3: 6 hits vs 14 expected
  (slightly depleted — plausibly because x^2-1 = (x-1)(x+1) has two forced factors).
- Fourth powers: n = y^4-c mildly enriched at c = 3,17,18,27 (5-8 hits vs 1.4
  expected; same m^2+{1,2} mechanism; counts too small to be more than suggestive).
- k >= 4: nothing enriched at all; members look "generic smooth".

### P5. Members ride the very edge of the smoothness constraint
(mine_window.out) For the max largest-prime-factor P over the window,
u = log P / log sqrt(2n):
- k=2 members: median u = 0.926, 15.3% have P > 0.9*sqrt(2n), max ratio 1.0
  (P = isqrt(2n) exactly attained).
- k=3: median 0.967; k=4: 0.976; k=5: 0.981; k=6: 0.987; fraction with
  P > 0.9 sqrt(2n): 23% (k=3), 30% (k=4), 34% (k=5), 44% (k=6).
As k grows, members are forced ever closer to the sqrt(2n) smoothness ceiling — the
windows are barely-smooth, generic (typical slot: 3-5 distinct prime factors,
squarefree-dominated shapes), with NO structure in which slot carries the largest
prime factor (slot distribution uniform within noise for every k, e.g. k=6:
12/8/10/10/11/12 vs 10.5 uniform). Adjacent pairs (n, n+1 both in S_k) are strongly
enriched over the independence baseline (7.8x for k=2, 72x k=3, 710x k=4, 7025x k=5
— 72 pairs; even S_6 has 4 adjacent pairs, e.g. 30978449/50), as predicted by window
overlap (a pair needs k+1 smooth values, not 2k); runs up to length 6 occur for k=2.

## 3. Interpretation relative to the routes (heuristic only)

- Everything mined is consistent with "smooth windows + digit conditions behave like
  independent mild constraints": S_k density stabilizes at a positive constant
  c_k ≈ 1.4e-2, 1.4e-3, 1.3e-4, 1.0e-5, 6e-7 for k = 2..6 — the data give no hint of
  an eventual NO-branch obstruction for any k <= 6, and no modular or algebraic
  structure that a YES-branch proof could ride.
- Absence of enrichment for n = x^2-2 (P4) is a caution for family-based YES attempts
  at k=2: quadratic families are not privileged among members; what matters is window
  smoothness, and members are typically barely-smooth generic windows (P5).
- A YES proof must beat the product-over-primes digit obstruction (P2); no finite set
  of primes dominates.

## 4. Files

- sievelib.py — core segmented sieve (rough remainder sieve + vectorized digit check).
- driver.py — checkpointed, resumable, deterministic production driver (4 workers).
- calibrate_sieve.py — calibration gate (C1-C3), kill_order_k2.json.
- mine_density.py, mine_congruence.py, mine_algebraic.py, mine_digit.py,
  mine_window.py — miners; outputs in logs/mine_*.out.
- data/S{2,3,4,5,6}_run1.txt — exact sorted member lists on [1, 1e8).
- data/summary_run1.json, data/blocks/run1_b*.json — counts + checkpoints.
- logs/run1.log — production log (250 s wall, 50 blocks).

Not run (feasible, ~30 min): extension to [1e8, 1e9) via
python3 driver.py --start 100000000 --end 1000000000 --ks 2,3,4,5,6 --tag run2
(same pipeline; resumable).
