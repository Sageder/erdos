# CORE.md — rigorously proved core lemmas (session 1, inline work)

Status: each lemma below is stated with a full proof. Machine sanity checks live in
`experiments/core_checks.py`. Nothing here claims to resolve 196; these are shared
infrastructure for all routes. Conventions: PROBLEM.md governs. ℕ = {1,2,3,...}.
For a permutation (bijection) a : ℕ → ℕ write pos = a^{-1} (position of a value), and
define the induced order on values: v ≺ w  ⟺  pos(v) < pos(w).

---

## Lemma 1 (order-type lemma)

Bijections a : ℕ → ℕ correspond exactly to linear orders ≺ on ℕ in which every element
has finitely many predecessors, via v ≺ w ⟺ pos(v) < pos(w).

Proof. (⇒) Given a bijection, pred(v) = {w : pos(w) < pos(v)} has exactly pos(v) − 1
elements — finite. The order is linear since pos is injective into ℕ.

(⇐) Given a linear order ≺ with all pred sets finite, define r(v) = #pred(v) + 1 ∈ ℕ.
- r is injective: if v ≺ w then pred(v) ∪ {v} ⊆ pred(w), so r(v) < r(w); by linearity
  distinct elements are comparable, so distinct elements get distinct ranks.
- r is order-preserving (same computation).
- The image of r is downward closed in ℕ: if r(w) = m + 1 with m ≥ 1, let
  P = pred(w) ≠ ∅; P is finite and nonempty, so it has a ≺-maximum u (finite linear
  orders have maxima); then pred(u) = P ∖ {u}, so r(u) = m. With r(v₀) = 1 for the
  ≺-least element v₀ of, e.g., the finite nonempty set pred(w) ∪ {w} for any w… more
  directly: the ≺-least element of ℕ exists (take any w; pred(w) ∪ {w} is finite and
  nonempty, its ≺-min is a global ≺-min since anything below it would lie in pred(w)),
  and it has rank 1. So the image is a downward-closed subset of ℕ.
- The image is infinite (r injective on an infinite set), and an infinite downward-closed
  subset of ℕ is ℕ itself.
Thus r : ℕ → ℕ is an order isomorphism from (ℕ, ≺) to (ℕ, <); a := r^{-1} is the
permutation with induced order ≺. The two constructions are mutually inverse. ∎

Consequence used everywhere: (ℕ, ≺) has order type ω; in particular it has NO infinite
strictly ≺-descending chain c₀ ≻ c₁ ≻ c₂ ≻ ⋯ (all c_k with k ≥ 1 would be predecessors
of c₀).

## Lemma 2 (3-AP forcing; = [DEGS77](a), independent short proof)

Every permutation a of ℕ contains a monotone 3-term AP.

Proof. Let ≺ be the induced order and z := a(1), the ≺-minimum of ℕ (it exists and is
unique: value at position 1). Suppose a has no monotone 3-AP. For every d ≥ 1 consider
the value triple (z, z+d, z+2d), which exists in ℕ. Since z is the ≺-minimum, the
positional order of the triple must put z first; the two possibilities are
z ≺ z+d ≺ z+2d (a monotone increasing 3-AP with x = z — excluded) and
z ≺ z+2d ≺ z+d. Hence z+2d ≺ z+d for every d ≥ 1.
Apply this with d = 2^k: the values v_k := z + 2^k satisfy v_{k+1} ≺ v_k for all k ≥ 0,
an infinite strictly ≺-descending chain — contradicting order type ω (Lemma 1). ∎

Remarks (verified against PROBLEM.md conventions):
- Surjectivity is used twice: z is the minimum of ALL of ℕ (so every triple (z,z+d,z+2d)
  lies in the ordered set), and Lemma 1 (order type ω) needs bijectivity.
- Only the increasing orientation was invoked; minimality of z made the decreasing
  orientation impossible at these triples. The proof is genuinely one-sided (uses ω).

## Lemma 3 (normalization for the NO branch)

If some permutation of ℕ has no monotone 4-AP, then some permutation b of ℕ with
b(1) = 1 has no monotone 4-AP.

Proof. Let a be a 4-AP-free permutation, z = a(1) its ≺-minimum. The set
S = {z, z+1, z+2, ...} listed in position order is an injective sequence exhausting S.
Define b as this sequence translated by t ↦ t − (z−1); b is a bijection ℕ → ℕ (composition
of: order-isomorphic enumeration of S — a bijection ℕ → S with the induced order, order
type ω since it is a suborder of an ω-order… precisely: the enumeration of S in position
order is a bijection ℕ → S; translation S → ℕ is a bijection). Translation by −(z−1) maps
4-APs to 4-APs (in both orientations), and passing to the subsequence of positions
preserves the relative positional order; hence a monotone 4-AP of b would yield one of a.
Finally b(1) = 1: the first listed element of S is its ≺-min, which is z (global min),
and z ↦ 1. ∎

