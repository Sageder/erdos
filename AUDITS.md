# AUDITS.md — adversarial audit reports for Erdős 196

One entry per candidate argument, verdict first. Checklist per PROMPT §7 (12 items), every audit.

(none yet)

## Audit: CORE.md + ASYM.md, fresh-context pass (2026-07-28)

Adversarial audit of all numbered items in attempts/core/CORE.md and attempts/core/ASYM.md
against PROBLEM.md conventions. Machine hunts: scratchpad audit_hunt.py (exhaustive finite
shadows, exact Fraction arithmetic, trusted checker experiments/apcheck.py), plus re-runs of
experiments/apcheck.py, experiments/core_checks.py, and an independent cross-validated DFS
recount of the ASYM witness counts (N=3..10: 5, 16, 51, 196, 689, 2936, 11691, 45875 — all
match ASYM.md's claimed list).

### Verdict summary

| Item | Verdict |
|---|---|
| Lemma 1 (order-type) | SOUND |
| Lemma 2 (3-AP forcing) | SOUND |
| Lemma 3 (normalization) | SOUND |
| Lemma 4 (anchored disjunction) | SOUND |
| Lemma 5 (linear displacement) | SOUND |
| Lemma 6 (displacement compactness) | SOUND |
| Lemma 7 (FIN(K) criterion) | SOUND |
| Lemma 8 (interval characterization) | SOUND (machine-verified exhaustively) |
| Lemma 9 (slot relaxation) | SOUND |
| Lemma 10 (stuckness = X-config) | SOUND (machine-verified exhaustively) |
| Lemma 11 (universal two-spine structure) | SOUND (one harmless wording nit) |
| Theorem 12 (LP(9/8)) | REPAIRABLE GAP — the "Consequently ... limsup" clause; main statement + finite form SOUND |
| Lemma 13 (spines 3-AP-free) | (a) SOUND; (b) REPAIRABLE GAP — strict "g2 > 2g1" unproven at e = g1; must be weakened to "g2 >= 2g1" |
| Prop A1 (word constraints) | SOUND (same wording nit) |
| Prop A2 (leader structure) | SOUND |

No circularity found anywhere (nothing assumes 196 or an equivalent). All Szemerédi/König
uses have hypotheses verified. Conventions (N starts at 1, values-vs-positions, both
orientations) respected except at the two flagged points.

### Non-SOUND items in detail

#### Theorem 12 — REPAIRABLE GAP in the "Consequently" clause (sup vs limsup)

What is proven: for each C < 9/8, every permutation with pos(v) <= C·v for ALL v has an
increasing 4-AP. Contrapositive: an inc-4AP-free permutation has, for every C < 9/8, SOME v
with pos(v) > Cv — i.e. sup_v pos(v)/v >= 9/8. That is weaker than the claimed
limsup_{v->inf} pos(v)/v >= 9/8: a permutation with finitely many exceptional values (say
pos(1) = 100, pos(v) <= 1.01 v for v >= 2) already defeats "pos(v) <= Cv for all v" for
every C < 9/8 without constraining the tail, so the theorem-as-stated does not apply to it
and the limsup deduction as written is a quantifier slip.

Repair (small and verified): additive-slack ledger. If pos_a(v) <= Cv for all v >= V0, set
Q := max_{v < V0} pos_a(v); then pos_a(v) <= Cv + Q for ALL v, hence pos_{sigma_N}(v) <=
Cv + Q. The supply step becomes pos(w) <= C(w - e*(w)) + Q; summing gives
Sum e*(w) <= (1 - 1/C)·N(N+1)/2 + NQ/C. The demand side is unchanged (N^2/18 - O(N)), so the
N -> inf limit still forces C >= 9/8; contradiction for C < 9/8, giving genuinely infinitely
many v with pos(v) > Cv for every C < 9/8, i.e. limsup >= 9/8. Machine check: C = 11/10 with
slack Q = 50 still fails at N = 4522 (exact fractions).

Everything else in Theorem 12 checks out line by line:
- e*(w) = 0 case: pos(w) <= Cw = C(w - 0) uses the hypothesis directly. OK.
- Summation identity Sum pos = N(N+1)/2 is applied only to sigma_N, a genuine permutation of
  [1..N] (never to a non-surjective slot map). OK.
- Demand disjointness: each u in [1..N-3e] yields an e-dropping w in {u+e, u+2e, u+3e}; the
  fiber of each w has size <= 3 (u in {w-e, w-2e, w-3e}), so #{w with e-drop} >= (N-3e)/3.
  Layer cake Sum_w e*(w) = Sum_e #{w : e*(w) >= e} is an exact identity; dropping e >
  floor((N-1)/3) only weakens the lower bound; all kept terms are positive. OK.
- Final limit: Sum_{e<=E} (N-3e)/3 = NE/3 - E(E+1)/2 = N^2/18 - O(N), E = floor((N-1)/3);
  (1-1/C)/2 < 1/18 iff C < 9/8. Machine: finite form NEVER fails for C = 9/8 (N < 3000);
  first failure N = 22 at C = 11/10, N = 40 at C = 10/9, N = 43 at C = 89/80 — the failure
  frontier approaches infinity as C -> 9/8-, exactly as the theorem's shape requires.
- Infinite-from-finite via restriction: pos_{sigma_N}(v) <= pos_a(v) <= Cv, and an
  increasing 4-AP of sigma_N is one of a (relative order preserved). OK.
- Exhaustive verification of ledger inequality, demand count, layer-cake identity, and the
  finite form (with exact C = max_v pos(v)/v) on all 35847 inc-4AP-free permutations of
  [1..N], N <= 8: all PASS.

#### Lemma 13(b) — REPAIRABLE GAP: strict inequality overclaims the boundary case e = g1

The statement says every 3-AP (g1, g2, g3) in Gamma has g2 > 2g1, i.e. step e > g1. The
proof needs g0 := g1 - e >= 1 and therefore only excludes e < g1 (checklist item 6: this is
exactly a "v - d < 1" boundary failure; N starts at 1, so g0 = 0 is not a value). The case
e = g1 — a grounded 3-AP (g, 2g, 3g) — is NOT excluded by the proof, and cannot be excluded
by any local forcing: the downward extension is 0 (does not exist) and the upward extension
4g is not position-constrained by groundedness of 3g (groundedness of v constrains only
values BELOW v). Machine counterexamples to the finite shadow of the strict claim:
  perm (1,2,4,3) of [1..4] is monotone-4-AP-free with Gamma = {1,2,3}: grounded 3-AP
  (1,2,3) with e = g1 = 1, g2 = 2 = 2g1 exactly; likewise (1,4,2,3), (4,1,2,3),
  (1,2,4,3,5), and many more.
Repair: weaken to "every 3-AP in Gamma has g2 >= 2g1 (step e >= g1)"; equivalently, only
3-APs with step < first term are impossible. The displayed consequence SURVIVES the repair:
a 3-AP inside [M, 2M] has step e <= M/2 < M <= g1, i.e. e < g1, which the repaired lemma
still excludes; so "Gamma cap [M,2M] is 3-AP-free" and |Gamma cap [M,2M]| <= r3(2M) stand.
Note that remark (iii)'s own finite shadow ("grounded g1, g2, g3 with g1 - e >= 1") matches
the PROOF, not the stated strict inequality — the statement line is the slip.

Lemma 13(a) is SOUND, including the forced-extension step queried in the audit brief:
pos(w+3e) > pos(w+2e) is precisely the record property of w+2e applied with step e
(w+2e < w+3e and w+2e in Lambda means w+2e precedes every larger value; if w+3e were placed
BEFORE w+2e, then a larger value would precede w+2e and it would not be a record). The
ordering pos(w) < pos(w+e) < pos(w+2e) uses that w and w+e are records (order agreement,
Lemma 11(b)); existence of w+3e as a placed value uses surjectivity. Machine: exhaustive
N <= 9, no 4-AP-free permutation has records w, w+e, w+2e with w+3e <= N (60123 boundary
record-3APs with w+3e > N do occur, so the w+3e <= N proviso in the finite shadow is
necessary and correctly stated in remark (iii)).

### SOUND items — audit notes (selected checklist findings)

- Lemma 1: both constructions verified; downward-closure argument for the image of the rank
  map is complete (predecessor-max step and global-minimum existence both check); the
  "no infinite descending chain" consequence is correctly derived (all c_k, k >= 1, are
  predecessors of c_0). Mutual inverseness holds (r = pos).
- Lemma 2: the decreasing orientation at the anchored triples is genuinely impossible
  (z = a(1) is positionally first), so only z < z+d < z+2d needed excluding; the chain
  v_k = z + 2^k with d = 2^k gives v_{k+1} before v_k, an infinite descending chain. Uses
  surjectivity (z is the minimum of ALL of N; every z+d occurs) and order type omega. OK.
- Lemma 3: enumeration of S = {z, z+1, ...} in position order is a well-defined bijection
  N -> S (each element has finite positional rank in S); translation preserves APs in both
  orientations and subsequences preserve relative position order; b(1) = 1 because z is the
  global positional minimum and z is in S. The mid-proof ellipsis ("...") is prose slop but
  the completed argument that follows it is correct.
- Lemma 4: (**) correct; the key inequality chain v + j > j > E(v) shows none of
  v+j, v+2j, v+3j can precede v. The v = z, E = 0 boundary is handled. Finite shadows
  T1/T2 in core_checks.py are the right shadows and PASS (re-run). The caution paragraph's
  digraph claims (acyclicity via 2^{a+b} = 3^b having no nontrivial solution; ancestors of
  n bounded because 2^{a+b} must divide n·3^b, forcing a + b <= v2(n) + ...) check out and
  are machine-verified (T4). One remark-level nit: "extends to SOME type-omega linear
  order" is asserted, not proved, in the file; it is true (greedily place the
  smallest-index node whose ancestors are all placed; finite ancestor sets + the
  smallest-first rule imply every node is placed after finitely many steps) but a one-line
  proof belongs there if the remark is ever load-bearing. It currently is not.
