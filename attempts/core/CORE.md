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

## Remark 17 (STRATEGIC: linear-profile extinction cannot decide 196)

Certified extinction data for the plain target (no monotone 4-AP, both orientations)
under pos(v) ≤ ⌊C·v⌋ — the minimal N with no such permutation of [1..N]:

    C     = 1.25   1.5    1.75   2.0
    N*(C) =    4     15      31    90

The C = 1.5 and C = 1.75 entries were obtained twice by unrelated methods (route R9's
exhaustive enumeration of the extension tree and this session's SAT), and C = 2.0 by
lazy-transitivity CEGAR (experiments/profile_cegar.py) with an independent eager
two-solver re-verification (experiments/verify_c2_n90.out). Growth is roughly
N*(C) ≈ 4·exp(4.15 (C − 1.25)), so C = 3 would first die near N ≈ 6·10³ and C = 5 far
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

From the certified extinction law N*(C) ≈ 4·exp(4.15(C − 1.25)) (Remark 17), a design
whose AP-restriction has linear displacement with constant C cannot die before roughly

    C = 3 : N ≈ 6·10³      C = 5 : N ≈ 10⁷      C = 6 : N ≈ 10⁹

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
