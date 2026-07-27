# BLOCKS.md — contiguous-block architectures: exact pattern taxonomy and sign calculus

Derived inline (session 1). Status: rigorous derivation of the residual constraint
system for contiguous-block designs with ratio-3 value blocks; viability GATED on the
plain-linear-profile probe (experiments/plain_linear_profile.py): every contiguous
geometric-block design induces pos(v) ≤ C·v for a modest constant C, so extinction of
linear-profile plain avoiders at all C would kill this whole family.

## Setup

Value blocks: intervals I_k := [n_k, n_{k+1}) with n_k = 3^k (so |I_k| = 2·3^k),
k = 0, 1, 2, … (I_0 = {1, 2}). Position layout: contiguous chunks, one block per
chunk; chunk order given by a bijection π of the block indices (π(k) = slot of block k).
In-block arrangement ("gadget") g_k: a permutation of I_k. Any such design is a genuine
permutation of ℕ with order type ω provided every block has a finite slot (π bijection).

## Lemma B1 (ratio-3 scale confinement)

For any 4-AP t₁ < t₂ < t₃ < t₄ (tᵢ = x + (i−1)d, d ≥ 1, x ≥ 1):
t₃ < 2t₂ and t₄ < 3t₂ and t₄ < 2t₃.
Hence with n_k = 3^k: if t₂ ∈ I_j then t₃, t₄ ∈ I_j ∪ I_{j+1}; a 4-AP meets at most
3 distinct blocks, and never 4. Moreover block membership of the four terms is by
CONSECUTIVE runs (blocks are intervals — convexity).

Proof. d = t₂ − t₁ ≤ t₂ − 1 < t₂, so t₃ = t₂ + d < 2t₂, t₄ = t₂ + 2d < 3t₂ ≤ 3n_{j+1}
≤ n_{j+2} when t₂ ∈ I_j; also t₄ = t₃ + d < 2t₃. Convexity: blocks are intervals. ∎

## Pattern taxonomy (exhaustive, given B1)

