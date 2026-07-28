# Route R20 — superlinear (v log v) displacement witnesses, NO side

Filed by the coordinator from the agent's returned text (its harness blocked writing
`.md` files). All machine claims come from code in this directory. The vectorised checker
in `framework.py` is cross-validated against `experiments/apcheck.py` (2000 random
permutations at k=3,4 against both apcheck implementations, plus 400 exact violation-set
comparisons against a literal enumeration).

## 0. Verdict first

**The mission premise — "displacement Θ(v log v) is consistent with every certificate so
far" — is FALSIFIED for the natural one-parameter family, and the structural picture
("logarithmically growing lag") is not what optimal finite witnesses look like.**

1. **New extinction certificates.** For φ_α(v) = ⌈α·v·log₂(2v)⌉, the minimal α admitting a
   φ_α-bounded avoider:

   | N | 20 | 30 | 45 | 60 | 90 | 130 |
   |---|----|----|----|----|----|-----|
   | α*(N) | 0.45 | 0.50 | 0.50 | 0.50 | 0.50 | **> 0.50** |

   So φ_{0.5} admits no monotone-4-AP-free permutation of [1..130] (CEGAR UNSAT, 4947
   rounds, 1721 s) and is dead as a 196-NO profile by Lemma 6. Fit on the two certified
   wall points: N*(α) ≈ 20·e^{37(α−0.45)}, versus Remark 17's N*(C) ≈ 4·e^{4.15(C−1.25)} —
   the wall recedes ≈9× more slowly per unit parameter, but it is still a wall.
   *(Coordinator note: this UNSAT was single-solver; an eager two-solver re-verification
   was run separately — see `experiments/verify_r20_alpha.out`.)*

2. **Witness anatomy.** The φ_{0.5}-bounded avoider of [1..90] is not a log-lag
   interleaving: exact cut points {1,2,4,11,90}, emission order
   `[1..11] [12..31] [61..90] [44..60] [32..43]` — geometric ratio ≈2.8 blocks in order,
   then a reversed tail, plus one advanced value. Delay is not concentrated on high-v₂
   values (mean pos/v = 1.11, 1.15, 1.26, 1.05 for v₂ = 0,1,2,3).

3. **Proved:** Lemma R20-1, the first *non-interval* block architecture for 196.
4. **Proved:** Propositions R20-2 and R20-3 — every member of that architecture is either
   linear-displacement on some infinite AP (doomed) or has O(log v)-thin classes (no
   reduction). Machine-confirmed: CLS(3,a) UNSAT at N=250 over ALL within-class orders,
   while CLS(5,a) is still SAT at N=250.
5. **Methodological (portfolio-wide).** A design whose AP-restriction is linear with
   constant C dies only near N ≈ 4e^{4.15(C−1.25)} (≈6·10³ at C=3, ≈10⁷ at C=5, ≈10⁹ at
   C=6). Verification to M = 10⁴–10⁵ cannot certify or refute such designs; R1's ratio-5/6
   island and CLS(5,a)/CLS(6,a) sit in this blind spot. (Folded into CORE.md Remark 27.)
6. **Open:** whether α*(N) → ∞ (only two wall points certified); whether the minimal
   profile's shape is asymptotically linear. Probe: with pos(v) ≤ 2v imposed only for
   v ≤ 12, N=90 is SAT while the full C=2 profile is UNSAT at N=90 — so the C=2 wall is
   not an initial-segment artifact.

## 1. Lemma R20-1 (class architecture) — proved, machine-verified

**Definition.** t : ℕ → ℤ≥0 is *AP-alternating* if for every 4-AP (x, x+d, x+2d, x+3d),
writing t_i = t(x+id), one of: (i) t₀=t₁=t₂=t₃; (ii) t₀=t₂ < min(t₁,t₃);
(iii) t₁=t₃ < min(t₀,t₂).

**Lemma R20-1.** For b ≥ 3, t AP-alternating, j(v) = ⌊log_b v⌋, c(v) = j(v) + t(v): for
every 4-AP the class sequence (c₀,c₁,c₂,c₃) is neither strictly increasing nor strictly
decreasing.

