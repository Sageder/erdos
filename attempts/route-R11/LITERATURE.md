# Route R11 — Literature: the analytic frontier for Statement B

Scope: pure literature research on the analytic technology relevant to Statement B
(infinitely many prime quadruples q, p, s, r with pq + 1 = 2rs, (3q+1)/2 ≤ p ≤ 2q−1,
2s+1 ≤ r ≤ 4s−1, r/s in the prescribed archimedean windows), which implies the k = 2
variant of the target problem via the verified elementary lemma (n = pq − 1 ∈ S_2).
All statements below were checked against the cited sources (arXiv full texts, zbMATH
reviews via the public API, journal pages) during this session. Where I could only
verify a statement through a secondary source, this is flagged explicitly. Nothing
below was obtained by searching for the target problem itself.

## 0. What Statement B demands, in sieve-theoretic coordinates (frame for everything below)

Write N = pq (so n = N − 1, N + 1 = 2rs, m := (N+1)/2 = rs). Statement B asks: infinitely
many m such that the **specific pair** of linear forms

    L1(m) = 2m − 1  is an E_2 number pq  (both factors odd primes, p/q ∈ (roughly) [3/2, 2)),
    L2(m) = m       is an E_2 number rs  (r/s ∈ [9/4,5/2)∪[11/4,3)∪[13/4,7/2)∪[15/4,4)).

Three separable analytic obstructions, in increasing order of depth:

- (O1) **Archimedean localization** (the ratio windows): harmless in principle. Restricting
  the two prime factors of an E_2 to fixed positive-measure ratio/size windows only changes
  singular-series/Mertens constants; every sieve framework below tolerates it.
- (O2) **Balancedness**: both factors of each E_2 must be ≍ N^{1/2} (within a factor 2).
  This is *forced by the problem*, not an artifact of the lemma: by the large-prime
  criterion in PROBLEM.md, any n ∈ S_2 has n+1, n+2 both √(2n)-smooth, so if n+1 = pq
  then automatically √(n/2) ≤ p, q ≤ √(2n). (Verified numerically on the first 20 elements
  of S_2.) Balanced E_2's are exactly the E_2's that current detection methods *cannot* use
  (see §3, (1.24) of GGPY-PLMS).
- (O3) **Parity, squared**: prescribing that a *specific* form takes E_2 values (exact
  parity of Ω) is the parity problem; Statement B prescribes it at *two* specified forms
  simultaneously. Even the single-form version ("2p+1 is E_2 for infinitely many primes p")
  is explicitly open (§2). No published unconditional technique specifies the parity of
  Ω at even one member of a tuple, except by anchoring that member as a *prime* via
  Bombieri–Vinogradov — and O2 rules out prime anchors here (a prime > √(2n) in n+1 or
  n+2 destroys S_2 membership).

Consequence used repeatedly below: **Chen-style anchoring is structurally unavailable** for
S_2. Chen's device (one variable an honest prime, the other sieved to P_2) cannot produce
S_2 configurations because S_2 forbids any prime factor > √(2n) in the window.

---

## 1. Heath-Brown, "Consecutive almost-primes" (1987) and its orbit

**Citation.** D. R. Heath-Brown, *Consecutive almost-primes*, J. Indian Math. Soc. (N.S.)
52 (1987), 39–49; correction/addendum: *A note on the paper "Consecutive almost-primes"*,
J. Indian Math. Soc. (N.S.) 66 (1999), 203–205.

**Exact statement** (from the zbMATH review of the 1987 paper, cross-checked against later
citations, e.g. Banks–Pollack–Pomerance, arXiv:1908.06161, which cites the 1987 paper and
the 1999 note jointly). There is an absolute constant c > 0 such that there are infinitely
many n for which **both n and n+1 have a prime factor > n^{1−ε(n)} with
ε(n) = c (log log n / log n)^{1/4}**. This is a quantitative sharpening of:

- A. Hildebrand, *On a conjecture of Balog*, Proc. Amer. Math. Soc. 95 (1985), 517–523:
  for every fixed 0 ≤ α < β ≤ 1, the set of n with n^α < P(n) < n^β **and**
  (n+1)^α < P(n+1) < (n+1)^β has **positive lower density** (P = largest prime factor).
  This proves a 1982 conjecture of Balog giving a general sufficient condition on a set
  A ⊆ ℕ (defined by constraints on largest-prime-factor size) for A ∩ (A+1) to be infinite,
  and answers an Erdős problem (both n, n+1 with a prime factor > n^{1−ε}).

