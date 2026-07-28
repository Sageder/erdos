# PROOFS.md — Construction A and its properties (Route R2)

All conventions as in `/home/user/erdos/PROBLEM.md` (values and positions in
N = {1,2,...}; monotone k-AP = k positions increasing, values an AP read
ascending or descending; AP difference d >= 1 in the values).

## The construction

**Blocks.** For m >= 0 let
  B_m = { 4^m, 4^m + 1, ..., 4^{m+1} - 1 },   |B_m| = 3·4^m.
The B_m partition N (B_0 = {1,2,3}).

**Internal order.** For a finite set S of positive integers, the
*van der Corput order* (vdC) is: u comes before v iff at the least
significant bit position where the binary expansions of u and v differ, u has
bit 0. (Equivalently: sort by the reversed bit string, LSB first,
lexicographically.) Define
  pi_m = vdC order of B_m,  reversed when m is odd.

**Permutation.** a = the concatenation pi_0 pi_1 pi_2 ...  So position p
carries: find m with 4^m <= p < 4^{m+1}; then a(p) = the (p - 4^m + 1)-th
entry of pi_m.

Example: a = 2,1,3, 15,7,11,13,5,9,14,6,10,12,4,8, 32,16,48,40,24,56,...

## Lemma 0 (bijection, order type omega)

The blocks are finite sets partitioning N, listed one after another, each
exactly once. So every n in N occurs at exactly one position, and
pos(n) < 4^{m+1} when n in B_m: every value at a finite position, every
position filled. a is a bijection N -> N of order type omega. QED.

Moreover pos(v) and v lie in the same window [4^m, 4^{m+1}), hence

  **v/4 < pos(v) < 4·v for all v**  (linearly bounded displacement).

## Lemma 1 (no monotone 3-AP inside any block)

Let S be any finite set of positive integers and consider its vdC order or
the reverse of it. Then no 3-AP u, u+e, u+2e (e >= 1) with all three terms in
S occurs monotonically (neither ascending nor descending).

*Proof.* Let l = v2(e), e = 2^l e' with e' odd.
Adding e to u leaves bits 0..l-1 unchanged (e ≡ 0 mod 2^l) and flips bit l
(the carry into bit l is 0 and e has bit l equal to 1). Adding 2e leaves bits
0..l unchanged. Hence:
  bit_j(u) = bit_j(u+e) = bit_j(u+2e) for j < l;
  bit_l(u) = bit_l(u+2e) = 1 - bit_l(u+e).
So in vdC order, the comparisons (u vs u+e) and (u+2e vs u+e) are both decided
at bit l, in the same direction: the middle term u+e lies before BOTH u and
u+2e (if bit_l(u+e) = 0) or after both (if bit_l(u+e) = 1). A monotone
occurrence would need the middle value u+e at the middle of the three
positions — impossible. Reversing the order preserves the property (the
middle term stays extremal). QED.

## Lemma 2 (block-major positions)

If block(v) < block(w) then pos(v) < pos(w). If v < w then
block(v) <= block(w). (Blocks are increasing intervals concatenated in
increasing order.) QED.

## Lemma 3 (descending monotone APs have length <= 2)

Suppose values v_1 > v_2 > ... > v_k occur at increasing positions. By
Lemma 2, blocks weakly decrease along positions and weakly increase — hence
all v_i lie in ONE block. If k >= 3 and the v_i form an AP, then v_1, v_2, v_3
is a 3-AP occurring descending inside one pi_m, contradicting Lemma 1. So a
monotone descending AP has length <= 2. In particular **a has no monotone
descending 3-AP, hence none of any length >= 3**. QED.

## Lemma 4 (contiguity)

If x, x+d, ..., x+(k-1)d is an AP (d >= 1), the set of indices i with
x+id in B_m is a contiguous range, because the terms increase with i and B_m
is an interval. QED.

## Lemma 5 (adjacency / Lipschitz)

For i >= 1, t_{i+1} := x+(i+1)d < 2·t_i (since (1-i)d <= 0 < x). Hence if
t_i in B_j then t_{i+1} < 2·4^{j+1} < 4^{j+2}, so block(t_{i+1}) <= j+1:
from the second term on, consecutive AP terms lie in the same or adjacent
blocks. QED.

## Lemma 6 (tail-spread of a 5-AP)

For a 5-AP x, x+d, ..., x+4d write t_i = x+id. Then t_4 = 4·t_1 - 3x < 4·t_1.
If t_1, t_2, t_3, t_4 met >= 3 distinct blocks, the largest met block index
would be >= block(t_1) + 2, giving
  t_4 >= 4^{block(t_1)+2} = 4·4^{block(t_1)+1} > 4·t_1,
