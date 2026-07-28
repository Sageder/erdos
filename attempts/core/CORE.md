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

## Lemma 9 (slot relaxation — surjectivity onto positions is free)

196-NO ⟺ there exists an injective map pos : ℕ → ℕ (values to "slots", NOT required
to be surjective) such that for every v and every d ≥ 1 with v − 3d ≥ 1:
  ¬( pos(v−3d) < pos(v−2d) < pos(v−d) < pos(v) )  and
  ¬( pos(v−3d) > pos(v−2d) > pos(v−d) > pos(v) ).

Proof. (⇒) The position map of a NO-witness is such a map (Lemma 8's condition,
regrouped by largest AP element, is exactly displayed above).
(⇐) Given such a pos, list the used slots in increasing order and let b(n) := the value
occupying the n-th used slot. Every value w with pos(w) < pos(v) satisfies
pos(w) ∈ [1, pos(v)−1], so each value has at most pos(v) − 1 values before it: the
induced order on values has all predecessor sets finite, and b is a bijection ℕ → ℕ
(Lemma 1). Relative slot order equals relative position order in b, and the displayed
condition forbids exactly the monotone 4-APs (unique-largest-element grouping as in
Lemma 8). So b is a NO-witness. ∎

Equivalently (order-density version): 196-NO ⟺ there is an injective pos : ℕ → ℚ with
(i) {w : pos(w) < pos(v)} finite for every v, and (ii) the same two forbidden patterns.
(ℚ can be re-embedded into ℕ preserving order on the used set: enumerate used slots in
increasing order — well-ordered by (i)… precisely, (i) makes the induced value-order
have finite predecessor sets, and only the order matters.)

Moral: the difficulty of the NO branch is NOT "filling every position" — it is that
every VALUE must be placed with only finitely many values below it. "Skipping slots"
buys nothing structurally but makes greedy/online constructions cleaner: values arrive
in increasing order 1, 2, 3, … and each v must be inserted into the current order
inside the open order-interval (Lo(v), Hi(v)) of Lemma 8.

## Lemma 10 (stuckness = X-configuration)

Place values 1, …, v−1 injectively (any linear order with the above conventions).
Call d an inc-step / dec-step for v as in Lemma 8. Then there is NO admissible
order-position for v (i.e. the open order-interval (Lo(v), Hi(v)) is empty, even
allowing arbitrary insertion between existing elements à la the ℚ-version) if and only
if there exist d₁, d₂ with:
  (v−3d₁, v−2d₁, v−d₁) positionally increasing,   [inc-step d₁]
  (v−3d₂, v−2d₂, v−d₂) positionally decreasing,   [dec-step d₂]
  pos(v−d₁) < pos(v−d₂).
We call this an X-configuration aimed at v.

Proof. In the dense (ℚ) setting an admissible slot exists iff Lo(v) < Hi(v), where
Lo(v) = max{pos(v−d) : d dec-step} and Hi(v) = min{pos(v−d) : d inc-step}
(max ∅ = −∞, min ∅ = +∞). Emptiness Lo(v) ≥ Hi(v) happens iff some dec-step's pos
exceeds some inc-step's pos (equality impossible: pos injective, v−d₁ ≠ v−d₂ for
d₁ ≠ d₂), which is the displayed configuration. ∎

Consequences.
(a) YES-strategy target: prove that any type-ω placement of ℕ eventually creates an
    X-configuration aimed at a yet-unplaced value all three of whose "aiming" terms
    v−3dᵢ, v−2dᵢ, v−dᵢ are already placed before v — OR forces infinitely many values
    below one point (violating finite predecessors). NOTE the adversary places values
    in increasing order, so "aimed at v" configurations use only values < v: the first
    failure mode is fully finitary.
(b) NO-strategy invariant: maintain, for all (not-yet-reached) v and all step pairs,
    the absence of bad pairs; i.e., whenever an increasing 3-AP (a, a+d, a+2d) and a
    decreasing 3-AP (b, b+e, b+2e) satisfy a+3d = b+3e (common target) and the target
    exceeds all four... (both targets not yet placed), keep pos(a+2d) > pos(b+2e).

