# TOOLBOX.md — Route R8: verified citable forms of classical tools (T1–T8)

Conventions. e(t) = e^{2πi t}. P(n) = largest prime factor of n (P(1)=1). Ψ(x,y) =
#{n ≤ x : P(n) ≤ y}; Ψ_q(x,y) additionally requires (n,q)=1; Ψ(x,y;a,q) additionally
requires n ≡ a (mod q). ρ(u) = Dickman's function; u = log x / log y. All statements below
were checked against the cited sources (PDFs fetched and text-extracted where noted); when a
quote is abbreviated, the omissions are marked […]. Web search was used only for the standard
named results below; nothing touching Erdős 727/728/729 was searched.

Verification method note. Sources verified verbatim from extracted text: Granville's survey
(MSRI copy, pdftotext), Cochrane–Zheng survey (pdftotext), Saffari–Vaughan II (Numdam scan,
pdftotext — OCR noisy but formulas legible), Richert's TIFR lectures (pdftotext),
Ford's sieve notes (pdftotext), /home/user/erdos/references/aristotle728.txt (local).
Weyl's inequality was verified against secondary quotations only (see T3 caveat).

---

## T1. Smooth numbers in a FIXED arithmetic progression

**Target.** Fixed u > 1, fixed q: #{x < n ≤ 2x : P(n) ≤ n^{1/u}, n ≡ a (mod q)}
= (ρ(u)/q + o(1)) x.

**Status: citable-as-needed** (three literature inputs plus a four-line routine reduction;
each input is far stronger than the fixed-q case needs).

**Input 1 (Hildebrand's range for Ψ(x,y) ~ ρ(u)x).** Granville, "Smooth numbers:
computational number theory and beyond", *Algorithmic Number Theory* (MSRI Publications 44,
2008), 267–323, eqs. (1.8)–(1.10), quoting the extracted text:

> "De Bruijn [1951a; 1951b; 1966] showed that
> Ψ(x, y) = xρ(u){1 + O(log(u+1)/log y)}, where x = y^u,   (1.8)
> holds for 1 ≤ u ≤ (log y)^{3/5−ε} […] Hildebrand [1986] improved this substantially to
> the range 1 ≤ u ≤ exp((log y)^{3/5−ε}), that is, y > exp((log log x)^{5/3+ε})." (1.10)

Original: A. Hildebrand, *On the number of positive integers ≤ x and free of prime factors
> y*, J. Number Theory 22 (1986), 289–307. For fixed u this is overkill: any fixed-u form
of Dickman–de Bruijn suffices (e.g. Tenenbaum, *Introduction to Analytic and Probabilistic
Number Theory*, 3rd ed., Thm. III.5.13).

**Input 2 (removing the coprimality weight, fixed q).** Same survey, §4.2 (verbatim from
extracted text):

> "Let Ψ_q(x,y) be the number of integers in S(x,y) that are coprime to q. As one might
> guess, Ψ_q(x,y) ∼ (φ(q)/q) Ψ(x,y) in a very wide range: Tenenbaum [1993] showed this,
> provided there are at most y^{o(1/log u)} prime factors of q that are ≤ y."

For fixed q the hypothesis is trivial (ω(q) = O(1)).

**Input 3 (equidistribution among reduced classes).** Same survey, §4.2, eqs. (4.5)–(4.6)
(verbatim):

> "Let Ψ(x,y;a,q) be the number of integers in S(x,y) that are equivalent to a modulo q. We
> would expect Ψ(x,y;a,q) ∼ (1/φ(q)) Ψ_q(x,y) whenever (a,q) = 1. (4.5)
> I showed that this is true for x ≥ y ≥ q^{1+ε} as (log x)/(log q) → ∞. (4.6)"

Original: A. Granville, *Integers, without large prime factors, in arithmetic progressions
I*, Acta Math. 170 (1993), 255–273; *II*, Philos. Trans. Roy. Soc. London Ser. A 345 (1993),
349–362. (Much stronger uniform ranges exist — Harman 1999 for q cube-free, y > q^{1/(4√e)+ε};
Soundararajan, *The distribution of smooth numbers in arithmetic progressions*
(arXiv:0707.0299), q < y^{4√e−ε} — but fixed q needs none of this.)

