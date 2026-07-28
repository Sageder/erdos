# BREAKAGE.md — exactly what breaks at k = 2

Route R3, step 2. Notation as in PROBLEM.md and FAMILY.md: c_ℓ(n) = number of carries
in n + n base ℓ = ν_ℓ(binom(2n,n)). All numerical claims are from the scripts listed
in the ledger at the end; every deterministic claim below was numerically confirmed
before being proved.

## 0. The k = 2 criterion

Lemma 1 of FAMILY.md with k = 2 (verified as R2/R4 in reductions.py, n ≤ 3000):

n ∈ S_2 ⇔ ((n+1)(n+2))² | binom(2n,n) ⇔
for every prime ℓ | (n+1)(n+2): c_ℓ(n) ≥ 2ν_ℓ(n+1) + 2ν_ℓ(n+2).

Since gcd(n+1, n+2) = 1, each prime serves only one of the two neighbours. The k = 2
problem is therefore EXACTLY the k = 1 problem plus one extra clause: the complete
prime factorization of the second neighbour must also be paid for in carries.

## 1. Re-running the k = 1 construction: what survives, what breaks

Take the proven k = 1 family n = pq − 1, q < p primes, (3q+1)/2 ≤ p ≤ 2q−1.

**Survives (provable, unchanged).** At ℓ ∈ {p, q}: ν_ℓ(n+2) = 0, so the k = 2 demand
at p and q is still 2 carries each, and Lemmas 2–3 of FAMILY.md still deliver them.
Confirmed: among all 699 family members with q ≤ 300 that fail S_2, EVERY failing
prime divides n + 2; none divides n + 1 (breakage_test.py, B1; zero exceptions).

**Breaks (measured on the 699 members with q ≤ 300).**

| outcome | count | share |
|---|---|---|
| n ∈ S_2 (luck: n+2 = pq+1 happens to cooperate) | 82 | 11.7% |
| killed by a failing prime ℓ | n+2 with ℓ² > 2n | 403 | 57.7% |
| n+2 is √(2n)-smooth but a carry demand at a prime of n+2 fails | 214 | 30.6% |

The construction breaks in exactly one place: n + 2 = pq + 1 is an arithmetically
uncontrolled integer. Notably the smallest element of S_2, n = 208 (n+1 = 11·19,
n+2 = 210 = 2·3·5·7), IS a member of the k = 1 family — the family is the right
skeleton; what is missing is any theorem about the factorization of pq + 1.

## 2. Taxonomy of failing primes (size ranges and digit patterns)

Let ℓ^e ∥ n+2 (the same discussion applies to n+1 with n ≡ −1 replacing n ≡ −2).

**(F-I) Large primes, ℓ(ℓ−1) > 2n, e = 1: unconditional death.**
*Lemma.* If ℓ | n+2 and ℓ(ℓ−1) > 2n, then n ∉ S_2.
*Proof.* n < ℓ², so n = d₁ℓ + (ℓ−2) with d₁ = ⌊n/ℓ⌋, and the demand is c_ℓ(n) ≥ 2.
Position 0 can carry, but position 1 carries only if 2d₁ + 1 ≥ ℓ, i.e.
d₁ ≥ (ℓ−1)/2, i.e. 2n ≥ 2d₁ℓ ≥ ℓ(ℓ−1), contradiction. So c_ℓ(n) ≤ 1 < 2. ∎
This is PROBLEM.md's large-prime criterion localized to our situation, and it forces
n+1 AND n+2 both (essentially) √(2n)-smooth — the double-smoothness wall. It kills
57.7% of family members; for a "random" integer the survival probability of the n+2
side alone is Dickman ρ(u) with u → 2, i.e. ρ(2) = 1 − log 2 ≈ 0.307 (measured
survival 42.3%, consistent since ν-thresholds sit slightly below u = 2).

**(F-II) Medium primes, roughly n^{1/3} < ℓ ≤ √(2n), e = 1: a coin-flip digit condition.**
n has 2–3 digits base ℓ; d₀ = ℓ−2 always carries (ℓ ≥ 5); the required second carry
happens iff a leading digit is ≥ (ℓ−1)/2 (up to a carry-in). For n = pq − 1 the base-ℓ
digits of n are rigid (determined by pq mod ℓ³), so per prime this is an
uncontrollable ≈ 1/2 event. Examples (breakage_test.py output): n = 492 fails at
19 | 494 (2s₁₉(494) − s₁₉(984) = −14 < 4); n = 1362 fails at 11 and 31 | 1364.