## Lemma 11 (universal structure of any 4-AP-free permutation)

Let a be ANY monotone-4-AP-free permutation of ℕ, D(u,e) := [u+e ≺ u] its drop
indicator. Then:

(a) [words] For every u, e ≥ 1: ¬(D(u,e) ∧ D(u+e,e) ∧ D(u+2e,e)) and
    ¬(¬D(u,e) ∧ ¬D(u+e,e) ∧ ¬D(u+2e,e)). Hence along every arithmetic progression, at
    every step e, the descent word avoids the factors 000 and 111; every window of 3 letters contains a 0 and a 1 (so all its density limit
    points lie in [1/3, 2/3]).

(b) [two spines] Call w a *value-record* (w ∈ Λ) if w is larger than every value placed
    before it — equivalently w ≺ w + e for all e ≥ 1. Call g *grounded* (g ∈ Γ) if
    pos(g) > pos(v) for all v < g (placed after all smaller values). Then:
    - Λ and Γ are both infinite;
    - value order and position order agree on Λ, and on Γ (each is an increasing
      subsequence of a);
    - neither Λ nor Γ contains a 4-term AP; by Szemerédi's theorem (4-AP case), both
      have upper density 0;
    - pos(w) ≤ w on Λ, and pos(g) ≥ g on Γ.

Proof. (a) Three consecutive drops along step e give pos(u) > pos(u+e) > pos(u+2e) >
pos(u+3e): the values u+3e, u+2e, u+e, u read in increasing position order form a
decreasing 4-AP. Three consecutive non-drops give an increasing 4-AP. Densities:
in any window of 3 letters there is a 0 and a 1.

(b) Λ: the equivalence — if some value placed before w exceeded w, that value is w + e
for some e ≥ 1 with w + e ≺ w; conversely if w + e ≺ w then a larger value precedes w.
Λ is infinite: the running maximum M(n) := max(a(1..n)) is unbounded (a is surjective)
and strictly increases exactly at positions holding value-records. Order agreement: for
records w < w', w ≺ w' by the defining property of w (w ≺ w + e with e = w' − w).
No 4-AP in Λ: four records in value-AP appear in increasing position order — a monotone
increasing 4-AP. pos(w) ≤ w: all values before w are smaller than w, and there are
pos(w) − 1 distinct such values, so pos(w) − 1 ≤ w − 1.
Γ: g is grounded iff pos(g) > max(pos(1), …, pos(g−1)), i.e. iff g is a record of the
bijection pos : ℕ → ℕ; the running maximum of pos on [1..v] is unbounded and jumps
exactly at grounded values, so Γ is infinite. For grounded g < g': pos(g') > pos(g) by
definition of g' grounded. Four grounded values in AP: again an increasing 4-AP.
pos(g) ≥ g: the g − 1 smaller values occupy distinct positions < pos(g). ∎

Remarks. (i) In the asymmetric setting (ASYM.md) Λ is exactly the leader set; Lemma 11
shows the two-spine structure is universal, not special to the asymmetric strategy.
(ii) Any NO-witness therefore contains two infinite increasing subsequences whose value
sets are 4-AP-free density-0 sets with pos ≤ v (resp. pos ≥ v) — quantitative handles
for YES-side counting arguments: e.g. with r₄(M) := max size of a 4-AP-free subset of
[1..M], |Λ ∩ [1..M]| ≤ r₄(M) and |Γ ∩ [1..M]| ≤ r₄(M) for every M.

## Theorem 12 (LP(9/8) — first quantitative displacement bound)

Let C < 9/8. Then every permutation of ℕ with pos(v) ≤ C·v for all v contains an
increasing monotone 4-AP. Moreover (additive-slack form, AUDITS.md 2026-07-28): if
pos(v) ≤ C·v holds for all v ≥ V₀ (any V₀), the same conclusion follows — with
Q := max_{v<V₀} pos(v) the ledger becomes pos(w) ≤ C(w − e*(w)) + Q, the supply bound
Σe* ≤ (1−1/C)N(N+1)/2 + NQ/C, and the unchanged demand N²/18 − O(N) still forces
C ≥ 9/8 in the limit. Consequently every permutation of ℕ with no increasing monotone
4-AP (in particular every monotone-4-AP-free permutation) satisfies
limsup_{v→∞} pos(v)/v ≥ 9/8 (genuinely limsup: for each C < 9/8 infinitely many v have
pos(v) > Cv, since finitely many exceptions could be absorbed into V₀).