Writing the block-run pattern of (t₁,t₂,t₃,t₄):
 (a) 4          — all four in one block I_j.
 (b) 3+1 / 1+3  — three consecutive terms in one block (they form a 3-AP), one outside.
 (P2) 2+2       — {t₁,t₂} ⊂ I_j, {t₃,t₄} ⊂ I_{j'}; B1 forces j' = j+1.
 (P3) 2+1+1     — {t₁,t₂} ⊂ I_j, t₃ ∈ I_{j+1}, t₄ ∈ I_{j+2} (B1: t₃ ∈ I_{j+1} forced
                  since t₃ < 2t₂ < 2n_{j+1} < n_{j+2}; t₄ ∈ I_{j+1} would be P2-type…
                  here t₄ ∈ I_{j+2}, which B1 allows: t₄ < 2t₃ < 2n_{j+2} < n_{j+3}).
 (P1) 1+2+1     — t₁ ∈ I_i (i < k), {t₂,t₃} ⊂ I_k, t₄ ∈ I_{k+1} (B1: t₄ < 2t₃).
 (P4) 1+1+2     — t₁ ∈ I_i (i < k−1), t₂ ∈ I_{k−1}, {t₃,t₄} ⊂ I_k (B1: t₃ < 2t₂ forces
                  t₂'s block adjacent-below t₃'s).
 1+1+1+1        — impossible (B1).
(The reflected reading is not separate: orientation is handled per pattern below.)

## Kill mechanisms

- (a): choose g_k with no monotone 4-AP within I_k — e.g. affine parity gadget
  (3-AP-free) kills (a) and (b) at once.
- (b): the three same-block terms are consecutive (convexity) hence a 3-AP; a monotone
  4-AP needs them monotone: killed by 3-AP-free gadgets. NOTE: this uses that any 3
  consecutive terms of a 4-AP form a 3-AP; the outside term is irrelevant.
- (P3): monotone (either orientation) forces π(j), π(j+1), π(j+2) monotone. Killed for
  ALL j iff π has no monotone consecutive triple. The pair-swap order
  π = (1, 0, 3, 2, 5, 4, …), i.e. π(k) = k+2 for even k, π(k) = k for odd k, has this
  property (verified: triples (π(k), π(k+1), π(k+2)) = (k+2, k+1, k+4) for even k,
  (k, k+3, k+2) for odd k — never monotone).
- (P1): increasing needs π(i) < π(k) < π(k+1) and pair (t₂,t₃) increasing in g_k;
  decreasing needs π(k+1) < π(k) < π(i) and pair decreasing. With pair-swap π:
  · k even: π(k) = k+2 > π(k+1) = k+1 kills increasing; and no i < k has
    π(i) ≥ k+2 (π(i) ≤ i+2 ≤ k+1), killing decreasing. NO gadget constraint.
  · k odd: π(k) = k < π(k+1) = k+3, and i with π(i) < k exist (all i ≤ k−2 have
    π(i) ≤ k−...: π(i) ∈ {i, i+2} ≤ k ; note π(k−1) = k+1 > k — the specific i must
    satisfy π(i) < π(k): i ≤ k−2 suffices for i even (π = i+2 ≤ k) and any odd i < k
    (π = i < k); such i < k exist for k ≥ 2, and t₁ ∈ I_i is realizable for every
    i < k for SOME AP — see B2 below): so increasing must be killed by the gadget:
    DEMAND: every "high pair" of an odd block is positioned DEcreasingly, where a high
    pair of I_k is (u, u+d) ⊂ I_k with u + 2d ∈ I_{k+1} and u − d ≥ 1.
    Decreasing: needs π(i) > π(k) = k for some i < k with t₁ ∈ I_i: π(i) > k iff
    i = k−1 (π(k−1) = k+1). So ALSO demand: pairs (t₂,t₃) ⊂ I_k (k odd) with
    u + 2d ∈ I_{k+1} AND u − d ∈ I_{k−1} must not be positioned decreasingly — but the
    high-pair demand says decreasing! CONFLICT unless no high pair of an odd block has
    its backward extension in I_{k−1}. Such pairs DO exist (see B3). ⇒ the naive
    uniform demand is INCONSISTENT; killing must be configuration-dependent.
- (P4), (P2): analogous sign calculus; several demands overlap on the same pairs, with
  at least one genuine conflict instance exhibited (B3).

## Lemma B2 (realizability of P1 configurations, k odd, any i ≤ k−2)

For k ≥ i+2, there exist APs with t₁ ∈ I_i, t₂, t₃ ∈ I_k, t₄ ∈ I_{k+1}:
take d slightly under n_k (e.g. d = n_k − s for small s ≥ 1 with t₁ := n_k + n_{k-1} −
… concretely t₂ = t₁ + d with t₁ ∈ I_i arbitrary, d chosen with t₂, t₂+d ∈ I_k,
t₂+2d ∈ I_{k+1}: since |I_k| = 2n_k and d can range in (n_k/2, n_k), the window is
nonempty for every t₁ < n_{i+1} ≤ n_{k−1}). Machine-verified in blocks_check.py.

## Lemma B3 (conflict instance)

In I_k (n_k = 3^k, k ≥ 3): the pair (u, u+d) with u = ⌈1.85·3^k⌉, d = ⌈0.9·3^k⌉
(exact witnesses in blocks_check.py) satisfies simultaneously:
 - u + 2d ∈ I_{k+1} (high pair), and
 - u − d ∈ I_{k−1}, 1 ≤ u − 2d < n_{k−1}.
Hence it receives contradictory uniform demands from P1-increasing (DEC) and
P1-decreasing/P4 (NOT-DEC / DEC as the case may be) — uniform per-block direction
assignments cannot close the case analysis; a finer, configuration-dependent kill
assignment (a genuine CSP across neighboring blocks) is required.

## Program (route R12)

1. Machine-verify B1–B3 and the taxonomy exhaustively at small scales (all APs in
   [1..3^6], classified against the pattern list — no AP escapes the taxonomy).
2. Encode the residual CSP: blocks 0..K (K ≈ 5–6), pair-swap π (and variants),
   in-block orders as SAT variables, all cross-block monotone-AP clauses; solve.
   If SAT: extract gadget structure, look for an affine/self-similar uniform gadget,
   then attempt an all-k proof. If UNSAT at some K: contiguous ratio-3 pair-swap
   designs are DEAD (finite certificate); vary π (other zigzag orders, ratio 4+,
   non-geometric growth) before declaring the contiguous family blocked.
3. GATE (runs first): plain_linear_profile.py — extinction of pos(v) ≤ 15·v plain
   avoiders at moderate N kills every contiguous geometric design a priori.