**Assembly to the target form (routine, do inline).** Fix u > 1, q, a.
(i) For (a,q) = 1: by Inputs 3, 2, 1, #{n ≤ x : P(n) ≤ y, n ≡ a (q)} =
(1/φ(q))·(φ(q)/q)·ρ(u)x·(1+o(1)) = (ρ(u)/q + o(1))x with y = x^{1/u}.
(ii) For g = (a,q) > 1: n ≡ a (q) forces n = g·m with m ≡ a/g (mod q/g), (a/g, q/g) = 1, and
for y > g (all large x) n is y-smooth iff m is; apply (i) at modulus q/g and length x/g;
since log(x/g)/log y → u, the count is again (ρ(u)/q + o(1))x.
(iii) Dyadic window and the varying threshold n^{1/u}: for x < n ≤ 2x one has
x^{1/u} ≤ n^{1/u} ≤ (2x)^{1/u}; sandwiching between the two fixed thresholds and using
continuity of ρ gives #{x < n ≤ 2x : P(n) ≤ n^{1/u}, n ≡ a (q)} = (ρ(u)/q + o(1))x.
(All three steps are standard; no uniformity in q is claimed or needed.)

---

## T2. Equidistribution of {N/p} (and jointly {N/p}, {N/p^2}, …), p ∈ [P, 2P], N ≍ P^c, 1 < c < 4

**Status: single sequence {N/p}: citable-as-needed with o(1) discrepancy (not power-saving);
power-saving discrepancy and the JOINT version: must-prove-inline from citable components.**

**Literature theorem (single sequence, primes).** B. Saffari and R. C. Vaughan, *On the
fractional parts of x/n and related sequences. II*, Ann. Inst. Fourier (Grenoble) 27, no. 2
(1977), 1–30. With c_α(t) := 1 if {t} ≤ α, else 0, and
Θ*_{x,y}(α) := y^{−1} Σ_{p ≤ y} (log p) c_α(x/p)  (their (1.27)),

> **Theorem 10.** "Suppose that ε > 0 and x^{1/6+ε} < y ≤ x. Then
> Θ*_{x,y}(α) = F(α, x/y) + O( exp(−C(ε) (log x)^{1/3}) )  (1.28)
> where C(ε) is a positive number depending at most on ε."

Here F(α, ξ) is their limiting distribution function ((1.2)–(1.4) of the paper, defined in
part I, Ann. Inst. Fourier 26 (1976), no. 4, 115–131); its deviation from uniformity is
quantified by their Corollary 1.3 (for the integer version):

> **Corollary 1.3.** "Suppose that y/x → 0 as x → ∞. Then
> Θ_{x,y}(α) = α + O( y x^{−1} + x^{1/3} y^{−1} log x )."  (1.11)

i.e. F(α, ξ) = α + O(1/ξ) uniformly in α. (The paper also proves, Theorem 1, the integer-n
version Θ_{x,y}(α) = F(α, x/y) + O(x^{1/3} y^{−1} log x) for all 1 ≤ y < x.)

**Deduction for the brief's setting (short inline computation).** Take x = N, y = 2P and
y = P and difference; then partial summation removes the log p weight. Hypotheses: N ≍ P^c
with 1 < c < 4 gives P > N^{1/4} > N^{1/6+ε} (so Theorem 10 applies at both endpoints) and
x/y ≍ P^{c−1} → ∞ (so F(α, x/y) = α + O(P^{1−c})). Conclusion:
  #{p ∈ (P, 2P] : {N/p} ≤ α} = α·π_{(P,2P]} + O( P·exp(−C(c)(log P)^{1/3}) + P^{2−c} )·(1/log P adjustments),