Finite form: if σ is a permutation of [1..N] with pos(v) ≤ C·v for all v ≤ N and σ has
no increasing monotone 4-AP, then
  N(N+1)/2 · (1 − 1/C)  ≥  Σ_{e=1}^{⌊(N-1)/3⌋} (N − 3e)/3   [≈ N²/18],
which fails for C < 9/8 once N ≥ N₀(C) (explicitly computable).

Proof. Work with the finite form; the infinite statement follows by restriction
(pos_{σ_N}(v) ≤ pos_a(v) ≤ Cv, and an increasing 4-AP of σ_N is one of a).

Say "w has an e-drop" (e ≥ 1, w − e ≥ 1) if pos(w) < pos(w − e). Let
e*(w) := max{e : w has an e-drop} (0 if none).

(Supply / ledger.) If w has an e-drop then pos(w) < pos(w−e) ≤ C(w−e); applying this
with e = e*(w) (and pos(w) ≤ Cw when e*(w) = 0):
  pos(w) ≤ C·(w − e*(w))    for every w ≤ N.
Summing over w ≤ N and using Σ pos(w) = N(N+1)/2 (σ is a bijection onto [1..N]):
  N(N+1)/2 ≤ C·[N(N+1)/2 − Σ_w e*(w)],  i.e.  Σ_w e*(w) ≤ (1 − 1/C)·N(N+1)/2.

(Demand.) No increasing 4-AP means: for every u ≥ 1, e ≥ 1 with u + 3e ≤ N,
NOT(pos(u) < pos(u+e) < pos(u+2e) < pos(u+3e)); hence some i ∈ {0,1,2} has
pos(u+(i+1)e) < pos(u+ie): the value w = u+(i+1)e ∈ {u+e, u+2e, u+3e} has an e-drop.
For fixed e, each w is of the form u+e, u+2e or u+3e for at most 3 values of u, so
  #{w ≤ N : w has an e-drop} ≥ (N − 3e)/3   for each e ≤ (N−1)/3.
Since e*(w) ≥ e whenever w has an e-drop,
  Σ_w e*(w) = Σ_{e≥1} #{w : e*(w) ≥ e} ≥ Σ_{e=1}^{⌊(N-1)/3⌋} (N − 3e)/3
            = N²/18 − O(N).

(Conclusion.) Combining: N²/18 − O(N) ≤ (1 − 1/C)·N(N+1)/2. As N → ∞ this forces
1/18 ≤ (1 − 1/C)/2, i.e. C ≥ 9/8. So for C < 9/8 the finite form fails at large N. ∎

Remarks. (i) Only the INCREASING orientation is used; the theorem covers the
asymmetric family as well. (ii) The empirical extinction thresholds (NOTES 00:20)
persist to C = 3 at least, so LP(9/8) is far from the truth; sharpening candidates:
drop-chains (mind the Γ-escape: the grounded set can be Behrend-dense, so pure
chain-to-Γ accounting does NOT extend the range — verified failed attempt), and
multi-scale ledgers where each scale pays separately. (iii) At C = 1 the inequality
degenerates to "some drop exists", matching the exact threshold N(1) = 4.

## Lemma 13 (spines are 3-AP-free, not just 4-AP-free)

Let a be any monotone-4-AP-free permutation of ℕ, Λ its value-records, Γ its grounded
values (Lemma 11). Then:

(a) Λ contains NO 3-term AP at all: |Λ ∩ [1..N]| ≤ r₃(N) for every N.

