# LEMMA_SP.md — Route R2: small-prime carry machinery for Erdős 727 (fixed k)

Status: **proved in full**, every constant explicit, every quantifier explicit.
Numerical certificates: `verify_sp.py` in this directory (test numbers `T*` are
cited inline; all tests pass, see `verify_sp.out`).

Provenance of methods: the forced-carry / Chernoff / residue-counting /
spike-exclusion machinery is ported from the licensed background paper
arXiv:2601.07421 (writeup of the Erdős-728 resolution), Lemmas 3–13 there.
**No conclusion about problem 727 is imported from anywhere.** The port is not
verbatim: the 727 demand is `ν_p((2m)(2m−1)⋯(2m−2k+1))` (a block *below* `2m`,
carrying the `ν_p((2k)!)` bulk term — the "2k-deficit" of PROBLEM.md), and the
whole machinery is re-engineered to survive restriction to an arithmetic
progression (masked digit positions, and a `ν_p(2q0)`-corrected spike bound —
the uncorrected bound is *false* in APs, falsified in T7.2).

---

## 0. Setting and notation

Throughout, `k ≥ 2` is a fixed integer, `p` denotes a prime, `log` is the
natural logarithm, `log_2 x = log x/log 2`. For an integer `x ≥ 1`, `ν_p(x)` is
the exponent of `p` in `x` and `s_p(x)` the sum of the base-`p` digits of `x`
(`ν_p`, `s_p(0) = 0`). For `m ≥ 1` write its base-`p` digits as
`m = Σ_{j≥0} a_j(m,p) p^j`, `0 ≤ a_j < p` (all but finitely many zero). Define:

- `κ_p(m) := ν_p(binom(2m, m))`;
- `W_p(m) := ν_p((2m)(2m−1)⋯(2m−2k+1)) = Σ_{i=0}^{2k−1} ν_p(2m−i)`
  (defined for `m ≥ k`, so every factor is ≥ 1) — the **demand** at `p`;
- `V_p(m) := max_{0 ≤ i < 2k} ν_p(2m−i)` — the **spike height** at `p`;
- `J_p := ⌊log(2k)/log p⌋`, i.e. the unique integer with `p^{J_p} ≤ 2k < p^{J_p+1}` (T11.c);
- `θ(p) := ⌊p/2⌋/p` (so `θ(2) = 1/2`, `θ(p) = (p−1)/(2p)` for odd `p`;
  `θ(p) ≥ 1/3` for every prime, with equality only at `p = 3`);
- a digit `a ∈ {0,…,p−1}` is **large** if `a ≥ ⌈p/2⌉`; the number of large
  values is exactly `⌊p/2⌋`, so a uniformly random digit is large with
  probability `θ(p)`;
- for integers `0 ≤ e ≤ L`:
  `X_p^{[e,L)}(m) := #{ j : e ≤ j < L, a_j(m,p) ≥ ⌈p/2⌉ }`
  (the number of large digits of `m` in positions `e,…,L−1`).

**727 criterion (from PROBLEM.md, governing).** For `n ≥ k` and `m := n + k`:

```
n ∈ S_k  ⟺  (2m)(2m−1)⋯(2m−2k+1) | binom(2m,m)  ⟺  ∀p: κ_p(m) ≥ W_p(m).
```

We call `κ_p(m) ≥ W_p(m)` the **criterion at p** and write it `Crit_p(m)`.
(Implementations of both sides are cross-validated against all PROBLEM.md
sanity data — `S_1, S_2, S_3, S_4` prefixes and counts — in T1.)

### Lemma SP.0 (per-prime identity)

For all `k ≥ 1`, `m ≥ k`, and every prime `p`, with `n := m − k`:

```
ν_p((2n)!) − 2 ν_p((n+k)!) = κ_p(m) − W_p(m).
```

In particular `Crit_p(m)` ⟺ `ν_p((2n)!) ≥ 2 ν_p((n+k)!)`.

*Proof.* `(2m)! = (2n)! · (2m)(2m−1)⋯(2m−2k+1)` because `2n = 2m − 2k`, so
`ν_p((2m)!) = ν_p((2n)!) + W_p(m)`. Also
`κ_p(m) = ν_p((2m)!) − 2ν_p(m!)` and `(n+k)! = m!`. Subtract. ∎
(Verified on random instances in T1.7; equivalence of the product form with
the digit-sum form and with raw factorial divisibility in T1.5, T1.6.)

### Lemma SP.K (Kummer, with proof) and Lemma SP.1 (p = 2)

**SP.K.** For every prime `p` and `m ≥ 1`, `κ_p(m)` equals the number of
carries in the base-`p` addition `m + m`. Precisely: let `m = Σ_{j=0}^{d} a_j p^j`
with digits `a_j`, put `c_{−1} := 0` and, for `0 ≤ j ≤ d`,

```
c_j := 1 if 2a_j + c_{j−1} ≥ p, else 0;      b_j := 2a_j + c_{j−1} − p c_j.
```

Then `κ_p(m) = C := Σ_{j=0}^{d} c_j`.