**Mechanism** (important as a template): construction of sets S = {d_1 < … < d_R} ⊂ ℕ with
d_j − d_i | (d_i, d_j) for all i < j, minimizing τ(S) = lcm{d_j − d_i}; Heath-Brown proves
such sets exist with log τ ≪ R³ log R (and any such set has log τ ≫ R log R). Given such a
set, one engineers n with n ≡ −? (mod scaled d_i) so that several of the numbers a·n + 1
share structure; the same combinatorial gadget underlies the Erdős–Mirsky solution
(Heath-Brown, *The divisor function at consecutive integers*, Mathematika 31 (1984),
141–149) and Banks–Pollack–Pomerance's symmetric-primes theorem. The 1999 note repairs
the 1987 paper; later authors cite the pair [1987]+[1999] together for both the theorem
and the set construction (I could not access the note's text; zbMATH blocks it. Treat the
1987 numerical exponent as "as corrected in 1999" when precision matters).

**Consecutive P_2's (Chen-type for n, n+1 both almost-prime).** The strongest facts I can
find are:
- Via Chen's 2p+1 theorem (§2): infinitely many n with **n and n+1 both P_2** — take
  n = 2p (Ω = 2) and n + 1 = 2p + 1 ∈ P_2. Hence also Ω(n(n+1)) ≤ 4 infinitely often.
  This deduction is folklore-level (immediate from Halberstam–Richert Ch. 11) but I found
  no paper stating "consecutive P_2's" as a headline; treat as folklore-with-proof.
- GGPY (§3, Theorem 3 of PLMS 2009): for **any admissible pair** of linear forms {L1, L2},
  infinitely many n with L1(n), L2(n) both P_2 and all prime factors of L1(n)L2(n)
  exceeding n^{1/10}. Applied to the admissible pair {m, 2m−1}: infinitely many m with
  m and 2m−1 both P_2, all prime factors > m^{1/10} — i.e. consecutive integers
  N = 2m−1, N+1 = 2m with N ∈ P_2, N+1 = 2·P_2, all odd prime factors > N^{1/10}.
  This is the *closest published statement to Statement B* (see §8).
- Getting Ω(n(n+1)) ≤ 3, or both n, n+1 ∈ P_2 with the P_2's *specified to be E_2*, is open
  (parity; §2–3).

**Applicability.** (b) Template, double-barreled. Hildebrand 1985 with (α, β) → (1/2 − δ, 1/2)
produces a **positive-density** set of n with n+1, n+2 both √-smooth *and* both possessing
a prime factor in (n^{1/2−δ}, n^{1/2}) — i.e. precisely the "one balanced large prime factor
+ smooth cofactor" skeleton that S_2 forces, with no parity input needed. What it cannot do:
make the cofactors prime (that is O3), nor control the digit/carry conditions at small primes.
If the elementary side of this project can be generalized from the pattern (pq, 2rs) to a
family of patterns "(a·p, 2b·q): a, b smooth and controlled, p, q balanced primes in windows",
then Heath-Brown/Hildebrand technology is the natural analytic engine — it is the only
unconditional technology in the literature that imposes nontrivial multiplicative structure
at *two consecutive integers with positive density*. Direct implication of Statement B: none.

---

## 2. Chen-type theorems with structure