(b) Every 3-term AP (g₁, g₂, g₃) ⊆ Γ has g₂ ≥ 2g₁ (step e ≥ g₁; REPAIRED per
    AUDITS.md 2026-07-28 — the boundary case e = g₁, i.e. grounded (g, 2g, 3g), is not
    excluded by the argument and does occur, e.g. Γ = {1,2,3} for (1,2,4,3)).
    In particular Γ ∩ [M, 2M] is 3-AP-free for every M (its steps satisfy
    e ≤ M/2 < M ≤ g₁), so |Γ ∩ [M, 2M]| ≤ r₃(2M).

(Here r₃(N) = max size of a 3-AP-free subset of [1..N].)

Proof. (a) Suppose w, w+e, w+2e ∈ Λ. Records appear in increasing position order
(Lemma 11), so pos(w) < pos(w+e) < pos(w+2e). The value w+3e exists in ℕ, and w+2e is
a record — placed before every larger value — so pos(w+3e) > pos(w+2e). Then
(w, w+e, w+2e, w+3e) is an increasing monotone 4-AP: contradiction.

(b) It suffices to exclude e < g₁. Suppose g₁, g₂ = g₁+e, g₃ = g₁+2e ∈ Γ with
e < g₁, so g₀ := g₁ − e ≥ 1 exists.
Grounded values appear in increasing position order, so pos(g₁) < pos(g₂) < pos(g₃);
and g₁ is grounded — placed after every smaller value — so pos(g₀) < pos(g₁). Then
(g₀, g₁, g₂, g₃) is an increasing monotone 4-AP: contradiction. A 3-AP inside [M, 2M]
has step e ≤ M/2 < M ≤ g₁, hence is excluded. ∎

