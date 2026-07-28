# VERDICT — Erdős problem 196

**Question (site statement, governing).** Must every permutation of ℕ contain a monotone
4-term arithmetic progression?

**Result of this run: NOT RESOLVED.** Neither branch was proved. No counterexample
permutation was constructed, and no proof of unavoidability was obtained. This document
records exactly what was established, what was refuted, where the open gap now sits, and
which of the run's own intermediate claims had to be corrected.

Everything below is either proved with a written proof in `attempts/core/CORE.md`
(33 numbered items) or is explicitly labelled MEASURED. Machine results are labelled with
their verification standard. The lab notebook `NOTES.md` allows a cold resume.

---

## 1. What was proved

### 1.1 Framework

- **Lemma 1 (order-type lemma).** Bijections ℕ→ℕ correspond exactly to linear orders on ℕ
  with all predecessor sets finite. All order reformulations rest on this.
- **Lemma 6 (displacement compactness).** 196-NO ⟺ there EXISTS a profile φ : ℕ→ℕ such
  that for every N some monotone-4-AP-free permutation σ of [1..N] has pos_σ(v) ≤ φ(v).
  This repairs the classic König trap: the pointwise bound φ is what survives the limit
  and delivers order type ω. It is the frame in which most of the run's work is stated.
- **Lemma 8 / Lemma 9 / Lemma 10.** The insertion-interval characterization (placing
  values in increasing order, the admissible positions for v form an interval
  (Lo(v), Hi(v))), the slot relaxation (surjectivity onto positions is free — only finite
  predecessor sets matter), and the exact stuckness criterion (an X-configuration).
- **Lemma 2.** A short independent proof of [DEGS77](a): every permutation of ℕ contains a
  monotone 3-AP. Also **Lemma 16.1**: for every value w and modulus m there is e ∈ mℕ with
  (w, w+e, w+2e) positionally increasing.

### 1.2 Structure of any counterexample

- **Lemma 11.** Two infinite increasing "spines": value-records Λ (with pos(w) ≤ w) and
  grounded values Γ (with pos(g) ≥ g); neither contains a 4-term AP.
- **Lemma 13.** Sharper: Λ contains no 3-term AP at all; Γ contains none within any dyadic
  window.
- **Lemma 24 (coupled family).** Every affine sub-copy and every value-tail of a
  counterexample is itself a counterexample, so EACH has its own infinite 3-AP-free record
  set — an infinite coupled family of Roth-critical sets inside one order.
- **Theorem 16 (forcing closure) — an exact ω-reformulation.** Call u *open at scale d* if
  (u−2d, u−d, u) is positionally increasing; then u+d is forced before u, so the forward
  closure Cl(u) lies inside pred(u) and |Cl(u)| ≤ pos(u). By König,
  **196-YES ⟺ every 4-AP-free permutation admits an infinite forcing chain.**
- **Corollary 26.** Every quantitative theorem applies to every arithmetic-progression
  restriction simultaneously.

### 1.3 Quantitative

