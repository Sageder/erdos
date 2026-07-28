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

    ⚠ SEE THE TWO LATER CORRECTIONS BEFORE USING (c): it is VACUOUS (P ⟺ P) — see
    "Correction to Theorem 16(c)" below — and the programme built on it is DEAD, since
    co-supply is refuted and every forced-descent digraph has a sink (Theorems 44, 47).
    Parts (a) and (b) stand; the quantitative reading of (b) is also corrected in
    Theorem 44.

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

## Remark 17 (STRATEGIC: linear-profile extinction cannot decide 196)

Certified extinction data for the plain target (no monotone 4-AP, both orientations)
under pos(v) ≤ ⌊C·v⌋ — the minimal N with no such permutation of [1..N]:

    C     = 1.25   1.5    1.75   2.0
    N*(C) =    4     15      31    74      <-- 2.0 CORRECTED from 90 (see below)

The C = 1.5 and C = 1.75 entries were obtained twice by unrelated methods (route R9's
exhaustive enumeration of the extension tree and this session's SAT), and C = 2.0 by an eager
two-solver check.

**CORRECTION (found by route R18's auditor, verified by me).** I originally listed
N*(2.0) = 90. That was the first size I happened to test that returned UNSAT — NOT the
minimal one, although the column is headed "minimal N". The true value is 74: the eager
encoding with cadical and glucose agreeing gives SAT at N = 70 and N = 72 and UNSAT at
N = 74. Satisfiability is inherited downward (delete the largest value; no position
increases), so 90 was merely a non-minimal UNSAT point. The fitted law and every number
derived from it are corrected accordingly; Remark 27's conclusion is unaffected in
substance (the revised blind-spot sizes are ≈3.6·10³ at C = 3, ≈9·10⁶ at C = 5,
≈4·10⁸ at C = 6). Lesson, consistent with the rest of this run: a single UNSAT witnesses
extinction AT that size, never minimality — minimality needs the SAT point just below it. Growth is roughly
N*(C) ≈ 4·exp(3.89 (C − 1.25)), so C = 3 would first die near N ≈ 3.6·10³ and C = 5 far
beyond any feasible search — consistent with route R9's independent fit N*(C) ≈ a e^{bC},
b ≈ 2.2–2.8.

The strategic point. It is tempting to read "every linear profile eventually dies" as
progress toward 196-YES. It is NOT, for two independent reasons.

(a) **Lemma 6 quantifies over ALL profiles φ, not just linear ones.** 196-NO requires
    only SOME φ : ℕ → ℕ admitting φ-bounded avoiders at every N. Proving extinction for
    every LINEAR φ leaves φ(v) = v log v, v^{1+ε}, etc. completely untouched. A complete
    "LP theorem for all C" would therefore refute only linear-displacement witnesses.

(b) **The same phenomenon occurs in the known-NO case k = 5.** By [DEGS77](b) an
    infinite monotone-5-AP-free permutation of ℕ exists, yet finite 5-AP-free
    permutations of [1..N] under pos(v) ≤ ⌊1.25 v⌋ go EXTINCT at N = 13
    (experiments/k5_calibration.py; eager encoding, cadical and glucose agreeing).
    So linear-profile extinction is observed in a case where the negative answer is a
    theorem: the signature simply does not distinguish the two branches.
    (Side-by-side: at C = 1.5 and C = 1.75, k = 4 dies at N = 15 and N = 31 while k = 5
    survives past N = 70 — so k = 4 is harder to embed than k = 5, as expected, but the
    qualitative behaviour is shared.)

Consequences for the portfolio. Route R19's LP program is re-scoped: it can prove that
any NO-witness has superlinear displacement — a genuine structure theorem, and the
sharpest constraint we have on a counterexample — but it is not a path to YES.
A YES proof must attack ∀φ-extinction (or avoid Lemma 6 entirely, e.g. via the forcing
chains of Theorem 16). Conversely the NO side gains a concrete, data-driven target:
a construction with displacement pos(v) = Θ(v log v) is consistent with every
certificate obtained so far.

## Remark 18 (where the profile constraint actually bites — the shape of any NO-witness)

Two facts, taken together, locate a candidate NO-witness precisely.

(i) **Small values need not be delayed.** Machine search (experiments/shallow_scan.py)
finds monotone-4-AP-free permutations of [1..N] with pos(v) ≤ 2v for ALL v ≤ 8, at
N = 355 (and with pos(v) ≤ 3v for v ≤ 8 at N = 305). So the FIN/FINlin criteria of
Lemmas 7 and 7b are not realized at accessible parameters: the obstruction to a
counterexample is not "some fixed small value is pushed to infinity".

(ii) **Linear profiles die because they constrain the LARGE values.** pos(v) ≤ Cv for
v comparable to N forces the top of the board into the tail of the position axis, and
that is what the certified extinctions (N* = 4, 15, 31, 90 at C = 1.25, 1.5, 1.75, 2)
are detecting.

A profile of the form φ(v) = v·log₂ v behaves completely differently from a linear one
on a board of size N: since φ(v) ≥ N as soon as v ≳ N/log₂ N, it imposes NO constraint
on the top ~(1 − 1/log₂ N) fraction of values, and constrains only the smaller ones —
i.e. exactly the regime that (i) shows to be unproblematic. This is why v log v is the
natural candidate profile, and why the linear-profile certificates say nothing against
it. The direct test (experiments/vlogv_probe.py: is there a 4-AP-free permutation of
[1..N] with pos(v) ≤ v log₂ v for all v?) is therefore the decisive feasibility question
for the negative branch under Lemma 6; results are recorded in NOTES.md.

Caution for the write-up: none of this is a proof of either branch. (i) and (ii) are
finite computations; the infinite statement needs a construction (with the three
obligations of PROBLEM.md: no monotone 4-AP, bijectivity, order type ω) or an
∀φ-extinction theorem.

## Remark 19 (exactly what the prefix experiments can and cannot prove)

Because pos(v) ≤ N holds automatically on a board of size N, a profile bound
pos(v) ≤ φ(v) is vacuous for every v with φ(v) ≥ N. For a fast-growing φ (say φ(v) = 2^v)
the entire content of Lemma 6 at board size N is therefore a statement about an INITIAL
SEGMENT of values: can 1, 2, …, K be held at bounded positions while N → ∞?

Two directions, with different logical strength — do not conflate them.

(⇒ decisive) If FIN(K) holds for some K — i.e. for EVERY c there is an N such that every
monotone-4-AP-free permutation of [1..N] has some v ≤ K with pos(v) > c·v — then 196-YES
(Lemma 7). A single UNSAT at one c is NOT enough: it must hold for every c. So a machine
UNSAT at (K, c, N) is a genuine finite theorem ("every avoider of [1..N] pushes some
v ≤ K past c·v") and one instance of the family FIN(K) needs, but it does not by itself
resolve the problem.

(⇐ NOT automatic) Suppose that for every K there is a constant c(K) with avoiders at
every N satisfying pos(v) ≤ c(K)·v for all v ≤ K. This does NOT immediately give 196-NO.
Lemma 6 needs ONE profile φ working simultaneously for all values on each board; the
natural candidate φ(v) := c(v)·v is SMALLER than the bound c(N)·v that the hypothesis
supplies at board size N, so the implication fails as stated. Closing that gap requires a
diagonal/compactness argument that produces a single avoider per N meeting all the
prefix bounds at once — an explicit construction is the honest way to get it.

Consequently: prefix experiments (experiments/prefix_bounded.py, shallow_scan.py) can
PROVE the affirmative branch if they go extinct across every c, and can only SUPPORT the
negative branch when they stay satisfiable. The negative branch still requires a
construction discharging all three obligations of PROBLEM.md.

Status of the surrounding certificates (all cross-verified):
- plain pos(v) ≤ 2v: UNSAT at N = 85 under the eager O(N³)-transitivity encoding, with
  cadical and glucose agreeing (298 593 clauses); CEGAR independently UNSAT at N = 90.
- The CEGAR engine reproduces route R9's exhaustive extension-tree thresholds exactly
  (C = 1.5: SAT 14 / UNSAT 15; C = 1.75: SAT 30 / UNSAT 31) and is SAT on unconstrained
  controls at N = 50, 120.

## Remark 20 (the digit-comparator dichotomy — why base-3 orders cannot be repaired)

Define the comparator τ on ℕ: write u, w in base 3 and compare them at the SMALLEST
level where their digits differ, using any fixed linear order on {0,1,2} at that level
(the order may vary from level to level).

(a) **τ kills every monotone 4-AP, on every subset of ℕ, in both orientations.**
Proof. Let t_i = x + (i−1)d, i = 1..4, and let k = v₃(d), m = (d/3^k) mod 3 ≠ 0. All four
terms agree in digits 0..k−1. At level k their digits are a, a+m, a+2m, a (mod 3), since
3m ≡ 0. So the pairs (t₁,t₂), (t₂,t₃), (t₃,t₄) each differ first at level k, while
(t₁,t₄) differs first at a level > k. Write ≺_k for the chosen order on digits at level
k. A monotone increasing arrangement requires a ≺_k a+m (from t₁≺t₂), a+m ≺_k a+2m
(from t₂≺t₃) and a+2m ≺_k a (from t₃≺t₄, whose digits are a+2m and a) — a 3-cycle in a
linear order, impossible. The decreasing orientation reverses all three, equally
impossible. ∎
Machine-verified independently here: no monotone 4-AP on [1..N] for N = 40, 100, 243, 500,
for the natural level orders and for a rotated family (brute-force cross-checked at
N = 12). τ does contain monotone 3-APs, as it must.

(b) **τ is not a permutation of ℕ:** its predecessor sets are infinite. Measured:
pos(2) = 55, 163, 487 on [1..81], [1..243], [1..729] (≈ 2N/3, since 2 has last digit 2),
so value 2 has infinitely many predecessors in the limit — order type ≫ ω.

(c) **The dichotomy.** For the cyclic argument in (a) to run, every pair (u,w) whose
first differing level is k must be decided at level k — that is exactly the
least-significant-digit priority. Any order with that property makes each level-0 digit
class an initial segment of an infinite set, so predecessor sets are infinite. Conversely
a most-significant-digit priority (compare at the LARGEST differing level) has finite
classes [3^k, 3^{k+1}) and order type ω, but is precisely a contiguous block layout,
which routes R1 and R3 killed by exhaustive certificates. Truncating τ at level L(v) does
not escape: an AP with terms ≤ v has critical level k ≤ log₃ v, so protecting all of them
already requires every level up to the top, i.e. full τ.

Consequence for the portfolio: the base-3 (and by the same argument base-b) digit family
is closed — no member is simultaneously 4-AP-free and of order type ω. A NO-witness, if
one exists, must break monotone 4-APs by a mechanism that is NOT "compare at the first
differing digit", and route R16's repair programme must be judged against this
dichotomy rather than against individual failed instances.

## Theorem 21 (explicit 5-AP-free permutation; independent confirmation of [DEGS77](b))

Define a : ℕ → ℕ as the block-major concatenation π₀ π₁ π₂ ⋯ where
  B_m := [4^m, 4^{m+1}) (so |B_m| = 3·4^m, and the B_m partition ℕ), and
  π_m := B_m sorted in van der Corput order (compare binary expansions
         least-significant-bit first, 0 before 1), REVERSED when m is odd.
Then a is a permutation of ℕ of order type ω containing NO monotone 5-term AP.

Order type ω is immediate: the blocks are finite, partition ℕ, and are listed one after
another, so every value occupies a finite position and every position is filled.

Kill mechanism (route R2's argument, reproduced): within a block the van der Corput order
(and its reverse) has no monotone 3-AP, so a monotone DEcreasing AP inside one block has
length ≤ 2; ratio-4 spread forces the last four terms of a 5-AP into at most two adjacent
blocks, so an ascending 5-AP must split as (x)(x+d, x+2d)(x+3d, x+4d) across adjacent
blocks B_m, B_{m+1}; the pair criterion — for u, u+d ∈ B_m with l = v₂(d), u precedes u+d
in π_m iff bit_l(u) = m mod 2 — then demands bit_l(x+d) = m mod 2 and
bit_l(x+3d) = (m+1) mod 2, while (x+3d) − (x+d) = 2d is divisible by 2^{l+1}, forcing
bit_l(x+3d) = bit_l(x+d). Contradiction.

Machine verification (independent re-implementation, exact integer arithmetic, fast
checker cross-validated against the trusted checker on the N = 63 prefix): the value
restrictions to [1..N] are permutations of [1..N] with no monotone 5-AP for
N = 255, 1023, 4095, 16383, 65535. As expected they DO contain monotone 4-APs — the
first is (2, 7, 12, 17) (x = 2, d = 5) — and monotone 3-APs.

## Remark 22 (the 4-versus-5 gap, stated exactly)

Theorem 21 and route R1's impossibility certificates together give the sharpest available
description of why length 4 is hard.

- The construction that settles length 5 is a CONTIGUOUS GEOMETRIC BLOCK LAYOUT: finite
  value-blocks of ratio 4, listed in increasing order, with a digit-order gadget inside
  each block and an alternating reversal. Its top-level structure is most-significant-
  digit-like (finite blocks ⇒ order type ω) and its within-block structure is
  least-significant-digit-like (the van der Corput order ⇒ AP killing). It threads the
  needle of Remark 20 by putting the two priorities at different scales.
- Route R1 proved (SAT over construction stages + König, so the finite UNSATs are
  impossibility theorems quantified over ALL within-block gadgets) that for monotone
  4-APs this entire architecture fails: in-order geometric layouts die at ratio 3 and
  ratio 4, with minimal infeasible cut-set {8, 26, 80}, and bounded-lag interleavings die
  at stage 7.

So the exact mechanism that succeeds at length 5 is provably unavailable at length 4.
That is the concrete content of the gap, and it says what a negative answer would need:
either a layout escaping R1's cut-set certificates (the ratio-5 island, whose depth-5
continuations all came back UNSAT — pending final verification), or a non-block mechanism
outside the digit-comparator dichotomy of Remark 20 entirely.

Independent corroboration of the core structure theory: a fresh-context agent, given only
the problem statement and no route history, re-derived Lemma 13(a) (the record set of a
monotone-k-AP-free permutation is infinite and contains no (k−1)-term AP) and rediscovered
that the one-base-point argument cannot work at length 4 — matching route R5's Generic
Escape Proposition. Two independent derivations of both facts.

## Remark 23 (the pair-counting reason the length-5 mechanism has no length-4 analogue)

Theorem 21's contradiction is a PAIR argument, and it needs TWO pairs.

In a contiguous in-order block layout of ratio r ≥ 3, consider a monotone k-AP
t₁ < ⋯ < t_k. Since t_k < (k−1)·t₂ (because d < t₂), the terms t₂, …, t_k occupy at most
⌈log_r(k−1)⌉ + 1 blocks. So:

- k = 5, r = 4: t₂…t₅ occupy at most 2 blocks, and being four terms in two blocks they
  split as PAIR + PAIR. The pair criterion (u before u+d in π_m iff bit_l(u) = m mod 2,
  l = v₂(d)) applies to BOTH pairs; since the two pairs' first elements differ by 2d,
  which is divisible by 2^{l+1}, their bit_l agree, while adjacent blocks demand opposite
  parities. Contradiction — this is exactly Theorem 21's argument.
- k = 4, r = 3 (or 4): t₂, t₃, t₄ occupy at most 2 blocks, and being THREE terms in two
  blocks they split as PAIR + SINGLETON. Only one pair criterion is available, so it
  yields one condition and no contradiction. The surviving cases (R1's patterns 2+1+1,
  1+2+1, 1+1+2) instead impose "this pair must be inverted" demands on the gadgets, and
  route R1 proved those demands are jointly unsatisfiable at ratios 3 and 4 for EVERY
  gadget choice.

Machine confirmation (this session, independent implementation): the natural length-4
analogues of Theorem 21 — ratio-3 blocks with a van der Corput internal order, base 2 or
base 3, with or without alternating reversal — all contain monotone 4-APs at once:

    ratio 3, base-2 vdC, alternating : (2, 5, 8, 11)   increasing
    ratio 3, base-2 vdC, no reversal : (5, 7, 9, 11)   increasing
    ratio 3, base-3 vdC, alternating : (8, 9, 10, 11)  increasing
    ratio 3, base-3 vdC, no reversal : (1, 2, 3, 4)    increasing

and (2, 5, 8, 11) is precisely a 1+2+1 pattern (2 ∈ B₀, 5, 8 ∈ B₁, 11 ∈ B₂) — the
pair-plus-singleton case with no second pair to play against it. The same script
reconfirms the control: the ratio-4 base-2 alternating construction has no monotone 5-AP.

Reading: the length-5 solution is a two-pair parity argument, and four terms simply do
not supply two pairs at any ratio ≥ 3. A negative answer at length 4 therefore needs a
mechanism that extracts a contradiction from ONE pair plus singletons, or an architecture
in which 4-APs are forced to straddle blocks in pairs — which is what route R1's cut-set
and island analysis was probing, and where its certificates currently say no.

## Lemma 24 (coupled family: every affine sub-copy has a 3-AP-free record set)

Let a be a monotone-4-AP-free permutation of ℕ. For α ≥ 1, β ≥ 0 let
P = {β+α, β+2α, β+3α, …}, and let a|_P denote the values of P listed in a-position order.
Let R(P) := the running maxima (records) of a|_P, i.e. the v ∈ P larger than every
P-value positioned before v. Then for EVERY such P:

    R(P) is infinite and contains no 3-term arithmetic progression.

The same holds for every value-tail P = {m, m+1, m+2, …}.

Proof. The map ι(β+jα) = j is an order isomorphism of P onto ℕ carrying APs to APs in
both directions (affine maps preserve arithmetic progressions and their orientations).
Listing P in a-position order gives a linear order on P in which every element has only
finitely many predecessors (its P-predecessors are a subset of its a-predecessors), so by
Lemma 1 the transported order is a permutation of ℕ. It is monotone-4-AP-free: a monotone
4-AP of a|_P is, after applying ι^{-1}, a monotone 4-AP of a. Lemma 13(a) applied to that
permutation says its record set has no 3-term AP and is infinite; transporting back by ι
gives the claim. ∎

Remark. This upgrades Lemma 13(a) from one 3-AP-free set to an infinite COUPLED family of
them — one for every arithmetic progression and every tail, all living inside a single
order. The fresh-eyes route independently identified the same coupling and named the
right obstacle: each R(P) may be arbitrarily sparse (running maxima can jump far), so
there is no density lower bound to play against Roth's theorem, and absent further
constraints any prescribed infinite set is realizable as a record set. A contradiction
would therefore have to come from the COUPLING between different P — e.g. a lower bound
on |R(P) ∩ [1..N]| for suitably chosen P, or an incompatibility between R(ℕ) and R(P)
for P a sub-progression. Both are open; note that any such lower bound must be consistent
with Theorem 21's 5-AP-free permutation under the analogous (weaker) statement, which is
a useful sanity target for candidate inequalities.

## Remark 25 (why the length-5 sign must be carried by a convex block partition)

Remark 23 showed the length-5 argument needs two pairs, which four terms cannot supply.
There is a natural attempt to escape this: keep ONE pair and get the second constraint
from an arithmetic sign instead of a block parity. Spelled out, one looks for a rule

    u ≺ u+d  ⟺  ε(u, l) = bit_l(u),     where l = v₂(d)

(note l is exactly the lowest bit at which u and u+d differ, so this is the general shape
of a van der Corput-style rule). For a monotone 4-AP with v₂(d) = l one has
t₃ = t₁ + 2d with v₂(2d) = l+1, hence bit_l(t₁) = bit_l(t₃); so if ε could be made to
FLIP between t₁ and t₃ — e.g. ε(u,l) := bit_{l+1}(u), which does flip when 2^{l+1}·odd is
added — then exactly one of "t₁ ≺ t₂", "t₃ ≺ t₄" could hold, killing both orientations at
once, with no blocks and no second pair.

This fails, and the reason is instructive: **such rules are not transitive.**
Machine classification (exact, exhaustive over the family ε(u,l) = f_l(bit_{l+1}(u)) with
f_l ∈ {0, 1, id, not} independently at each level l):
  - ε = bit_{l+1}(u), its complement, the parity of u above level l, and bit_{l+2}(u) all
    fail transitivity on [1..40], with witnesses as small as (1,2,3) and (1,4,5);
  - over the whole family, only 16 of 256 combinations (levels l = 0..3) are transitive on
    [1..64] and on [1..96], and NONE of them is genuinely u-dependent — every transitive
    member has the sign constant in u at each level where bit_{l+1} actually varies.
    (Apparent u-dependent survivors at the top level are a boundary artifact: there
    bit_{l+1} is constant on the tested range.)
  - The constant-sign member is exactly the van der Corput order, which is the base-2
    comparator τ₂ of Remark 20: transitive, kills even 3-APs — and has infinite
    predecessor classes (evens before odds), so it is not a permutation of ℕ.

Conclusion. A sign that varies with u cannot be an arithmetic function of u's bits above
the critical level; transitivity forces it to be constant on the pieces of a CONVEX
partition — which is precisely what a block layout provides, and why Theorem 21 carries
the sign in the block index. But then the argument only bites when t₁ and t₃ lie in
different blocks, i.e. when the AP straddles a boundary in PAIRS — and by Remark 23 four
terms cannot straddle in pairs at any ratio ≥ 3. The block layout is therefore not an
incidental choice in the length-5 construction but a forced one, and this closes the
"replace block parity by an arithmetic sign" escape route for length 4.

## Correction to Remark 22 (2026-07-28, from route R1's final pass)

Remark 22 said the block architecture "fails for 4-APs", citing R1's certificates. That
statement must be narrowed, and the narrowing matters.

What R1's certificates actually establish is the death of GEOMETRIC in-order layouts at
ratios 3 and 4 (minimal infeasible cut-set {8, 26, 80}) and of bounded-lag interleavings
(stage 7). Earlier depth-5 probes returned UNSAT only for continuations of the SPECIFIC
prefix {2, 8, 26, 140}. R1's final pass, scanning other prefixes, finds DEPTH-5 FEASIBLE
cut sequences — for example

    [1, 2, 4, 10, 90],  [1, 2, 4, 10, 91],  [1, 2, 4, 10, 92]

whose successive ratios (2, 2, 2.5, 9) are ACCELERATING and non-geometric. So the
in-order block program is NOT closed: the feasible window moves as the prefix changes
rather than vanishing, exactly the behaviour the window law predicted and the reason that
"does the island simply move?" was the right question to ask.

Consequently the honest status is:
- geometric ratios 3 and 4, and bounded-lag interleavings: DEAD (certificates);
- tuned accelerating cut sequences: ALIVE at depth 5, unknown beyond;
- Remarks 23 and 25 are unaffected — they explain why the length-5 PAIR mechanism has no
  length-4 analogue and why its sign must be carried by a convex partition. They do not
  by themselves close the block family; a surviving layout would have to kill 4-APs by
  some other within-block mechanism, and whether the accelerating corridor supports one is
  precisely what remains open.

Discipline note: this is the second time in this run that a negative reading of finite
certificates had to be narrowed (the first being Remark 17, where linear-profile
extinction turned out not to discriminate the branches at all). Finite UNSATs bound only
the exact family they quantify over.

## Corollary 26 (AP-restriction principle for displacement — route R20, verified)

Let a be a monotone-4-AP-free permutation of ℕ and P = {r+q, r+2q, …} any infinite
arithmetic progression. Transport the induced order on P to ℕ by n ↦ r+qn. Then the
transported order is a monotone-4-AP-free permutation of ℕ of order type ω. (Same proof
as Lemma 24's first step: affine maps carry APs to APs in both directions, and
P-predecessors are a subset of a-predecessors, so Lemma 1 applies.)

Consequence: EVERY quantitative theorem about 4-AP-free permutations applies to every AP
restriction simultaneously. In particular Theorem 12 gives
limsup_n pos_P(n)/n ≥ 9/8 for every infinite AP P, and the certified linear-profile
extinctions apply to each restriction separately.

**Design principle D1** (conditional on linear-profile extinction holding at every C —
which is NOT proved; see Remark 17): a NO-witness must have unbounded relative
displacement along EVERY infinite AP, not merely globally. This is a far sharper filter
than any global profile condition, and route R20 used it to kill the natural
"delay by 2-adic valuation" architectures: in those, the odd numbers carry constant delay,
so the restriction to the odds is an in-order geometric block ordering with linear
displacement.

## Remark 27 (SEARCH BLIND SPOT — a methodological warning that qualifies several results)

From the certified extinction law N*(C) ≈ 4·exp(3.89(C − 1.25)) (Remark 17, as corrected), a design
whose AP-restriction has linear displacement with constant C cannot die before roughly

    C = 3 : N ≈ 3.6·10³    C = 5 : N ≈ 9·10⁶    C = 6 : N ≈ 4·10⁸

So verifying a candidate construction to M = 10⁴–10⁵ — the standard bar used throughout
this project — CANNOT certify or refute any design with displacement constant ≳ 3.
Consequences that must be carried forward:
- Route R1's surviving ratio-5/6 corridor (including the depth-5 feasible cut sequences
  [1,2,4,10,90…92]) sits squarely in this blind spot: its survival at reachable sizes is
  NOT evidence of survival.
- Route R20's CLS(5,a) architecture, alive at N = 250 over all within-class orders, is in
  the same blind spot, whereas CLS(3,a) died at N = 250 — consistent with the law rather
  than with a real difference in viability.
- Conversely, an UNSAT obtained at reachable N for a low-C design is genuinely
  informative, because the law says such designs should die early.
The methodological upshot: for the negative branch, only an explicit rule with a PROOF
can settle anything in the C ≳ 3 regime; finite verification is structurally incapable of
it. For the affirmative branch, extinction certificates at small C say nothing about
large C (and by Remark 17 would not decide the problem even if extended to all C).


## Remark 28 (audit discharge: the v log v falsification is verified)

Route R20's α-wall UNSAT at φ_{0.5}(v) = ⌈0.5·v·log₂(2v)⌉, N = 130, was obtained by
single-solver CEGAR and was flagged by its own author as the outstanding audit item. It is
now independently re-verified with the eager O(N³)-transitivity encoding (932 414 clauses)
by TWO solvers, cadical and glucose, both returning UNSAT and agreeing
(experiments/verify_r20_alpha.out).

So the following is certified to the project's verification standard: there is NO
monotone-4-AP-free permutation of [1..130] with pos(v) ≤ ⌈0.5·v·log₂(2v)⌉ for all v.
By Lemma 6 that profile is dead as a candidate for the negative branch, and the
"displacement Θ(v log v)" target proposed earlier in this run is falsified for the natural
one-parameter family. The surviving negative-branch question is not the SHAPE of the
profile but AP-uniformity (Corollary 26, design principle D1).

## Proposition 29 (class-architecture tameness bound — route R21, verified)

Let c : ℕ → ℤ≥0 have finite fibres F_j, with classes emitted in increasing index order and
ARBITRARY orders within each class. Call an infinite AP P *tame* if c|_P is weakly
increasing from some index n₀ on. For tame P and n > n₀,

    pos_P(n) ≤ (n − 1) + |F_{c(p_n)} ∩ P|,   hence
    sup_{n>n₀} pos_P(n)/n ≤ 1 + R_P,   R_P := sup_j |F_j ∩ P| / (1 + |P ∩ (F_0∪…∪F_{j−1})|).

Proof. Weak monotonicity beyond n₀ means every P-element in a strictly lower class has
index < n and is emitted earlier; inside p_n's own class at most |F_{c(p_n)} ∩ P| − 1
further P-elements can precede it. Divide by n at the first index of the class. ∎

Consequence: a geometric fibre design (|F_j| ≍ b^j, so R_P = O(b)) forces LINEAR
displacement along every tame P — so P violates design principle D1 (Corollary 26).
This holds uniformly over all within-class orders, so it is an impossibility statement
about the architecture, not about a particular gadget.

## Corollary 30 (every congruence-determined delay fails D1 — the arithmetic world closed)

Let c = j + t where j is a non-decreasing geometric block index and t : ℕ → ℤ≥0 is
finite-valued. Put U_k := {v : t(v) ≥ k} and let k* be least with U_{k*} ≠ ℕ (it exists as
t is finite-valued; note U_0 = ℕ, so k* ≥ 1). If U_{k*} is a union of residue classes
modulo some m, then t is CONSTANT on an infinite AP, that AP is tame, and by
Proposition 29 the architecture has linear displacement there — D1 fails.

Proof. By minimality U_{k*−1} = ℕ, so t ≥ k*−1 everywhere. The complement of U_{k*} is a
nonempty union of residue classes mod m, hence contains a full class P = r + mℕ. On P we
have k*−1 ≤ t < k*, so t ≡ k*−1 there, and c|_P = j|_P + const is non-decreasing: P is
tame. ∎

This retires, in one line and for ALL geometric-fibre class architectures at once:
ρ(v_p(v)) for every prime p, the shifted family ρ(v_p(v+s)), every function of v mod m,
and every finite Boolean combination of congruence conditions — i.e. the entire arithmetic
delay world. In particular route R20's surviving candidate CLS(5,a) (t = v₂) is now
D1-dead BY PROOF rather than by a search sitting in the blind spot of Remark 27: there
{v₂ ≥ 1} is the even numbers, so the odd numbers form a tame AP on which the delay is
constant. (Verified: exactly the tame-AP families route R21 measured, 14 of the 36 APs
with q ≤ 8 for both CLS(3,a) and CLS(5,a), with the bound 1+R_P nearly tight against the
measured maxima.)

## Remark 31 (the AP-uniformity experiment was VACUOUS — a mis-specification, recorded)

The coordinator endorsed route R20's closing recommendation and commissioned a direct
search for a class function with finite fibres, no strictly monotone 4-AP class sequence
(condition (ii)), and maximal displacement along every AP of step ≤ 8. Route R21 showed
the experiment as specified cannot decide anything, for two proved reasons:

(a) **The objective is degenerate.** max_σ min_{q≤8,r} max_n pos_P(n)/n equals the trivial
    bound min_{q,r} |P_{q,r} ∩ [1..N]| ≈ N/8, attained by any avoider that places the
    values 1…15 after all larger ones (certified: N=60 → 6, N=100 → 11). The optimum is
    realised at index n = 1 and says nothing about D1.
(b) **Feasibility is automatic and infeasibility is impossible.** For ANY finite avoider
    and any b > 1, the geometric coarsening c(v) := j where pos(v) ∈ [b^j, b^{j+1})
    has exactly the geometric fibre design and satisfies (ii) (a strictly monotone class
    sequence along a 4-AP would make pos monotone along it). Since avoiders exist at every
    N, the system (i)+(ii) can never go extinct. And every finite avoider already meets the
    γ-floor of Remark 17 along every AP, so infeasibility of D1 cannot be certified at any
    level ≤ γ.

So D1 has no independent finite content: it is exactly Corollary 26 plus universal linear
extinction, and neither branch can be advanced by searching for it. What survived the
exercise is Proposition 29 and Corollary 30 — obtained by proof, not by search — and the
open Conjecture R21-C below.

**Conjecture R21-C (open).** For c = ⌊log_b v⌋ + t with a geometric fibre design,
condition (ii) forces t to be constant on some infinite AP. If true, no block-index-plus-
delay architecture is D1-compatible. It is NOT implied by Corollary 30 (which assumes
congruence-determinacy), and by (b) above it cannot be settled by finite search — any
argument that would also apply to the geometric coarsening of a finite avoider is wrong.
That last sentence is the sanity check every candidate proof must pass.

## Remark 32 (a natural proof of R21-C fails, and the natural refutation fails too)

Two attempts on Conjecture R21-C, both by the coordinator, both recorded as FAILED with
their exact failure points. Neither is a claim.

**(a) The van der Waerden route — GAP, not a proof.** Suppose t is bounded by T. Colouring
ℕ by t uses T+1 colours, so van der Waerden gives arbitrarily long finite APs on which t is
constant; on such a window W, c = j + const is non-decreasing (j = ⌊log_b ·⌋ is
non-decreasing along every AP — verified). One then hopes to bound the displacement of the
restriction to W and contradict linear-profile extinction. The window bound itself is
correct and machine-verified (experiments/bounded_delay.py): for every n,
pos_W(n) ≤ n + #{m : j(p_m) = j(p_n)}. **But the resulting displacement is NOT bounded by
O(b).** The ratio pos_W(n)/n is dominated by SMALL n, and a vdW window sits at an arbitrary
position: if W begins at the start of a block, then at n = 1 the bound is 1 + (number of
W-elements in that block), which grows with the block. Only when W is an INITIAL segment of
its progression does the telescoping give ratio ≈ b, and van der Waerden gives no control
over position. Measured maxima over random windows: ≈3–4 for b=2,3 and up to 19 for b=5,
fluctuating with the window's placement rather than converging to b. So this route needs
either a positioned-window vdW variant or a displacement statistic insensitive to small n —
note that route R21's Proposition R21-2 shows the small-n sensitivity is exactly what made
the AP-uniformity objective degenerate, so this is the same trap in a new guise.

**(b) The Sturmian refutation — REFUTED.** The natural way to falsify R21-C is an aperiodic
delay whose level sets are not unions of residue classes (required, by Corollary 30) and
which is non-monotone along every progression (so that no tame AP exists). The canonical
candidate is a Beatty/Sturmian delay t(v) = 1 if {vα} < β else 0 with α irrational. Such t
does have both properties. But it FAILS condition (ii) immediately, for every parameter
tested (α a high convergent of the golden ratio, β ∈ {1/2, 1/3, 2/3}, b ∈ {3,4,5}; exact
rational arithmetic, values to 4000):

    b=3, β=1/3: fails at x=1,  d=3   with classes (0,1,2,3)
    b=4, β=1/3: fails at x=3,  d=5   with classes (0,1,2,3)
    b=5, β=1/2: fails at x=17, d=36  with classes (1,2,3,4)

Every failure has the same shape: the class sequence rises by exactly 1 at each step, with
the block index supplying part of the increase and the delay the rest — e.g. for b=4,
x=3, d=5 the values 3, 8, 13, 18 have block indices (0,1,1,2), so t = (0,0,1,1) completes a
strictly increasing class sequence. Condition (ii) therefore forbids the delay from taking
the pattern (0,0,1,1) on any progression whose block indices read (j, j+1, j+1, j+2), and
aperiodic delays of Sturmian type hit that pattern almost immediately.

**Reading.** (b) is mild evidence FOR R21-C: condition (ii) is restrictive enough to kill
the most natural aperiodic candidate at once. (a) says the most natural proof strategy does
not work as stated. The conjecture remains open, and the two failures together sharpen it:
a refutation needs an aperiodic delay avoiding the (0,0,1,1)-on-(j,j+1,j+1,j+2) pattern and
all its analogues, while a proof needs a displacement statistic that is not dominated by
small indices.

## Correction to Theorem 16(c) (self-audit prompted by the route R19 audit, 2026-07-28)

The route R19 audit rated that route's analogous claim — "196-YES ⟺ some value has an
infinite mixed chain" — as **SOUND BUT VACUOUS (P ⟺ P)**. The same criticism applies to
Theorem 16(c) above, and it is correct. Recorded here rather than quietly left standing.

Theorem 16(c) reads: 196-YES ⟺ every monotone-4-AP-free permutation of ℕ admits an
infinite forcing chain. Both directions are immediate: if 196-YES there are no such
permutations and the right-hand side is vacuously true; if 196-NO then part (b) says the
closures of the witness are finite, so it admits no infinite chain. So (c) is a genuine
equivalence but carries no information beyond (b) — it is "YES ⟺ no counterexample exists"
in chain language. It should NOT be described as a reduction of the problem, and earlier
descriptions of it in this file and in the run's reports as "an exact ω-reformulation"
overstate it.

What Theorem 16 does contribute, and what survives unchanged:
- **(a) is a real constraint.** If (u−2d, u−d, u) is positionally increasing then u+d must
  precede u. This is a usable local forcing rule, verified exhaustively on all 195 154
  avoiders with N ≤ 9.
- **(b) is a real quantitative constraint.** The forward closure Cl(u) sits inside pred(u),
  so |Cl(u)| ≤ pos(u): a lower bound on closure size is a lower bound on position. That is
  genuine content and is what any use of Theorem 16 should rest on.
- The heuristic value of (c) is that it names the missing ingredient precisely (co-supply —
  an increasing 3-AP ENDING at a prescribed value), which is why the route was worth
  running. Naming a target is not reducing a problem.

Discipline note: this is the third vacuity-or-overstatement caught in this run
(Remark 31's degenerate objective, route R17's circular biconditional, and now this).
All three had the same shape — an equivalence or optimum that is true but empty. Every
future claimed reformulation in this project must be checked by asking explicitly whether
it is P ⟺ P.

## Remark 33 (third independent confirmation of the extinction data)

The route R19 audit re-derived the plain-target extinction certificates by **exhaustive
DFS over the insertion tree with no SAT solver at all**, independently confirming
extinction at C = 1, 5/4, 3/2, 7/4. Together with this session's CEGAR results and the
eager two-solver encoding, the low-C extinction table now rests on three methodologically
independent computations. The audit also found two data-integrity defects in that route's
own artifacts (one bad table row and five stored witnesses that do not verify) — those are
recorded in its AUDIT.md and do not affect the confirmed certificates.

## Lemma 34 (far-left reduction of condition (ii)) — proved, machine-verified

Setting: class architecture c = j + t, j(v) = ⌊log_b v⌋, t : ℕ → ℤ≥0 finite-valued.
Fix x ≥ 1 and let d be large enough that

    (FL)    j(x) + t(x) < j(x+d)

— true for all d beyond a finite threshold, since t(x) is a fixed number and
j(x+d) → ∞. Write u_i = x + i·d (i = 1,2,3) and k = j(u_1). Then:

**(1) Far-left APs constrain only the INCREASING orientation.** (FL) gives
c(x) = j(x)+t(x) < j(u_1) ≤ c(u_1), so c(x) > c(u_1) is impossible and the decreasing
pattern cannot occur. (A genuine asymmetry: the architecture's decreasing orientation is
free at far-left APs, all the content is in the increasing one.)

**(2) On these APs condition (ii) is EQUIVALENT to a condition on t alone.** By the
block-gap lemma (j₃ ≤ j₁+1 since x+3d < 3(x+d) ≤ b(x+d) for b ≥ 3) the pattern
(j(u_1), j(u_2), j(u_3)) is one of (k,k,k), (k,k,k+1), (k,k+1,k+1), and (ii) says exactly

    (k,k,k)      :  ¬( t(u_1) <  t(u_2) <  t(u_3) )
    (k,k,k+1)    :  ¬( t(u_1) <  t(u_2) ≤  t(u_3) )
    (k,k+1,k+1)  :  ¬( t(u_1) ≤  t(u_2) <  t(u_3) )

**(3) The constrained triples are the "geometric" ones.** Taking x small, d = u−x with
u = u_1, the triple is (u, 2u−x, 3u−2x) — for x = 1, exactly (u, 2u−1, 3u−2). So (ii)
constrains t on every triple of the shape (u, ≈2u, ≈3u), at every scale.

Verification (experiments/farleft.py, exact integer arithmetic, x ≤ 3, values to 20 000,
b ∈ {3,4,5}, five delay families): (1), (2) and the block-gap lemma hold in every one of
≈300 000 far-left instances, with zero exceptions. Measured pattern frequencies (b=3):
(k,k,k) 0%, (k,k,k+1) 26%, (k,k+1,k+1) 74%; (b=5): 39% / 32% / 29%. Delay families
t = v₂(v), t ≡ 0 and t = 1_{odd} have zero (ii)-violations; t = v mod 3 and a random
delay violate on ≈11% of far-left APs.

**Specialization to t ∈ {0,1} (the first open case beyond Corollary 30).** With two values
the (k,k,k) constraint is vacuous, and the other two read: pattern (k,k,k+1) forbids
(t(u), t(2u−1), t(3u−2)) = (0,1,1); pattern (k,k+1,k+1) forbids (0,0,1). For b = 3 the
pattern is (k,k,k+1) for u in the lower part of block k and (k,k+1,k+1) in the upper part,
so: whenever t(u) = 0 and t(3u−2) = 1, the value t(2u−1) is FORCED — to 0 for u low in its
block, to 1 for u high. The congruence solution t = 1_{odd} satisfies this (its triples read
(0,1,0), which is neither forbidden pattern) but is killed by Corollary 30. So the sharp
open question for T = 1 is whether a NON-congruence-determined 0/1 delay can satisfy these
forcings while leaving no progression on which t is eventually non-decreasing.

## Lemma 35 (local descent rules: the delay cannot rise twice in a row) — verified

Immediate from Lemma 34, for far-left triples (u₁, u₂, u₃) with u₂−u₁ = u₃−u₂ = d:

    block pattern (k,k,k+1)   :  t(u₁) <  t(u₂)  ⟹  t(u₃) <  t(u₂)
    block pattern (k,k+1,k+1) :  t(u₁) ≤  t(u₂)  ⟹  t(u₃) ≤  t(u₂)
    block pattern (k,k,k)     :  t(u₁) <  t(u₂)  ⟹  t(u₃) ≤  t(u₂)

In words: along far-left triples a rise in the delay must be followed by a fall — the delay
cannot rise twice in a row. This is the exact analogue, one level up, of the descent-word
conditions of ASYM.md (no 000 / no 111 along every progression).

Verification (exact, values to 12 000, b ∈ {3,4,5}): the rules fire 4 400–7 900 times per
family per base with ZERO violations for every delay family that satisfies condition (ii)
(t = v₂(v), t = 1_odd, t ≡ 0), and are violated ≈1 300 times by t = v mod 3, which does not
satisfy (ii) — so the test has teeth in both directions.

**Specialization to t ∈ {0,1}, and what tameness means there.** With c = j + t and j
non-decreasing, c decreases along a progression only at a step where the block index does
NOT increase and t falls from 1 to 0. Along a fixed progression of step q, steps at which
the block index increases have density → 0 (there are only O(log X) block boundaries below
X). Hence: a progression is tame precisely when the delay's descents along it are confined
to those rare boundary steps — i.e. when t is eventually constant along it apart from
vanishing density. So at T = 1, Conjecture R21-C says: condition (ii) forces the delay to be
eventually constant along some progression.

## Remark 36 (two encoding traps hit while testing T = 1 — recorded, both were mine)

Both were caught by re-verifying solver models against the literal definition, which is why
that step is non-negotiable in this project.

1. **Degenerate finite proxy.** Encoding "no tame progression" as "a descent somewhere in
   the second half of each progression window" is satisfied trivially by a delay that is 1
   almost everywhere (all the (ii) constraints have t(u₁) = 0 in their forbidden patterns,
   so an almost-constant delay makes them vacuous), and a handful of well-placed zeros
   covers all the finitely many progressions tested. The correct proxy demands a descent in
   EVERY window of L consecutive progression elements — a positive descent rate. This is the
   same failure shape as Remark 31; finite proxies for asymptotic conditions must bound a
   RATE, not merely require one occurrence.
2. **Dropped clauses at automatic steps.** When a step of the 4-AP jumps ≥ 2 block indices
   the corresponding class comparison is automatically increasing. Treating that as "no
   literal available" and skipping the whole clause silently removes the constraint. The
   correct encoding lets such a step contribute nothing to the conjunction and forbids the
   REMAINING steps. (By the block-gap lemma D₂ + D₃ ≤ 1, so at most the first step can be
   automatic and the clause is never empty.) The bug produced spurious SAT results that the
   literal re-check caught immediately at (x, d) = (2, 10), values 2, 12, 22, 32 with block
   indices (0,2,2,3).

Corollary of trap 1 for the far-left programme: the far-left constraint set of Lemma 34 is
STRICTLY WEAKER than full condition (ii) — a delay satisfying all far-left constraints at
N = 3000 was found that violates full (ii) at (x, d) = (7, 11). So Lemma 34 localises the
condition usefully but cannot by itself settle Conjecture R21-C; the near-left APs carry
essential content.

## Proposition 37 (complete characterization of condition (ii) at T = 1) — proved

Let c = j + t with j = ⌊log_b ·⌋ and t : ℕ → {0,1}. For a 4-AP (x, x+d, x+2d, x+3d) put
D₁ = j(x+d) − j(x), D₂ = j(x+2d) − j(x+d), D₃ = j(x+3d) − j(x+2d) (all ≥ 0, and
D₂ + D₃ ≤ 1 by the block-gap lemma). Then:

**(a) The decreasing orientation is impossible outright.** A step can decrease the class
only when its block jump is 0 and t falls 1 → 0; three consecutive such steps would need
t = 1,0 then 1,0 then 1,0 on overlapping pairs, forcing t(x+d) = 0 and = 1. So at T = 1 the
architecture never contains a decreasing class sequence, for ANY t. All of condition (ii)
lives in the increasing orientation.

**(b) The increasing orientation reduces to two forbidden patterns.** Since D₂ + D₃ ≤ 1:
- (D₂,D₃) = (0,0): steps 2 and 3 would both need a rise, forcing t(x+2d) = 1 and = 0.
  Impossible — no constraint.
- (D₂,D₃) = (0,1): violation ⟺ (t(x+d), t(x+2d), t(x+3d)) = (0,1,1) and step 1 increases.
- (D₂,D₃) = (1,0): violation ⟺ (t(x+d), t(x+2d), t(x+3d)) = (0,0,1) and step 1 increases,
where "step 1 increases" means D₁ ≥ 2, or D₁ = 1 and t(x) = 0 (D₁ = 0 is impossible here
since it would need t(x+d) = 1).

**(c) The (1,0) case is a closure property of the zero set.** Writing Z := t^{-1}(0) and
u := x+d, the (1,0) constraint says exactly

    u ∈ Z  and  u+d ∈ Z   ⟹   u+2d ∈ Z,

i.e. **Z is closed under completing an arithmetic progression by one more step**, for every
(u,d) whose block geometry is (1,0) and whose step-1 condition holds. Working out the
geometry for b = 3: this applies for u in the upper half of its block (u ≥ (3^{k+1}+1)/2)
and 3^{k+1} − u ≤ d ≤ min(u−1, (3^{k+2}−u)/2); at d = u−1 the preceding term is x = 1 and
the step-1 condition is automatic.

**Consequence and proof route for T = 1 (not yet a proof).** Sets closed under
(u, w) ↦ 2w−u are highly rigid — unrestricted closure in both directions forces a coset of
a subgroup, i.e. an arithmetic progression. Our closure is one-directional and
range-restricted, so rigidity is not immediate; but if it can be shown to force Z to be a
union of residue classes (or to differ from one by a density-zero set), then Corollary 30
applies and yields a tame progression, proving Conjecture R21-C at T = 1. The two
degenerate possibilities are already handled: Z = ∅ makes t ≡ 1, constant, hence every
progression tame; and Z a full residue class is congruence-determined, again Corollary 30.
The open case is a Z that is neither.

Status: (a), (b), (c) are proved. The rigidity step is CONJECTURED and is exactly what the
running experiment (experiments/t01_full.py, full-(ii) encoding with a positive
descent-rate proxy and a non-periodicity requirement) is testing.

## Proposition 38 (a proof route for Conjecture R21-C at T = 1) — one step still conjectural

Setting as in Proposition 37: c = j + t, t : ℕ → {0,1}, Z := t^{-1}(0), b = 3. Recall the
two rules extracted there (each valid for the (u,d) whose block geometry and step-1
condition apply):

    (R↓)  u ∈ Z  and  u+d ∈ Z    ⟹  u+2d ∈ Z        [the (1,0) pattern]
    (R↑)  u ∈ Z  and  u+d ∉ Z    ⟹  u+2d ∈ Z        [the (0,1) pattern]

Note both rules conclude membership in Z: the constraints push everything TOWARD the zero
set. The route:

**Case 1 — Z misses some progression eventually.** Then along that progression t ≡ 1, so
c = j + 1 is non-decreasing there: the progression is TAME, and Proposition 29 gives linear
displacement. Done.

**Case 2 — Z meets every progression infinitely often.** Then (CONJECTURAL STEP) the
closure under (R↓) forces the density of Z to tend to 1. Granting that, Z^c has density → 0;
but rule (R↑) says that for every u ∈ Z and every w ∈ Z^c with w−u in the valid range,
2w−u ∈ Z. With Z of density → 1 the points 2w−u sweep almost everything, so Z^c must be
finite. Then t ≡ 0 on a tail, c = j is non-decreasing along every progression, and every
progression is TAME. Done.

So both cases produce a tame progression, which is exactly Conjecture R21-C at T = 1.

**Evidence for the conjectural step** (experiments in this session, exact arithmetic, b = 3,
closure computed inside [1..N]):
- Residue classes are FIXED POINTS of the closure (0 mod 2 stays at density 0.5, 1 mod 3 at
  0.333) — as they must be, since they are the congruence solutions Corollary 30 handles.
- Random seeds show a sharp percolation-like threshold, and **the threshold moves toward 0
  as N grows**: at seed density 0.002 the closure reaches density 0.002, 0.046, 0.333 for
  N = 1500, 4500, 13500; at 0.005 it reaches 0.081, 0.271, 0.607; at 0.01 it reaches 0.022,
  0.546, 0.665.
- The decisive case: a DENSITY-ZERO set that still meets every progression infinitely often
  (Z₀ = ⋃_k {v ∈ [2^k, 2^{k+1}) : v ≡ k mod (k+1)}, density ≍ 1/log N, AP-dense by CRT)
  blows up to density **0.908, 0.936, 0.964** at N = 2000, 6000, 18000, and its closure
  misses NO progression of step ≤ 8 in the top half of the range.

So the numerics support exactly the statement Case 2 needs, and the trend in N is the right
one. What is missing is a proof that AP-density forces the closure to have density → 1;
that is an additive-combinatorics statement about sets closed under range-restricted
AP-completion, and it is the single remaining gap at T = 1.

**Caveats, explicitly.** (i) All of the above is the T = 1 case; the conjecture is about
arbitrary bounded (indeed arbitrary finite-valued) delays. (ii) The numerics are finite and
this project has repeatedly shown that finite evidence about asymptotic statements can
mislead — see Remarks 17, 27, 31, 36. (iii) Even a complete proof of R21-C at T = 1 would
not resolve Erdős 196; it would close one architecture family (block-index-plus-bounded-
binary-delay) on the negative branch.

## Proposition 39 (the missing step of Proposition 38 is an inverse-sumset dichotomy)

The gap in Proposition 38 was: does progression-density force the closure of Z to have
density → 1? Here is the precise additive-combinatorial shape of that step, which converts
it from a vague "blow-up" into a standard dichotomy.

Fix b = 3 and a block index k. Put
    A' := Z ∩ [2.25·3^k, 3^{k+1})      (top of block k),
    W  := [3^{k+1}, 1.5·3^{k+1}),      B_W := Z ∩ W,      B := Z ∩ block (k+1).
For u ∈ A' and w ∈ B_W one checks the block geometry is the (1,0) pattern with the step-1
condition satisfied, and 2w−u ∈ block (k+1). So rule (R↓) of Proposition 37 gives

    2·B_W − A'  ⊆  B .                                            (★)

Now the dichotomy. Write δ for the density of Z in blocks k, k+1, so |A'| ≍ δ·3^k,
|B_W| ≍ δ·3^k and |B| ≍ 6δ·3^k. By (★),

    |2·B_W − A'|  ≤  |B|  ≍  6δ·3^k  ≍  6·max(|A'|, |B_W|),

i.e. **the sumset 2·B_W − A' has bounded doubling relative to its summands**. Two cases:

- If A' and B_W behave generically, |2·B_W − A'| ≍ min(|A'|·|B_W|, |window|), which
  exceeds 6δ·3^k as soon as δ·3^k is large — contradiction unless δ → 1. This is the
  blow-up the numerics of Proposition 38 exhibit.
- Otherwise the bounded-doubling hypothesis of the Freiman–Ruzsa inverse theory is met, and
  A', B_W are each contained in arithmetic progressions of length O(max(|A'|,|B_W|)). In
  ℤ the sharp tool is Freiman's 3k−4 theorem (for distinct summands, in the Lev–Smeliansky
  / Stanchescu form): small doubling forces containment in a short AP.