*Proof.* First, `b_j ∈ {0,…,p−1}`: if `c_j = 0` then `0 ≤ b_j = 2a_j + c_{j−1} ≤ p−1`
by definition of `c_j`; if `c_j = 1` then `b_j = 2a_j + c_{j−1} − p ≥ 0` and
`b_j ≤ 2(p−1) + 1 − p = p − 1`. Telescoping,
`Σ_{j=0}^{d} (b_j + p c_j − c_{j−1}) p^j = Σ_j b_j p^j + c_d p^{d+1} = 2m`,
so `(b_0,…,b_d, c_d)` are the base-`p` digits of `2m` and
`s_p(2m) = Σ_j b_j + c_d = 2 s_p(m) + (C − c_d) − pC + c_d = 2 s_p(m) − (p−1) C`.
By Legendre's formula (`ν_p(x!) = (x − s_p(x))/(p−1)`, standard background),

```
κ_p(m) = ν_p((2m)!) − 2ν_p(m!) = [2 s_p(m) − s_p(2m)]/(p−1) = C.   ∎
```

(Integrality `(p−1) | 2s_p(m) − s_p(2m)` and the carry-count identity are
verified in T2.2, T2.3.)

**SP.1 (p = 2, as required by the brief).** `κ_2(m) = s_2(m)` for all `m ≥ 1`.

*Proof.* Doubling shifts binary digits, so `s_2(2m) = s_2(m)`; by the displayed
formula with `p = 2`: `κ_2(m) = 2 s_2(m) − s_2(2m) = s_2(m)`. ∎ (T2.1.)

---

## 1. Statement of the results

### Master Lemma SP

Fix an integer `k ≥ 2`. Let the parameters `M, q0, a, P, t` satisfy:

- **(H1)** `M` is an integer with `M ≥ 70000` and `M ≥ (4k)^{5/4}`;
- **(H2)** `q0` is an integer with `1 ≤ q0 ≤ M^{1/10}`, and `a ∈ {0,…,q0−1}`;
- **(H3)** `P` is a real number with `2 ≤ P ≤ M^{1/20}`;
- **(H4)** `t` is an integer with `t ≥ 3` and
  `log M / log P ≥ 60 ( 2k + log_2(2k) + t + 1 )`.

Write, for each prime `p ≤ P`:

```
L_p := ⌊ (4/5)·log M / log p ⌋ ,        e_p := ν_p(q0) ,
```

and define the **good set**

```
G := { m ∈ ℤ ∩ [M, 2M] :  m ≡ a (mod q0),  and for every prime p ≤ P:
        (C_p)  X_p^{[e_p, L_p)}(m) ≥ θ(p)·(L_p − e_p)/2 ,   and
        (S_p)  V_p(m) ≤ ν_p(2 q0) + J_p + t }.
```

Let `AP := { m ∈ ℤ ∩ [M,2M] : m ≡ a (mod q0) }`, so
`(M+1)/q0 − 1 ≤ |AP| ≤ (M+1)/q0 + 1` and `|AP| ≥ (M+1)/(2 q0) ≥ M^{9/10}/2`.

Then:

**(1) (criterion + no spike).** Every `m ∈ G` satisfies, for **every** prime
`p ≤ P`, the 727 criterion at `p`:

```
κ_p(m) ≥ ν_p( (2m)(2m−1)⋯(2m−2k+1) ) ,
```

equivalently (SP.0), with `n := m − k`: `ν_p((2n)!) ≥ 2 ν_p((n+k)!)` for every
prime `p ≤ P`; and the spike bound (S_p) holds for every `p ≤ P` by definition
of `G` (this is item (ii) of the brief, with the bound
`ν_p(2q0) + ⌊log_p(2k)⌋ + t`).

**(2) (gap form).** If moreover `log M / log P ≥ 120 (2k + log_2(2k) + t + 1)`,
then every `m ∈ G` has the surplus

```
κ_p(m) − W_p(m) ≥ (1/120) · log M / log p      for every prime p ≤ P.
```

**(3) (density, uniform in the progression).**

```
|G| ≥ (1 − Ê) · |AP| ,   where
Ê = Ê(M,P,t) := 3 P · exp( −(7/240)·log M/log P ) + 6·2^{−t} + 3 M^{−1/20}.
```

All constants are absolute; `k` enters only through (H1), (H4).

### Corollary SP-A (growing prime range `P(M) = exp(c √log M)`, density → 1)

Fix `k ≥ 2` and a real `c ∈ (0, 1/6]`. Set `P(M) := exp(c √(log M))`,
`t(M) := ⌊ √(log M)/20 ⌋`, and

```
M_A(k) := ⌈ exp( 400·(2k + log_2(2k) + 1)² ) ⌉ .
```

Then for every integer `M ≥ M_A(k)`, every `q0 ≤ M^{1/10}` and every residue
`a mod q0`, all but at most

```
E_A(M) := 18 · exp( − √(log M) / 120 )
```

fraction of the `m ∈ [M, 2M]` with `m ≡ a (mod q0)` satisfy **both** (i) the
727 criterion at every prime `p ≤ P(M)` and (ii) the spike bound
`V_p(m) ≤ ν_p(2q0) + J_p + t(M)` for every prime `p ≤ P(M)`. In particular the
density of such `m` tends to `1` as `M → ∞`, uniformly over all progressions of
modulus `≤ M^{1/10}`, with `P(M) = exp(√(log M)/6)` reached at `c = 1/6`.