So: WLOG a counterexample has value 1 at position 1. (Pure normalization; no strength
gained, but it anchors constraints.)

## Lemma 4 (anchored disjunction)

Let a be a 4-AP-free permutation of ℕ with induced order ≺ and z = a(1). Then

  (A_j ∨ B_j):   for every j ≥ 1,   z+2j ≺ z+j   or   z+3j ≺ z+2j.

More generally (★★): for every value v and every j > E(v) := max{w : w ≺ v} (E(v) := 0
if v = z): NOT ( v+j ≺ v+2j ≺ v+3j ).

Proof of (★★). Let v be any value, j > E(v). Then none of v+j, v+2j, v+3j is ≺ v: every
value ≺ v is ≤ E(v) < j < v + j. So v ≺ v+j, v ≺ v+2j, v ≺ v+3j. If v+j ≺ v+2j ≺ v+3j
held, then (v, v+j, v+2j, v+3j) would be a monotone increasing 4-AP (x = v, d = j) —
excluded. For v = z, E(z) = 0 and the hypothesis j > 0 is vacuous, giving (A_j ∨ B_j)
in the equivalent disjunctive form ¬(z+j ≺ z+2j) ∨ ¬(z+2j ≺ z+3j). ∎

Caution (established by the adversary analysis in NOTES): the anchored constraints alone
do NOT force a contradiction — the assignment "z+j ≺ z+2j and z+3j ≺ z+2j for all j"
extends to a partial order whose constraint digraph (edges k → 2k and 3j → 2j on the
index set) is acyclic with all ancestor sets finite (2^a = (3/2)^b has no nontrivial
solution; ancestors of n are among {n·3^b/2^{a+b}} ∩ ℕ, finitely many), hence extends to
SOME type-ω linear order. Whether such an extension can satisfy full 4-AP-freeness is
exactly the global problem. Do not mistake Lemma 4 for more than it is.

## Lemma 5 (tame permutations die: linear displacement profile)

Let a be a permutation of ℕ. Suppose there are constants c > 0 and B < ∞ with
|pos(v) − c·v| ≤ B for all v. Then a contains a monotone increasing 4-AP.
(Hence any NO-witness has sup_v |pos(v) − c v| = ∞ for every c > 0.)

Proof. Choose j with c·j > 2B, and any x ≥ 1. For k = 0,1,2:
pos(x+(k+1)j) ≥ c(x+(k+1)j) − B = c(x+kj) + cj − B > c(x+kj) + B ≥ pos(x+kj).
So pos(x) < pos(x+j) < pos(x+2j) < pos(x+3j): a monotone increasing 4-AP. ∎

## Lemma 6 (displacement compactness — the finite–infinite equivalence)

For a function φ : ℕ → ℕ say a permutation σ of [1..N] is φ-bounded if
pos_σ(v) ≤ φ(v) for all v ≤ N. Then:

  196-NO  (a 4-AP-free permutation of ℕ exists)
  ⟺  there exists φ : ℕ → ℕ such that for EVERY N ≥ 1 there exists a
      monotone-4-AP-free φ-bounded permutation of [1..N].

Proof. (⇒) Let a be a 4-AP-free permutation of ℕ; set φ(v) := pos_a(v). For each N, let
σ_N be the values 1..N listed in a-position order (the restriction; a permutation of
[1..N] by the restriction principle, PROBLEM.md §4). σ_N is 4-AP-free (its monotone
4-APs are monotone 4-APs of a). And pos_{σ_N}(v) = #{w ≤ N : pos_a(w) ≤ pos_a(v)}
≤ pos_a(v) = φ(v). ✓