**Chen's theorem.** J.-R. Chen, *On the representation of a larger even integer as the sum
of a prime and the product of at most two primes*, Sci. Sinica 16 (1973), 157–176 (announced
1966). Standard reference form (Halberstam–Richert, *Sieve Methods*, Academic Press 1974,
Ch. 11): there are infinitely many primes p with p + 2 ∈ P_2 (count ≫ x/log²x); the same
method gives, for fixed coprime (a, b) with 2 | ab, infinitely many primes p with
ap + b ∈ P_2; in particular **2p + 1 ∈ P_2 for infinitely many primes p**. GGPY
(arXiv:0803.2636, p. 2) state this exact disjunction: infinitely many p with 2p+1 ∈ 𝒫 or
2p+1 = p1p2, p1 ≠ p2 — and emphasize that *deciding which branch* ("the seemingly much
easier assertion that for infinitely many primes p, p+2 (or 2p+1) has an odd (or even)
number of prime factors") **is still open** — citing Hildebrand's survey. This is the
cleanest published certificate that "a specified form takes E_2 values" is beyond current
technology even with a prime anchor available.

**Factor localization inside Chen.** In the standard proof the E_2 branch comes with the
smaller prime factor localized: p + 2 = p1p2 with x^{1/10} < p1 ≤ x^{1/3} < p2 (sieve
parameters z = x^{1/10}, y = x^{1/3}; documented in Halberstam–Richert Ch. 11 and in the
expositions of Ross and Nathanson). So "P_2 with both factors > x^{1/10}" is classical.
Refinements that move the localization:
- Y.-C. Cai, *Chen's theorem with small primes*, Acta Math. Sin. (Engl. Ser.) 18 (2002),
  597–604 (zbMATH review verified): N = p + P_2 with the **prime anchor localized small**,
  p ≤ N^θ, θ = 0.95, with the expected lower bound of order C(N) N^θ (log N)^{−2}; uses
  Wu's short-interval generalized Bombieri–Vinogradov theorem (J. Wu, Q. J. Math. 44
  (1993), 109–128). Follow-ups: Chin. Ann. Math. B 32 (2011) 387–396; Taiwanese J. Math.
  19 (2015) 1183–1202.
- Heath-Brown–Li, *Almost-prime triples and Chen's theorem* (2015/2017): infinitely many
  primes p with p + 2 ∈ P_2 and p + 6 ∈ P_{r} for an explicit r — Chen plus an extra
  almost-prime condition at a third point. (Statement verified only at abstract level.)
- J. Maynard, *Almost-prime k-tuples* (arXiv:1205.4610, Mathematika): for admissible
  k-tuples, Ω(∏ L_i(n)) ≤ r_k infinitely often with r_k ~ k log k, improving classical
  weighted sieves for k ≥ 4; companion paper *3-tuples have at most 7 prime factors
  infinitely often* (arXiv:1205.5021).

**Applicability.** (c)/(b). Chen-type anchoring is structurally excluded for S_2 (see §0):
every Chen variant keeps one variable an honest prime of size N^{Ω(1)}, which S_2 forbids
(smoothness). What survives as a template is the *localization technology*: the sieve
tolerates prescribing both P_2 factors above x^{1/10} and one variable in archimedean
windows (O1, partially O2). No Chen variant addresses O3 for a specified form — the
2p+1-parity sentence above is the formal record that it cannot, today.

---

## 3. GGPY: E_2 numbers in tuples of linear forms ("Small gaps between products of two primes")

**Citation.** D. A. Goldston, S. W. Graham, J. Pintz, C. Y. Yıldırım, *Small gaps between
products of two primes*, Proc. Lond. Math. Soc. (3) 98 (2009), 741–774 (arXiv:math/0609615;
all statements below read from the arXiv full text). Companion: *Small gaps between primes
or almost primes*, Trans. Amer. Math. Soc. 361 (2009), 5285–5330 (arXiv:math/0506067;
earlier bound 26).

Let θ ∈ [1/2, 1) be a common level of distribution for primes and E_2 numbers in the
Bombieri–Vinogradov sense (their (1.17)), B = 2/θ; unconditionally B = 4 (θ = 1/2, by
Motohashi — see §4); Elliott–Halberstam for primes and E_2's would give B = 2 + ε.

- **Theorem 1.** For any constant D and admissible k-tuple of distinct linear forms
  L_i(x) = a_i x + b_i, there are ν + 1 forms among them which *simultaneously* take
  E_2 values with **both prime factors above D**, for infinitely many x, provided
  k ≥ C_1(ν) := (4e^{−γ}(1+o(1))/B) e^{Bν/4}.
- **Theorem 2.** For any admissible **triplet** {L1, L2, L3}: there exist two forms
  L_i, L_j (i ≠ j, *not chosen by us*) such that for infinitely many n both L_i(n), L_j(n)
  are E_2 numbers **all of whose prime factors exceed n^{1/144}**.
- **Theorem 3.** For any admissible **pair** {L1, L2}: infinitely many n with L1(n), L2(n)
  both **P_2**, and all prime factors of L1(n)L2(n) exceeding **n^{1/10}**; in particular
  n, n − d ∈ P_2 infinitely often for every even d.