### Corollary SP-B (fixed prime bound `P0`, polynomial-rate density 1)

Fix `k ≥ 2` and a real `P0 ≥ 2`. Set `β_0 := min( log 2/(120 log P0), 1/20 )`
and

```
M_B(k,P0) := ⌈ max( 70000, (4k)^{5/4}, P0^{20},
                    exp(360 log P0), exp( 120·log P0 ·(2k + log_2(2k) + 1) ) ) ⌉ .
```

Then for every integer `M ≥ M_B`, every `q0 ≤ M^{1/10}`, every `a`, all but at
most an `18·P0·M^{−β_0}` fraction of the `m ∈ [M,2M] ∩ (a mod q0)` satisfy the
727 criterion at every prime `p ≤ P0` together with the spike bound with
`t = ⌊log M/(120 log P0)⌋`. (Density `1` with a **power-of-M** error rate.)

### Corollary SP-C (the `δ_k` form requested by the brief)

Fix `k ≥ 2`. For every `δ < 1` there is an explicit `M_C(k, δ)` (from SP-A:
the least `M ≥ M_A(k)` with `18 e^{−√(log M)/120} ≤ 1−δ`; e.g. `δ = 1/2` needs
`log M ≥ (120 log 36)² ≈ 1.85·10^5` besides `M ≥ M_A(k)`) such that for all
`M ≥ M_C`, at least `δ·M` integers `m ∈ [M, 2M]` satisfy (i) at every prime
`p ≤ exp(√(log M)/6)` and (ii). Thus every fixed `δ_k < 1` is achieved, and
`δ_k → 1` is achieved in the strong form of SP-A (uniformly in APs), not just
for fixed `P0`.

Remark on strength: the brief's target shape asked for `δ_k > 0` with (i) for
`p ≤ P(M)`, and `δ_k → 1` possibly only for fixed `P0`. What is proved above is
stronger on both axes: density `→ 1` already for the growing range
`P(M) = exp(c√log M)`, `c ≤ 1/6`, and uniformly inside every AP of modulus up
to `M^{1/10}`, with the explicit gap (2) as an intersection-friendly surplus.

---

## 2. Deterministic lemmas

### Lemma SP.2 (interval valuation bound; demand ≤ bulk + spike)

For every prime `p`, every `k ≥ 1` and every `m ≥ k`:

```
W_p(m) ≤ ν_p((2k)!) + V_p(m).
```

*Proof.* The factors `2m−2k+1, …, 2m` are `2k` consecutive positive integers.
For `j ≥ 1` let `N_j := #{0 ≤ i < 2k : p^j | 2m−i}`; then
`W_p(m) = Σ_{j≥1} N_j` (each factor `2m−i` contributes `1` to `N_j` for exactly
`ν_p(2m−i)` values of `j`). Among `2k` consecutive integers, the multiples of
`p^j` number at most `⌈2k/p^j⌉ ≤ ⌊2k/p^j⌋ + 1`. For `j > J_p` we have
`p^j > 2k`, hence `N_j ≤ 1`; and `N_j = 0` for `j > V_p(m)` by definition of
`V_p`. Therefore, writing `V := V_p(m)`:

- if `V ≥ J_p`:
  `W_p ≤ Σ_{j=1}^{J_p} (⌊2k/p^j⌋ + 1) + Σ_{j=J_p+1}^{V} 1 = Σ_{j=1}^{J_p} ⌊2k/p^j⌋ + V`;
- if `V < J_p`:
  `W_p ≤ Σ_{j=1}^{V} (⌊2k/p^j⌋ + 1) ≤ Σ_{j=1}^{J_p} ⌊2k/p^j⌋ + V`.

By Legendre, `ν_p((2k)!) = Σ_{j≥1} ⌊2k/p^j⌋ = Σ_{j=1}^{J_p} ⌊2k/p^j⌋`. ∎

(T3.1, T3.2. The exact refinement `W_p(m) = ν_p(binom(2m,2k)) + ν_p((2k)!)`,
verified in T3.3, shows SP.2 is the Kummer bound `ν_p(binom(2m,2k)) ≤ V_p`;
we only need the inequality.)

This lemma is where the brief's note (a) is honoured: the demand at `p ≤ 2k`
contains the bulk `ν_p((2k)!) ≈ 2k/(p−1)` **plus** the spike part; the carry
supply below is engineered to cover `ν_p((2k)!) + spike`, not just the spike.

### Lemma SP.3 (forced carries from large digits, masked positions)

For every prime `p`, every `m ≥ 1`, and all integers `0 ≤ e ≤ L`:

```
κ_p(m) ≥ X_p^{[e,L)}(m).
```

*Proof.* By SP.K, `κ_p(m) = Σ_j c_j`. If `a_j ≥ ⌈p/2⌉` then
`2a_j + c_{j−1} ≥ 2⌈p/2⌉ ≥ p`, so `c_j = 1` **regardless of the incoming
carry**. Hence `κ_p(m) ≥ #{j ≥ 0 : a_j ≥ ⌈p/2⌉} ≥ X_p^{[e,L)}(m)`. ∎ (T4.1.)

### Lemma SP.4 (sufficiency chain)

Let `p` be a prime, `m ≥ k`, `0 ≤ e ≤ L`. If

```
X_p^{[e,L)}(m) ≥ ν_p((2k)!) + V_p(m),
```