So either the density tends to 1, or Z is AP-structured inside every block. In the second
case the cross-block coupling (★) ties the block-wise progressions together — if that
forces a single global progression, Z is a union of residue classes and **Corollary 30
applies**, producing a tame progression. Either way Conjecture R21-C at T = 1 follows.

**What remains to be done, stated honestly.** (i) The generic case needs a quantitative
lower bound on |2·B_W − A'| that does not assume genericity — i.e. one must actually invoke
the inverse theorem rather than wave at it. (ii) The structured case needs the cross-block
step: block-wise APs, coupled by (★) across all k, must be shown to have a common
difference (or to differ from one by a density-zero set, which is enough for Corollary 30).
(iii) All constants above are stated up to ≍ and must be made explicit; the windows were
chosen for convenience, not optimality. (iv) This is still only T = 1.

Discipline note: the hypotheses of any inverse theorem invoked here must be verified
exactly, not by analogy — this project's audit checklist flags precisely this failure mode,
and an earlier route in this run was caught claiming an infinite progression from a density
hypothesis, which is false. Freiman-type conclusions give containment in a FINITE
progression of controlled length, never an infinite one.

## Correction and verification of Proposition 39's windows

The windows quoted in Proposition 39 were stated loosely; the exact ones, derived and then
machine-verified, are as follows. For the (1,0) rule applied to the 4-AP (x, u, w, 2w−u)
with d = w−u and x = 2u−w, one needs simultaneously

    x ≥ 1                      ⟺  w < 2u,
    j(w) = j(u) + 1  and  j(2w−u) = j(w),
    step 1 increasing          ⟸  j(u) − j(x) ≥ 1  ⟺  2u − w < 3^k    (i.e. w > 2u − 3^k)