Remarks. (i) The one-sidedness of ℕ enters asymmetrically: Λ's forbidden extension is
UPWARD (always exists), so Λ is unconditionally 3-AP-free; Γ's is DOWNWARD (needs
g₁ − e ≥ 1), leaving only huge-relative-step 3-APs. (ii) With the Kelley–Meka bound (in Bloom–Sisask's refined form)
r₃(N) ≤ N·exp(−c(log N)^{1/9}) this is quantitatively much sharper than Lemma 11's
Szemerédi bound, but a ledger-vs-Γ-sparsity argument still cannot push Theorem 12 past
constants — Behrend-type sets are too dense; the true C ≥ 2 extinction mechanism must
be something else (UNSAT-core distillation of the C=2, N=34 instance is the designated
probe). (iii) Finite shadow for machine tests: records w, w+e, w+2e of σ_N with
w + 3e ≤ N; grounded g₁, g₂, g₃ with g₁ − e ≥ 1.

## Lemma 7b (FINlin criterion — scaled variant of Lemma 7)

For K ≥ 1 consider

  FINlin(K): for every c ≥ 1 there is N such that EVERY monotone-4-AP-free permutation
             of [1..N] has some value v ≤ K with pos(v) > c·v.

If FINlin(K) holds for some fixed K, then 196-YES holds.

Proof. Suppose a is a 4-AP-free permutation of ℕ. For each c, the restriction
σ_{N(c)} is a 4-AP-free permutation of [1..N(c)], so some v_c ≤ K has
pos_{σ}(v_c) > c·v_c ≥ c. By pigeonhole some fixed v* ≤ K occurs for unboundedly many
c; since pos_a(v*) ≥ pos_{σ_N}(v*) for every N, pos_a(v*) > c for unboundedly many c —
impossible. ∎

Motivation (experiments/mus_profile.py): the asym C=2 extinction at N=34 is driven
EXACTLY by the profile constraints on the initial segment [1..15] — the minimal
sufficient constraint set is an initial segment. If that pattern persists as c grows
(extinction always driven by an initial segment of bounded length), FINlin is the
natural finite target. Probe: experiments/shallow_scan.py.

## Theorem 14 (ceiling for increasing-only methods; found by route R6, proof re-derived)

Let T be the "triadic reversed-block" permutation of ℕ: list the blocks
I_k = [3^k, 3^{k+1}), k = 0, 1, 2, …, in increasing k-order, each block internally in
DECREASING order. Then:
 (i) T is a permutation of ℕ of order type ω with pos(v) ≤ 3v − 1 for all v;
 (ii) T contains NO increasing monotone 4-AP.
Consequently the hypothesis "pos(v) ≤ Cv" in Theorem 12 cannot force an increasing
4-AP for any C ≥ 3: the critical constant C*_inc for increasing-only extinction
satisfies 43/24 ≤ C*_inc ≤ 3 (lower bound: route R6's CP-SAT certificates), and any
proof of plain-family extinction at C ≥ 3 must engage the decreasing orientation.
(T is NOT a 196-witness: its blocks contain decreasing 4-APs, e.g. (12, 11, 10, 9).)

Proof. (i) Blocks partition ℕ; each value v ∈ I_k sits at position
≤ Σ_{m ≤ k} |I_m| = 3^{k+1} − 1 ≤ 3v − 1 (v ≥ 3^k). Order type ω: every position
filled, every value at a finite position (finite blocks in a listed order).
(ii) Suppose (t₁, t₂, t₃, t₄) is an increasing monotone 4-AP. Blocks are intervals and
in-block order is decreasing, so no two CONSECUTIVE terms tᵢ, tᵢ₊₁ share a block (the
pair would be positionally decreasing); hence the four terms lie in four strictly
increasing blocks (position order = block order). But by scale confinement
(BLOCKS.md Lemma B1): t₂ ∈ I_j ⟹ t₄ = t₂ + 2d < 3t₂ < 3^{j+2} ⟹ t₃, t₄ ∈ I_j ∪ I_{j+1},
so t₃ and t₄ cannot occupy two distinct blocks above I_j. Contradiction. ∎

Machine verification: independent prefix check (values 1..19682): profile and
inc-4-AP-freeness confirmed; dyadic analogue REFUTED — (1, 6, 11, 16) sits at positions
(1, 5, 12, 31), an increasing 4-AP, so ratio 2 does not work (ratio ≥ 3 is forced;
route R6 proved ratio → 3 is exactly the boundary in this family).

## Lemma 15 (record- and grounded-anchored nets — Lemma 4 at infinitely many anchors)

Let a be any monotone-4-AP-free permutation of ℕ, Λ its records, Γ its grounded values
(Lemma 11; both infinite).

(a) For EVERY record w ∈ Λ and EVERY e ≥ 1: ¬( pos(w+e) < pos(w+2e) < pos(w+3e) ).
    Moreover (w, w+e, w+2e) is an increasing monotone 3-AP iff pos(w+e) < pos(w+2e)
    (the first leg w ≺ w+e is automatic for records).

(b) For EVERY grounded g ∈ Γ and every e ≥ 1 with g − 3e ≥ 1:
    ¬( pos(g−3e) < pos(g−2e) < pos(g−e) ).

Proof. (a) A record precedes every larger value, so w ≺ w+e, w+2e, w+3e; if the three
displayed positions increased, (w, w+e, w+2e, w+3e) would be an increasing monotone
4-AP. (b) A grounded value follows every smaller value, so pos(g−e) < pos(g); if the
three displayed positions increased, (g−3e, g−2e, g−e, g) would be an increasing
monotone 4-AP. ∎

Remarks. (i) Lemma 4's (★★) needed j > E(v); at records/grounded values the net is
unconditional at all steps. (ii) Counting consequence: for fixed e, each net instance
forces a drop (pos(u) < pos(u−e)) landing at u ∈ {w+2e, w+3e}, and each u serves at
most 2 records; so #{u ≤ N with an e-drop} ≥ |Λ ∩ [1..N−3e]|/2 — a record-weighted
demand complementing Theorem 12's. Since Λ may be made sparse (records can jump), this
alone does not improve the constant; the ledger is exactly tight on sparse-record
big-jump structures (a huge early record W has e*(W) ≈ W − w and pos(W) ≈ C·w). Any
improvement past C*_inc-style ceilings must couple the two orientations (Theorem 14).
(iii) These nets are the natural constraint set for the two-point supply hunt (R13):
record–record and record–grounded pairs carry overlapping unconditional nets.

## Theorem 16 (forcing closure — an exact ω-reformulation of 196)

Let a be a monotone-4-AP-free permutation of ℕ. Call a value u **open at scale d**
(d ≥ 1, u − 2d ≥ 1) if pos(u−2d) < pos(u−d) < pos(u), i.e. (u−2d, u−d, u) is an
increasing monotone 3-AP. Define the **forcing relation** u ⟶ u+d for each scale d at
which u is open, and let Cl(u) be the forward closure of {u}.

(a) [forcing step] If u is open at d then pos(u+d) < pos(u), i.e. u+d ≺ u.
(b) [closure bound] Cl(u) ∖ {u} ⊆ pred(u); hence |Cl(u)| ≤ pos(u) < ∞ for every u.
(c) [equivalence] Since the forcing digraph is finitely branching at each node
    (scales d satisfy d ≤ (u−1)/2), Cl(u) is infinite iff there is an infinite forcing
    chain u = u_0 ⟶ u_1 ⟶ u_2 ⟶ ⋯ (König). Therefore:

    **196-YES ⟺ every monotone-4-AP-free permutation of ℕ admits an infinite
    forcing chain** (equivalently, an infinite ≺-descending chain, which order type ω
    forbids).

Proof. (a) (u−2d, u−d, u, u+d) is a 4-AP with difference d; its first three terms are
positionally increasing by openness, so pos(u+d) > pos(u) would make it an increasing
monotone 4-AP. Hence pos(u+d) < pos(u) (positions are distinct). (b) Induction along
chains using (a) and transitivity of ≺: every element of Cl(u) other than u is ≺ u, and
pred(u) has exactly pos(u) − 1 elements. (c) König's lemma on the finitely-branching
closure tree; an infinite chain is an infinite ≺-descending sequence, impossible in a
type-ω order (Lemma 1), so no 4-AP-free permutation could exist. ∎

Companion (supply, re-derived here in the form the chain needs):

**Lemma 16.1 (supply).** In ANY permutation a of ℕ, for every value w and every modulus
m ≥ 1 there is a step e ∈ mℕ with (w, w+e, w+2e) positionally increasing.

Proof. The set S = {v > w : v ≺ w} is finite (S ⊆ pred(w)), so with
E := max(S ∪ {w}) − w we have w ≺ w+e for all e > E. Suppose no e ∈ mℕ with e > E makes
(w, w+e, w+2e) increasing. For such e, since w ≺ w+e and w ≺ w+2e, failure forces
pos(w+2e) < pos(w+e), i.e. w+2e ≺ w+e. Apply this along e, 2e, 4e, …(all in mℕ, all
> E): w+e ≻ w+2e ≻ w+4e ≻ ⋯, an infinite ≺-descending chain, contradicting order type ω
(Lemma 1). ∎

Consequences and status.
- Supply makes u := w+2e open at scale e for every value w; so open values are dense in
  the weak sense that every w has an open value in (w, 1.5w]·(scale-free version).
  Each such u forces w+3e ≺ w+2e.
- The remaining gap (identical in shape to route R5's Generic Escape barrier, but now
  phrased on the ω side): supply produces increasing 3-APs *starting* at a prescribed
  value; a chain needs one *ending* at a prescribed value ("co-supply"). Co-supply is
  FALSE for finite boards (the parity permutation σ_N has no monotone 3-AP at all), so
  any proof of it must use order type ω essentially.
- Machine verification (experiments/forcing_closure.py): (a) and (b) hold on ALL
  monotone-4-AP-free permutations of [1..N] for N ≤ 9 (195 154 boards, 0 violations).
  Measurement on SAT-found avoiders: the fraction of open values rises with N
  (35% at N=40 → 64% at N=160) and max closure size grows roughly like N/2
  (9, 19, 20, 32, 65, 78 at N = 40, 60, 80, 100, 130, 160).
- Finite criterion (with Lemma 6): 196-NO requires a compatible tower of finite avoiders
  in which, for each fixed u, the closure size computed inside σ_N stays BOUNDED as
  N → ∞. Closure growth is therefore a direct obstruction measure for the NO side.