then `Crit_p(m)` holds, i.e. `κ_p(m) ≥ W_p(m)`, with surplus
`κ_p(m) − W_p(m) ≥ X_p^{[e,L)}(m) − ν_p((2k)!) − V_p(m)`.

*Proof.* `κ_p ≥ X` (SP.3) `≥ ν_p((2k)!) + V_p ≥ W_p` (SP.2). ∎
(T5.1: 187k+ random instances; T10.1: exhaustively inside three APs at
`M = 2·10^5`, `k = 3`, all `p ≤ 13` — zero violations.)

### Lemma SP.5 (spike solution sets are single residue classes)

Let `p` be prime, `T ≥ 1`, `i ∈ {0,…,2k−1}`.

- If `p` is odd: `{ m ∈ ℤ : p^T | 2m−i } = { m : m ≡ 2^{−1} i (mod p^T) }`,
  a single class mod `p^T`.
- If `p = 2` and `i` is odd: the set is empty (`2m−i` is odd).
- If `p = 2` and `i = 2i'`: `2^T | 2m−i ⟺ 2^{T−1} | m−i'`, a single class
  mod `2^{T−1}`.

In all nonempty cases the set is one class modulo `p^{T − ν_p(2)}`.

*Proof.* Immediate (`2` is invertible mod `p^T` for odd `p`). ∎ (T7.1.)

---

## 3. Counting lemmas

### Lemma SP.6 (residue class in an interval)

Let `M ≥ 1`, `Q ≥ 1` be integers and `c` any residue mod `Q`. Then

```
(M+1)/Q − 1  ≤  #{ x ∈ ℤ ∩ [M, 2M] : x ≡ c (mod Q) }  ≤  (M+1)/Q + 1 .
```

*Proof.* `ℤ ∩ [M,2M]` consists of `M+1` consecutive integers. Write
`M+1 = sQ + r`, `0 ≤ r < Q`. The interval is `s` full blocks of `Q`
consecutive integers plus `r` leftover; each full block contains exactly one
member of the class, the leftover contains `0` or `1`. So the count lies in
`{s, s+1}`, and `s > (M+1)/Q − 1`, `s + 1 ≤ (M+1)/Q + 1`. ∎

In particular `|AP| ≥ (M+1)/q0 − 1 ≥ (M+1)/(2q0)` whenever `M+1 ≥ 2q0`
(true under (H1)–(H2)), and `(M+1)/(2q0) ≥ M^{9/10}/2` since `q0 ≤ M^{1/10}`.

### Lemma SP.7 (CRT inside the progression)

Write `q0 = p^{e_p} q'` with `p ∤ q'`. Let `Λ ≥ e_p`, and let `a mod q0`,
`r mod p^Λ` be given. Then

```
{ m ∈ ℤ : m ≡ a (mod q0), m ≡ r (mod p^Λ) }
```

is empty if `r ≢ a (mod p^{e_p})`, and otherwise is a **single** residue class
modulo `q' p^Λ = q0 p^{Λ − e_p}`.

*Proof.* The condition `m ≡ a (mod q0)` splits (CRT, `gcd(q', p^{e_p}) = 1`)
into `m ≡ a (mod q')` and `m ≡ a (mod p^{e_p})`. The pair
`m ≡ a (mod p^{e_p})`, `m ≡ r (mod p^Λ)` is inconsistent unless
`r ≡ a (mod p^{e_p})`, in which case it is equivalent to `m ≡ r (mod p^Λ)`.
CRT for the coprime moduli `q'` and `p^Λ` finishes. ∎ (T9.1.)

**Consequence (digit patterns inside the AP).** Fix `p ≤ P` and let
`Λ := L_p − e_p ≥ 1`. For `m ≡ a (mod q0)`, the digits of `m` in positions
`0,…,e_p−1` are determined by `a mod p^{e_p}`; and for each pattern
`w ∈ {0,…,p−1}^Λ` of digits in positions `e_p,…,L_p−1`, the set
`{m ≡ a (q0) : digits e_p..L_p−1 of m equal w}` is exactly one residue class
modulo `q0 p^{Λ}` (apply SP.7 with the unique `r mod p^{L_p}` having low
digits from `a` and top digits `w`). By SP.6, each such class meets
`[M, 2M]` in at most `(M+1)/(q0 p^{Λ}) + 1` integers.

### Lemma SP.8 (Chernoff lower tail, counting form, constant 1/8)

Let `p` be prime, `Λ ≥ 1`, `θ = θ(p) = ⌊p/2⌋/p`, `μ := θΛ`. Then

```
#{ w ∈ {0,…,p−1}^Λ : #{j : w_j ≥ ⌈p/2⌉} ≤ μ/2 }  ≤  p^Λ · e^{−μ/8}.
```

*Proof.* Normalize: let `w` be uniform on `{0,…,p−1}^Λ`; the coordinates are
independent and each is large with probability exactly `θ` (there are exactly
`⌊p/2⌋` large values). So `X := #{j : w_j large} ~ Bin(Λ, θ)`. For any
`λ > 0`, by Markov applied to `e^{−λX}`:

```
P(X ≤ μ/2) ≤ e^{λμ/2} · E[e^{−λX}] = e^{λμ/2} (1 − θ + θe^{−λ})^Λ
           ≤ exp( λμ/2 + μ(e^{−λ} − 1) ),
```