(the case j(u) = j(x) imposes no constraint at all, since with t(u) = 0 step 1 cannot
increase). Writing P = 3^k, these give

    u ∈ [2.25·P, 2.75·P)      and      w ∈ ( 2u − P,  4.5·P ),

both inside blocks k and k+1 respectively, with 2w−u ∈ block k+1. Taking
u ∈ [2.25·P, 2.5·P) yields the common window W = (4P, 4.5P) of size P/2, so with
A' := Z ∩ [2.25P, 2.5P) and B_W := Z ∩ W the inclusion (★) 2·B_W − A' ⊆ Z ∩ block(k+1)
holds as stated, and |2·B_W − A'| ≥ |B_W| + |A'| − 1.

Machine verification (exact integer arithmetic, k = 4…8): the constraints above are met by
a genuine two-dimensional family — 1 640, 14 883, 132 860, 1 196 835 and 10 761 680 valid
(u,w) pairs at k = 4,…,8, roughly a third of the candidate rectangle, with the w-range
scaling as predicted (at k = 8, w ranges over [22 964, 29 523] inside block 9 =
[19 683, 59 049)). So the rule is not vacuous on the family Proposition 39 uses.

This corrects the loose windows in Proposition 39; its dichotomy and its four stated
obligations are unchanged.