(⇐) Fix φ as on the right side. Build a tree T: level-N nodes are the 4-AP-free
φ-bounded permutations of [1..N]; the parent of a level-(N+1) node σ is its restriction
to values [1..N] (delete value N+1 from the listing). The parent is a level-N node:
restriction preserves 4-AP-freeness (restriction principle) and can only shrink
positions (deleting an element from the listing does not increase any rank), so
φ-boundedness is preserved. Each level is FINITE (a φ-bounded permutation of [1..N] is
determined by the injective map v ↦ pos(v) ∈ [1..min(φ(v), N)], finitely many). Every
level is nonempty by hypothesis. Hence T is an infinite, finitely-branching tree, and
every node has a parent chain to the root; by König's lemma T has an infinite branch
(σ_N)_{N≥1} with σ_{N+1} restricting to σ_N.
Define the limit order ≺ on ℕ: for v ≠ w let N ≥ max(v,w) and set v ≺ w iff
pos_{σ_N}(v) < pos_{σ_N}(w); this is independent of N (restrictions preserve relative
order of surviving values — deleting elements never swaps two others), and transitive/
linear since each σ_N is.
Order type ω: pred(v) in ≺ = ∪_N {w ≤ N : w ≺ v}; for every N, #{w ≤ N : w ≺ v}
= pos_{σ_N}(v) − 1 ≤ φ(v) − 1. So every predecessor set is finite (≤ φ(v) − 1).
By Lemma 1, ≺ is induced by a permutation a of ℕ.
4-AP-freeness of a: any monotone 4-AP of a involves four values; take N ≥ their max;
the same four values with the same relative positional order sit inside σ_N (again since
restriction preserves relative order — concretely, pos_a and pos_{σ_N} induce the same
order on [1..N] by construction of ≺), contradicting σ_N being 4-AP-free. ∎

Commentary. This is precisely the repair of the §3 compactness trap: the pointwise
bound φ is what survives the limit and delivers order type ω. It converts 196 into a
statement about FINITE permutations quantified over profiles φ:
196-YES ⟺ for every φ there is a finite N at which φ-bounded avoiders die out.
This frames route R4's experiments and suggests the following sufficient criterion.

## Lemma 7 (FIN(K) criterion)

For K ≥ 1 consider the statement

  FIN(K): for every C there is N such that EVERY monotone-4-AP-free permutation of
          [1..N] has some value v ≤ K with pos(v) ≥ C.

If FIN(K) holds for some K, then 196-YES holds.

Proof. Suppose FIN(K) holds and, for contradiction, a is a 4-AP-free permutation of ℕ.
Let σ_N be its restrictions (4-AP-free permutations of [1..N]). For each C, with
N = N(C) from FIN(K): some v ≤ K has pos_{σ_{N(C)}}(v) ≥ C. By pigeonhole some fixed
v* ≤ K works for infinitely many C. Since pos_{σ_N}(v) ≤ pos_a(v) for all N (as in
Lemma 6(⇒)), pos_a(v*) ≥ C for arbitrarily large C — impossible: pos_a(v*) is a finite
natural number. ∎

Note: FIN(1) is FALSE — the parity recursion gives, for every N, a 4-AP-free (indeed
3-AP-free) permutation of [1..N] with pos(1) = 1. The candidate targets are FIN(K) for
small K ≥ 2, or the weaker ∀φ-extinction of Lemma 6 directly. Whether even FIN(2) is
plausible is a computational question first (see experiments/shallow_probe.py: for which
(K, C) do avoiders with all of [1..K] in the first C positions survive to large N?).

## Lemma 8 (incremental interval characterization)

Let positions of values 1, ..., v−1 be fixed (an injective map pos into ℕ). For d ≥ 1 with
v − 3d ≥ 1 call d an *inc-step* (for v) if pos(v−3d) < pos(v−2d) < pos(v−d), and a
*dec-step* if pos(v−3d) > pos(v−2d) > pos(v−d). Define
  Hi(v) := min { pos(v−d) : d an inc-step },   Lo(v) := max { pos(v−d) : d a dec-step }
(min ∅ = +∞, max ∅ = 0). Then an assignment of distinct positions to all of ℕ (or to
[1..N]) is monotone-4-AP-free iff for every value v: Lo(v) < pos(v) < Hi(v).

Proof. Every monotone 4-AP has a unique largest value v and is of the form
(v−3d, v−2d, v−d, v). The increasing orientation occurs iff d is an inc-step and
pos(v) > pos(v−d); the decreasing orientation iff d is a dec-step and pos(v) < pos(v−d).
Avoiding all monotone 4-APs with largest term v is thus equivalent to
pos(v) < pos(v−d) for every inc-step d and pos(v) > pos(v−d) for every dec-step d,
i.e. Lo(v) < pos(v) < Hi(v). Conjoin over v. ∎

Consequences. (i) Fast incremental search: placing values in increasing order, the
feasible positions for v form the interval (Lo(v), Hi(v)) minus occupied slots.
(ii) A NO-witness is exactly an assignment v ↦ pos(v) (bijective onto ℕ) with
Lo(v) < pos(v) < Hi(v) for all v: "Hi-pressure" (inc-steps) pushes values into early
slots, which are consumed; "Lo-pressure" pushes late. The design tension is explicit.