using `1 + y ≤ e^y` with `y = θ(e^{−λ}−1)`. Choose `λ = log 2`:
the exponent is `μ(log 2 /2 + 1/2 − 1) = −μ·(1 − log 2)/2 ≤ −μ/8`, since
`(1 − log 2)/2 ≥ 0.1534 > 1/8` (T11.d). Multiply by `p^Λ`. ∎

(The bound `P(X ≤ μ/2) ≤ e^{−μ/8}` is verified against exact rational tail
sums for many `(Λ, θ)` in T6.c; sharper KL-form bounds in T6.b are available
but not needed.)

---

## 4. The threshold lemma

### Lemma SP.9 (carry supply beats bulk + corrected spike bound)

Assume (H1)–(H4) of the Master Lemma. Then for **every** prime `p ≤ P`,
writing `u_p := log M / log p ( ≥ log M/log P )`:

```
θ(p)·(L_p − e_p)/2  ≥  ν_p((2k)!) + ν_p(2 q0) + J_p + t ,
```

and moreover the two sides differ by at least
`(1/60)·u_p − (2k + log_2(2k) + t + 1/6)`, a quantity that is `≥ 0` under
(H4) and `≥ u_p/120` under the hypothesis of part (2)
(`log M/log P ≥ 120(2k + log_2(2k) + t + 1)`).

*Proof.* All the bounds below are uniform in `p ≤ P`.

Lower bound for the left side: `θ(p) ≥ 1/3`;
`L_p ≥ (4/5)u_p − 1` (definition of `L_p` as a floor);
`e_p = ν_p(q0) ≤ log q0/log p ≤ (1/10)·u_p` (by (H2), `q0 ≤ M^{1/10}`). Hence

```
θ(p)(L_p − e_p)/2 ≥ (L_p − e_p)/6 ≥ ( (7/10)·u_p − 1 )/6 = (7/60)u_p − 1/6.
```

Upper bound for the right side: `ν_p((2k)!) = (2k − s_p(2k))/(p−1) ≤ 2k−1`
(Legendre, `s_p(2k) ≥ 1`); `ν_p(2q0) = ν_p(2) + e_p ≤ 1 + (1/10)u_p`;
`J_p ≤ log_2(2k)`. Hence

```
RHS ≤ (2k − 1) + 1 + (1/10)u_p + log_2(2k) + t.
```

Subtracting, and using `7/60 − 1/10 = 1/60` (T11.f):

```
LHS − RHS ≥ (1/60)·u_p − ( 2k + log_2(2k) + t + 1/6 ).
```

Under (H4), `u_p ≥ log M/log P ≥ 60(2k + log_2(2k) + t + 1)`, so
`(1/60)u_p ≥ 2k + log_2(2k) + t + 1 > 2k + log_2(2k) + t + 1/6` and
`LHS ≥ RHS`. Under the part-(2) hypothesis,
`2k + log_2(2k) + t + 1 ≤ (1/120)·log M/log P ≤ u_p/120`, so
`LHS − RHS ≥ (1/60)u_p − (1/120)u_p = u_p/120`. ∎

(Numeric check of exactly this inequality — in reduced form at the worst point
`u = log M/log P` and with exact `θ(p)` at small primes — in T11.e; the exact
per-instance version, as a `Fraction` comparison, gates every configuration of
the large-`M` sampling test T13.)

Note `L_p − e_p ≥ 3·(2k + log_2(2k) + t + 1) − stuff > 0`; indeed
`(L_p−e_p)/6 ≥ (7/60)u_p − 1/6 ≥ RHS ≥ t ≥ 3`, so `L_p − e_p ≥ 18 ≥ 1` and
`Λ := L_p − e_p` is a legitimate pattern length; also
`q0·p^{L_p−e_p} ≤ M^{1/10}·M^{4/5} ≤ M^{9/10}` (since `p^{L_p} ≤ M^{4/5}` by
the floor definition), so the moduli used below fit inside `[M,2M]`.

---

## 5. Proof of the Master Lemma

Assume (H1)–(H4). Fix `k, M, q0, a, P, t` accordingly and write
`Λ_p := L_p − e_p`, `μ_p := θ(p) Λ_p`.

### 5.1 Part (1): G ⟹ criterion at every p ≤ P (and part (2))

Let `m ∈ G` and let `p ≤ P` be prime. Chain:

```
κ_p(m)  ≥  X_p^{[e_p, L_p)}(m)          (SP.3)
        ≥  μ_p/2                        (condition C_p)
        ≥  ν_p((2k)!) + ν_p(2q0) + J_p + t     (SP.9, uses H4)
        ≥  ν_p((2k)!) + V_p(m)          (condition S_p)
        ≥  W_p(m)                       (SP.2).
```

This is `Crit_p(m)`; by SP.0 it is `ν_p((2n)!) ≥ 2ν_p((n+k)!)` for
`n = m − k` (`m ≥ M ≥ (4k)^{5/4} ≥ 4k > k`, so `n ≥ 1` and `W_p` is defined).
Under the part-(2) hypothesis, SP.9 gives the third inequality with surplus
`≥ u_p/120`, hence `κ_p(m) − W_p(m) ≥ (1/120)·log M/log p`. ∎(1),(2)