uniformly in α — an equidistribution statement with discrepancy O(exp(−C'(log P)^{1/3}))
relative to π(2P)−π(P). This is o(1) but NOT a power saving.

**What the literature does NOT give.** (a) A power-saving discrepancy for {N/p} over primes
(Saffari–Vaughan's prime error term is zero-density-driven; they note that on the density
hypothesis 1/6 improves to 1/11 — irrelevant here, and still not power-saving). (b) Anything
about the joint vector ({N/p}, {N/p^2}, …). Both must be proved inline if needed. The proof
is standard machinery with fully citable components:

- **Erdős–Turán inequality** (discrepancy from exponential sums): Kuipers & Niederreiter,
  *Uniform Distribution of Sequences*, Wiley 1974, Ch. 2, Thm. 2.5: there is an absolute
  constant C with D_M ≤ C( 1/H + Σ_{h=1}^{H} (1/h) |Σ_{m≤M} e(h x_m)| / M ) for every
  H ≥ 1. Multidimensional version (Erdős–Turán–Koksma): Drmota & Tichy, *Sequences,
  Discrepancies and Applications*, LNM 1651, Thm. 1.21 — needed for the joint version, with
  phases h₁N/p + h₂N/p² + ….
- **van der Corput derivative tests**: Graham & Kolesnik, *Van der Corput's Method of
  Exponential Sums*, LMS Lecture Notes 126, 1991. Second-derivative test (their Thm. 2.2):
  if f is real on [a,b] ⊂ [P,2P] with λ₂ ≤ f''(x) ≤ hλ₂ then Σ_{a<n≤b} e(f(n)) ≪
  h(b−a)λ₂^{1/2} + λ₂^{−1/2}. Third-derivative test (their Thm. 2.6): with λ₃ ≤ |f'''| ≤ hλ₃,
  Σ ≪ h(b−a)λ₃^{1/6} + (b−a)^{1/2} λ₃^{−1/6}. For f(x) = hN/x: λ₂ ≍ hN/P³ (nontrivial for
  1+ε < c < 3−ε), λ₃ ≍ hN/P⁴ (nontrivial for 1+ε < c < 4−ε); together these give
  power-saving bounds for the integer sums Σ_{n~P} e(hN/n) throughout 1+ε ≤ c ≤ 4−ε.
- **Vaughan's identity** to pass to primes: Davenport, *Multiplicative Number Theory*, 3rd
  ed., Ch. 24; type-I sums handled by the tests above, type-II bilinear sums by
  Cauchy–Schwarz + a Weyl shift exactly as in the Piatetski-Shapiro prime number theorem
  treatment (Graham–Kolesnik Ch. 4–5, or G. Harman, *Prime-Detecting Sieves*, Ch. 3). This
  yields power savings for c in a subrange of (1,4) determined by the type-II ranges; a
  full-range (1,4) power-saving prime result should NOT be assumed without doing the
  bilinear bookkeeping. If only o(1) discrepancy is needed, cite Saffari–Vaughan alone.

---

## T3. Weyl-sum equidistribution for v ↦ v⁴, modulus Q = p^t ≤ V^{4−δ}

**Status: citable-by-combination** (two exact literature inputs; the stated target follows
with c(δ) = δ/8 − ε; no single off-the-shelf theorem says it in one line).

**Input 1 (Weyl's inequality).** R. C. Vaughan, *The Hardy–Littlewood Method*, 2nd ed.,
Cambridge Tracts 125, 1997, Lemma 2.4: if f(x) = αx^k + α_{k−1}x^{k−1} + … + α₀ with real
coefficients, (a,q) = 1 and |α − a/q| ≤ q^{−2}, then
  Σ_{x=1}^{X} e(f(x)) ≪ X^{1+ε} ( q^{−1} + X^{−1} + q X^{−k} )^{2^{1−k}},
the implicit constant depending only on k and ε. [Caveat: verified against standard
secondary quotations (e.g. Wikipedia "Weyl's inequality (number theory)" and multiple
arXiv papers quoting Vaughan Lemma 2.4), not against the book's page image; the form above
is the universally quoted one. Lower-order coefficients are unrestricted, so the sum may be
taken over any interval of length V by shifting.]

Application with k = 4, α = a/Q exactly, (a,Q) = 1, Q = p^t: for v over an interval of
length V, |Σ_v e(a v⁴/Q)| ≪_ε V^{1+ε} (Q^{−1} + V^{−1} + Q V^{−4})^{1/8}. If
V^δ ≤ Q ≤ V^{4−δ} this is ≪ V^{1−δ/8+ε}: a power saving c(δ) = δ/8 − ε.

**Input 2 (small Q, via complete sums = T4).** If Q ≤ V^δ (where Input 1 saves nothing),
split the interval into ⌊V/Q⌋ complete blocks plus one incomplete block. Complete blocks:
use T4 below, |S(av⁴, Q)| ≤ 4.41·Q^{3/4}. Incomplete block: standard completion
(finite Fourier expansion) reduces to sums Σ_{z mod Q} e((a z⁴ + b z)/Q), each of which is a
degree-4 nonconstant polynomial mod p, so again ≤ 4.41·Q^{3/4} by T4/Cochrane–Zheng
(their bound holds for arbitrary nonconstant f mod p); total ≪ Q^{3/4} log Q. Hence
  |Σ_{v ∈ I, |I| = V} e(a v⁴/Q)| ≤ 4.41·V·Q^{−1/4} + O(Q^{3/4} log Q),
a power saving for all Q ∈ [V^{δ'}, V^{4/3}] — overlapping Input 1's range. Combined: for
every δ > 0 there is c(δ) > 0 with |Σ_{v~V} e(a v⁴/Q)| ≪ V^{1−c(δ)} for all p^t = Q ∈
[V^δ, V^{4−δ}], (a, p) = 1. Note the gcd hypothesis needed is (a, p) = 1 (equivalently
p ∤ a); for general a write a/Q in lowest terms and rescale Q.

Digit-cylinder equidistribution of v⁴ mod p^t follows from these bounds by Erdős–Turán
(T2 components) or directly by completing characteristic functions of cylinders — cylinders
of p-adic depth r are unions of arithmetic progressions mod p^r, handled by the same sums
with Q replaced by p^r, r ≤ t. Routine assembly; do inline.

---

## T4. Complete exponential sums mod p^L (quartic)

**Target.** |Σ_{z mod p^L} e(a z⁴/p^L)| ≤ C·p^{3L/4} for p odd, p ∤ a.

**Status: citable-as-needed, with explicit constants, and stronger than the target
(includes p = 2).**

Source: T. Cochrane and Z. Zheng, *A survey on pure and mixed exponential sums modulo prime
powers*, in Number Theory for the Millennium I (Proc. Millennial Conf., Urbana 2000),
quoting the extracted text of §3 verbatim:

> "Hua [30], [31], [32] established the following uniform upper bound on exponential sums:
> For any nonconstant polynomial f (mod p) of degree d and any prime power p^m with m ≥ 1,
> |S(f, p^m)| ≤ c₁(d) p^{m(1−1/d)}, (3.1) with c₁(d) = d³. In view of the preceding
> example, the exponent here is best possible […] In [14] we established that one may take
> c₁(d) = 4.41, including the case p = 2."

Here S(f, p^m) = Σ_{x mod p^m} e(f(x)/p^m), and [14] = T. Cochrane and Z. Zheng, *On upper
bounds of Chalk and Hua for exponential sums*, Proc. Amer. Math. Soc. 129 (2001), 2505–2516.
Also from the same section: "Nec̆aev and Topunov [74] determined the best possible constant
to be […] 2.263 for polynomials of degree 4", and c₁(d) = 1 is admissible when
p > (d−1)^{2d/(d−2)} (for d = 4: p > 3⁴ = 81, i.e. p ≥ 83). For m = 1 Weil's bound
(their (4.1)) gives |S(f, p)| ≤ (d−1)√p = 3√p for d = 4, valid for every p with f
nonconstant mod p.

**Specialization to the target.** f(z) = a z⁴ with p ∤ a is nonconstant mod p of degree 4
(all p, including p = 2), so
  |Σ_{z mod p^L} e(a z⁴/p^L)| ≤ 4.41 · p^{3L/4}   for ALL primes p and ALL L ≥ 1;
constant 2.263 admissible (Nec̆aev–Topunov), and 1 for p ≥ 83; and 3·p^{1/2} for L = 1.
Original sources: L.-K. Hua, *On exponential sums*, J. Chinese Math. Soc. 20 (1940),
301–312 (d³, all m ≥ 1); the exact Hardy–Littlewood evaluation S(Az^d, p^m) = p^{m(1−1/d)}
when d | m, p ∤ A shows the exponent 3L/4 cannot be improved.

---

## T5. Sieve upper bound for primes of the form (z²+1)/a, uniform in a

**Target.** For a ≤ x^{1−δ} with z² ≡ −1 (mod a) solvable, z₀ a fixed root:
#{z ≤ x : z ≡ z₀ (mod a), (z²+1)/a prime} ≤ C·(expected order), C explicit, uniform in a.

**Status: weaker-than-needed as a single quotable theorem; the axiom-level sieve theorem IS
in the literature with full uniformity, and yields C = 2 + o(1) after a short inline
verification of the axioms for this family.** (The brief's "any explicit constant, e.g.
4+o(1)" is met with room to spare.)

**Literature theorem (fully uniform given the axioms).** H.-E. Richert, *Lectures on Sieve
Methods*, Tata Institute Lectures 55, 1976, Theorem 11.4 (equivalently Halberstam–Richert,
*Sieve Methods*, Academic Press 1974, Theorems 5.1–5.2), quoting the extracted text:

> "**Theorem 11.4.** (Ω₁), (Ω₂(κ, L)), (R):
> S(A, 𝔭, z) ≤ Γ(κ+1) ∏_p {(1 − ω(p)/p)(1 − 1/p)^{−κ}} · X/log^κ z ·
> {1 + O((log log 3z + L)/log z)}   if z ≤ X^{1/2},  (11.12)
> where the infinite product converges and the O-constant depends at most on A₁, A₂ and κ."

Axioms (same source): (Ω₁): 0 ≤ ω(p)/p ≤ 1 − 1/A₁; (Ω₂(κ,L)): −L ≤
Σ_{w≤p<z} ω(p) log p / p − κ log(z/w) ≤ A₂ for 2 ≤ w ≤ z; (R): |R_d| ≤ ω(d) for
squarefree d, where A_d = (ω(d)/d)X + R_d. The crucial point for uniformity: the error
depends ONLY on A₁, A₂, κ — the sifted sequence (hence the polynomial's coefficients)
enters only through the axioms.

**Inline verification for this family (short, must be done in the writeup; not itself in
the literature).** Sift A = {F_a(t) : 1 ≤ t ≤ T}, T = x/a, where F_a(t) = ((z₀+at)²+1)/a =
a t² + 2 z₀ t + (z₀²+1)/a ∈ Z[t]. ω(p) = ρ_{F_a}(p) = #{t mod p : F_a(t) ≡ 0}. For
p ∤ 2a: ρ = 1 + χ₋₄(p) ≤ 2. For p | 2a: ρ ≤ 2 as well (linear or constant congruence;
degenerate p contribute ρ ∈ {0,1,p}-checks — p with ρ(p) = p cannot occur since F_a has
content 1 and a solvable root structure; verify when writing). (Ω₁) holds with A₁ = 3 say
(ρ(p) ≤ 2 < p for p ≥ 5; p = 2, 3 checked by hand). (Ω₂(1, L)): Σ_{p≤t} χ₋₄(p) log p/p =
O(1) by PNT for the FIXED character χ₋₄ (no uniformity issue), and the primes p | 2a
perturb the sum by ≤ Σ_{p|2a} 2 log p/p ≪ log log(3a); so L ≪ log log x uniformly for
a ≤ x. (R) holds since #{t ≤ T : d | F_a(t)} = (ρ(d)/d)T + O(ρ(d)). Then Theorem 11.4 with
κ = 1, z = T^{1/2} = (x/a)^{1/2} gives, uniformly for a ≤ x^{1−δ} (which guarantees
T ≥ x^δ, so log z ≍ log x and the o(1) is uniform):
  #{z ≤ x : z ≡ z₀ (a), (z²+1)/a prime}
    ≤ #{t ≤ T : F_a(t) has no prime factor < T^{1/2}} + O(T^{1/2})
    ≤ (2 + o(1)) · S(F_a) · T / log T,   S(F_a) := ∏_p (1 − ρ_{F_a}(p)/p)(1 − 1/p)^{−1},
using that (z²+1)/a ≥ x²/a·(1/2) > T^{1/2} makes prime values unsifted. Relative to the
heuristic count S(F_a)·T/log(x²/a) this is C_sieve = (2+o(1))·log(x²/a)/log(x/a) ∈
[2+o(1), 4/(1)-ish] depending on normalization; against the brief's natural normalization
T/log T the constant is **2 + o(1)**, uniform in a ≤ x^{1−δ}. (Brun–Titchmarsh for
reference, fully uniform, dimension 1, no o(1): Montgomery–Vaughan, *The large sieve*,
Mathematika 20 (1973), Theorem 2: π(x; q, ℓ) ≤ 2x/(φ(q) log(x/q)) for all x > q.)

**Plain statement of the gap.** No published theorem was found that states the (z²+1)/a
bound with uniformity in a as a self-contained result; the uniformity is genuinely in the
literature only at the axiom level (Theorem 11.4 above / H–R Thm 5.2, and the Fundamental
Lemma: K. Ford, sieve lecture notes, Theorem 3.6(b), whose error depends only on κ₀, B₀).
Hooley's work on P(n²+1) (Acta Math. 117 (1967), 281–299) carries out equivalent uniform
sieve estimates for this very family and can be cited for precedent, but quote the axiom
theorem + inline verification, not Hooley's intermediate lemmas.

---

## T6. Average of ρ₂(a) = #{t mod a : t² ≡ −1 (mod a)}

**Status: must-prove-inline (two-line classical computation); constant identified and
numerically verified; framework citable.**

Multiplicativity (CRT + Hensel): ρ₂(2) = 1, ρ₂(2^e) = 0 for e ≥ 2; ρ₂(p^e) = 2 for
p ≡ 1 (mod 4), e ≥ 1; ρ₂(p^e) = 0 for p ≡ 3 (mod 4). Dirichlet series (checked Euler
factor by Euler factor, including p = 2):
  Σ_{a≥1} ρ₂(a) a^{−s} = ζ(s) L(s, χ₋₄) / ζ(2s),
where ζ(s)L(s,χ₋₄) = ζ_{Q(i)}(s) (Landau; e.g. Landau, *Algebraische Zahlen*, or any
algebraic number theory text). Since ρ₂ = 1 * g with Σ |g(n)| n^{−σ} < ∞ for σ > 1/2
(g = coefficients of L(s,χ₋₄)/ζ(2s)), the hyperbola method gives immediately
  Σ_{a ≤ x} ρ₂(a) = (L(1,χ₋₄)/ζ(2)) x + O(x^{1/2+ε}) = **(3/(2π)) x** + O(x^{1/2+ε}),
and by partial summation (or directly)
  Σ_{A < a ≤ 2A} ρ₂(a)/a = (3/(2π)) log 2 + O(A^{−1/2+ε}).
Numerical check (this session, sieve to 2·10⁶): Σ_{a≤x}ρ₂(a)/x = 0.47746 at x = 2·10⁶ vs
3/(2π) = 0.477465; Σ_{5·10⁵<a≤10⁶} ρ₂(a)/a = 0.330917 vs (3/(2π))log 2 = 0.330953. ✓

Caution for consumers: the constant is 3/(2π) ≈ 0.4775, NOT 3/π; and ρ₂(a) = 0 whenever
4 | a or some p ≡ 3 (4) divides a, so ρ₂ is 0 on a positive density set while averaging to
3/(2π) — do not model ρ₂ as ≈ 1/2 pointwise. If a citation is preferred over the two-line
proof: the general theorem "Σ_{n≤x} ρ_f(n) ∼ c_f x for irreducible f" is classical via
Landau's prime ideal theorem; for f = t²+1 it appears in the literature around Hooley's
P(n²+1) work (Acta Math. 117 (1967)), but the inline proof is shorter than the citation
chase and is recommended.

---

## T7. Dickman distribution of large prime factors; prime factors in a dyadic power window

**Status: citable-as-needed for the integer statements (with one flagged restriction);
quadratic-value analogues are unconditional only as first moments / sieve upper bounds.**

(a) **Largest prime factor.** From T1-Input 1 (de Bruijn/Hildebrand, Granville survey
(1.8)/(1.10)): (1/x)#{n ≤ x : P(n) > n^β} → 1 − ρ(1/β) for fixed β ∈ (0,1) (sandwich
n^β between x^β(1+o(1)) as in T1(iii)). ρ satisfies ρ(u) = 1 − ∫_1^u ρ(v−1) dv/v
(Tenenbaum, 3rd ed., §III.5). **Restriction:** 1 − ρ(1/β) = log(1/β) ONLY for
1/2 ≤ β ≤ 1 (where ρ(u) = 1 − log u, 1 ≤ u ≤ 2). For β < 1/2 the stated
"→ log(1/β)" form is FALSE (log(1/β) > 1 for β < 1/e, while the left side is ≤ 1);
the correct limit is always 1 − ρ(1/β). Flag any use with β < 1/2.

(b) **Expected number of prime factors in (n^{b₁}, n^{b₂}), 0 < b₁ < b₂ ≤ 1.** Unconditional
identity: Σ_{n≤x} #{p | n : x^{b₁} < p ≤ x^{b₂}} = Σ_{x^{b₁}<p≤x^{b₂}} ⌊x/p⌋ =
x(log(b₂/b₁) + o(1)), by Mertens (Σ_{p≤t} 1/p = log log t + M + O(1/log t); Tenenbaum,
3rd ed., Thm. I.1.10; Rosser–Schoenfeld for explicit constants). The n^{b_i} vs x^{b_i}
threshold change is again a sandwich. Second moments and Poissonian refinements exist
(Erdős–Kac framework) but are not needed for upper-bound uses.

(c) **Shifted/quadratic values (z²+1): what is unconditional.**
  - First moment (elementary, unconditional): Σ_{z≤x} #{p | z²+1 : p > x^θ} =
    Σ_{p>x^θ} ρ₂(p)⌊x/p⌋ + O(x^{o(1)}) and ρ₂(p) = 1 + χ₋₄(p), so by Mertens in
    arithmetic progressions this is x·(log(2/θ) + o(1)) for fixed 0 < θ < 2 (primes
    p ≤ x²+1 can divide z²+1). Pure counting; no sieve.
  - Upper bounds on the number of z with (z²+1)/a prime (a in dyadic ranges): T5 gives
    (2+o(1))-constant sieve bounds uniformly for a ≤ x^{1−δ}; summing over a with the
    ρ₂-averages of T6 gives unconditional upper bounds of the expected order for counts
    like #{z ≤ x : P(z²+1) > x^{2−η}}. This T5+T6 pattern is exactly Hooley's (Acta Math.
    117 (1967)) and is unconditional.
  - NOT unconditional / open: any matching lower bounds or asymptotics for P(z²+1) beyond
    infinitude results (Hooley: P(z²+1) > z^{11/10} i.o.; Deshouillers–Iwaniec: z^{θ},
    θ = 1.202…; Merikoski 2023: θ = 1.279); Dickman-type limiting distributions for
    P(z²+1). Do not import these as if analogous to (a).

---

## T8. Carry/digit Markov chain for doubling in base p: large deviations

**Status: confirmed in the licensed local reference; short and re-provable inline (recommend
re-prove or quote with the caveat below).**

Source: /home/user/erdos/references/aristotle728.txt (= arXiv 2601.07421, Erdős-728
writeup), Appendix "effective bounds", Lemma 15, verified verbatim from the local copy:

> **Lemma 15 (Carry chain).** "Let p be a prime and L ≥ 1. Let m be uniform in
> {0, 1, …, p^L − 1}. Write m = Σ_{i=0}^{L−1} a_i p^i, a_i ∈ {0,…,p−1}, and define carries
> (C_i) ⊂ {0,1} by C₀ := 0 and C_{i+1} := 1{2a_i + C_i ≥ p}. Set S_L := Σ_{i=1}^{L} C_i.
> For λ ∈ R define the tilted matrix T_p(λ) := (P_p(u,v) e^{λv})_{u,v∈{0,1}}, where P_p is
> the transition matrix of the carry chain (C_i). Let ρ_p(λ) be the Perron–Frobenius
> eigenvalue of T_p(λ).
> 1. E[e^{λS_L}] = e₀ᵀ T_p(λ)^L 1 […] there is C_p(λ) > 0, not depending on L, with
>    E[e^{λS_L}] ≤ C_p(λ) ρ_p(λ)^L; for each fixed λ, sup_{p≥p₁(λ)} C_p(λ) =: C(λ) < ∞.
> 2. For any s ∈ (0,1) and λ < 0: P(S_L ≤ sL) ≤ C_p(λ) exp( L(log ρ_p(λ) − λs) ).
> 3. Fix δ ∈ (0,1), ε > 0, set s := (1−δ)/2 and I(δ) := D((1−δ)/2 ‖ 1/2) =
>    (1/2)[(1−δ)log(1−δ) + (1+δ)log(1+δ)]. Then there exist p₀ = p₀(δ,ε) and C(δ) > 0 such
>    that for all primes p ≥ p₀ and all L ≥ 1: P(S_L ≤ sL) ≤ C(δ) exp(−(I(δ) − ε)L).
> 4. For each fixed prime p and each δ ∈ (0,1) there exist γ_p(δ) > 0 and C_p(δ) > 0 such
>    that for all L ≥ 1: P(S_L ≤ sL) ≤ C_p(δ) e^{−γ_p(δ)L}."

And from its proof (verified in the file): "Conditioning on C_i and using that a_i is
uniform gives the two-state Markov chain. For p ≥ 3,
P_p = ( (1/2 + 1/(2p), 1/2 − 1/(2p)) ; (1/2 − 1/(2p), 1/2 + 1/(2p)) ),
and for p = 2 the carries are independent so both rows equal (1/2, 1/2)."
This is EXACTLY the transition matrix stated in the brief. The stationary distribution is
(1/2, 1/2); Λ_p(λ) = log ρ_p(λ) is convex with Λ_p(0)=0, Λ_p'(0)=1/2 (their step (4)),
giving the standard tilting large-deviation bound.

**Caveats.** (i) Publication status: this is an appendix of an arXiv preprint, drafted with
LLM assistance per the text ("The following result was derived in a conversation with
ChatGPT… edited and checked by the author"); the brief licenses its methods, but for a
self-contained writeup the lemma is 1 page of standard Perron–Frobenius/Chernoff and should
simply be re-proved inline. (ii) No other published reference stating precisely this carry
chain with these constants was searched for or found beyond the generic large-deviation
literature (Dembo–Zeitouni, Thm. 3.1.2, finite-state Markov additive processes — citable
for the general principle). (iii) Note the chain is for a UNIFORM digit string of fixed
length L; applications to m in an interval [M, 2M] need the boundary-digit correction
already carried out in the reference (their Lemma 11 pattern: count ≤ (M+1)·P(bad) + 2p^L).

---

## Summary table

| Item | Status | Key citation | Note |
|------|--------|--------------|------|
| T1 | citable-as-needed | Granville MSRI survey (1.8),(1.10),§4.2 (4.5)-(4.6); Hildebrand 1986; Granville Acta Math. 170 (1993) | fixed q trivial case; 4-line reduction for gcd>1 + threshold sandwich |
| T2 | citable (o(1) disc.) / must-prove-inline (power saving; joint) | Saffari–Vaughan II, Ann. Inst. Fourier 27 (1977), Thm 10, Cor 1.3 | prime range x^{1/6+ε} < y ≤ x covers all 1<c<4; joint version nowhere in literature |
| T3 | citable-by-combination | Vaughan HL Method Lemma 2.4 + T4 | saving c(δ)=δ/8−ε on V^δ ≤ Q ≤ V^{4−δ}; assembly inline |
| T4 | citable-as-needed | Hua 1940 (c=d³); Cochrane–Zheng PAMS 129 (2001): c=4.41 all p,m | 4.41·p^{3L/4}; 2.263 (NT); 1 for p≥83; 3√p for L=1 |
| T5 | axiom-level uniform + inline verification | Richert TIFR Lectures Thm 11.4 (=H–R Thms 5.1–5.2) | C = 2+o(1) uniform for a ≤ x^{1−δ}; no self-contained published statement |
| T6 | must-prove-inline (2 lines) | ζL(χ₋₄)/ζ(2s) factorization (Landau) | c = 3/(2π) ≈ 0.4775, numerically verified; dyadic version (3/(2π))log 2 |
| T7 | citable-as-needed (integers); first-moment/sieve only (quadratic) | Granville survey; Tenenbaum I.1.10, III.5; Hooley Acta Math. 117 | WARNING: log(1/β) form valid only for β ∈ [1/2,1] |
| T8 | confirmed in licensed reference; re-prove inline | aristotle728.txt Lemma 15 (arXiv 2601.07421 appendix) | transition matrix matches brief exactly; 1-page standard proof |