**(F-III) Small primes with e ≥ 2: demand collides with the digit supply cap.**
*Lemma (carry cap).* c_ℓ(n) ≤ ⌊log_ℓ n⌋ + 1 (carries occur only at the ≤ ⌊log_ℓ n⌋+1
digit positions of n). Hence if ℓ^e ∥ n+2 and 2e > ⌊log_ℓ n⌋ + 1 (in particular
whenever ℓ^{2e} > ℓn), then n ∉ S_2 unconditionally. ∎
Examples: n = 14 (n+2 = 2⁴: demand s₂(14) ≥ 8, cap 4); n = 702 (704 = 2⁶·11:
demand s₂(702) ≥ 12, actual 7).
More generally, e ≈ ν means the low 2e digits of n = (n+2) − 2 base ℓ are
(ℓ−2, ℓ−1, …, ℓ−1), which supply exactly 2e−… wait — supply exactly the low-position
carries, but demand grows twice as fast as the valuation, so any prime POWER carrying
a constant fraction of log n dies: the sustainable regime is ℓ^{2e} ≲ n.

**(F-IV) ℓ = 2, 3 (the 2k − s_p(2k) constants).** At ℓ = 2 the demand is
c₂(n) = s₂(n) ≥ 2ν₂(n+2) (for even n+2); mild for ν₂ = 1, deadly for large ν₂ (F-III).

**Quantified carry budget (balanced_smooth_test.py).** Build n+2 = 2·∏_{i≤t} p_i^{e_i}
(first t odd primes, balanced exponents, n ≈ 10¹⁰) and test only the n+2-side demands:

| t (number of odd primes of n+2) | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| success rate | 0.000% | 0.000% | 24.4% | 49.8% | 76.7% | 88.9% |

t ≤ 2 is IMPOSSIBLE-or-negligible (demand 2e_i ≈ (2/t)·log_{p_i} n versus supply
≈ κ·log_{p_i} n with carry density κ ≈ 0.5: need 2/t < κ), and the success rate rises
to 1 as t grows. Digit pattern of failure: the prime with the largest e_i relative to
its digit count fails first. Conclusion: a workable n+2 must be built from ≥ 3 (in
practice ≥ 4–5) prime factors of comparable logarithmic size, each with valuation
well below half its digit count — exactly the shape 210 = 2·3·5·7 of the real
smallest solution 208.

## 3. Repair attempts and why each fails

**(a) Congruence conditions on (p, q).** CRT can force pq ≡ −1 (mod M) for any fixed
smooth M, planting M inside n+2. But the cofactor (pq+1)/M has size n/M with M fixed
as n → ∞, and F-I applies to ITS prime factors with unchanged positive frequency; no
finite set of congruences controls a positive proportion of log(n+2) of the
factorization. Congruences fix F-IV and plant seeds, but cannot touch F-I/F-II.
Verdict: irreparable by congruences alone.

**(b) Polynomial parametrizations force squares, and squares lose.**
*Lemma Q.* Suppose X² + σX + β = (X+b)(X+c) and X² + σX + β + 1 = (X+d)(X+e) with
b, c, d, e ∈ ℤ (the generic way to make both neighbours split after a substitution
X = t² + at + const). Then d = e: the "+1 side" is a perfect square (X+d)².
*Proof.* b + c = d + e = σ and de = bc + 1, so (b−c)² = σ² − 4bc and
(d−e)² = σ² − 4bc − 4; hence (b−c)² − (d−e)² = 4. Two integer squares of the same
parity differing by 4 must be 4 and 0, so d = e. ∎
So the natural consecutive-splitting identities are n+1 = u² − 1, n+2 = u²
(u = X + d), and Pell variants below. But a square DOUBLES every valuation:
ν_ℓ(n+2) = 2ν_ℓ(u) =: 2e, demand 4e carries. Writing n = u² − 2, ℓ^e ∥ u: the low 2e
digits of n are (ℓ−2, ℓ−1, …, ℓ−1) — they supply EXACTLY 2e carries — and the missing
2e must come from doubling (u/ℓ^e)² − 1 in base ℓ. If u is prime (e = 1, u = ℓ): the
top part is 0, supply 2 < 4: deterministic failure. In general every prime of u must
find its extra 2e carries in a rigid digit expansion: no parameters remain.

