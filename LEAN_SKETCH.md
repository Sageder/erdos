# Lean formalization sketch — Erdős 196 and the results of this run

Target repository conventions: `google-deepmind/formal-conjectures`,
`FormalConjectures/ErdosProblems/196.lean`, which states

```lean
theorem erdos_196 : answer(sorry) ↔ ∀ (f : ℕ ≃ ℕ), HasMonotoneAP f 4
```

where `HasMonotoneAP f k` asks for a strictly increasing list of indices whose image under
`f` is `[x, x+d, x+2d, …]` or its reverse. Lean's `ℕ` contains `0`; the site's does not.
The two are equivalent by conjugating with the shift `n ↦ n+1`, which preserves index order
and translates values, and translation maps APs to APs. **Formalize against the existing
statement**, then bridge with the shift — this protects against misformalization, which is
the single most likely way to "prove" the wrong theorem.

Nothing in this run resolves `erdos_196`. What follows is a formalization plan for the
results that ARE established, ordered by (value × tractability).

---

## Tier 1 — formalize first (self-contained, high value, no analysis)

### 1. Lemma 1 (order-type correspondence)

```lean
/-- Permutations of ℕ correspond to linear orders on ℕ with finite predecessor sets. -/
def FinPred (r : ℕ → ℕ → Prop) : Prop := ∀ v, {w | r w v}.Finite

theorem orderTypeOmega (r : ℕ → ℕ → Prop) [IsStrictTotalOrder ℕ r] (h : FinPred r) :
    ∃ f : ℕ ≃ ℕ, ∀ v w, r v w ↔ f.symm v < f.symm w
```

Proof plan: define `rank v := (Set.Finite.toFinset (h v)).card`, show `rank` is strictly
monotone for `r`, that its range is downward closed (a finite nonempty predecessor set has
an `r`-maximum), and that a downward-closed infinite subset of `ℕ` is `univ`. All finite
combinatorics; `Set.Finite` and `Finset.card` suffice. This is the foundation every order
reformulation in the run rests on, so it should be first.

### 2. Theorem 21 (an explicit permutation with no monotone 5-AP)

The most valuable single item: it makes `[DEGS77](b)` machine-checkable rather than cited.

```lean
def vdcKey (m v : ℕ) : List Bool := (List.range (2*(m+1))).map (fun i => Nat.testBit v i)
def blockOrder (m : ℕ) : List ℕ :=      -- values [4^m, 4^(m+1)) sorted by vdcKey,
  ...                                    -- reversed when m is odd
def degsPerm : ℕ ≃ ℕ := ...              -- concatenation of blockOrder m, m = 0,1,2,…

theorem degs_no_monotone_5AP : ¬ HasMonotoneAP degsPerm 5
```

Proof plan follows the run's write-up exactly: (a) van der Corput order inside a block has
no monotone 3-AP; (b) block-major position order; (c) ratio-4 spread puts the last four
terms of a 5-AP in at most two adjacent blocks; (d) the pair criterion — `u` precedes `u+d`
in block `m` iff `Nat.testBit u (v₂ d) = decide (m % 2 = 1)` — plus
`(x+3d) − (x+d) = 2d` divisible by `2^(v₂ d + 1)`, forcing equal bits and contradicting the
adjacent-block parity flip. Bijectivity and order type ω are immediate (finite blocks
listed in order), which in Lean is the usual `Nat.rec`-style enumeration argument.

### 3. Theorem 47 (the forced-descent barrier)

Short, and it is the cleanest negative result of the run.

```lean
theorem forcedDescent_hasSink (f : ℕ ≃ ℕ) (E : ℕ → ℕ → Prop)
    (hdesc : ∀ s t, E s t → f.symm t < f.symm s) :
    ¬ ∃ c : ℕ → ℕ, ∀ n, E (c n) (c (n+1))
```

Proof: `fun n => f.symm (c n)` would be a strictly decreasing sequence in `ℕ`. One line with
`Nat.not_strictAnti` / well-foundedness. Then the corollary that `f 0` (the ≺-minimum) is a
sink for every rule of the form "positional facts ⟹ `t ≺ s`" is immediate.

---

## Tier 2 — formalize next (needs a little more machinery)

### 4. Lemma 6 (displacement compactness)

```lean
theorem displacement_compactness :
    (∃ f : ℕ ≃ ℕ, ¬ HasMonotoneAP f 4) ↔
    (∃ φ : ℕ → ℕ, ∀ N, ∃ σ : Equiv.Perm (Fin N), AvoidsMono4 σ ∧ ∀ v, pos σ v ≤ φ v)
```

The `←` direction is König's lemma on a finitely branching tree; Mathlib has
`WellFoundedTree`/`König`-style results but the cleanest route is a direct
`Nat.rec` construction of the branch using `Set.Finite` at each level. The key point to get
right — and the reason the classical version of this argument is wrong — is that the
pointwise bound `φ` is what makes each level FINITE and hence makes the limit order have
finite predecessor sets. Formalizing this correctly is worthwhile precisely because the
naive version is a known trap.

### 5. Theorem 12 (LP(9/8))

```lean
theorem lp_nine_eighths (f : ℕ ≃ ℕ) (C : ℚ) (hC : C < 9/8)
    (hprof : ∀ v, (f.symm v : ℚ) ≤ C * v) : HasMonotoneIncAP f 4
```

Proof plan: the drop-ledger. Needs `Finset.sum` manipulation, the layer-cake identity
`∑ w, e* w = ∑ e, card {w | e* w ≥ e}`, and the demand count (each `u` yields an
`e`-dropping `w` in a fiber of size ≤ 3). All finite sums over `Finset.range`; no analysis
beyond a limit at the end, which can be avoided by stating the finite form and instantiating
`N` explicitly.

---

## Tier 3 — state but do not attempt yet

Corollary 26 (AP-restriction), Lemma 13 (records 3-AP-free), Lemma 24 (coupled family) are
all short and would follow easily once Tier 1 is in place. Propositions 29–30 (the
class-architecture closure) are longer but elementary. Conjecture R21-C should be stated in
Lean and left as `sorry` — it is the run's main open successor question, and having it
stated precisely is itself useful.

---

## Verification protocol beyond Lean

1. **Re-run the suite.** `experiments/` is deterministic and seeded. `apcheck.py`
   self-validates against brute force; every downstream checker is cross-validated against
   it. `calibration_counts.py` must reproduce 6, 22, 102, 564, 3336, 22266, 168864.
2. **Re-verify the load-bearing UNSATs** with a second engine. The run's standard: the
   `pos(v) ≤ 2v` extinction is confirmed at N = 85 and 90 by an eager encoding with cadical
   and glucose agreeing, and independently by exhaustive solver-free DFS at C ≤ 7/4.
3. **Fresh-context audits.** `AUDITS.md` holds the pattern to follow: give an auditor only
   `PROBLEM.md` plus the draft, and instruct it to break the argument. In this run that
   process caught a broken lemma, a circular biconditional, a degenerate objective, and two
   encoding bugs — including in my own work.
4. **Check every claimed equivalence for vacuity** by asking explicitly whether it is
   `P ↔ P`. Three separate results in this run failed that test.