### 5.2 Part (3): counting the bad set

For each prime `p ≤ P` define inside `AP`:

```
BadC_p := { m ∈ AP : X_p^{[e_p,L_p)}(m) < μ_p/2 },
BadS_p := { m ∈ AP : V_p(m) > ν_p(2q0) + J_p + t },
Bad    := ∪_{p ≤ P} (BadC_p ∪ BadS_p),          so  AP ∖ G = Bad.
```

**Bad carries.** `X_p^{[e_p,L_p)}(m)` depends only on the digit pattern
`w ∈ {0,…,p−1}^{Λ_p}` of `m` in positions `e_p..L_p−1`. By SP.8 the number of
patterns with `X ≤ μ_p/2` is at most `p^{Λ_p} e^{−μ_p/8}`; by the consequence
of SP.7 + SP.6, each pattern is realized by at most
`(M+1)/(q0 p^{Λ_p}) + 1` elements of `AP`. Hence

```
|BadC_p| ≤ p^{Λ_p} e^{−μ_p/8} · ( (M+1)/(q0 p^{Λ_p}) + 1 )
         ≤ (M+1)·e^{−μ_p/8}/q0 + p^{Λ_p},     and   p^{Λ_p} ≤ p^{L_p} ≤ M^{4/5}.
```

Uniformly for `p ≤ P`: `μ_p/8 = θ(p)Λ_p/8 ≥ Λ_p/24 ≥ ((7/10)u_p − 1)/24`
(as in SP.9), so `e^{−μ_p/8} ≤ e^{1/24}·exp(−(7/240)·log M/log P)`. Summing
over the `π(P) ≤ P` primes:

```
Σ_{p≤P} |BadC_p| ≤ (M+1)/q0 · e^{1/24} P exp(−(7/240)·log M/log P) + P·M^{4/5}.
```

**Bad spikes.** Let `T_p := ν_p(2q0) + J_p + t + 1`. If `m ∈ BadS_p` then
`p^{T_p} | 2m−i` for some `0 ≤ i < 2k`.

- `p` odd: `T_p = e_p + J_p + t + 1 > e_p`. By SP.5 the solutions of
  `p^{T_p} | 2m−i` form one class mod `p^{T_p}`; by SP.7 (with `Λ = T_p`)
  its intersection with the progression `a mod q0` is empty or one class mod
  `q0 p^{T_p − e_p} = q0 p^{J_p + t + 1}`; by SP.6 that class meets `[M,2M]`
  in at most `(M+1)/(q0 p^{J_p+t+1}) + 1` points. Summing over the `2k`
  values of `i` and using `2k < p^{J_p+1}`:

  ```
  |BadS_p| ≤ 2k·(M+1)/(q0 p^{J_p+t+1}) + 2k ≤ (M+1)·p^{−t}/q0 + 2k.
  ```

- `p = 2`: `T_2 = e_2 + 1 + J_2 + t + 1 ≥ 1`, so odd `i` give no solutions;
  for `i = 2i'` (`0 ≤ i' < k`), `2^{T_2} | 2m−i ⟺ 2^{T_2−1} | m−i'` (SP.5),
  one class mod `2^{T_2−1}`, `T_2 − 1 = e_2 + J_2 + t + 1 > e_2`; by SP.7,
  inside the AP this is empty or one class mod `q0·2^{J_2+t+1}`; by SP.6 at
  most `(M+1)/(q0 2^{J_2+t+1}) + 1` points each. Summing over the `k` values
  of `i'` and using `k ≤ 2k < 2^{J_2+1}`:

  ```
  |BadS_2| ≤ k·(M+1)/(q0 2^{J_2+t+1}) + k ≤ (M+1)·2^{−t}/q0 + 2k.
  ```

Uniformly, `|BadS_p| ≤ (M+1) p^{−t}/q0 + 2k`, and, summing over `p ≤ P` with
`Σ_{p≤P} p^{−t} ≤ Σ_{n≥2} n^{−t} ≤ 3·2^{−t}` for `t ≥ 3` (T11.b):

```
Σ_{p≤P} |BadS_p| ≤ 3·2^{−t}(M+1)/q0 + 2kP.
```

**Assembly.** Using `|AP| ≥ (M+1)/(2q0)` (SP.6 and (H1), (H2)):

```
|Bad|/|AP| ≤ 2 e^{1/24} P exp(−(7/240) log M/log P)
             + 2 q0 P M^{4/5}/(M+1)
             + 6·2^{−t}
             + 4 k q0 P/(M+1).
```

Now bound each boundary term. Since `q0 ≤ M^{1/10}` and `P ≤ M^{1/20}` (H3):
`2 q0 P M^{4/5}/(M+1) ≤ 2 P M^{−1/10} ≤ 2 M^{−1/20}`; and
`4 k q0 P/(M+1) ≤ 4k P M^{−9/10} ≤ 4k·M^{1/20 − 9/10} = 4k M^{−17/20} ≤ M^{−1/20}`
because `4k ≤ M^{4/5}` by (H1) (`M ≥ (4k)^{5/4}`). Also `2e^{1/24} < 3`.
Hence

```
|Bad|/|AP| ≤ 3P exp(−(7/240)·log M/log P) + 6·2^{−t} + 3M^{−1/20} = Ê,
```