- Lemma 5: cj > 2B gives the strict position increase; x arbitrary, j exists for every
  c > 0. Finite shadow T3 (B = 1, N = 10 exhaustive; B = 2 sampled) is the right shadow
  (N >= 1 + 3(2B+1) matches c = 1, j = 2B+1) and PASSES.
- Lemma 6: (=>) restriction bound pos_{sigma_N}(v) = #{w <= N : pos_a(w) <= pos_a(v)} <=
  pos_a(v) is right. (<=) Koenig argument fully checks: parent map well-defined
  (restriction of a phi-bounded 4-AP-free perm is phi-bounded — ranks only shrink — and
  4-AP-free); levels finite (injective maps into [1..min(phi(v),N)]); root exists (phi(1)
  >= 1 since phi maps into N starting at 1); limit order coherent (deleting values never
  swaps survivors; consistency along the branch by induction); order type omega genuinely
  preserved with proof — the UNIFORM pointwise bound #pred stage sets <= phi(v) - 1 for
  every N is exactly what survives the union, this is the load-bearing step and it is
  correct; 4-AP-freeness of the limit via any N >= max of the four values. This is the one
  compactness step in the two files and it is done right.
- Lemma 7: pigeonhole over C with fixed v* <= K, plus pos_{sigma_N}(v*) <= pos_a(v*),
  gives the contradiction; no hidden uniformity (N(C) may depend on C arbitrarily; K < N(C)
  not needed). The FIN(1)-false note verified: parity recursion sigma has sigma(1) = 1 and
  is 3-AP-free (machine-checked at N = 1..100, 257, 1000).
