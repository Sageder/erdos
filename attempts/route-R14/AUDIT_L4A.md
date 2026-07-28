# AUDIT_L4A.md — adversarial audit of `attempts/route-R14/L4A.md`

Auditor: fresh adversarial reviewer. Sources read: `PROBLEM.md`, `attempts/route-R14/L4A.md`,
and the R14 scripts *only to see what they compute*. All verification below was done with
scripts written from scratch (listed at the end); none of R14's code was executed or reused.

---

## VERDICT

**The unconditional core survives. One conditional theorem does not. The headline framing is
misleading in a way that matters.**

1. **Lemmas 1, 2, 2′, 3, 3′, 4, 5 are CORRECT.** I re-derived every one of them by hand and
   re-verified them by independent computation: 720 406 exhaustive instances of Lemma 2,
   756 666 of Lemma 2′, 120 000 random large instances, exact residue counts for Lemma 3
   (including the `e ≥ 2` bound by brute force), a grid check of Lemma 3′, and 46 297 members of
   the class of Lemma 5 — **zero counterexamples**. The arithmetic constants of Lemma 3′ and the
   threshold table `b*(θ,C)` of §5 reproduce to the digit. The numerics of Tables 1, 5 and §7
   reproduce **exactly** (same integers) from my own sieve. R14's computational claims are honest.

2. **Proposition O1 is NOT proved.** §7 gives *no proof at all* — only a Dickman-model
   computation and a table of measurements. §9 nonetheless lists it under "**Proved
   unconditionally in this route (new)**". That is a false claim and must be corrected.
   (Its model form additionally presupposes `#SP_b(x) ≍ x ρ(1/b)²`, itself unproved.)

3. **Theorem A's proof is FATALLY BROKEN.** It applies Hypothesis U with the *right-hand side*
   normalised by `#{n ∈ 𝒮(x) : ℓ ∥ n+1, P(n+1) = ℓ}`, i.e. to the **ℓ-dependent subfamily
   `{P(n+1) = ℓ}`**, which Hypothesis U as stated does not cover. With the bound U actually
   supplies, the union bound over `ℓ` costs a factor `E[#{ℓ>4 : ℓ ∥ n+1}]`, which I measure to be
   **2.65 / 2.77 / 2.49 / 1.94** at `b = .5/.4/.3/.25` (`x = 10⁷`); with `C ≈ 1`, `q_{J₀} = 1/2`
   that gives `≈ 1.3·#𝒮(x)` — a **vacuous** bound. The gap is quantitative-fatal, not cosmetic.

4. **Theorem B's derivation from Hypothesis U + (L1) is essentially SOUND** — the quantifier
   order, the choice of `b` after `θ, C`, the coverage of all primes (`2, 3` by Lemma 5; all
   `ℓ ≥ 5` including prime powers and the boundary `ℓ ≍ x^b`), the interchange of summation, and
   the fact that `R` never depends on `n`, all check out. **But the `θ = 1` column of the §5
   corollary is vacuous: Hypothesis U(θ=1, C) is FALSE for every `C` and every `b`** (§B.3 below).

5. **The advertised robustness "any `θ>0` and any `C≥1` suffice because `b` is free" is
   misleading.** The binding constraint is not on `θ` but on the **ratio** `θ/b`: `C·K(b,θ)<1`
   forces `θ/b ≥ 62.8`, and `θ/b → ∞` as `θ ↓ 0` (I measure `θ/b = 62.8, 71.1, 79.2, 89.7, 97.5`
   at `θ = 1, .5, .25, .1, .05`, `C = 1`). Since the modulus is `x^θ = y^{θ/b}` with `y = x^b` the
   smoothness bound, **the route needs a level of distribution at moduli `q ≥ y^{63}`** — an order
   of magnitude past the `y^{4√e−ε} = y^{6.59}` of Soundararajan that §3.3 calls "comfortable".
   And §5's own remark that the crude prime-power step is "immaterial because `b` is free" is
   wrong in exactly the way that counts: the sharp `a=1` constant `H` needs only `θ/b ≈ 7.3`,
   so **the crude Lemma 3′ is what pushes the requirement from `y^{7.3}` (borderline) to
   `y^{63}` (hopeless)**.

