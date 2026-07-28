# AUDIT_SP.md — adversarial audit of `attempts/route-R2/LEMMA_SP.md`

Auditor: independent adversarial pass. Inputs read: `PROBLEM.md`, `attempts/route-R2/LEMMA_SP.md`
(and, only as a claim to be checked, the tail of `verify_sp.out`). **No** other attempt file,
`NOTES.md`, or `ROUTES.md` was read. All numerical claims below were re-derived with scripts
written from scratch for this audit:

`audit_sp_1.py` (SP.0–SP.3 + PROBLEM.md data), `audit_sp_2.py` (SP.6–SP.9 + scalars),
`audit_sp_4.py` (Section 7–8 prose numbers), `audit_sp_6.py` (corollary algebra, testability),
`audit_sp_8.py` (remaining PROBLEM.md counts), `audit_sp_9.py` (end-to-end at (H1)–(H4)-compliant
`M`), `audit_sp_10.py` (exact spike counts + exhaustive counting bounds), `audit_sp_11.py`
(broad sweep). Outputs: `audit6.out`, `audit8.out`, `audit9.out`, `audit10.out`, `audit11.out`;
`audit_sp_1/2` print to stdout. (`audit_sp_3.py`, `audit_sp_5.py`, `audit_sp_7.py` were earlier,
slower drafts superseded by 9/10/11 — kept for transparency.)

---

## VERDICT: **PASS — with (cosmetic) repairs**

Every **theorem** in LEMMA_SP.md — SP.0, SP.K, SP.1, SP.2, SP.3, SP.4, SP.5, SP.6, SP.7, SP.8,
SP.9, the Master Lemma parts (1)(2)(3), and Corollaries SP-A/SP-B/SP-C — is **true as stated**,
and every **load-bearing** step of every proof is correct. I recomputed each identity from
scratch, re-derived each constant by hand, and hunted for counterexamples exhaustively and by
exact computation at astronomically large `M`. **I found no fatal error and no false theorem.**
The document is also honest about its scope: Remark 7.1 states explicitly that only primes
`p ≤ P(M)` are handled and that nothing here touches the `p ∈ (√(2n), n+k]` regime.

Three *non*-load-bearing assertions are wrong (R1: a `⟺` threshold in a hypothesis check whose
correct value is `60`, not `80`, and which is over-satisfied either way; R2 and R3: two
illustrative numbers in the discussion remarks). None is used to derive anything.

The repairs listed below are all in *prose/illustrative* text (Section 6 hypothesis-check
bookkeeping, Remark 7.2, Section 8 commentary) and in how the numerical certificate is
described. None of them touches a proof.

**Scope warning that must accompany any downstream use** (already stated in the document, but
worth restating loudly): LEMMA_SP proves **nothing about problem 727**. It supplies a
density-1 statement for the criterion at primes `p ≤ exp(√(log M)/6)`. The 727 criterion at
the primes in `(exp(√log M/6), n+k]` — in particular the smooth-window regime that PROBLEM.md
flags, and which PROBLEM.md lists under "reductions to unproved statements of comparable
strength" — is entirely untouched. The header line "Status: **proved in full**" is true of the
*lemma* and must never be quoted as a status for the route or the problem.

---

## 1. Fatal errors

**None found.**

Specifically, all of the following adversarial hypotheses were tested and *refuted*:

| Suspected fault | Result |
|---|---|
| SP.0 identity wrong / off by `ν_p((2k)!)` | Correct; `(2m)! = (2n)!·∏_{i<2k}(2m−i)` since `2n = 2m−2k`. Verified on 4000 random `(k,m,p)` and at the boundary `m=k` (`n=0`). |
| statement not literally about `((n+k)!)² | (2n)!` | It is: SP.0 converts `κ_p ≥ W_p` into `ν_p((2n)!) ≥ 2ν_p((n+k)!)`; my four independent implementations (raw factorials, Legendre, digit-sums, product form) agree, and reproduce **all four** PROBLEM.md sanity datasets (`S_1` prefix + count 40; `S_2` min 208, first 20, count 1981 to 2·10⁵; `S_3` prefix + count 41; `S_4∩[1,6·10⁴]={8174,51984}`). |
| quantifier inversion (`p` chosen before `m`) | No. `G` is defined by conditions imposed *for every* `p ≤ P`; a single `m ∈ G` beats every `p ≤ P` simultaneously. `k` is fixed first and enters only through (H1),(H4); `Ê` is `k`-free. |
| `2k`-deficit dropped or mis-signed | No. The deficit is exactly the bulk term `ν_p((2k)!) = (2k−s_p(2k))/(p−1)` in SP.2/SP.4, and it is what forces the `60·2k` in (H4). I verified `W_p(m) = ν_p(binom(2m,2k)) + ν_p((2k)!)` exactly, matching PROBLEM.md's carries-vs-borrows form. |
| SP.2 inequality direction / boundary `V < J_p`, `V = 0`, `p > 2k`, `p = 2k` | All correct. Exhaustive check `k ≤ 8`, `p < 40`, `m < 3000`: zero violations; 6000 random large instances: zero violations (tight in 82% of them). |
| SP.3 fails when the incoming carry is 0 | No: `a_j ≥ ⌈p/2⌉ ⟹ 2a_j ≥ p`, carry is forced *regardless* of `c_{j−1}`. Verified on 6000 random `(m,p,e,L)`. |
| `p = 2` mishandled (`s_2(2m)=s_2(m)`, `⌈2/2⌉=1`, odd `i` in SP.5, `T_2−1` shift) | All correct. `κ_2 = s_2` verified for all `m < 5000`; the `p=2` branch of the spike count (`i=2i'`, one class mod `q0·2^{J_2+t+1}`, `k` values of `i'`, `k < 2^{J_2+1}`) is right and its `+k` is generously rounded to `+2k`. |
| `p | q0` (masked low digits) mishandled | No. SP.7's consequence is exactly right: the digits of `m` in positions `0..e_p−1` are pinned by `a mod p^{e_p}`, and each free pattern on `[e_p, L_p)` is **one** class mod `q0 p^{L_p−e_p}`. Verified by brute force over 2000 `(q0,p,a,Λ)` configurations. |
| `ν_p(2q0)` spike correction wrong or unnecessary | Correct and necessary. `ν_2(2m) = 1+ν_2(m) ≥ 11` on `m ≡ 0 (mod 2^{10})`, so the uncorrected bound is genuinely false in APs; the corrected one gives measured spike-failure rate 0.0440 there (`k=3, P₀=13, t=3, M=10⁶`) — I reproduce 0.0440 exactly. |
| Chernoff constant `1/8` too aggressive | Correct. `(1−log 2)/2 = 0.15343 > 1/8`. Exact rational tail counts for `p ∈ {2,3,5,7,11,13,17,101}`, `Λ = 1..59`: worst ratio (true count)/(bound) `= 0.695 < 1`. |
| counting boundary term `π(P)p^{L_p}` vs `M/q0` mishandled | Correct. `p^{Λ_p} ≤ p^{L_p} ≤ M^{4/5}`, and `2q₀PM^{4/5}/(M+1) ≤ 2M^{−1/20}` using `q₀ ≤ M^{1/10}`, `P ≤ M^{1/20}`; `4kq₀P/(M+1) ≤ 4kM^{−17/20} ≤ M^{−1/20}` using `4k ≤ M^{4/5}` from (H1). |
| SP.9 arithmetic (`7/60−1/10=1/60`, `θ ≥ 1/3`, `ν_p((2k)!) ≤ 2k−1`, `J_p ≤ log₂ 2k`, floors) | All correct; I re-derived it independently. Exact-`Fraction` verification at **1775** `(k,P,q₀,p)` points with `(H4)` satisfied as tightly as the construction allows: zero failures, minimum margin `70.3`. |
| union-bound assembly `Ê` mis-assembled | Correct. `Σ_{n≥2} n^{−t} ≤ 3·2^{−t}` for `t ≥ 3` (checked to `t=40`, and the prime version too); `2e^{1/24} = 2.0851 < 3`; the three surviving terms are exactly `3P e^{−(7/240)log M/log P} + 6·2^{−t} + 3M^{−1/20}`. |
| SP-A/SP-B/SP-C hypothesis derivations wrong | The (H1)–(H4) checks and the error algebra hold at every point I could construct: for SP-A over `k ∈ {2,3,10,10³,10⁶}`, `c ∈ {1/6,0.1,0.05,0.01,10⁻⁴}` and `log M ∈ [log M_A, 10⁶·log M_A]`, and for SP-B over `k` as above and `P₀ ∈ {2,3,13,10³,10⁶,10¹²}`: **0 failures** (the `P<2` cases the document declares vacuous are indeed vacuous — no primes `≤ P`). `c − 7/(240c) ≤ −1/120` with equality at `c=1/6` confirmed. |
| circularity / smuggled unproved auxiliary | None. Only Legendre's formula is imported as background; Kummer (SP.K) and the Chernoff bound (SP.8) are proved in place. `arXiv:2601.07421` is cited for *methods* and, in Remark 3, for an explicitly-flagged **heuristic** improvement that is not used. Nothing about 727 is imported. |
| counterexample to Master Lemma part (1) | None found. See §4. |