## Proposition 40 (the closure mechanism is not special to binary delays) — verified

Proposition 37(c) exhibited, for t ∈ {0,1}, a closure property of the zero set. It
generalizes to arbitrary finite-valued delays, which means the route of Propositions 38–39
is not confined to T = 1.

**Statement.** Let c = j + t satisfy condition (ii), t : ℕ → ℤ≥0 finite-valued. For every
level ℓ write L_ℓ := {v : t(v) ≤ ℓ}. Then for every far-left triple (u₁, u₂, u₃) with
u₂−u₁ = u₃−u₂ and block pattern (k, k+1, k+1):

    u₁ ∈ L_ℓ  and  t(u₂) = ℓ    ⟹    u₃ = 2u₂ − u₁ ∈ L_ℓ .

**Proof.** Lemma 35 for this pattern gives t(u₁) ≤ t(u₂) ⟹ t(u₃) ≤ t(u₂). Take ℓ = t(u₂):
the hypothesis u₁ ∈ L_ℓ is t(u₁) ≤ ℓ = t(u₂), so the conclusion is t(u₃) ≤ ℓ. ∎

So **every sublevel set is closed under completing an arithmetic progression by one step**,
provided the middle term sits exactly at that level. For t ∈ {0,1} and ℓ = 0 this is
exactly rule (R↓) of Proposition 37, so the binary case is the ℓ = 0 instance of a general
phenomenon.

