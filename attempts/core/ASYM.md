# ASYM.md — the asymmetric strategy (no dec-3AP + no inc-4AP) : structure theory

Target studied: a permutation of ℕ with NO monotone decreasing 3-AP and NO monotone
increasing 4-AP. Any such permutation is a full NO-witness for 196 (a decreasing
monotone 4-AP contains a decreasing monotone 3-AP). This is a STRICTLY stronger
avoidance than 196 needs; it is studied because its combinatorics is cleaner.
Status: OPEN whether such a permutation of ℕ exists. Finite boards: witnesses exist for
all N ≤ 27 so far (experiments/asym_exhaust.py, exhaustive), with exploding search cost.

Fix such a hypothetical permutation, ≺ the induced order (type ω, Lemma 1 of CORE.md).
Define the drop indicator D(u, e) := [ u + e ≺ u ] for u, e ≥ 1.

## Proposition A1 (word constraints: Fibonacci-type descent words at every scale)

For every u, e ≥ 1:
  (no-11)   ¬( D(u, e) ∧ D(u+e, e) )                      [else dec-3AP (u, u+e, u+2e)]
  (no-000)  D(u, e) ∨ D(u+e, e) ∨ D(u+2e, e)              [else inc-4AP (u, …, u+3e)]
Hence along EVERY arithmetic progression u, u+e, u+2e, … the binary word
k ↦ D(u+ke, e) has no factor 11 and no factor 000; its 1-density lies in [1/3, 1/2].
Moreover D is order-coherent (transitivity): D(u,e₁) ∧ D(u+e₁,e₂) ⟹ D(u,e₁+e₂), and
¬D(u,e₁) ∧ ¬D(u+e₁,e₂) ⟹ ¬D(u,e₁+e₂).

Proof. (no-11): D(u,e) ∧ D(u+e,e) means pos(u) > pos(u+e) > pos(u+2e): the values
u+2e, u+e, u read at increasing positions decrease in AP — a monotone decreasing 3-AP.
(no-000): ¬D at (u,e),(u+e,e),(u+2e,e) means pos(u) < pos(u+e) < pos(u+2e) < pos(u+3e):
increasing 4-AP. Word/density: a word with no 11 has 1-density ≤ 1/2; with no 000,
every window of 3 has a 1, so density ≥ 1/3. Transitivity: from the linear order. ∎

Side remark (single-scale realization is impossible): if pos were induced by
f(u) = {uθ} (circle rotation), the descent word at step e is Sturmian with density
{eθ}; the constraints would need {eθ} ∈ [1/3, 1/2] for every e ≥ 1 — impossible
(rational θ hits 0; irrational θ equidistributes). Any realization must be genuinely
multi-scale.

## Proposition A2 (leader structure)

Call w a *leader* if D(w, e) = 0 for all e ≥ 1 (w ≺ w + e for every e: w is placed
before every larger value). Let Λ be the set of leaders. Then:
 (a) The ≺-minimum z = a(1) is a leader.
 (b) Value order and ≺ agree on Λ (leaders form an increasing subsequence).
 (c) Λ contains no 4-term AP; hence (Szemerédi, 4-AP case) Λ has upper density 0.
 (d) Λ is infinite — indeed unbounded; and every non-leader u admits a finite
     "drop-chain" u ≻ u+e₁ ≻ u+e₁+e₂ ≻ ⋯ ≻ w ending at a leader w with w > u and
     w ≺ u.

Proof. (a) z ≺ everything, in particular z ≺ z+e. (b) For leaders w < w', apply
leadership of w with e = w' − w. (c) If leaders w, w+d, w+2d, w+3d all lie in Λ, they
appear in increasing ≺ order by (b) — an increasing monotone 4-AP. Szemerédi's theorem
(every subset of ℕ of positive upper density contains a 4-term AP) gives density 0.
(d) Every non-leader u has some drop D(u, e); iterate at u+e: any maximal drop-chain
is strictly ≺-decreasing, hence finite (order type ω forbids infinite descending
chains), and its terminal element has no drops: a leader. Chain values strictly
increase, so the terminal leader w satisfies w > u; ≺-decrease gives w ≺ u.
Unboundedness of Λ: for any u there are non-leaders u' > u (if all values > u were
leaders, Λ would contain 4-APs, contradicting (c); note any infinite interval-tail
contains 4-APs), and the terminal leader of a chain from u' exceeds u' > u. ∎

## Consequences / reading

- Any asymmetric witness is built on an infinite density-0 "spine" Λ placed in
  increasing order, with all other values hung ≺-above chains leading down to the
  spine, while EVERY arithmetic progression at EVERY scale carries a no-11/no-000
  descent word. The construction problem recurses at all scales (the no-000 constraint
  inside long leader-free stretches reproduces the original difficulty).
- If finite boards ever go EXTINCT (asym_exhaust.py), the asymmetric route is dead
  finitely, and every 196-NO-witness must contain monotone decreasing 3-APs (in fact
  infinitely many, by applying the extinct statement to value-translates/tails).
- Conversely, surviving finite witnesses at growing N should be mined for the spine
  structure predicted by A2 (which values act as leaders?).

Machine checks: experiments/asym_strategy.py (definition-level checker, exhaustive
counts N ≤ 10: 5, 16, 51, 196, 689, 2936, 11691, 45875), experiments/asym_exhaust.py
(exhaustive existence, N ≤ 27 all EXISTS so far).