---

## 2. Repairs needed (all cosmetic / non-load-bearing)

**R1. Section 6, SP-A, (H4) bullet: the `t ≥ 3` threshold is wrong.**
The text says "Also `t ≥ 3 ⟺ √L ≥ 80`, implied." With `t := ⌊√(log M)/20⌋` the correct
equivalence is `t ≥ 3 ⟺ √L ≥ 60`. Both are implied by `√L ≥ 20(2k+log₂(2k)+1) ≥ 140`
(which gives `t ≥ 7`), so nothing downstream changes. **Fix:** replace `80` by `60`.

**R2. Remark 7.2 and Section 8: "the forced demand at `p = 2` is `≥ 11 + ν_2((2k)!)`" is false
as written.**
For `k = 3`, `q₀ = 2^{10}`, `M = 10⁶`: `ν_2((2k)!) = ν_2(6!) = 4`, so the claim asserts
`W_2(m) ≥ 15`; the true minimum over that AP is `W_2 = 14`, and `W_2 < 15` for **489 of the 977**
elements (my `audit_sp_4.py`). The correct and sufficient statement is
`W_2(m) ≥ ν_2(2m) = 1 + ν_2(m) ≥ 11` (empirically `≥ 14` for `k=3`). **Fix:** state the bound
as `W_2(m) ≥ ν_2(2m) ≥ 11` and drop the `+ ν_2((2k)!)`. The conclusion drawn from it
(density of (i) is `0.0000` in that AP at that scale) is *correct* and I reproduce it exactly.

**R3. Section 8: "`κ_2(m) = s_2(m) ≈ 10` at that scale" overstates the supply.**
On `m ≡ 0 (mod 2^{10})`, `m ∈ [10⁶, 2·10⁶]` (11 free bits), the mean of `s_2(m)` is **5.885**
and its maximum is **10**. **Fix:** "`s_2(m) ≤ 10`, mean `≈ 5.9`". This only strengthens the
point being made.

**R4. Section 8 / the certificate description: the T13 configurations do not satisfy the
Master Lemma's own hypotheses, and the table should say so.**
For `k=2, P=13, t=3`, (H4) demands `log M ≥ 60(4+2+3+1)·log 13 ≈ 1539`, i.e. `M ≳ 10^{668}`;
the T13 configurations are `M = 2^{64}, 2^{200}, 10^{60}` (`log M = 44, 139, 138`). So T13
tests the deterministic part-(1) **chain** under a per-instance surrogate for (H4) (namely the
*conclusion* of SP.9, which is far weaker and does hold there) — legitimate, and the document
half-says this ("the exact per-instance version … gates every configuration"), but the table
row "packaged lemma at `M = 2^64 … 10^60`" reads as if the lemma's hypotheses were met.
**Fix:** relabel that row "part-(1) chain, with SP.9's conclusion verified per instance
((H1)–(H4) themselves are numerically unreachable)". *I closed this gap independently*: see
§4, where I re-ran the end-to-end test at genuinely (H1)–(H4)-compliant `M`
(`M = 2^{600}, 3^{600}, 3^{1309}, 7^{1511}, 11^{816}, 13^{600}, 13^{1200}, 101^{720},
251^{1040}` — from 181 to 2496 decimal digits).