Verification (exact, values to 12 000, b = 3): the closure fires 4 107 / 5 862 / 7 051 times
with ZERO violations for t = v₂(v), t = 1_odd and t ≡ 0 — all of which satisfy (ii). It is
violated 1 179 times by t(v) = ⌊v₂(v)/2⌋, which is only weakly (not strictly) increasing in
the valuation and therefore is not AP-alternating, so does not satisfy (ii): the test has
teeth in both directions.

**Consequence for the programme.** The dichotomy of Propositions 38–39 — either the
sublevel set densifies (via sumset growth) or it is Freiman-structured, and structure feeds
Corollary 30 — now applies level by level to an arbitrary finite-valued delay, not just to
a binary one. The obligations listed in Proposition 39 are unchanged and remain open; what
this adds is that discharging them would settle Conjecture R21-C in general rather than in
the first case only.

## Correction to Proposition 38 (Case 2 is NOT supported — fourth self-correction of this run)

Proposition 38's Case 2 asserted that if the zero set meets every progression infinitely
often then the closure forces its density to tend to 1. The evidence I gave for it came
from closing RANDOM seeds, which does blow up. That was the wrong experiment: the object
we care about is a set that is ALREADY closed and consistent with all the constraints, not
the closure of an arbitrary seed. Residue classes are the obvious counterexample to the
naive reading — they are closed and have density 1/m — and the solver finds much better
ones.