*Proof.* Block gap: j₀ ≤ j₁ ≤ j₂ ≤ j₃ and x+3d < 3(x+d) ≤ b(x+d) give j₃ ≤ j₁+1, so with
k := j₁ the triple (j₁,j₂,j₃) ∈ {(k,k,k), (k,k,k+1), (k,k+1,k+1)}. Checking each against
the three AP-alternating cases eliminates strict monotonicity in both directions. ∎

**Lemma R20-1a.** For fixed s ≥ 0 and strictly increasing ρ, t(v) := ρ(v₂(v+s)) is
AP-alternating.
**Lemma R20-1b.** With ρ strictly increasing and ρ(0)=0 every class is finite, so
"classes in increasing index order, arbitrary order inside" is a permutation of ℕ of
order type ω (CORE Lemma 1).

**Sharpness** (`classlemma.py`, all APs with x+3d ≤ 3000): verified for (b,ρ) =
(3,a), (4,a), (5,a), (3,2a), (3,a+⌊a/2⌋). Both hypotheses are necessary — b=2, ρ(a)=a
fails at x=1, d=6 (the 2^M(1,6,11,16) family); b=3, ρ=⌊a/2⌋ (only weakly increasing)
fails at x=1, d=5.

**Profile.** |class c| ≍ b^c, so pos(v) ≍ v·b^{ρ(v₂(v))}; since ρ must be strictly
increasing, at v = 2ⁿ this gives pos(v) ≍ v^{1+log₂ b} — polynomial, never Θ(v log v). So
this architecture and the v log v target are incompatible (not a defect for 196, since
Lemma 6 accepts any profile).

## 2. Proposition R20-2 (AP-restriction principle)

Let a be monotone-4-AP-free and P = {r+qn : n ≥ 0} infinite. The induced order on P,
transported by n ↦ r+qn, is a monotone-4-AP-free permutation of ℕ of order type ω. Hence
Theorem 12 gives limsup_n pos_P(n)/n ≥ 9/8 for **every** P.
(Filed as CORE.md Corollary 26.)

**Design principle D1** (conditional on linear extinction at every C): a NO-witness must
satisfy sup_n pos_P(n)/n = ∞ for every infinite AP P.

## 3. Proposition R20-3 (dichotomy for class architectures)

For b ≥ 3, t AP-alternating, c = ⌊log_b ·⌋ + t, exactly one of:
**(a)** t is constant on the tail of some infinite AP P ⟹ the induced order on P is an
eventually contiguous geometric block ordering of ratio b, so limsup pos_P(n)/n ≤ b(1+o(1))
— P violates D1;
**(b)** t is non-constant on every AP tail ⟹ t(u) ≠ t(w) whenever u < w < 2u, so every
fibre meets every block in ≤ ⌊log₂ b⌋+1 values and |class c| = O(log v) — no reduction.
For t(v) = ρ(v₂(v)), alternative (a) always holds (t ≡ ρ(0) on the odds).

## 4. Machine results

**α-wall** (`profile_sat.py`, `alpha_wall.py`, `alpha_wall.log`): N=20: α ≤ 0.40 UNSAT,
α=0.45 SAT. N=30/45/60/90: α ≤ 0.45 UNSAT, α=0.50 SAT. N=130: α ≤ 0.45 UNSAT and α=0.50
UNSAT (1721 s, 4947 rounds).