and `|G| = |AP| − |Bad| ≥ (1 − Ê)|AP|`. ∎ (Master Lemma)

---

## 6. Proofs of the corollaries

### SP-A

Take `P := exp(c√(log M))`, `t := ⌊√(log M)/20⌋`, `q0, a` arbitrary with
`q0 ≤ M^{1/10}`. Check the hypotheses for `M ≥ M_A(k)`; write `L := log M`.

- (H1): `M_A(k) ≥ exp(400·(2k+log_2(2k)+1)²) ≥ exp(400·49) > 70000` and
  `exp(400(2k+1)²...) ≥ (4k)^{5/4}` (crude: `400(2k+...)² ≥ (5/4)log(4k)` for
  all `k ≥ 2`). ✓
- (H3): `P ≤ M^{1/20} ⟺ c√L ≤ L/20 ⟺ √L ≥ 20c`; since `c ≤ 1/6` this needs
  `L ≥ (10/3)² = 100/9`, true for `M ≥ 70000 > e^{100/9}`. Also `P ≥ 2`
  whenever `c√L ≥ log 2`, true here; if `P < 2` the statement is vacuous
  anyway. ✓
- (H4): `log M/log P = √L/c ≥ 6√L`. Need `6√L ≥ 60(2k + log_2(2k) + t + 1)`
  with `t ≤ √L/20`: since `60·√L/20 = 3√L`, it suffices that
  `3√L ≥ 60(2k + log_2(2k) + 1)`, i.e. `√L ≥ 20(2k + log_2(2k) + 1)`, which
  is the definition of `M_A(k)`. Also `t ≥ 3 ⟺ √L ≥ 80`, implied. ✓

Master (3) then gives, using `c − 7/(240c) ≤ −1/120` for `0 < c ≤ 1/6`
(the map `c ↦ c − 7/(240c)` is increasing; equality `−1/120` at `c = 1/6`;
T11.a):

```
3P exp(−(7/240)√L/c) = 3 exp( (c − 7/(240c))√L ) ≤ 3 e^{−√L/120};
6·2^{−t} ≤ 12·2^{−√L/20} = 12 e^{−(log 2/20)√L} ≤ 12 e^{−√L/120};
3M^{−1/20} = 3e^{−L/20} ≤ 3 e^{−√L/120}       (L/20 ≥ √L/120 always).
```

Sum: `Ê ≤ 18 e^{−√(log M)/120} = E_A(M)`. Master (1) gives the criterion (i)
at every `p ≤ P(M)` and the spike bound (ii) on `G`. ∎

### SP-B

Take `P := P0` (constant), `t := ⌊log M/(120 log P0)⌋`. For `M ≥ M_B`:
(H1) ✓ by definition; (H3) `P0 ≤ M^{1/20} ⟺ M ≥ P0^{20}` ✓;
`t ≥ 3 ⟺ log M ≥ 360 log P0` ✓; (H4): need
`log M/log P0 ≥ 60(2k + log_2(2k) + 1) + 60t`; since
`60 t ≤ (1/2)·log M/log P0`, it suffices that
`(1/2)log M/log P0 ≥ 60(2k + log_2(2k) + 1)`, i.e.
`log M ≥ 120 log P0 (2k + log_2(2k) + 1)` ✓. Then

```
Ê ≤ 3P0·M^{−7/(240 log P0)} + 12·M^{−log 2/(120 log P0)} + 3M^{−1/20}
  ≤ (3P0 + 12 + 3)·M^{−β_0} ≤ 18 P0 · M^{−β_0}
```

with `β_0 = min(log2/(120 log P0), 1/20)` (note
`7/(240 log P0) > log 2/(120 log P0)`, and `3P0 + 15 ≤ 18P0` for `P0 ≥ 2`). ∎

### SP-C

Immediate from SP-A with `q0 = 1`: `|AP| = M + 1 > M`, so the good count is
`≥ (1 − E_A(M))·M`, and `E_A(M) ≤ 1 − δ` for `M ≥ M_C(k,δ)` as stated. ∎

---

## 7. Remarks: sharpness, and what this route does and does not claim

1. **What is proved is only about primes `p ≤ P(M)`.** Membership `n ∈ S_k`
   (`n = m − k`) additionally requires the criterion at every prime
   `p > P(M)`, in particular at the primes in `(√(2n), n+k]` where PROBLEM.md
   shows the window `n+1,…,n+k` must be `√(2n)`-smooth. Nothing here touches
   that regime; Lemma SP is a building block designed for intersection with
   other constraints (hence the AP-uniform form and the surplus (2)).

2. **The `ν_p(2q0)` correction is necessary.** In the progression
   `m ≡ 0 (mod 2^{10})` every `m` has `ν_2(2m) ≥ 11`, so a spike bound
   without the `ν_p(2q0)` term is false (falsified numerically in T7.2, and
   visible in the density data T8: in that AP the demand at `p = 2` is
   `≥ 11 + ν_2((2k)!)` for the `i = 0` factor). The corrected bound makes the
   spike event genuinely rare inside every admissible AP (T8.4).