6. **Critical judgement on Hypothesis U: it is a reduction to a statement of comparable
   strength.** It is simultaneously a *smooth-neighbour conjecture* and *digit/congruence
   equidistribution along the smooth-pair family* — two items that `PROBLEM.md`'s insufficiency
   list names explicitly. It has no known implication from any standard conjecture, no partial
   case for pairs above `(log x)^c`, and the numerical support is at `b ≥ 0.25` while the theorem
   operates at `b ≤ 0.016` (i.e. `x ≥ 5^{63} ≈ 10^{44}`). **It does not count as progress under
   `PROBLEM.md`.** L4A.md itself says this in §9 — that honesty is credited, and the verdict
   agrees with it. Full two-sided argument in Part C.

Nothing in L4A.md resolves Erdős 727 or its `k = 2` variant, and L4A.md does not claim otherwise.

---

## Part A — the unconditional lemmas

### Lemma 1 (criterion). **CORRECT.**

Re-derivation: `ν_p((n+2)!) = ν_p(n!) + ν_p(n+1) + ν_p(n+2)`, and by Kummer
`ν_p((2n)!) − 2ν_p(n!) = ν_p\binom{2n}{n} = κ_p(n)`. Subtracting gives exactly the stated form.
Consistent with `PROBLEM.md`'s `2s_p(n+k) − s_p(2n) ≥ 2k` form.

Independent check (`aud1.py`): the criterion agrees with Legendre-valuation divisibility
`((n+2)!)² | (2n)!` at **every** prime `≤ 2n` for all `2 ≤ n ≤ 1500` (0 mismatches), and produces
`S₂ = 208, 458, 987, 1220, 1455, 1597, 1889, 2012, 2144, 2330, …`, matching `PROBLEM.md`.

### Lemma 2 (digit-poor characterisation, `e = 1`). **CORRECT.**

Re-derivation verified line by line. `n = ℓV + (ℓ−j)` with `ℓ−j ∈ {ℓ−2, ℓ−1} ⊆ [1, ℓ−1]`, so the
base-`ℓ` digit string of `n` is `(ℓ−j, d₀(V), d₁(V), …)`. Position 0 always carries
(`2(ℓ−j) ≥ ℓ` for `ℓ ≥ 5`, since `j ≤ 2`). The rest is a correct induction on
`c_{i+1} = 1[2d_i + c_i ≥ ℓ]` with `c₀ = 1`. Odd `ℓ` is used correctly to turn `2d₀ + 1 < ℓ` into
`d₀ ≤ (ℓ−3)/2` and `2d_i < ℓ` into `d_i ≤ (ℓ−1)/2`. Boundary case `W = 1` (i.e. `n+j` prime,
`V = 0`) is digit-poor and indeed `κ_ℓ(n) = 1 < 2` — consistent with `PROBLEM.md`'s "every prime
in `(n, n+k]` fails".

Independent check (`aud2.py`): **720 406** exhaustive instances (`n ≤ 2·10⁵`, `j ∈ {1,2}`, all
`ℓ ≥ 5` with `ℓ ∥ n+j`) — **0 violations**; plus 120 000 random instances with `ℓ < 4000`,
`W < 10⁸` — 0 violations.

**Small point worth adding to the write-up (used implicitly and true):** digit-poorness at
position 0 forces `W ≡ d₀+1 ∈ [1,(ℓ−1)/2] (mod ℓ)`, hence the residue set `R` automatically lies
in the *coprime* residues, as Hypothesis U requires. The document never checks this.

### Lemma 2′ (prime powers). **CORRECT.**

`ℓ^e − j = (ℓ−j) + (ℓ−1)(ℓ + … + ℓ^{e−1})` — verified. Positions `1..e−1` carry because
`2(ℓ−1)+1 = 2ℓ−1 ≥ ℓ`. Verified independently on **756 666** exhaustive instances and 120 000
random ones (`e` up to 3, `W < 10⁸`): `κ_ℓ(n) = e + #carries(V, carry-in 1)` — **0 violations**.

### Lemma 3 (truncation to a congruence mod `ℓ^J`). **CORRECT.**

`e = 1`: the count `((ℓ−1)/2)((ℓ+1)/2)^{J−1}` and the proportion
`q_J(ℓ) = (1/2)((ℓ+1)/(2ℓ))^{J−1}` verified by brute force over all `V mod ℓ^J` for
`ℓ ∈ {5,7,11,13,101}`, `J ≤ 4` (exact equality). `r = (ℓ+1)/(2ℓ) ≤ 3/5` for `ℓ ≥ 5` ✓.