- Lemma 8: unique-largest-element grouping of monotone 4-APs is exhaustive and covers BOTH
  orientations (inc-step + later position = increasing 4-AP; dec-step + earlier position =
  decreasing 4-AP, largest value positionally FIRST — orientation bookkeeping correct);
  v <= 3 vacuous under min-empty = +inf, max-empty = 0. Machine: characterization ==
  4-AP-freeness for ALL permutations of [1..N], N <= 8, exhaustive. PASS.
- Lemma 9: (<=) is where the work is: injectivity of pos into N gives finite predecessor
  sets for free, Lemma 1 converts the slot order to a bijection b, and slot order = position
  order in b transfers the forbidden patterns to exactly the monotone 4-APs of b (both
  orientations, same grouping as Lemma 8). The Q-version correctly ADDS hypothesis (i)
  (finite lower sets), which was automatic over N — no hidden assumption. Surjectivity onto
  positions is genuinely free; onto VALUES is still required (domain of pos is all of N) —
  the "moral" paragraph states this accurately.
- Lemma 10: equality case correctly disposed of (pos injective; d1 != d2 because no d is
  both inc- and dec-step); empty-side cases (no inc-steps / no dec-steps) correctly give
  non-stuck under max-empty = -inf, min-empty = +inf (the convention switch from Lemma 8's
  max-empty = 0 is deliberate for the Q-setting and stated). Machine: stuckness <=>
  X-configuration for ALL prefix orderings of [1..m], m <= 7 (freeness of the prefix NOT
  assumed, matching the lemma's "any linear order"), exhaustive. PASS.
- Lemma 11: (a) drop/non-drop triple -> decreasing/increasing 4-AP orientation bookkeeping
  correct. (b) Lambda-infinite uses surjectivity of a (running max unbounded);
  Gamma-infinite uses surjectivity of pos; order agreement on Lambda uses the record
  property of the SMALLER record (correct); pos(w) <= w and pos(g) >= g are clean counting.
  Machine: all claims verified on every 4-AP-free permutation of [1..N], N <= 9. PASS.
  Wording nit (harmless): "its 1-density lies in [1/3, 2/3]" — the density need not exist;
  the window argument proves every limit point of frequencies (hence lower and upper
  density) lies in [1/3, 2/3]. Same nit in A1 with [1/3, 1/2].
- Prop A1: no-11 <-> dec-3AP and no-000 <-> inc-4AP orientation bookkeeping correct;
  transitivity claims are immediate from linearity of the induced order. The Sturmian side
  remark is heuristic and flagged as such; its impossibility argument (rational theta gives
  a zero-density step, irrational theta equidistributes below 1/3) is right. Machine:
  no-11/no-000 shadows verified on every asym witness, N <= 9; witness counts independently
  recomputed and match ASYM.md for N = 3..10.
- Prop A2: (a) z is the precedes-minimum, hence leader. (b),(c) as in Lemma 11 with
  Szemerédi (4-AP case) correctly applied in contrapositive. (d) chain termination is by
  order type omega (an unterminated extension process would build an infinite descending
  chain — correct use of Lemma 1's consequence); the non-leader-existence step ("all values
  > u leaders would put an interval tail, hence a 4-AP, inside Lambda") is correct. Machine:
  leader shadows (a(1) leader, order agreement, no leader 4-AP, drop-chains terminate at
  leaders) verified on every asym witness, N <= 9. PASS.

### Minor nits (no verdict impact)

1. Lemma 13 remark (ii) attributes the r3(N) <= N exp(-c (log N)^{1/9}) bound to
   Kelley–Meka; the 1/9 exponent is the Bloom–Sisask refinement (Kelley–Meka's original is
   1/12). Non-load-bearing.
2. Lemma 3 and Lemma 9 contain mid-proof ellipses/self-corrections; the completed arguments
   are present but the prose should be cleaned before any external use.
3. Density wording in Lemma 11(a) / Prop A1 as noted above.
4. ASYM.md status line says finite witnesses exist for N <= 27; experiments/asym_exhaust.out
   now shows EXISTS through N = 28 (N = 29 inconclusive, node cap). Update the status line.

### Machine evidence

- scratchpad/audit_hunt.py: L8 exhaustive N<=8; L10 exhaustive m<=7; L11 exhaustive
  4-AP-free N<=9; L13(a) exhaustive N<=9 (+60123 boundary cases confirming the w+3e<=N
  proviso); L13(b) e<g1 exhaustive N<=9 PASS and e=g1 counterexamples found; T12
  layer-cake/demand/ledger/finite-form exact-arithmetic on all 35847 inc-4AP-free perms
  N<=8, plus asymptotic frontier (no failure at C=9/8 for N<3000; failures at N=22/40/43
  for C=1.1/1.111../1.1125) and slack-repair check; A1/A2 shadows on all asym witnesses
  N<=9; FIN(1)-false parity check. ALL PASS except the two flagged gaps.
- experiments/apcheck.py self-test and experiments/core_checks.py (T1–T4): re-run, PASS.
- Independent DFS recount of asym witnesses cross-validated against brute force (N<=8),
  extended to N=9,10: matches ASYM.md's 11691, 45875.