- **Corollary 2.** liminf (q_{n+1} − q_n) ≤ 6, q_n the n-th E_2 number (unconditional;
  via the triple {n, n+2, n+6}). General: liminf (q_{n+ν} − q_n) ≤ νe^{ν−γ}(1+o(1)).
- **Parity anatomy, their (1.22)–(1.24)** (crucial for us): they state explicitly that
  their method succeeds *because* it exploits E_2 numbers of the special shape
  **n = p1p2, p1 < n^ε, p2 > n^{1−ε}** ("for any given small ε > 0"), and that "if we
  exclude numbers of type (1.24) for ε < c_0, then we would be unable to show Theorem 1".
  I.e., the detected E_2's are **essentially unbalanced**; the n^{1/144} localization of
  Theorem 2 is the published record in the balanced direction, and nothing in the paper
  (or, as far as I can find, in any successor: Thorne's number-field version, IMRN 2008;
  Sono; Vatwani) produces E_2's with both factors > n^δ for fixed large δ, let alone
  balanced ≍ n^{1/2} — for a *chosen* form or otherwise.
- **Consecutive E_2's (n, n+1 both E_2):** open, and doubly so. One of n, n+1 is even, so
  this is exactly "p prime with 2p ± 1 = E_2" up to the factor 2 — the parity-obstructed
  branch of Chen (§2). GGPY treat only even differences (their forms have equal leading
  coefficients in the gap corollaries); their Part-I paper (arXiv:0803.2636, p. 5) adds:
  "it is still unclear whether there is any theoretical obstacle which prevents us to find
  infinitely many pairs of E_2-numbers with a fixed difference" — i.e., even *fixed even
  difference* E_2 pairs are open; only "≤ 6" is known.

**The "which pair?" trick (how GGPY beat parity for consecutive integers).** In
*Small gaps between almost primes, the parity problem and some conjectures of Erdős on
consecutive integers* (arXiv:0803.2636; sequel: … II, J. Number Theory, 2021,
arXiv:2003.03661) they prove: for every A ≥ 4 infinitely many x with **Ω(x) = Ω(x+1) = A**;
for every A ≥ 3 infinitely many x with ω(x) = ω(x+1) = A; for every A with 24 | A,
d(x) = d(x+1) = A; and x, x+1 both with exponent pattern {2,1,1,1} (so d = 24, ω = 4,
Ω = 5). Method: choose a *designed* admissible triple with linear relations, e.g.
L1 = 6m+1, L2 = 8m+1, L3 = 9m+1 with 4L1 = 3L2 + 1, 3L1 = 2L3 + 1, 9L2 = 8L3 + 1, so that
**whichever** two forms the Basic Theorem makes E_2, suitable constant multiples of them are
consecutive integers with the desired invariants. The parity problem is "not bypassed but
overcome" *because* the target invariants (Ω = A ≥ 4, etc.) are stable under multiplying
an E_2 by a fixed constant with 2–3 prime factors. Limits of the trick: A = 2, 3 for
Ω(x) = Ω(x+1) = A remain **open** (their Theorem 7 only gives Ω = 3 numbers at distance
≤ 2), and prescribing *unequal* small values (Ω(x), Ω(x+1)) = (2, 3) — which is exactly
the S_2 shape (n+1 = pq, n+2 = 2rs) — is open a fortiori.

**Applicability.** (b) as template, (c) as direct tool. Direct use fails twice: (i) the
lemma's pattern is not stable under "multiply by a constant" (c·pq has Ω = 2 + Ω(c), no
longer the lemma's shape), so the which-pair trick cannot be transplanted *unless the
elementary side supplies a whole family of S_2-sufficient patterns covering all pairs of a
designed triple* — a concrete, well-posed research direction (see §8); (ii) even then, O2
kills it: the GGPY detector *needs* unbalanced E_2's (their own statement at (1.24)), while
S_2 forces balanced ones. Any GGPY-route proof of Statement B needs a new detection
mechanism for balanced E_2's in tuples — not available in the literature at any level of
localization beyond n^{1/144}-from-below (Theorem 2), and not for chosen forms at all.

---

## 4. Level of distribution for E_2 numbers; Titchmarsh-type problems for pq + 1