**Class architectures, impossibility over ALL within-class orders** (`classsat.py`):
CLS(3,a) SAT at 60/100/160, **UNSAT at 250**; CLS(5,a) SAT at 100/160/250 (895 s).
Diagnosis (`oddcuts.py`): in CLS(b,a) every odd value has class = block_b(v), so the odd
restriction is the in-order geometric block ordering with cuts (b^j+1)/2 — for b=3 that is
1,2,5,14,41,122 (R1's "SAT shoulder", V_{j+1} = 3V_j − 1), and that system alone is SAT at
n = 40, 70, 110 and **UNSAT at n = 160** (odd values ≤ 319). Side datum for R1: an UNSAT on
a ratio-3 cut chain inside the predicted shoulder — evidence against the optimistic
reading of Conjecture W for ratio-3 chains.

**Explicit rules — failure ledger** (`scan.py` 190 rules to M=1200, `banded.py`,
`prefixfix.py`): every order-type-ω rule tried dies, all with largest term ≤ 33. Controls
behave correctly (pure σ and pure τ survive to M=1200 but are not of order type ω).

| family | mechanism | canonical first kill |
|---|---|---|
| L-ASC (within-class σ, τ, ascending, bit-reversal) | class sequence weakly increasing with one same-class adjacent pair the rule fails to invert | CLS(3,a)×σ: (5,7,9,11) |
| L-DESC (descending, T(3), reversed-block-ascending) | too many inversions: four same-class AP values become a decreasing 4-AP | CLS(3,a)×desc: (9,11,13,15) |
| L-BAND (bands B=2,3,4, permutation π) | bands fix L-ASC pairs but manufacture L-DESC kills at band crossings | CLS(6,a) B=3: (21,23,25,27) |
| L-CROSS (τ-based within class) | the class cut splits τ's digit cycle | CLS(6,a)×τ₁₂₀: (1,11,21,31) |
| L-SMALL (all) | blocks 0,1,2 too small for the asymptotic mechanism | universal; matches R3 (all 26 orderings died by value 24) |
| L-3ADIC (ρ(v₃)) | ρ(v₃) is not AP-alternating | CLS3(3,a): (1,4,7,10) |

Also negative: profile-bounded beam/greedy reaches only v=27 at α=0.5; CP-SAT is worse
than CEGAR here (UNKNOWN at N=90 in 181 s).

## 5. Proof-attempt skeleton, with honest gaps

- Case A (class sequence strictly monotone): CLOSED by Lemma R20-1.
- Case B (exactly one same-class adjacent pair): OPEN — R3's forced-pair system on
  non-interval classes; source of the L-ASC/L-DESC ledger.
- Case C (≥2 contacts / all four in one class): OPEN — reduces to the finite 196 problem
  on an interval of length ≈ b^c/2 with Case-B boundary conditions.
- Global: Proposition R20-3 — even if B and C were solvable, the design violates D1 on the
  odds. For b ≥ 5 this makes the skeleton moot: it cannot be closed or refuted at
  reachable N (Remark 27).

Nothing is claimed beyond Lemmas R20-1/1a/1b and Propositions R20-2/R20-3.

## 6. Best candidate and next step

Best candidate: **CLS(5,a)**, c(v) = ⌊log₅ v⌋ + v₂(v), classes emitted in increasing index
order, within-class orders chosen by SAT — verified 4-AP-free on [1..250]
(`cw_CLS(5,a)_250.txt`), a genuine order-type-ω architecture, but not an explicit rule and
not a v log v profile (its profile is ≍ v^{3.32} on powers of 2). Best explicit rule: none
survives past largest term 33.

**Recommended next step (endorsed by the coordinator):** replace the profile-shape
programme with an **AP-uniformity programme** — search directly (SAT/CP on [1..N]) for a
class function c : ℕ → ℤ with finite fibres, no strictly monotone 4-AP class sequence, and
unbounded relative displacement on every AP r+qℕ for q ≤ 8, maximising the minimum
AP-displacement. Proposition R20-3 shows the natural family fails this; a machine answer
either produces the first D1-compatible architecture or converts D1 into a genuine
affirmative-side obstruction — the first experiment bearing on both branches at once.

## 7. Files

`framework.py` · `classlemma.py` · `constructions.py` · `scan.py` · `banded.py` ·
`prefixfix.py` · `profile_sat.py`, `alpha_wall.py`, `alpha_wall.log` · `cpsat_profile.py` ·
`classsat.py`, `run_classsat.py`, `classsat_b34.log`, `classsat_b56.log` · `oddcuts.py`,
`oddcuts_b3.log` · `headtail.py`, `headtail_C2.log` · `beam.py` · `mine.py` · witnesses
`wit_N*_a*.txt`, `cw_*.txt`.