**What the direct test shows.** Solving the full T = 1 system (condition (ii) in full, a
positive descent rate along every progression of step ≤ 4, no level set periodic mod m ≤ 6)
gives SAT at N = 150, 200, 260, 340, 440 with zero-set densities 0.260, 0.265, 0.519,
0.553, 0.534 — climbing at first and then PLATEAUING near 0.55, not tending to 1. Every
model was re-verified against the literal definition of (ii).

**And the solutions are not structured either.** Measuring the best agreement of the
N = 340 solution with any union of residue classes: 63.2% (mod 19), 60.9% (mod 23), 60.0%
(mod 22), and below 60% for all other moduli up to 24. A structured set would score near
100%. So this zero set is genuinely aperiodic.

**Consequence.** At N = 340 the solver exhibits a zero set that escapes BOTH branches of the
Proposition 39 dichotomy — it neither densifies toward 1 nor sits close to a union of
residue classes. That does not refute Proposition 39, which is an asymptotic statement and
whose Freiman branch concerns bounded doubling rather than exact periodicity; but it
removes the empirical support for Case 2 as I stated it, and it means the dichotomy is not
visible at reachable sizes. Anyone continuing this line should treat "the closure densifies"
as unsupported, and should note that the T = 1 case now looks at least as promising as a
REFUTATION route for Conjecture R21-C as it does as a proof route.