`e ≥ 2` bound `(5/4)Σ_{i<e}\binom{J}{i}r^{J−i}`: the decoupling argument is valid — for a fixed
carry-set `S` the carry-in `c_t` is determined by `S`, so positions decouple; positions outside
`S` admit `≤ (ℓ+1)/2` digits, positions in `S` are bounded by `ℓ`; dividing by
`ℓ^{J−1}(ℓ−1) ≥ (4/5)ℓ^J` supplies the `5/4`. Verified by exhaustive enumeration for
`ℓ ∈ {5,7,11}`, `J ≤ 5`, `e ≤ 3` — **no violations**.

Containment (failure ⟹ truncated event) is correct: fewer than `e` carries overall implies fewer
than `e` among positions `0..J−1`.

### Lemma 3′ (Chernoff form). **CORRECT, one rounding slip in the wrong direction.**

The chain `Σ_{i<a}\binom{J}{i}r^{J−i} ≤ z^{−a}(r+z)^J` (`z ≤ 1`) is right, `z = 1/10`,
`r + z ≤ 0.7`. Exact constants (my computation):

| quantity | paper | exact |
|---|---|---|
| `log₂(1/0.7)` | `0.5146` | `0.514573` |
| constant term `log₂(5/4)+log₂(1/0.7)` | `0.837` | `0.836501` |
| coefficient of `a` | `3.836` | `3.836501` |
| final exponent `0.514573 − 3.8365/11` | **`0.1659`** | **`0.165800`** |
| `2^{0.8365}` | `1.79` | `1.7857` |

The paper's `0.1659` is rounded **up** (i.e. in the direction that overstates the bound). Harmless:
the final claim only uses `0.1658 > 1/7 = 0.142857`. `J ≥ 1` is safe (`J ≥ 9` in fact, from
`aβ ≤ θ/11` and `a ≥ 1`), and `ℓ^{a+J} ≤ x^θ` holds by `a+J = ⌊θ/β⌋`. Grid check over
`log x ∈ {50,…,20000}`, `ℓ ∈ {5,…,10⁵}`, `θ ∈ {1,.5,.25,.1,.05}`, all admissible `a`: the true
proportion is at most `e^{−4.86}` times the claimed `2·2^{−θ/(7β)}` — the bound is safe with a
large margin.

### Lemma 4 (distribution-free budget). **CORRECT.**

`k(ℓ) = ⌊b/β_ℓ⌋ ≥ 1`; `β_ℓ ≤ b/k(ℓ)` ⟹ `r^{θ/β_ℓ} ≤ t^{k(ℓ)}`; `Σ_{ℓ|m}β_ℓ ≤ 1` (from
`∏ℓ ≤ m ≤ x`) and `β_ℓ > b/(k+1)` on the level set ⟹ `#{ℓ : k(ℓ)=k} < (k+1)/b`;
`Σ_{k≥1}(k+1)t^k = t(2−t)/(1−t)²` ✓. The claim that it uses **no** distributional input is
accurate and is the genuine structural gain of the route.

*Nit:* it is applied to `m = n+2 ≤ x+2`, marginally outside the stated `m ≤ x`; trivially fixed.

### Lemma 5 (`n ≡ 157 mod 648`). **CORRECT.**

`157 ≡ 5 (8)`, `157 ≡ 76 (81)` ✓. `n ≡ 5 (8)` ⟹ `ν₂(n+1)=1`, `ν₂(n+2)=0`, and bits 0 and 2 of
`n` are set so `κ₂(n) = s₂(n) ≥ 2` (using `s₂(2n)=s₂(n)`). `76 = (2,2,1,1)₃` ⟹ `n ≡ 1 (3)`,
`ν₃(n+1)=0`, `n+2 ≡ 78 (81)` so `ν₃(n+2)=1`, and digits 2,3 of `n` equal `2`, each of which
carries on doubling, so `κ₃(n) ≥ 2`. Both demands are exactly `2`, met with equality.

Independent check: all **46 297** values `n ≡ 157 (mod 648)` up to `3·10⁷` — 0 violations.
I also re-certified the eight claimed `S₂` members `48109, 67549, 216589, 312493, 508837, 561973,
1776973, 2676397` by Legendre valuations at *every* prime `≤ 2n` (sympy): all in `S₂`, all
`≡ 157 (mod 648)`.

### Proposition O1. **NOT PROVED — mislabelled as unconditional.**

