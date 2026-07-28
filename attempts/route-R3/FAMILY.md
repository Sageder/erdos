# FAMILY.md — an explicit infinite family inside S_1, with complete proof

Route R3, step 1. All notation as in PROBLEM.md. Throughout, for a prime ℓ let
c_ℓ(n) denote the number of carries when adding n + n in base ℓ; by Kummer,
c_ℓ(n) = ν_ℓ(binom(2n, n)), and by Legendre c_ℓ(n) = (2 s_ℓ(n) − s_ℓ(2n))/(ℓ−1).

## The family

**Definition (family F).**
F = { n = pq − 1 : q and p are primes, q ≥ 3, and (3q+1)/2 ≤ p ≤ 2q − 1 }.

(For q an odd prime, (3q+1)/2 is an integer.) First members, by increasing q:

| q | admissible p | n = pq − 1 |
|---|---|---|
| 3 | 5 | 14 |
| 5 | (none: no prime in [8, 9]) | — |
| 7 | 11, 13 | 76, 90 |
| 11 | 17, 19 | 186, 208 |
| 13 | 23 | 298 |
| 17 | 29, 31 | 492, 526 |
| 19 | 29, 31, 37 | 550, 588, 702 |
| 23 | 37, 41, 43 | 850, 942, 988 |

All of 14, 76, 90, 186, 208, 298 appear in the verified initial segment of S_1
(PROBLEM.md sanity table / membership.py output).

**Theorem 1.** F ⊆ S_1, i.e. ((n+1)!)² | (2n)! for every n ∈ F.