- **Motohashi's induction principle.** Y. Motohashi, *An induction principle for the
  generalization of Bombieri's prime number theorem*, Proc. Japan Acad. 52 (1976), 273–275.
  As stated by GGPY (PLMS 2009, §1, verified): if two arithmetic functions satisfy
  Bombieri–Vinogradov-type equidistribution (level x^{1/2}(log x)^{−C}), then under mild
  conditions so does their Dirichlet convolution; consequently **E_2 numbers (and products
  of two primes with factor-size weights) satisfy Bombieri–Vinogradov with level
  x^{1/2−ε} unconditionally**. This is the input GGPY use (θ = 1/2, B = 4). The principle
  is insensitive to O1/O2-type restrictions of the factors (the convolution can be
  restricted to p1 in a fixed range), which is why balanced-E_2 *counting in APs on
  average to level x^{1/2}* is available — detection in tuples is what's missing.
- **Beyond x^{1/2} for special convolutions.** É. Fouvry, M. Radziwiłł, *Level of
  distribution of unbalanced convolutions*, Ann. Sci. Éc. Norm. Supér. (4) 55 (2022)
  (arXiv:1811.08672, abstract verified): if an essentially arbitrary sequence supported on
  an interval of length x is convolved with a "tiny" Siegel–Walfisz-type sequence supported
  on an interval of length exp((log x)^ε), the convolution has (in a weak, averaged sense)
  level of distribution **x^{1/2 + 1/66 − ε}**; consequences include products of exactly
  two primes in APs to large moduli — but only for **extremely unbalanced** products (one
  factor of sub-polynomial size). Improved ranges: T. Wright (2023+). For balanced E_2's
  no level beyond x^{1/2} is published (the BFI-era results for αβ-convolutions with both
  factors ≫ x^δ concern well-factorable weights and special moduli; nothing citable gives
  a usable exponent > 1/2 for balanced E_2 with fixed residue).
- **Primes (for comparison/anchoring):** Bombieri–Friedlander–Iwaniec, Acta Math. 156
  (1986), 203–251: level x^{4/7−ε} for Λ with well-factorable weights, fixed residue;
  refined by Maynard (2020s) — irrelevant here since prime anchors are excluded (§0).
- **Titchmarsh divisor problems.** Classical: Σ_{p≤x} τ(p − a) = c·x + c1·Li(x) +
  O(x/(log x)^A) (Linnik dispersion; BFI Corollary 1; Fouvry Corollaire 2). Power-saving
  error: S. Drappeau, *Sums of Kloosterman sums in arithmetic progressions, and the error
  term in the dispersion method*, Proc. Lond. Math. Soc. 114 (2017), 684–732 — error
  O(x^{1−δ}) up to the contribution of a possible exceptional (Siegel) character.
  **For products of two primes:** S. Drappeau, B. Topacogullari, *Combinatorial identities
  and Titchmarsh's divisor problem for multiplicative functions*, Algebra & Number Theory
  13 (2019), 2383–2425 (abstract verified): full asymptotic expansions for shifted sums
  including Σ_{n ≤ x, ω(n)=k or Ω(n)=k} τ(n − h), uniform in the shift h — this contains
  the "Titchmarsh divisor problem for E_2" (asymptotics for Σ_{pq ≤ x} τ(pq + a));
  a function-field variant with Motohashi's induction principle: Darbar–Mukhopadhyay,
  arXiv:2301.12669. (An older integer-setting asymptotic of this type is attributed to
  Fujii (1976) in secondary sources; I could not verify the primary citation and flag it
  as unverified.)

**Applicability.** (a) for weak relaxations, (c) for Statement B itself. These results give:
average divisor statistics of pq + 1 and BV-level equidistribution of E_2's — enough to run
any GPY/Selberg-weighted argument with E_2-inputs (this is exactly what GGPY consume), and
enough to compute *expected* counts for Statement B's quadruples (the heuristic count is
≍ x/(log x)^4 · (window constants) — but no published machinery converts level-1/2
information into a lower bound for a doubly-parity-specified event. The specific sequence
{pq + 1 : p, q balanced primes} has no published level-of-distribution theorem of its own;
what exists is BV for E_2 (Motohashi) which contains it on the "source" side, not for the
shifted set.

---

## 5. The equation pq − 2rs = c and shifted-product equations