Propositions 37, 40 and Lemmas 34, 35 are unaffected — they are proved statements about the
constraint structure, verified two-sidedly. What is withdrawn is the heuristic in
Proposition 38 Case 2 and the confidence it lent to Proposition 39's first branch.

Running tally of self-corrections in this run: the meaning of linear-profile extinction
(Remark 17), the claim that block layouts were dead (correction to Remark 22), the
vacuity of Theorem 16(c) (self-audit), the degenerate objective and dropped clauses
(Remarks 31, 36), and now this. Every one had the same root cause: reading finite or
partial evidence as if it settled an asymptotic statement.

## Proposition 41 (condition (ii) is necessary but far from sufficient) — verified

Condition (ii) constrains only the CLASS sequence. Values sharing a class are ordered
freely, and those free orders must themselves avoid monotone 4-APs. So a delay satisfying
(ii) need not yield any 4-AP-free permutation at all.

This is not a theoretical caveat — it is what happens. Taking the aperiodic delays produced
by the T = 1 solver (which satisfy full condition (ii), have a positive descent rate along
every progression of step ≤ 4, and are genuinely aperiodic — best agreement with any union
of residue classes 63%), and asking SAT whether ANY choice of within-class orders realizes
them as a monotone-4-AP-free permutation:

    N = 150 : UNSAT      N = 260 : UNSAT      N = 340 : UNSAT

— impossibility over ALL within-class orders, the same logical shape as route R1's stage
certificates (experiments/classreal.py, lazy-transitivity CEGAR, engine validated in
profile_cegar.py).

**Consequences.**
1. The escaping solutions of the correction to Proposition 38 do NOT threaten Erdős 196:
   they satisfy the necessary condition and fail the sufficient one. My worry that they
   might constitute a counterexample lead was misplaced in that respect.
2. Conjecture R21-C, as stated, is about condition (ii) alone — so those solutions may
   still refute IT while being irrelevant to 196. The conjecture is therefore weaker than
   the question one actually cares about, and the sharper target is: **is there a binary
   delay t AND a choice of within-class orders giving a monotone-4-AP-free permutation, at
   every N?** Equivalently (clean reformulation, since the architecture's permutations are
   exactly the linear extensions of c): is there a monotone-4-AP-free permutation of [1..N]
   together with a binary t making c = j + t non-decreasing along its position order?
3. That reformulation is what experiments/t01_realize2.py tests, jointly over the delay and
   the orders. Reference points: t ≡ 0 is the contiguous ratio-b block layout, dead by
   routes R1/R3; the valuation delays are the CLS families, with CLS(3,a) dead at N = 250
   (route R20). An UNSAT at moderate N would be an impossibility theorem for the entire
   binary-delay architecture family, quantified over all delays and all within-class orders.

## Remark 42 (scoping: how much the T = 1 case can possibly matter)

An honest limit on the value of the T = 1 work above. With t ∈ {0,1} the class of a value
is either j(v) or j(v)+1, and classes are emitted in increasing order — so the architecture
is exactly a contiguous block layout in which each value may be delayed by AT MOST ONE
phase. That is a bounded-lag layout, and route R1 already established that bounded-lag
interleavings die (its lag-2 pattern dies at stage 7, with debt propagating backwards as
decreasing-AP pressure), while the zero-delay case is the plain in-order block layout, dead
at ratios 3 and 4 for every gadget.

So whichever way experiments/t01_realize2.py resolves, the consequence for Erdős 196 is
limited: an UNSAT would be a clean impossibility theorem for a family already believed dead
on independent grounds, and a SAT persisting to large N would be surprising but would sit
inside the Remark 27 blind spot.

**Where the real question lives.** The negative branch needs UNBOUNDED delay — the growing
debt that R20's CLS families and R1's accelerating corridor both exhibit — and by Remark 27
no finite search can settle designs in that regime. So the genuinely open negative-branch
question requires an explicit rule together with a proof, not a search. The propositions
that survive from this stretch and DO apply there are the general ones: Lemma 34 (far-left
reduction), Lemma 35 (the delay cannot rise twice in a row), Proposition 40 (every sublevel
set is closed under AP-completion, for arbitrary finite-valued delays), and Proposition 41
(condition (ii) is necessary, not sufficient — the realizability layer is a separate and
apparently severe constraint).

This remark is recorded so that the effort spent on T = 1 is not mistaken, later, for
progress on the problem itself.

## Lemma 43 (record positions are controlled by the previous record's value)

Let a be ANY permutation of ℕ and let w₁ < w₂ < ⋯ be its value-records (running maxima).
Then for every i:

    pos(w_{i+1})  ≤  w_i + 1.

Proof. Every position strictly before pos(w_{i+1}) holds a value that is not a record
larger than w_i, hence is ≤ w_i (the running maximum equals w_i throughout that stretch).
Those values are distinct, so there are at most w_i of them: pos(w_{i+1}) − 1 ≤ w_i. ∎

Verified on ALL 408 240 permutations of [1..7], [1..8], [1..9] (740 988 record pairs, zero
violations).

**Combined with Lemma 13(a).** In a monotone-4-AP-free permutation the record set is
additionally 3-AP-FREE, hence sparse: |Λ ∩ [1..N]| ≤ r₃(N) = N·exp(−c(log N)^{1/9}). So a
counterexample must have records that are simultaneously
  (i) sparse in value (a Roth/Behrend-type set),
  (ii) positioned very early — the (i+1)-st record sits at position at most w_i + 1, which
      for a sparse record set is far below w_{i+1}, and
  (iii) increasing in both value and position, with pos(w) ≤ w throughout (Lemma 11).
(Re-verified here: zero record 3-APs with extension room across all 168 864 avoiders of
[1..9].)

This is recorded as a clean constraint on any counterexample. It is NOT by itself a
contradiction: sparse record sets satisfying all three conditions are easy to write down
(e.g. w_i growing geometrically), so the tension has to come from coupling these with the
placement of the non-record values, which is where every affirmative-side attempt in this
run has stalled.

## Theorem 44 (CO-SUPPLY IS REFUTED — the Theorem 16 chain programme is dead)

Route R17's result, re-derived and checked here. **Every value-record is closed.**

Proof. If u is open at scale d then Theorem 16(a) gives pos(u+d) < pos(u); since u+d > u,
a value larger than u precedes u, so u is not a record. Contrapositive: every record is
closed (has no increasing 3-AP ending at it). ∎

Since the record set Λ is infinite (Lemma 11), a 4-AP-free permutation has infinitely many
closed values. So the co-supply statement — "all but finitely many values are open" — is
FALSE, not merely unproved. Machine check: 0 violations across all 195 154 avoiders with
N ≤ 9 (apparent violations are board-edge artifacts with u+d > N, separated and counted).

**Consequences, stated bluntly.**
1. The programme announced with Theorem 16 — prove co-supply, get an infinite forcing
   chain, contradict order type ω — cannot work. Any proof of co-supply must break at Λ.
2. **Every propagation-style weakening is refuted as a family** (R17's Thm R17.2): in ANY
   digraph whose edges descend in position, closures are finite and acyclic, so every
   maximal chain terminates at a sink; hence an open value whose forced successor is closed
   always exists. Universally quantified "openness propagates" statements are therefore all
   false. Measured: 40–67% of Theorem 16's forcing edges land on a closed value (84%
   exhaustively at N = 9). Only existential-selection forms survive, and those are
   literally equivalent to 196-YES.
3. **The quantitative reading of Theorem 16(b) was mis-calibrated — my error.** I wrote that
   "any unbounded lower bound on |Cl(u)| resolves 196-YES". That is wrong: |Cl(u)| ≥ f(u)
   only gives pos(u) ≥ f(u), which is a contradiction iff #{u : f(u) ≤ P} < P for some P
   (so f(u) ≥ u+1 eventually suffices, while f(u) = log u or even f(u) = u prove nothing).
   And for Theorem 16's own digraph no admissible f exists at all, since |Cl(w)| = 1 at
   every record.

What survives: Theorem 16(a) and (b) remain true and are still the correct local forcing
rule and closure bound. What is withdrawn is the programme built on them.

**Net positive from R17.** A six-rule forced-descent digraph G* that removes the record
obstruction: sinks drop from 40–65% to 1–3%, immediate-death edges from 40–67% to 2–9%,
and the longest chain grows from 14 to 132 at N = 320. Also an ω-free explicit chain
construction quantifying route R5's barrier: one anchor buys at most log₂ m steps, and the
adversary holds it to 2–3 steps regardless of N.

## Theorem 45 (Theorem 16 says NOTHING about block architectures — route R18)