3. **Constant improvements (all unproved here; marked heuristic).**
   (h1) Replacing the per-digit Chernoff bound by the carry-chain large
   deviation analysis (Lemma 15 of the background paper) effectively replaces
   `θ(p) ≥ 1/3` by `1/2` and the constant `1/8` by an entropy `I(δ)` up to
   `log 2`, pushing the admissible `c` in `P(M) = e^{c√log M}` from our
   `1/6` toward `√((7/10)·log 2) ≈ 0.70` and improving every rate constant;
   (h2) re-optimizing `L_p = ⌊(1−η)log M/log p⌋` and `q0 ≤ M^β` under the
   constraints `β < η` and `β < (1−η)/7` (this proof) allows any `β < 1/8`
   by the identical argument (constants not re-tracked), and heuristically
   any `β < 1/6` with (h1). None of these is needed downstream; we fixed
   `η = 1/5`, `β = 1/10`, `c ≤ 1/6`, Chernoff constant `1/8` to keep every
   constant explicit and verified.

4. **Where the proof would break if pushed.** (i) `P(M)` cannot exceed
   `exp(O(√log M))` by this counting: the union over `π(P)` primes must be
   beaten by `exp(−c'·log M/log P)`, forcing `log P ≪ √log M` — same barrier
   as in the background paper (its Remark 1). (ii) The AP modulus cannot
   reach `M^{1/5}` here: the pattern-boundary term `π(P)·p^{L_p}` must stay
   below `M/q0`.

5. **Quantifier structure (explicit).** In SP-A: `∀k ≥ 2 ∀c ∈ (0,1/6]
   ∃M_A(k) explicit ∀M ≥ M_A(k) ∀q0 ≤ M^{1/10} ∀a mod q0`: at least
   `(1 − 18e^{−√(log M)/120})·|AP|` integers `m ∈ AP` satisfy
   `∀p ≤ e^{c√log M}`: (i) ∧ (ii). `k` never depends on `M`; the constants
   `70000, 4/5, 1/10, 1/20, 1/60, 1/120, 7/240, 1/8, 3, 6, 12, 18` are
   absolute.

---

## 8. Numerical verification map (`verify_sp.py`)

| Lemma / claim | Test(s) | Type |
|---|---|---|
| criterion implementations vs PROBLEM.md data (S_1..S_4) | T1.0–T1.4 | exact, exhaustive |
| product form ⟺ digit form ⟺ factorial divisibility | T1.5, T1.6 | exact, exhaustive |
| SP.0 identity | T1.7 | exact, random |
| SP.1 (κ_2 = s_2), SP.K (Kummer) | T2.1–T2.3 | exact |
| SP.2 interval bound + exact refinement | T3.1–T3.3 | exact |
| SP.3 masked forced carries | T4.1 | exact, random |
| SP.4 sufficiency chain | T5.1 (random), T10.1 (exhaustive, in 3 APs) | exact |
| SP.8 Chernoff 1/8 (and sharper variants) | T6.a–T6.d | exact rational |
| SP.5 spike classes; necessity of ν_p(2q0) correction | T7.1, T7.2 | exact |
| SP.6/SP.7 counting + CRT in AP | T9.1 | exact |
| SP.9 threshold (reduced + exact small-prime form) | T11.e, T13.thr | numeric / exact Fraction |
| scalar constants (T11.a,b,c,d,f) | T11 | exact / margin |
| packaged lemma at `M = 2^64 … 2^200, 10^60`, incl. APs `q0 = 24, 2^10·3^4` | T13 | exact sampling, 20000 pts/config |
| density data `k=3, P0=13` plain + APs; union-bound consistency; trend to 1 | T8 | exact, exhaustive to `M = 10^6` |

Density calibration (brief item (c), `k = 3`, `P0 = 13`): measured density of
(i) for all `p ≤ 13` on `[M, 2M]` rises with `M` — exactly `0.6264` at
`M = 10^5` and `0.7970` at `M = 10^6` (T8, exhaustive), with the failure rate
bounded by the per-prime union sum (`0.4414` resp. `0.2222`) and dominated by
the smallest primes, exactly as the union-bound structure predicts; in the AP
`m ≡ 7 (mod 24)` at `M = 10^6` the density is `0.8237`. At `M = 2^{64}` the
sampled density of the *good set* `G` itself is `0.736`, and `0.946`–`0.998`
at `M = 2^{200}, 10^{60}` (T13), with zero violations of `G ⟹ (i)` in
80000 exact samples. Two honest caveats visible in the data: the *explicit*
bound `E_A(M)` is vacuous (`> 1`) at numerically reachable `M` (the asymptotic
claim is the content of SP-A/SP-B; the mechanism is what is verified exactly);
and in the extreme progression `m ≡ 0 (mod 2^{10})` at `M = 10^6` the measured
density of (i) is `0.0000` — there the forced demand at `p = 2` is
`≥ 11 + ν_2((2k)!)` while `κ_2(m) = s_2(m) ≈ 10` at that scale, so failure is
certain for small `M`; SP-A still applies for `M ≥ M_A(k)` because the masked
digit supply `s_2` in positions `[e_2, L_2)` grows like `(2/5)log_2 M` — this
is precisely why the threshold lemma SP.9 needs `L_p − e_p` large and why the
AP-uniform statement is a genuinely asymptotic one (spike condition (ii) with
the corrected threshold is already rare there: rate `0.044`, T8.4).