a contradiction. So t_1..t_4 lie in at most 2 distinct blocks; if exactly two,
they are adjacent (Lemma 5 steps are 0 or +1). QED.

## Lemma 7 (pair criterion)

Let u, u+d in B_m, l = v2(d). As in Lemma 1, u and u+d first differ at bit l.
In vdC order, u precedes u+d iff bit_l(u) = 0; in the reversed order iff
bit_l(u) = 1. Hence in pi_m:
  **u precedes u+d  <=>  bit_l(u) = m mod 2.** QED.

## Theorem (no monotone 5-AP)

a contains no monotone 5-term AP, in either orientation.

*Proof.* Descending: Lemma 3. Ascending: suppose t_0 < t_1 < ... < t_4
(t_i = x+id) occur at increasing positions. If some block held >= 3 of the
terms, by Lemma 4 it would hold 3 consecutive terms — a 3-AP with difference
d occurring ascending inside one pi_m, contradicting Lemma 1. So every block
holds <= 2 terms. By Lemma 6, t_1..t_4 meet at most 2 blocks; four terms, at
most two per block, means exactly the split
  {t_1, t_2} ⊂ B_m,  {t_3, t_4} ⊂ B_{m+1}  (adjacent by Lemma 6).
t_0's block is <= m (Lemma 2) and not m (else B_m holds t_0,t_1,t_2). Fine —
t_0 sits in an earlier block, at an automatically earlier position.
Monotonicity forces, by Lemma 7 with l = v2(d):
  bit_l(t_1) = m mod 2   and   bit_l(t_3) = (m+1) mod 2.
But t_3 - t_1 = 2d ≡ 0 (mod 2^{l+1}), so bit_l(t_3) = bit_l(t_1).
Contradiction. QED.

## Proposition (exact structure of the monotone 4-APs of a)

Every monotone 4-AP of a is ascending, and is of one of two shapes
(t_i = x+id, l = v2(d)):

  **S1** (1|1|2): block(t_0) < block(t_1) = m-1, {t_2, t_3} ⊂ B_m,
        with bit_l(t_2) = m mod 2;
  **S2** (1|2|1): block(t_0) < m, {t_1, t_2} ⊂ B_m, t_3 in B_{m+1},
        with bit_l(t_1) = m mod 2.

Conversely every configuration of shape S1 or S2 (with the stated block
memberships and bit condition) IS a monotone 4-AP of a.

*Proof sketch.* Descending is dead by Lemma 3. For ascending 4-APs, the same
group analysis as in the Theorem: no block holds 3 terms (Lemma 1 + Lemma 4);
t_1, t_2, t_3 meet at most 2 blocks (as in Lemma 6: three distinct blocks
would force t_3 > 4 t_1 >= t_3 + 3x, impossible); Lemma 5 forces adjacency,
Lemma 7 turns the single within-block pair into the bit condition. The two
possible splits of {t_1,t_2,t_3} into contiguous groups of size <= 2 over two
adjacent blocks give S1 ({t_2,t_3} paired, forcing block(t_1) = m-1 by
Lemma 5) and S2 ({t_1,t_2} paired, t_3 in B_{m+1} by Lemma 5). The (2,2)
split {t_0,t_1} ⊂ B_{m-1}, {t_2,t_3} ⊂ B_m dies exactly like the 5-AP:
bit_l(t_0) = (m-1) mod 2 and bit_l(t_2) = m mod 2 contradict
t_2 - t_0 = 2d ≡ 0 mod 2^{l+1}. For the converse, in shape S1/S2 all
cross-block position requirements hold automatically (Lemma 2) and the pair
ascends by Lemma 7. QED.

*Machine confirmation*: the census of all 1,304,268 monotone 4-APs of the
N = 16383 prefix matches exactly (verify_construction.py, V5): every 4-AP is
ascending, of shape S1 (979,436) or S2 (324,832), with the bit condition.

## Status of verification

- Lemmas 0-7, Theorem, Proposition: proved above (hand proofs).
- Machine evidence (exact arithmetic, validated checkers): no monotone 5-AP
  and no descending monotone 3-AP in the prefix N = 65535; bijectivity of
  prefixes up to N = 65535; the 4-AP census at N = 16383.
- Finite prefix checks are evidence for the infinite claims, not proof; the
  infinite claims rest on the proofs above.