**Theorem 2 (infinitude).** For every prime q ≥ 17 there exists a prime p with
(3q+1)/2 ≤ p ≤ 2q − 1. Consequently F is infinite, and S_1 is infinite
(Balakran's theorem re-derived, with an explicit family).

## Proof of Theorem 1

### Lemma 1 (localized valuation criterion, any k ≥ 1)

For every n ≥ k ≥ 1:
n ∈ S_k ⇔ ( ∏_{j=1}^{k}(n+j) )² divides binom(2n, n)
⇔ for every prime ℓ dividing (n+1)⋯(n+k): c_ℓ(n) ≥ 2 Σ_{j=1}^{k} ν_ℓ(n+j).

*Proof.* For any prime ℓ,
ν_ℓ((2n)!) − 2 ν_ℓ((n+k)!) = [ν_ℓ((2n)!) − 2 ν_ℓ(n!)] − 2 Σ_{j=1}^{k} ν_ℓ(n+j)
= ν_ℓ(binom(2n,n)) − 2 Σ_{j=1}^{k} ν_ℓ(n+j),
using (n+k)! = n! · ∏_{j=1}^k (n+j). So ((n+k)!)² | (2n)! holds iff for EVERY prime ℓ,
ν_ℓ(binom(2n,n)) ≥ 2 Σ_j ν_ℓ(n+j). For ℓ ∤ (n+1)⋯(n+k) the right side is 0 and the
left side is ≥ 0, so only primes dividing the window matter. Kummer's theorem converts
ν_ℓ(binom(2n,n)) into c_ℓ(n). ∎

(For k = 1 this reads: n ∈ S_1 ⇔ (n+1)² | binom(2n,n) ⇔ ∀ ℓ | n+1 : c_ℓ(n) ≥ 2ν_ℓ(n+1).
Numerical cross-check of Lemma 1 against the verbatim PROBLEM.md digit criterion
"∀p: 2s_p(n+k) − s_p(2n) ≥ 2k": reductions.py, claims R1–R5, all n ≤ 3000, k = 1, 2,
zero discrepancies; the PROBLEM.md sanity tables for S_1, S_2, S_3 are reproduced
exactly by membership.py.)

### Setting

Let q ≥ 3 and p be primes with (3q+1)/2 ≤ p ≤ 2q − 1, and n = pq − 1. Since
p ≥ (3q+1)/2 > q, we have p > q, so p ≠ q and
n + 1 = pq, ν_p(n+1) = ν_q(n+1) = 1, ν_ℓ(n+1) = 0 for all ℓ ∉ {p, q}.
By Lemma 1 it suffices to prove c_p(n) ≥ 2 and c_q(n) ≥ 2.

### Lemma 2 (two carries at p)

Base-p expansion: n = pq − 1 = (q−1)·p + (p−1), and 0 ≤ q − 1 < p, so the base-p
digits of n are (d_1, d_0) = (q−1, p−1). Adding n + n in base p:
- position 0: d_0 + d_0 = 2(p−1) = p + (p−2) ≥ p (as p ≥ 2), so a carry occurs;
- position 1: d_1 + d_1 + 1 = 2(q−1) + 1 = 2q − 1 ≥ p by the hypothesis p ≤ 2q − 1,
  so a carry occurs.
Hence c_p(n) ≥ 2. ∎

### Lemma 3 (two carries at q)

Let r = p − q. The hypotheses (3q+1)/2 ≤ p ≤ 2q − 1 give exactly
(q+1)/2 ≤ r ≤ q − 1.
Base-q expansion: n = (q + r)q − 1 = 1·q² + (r−1)·q + (q−1), with digits
(d_2, d_1, d_0) = (1, r−1, q−1), valid since 0 ≤ r − 1 ≤ q − 2 < q. Adding n + n:
- position 0: 2(q−1) = q + (q−2) ≥ q (as q ≥ 2): carry;
- position 1: 2(r−1) + 1 = 2r − 1 ≥ q ⇔ r ≥ (q+1)/2, which holds: carry.
Hence c_q(n) ≥ 2. ∎

### Conclusion of Theorem 1

By Lemmas 2 and 3, c_p(n) ≥ 2 = 2ν_p(n+1) and c_q(n) ≥ 2 = 2ν_q(n+1); all other
primes impose no condition by Lemma 1. So n ∈ S_1. ∎

Remark (exactness). For every member with q ≤ 300 the carry counts are EXACTLY
c_p(n) = 2 and c_q(n) = 2 (except q = 3, where a third carry occurs at position 2:
2·1 + 1 = 3 ≥ 3) — verified in family_verify_extra.py (V3). The proof spends the
whole carry budget; nothing is wasted, and both interval endpoints are sharp (below).

## Proof of Theorem 2 (infinitude)

We use one classical effective prime-gap result:

**Nagura's theorem [Nagura 1952].** For every real x ≥ 25 there is a prime p with
x < p < (6/5)x.

Let q ≥ 17 be prime and set x = (3q+1)/2 ≥ 26 ≥ 25. Nagura gives a prime p with
(3q+1)/2 < p < (9q+3)/5.
Since q ≥ 8 we have 9q + 3 ≤ 10q − 5, i.e. (9q+3)/5 ≤ 2q − 1, so p ≤ 2q − 1 (indeed
p < 2q and p is an integer ≠ 2q). Thus for EVERY prime q ≥ 17 an admissible p exists,
and n = pq − 1 ∈ F ⊆ S_1.

Infinitude: the map n ↦ n + 1 = pq determines the unordered pair {p, q} by unique
factorization, and q is the smaller factor; distinct primes q therefore give distinct
n. Since there are infinitely many primes q ≥ 17 (Euclid) and n + 1 = pq > (3/2)q²,
the family F contains members exceeding any bound: F is infinite. ∎

Quantifier audit: for every N, choose (Bertrand/Euclid) a prime q ≥ max(17, √N);
Nagura supplies p; then n = pq − 1 > q² − 1 ≥ N and n ∈ S_1. All constants explicit
(25 in Nagura; q ≥ 17; q ≥ 8 for the interval inclusion). No parameter depends on n.

## Sharpness and non-maximality (numerics)

- Upper endpoint sharp: for p = 2q + 1 (one step past 2q − 1; then position-1 sum at p
  is 2q − 1 < p), n = pq − 1 ∉ S_1 in all 20 cases with q < 400 where 2q+1 is prime.
- Lower endpoint: taking the largest prime p' < (3q+1)/2 with p' > q, membership
  fails in 75 cases with q < 400 (it can accidentally survive via a deeper carry, so
  the lower endpoint is sharp for the METHOD, not a membership boundary).
- F is a strict subfamily of S_1: e.g. n = 27 (n+1 = 28 = 2²·7), n = 41
  (42 = 2·3·7), n = 44 (45 = 3²·5) are in S_1 but not of the form pq.

## Relation to the hexagonal hint

Hexagonal numbers are m = j(2j−1). The boundary case p = 2q − 1 of F gives
n + 1 = q(2q−1): hexagonal numbers whose index j = q is prime and whose companion
2q − 1 is also prime. Hint values explained:
- 15 = 3·5 (q=3, p=5), 91 = 7·13 (q=7, p=13 = 2q−1): family members;
- 77 = 7·11 (q=7, p=11 ∈ [11,13]): family member, not hexagonal;
- 6, 28, 45, 66, 153, 42, 110, 126, 140, 156, 170: in S_1 + 1 but not semiprime pq
  with the required balance — outside F (S_1 is larger than F);
- 120 = 2³·3·5 (hexagonal, j = 8 composite) is NOT in S_1 + 1: it fails exactly at
  ℓ = 3: 2s_3(120) − s_3(238) = 8 − 8 = 0 < 2 (verified). The hexagonal pattern is
  a shadow of the true mechanism (balanced factorization + carries), not the mechanism.

## Numerical verification ledger (all exact integer arithmetic)

Scripts in this directory; every claim above was falsified-then-confirmed BEFORE the
proof was written.

| script | what it verifies | result |
|---|---|---|
| membership.py | PROBLEM.md digit criterion vs. independent Legendre-valuation check (n < 500, k ≤ 3); reproduces PROBLEM.md tables for S_1 (all 40 elements ≤ 441), S_2 (first 20, smallest 208), S_3 (first 4) | all gates pass |
| s2_count_gate.py | PROBLEM.md calibration count \|S_2 ∩ [1, 2·10⁵]\| = 1981 (fast R4 form) | 1981 exactly |
| reductions.py | Lemma 1 forms R1–R4 and Kummer/Legendre identity R5, n ≤ 3000 | confirmed |
| family_test.py | F ⊆ S_1 by the FULL all-primes PROBLEM.md criterion for all 1137 members with q ≤ 400; the exact digit expansions of Lemmas 2–3; sharpness; Nagura coverage: the only prime q < 2·10⁵ with no admissible p is q = 5 | confirmed |
| family_verify_extra.py | V1: direct big-integer ((n+1)!)² \| (2n)! for the 29 members with n ≤ 3000; V2: per-prime test for all 36 697 members with q ≤ 3000 (largest n = 17 955 012); V3: carry counts exactly 2 | confirmed |

## Status

Proof status: COMPLETE. Theorem 1 is fully elementary (Legendre + Kummer + two
2-line digit computations). Theorem 2 uses Nagura (1952), an effective, classical,
unconditional result within the PROBLEM.md-allowed toolbox ("Bertrand/prime
counting"). No heuristics enter the statements; the density remark
|F ∩ [1,X]| ≍ X/log²X (PNT heuristic, consistent with the counts above) is marked
heuristic and is not used anywhere.