**(c) Pell parametrizations (the only non-square-free escape from Lemma Q).**
x² − 2y² = ∓1 gives (n+1, n+2) = (x², 2y²) or (2y², x²), n = x² − 2. Numerics
(breakage_test.py B3, breakage_test2.py B3'): among the first 30 solutions of each
sign (x up to ~10²³): Pell(−1): 1 member of S_2; Pell(+1): 4 members. Every failure
is at the large prime(-power) factors of x or y with carry deficit exactly as
predicted (e.g. x = 41: demand 4, supply 2; x = 275807 = 7·31²·41: at 31², demand 8,
supply 6). The sporadic hits occur precisely when x AND y are simultaneously very
smooth with lucky digits (e.g. y = 543339720 = 2³·3·5·…). To prove infinitude along
Pell one would need: infinitely many Pell solutions whose x and y are BOTH
n^{o(1)}-ish smooth with prescribed digit luck — a smoothness statement about a
rigid exponentially-growing recurrence. Størmer/Lehmer theory gives the OPPOSITE
(finiteness for any fixed smoothness bound); nothing is known for growing bounds.
Dead end for proofs; the mechanism (valuation doubling vs. rigid digits) is now precise.

**(d) Sieve technology.** What is needed is: infinitely many n with n+1 = pq
(balanced semiprime) AND n+2 both √(2n)-smooth AND per-prime carry conditions. Known
unconditional smoothness for shifted primes — e.g. Baker–Harman: infinitely many
primes P with P⁺(P−1) < P^{0.2961} — controls ONE shifted prime, gives no
simultaneous control of a second neighbour, no balanced-semiprime structure, no
valuation/digit control (sieves bound P⁺ but cannot prescribe exponents e_i or
digits). Moreover smoothness alone is demonstrably insufficient: 30.6% of family
members have n+2 fully √(2n)-smooth and still fail carries. No current sieve
statement even addresses the factorization type of pq + 1.

## 4. The repaired construction (rigorous, conditional): Lemma R

The k = 1 proof used 2 free prime parameters to control n+1. The unique repair that
keeps every step elementary is to spend 2 MORE free prime parameters on n+2 — at the
price of one Diophantine equation tying them.

**Lemma R.** Let q, p, s, r be primes with q ≥ 3, s ≥ 5, and n = pq − 1, satisfying
1. pq + 1 = 2rs;
2. (3q+1)/2 ≤ p ≤ 2q − 1;
3. 2s + 1 ≤ r ≤ 4s − 1;
4. (2r mod s) ≥ (s+1)/2;
5. n is not a power of 2.
Then n ∈ S_2, i.e. ((n+2)!)² | (2n)!.

*Proof.* n + 1 = pq and n + 2 = 2rs, with p > q (from 2), r > s (from 3), and
{p,q} ∩ {2,r,s} = ∅ (consecutive integers are coprime). So ν is 1 at each of
p, q, r, s, ν₂(n+2) = 1, and by Lemma 1 (k = 2) the demands are: 2 carries at each
of p, q, r, s and c₂(n) ≥ 2. 
At p and q: identical to Lemmas 2–3 of FAMILY.md (hypothesis 2). 
At r: 2s − 1 < r by (3), so n = 2rs − 2 = (2s−1)·r + (r−2) has base-r digits
(2s−1, r−2). Position 0: 2(r−2) ≥ r ⇔ r ≥ 4: carry. Position 1: 2(2s−1) + 1 =
4s − 1 ≥ r by (3): carry. Total ≥ 2. 
At s: write 2r = As + b, A = ⌊2r/s⌋, b = 2r mod s; b ≠ 0 since s ∤ 2r (s odd prime
≠ r). Then n = As² + (b−1)s + (s−2), so the two low base-s digits are (b−1, s−2)
regardless of how A expands further. Position 0: 2(s−2) ≥ s ⇔ s ≥ 4: carry (s ≥ 5).
Position 1: 2(b−1) + 1 = 2b − 1 ≥ s ⇔ b ≥ (s+1)/2, which is hypothesis 4: carry.
Total ≥ 2. 
At 2: c₂(n) = ν₂(binom(2n,n)) = 2s₂(n) − s₂(2n) = s₂(n) ≥ 2, since n is even
(indeed rs odd ⇒ n = 2rs − 2 ≡ 0 mod 4) and not a power of 2 (hypothesis 5). 
No other prime divides (n+1)(n+2). ∎

**Numerical status (breakage_test2.py B4', lemmaR_digit_check.py).** Among family
pairs with q ≤ 4000 there are 8916 members with n+2 = 2rs (r, s distinct odd
primes); 123 of them satisfy all hypotheses of Lemma R, and ALL 123 are confirmed in
S_2 (fast equivalent criterion for all; verbatim PROBLEM.md all-primes criterion for
22 of them including the 5 smallest; every internal digit claim of the proof checked
on all 123). First solutions (q, p, s, r, n): (109, 193, 67, 157, 21036),
(389, 773, 251, 599, 300696), (439, 787, 227, 761, 345492), … Growth of the solution
count: 10 at q ≤ 1000, 38 at q ≤ 2000, 123 at q ≤ 4000 — consistent with the
heuristic count ≍ Q²/log⁴Q (four prime conditions, one equation, one ≈1/2 digit
condition; no local obstruction detected).

## 5. Precise breakage statement and the most promising repair

**The k = 2 breakage mechanism, in one sentence.** The k = 1 proof works because the
entire multiplicative structure of the single constrained neighbour n+1 can be CHOSEN
(two free prime parameters, digit conditions then verified in two lines); at k = 2
the second neighbour n+2 = (chosen n+1) + 1 has rigid, unchoosable multiplicative
structure, and the criterion taxes EVERY prime power of it: large primes are fatal
(F-I, 57.7%), medium primes are coin flips (F-II), high valuations are fatal (F-III),
and no known tool (congruences, polynomial identities — which force squares by Lemma
Q, and squares double valuations past the digit supply —, Pell recurrences, sieves)
converts "chosen + 1" into controlled factored form.

**Blocking statement B (single missing ingredient).** Infinitely many prime
quadruples (q, p, s, r) with
pq + 1 = 2rs, (3q+1)/2 ≤ p ≤ 2q−1, 2s+1 ≤ r ≤ 4s−1, (2r mod s) ≥ (s+1)/2.
By Lemma R (hypothesis 5 can fail only for the ≤ log₂-many powers of 2), statement B
implies S_2 is infinite, resolving the open k = 2 variant of Erdős 727 affirmatively.

**Ranking of repair routes.**
1. (Most promising) Statement B as a bilinear equation in primes: pq − 2rs = −1 with
   all four variables in prescribed dyadic boxes (p ≍ q ≍ √n balanced, r ≍ s ≍ √n
   balanced) and one positive-proportion digit condition. It is a fixed-coefficient
   analogue of Diophantine equations attacked by dispersion/bilinear-sums methods
   (Friedlander–Iwaniec, Bombieri–Friedlander–Iwaniec, Drappeau on E(x) for
   pq + 1-type equations); solutions are numerically abundant with quadratic growth,
   and the digit condition only needs equidistribution of r mod s. Everything else
   about the route is proved (Lemma R is complete and elementary).
2. Relaxation of Lemma R to n+2 = 2·(product of t = 3..5 controlled primes in
   dyadic/digit boxes) — the balanced-smooth data (Section 2) shows the digit
   conditions become nearly free as t grows, so many-variable versions of B (more
   freedom, same single equation) are strictly easier targets for analytic methods:
   e.g. pq + 1 = 2·r₁r₂r₃ with r_i ≍ n^{1/3} and mild digit conditions.
3. (Not promising) Pell/polynomial families: mechanism understood and provably
   square-burdened; would need unproved smoothness of rigid recurrences.
4. (Not promising) Congruence engineering: structurally cannot reach F-I.

## 6. Numerical ledger

| script | contents |
|---|---|
| breakage_test.py (B1, B2) | localization of k=2 failures to primes of n+2 (0 exceptions/699); failure taxonomy counts; Pell(−1) small solutions with per-prime carry deficits |
| breakage_test2.py (B3', B4') | 30+30 Pell solutions both signs (fast criterion, proved equivalent and re-checked vs. full criterion for n < 4000); Lemma-R solution search q ≤ 4000: 123 solutions, 0 counterexamples |
| lemmaR_digit_check.py | every internal digit claim of Lemma R verified on all 123 solutions; full PROBLEM.md criterion on the smallest 5 |
| balanced_smooth_test.py | carry-budget phase transition in t = number of odd primes of n+2 |
| reductions.py | equivalence of all criterion forms used here (R1–R5), n ≤ 3000 |

Proved here: Lemma 1 (k=2 form), F-I lemma, carry-cap lemma, Lemma Q, Lemma R.
Heuristic (marked as such): all density/percentage statements, the Q²/log⁴Q solution
count, and the expectation that statement B holds.