In any MONOTONE-4-AP-FREE layered permutation (value-intervals listed in increasing order,
arbitrary order inside each), every forcing edge stays inside a single block: u ⟶ u+d has u+d > u, and
Theorem 16(a) forces pos(u+d) < pos(u), so u+d cannot be in a later block. Hence
Cl(u) ⊆ B(u) automatically and |Cl(u)| ≤ |B(u)| for free.

So "make forcing chains terminate" imposes ZERO constraint on the entire block-architecture
family — it is satisfied by every block construction ever tried, including all the dead
ones. The bounded-closure design mission I commissioned was therefore vacuous, and route
R18 proved it (its Prop R18.1: the parity permutation σ_N has no monotone 3-AP at all,
hence no open value, hence trivial closures at every N — so "all closures ≤ B" is SAT at
every N for every B ≥ 1). Its UNSAT direction would not have been a YES theorem either
(Prop R18.3).

**Hypothesis correction (route R18's auditor, accepted).** The statement needs
4-AP-freeness: the proof invokes Theorem 16(a), which is available only for 4-AP-free
permutations. Without it the claim is false — the identity permutation of [1..9], layered
for cuts (1,4,10), has value 3 open at scale 1 and hence a forcing edge 3 → 4 crossing a
block boundary. The conclusion is unaffected for our purposes, since every candidate
counterexample is 4-AP-free by definition.

Net positive from R18: an exact block decomposition of 4-AP-freeness read off the forcing
relation, deciding layered architectures 2–3 orders of magnitude faster than global SAT and
localizing each death to a single block; two new finite theorems (geometric cuts at ratios
3 and 4 are dead); and a reduction of "parity inside blocks" to 2-SAT, dead for every ratio.

## Theorem 46 (the ledger ceiling is exactly 2 — route R19)

Route R19 reduced Theorem 12's ledger to an exact identity and computed its ceiling. For
the triadic permutation T and N = 3^{K+1}−1, Σ_j τ_j(T) = (3/4)N² + N/2 exactly (verified
K = 2…9), giving C_ledger(N) ≤ 2(N+1)/(N+2) < 2 for every N. Therefore:

**No unweighted-ledger argument can prove LP-inc(C) for any C ≥ 2.**

Moreover Theorem 16's forcing step coincides with the i = 2 case of Theorem 12's demand
disjunction, and closure bounds give LOWER bounds on positions whereas the ledger's content
is an upper bound.

**Scope correction (route R19's auditor, accepted).** R19 stated "closures do not help the
ledger" as a theorem; the auditor downgraded it to a remark, and I follow that here — it is
a well-supported observation about the two mechanisms, not a proved impossibility. The
auditor also found two gaps in the "exact ceiling" computation (floor/ceiling handling, and
that the quantity computed is not the ceiling of profile-only reasoning — a strictly better
constant follows from R19's own data). The headline that no UNWEIGHTED-ledger argument
reaches C ≥ 2 rests on the exact triadic evaluation and survives; the word "exact" should
not be attached to the general-N ceiling formula.

## Theorem 47 (the forced-descent method cannot work — a one-line barrier for the whole family)

Route R17's six rules are exactly the unit propagations of the two 3-literal clauses that a
single 4-AP contributes. Writing s for the source and l_i = [x+(i−1)d ≺ x+id]:

    (U1) s−2d ≺ s−d ≺ s              ⟹ s+d ≺ s
    (U2) s+d ≺ s+2d ≺ s+3d           ⟹ s+d ≺ s
    (U3) s−d ≺ s  and  s+d ≺ s+2d    ⟹ s+d ≺ s
    (D1) s+2d ≺ s+d ≺ s              ⟹ s−d ≺ s
    (D2) s−d ≺ s−2d ≺ s−3d           ⟹ s−d ≺ s
    (D3) s−d ≺ s−2d  and  s+d ≺ s    ⟹ s−d ≺ s

(U1 is Theorem 16(a).) Independently verified here: on all 168 864 monotone-4-AP-free
permutations of [1..9], every edge produced by these rules descends in position — zero
violations.

**Barrier.** Every one of these rules, and indeed every rule of the shape "such-and-such
positional facts force t ≺ s", produces an edge that DESCENDS in position. Consequently:

1. Chains descend in position, so from any u a chain has length at most pos(u) — finite.
2. The ≺-minimum z = a(1) has NO out-edge under ANY such rule, since every conclusion is of
   the form "t ≺ s" and nothing precedes z. **z is always a sink.** (Verified: a(1) is a
   sink on every one of the 168 864 boards; sink counts per board range over 2–7.)

So no forced-descent digraph — G, G*, or any extension by further rules of this shape — can
prove 196-YES via "some value has an infinite closure". Chains always terminate, and they
terminate at sinks that provably exist. This subsumes Theorem 44 (which showed records are
sinks for the U-rules) and route R17's Thm R17.2 (which showed propagation statements fail
as a family): the obstruction is not about records or about which rules one adds, it is that
descent in a well-founded order is finite and the minimum is always a sink.

**What this closes.** The entire "local forcing ⟹ infinite chain ⟹ contradiction with order
type ω" strategy, which this run pursued under Theorem 16 and which route R17 extended to
G*. Its measured improvements are real but irrelevant to the goal: G* reduces sinks from
40–65% to 1–3% and lengthens the longest chain from 14 to 132 at N = 320, yet 1–3% of sinks
is as fatal as 65% — one sink per chain suffices, and z is always one.

**What is still worth taking from it.** The six rules are a complete and correct local
propagation system for 4-AP-freeness. They are the right engine for SEARCH (route R18 used
the same locality to get a 2–3 order-of-magnitude speedup on layered architectures, and to
localize each death to a single block), and they give sharp finite structure. They are
simply not a route to the affirmative branch.

## Corollary 48 (class-records have density zero at EVERY modulus)

Let a be a monotone-4-AP-free permutation of ℕ. For q ≥ 1 define

    S_q := { v : no value v + kq (k ≥ 1) precedes v }
         = the values not overtaken inside their own residue class mod q.

Then S_q has density 0 for every fixed q. Indeed S_q ∩ P_{q,r} is exactly the record set of
a restricted to the progression P_{q,r} = {r, r+q, r+2q, …}, which by Lemma 24 is 3-AP-free;
Roth's theorem gives |S_q ∩ P_{q,r} ∩ [1..N]| = o(N/q), and summing the q classes gives
|S_q ∩ [1..N]| = o(N). With the Kelley–Meka/Bloom–Sisask bound this is quantitative:
|S_q ∩ [1..N]| ≤ q·r₃(N/q) ≤ N·exp(−c(log(N/q))^{1/9}).

So: **for every fixed modulus q, almost every value is overtaken by a larger value in its
own residue class mod q.** For q = 1 this is the (already known) density-0 statement for
records; the content is that it holds simultaneously at every modulus, which is the
sharpest form of the "coupled family" of Lemma 24 obtained so far.

**Honest assessment — this does NOT give a contradiction, and I checked why.** Converting
it into a lower bound on the inversion count I of the restriction σ_N: each (v, q) with
v ∉ S_q supplies an inverted pair (v, w) with q | (w−v), and a single pair serves at most
d(w−v) ≤ N^{o(1)} moduli, so summing over q ≤ N/K gives

    I ≥ N² · exp(−O(log N / log log N)) = N^{2−o(1)}.

That is WEAKER than what Theorem 12's demand count already gives (I ≥ N²/18 − O(N), a
constant fraction), because the divisor factor costs more than the density saving buys. So
the multi-modulus structure, in this counting form, is not a route to the affirmative
branch. Recorded both because the structural statement is worth having and because the
natural counting use of it is now closed — anyone tempted by "sum over all moduli" should
know the divisor loss kills it.

## Proposition 49 (avoiders are overwhelmingly INDECOMPOSABLE — a scope correction to the block programme)

Call V a *cut point* of a permutation if the values [1..V] occupy exactly the positions
[1..V] (equivalently the running maximum equals the index at V); a permutation with
infinitely many cut points is precisely a block layout with those cuts. Measured:

- **Exhaustively over all 168 864 monotone-4-AP-free permutations of [1..9]:** 78.9% have
  ZERO proper cut points, 17.8% have one, 2.9% have two, 0.3% have three, 0.02% have four.
- **The parity construction σ_N** — the standard avoider, existing at every N — has cut
  points only at 1, N−1 and N, for every N tested (8, 16, 32, 64, 128, 256). It is
  essentially indecomposable.
- **Solver-found avoiders at scale have no proper cut point at all:** at N = 200, 300, 400
  the only cut is the trivial one at N.

**Why this matters, and what it corrects.** Route R1's programme — and the impossibility
results built on it (REQUIREMENTS B4, and the cut-set {8, 26, 80}, the window law, the
accelerating-cut corridor) — is a statement about permutations WITH an infinite cut
sequence. The data says avoiders overwhelmingly have no proper cuts at all, and the
proportion with several decays sharply. So those theorems, while genuine, constrain a thin
subfamily, and "block layouts are dead" is much weaker evidence against the negative branch
than the accumulated weight of that work suggests. The natural home of a counterexample is
the INDECOMPOSABLE permutations, which the cut-based results do not touch.

**A distinction that must be kept.** This scope limitation applies to the cut-sequence work
(R1, and REQUIREMENTS B4's ratio-3/4 statements). It does NOT apply to the class-architecture
results (Propositions 29, 30, 40, 41): there the fibres F_j need not be intervals, so
emitting classes in increasing index order does NOT make the permutation a block layout, and
those propositions constrain a genuinely wider family. Likewise the digit-comparator
dichotomy (REQUIREMENTS B2) and the length-5 pair-counting obstruction (B5) are not
cut-based.

**Consequence for the portfolio.** The negative branch is less constrained than this run's
own summary implied. The right target is an indecomposable permutation of ℕ, and the tools
that still bite on it are the class-architecture propositions and the displacement bounds —
not the cut certificates. REQUIREMENTS.md B4 should be read with this scope attached.