§7 states O1 as a Proposition and then supplies (i) a Dickman-model asymptotic
`A/S ≍ 2^{−1/b}/ρ(1/b)` and (ii) a measurement table. **There is no proof.** Two independent
defects:

* The model step `S(x,b) ≍ x ρ(1/b)²` (needed for the ratio) is itself an unproved
  independence heuristic; unconditionally only `S ≤ Ψ(x,x^b) ≍ xρ(1/b)` is available, and with
  that upper bound the argument gives nothing (`A ≤ Ψ` too).
* The quantifier "`A(x,b)/S(x,b) → ∞ as b → 0, uniformly for x large`" is ill-posed: in the model
  the ratio is `x`-independent, so "uniformly for `x` large" has no content; the observed growth in
  `x` (`9.17 → 13.12` at `b=.25`) is a finite-size effect the document elsewhere identifies as
  transient.
* The follow-on sieve claim ("recovers only a factor `≍ b/θ′` by Mertens … therefore the second
  smoothness must be carried unfactorised through the entire argument") is a heuristic about two
  particular strategies, presented as a statement about all proofs.

I reproduced the O1 table exactly from my own sieve at `x = 10⁷`
(`A/S = 1.40, 2.55, 5.98, 9.17` at `b = .5,.4,.3,.25`; `A = 1557937, 593725, 77402, 15459`;
`S = 1114139, 233279, 12945, 1685`). The *numbers* are right; the *Proposition* is not proved.

**Required fix:** move O1 to §"model/heuristic", and delete it from the §9 list of things
"proved unconditionally".

---

## Part B — the conditional theorems

### B.1 Theorem A — **FATAL: Hypothesis U is applied to an ℓ-dependent family.**

Hypothesis U supplies, verbatim,

```
#{n ∈ 𝒮(x) : ℓ^a ∥ n+ν, W mod ℓ^J ∈ R}  ≤  C·(|R|/(ℓ^{J−1}(ℓ−1)))·#{n ∈ 𝒮(x) : ℓ^a ∥ n+ν}.
```

The proof of Theorem A uses (line 269 of L4A.md)

```
#{fail, P(n+1)=ℓ}  ≤  C(1/2)(3/5)^{J₀−1}·#{n ∈ 𝒮(x) : ℓ ∥ n+1, P(n+1) = ℓ}.
```

The **right-hand side carries the extra constraint `P(n+1) = ℓ`**, which U does not provide. The
constraint is essential to the proof: it is only because the sets `{P(n+1)=ℓ}` *partition* `𝒮(x)`
that the sum over `ℓ` telescopes to `#𝒮(x)`. `{P(n+1)=ℓ}` is a multiplicative/archimedean
condition on the cofactor `W` (`P(W) < ℓ`), not a congruence mod `ℓ^J`, so it cannot be absorbed
into `R`.

What U legitimately gives is

```
Σ_ℓ #{n ∈ 𝒮 : ℓ ∥ n+1, digit-poor} ≤ C q_{J₀} Σ_ℓ #{n ∈ 𝒮 : ℓ ∥ n+1}
                                    = C q_{J₀} Σ_{n∈𝒮} #{ℓ>4 : ℓ ∥ n+1}.
```

I measured `E[#{ℓ>4 : ℓ ∥ n+1}]` over smooth pairs at `x = 10⁷`:

| `b` | .50 | .40 | .30 | .25 |
|---|---|---|---|---|
| mean `#{ℓ>4 : ℓ ∥ n+1}` | 2.652 | 2.767 | 2.488 | 1.944 |

With `C ≈ 1.01`, `q_1 = 1/2` this is `≈ 1.3–1.4` times `#𝒮(x)` — the bound is worse than trivial,
so `δ` cannot be made positive. Nor can the loss be beaten by raising `J₀`: one would need
`C q_{J₀}·E[ω] < 1` with `E[ω] ≍ log log x → ∞`, forcing `J₀ ≍ log₂ log log x → ∞` and hence
`b < θ/(J₀+1) → 0` with `x` — illegal for fixed `b`.

**Repairs (pick one):**

* (a) State a strengthened hypothesis **U′**, identical to U but with `𝒮(x)` replaced by
  `𝒮(x) ∩ {P(n+1) = ℓ}` (an `ℓ`-dependent family). §8 Table 5 *measures exactly this* quantity and
  finds `1.001–1.056`, so U′ is numerically supported — but U′ is strictly stronger than U, and the
  "Open Problem" stated in §9 is the *weaker* U, so **as written §9's open problem does not imply
  Theorem A**. This must be corrected.
* (b) Demote Theorem A to a corollary of Theorem B: for `b < b*(θ,C)` Theorem B bounds failures at
  *all* primes, in particular at `P(n+1)`, giving the conclusion with `δ = 1 − CK(b,θ)`. This is
  sound but sacrifices the advertised range `b < θ/(J₀+1)` (e.g. `b < θ/2` when `C < 2`) — a factor
  of ~30 in `b` — and the advertised `δ ≈ 1/2`.

The observation behind this is structural and worth recording: **a constant per-prime saving
`q_{J₀}` can never survive a union bound over the `≍ log log x` prime factors; only Lemma 4's
`ℓ`-decaying factor `2^{−θ/(7β_ℓ)}` can.** Theorem A tried to dodge that by partitioning, and the
partition is not licensed.

### B.2 Theorem B — **the derivation is sound.** Checks performed:

* **Quantifier order.** `k = 2` fixed first; `θ, C` fixed; then `b` chosen; then `x → ∞`. `b` never
  depends on `n` or `x`. ✓ (`Q₀, c₀` are absolute.) The logical form is
  `∃θ,C,b [ U(θ,C;b,Q₀,c₀) ∧ b<θ/11 ∧ CK(b,θ)<1 ] ⟹ S₂ infinite`, which is what is proved.
* **`R` never depends on `n`.** For each triple `(ℓ,a,ν)`, `J = ⌊θ/β_ℓ⌋ − a` and
  `R = {r : <a carries in positions 0..J−1}` depend only on `(ℓ,a)`. `a` varies with `n`, but the
  sum is organised over `(ℓ,a)` pairs, so within each application `R` is fixed. ✓ **This is the
  main thing I tried to break and could not.**
* **Union bound covers all primes.** `p=2,3` identically by Lemma 5 (equality, verified);
  `ℓ ≥ 5` with `ℓ^a > x^{θ/11}` in part (a); `ℓ ≥ 5` with `ℓ^a ≤ x^{θ/11}` in part (b); primes not
  dividing `(n+1)(n+2)` are vacuous. Prime powers `a ≥ 2` are handled by Lemma 2′/3. Primes in
  `(n, n+2]` are excluded automatically by `x^b`-smoothness, consistent with `PROBLEM.md`. ✓
* **Boundary `ℓ ≍ x^b`.** `β_ℓ = b < θ/11`, `a=1`, `J = ⌊θ/b⌋−1 ≥ 10 ≥ 1`, `ℓ^{1+J} ≤ x^θ`. ✓
* **Part (a) bookkeeping.** `#{n ≤ x : ℓ^a | n+ν} ≤ x^{1−θ/11}+1`; `≤ π(x^b)·log x/log 5` pairs;
  total `≪ x^{1−(θ/11−b)}log x = o(x)`. Requires `b < θ/11` strictly ✓.
* **Interchange of summation** in part (b): legitimate, the weight `2C·2^{−θ/(7β_ℓ)}` is
  `n`-independent; the resulting `Σ_{n}Σ_{ν}Σ_{ℓ|n+ν}` is exactly Lemma 4's shape. ✓
* **`K(b,θ)` and the threshold table.** Reproduced independently to 5 digits:
  `b* = 0.01591, 0.00704, 0.00316, 0.00112, 0.00051` (`C=1`), `0.01407, 0.00632, 0.00287,
  0.00103, 0.00047` (`C=2`) — identical to §5. The constraint `b < θ/11` is never binding
  (`K(θ/11,θ) = 56.1/θ > 1`). ✓
* Conclusion `#(S₂∩𝒮) ≥ (1−CK−o(1))#𝒮 ≫ x` for infinitely many `x` ⟹ `S₂` infinite. ✓

### B.3 **Hypothesis U(θ=1, C) is FALSE.** (Corollary table's first column is vacuous.)

Take `m = ⌈1/b⌉` and `ℓ =` the largest prime `≤ x^{1/m}`; then `ℓ ≤ x^b`, and with `a=1`,
`J = m−1` we have `ℓ^{a+J} = ℓ^m ≤ x = x^θ`, so U applies. But then
`ℓ^J = ℓ^{m−1} ≈ x/ℓ`, which is the full range of `W = (n+1)/ℓ`: each residue class mod `ℓ^J`
contains `O(1)` values of `W`. Taking `R` = one occupied class, U demands

`1 ≤ LHS ≤ C·(1/(ℓ^{J−1}(ℓ−1)))·#{n∈𝒮 : ℓ ∥ n+1} ≈ C·δ_b`,

where `δ_b` is the density of `𝒮`. At the operative `b = 0.016`, `δ_b ≈ ρ(63)²/648 ≈ 10^{−224}`,
so U forces `#{n∈𝒮 : ℓ ∥ n+1} = 0`, contradicting the supply hypothesis (L1)/(S). More generally
U survives only while `x^{1−θ}δ_b → ∞`, i.e. for `θ < 1` strictly. **Fix:** restrict `θ ∈ (0,1)`
in Lemma 3′ and in the corollary table; drop the `θ=1` column (or replace by `θ = 0.99`, whose
`b*` is essentially unchanged).

Note this is not a remote corner: at `θ` near 1, Theorem B's *own* application at `ℓ ≍ x^b`,
`a=1` lands on `ℓ^J ≈ x/ℓ` — precisely the falsifying parameters.

### B.4 **"Any `θ > 0` and any `C ≥ 1` suffice because `b` is free" — misleading.**

The condition `C·K(b,θ)<1` with `K = (4/b)t(2−t)/(1−t)²`, `t = 2^{−θ/(7b)}` is, to leading order,
`θ/b > 7 log₂(8C/b)`. Hence the *ratio* `R = θ/b` is bounded below, and the modulus in U is

`ℓ^{a+J} ≤ x^θ = y^{θ/b} = y^R`, `y = x^b` the smoothness bound.

Measured minimum admissible `R` (my computation):

| `C \ θ` | `1` | `0.5` | `0.25` | `0.1` | `0.05` |
|---|---|---|---|---|---|
| `1.0` | 62.8 | 71.1 | 79.2 | 89.7 | 97.5 |
| `2.0` | 71.1 | 79.2 | 87.1 | 97.5 | 105.3 |

Since `θ = 1` is excluded (B.3), the **infimum of `θ/b` over admissible parameters is ≈ 62.8**.
So U is needed at moduli `q ≥ y^{62.8}`. Consequences:

* §3.3's "For a *single* smooth number … Soundararajan … Since our moduli are `ℓ^J ≤ x^θ` with
  `θ` free, this is comfortable" is **not** justified in the `y`-aspect: Soundararajan's individual-
  modulus range is `q ≤ y^{4√e−ε} = y^{6.59}`, a factor `9.5` short in the exponent; and his range
  `u ≥ (log log y)^4` with `u = 1/b = 63` forces `y ≤ exp(e^{2.82}) ≈ 2·10⁷`, i.e. a *bounded*
  `x` — the theorem cannot be invoked at all as `x → ∞`. Only the averaged results (Pascadi,
  `x^{66/107}`) are in the right shape, and **those are averages over moduli whereas U is stated
  pointwise in `ℓ`** — a mismatch the document never addresses. (Theorem B does sum over `(ℓ,a)`,
  so an averaged U might suffice, but the weights `2^{−θ/(7β_ℓ)}` and the varying normalisations
  `#{n∈𝒮 : ℓ^a ∥ n+ν}` make that a non-trivial reformulation, not a remark.)
* §5's Remark — "Lemma 3′ is deliberately crude at prime powers … Since `b` is a free parameter
  this loss is immaterial" — is **wrong where it matters**. With the sharp `a=1` constant `H` the
  requirement drops to `θ/b ≈ 7.3` (I verify `b* = 0.1365` at `θ=1`), i.e. moduli `y^{7.3}` —
  right at the edge of Soundararajan's `y^{6.59}`. The crude prime-power step is therefore the
  single reason the route asks for `y^{63}` rather than `y^{7.3}`. **Sharpening Lemma 3′ at
  `a ≥ 2` is the highest-value repair in the whole document**, and it should be flagged as such
  rather than dismissed.
* A uniformity question is silently begged: U's constants `θ, C` are asserted for one `b`, but
  §8's evidence shows the bias factor *growing* as `b` decreases at fixed `x`
  (`1.041, 1.196, 1.364, 2.263` at `b = .5,.35,.30,.25`). If `C = C(b)` grows even like
  `ρ(1/b)^{−1} = b^{−1/b}`, then `C(b)K(b,θ)<1` needs `θ ≳ 7 log₂(1/b) → ∞`, and **no fixed `θ`
  works**. R14 attributes the growth to a transient archimedean/finite-size effect; that is
  plausible but is not established, and it is a live failure mode of the "any `C`" claim.

### B.5 The numerical support is evaluated far from the operative regime

Theorem B operates at `b ≤ 0.016`, i.e. `u = 1/b ≥ 63`; for `y = x^b ≥ 5` this needs
`x ≥ 5^{62.5} ≈ 10^{44}`. All of §8's data is at `x ≤ 10⁸`, `b ≥ 0.25`. Moreover for `ℓ` near
`x^b`, `J = ⌊θ/β⌋−1 ≈ 1/b − 1` equals essentially the *total* number of base-`ℓ` digits of `W`, so
the event Theorem B needs U for is the **untruncated** digit-poor event — the one with the *large*
measured bias (`1.04 → 2.26`), not the benign `DP₁` (`1.003–1.013`). §9's point 3 ("the numerics
say the statement is true, with `C ≈ 1.01` … for the truncation `DP₁` that Theorem A actually
uses") is accurate about Theorem A but does not support Theorem B — and Theorem A is the one whose
proof is broken. The two halves of the numerical case do not meet.

### B.6 (L1)

Not re-provable here; correctly flagged as a second conditional dependency. Two remarks: (i) the
conclusion of Theorem B should read `≫_{b,Q₀} x`, not `≫_b x`; (ii) the Hildebrand citation for
(S) is for consecutive smooth *triples*/pairs with positive density and is plausible, but I could
not verify "Cor. 2" of that paper from here — it is cited, not proved, which is stated.

---

## Part C — Critical judgement: is Hypothesis U of comparable strength to 727(k=2)?

**Case that U is genuinely weaker / standard-shaped.**
1. U is an **upper bound only**, with **no asymptotic**, an **arbitrary constant `C`**, and (as
   advertised) an arbitrarily small level `θ`. Upper-bound level-of-distribution statements are a
   strictly weaker species than asymptotics and are sometimes accessible to large-sieve/Selberg
   technology that asymptotics are not.
2. Its **single-smooth analogue is a theorem** (Soundararajan; Fouvry–Tenenbaum, Drappeau,
   Maynard, Harper, Pascadi on average). The *shape* is established technology; only the pair
   aspect is new.
3. U contains **no factorials, no carries, and no "one `n` beats every prime simultaneously"
   structure** — the features that make 727 what it is. Lemmas 2–4 genuinely retire all of that
   combinatorics; that is a real, checkable gain and it is the honest achievement of R14.
4. `𝒮(x)` is a **positive-density** set (density `ρ(1/b)²/Q₀`), not a sparse family; equidistribution
   statements for positive-density sets are not automatically hopeless.
5. There is **no converse**: 727(k=2) does not imply U, so the two are not equivalent.

**Case that U is of comparable strength (and thus a forbidden reduction).**
1. `PROBLEM.md`'s insufficiency list names, verbatim, "**smooth-neighbor conjectures**" and
   "**digit equidistribution along sparse families**". U is the *conjunction* of both: it is a
   statement about consecutive smooth numbers, asserting congruence (=digit) equidistribution
   along that family. It is excluded by name, not by analogy.
2. **No case of it is known for pairs above `(log x)^c`** — the gap to `x^θ` is not a constant
   factor but a change of category. The only known route to smooth-pair counts runs through
   correlations of multiplicative functions (Matomäki–Radziwiłł / logarithmic Elliott / Pilatte),
   which are intrinsically polylog-limited in the dilation parameter. §9 says this correctly.
3. **No standard conjecture implies U.** It is not a consequence of GRH, EH, ABC, or any named
   hypothesis. A reduction whose target has no established route and no known special case is not
   a reduction to "a statement in a well-developed area"; it is a reduction to a new conjecture.
4. Points B.3–B.5 show the required parameters are far more extreme than advertised
   (`q ≥ y^{63}`, `θ<1` forced, `C` uniform in `b` needed, numerics 15× away in `b` and `10^{36}`
   away in `x`). The claimed "robustness" that made U look weak than 727 does not survive audit at
   full strength.
5. Even under U, the conclusion is only the **named `k=2` variant**, not the headline — as §9
   states. So the "purchase" of the reduction is bounded even if U were proved.

**Decision.** U is *logically* weaker than 727(k=2) in form — it is an upper bound, it is not
equivalent, and it strips out the digit combinatorics — but it is **not demonstrably weaker in
difficulty**, it has **no known partial case in the operative range**, and it sits squarely inside
the class `PROBLEM.md` excludes by name. **Hypothesis U counts as a reduction to an unproved
statement of comparable strength; it is not progress on 727 under the stated rules.** The
document reaches the same conclusion in §9 and is not misrepresenting itself; the criticism here
is confined to §0/§3.3/§5's rhetoric ("comfortable", "immaterial", "very weak level suffices"),
which overstates how weak U is by roughly an order of magnitude in the modulus exponent.

---

## Minor issues (non-fatal, should be fixed)

1. §4: `J₀ ≤ 2 + log(C/2)/log(5/3)` **fails at `C = 1`** (gives `0.643 < 1 = J₀`). Should be
   `J₀ ≤ max(1, 2 + log(C/2)/log(5/3))`. Verified for `C ≥ 1.5`.
2. §2 Lemma 3′: `0.1659` should be `0.16580` (rounded the wrong way); `1.79` should be `1.786`.
   Both harmless because the final claim uses `1/7`.
3. §5 Remark: the constant `H = (25/(9b))·…` should be `(125/(27b))·…`. With `a=1`,
   `J = ⌊θ/β⌋−1 ≥ θ/β−2`, so `J−1 ≥ θ/β−3` and the factor is `r^{−3}=125/27`, not `r^{−2}=25/9`.
   Consequence: `b* = 0.1162, 0.0486, 0.0210, 0.0071` rather than `0.137, 0.055, 0.023, 0.0078`
   (a ~15 % correction; does not change the argument of B.4).
4. §0: "of relative size exactly `(1/2)((ℓ+1)/(2ℓ))^{J−1} ≈ 2^{−J}`" — the `≈ 2^{−J}` holds only
   as `ℓ → ∞`; at `ℓ = 5` it is `(1/2)(3/5)^{J−1}`, which is what the proofs actually use.
5. Lemma 4 is applied with `m = n+2 ≤ x+2`, outside the stated `m ≤ x`; state it for `m ≤ 2x`.
6. Theorem B's conclusion `≫_b x` should be `≫_{b,Q₀} x`; and the implied constant is
   `≈ ρ(1/b)²/648 ≈ 10^{−224}` at the operative `b` — worth stating so "positive proportion" is
   not read as a large proportion.
7. Lemma 3, `e ≥ 2` case: the numerator counts all `V mod ℓ^J` with `< e` carries, including those
   with `ℓ | W`, while the denominator is the coprime count. Fine as an upper bound, but the
   wording "the proportion of `W mod ℓ^J` coprime to `ℓ` satisfying `DP_J^{(e)}`" should say
   "at most (count of all residues)/(number of coprime residues)". For `e = 1` no correction is
   needed (digit-poorness at position 0 forces `ℓ ∤ W`) — this should be stated, since it is what
   makes `R` admissible for Hypothesis U.
8. §7's O1 statement mixes limits (`b → 0` "uniformly for `x` large") in a way that has no content
   under its own model, which is `x`-independent.

---

## Files

Audit scripts (written from scratch, none of R14's code used):

* `/tmp/claude-0/-home-user-erdos/49f04ef0-a63d-55e0-b5d7-ad8e910eb3fe/scratchpad/aud1.py`
  — Lemma 1 vs Legendre-exact `((n+2)!)² | (2n)!` for `n ≤ 1500`; `S₂` reproduction.
* `.../aud2.py` — exhaustive Lemma 2 (720 406 instances) and Lemma 2′ (756 666), 120 000 random
  large instances, exact Lemma 3 residue counts, brute-force check of the `e ≥ 2` bound.
* `.../aud3.py` — Lemma 5 class (46 297 values to `3·10⁷`), Lemma 3′ constants, `J₀` formula,
  `K`/`H` thresholds.
* `.../aud4.py` — independent sieve reproduction of Table 5 (`DP₁` rate, exact failure rate) and
  the §7 `A/S` table at `x = 10⁷`.
* `.../aud5.py` — independent reproduction of Table 1 (`E, E1, E2, Esm, pass, Plpf, sqfr`);
  the `x = 10⁷, b = .50` row matches L4A.md digit for digit.

Audited document: `/home/user/erdos/attempts/route-R14/L4A.md`.
This report: `/home/user/erdos/attempts/route-R14/AUDIT_L4A.md`.