---

## 3. Minor issues / observations (no fix required)

**M1. Everything is asymptotic at astronomically large `M`.** `M_A(2) = e^{19600}`,
`M_A(3) = e^{36750}`, `M_A(10) = e^{256500}`; and `E_A(M) < 1` needs `log M > (120 log 18)² ≈
1.203·10⁵` regardless of `k`. The document concedes this ("the *explicit* bound `E_A(M)` is
vacuous at numerically reachable `M`"). Fine for a lemma, but any downstream intersection
argument inherits these thresholds.

**M2. §0's "for `n ≥ k`" is stronger than needed.** SP.0 and the product form are valid for
`m ≥ k`, i.e. `n ≥ 0`. Harmless.

**M3. `J_p := ⌊log(2k)/log p⌋` is a floating-point definition.** The document immediately gives
the exact characterization `p^{J_p} ≤ 2k < p^{J_p+1}` (which is what the proofs use), and the
two agree for all `k < 500`, `p < 200` in my check. Recommend making the exact characterization
the definition.

**M4. Remark 3(h2)'s `β < 1/8`.** The two stated constraints `β < η` and `β < (1−η)/7` do
optimize at `η = 1/8`, giving `β < 1/8`; the arithmetic behind `(1−η)/7` is the SP.9 condition
`(1−η−β)/6 > β`. Consistent, and explicitly marked as "constants not re-tracked".

**M5. Strategic (route-level, not a defect in the lemma).** The AP-uniformity is advertised as
"intersection-friendly", but the constraint this lemma must eventually be intersected with —
`n+1,…,n+k` all `√(2n)`-smooth — is *not* a union of arithmetic progressions, so AP-uniformity
does not by itself deliver the intersection. Remark 4(i) correctly identifies that this method
cannot push `P` beyond `exp(O(√log M))`, which leaves the entire range
`(exp(√log M/6), √(2n)]` — i.e. essentially all of the difficulty — outside the lemma.

---

## 4. What I ran (independent re-verification)

All exact integer / `Fraction` arithmetic; no floating point in any acceptance test except
where explicitly comparing to the document's own float constants.

1. **Criterion implementations** (`audit_sp_1.py`, `audit_sp_8.py`). Four independent
   implementations (raw `factorial` divisibility; Legendre valuations; digit-sum form
   `2s_p(n+k)−s_p(2n) ≥ 2k`; product form `∏_{j=n−k+1}^{n+k} j | binom(2n,n+k)`) agree for all
   `n < 60`, `k ∈ {1,2,3}`, and reproduce **every** PROBLEM.md dataset:
   `S_1` prefix and `|S_1 ∩ [1,441]| = 40`; `S_2` min `208` and first 20 and
   `|S_2 ∩ [1,2·10⁵]| = 1981`; `S_3` prefix and `|S_3 ∩ [1,6·10⁴]| = 41`;
   `S_4 ∩ [1,6·10⁴] = {8174, 51984}`.
2. **SP.0** on 4000 random `(k ≤ 12, m ≤ 4·10⁴, p < 200)` plus the boundary `m = k`: 0 failures.
3. **SP.K / SP.1** on 4000 random `(m ≤ 10⁷, p < 300)` and all `m < 5000` at `p=2`: 0 failures,
   including the integrality `(p−1) | 2s_p(m) − s_p(2m)`.
4. **SP.2** exhaustively (`k ≤ 8`, `p < 40`, `m < 3000`) and on 6000 random instances
   (`k ≤ 20`, `m ≤ 10⁶`, `p < 120`): 0 failures; the exact refinement
   `W_p = ν_p(binom(2m,2k)) + ν_p((2k)!)` holds identically.
5. **SP.3** on 6000 random `(m ≤ 10⁹, p < 200, 0 ≤ e ≤ L ≤ 20)`: 0 failures. `θ(p) = ⌊p/2⌋/p`
   and `θ ≥ 1/3` (equality only at `p=3`) confirmed for all `p < 60`.
6. **SP.5 / SP.6 / SP.7** by brute force (3000 interval-count instances; 2000 CRT/digit-pattern
   instances including `p | q₀`): 0 failures.
7. **SP.8** against exact rational tails: worst (count)/(bound) ratio `0.695`.
8. **SP.9** exactly, at **1775** `(k,P,q₀,p)` points with `M = P^{⌈60(2k+log₂2k+t+1)⌉}` so that
   `(H4)` binds as tightly as possible (`k ∈ {2,3,4,7,25}`, `P ∈ {2,3,5,29,257}`,
   `q₀ ∈ {1,2,P,2^{10}3^4,720720}`, `t = 3`): 0 failures, min margin `70.3`; plus 240 further
   points at `M = 2^{200..3000}`.
9. **Master Lemma parts (1)+(2) end-to-end at genuinely (H1)–(H4)-compliant `M`**
   (`audit_sp_9.py`, part F1): see the run log below. 13 configurations, `M` from `2^{600}`
   (181 digits) to `251^{1040}` (2496 digits). Every sampled `m ∈ G` satisfies
   `κ_p(m) ≥ W_p(m)` for **every** `p ≤ P`, and (where part (2)'s hypothesis is imposed) the
   surplus `κ_p − W_p ≥ (1/120)log M/log p`. **0 violations.**
10. **Counting bounds `|BadC_p|`, `|BadS_p|` by exhaustion** over all of `[M,2M]`
    (`audit_sp_10.py`, part G-B) for `M ∈ {2·10⁴, 5·10⁴, 10⁵}`,
    `q₀ ∈ {1,2,6,24,105,1024,2401,2^5 3^3,3^6}`, `p ≤ 13`, `k ∈ {2,3,7,16}`, `t ∈ {3,4,6}` —
    these two bounds are proved without (H1)–(H4), so they must (and do) hold at reachable
    `M`: **1620 checks, 0 violations.**
11. **Exact `|BadS_p|` at astronomical `M`** (`audit_sp_10.py`, part G-A). Rather than sample,
    I computed `|BadS_p ∩ AP ∩ [M,2M]|` **exactly** by CRT (the `2k` spike classes are pairwise
    disjoint, so the count is a sum of exact residue-class counts) at
    `M ∈ {2^{200}, 2^{500}, 10^{300}, 3^{400}}`, `q₀ ∈ {1,2,24,1024,2^{10}3^4,720720,2^{30},3^{20}}`,
    four residues `a` each, `k ∈ {2,3,4,8,20,200}`, `p ∈ {2,3,5,7,11,13,23,31,127}`,
    `t ∈ {3,4,6,10}` — **25920 exact checks, 0 violations**, worst
    `exact/bound = 0.8889`. This settles the spike bound completely.
12. **Broad randomized sweep** (`audit_sp_11.py`) at `M = 2^{400},2^{900},2^{1800}`,
    `k ∈ {2,3,4,8,20,50,200}`, `q₀ ∈ {1,2,24,1024,2^{10}3^4,720720,2^{30}}`, `P ≤ 127`,
    `t ∈ {3,6}`, gated on the exact SP.9 conclusion: hunting for any `m ∈ G` violating the
    criterion, with per-prime bad-rate diagnostics in log space and a Poisson tail test.
13. **Section 8 density claims** (`audit_sp_4.py`) — all reproduced **exactly**:
    `0.6264` (`M=10⁵`) and `0.7970` (`M=10⁶`) for the criterion at all `p ≤ 13`, `k=3`;
    union sums `0.4414` and `0.2222`; per-prime rates
    `p=2:0.1167, 3:0.1063, 5:0.1014, 7:0.0502, 11:0.0287, 13:0.0381` (`M=10⁵`);
    `0.8237` in `m ≡ 7 (mod 24)`; `0.0000` in `m ≡ 0 (mod 2^{10})`; spike rate `0.0440`.
14. **Cross-check against PROBLEM.md's own carries-vs-borrows form.** On 3000 random
    `(k ≤ 10, m ≤ 10⁶, p < 100)`: `W_p(m) = ν_p(binom(2m,2k)) + ν_p((2k)!)`,
    `(p−1)ν_p((2k)!) = 2k − s_p(2k)`, and `(p−1)(c_p−b_p) ≥ 2k−s_p(2k) ⟺ κ_p ≥ W_p` — 0
    mismatches. PROBLEM.md's concrete `k=2` numbers (`c_2−b_2 ≥ 3`, `c_3−b_3 ≥ 1`,
    `c_p ≥ b_p` for `p ≥ 5`) are exactly `ν_2(4!)=3, ν_3(4!)=1, ν_5(4!)=0`. So LEMMA_SP's
    `W_p` really is the governing demand, with the `2k`-deficit in the right place.
15. **Testability finding** (`audit_sp_6.py`). Fully exhaustive verification of the part-(1)
    chain with the lemma's own `L_p` is *impossible* at reachable `M`: even in the easiest case
    (`k=2, q₀=1, t=3, p=2`) SP.9's threshold needs `Λ_2 ≳ 36`, i.e. `M ≳ 2^{45}`. This is why
    every end-to-end test (mine and the document's) is a sampling test.
16. **Scalar constants**: `(1−log2)/2 = 0.153426 ≥ 1/8`; `Σ_{n≥2}n^{−t} ≤ 3·2^{−t}` (`3≤t≤40`);
    `c−7/(240c) ≤ −1/120` on `(0,1/6]` with equality at `1/6`; `2e^{1/24}=2.0851<3`;
    `e^{100/9}=66910 < 70000` (so `M ≥ 70000` really does give (H3) headroom in SP-A);
    `7/240 > log2/120`; `(120 log 36)² = 184919 ≈ 1.85·10⁵`; `7/60 − 1/10 = 1/60`.
17. **`verify_sp.out`** was inspected only to check the claim "all tests pass": it does end in
    `ALL CHECKS PASSED`, and every number in it that I recomputed matches mine.

### Run log (end-to-end, at `M` that genuinely satisfies (H1)–(H4))

`audit_sp_9.py`, part F1. `M = P^E` with `E = ⌈f·(2k+log₂(2k)+t+1)⌉`, `f = 60` for parts
(1), `f = 120` for part (2); the (H1)–(H4) audit is an assertion inside the runner, so a
non-compliant configuration aborts rather than passing silently.

```
k=  2 P=  13 t=3 q0=1        E=600  digits(M)=669   SP.9-ok Lam>=18  |G|/N=378/400  part1-viol=0 part2-viol=0
k=  2 P=  13 t=3 q0=24       E=600  digits(M)=669   SP.9-ok Lam>=18  |G|/N=395/400  part1-viol=0 part2-viol=0
k=  2 P=  13 t=3 q0=2^10·3^4 E=600  digits(M)=669   SP.9-ok Lam>=18  |G|/N=397/400  part1-viol=0 part2-viol=0
k=  3 P=  11 t=4 q0=1        E=816  digits(M)=850   SP.9-ok Lam>=18  |G|/N=289/300  part1-viol=0 part2-viol=0
k=  3 P=  11 t=4 q0=30030    E=816  digits(M)=850   SP.9-ok Lam>=18  |G|/N=298/300  part1-viol=0 part2-viol=0
k=  2 P=   2 t=3 q0=1        E=600  digits(M)=181   SP.9-ok Lam>=18  |G|/N=382/400  part1-viol=0 part2-viol=0
k=  2 P=   3 t=3 q0=1        E=600  digits(M)=287   SP.9-ok Lam>=18  |G|/N=383/400  part1-viol=0 part2-viol=0
k=  7 P=   3 t=3 q0=1        E=1309 digits(M)=625   SP.9-ok Lam>=18  |G|/N=230/250  part1-viol=0 part2-viol=0
k=  2 P= 101 t=5 q0=1        E=720  digits(M)=1444  SP.9-ok Lam>=18  |G|/N=145/150  part1-viol=0 part2-viol=0
k=  5 P= 251 t=3 q0=1        E=1040 digits(M)=2496  SP.9-ok Lam>=18  |G|/N=115/120  part1-viol=0 part2-viol=0
k=  2 P=  13 t=3 q0=1        E=1200 digits(M)=1337  SP.9-ok Lam>=18  |G|/N=240/250  part1-viol=0 part2-viol=0   (part 2)
k=  2 P=  13 t=3 q0=2^10·3^4 E=1200 digits(M)=1337  SP.9-ok Lam>=18  |G|/N=247/250  part1-viol=0 part2-viol=0   (part 2)
k=  3 P=   7 t=3 q0=2^20     E=1511 digits(M)=1277  SP.9-ok Lam>=18  |G|/N=197/200  part1-viol=0 part2-viol=0   (part 2)
TOTAL violations: 0
```

At these (and only these) parameters the density claim (3) is also non-vacuous, and it holds
with room. Comparing the document's `Ê` against my measured bad fraction:

| config | `Ê` (terms `3P e^{−(7/240)E}`, `6·2^{−t}`, `3M^{−1/20}`) | measured `|Bad|/|AP|` |
|---|---|---|
| `k=2,P=13,t=3,q₀=1` | `0.7500` (`9.8e−7`, `0.75`, `1.2e−33`) | `0.0550` |
| `k=3,P=11,t=4,q₀=1` | `0.3750` (`1.5e−9`, `0.375`, `1e−42`) | `0.0367` |
| `k=2,P=101,t=5,q₀=1` | `0.1875` (`2.3e−7`, `0.1875`, `2e−72`) | `0.0333` |
| `k=7,P=3,t=3,q₀=1` | `0.7500` | `0.0800` |
| `k=5,P=251,t=3,q₀=1` | `0.7500` | `0.0417` |

(13/13 configurations OK; `Ê` is dominated entirely by the `6·2^{−t}` spike term, which is the
term the document's own Remark 3 identifies as the crude one.)

### Exact spike-count log (`audit_sp_10.py`)

```
G-A: exact |BadS_p| by CRT at M = 2^200, 2^500, 10^300, 3^400 : 25920 checks, 0 violations,
     worst exact/bound ratio 0.8889
G-B: exhaustive |BadC_p|,|BadS_p| over all of [M,2M], M in {2e4,5e4,1e5},
     q0 in {1,2,6,24,105,1024,2401,2^5·3^3,3^6}, p<=13, k in {2,3,7,16}, t in {3,4,6}:
     1620 checks, 0 violations
```

**Note on a false alarm I raised and then closed.** An earlier sampling sweep flagged ~10
`(config, p)` pairs where the *empirical* spike-failure rate (`1/120` or `2/120`) exceeded the
proved bound plus 4 Gaussian sigma. This was an artifact of my own test: for events with true
rate `~10⁻⁴–10⁻⁶`, `√(rate/N)` is a meaningless error bar and a single hit trips it. The exact
CRT computation above (25920 configurations, no sampling at all) shows the bound is never
violated — worst case it is `89%` saturated. **No defect in the document.**

---

## 5. Checklist (as issued)

1. **Literally about `((n+k)!)² | (2n)!` or a correctly-derived equivalent** — YES, via SP.0
   (`ν_p((2n)!) − 2ν_p((n+k)!) = κ_p(m) − W_p(m)`, `m=n+k`), independently re-derived and
   verified. But only for `p ≤ P`; the statement proved is a *partial* criterion, and says so.
2. **Quantifier order** — CORRECT. `k` fixed first, `M → ∞` after, `k` never depends on `M`;
   inside the lemma a single `m ∈ G` satisfies the criterion at every `p ≤ P` simultaneously.
   `Ê` is free of `k`. Not correct-to-727 because `P < M^{1/20} ≪ n+k`.
3. **Per-prime inequality direction and the `2k`-deficit** — CORRECT. Direction is
   `κ_p ≥ W_p` throughout; the deficit is carried explicitly as `ν_p((2k)!)` in SP.2/SP.4 and
   drives the `2k` in (H4).
4. **Prime ranges / boundaries** — `p = 2`: handled separately and correctly (SP.1, SP.5,
   `T_2−1` shift). `p ≤ 2k`: handled by the bulk term. `p | q₀`: handled by the masking
   `[e_p, L_p)` and the `ν_p(2q₀)` correction. `p ≈ √(2n)`: **NOT covered** — hard cap
   `P ≤ M^{1/20}`, and in SP-A only `P = exp(c√log M)`. Explicitly disclaimed (Remark 7.1).
5. **Constants explicit, uniformities tracked** — YES.
   `70000, 4/5, 1/10, 1/20, 1/60, 1/120, 7/240, 1/8, 3, 6, 12, 18` are absolute; the only
   `k`-dependence is (H1),(H4) hence `M_A(k)`, `M_B(k,P₀)`. Verified by recomputation.
6. **Every numerical claim re-checked independently** — DONE (see §4). Everything reproduces
   except the three prose numbers R2/R3 (and the mislabeled threshold R1), none load-bearing.
7. **Circularity / unproved auxiliary infinitude** — NONE. No infinitude is assumed or claimed;
   Kummer and Chernoff are proved in place; the background paper is used for methods only, and
   the one place its results are invoked (Remark 3, h1) is labeled heuristic and unused.
8. **Edge cases** — all checked:
   - small `M` (lemma vacuous, correctly so); `M ≥ 70000` is exactly what SP-A's (H3) check
     needs (`e^{100/9} = 66910 < 70000`);
   - `q₀ = 1`; `q₀` a high prime power (`2^{10}, 2^{20}, 2^{30}, 3^{20}, 7^4`); `p | q₀`
     with `e_p > 0` (masking + `ν_p(2q₀)`);
   - prime powers / **spike-class collisions** (the brief's "`r = s` collisions"): the `2k`
     classes `{m : p^{T_p} | 2m−i}` are pairwise *disjoint* (distinct residues mod `p^{T_p}`,
     resp. mod `2^{T_2−1}`), so the union bound over `i` is not even lossy; I confirmed this by
     computing the exact union count, which equals the sum;
   - **digit-expansion validity**: `p^{L_p} ≤ M^{4/5} < M ≤ m`, so positions `0..L_p−1` are
     genuine digits of every `m ∈ [M,2M]`, and `Λ_p = L_p − e_p ≥ 18 ≥ 1` is proved inside
     SP.9, so the pattern space `{0,…,p−1}^{Λ_p}` is legitimate;
   - `V_p = 0`; `V_p < J_p`; `p > 2k` (`J_p = 0`, `ν_p((2k)!) = 0`); `p = 2k` (`k=1,p=2`);
     `p = 2` with odd `i` (empty solution set); `T_p > e_p` always, so SP.7 never degenerates;
   - `P < 2` in SP-A (vacuous, and correctly declared so); `n = m − k ≥ M − k ≥ 1`.

---

## 6. Bottom line

`LEMMA_SP.md` is a correct, fully explicit, self-contained lemma. Apply repairs R1–R4 (all
one-line prose edits). Do not let the "proved in full" header migrate into any claim about
Erdős 727: the lemma's reach stops at `p ≤ exp(√(log M)/6)`, and the hard part of 727 lives
above that.