**Direct literature: none.** I found **no published lower bound or asymptotic** for the
number of solutions of p1p2 − 2p3p4 = c (all four prime, c ≠ 0 fixed) in boxes — under any
balancedness restriction or none — by dispersion, Friedlander–Iwaniec-style bilinear
methods, or otherwise. This is expected: specifying E_2 values at both ends is parity
squared (§0, O3); even the "half" equation with a prime anchor (p − 2rs = c, i.e. Chen with
the P_2 specified to be E_2) is the open branch of Chen's theorem (§2). Upper bounds of the
conjecturally correct order for such counts follow from standard upper-bound sieves
(folklore; e.g. via Selberg's sieve in four variables) — only the lower bound is deep.

**Adjacent published results (all upper-bound/solvability flavored):**
- Finite-field solvability of ab + 1 = cd with restricted variables: A. Sárközy (Acta
  Arith., 2005-era) proved solvability for A, B, C, D ⊆ F_p once |A||B||C||D| ≫ p³
  (density p^{−1/4} each); generalizations: K. Gyarmati, A. Sárközy, *Equations in finite
  fields with restricted solution sets I, II*, Acta Math. Hungar. (2008); P. Csikvári,
  K. Gyarmati, A. Sárközy, *Density and Ramsey type results on algebraic equations with
  restricted solution sets*, Combinatorica 32 (2012), 425–449. These densities are far
  above the density of primes-in-boxes reduced mod p; they certify only that there is no
  *local/CRT* obstruction to pq + 1 = 2rs-type equations — which for Statement B is
  already clear from the verified lemma's admissibility.
- Shifted-product/multiplication-table literature (Sárközy, Gyarmati, Stewart on P((ab+1)(cd+1)),
  Diophantine-tuple bounds, multiplicative energy of shifted sets): concerns largest prime
  factors or counts of *coincidences* ab + 1 = cd with a, b, c, d ranging over full
  intervals or fixed finite sets — no prime restriction on all four variables, no lower
  bounds for sparse prime inputs. (c) irrelevant beyond local-obstruction sanity.

**Applicability.** (c) for existing statements; the equation itself is *the* open core of
Statement B once O1/O2 are absorbed into weights. Honest summary: proving any nontrivial
lower bound for #{(p,q,r,s) prime: pq − 2rs = −1, all ≍ x} would be a major advance in its
own right, independent of this project.

---

## 6. Harman's sieve: exactly-two-prime-factor outputs with localized factors

**Framework.** G. Harman, *Prime-Detecting Sieves*, LMS Monographs 33, Princeton, 2007.
The comparison ("alternative") sieve produces asymptotics-with-positive-proportion for
counts of p1p2 with **both factors localized** (p1 ∈ [x^α, x^β] prescribed), in a sequence
𝒜, provided the sequence has: Type I information (linear sums Σ_{d ≤ x^{θ1}} a_d error
control — a level of distribution), and Type II information (bilinear sums with both
variables in [x^{σ}, x^{1−σ}] for some window). E_2-detection is *easier* than
prime-detection in this framework precisely because one may give away one factor to the
Type II range: the standard trick writes the E_2 count as a double sum anchored at the
smaller factor, so the smaller factor lands where the bilinear information lives. That is
why all published applications produce **unbalanced or mildly-balanced** E_2's.

**Published applications (verified at abstract level):**
- J. Teräväinen, *Almost primes in almost all short intervals*, Math. Proc. Camb. Phil.
  Soc. (2018) (arXiv:1510.06005): almost all intervals [x, x + log^{3.51} x] contain an
  E_2 number; almost all [x, x + log^{1+ε} x] contain an E_3 number.
- K. Matomäki, J. Teräväinen, *Almost primes in almost all short intervals II*
  (arXiv:2207.05038): (log x)^{2.1} for E_2; new Type II estimate via Heath-Brown's mean
  value for sparse Dirichlet polynomials.
- K. Matomäki, *Almost primes in almost all very short intervals* (arXiv:2012.11565):
  P_2 (at most two) in almost all intervals of length h log X, h → ∞ arbitrarily slowly
  (Richert weights + Kloosterman averages) — P_2, not E_2: parity again marks the boundary.
- Older/parallel: E_2/P_2 results in Piatetski-Shapiro sequences, Beatty sequences,
  a² + b² + 1, etc. (Baker–Banks–…, Iwaniec-school); all share the unbalanced-E_2 shape.

**Applicability.** (b) — the *only* framework in the literature designed to output
"exactly two prime factors, both localized", hence the natural tool for any single-form
component of a relaxed Statement B (e.g. counting balanced E_2's rs with 2rs − 1 lying in
a prescribed sparse but *sieve-friendly* set). What it cannot do: the target set here,
{m : 2m − 1 = E_2}, is itself parity-defined, so it supplies no usable Type I/II inputs;
Harman's sieve applied to 𝒜 = {(pq+1)/2 : p, q balanced primes} founders at the Type II
stage (the sequence has no proven bilinear estimates — this is again the pq − 2rs = c
problem of §5). For balanced-E_2 detection in *nice* sequences (short intervals, APs), the
Type II requirement with both variables near x^{1/2} is exactly the hard regime; no
published application achieves truly balanced output localization p1 ≍ x^{1/2} in a sparse
sequence. (For the full set of integers, balanced-E_2 counting ("RSA integers") is
elementary — Mertens sums; e.g. Decker–Moree, *Counting RSA integers* — irrelevant depth.)

---

## 7. Consecutive integers with prescribed factorization shapes (beyond Heath-Brown)

- **Consecutive smooth:** R. B. Eggleton, J. L. Selfridge, J. Austral. Math. Soc. A 22
  (1976), 1–11 (strings of length ≤ 5, smoothness n^{ε(n)}, ε(n) ≍ (log log log n)^{−1/2});
  **A. Balog, T. D. Wooley, *On strings of consecutive integers with no large prime
  factors*, J. Austral. Math. Soc. A 64 (1998), 266–276** (zbMATH review verified): for
  every ε > 0 there are **arbitrarily long strings n+1, …, n+t all of whose prime factors
  are ≤ n^ε**, quantitatively with t(n) ≫ log log log log n; moreover the same holds with
  the string replaced by t linear forms a_i n + b_i. Elementary proof. — So the *necessary*
  smoothness condition for S_k windows (all of n+1..n+k being √(2n)-smooth) is abundantly
  satisfiable for every fixed k; what Balog–Wooley gives no hold on is the *shape* (number
  and size of prime factors) of the window elements or the digit conditions: their n's are
  built from factorial/binomial-type constructions, and their window elements are typically
  very far from E_2 (they are extremely smooth). Note PROBLEM.md's ban is on *assuming*
  smooth-window statements **with additional unproved structure**; Balog–Wooley itself is
  proved and citable, but does not by itself certify any S_k membership.
- **Equal-invariant consecutive integers:** Heath-Brown 1984 (d(n) = d(n+1), Erdős–Mirsky;
  via Spiro's d(n) = d(n+5040), 1981); J.-C. Schlage-Puchta (ω(n) = ω(n+1), c. 2003;
  arXiv:1105.1621); Pinner (shifts d(n) = d(n+b), 1997); Buttkewitz (ω, infinite set of
  shifts); **GGPY 0803.2636 + 2003.03661 (J. Number Theory 2021)**: the prescribed-value
  results quoted in §3 (Ω(x) = Ω(x+1) = A for every A ≥ 4; ω-version A ≥ 3; d-version
  24 | A; exponent pattern {2,1,1,1} at x and x+1; versions for arbitrary shifts).
- **Open at the small end:** Ω(x) = Ω(x+1) = 3 ("E_3 + E_3 at consecutive integers" in
  its strongest form) and Ω(x) = Ω(x+1) = 2 (consecutive E_2's) are open; likewise the
  mixed prescriptions (Ω(x), Ω(x+1)) = (2, 3) — the S_2 shape — and any version with
  factor-size constraints. The published frontier for "both Ω-values prescribed" is
  exactly A ≥ 4, and the GGPY constant-multiplier mechanism is why 4 is the limit:
  overcoming parity costs ≥ 2 extra prime factors on each side (multipliers 3, 4, 8, 9…),
  and Ω = A ≥ 4 leaves room for E_2 × multiplier; Ω = 2 or 3 does not.
- **Both n, n+1 with all prime factors large:** from GGPY Theorem 3 applied to {m, 2m−1}:
  infinitely many N with N, N+1 both P_2 up to a factor 2, all odd prime factors
  > N^{1/10} (§1). Combined statements of the form "n, n+1 both with exactly j prime
  factors, all > n^δ" for any j: **not in the literature** for any (j, δ) with j ≤ 3;
  for j ≥ 4 (unlocalized) see GGPY §3.

**Applicability.** (b)/(c) mosaics; see §8.

---

## 8. Synthesis: what each item can and cannot do for Statement B

Statement B = (O1) archimedean windows + (O2) balanced factors + (O3) double exact-parity,
at the specific consecutive pair (2m−1, m). Verdicts:

1. **Heath-Brown 1987 / Hildebrand 1985 / Balog 1985** — (b) *the strongest template*.
   Delivers, with positive density, consecutive integers both √-smooth with largest prime
   factor in a prescribed window (O1+O2 for the *largest* factor, at both positions, no
   parity needed). Missing: primality of cofactors (O3) and small-prime digit control.
   Usable relaxation served: "n+1, n+2 both of the form (smooth a ≤ n^δ)·(prime in
   (n^{1/2−δ}, n^{1/2}))" — *if* the elementary lemma can be re-proved for such patterns
   (new elementary work needed: the current lemma needs exact pq, 2rs).
2. **Chen-type** — (c) directly (prime anchors are forbidden by S_2-smoothness); (b) for
   its localization technology (both P_2 factors > x^{1/10}; anchor localizable to N^{0.95}).
   The open 2p+1-parity branch is the formal witness that O3 is beyond current methods
   even in the easiest configuration.
3. **GGPY E_2-tuples** — (b) with two fatal gaps identified precisely: (i) which-pair
   ambiguity can only be beaten by designing triples all of whose pairs certify S_2 —
   requires a *family* of elementary lemmas (elementary-side research direction); (ii)
   their detector provably (their own (1.24)) lives on unbalanced E_2's, which S_2
   excludes. Best citable relaxations: Theorem 3 on {m, 2m−1} (consecutive P_2·{1,2},
   odd factors > n^{1/10}) — the closest proved statement to Statement B in print; and
   Theorem 2 (two of three forms E_2, factors > n^{1/144}).
4. **Levels of distribution** — (a) for inputs: Motohashi 1976 gives BV level 1/2 for E_2
   (uniform enough for GPY-type weights, tolerant of O1/O2 restrictions on the source
   side); Fouvry–Radziwiłł 2022 pushes past 1/2 only for extremely unbalanced products;
   Drappeau(–Topacogullari) settle Titchmarsh-type averages including Σ τ(pq + a) with
   full expansions. None of this touches O3; no level-of-distribution theorem exists for
   the shifted set {pq + 1} itself beyond what BV-for-E_2 + divisor switching yields on
   average.
5. **pq − 2rs = c** — nothing published (lower bounds); F_p-solvability results certify
   absence of local obstructions only. The equation *is* Statement B minus the archimedean
   conditions; flagging any claimed citation of a lower bound as suspect.
6. **Harman's sieve** — (b): the only framework built to output E_2 with both factors
   localized; its Type II needs are exactly what the sparse parity-defined sequences of
   Statement B lack. Realistic use: balanced-E_2 counts in *auxiliary* sieve-friendly sets
   inside a hybrid elementary/analytic scheme.
7. **Consecutive-shape results** — the proved frontier is: arbitrary-length n^ε-smooth
   strings (Balog–Wooley — necessary conditions abundantly satisfiable); equal prescribed
   Ω ≥ 4 / ω ≥ 3 / d (GGPY); consecutive P_2-up-to-2 with large factors (GGPY Thm 3).
   The S_2 shape (2, 3) with balance sits strictly beyond every one of these, and each
   frontier's position is explained by a structural mechanism (constant-multiplier cost,
   unbalanced detection, parity) — not by lack of effort.

**Bottom line.** No published result implies Statement B or any relaxation of it that the
current elementary lemma can consume; the obstruction profile (O2 + O3 jointly) sits beyond
each individual frontier for an identified structural reason. The most promising *proof
template* in the literature is a hybrid: (α) generalize the elementary lemma from the
single pattern (pq, 2rs) to families tolerant of smooth cofactors ("(a·p, 2b·q), a, b
smooth-small, p, q balanced primes in windows") so that Hildebrand/Heath-Brown
consecutive-large-factor technology (positive density!) or a designed GGPY triple can feed
it; (β) failing that, Statement B's analytic core (§5's equation with balanced variables)
should be treated as a parity²-hard open problem on par with the specified-parity branch
of Chen's theorem, i.e., not currently provable.