- **Theorem 12 (LP(9/8)).** Every permutation with pos(v) ≤ Cv for C < 9/8 contains an
  increasing monotone 4-AP (drop-ledger against the "no three consecutive ascents at any
  scale" constraint), with an additive-slack form giving limsup pos(v)/v ≥ 9/8.
- **Theorem 14 (ceiling).** The triadic reversed-block permutation has pos(v) ≤ 3v−1 and no
  increasing 4-AP, so increasing-only methods provably cannot pass C = 3.

### 1.4 Closing whole families (the bulk of the run's content)

- **Remark 20 (digit-comparator dichotomy).** The base-b comparator that compares values at
  their first differing digit kills every monotone 4-AP (proved; machine-verified to
  N = 500) but necessarily has infinite predecessor classes; the reverse priority has order
  type ω but is a contiguous block layout. Truncation escapes neither. The whole digit
  family is closed.
- **Remark 25.** Attempting to replace the block parity by an arithmetic sign fails because
  such rules are not transitive — exhaustive classification: only 16 of 256 candidate rules
  are transitive and none is genuinely value-dependent. The block structure in the length-5
  solution is *forced*, not incidental.
- **Theorem 21 + Remarks 22–23 (the 4-vs-5 gap).** An explicit no-monotone-5-AP permutation
  (blocks [4^m, 4^{m+1}) concatenated, van der Corput inside, reversed on odd blocks) was
  independently verified to N = 65 535 — a confirmation of [DEGS77](b) with an explicit
  mechanism. Its contradiction is a TWO-PAIR parity argument, and a 4-AP cannot supply two
  pairs at any ratio ≥ 3 (it splits as pair + singleton). All four naive length-4 analogues
  die immediately, the first at (2, 5, 8, 11).
- **Propositions 29–30 (arithmetic delay world closed).** For any class function with finite
  fibres emitted in increasing index order and *arbitrary* within-class orders, a
  progression along which the class index is eventually non-decreasing has linear
  displacement (Prop. 29). Hence if the delay's level set is a union of residue classes, the
  delay is constant on a full progression and the architecture dies (Cor. 30). This retires
  ρ(v_p(v)) for every prime, its shifted variants, every function of v mod m, and every
  Boolean combination of congruences — all at once.

### 1.5 Barrier results (why the standard attacks cannot work)

- **Generic Escape (route R5, re-derived independently by an isolated agent).** No finite
  forcing tree built from one-point-anchored 3-AP supply can ever close: the adversary
  answers every probe at a fresh scale beyond twice the named span.
- **Remark 17.** Linear-profile extinction cannot decide the problem, for two independent
  reasons: Lemma 6 quantifies over ALL profiles, and the *known-negative* case at length 5
  exhibits the same extinction signature (5-AP-free permutations under pos(v) ≤ 1.25v die
  at N = 13, verified by two solvers).
- **Remark 27 (search blind spot).** From the certified law N*(C) ≈ 4·exp(4.15(C−1.25)), a
  design with AP-restriction displacement constant C cannot die before N ≈ 6·10³ (C=3),
  10⁷ (C=5), 10⁹ (C=6). Verification to 10⁴–10⁵ is therefore structurally incapable of
  settling anything in that regime.
- **Remark 31.** The AP-uniformity search is provably vacuous: its objective is degenerate,
  and the geometric coarsening of any finite avoider already satisfies the constraints, so
  the system can never go extinct.

---

## 2. Certified finite data (MEASURED, with verification standard)

- Calibration reproduced exactly: monotone-4-AP-free permutation counts for N = 3..9 are
  6, 22, 102, 564, 3336, 22266, 168864; 3-AP-free counts 4, 10, 20, 48, 104, 282, 496.
- Extinction thresholds for pos(v) ≤ ⌊Cv⌋ (plain, both orientations):
  N*(C) = 4, 15, 31, 90 at C = 1.25, 1.5, 1.75, 2. The C = 1.5 and 1.75 entries agree
  between exhaustive extension-tree enumeration and SAT; C = 2 is confirmed by CEGAR
  (N = 90) and independently by the eager O(N³) encoding at N = 85 and N = 90 with cadical
  and glucose both UNSAT.
- The profile ⌈0.5·v·log₂(2v)⌉ admits no avoider of [1..130] — eager encoding, 932 414
  clauses, two solvers agreeing. This falsifies the "displacement Θ(v log v)" target.
- Forcing-closure statement verified on all 195 154 avoiders with N ≤ 9; Lemma 24's finite
  shadow on 191 130 avoiders across all progressions of step ≤ 3; Lemma 13's shadows on
  168 864 avoiders.
- Every solver engine used was cross-validated: the CEGAR engine reproduces the exhaustive
  enumeration thresholds exactly and agrees with a two-solver eager encoding.

---

## 3. Corrections made during the run (recorded deliberately)

Three substantive intermediate claims had to be narrowed or withdrawn. They are listed
because the pattern — over-reading finite certificates — is the main hazard of this problem.

1. **"Linear profiles all die, so the affirmative branch is gaining."** Withdrawn
   (Remark 17). The same signature appears in the known-negative case at length 5; the
   quantitative programme cannot discriminate the branches at all.
2. **"Block layouts are dead."** Narrowed (Correction to Remark 22). The certificates kill
   *geometric* in-order layouts at ratios 3–4 and bounded-lag interleavings. Accelerating
   non-geometric cut sequences — e.g. [1, 2, 4, 10, 90] — remain feasible at depth 5.
3. **"Θ(v log v) displacement is consistent with all certificates."** Falsified
   (Remark 28), by a certificate obtained after the claim was made.

A fourth item is a process error rather than a mathematical one: the AP-uniformity
experiment was commissioned without first checking whether a trivial construction satisfies
its constraints. It did (Remark 31).

---

## 4. Where the open gap now sits

**Affirmative branch.** By Theorem 16 the problem is exactly: does every 4-AP-free
permutation admit an infinite forcing chain? The missing ingredient is "co-supply" — an
increasing 3-AP *ending* at a prescribed value, whereas Lemma 16.1 supplies only ones
*starting* there. Co-supply is false on finite boards (the parity permutation has no
monotone 3-AP at all), so any proof must be essentially infinitary. The equivalent
record-set formulation (Lemma 24) is Roth-critical and lacks any density lower bound.

**Negative branch.** Two live regions, both requiring a proof rather than a search:
- accelerating non-geometric cut sequences (route R1's corridor), which sit inside the
  Remark 27 blind spot;
- **Conjecture R21-C:** for c = ⌊log_b v⌋ + t with geometric fibres, does the
  no-monotone-class-sequence condition force t to be constant on some infinite progression?
  If yes, block-index-plus-delay architectures are finished entirely. Not implied by
  Corollary 30, and provably not finitely decidable — the standing sanity check is that any
  argument which would also apply to the geometric coarsening of a finite avoider is wrong.

---

## 5. Independent-verification plan

1. **Re-audit.** `AUDITS.md` holds a fresh-context adversarial audit of the core (13 of 15
   items SOUND, two repairable gaps found and repaired as specified). Wave-2 audits were
   commissioned per route. Any future claim should get a fresh-context audit before belief.
2. **Re-run.** `experiments/` is deterministic and seeded; `apcheck.py` self-validates
   against brute force, and every downstream checker is cross-validated against it. The
   suite re-runs clean.
3. **Lean sketch.** The natural formal target is the statement, not the proof:
   `theorem erdos_196 : ∀ (f : ℕ ≃ ℕ), HasMonotoneAP f 4` (or its negation with an explicit
   witness), matching `google-deepmind/formal-conjectures`. Two supporting items are
   formalizable independently and would be worth doing first: Lemma 1 (order-type
   correspondence) and Theorem 16 (forcing closure), the latter being a clean statement
   about a relation on ℕ and its transitive closure.

---

## 6. Honest bottom line

Erdős 196 remains open. This run did not resolve it and did not come close to resolving it.
What it produced is a map of why the standard approaches fail: the digit-comparator family,
the arithmetic-delay family, and the mechanism that settles length 5 are each closed by
proof; the affirmative-side forcing arguments are closed by an explicit barrier; and the
quantitative programme is proved incapable of discriminating the two branches. The two
remaining directions are sharply posed and each needs a genuinely new idea, in a regime
where additional computation is provably unhelpful.
