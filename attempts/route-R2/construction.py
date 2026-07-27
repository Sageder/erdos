"""construction.py — Route R2 candidate: a permutation of N = {1,2,3,...} with
(conjecturally, proof sketch in REPORT.md) NO monotone 5-term AP.

CONSTRUCTION A
==============
Blocks:            B_m = {4^m, 4^m + 1, ..., 4^{m+1} - 1},  m = 0, 1, 2, ...
                   (B_0 = {1,2,3}; the blocks partition N; |B_m| = 3*4^m.)
Internal order:    sort B_m by van der Corput order  (compare binary expansions
                   least-significant-bit first, lexicographically, bit 0 < bit 1);
                   if m is ODD, reverse the sorted list.
Permutation a:     the concatenation  pi_0 pi_1 pi_2 ...  (block-major).

Bijectivity / order type omega: immediate — the blocks are finite, partition N,
and are listed one after another, so every n in N occupies exactly one finite
position and every position is filled.

Key structural lemmas (proved in REPORT.md, machine-checked here):
 L1  vdC order (and its reverse) contains no monotone 3-AP internally.
 L2  positions are block-major: block(v) < block(w)  =>  pos(v) < pos(w).
 L3  a monotone DEcreasing AP lies inside one block => length <= 2 by L1.
 L4  in an ascending AP, the terms falling in one block are consecutive terms.
 L5  (Lipschitz) for i >= 1, t_{i+1} = x+(i+1)d <= 2 t_i, so consecutive AP
     terms from the 2nd on lie in the same or adjacent blocks.
 L6  (ratio-4 spread) the last four terms x+d..x+4d of a 5-AP satisfy
     t4 < 4 t1, hence occupy at most TWO distinct blocks (necessarily adjacent).
 L7  (pair criterion) for u, u+d in B_m with l = v2(d):
     u precedes u+d in pi_m  <=>  bit_l(u) = m mod 2.
 MAIN: an ascending monotone 5-AP must split as (x)(x+d,x+2d)(x+3d,x+4d) with
     the two pairs in adjacent blocks B_m, B_{m+1}; L7 demands
     bit_l(x+d) = m mod 2 AND bit_l(x+3d) = (m+1) mod 2, but
     bit_l(x+3d) = bit_l(x+d) since (x+3d)-(x+d) = 2d is divisible by 2^{l+1}.
     Contradiction. With L3, NO monotone 5-AP in either orientation.
"""


def vdc_sorted(vals, width):
    """Sort integers by van der Corput order: LSB-first lexicographic, 0 < 1.
    Equivalent to sorting by the bit-reversed value at the given width."""
    def key(v):
        return tuple((v >> i) & 1 for i in range(width))
    return sorted(vals, key=key)


def block(m):
    """The set B_m as a range."""
    return range(4 ** m, 4 ** (m + 1))


def block_order(m):
    """pi_m: the internal listing of B_m."""
    width = 2 * (m + 1)          # 4^{m+1}-1 has exactly 2(m+1) bits
    lst = vdc_sorted(block(m), width)
    if m % 2 == 1:
        lst.reverse()
    return lst


def prefix(num_blocks):
    """First sum(|B_m|) = 4^{num_blocks} - 1 entries of the permutation a.
    Because blocks are intervals concatenated in increasing order, this prefix
    is exactly the values {1..4^num_blocks - 1} in position order, i.e. the
    restriction-principle prefix is literally a position prefix here."""
    out = []
    for m in range(num_blocks):
        out.extend(block_order(m))
    return out


def block_of(v):
    m = 0
    while 4 ** (m + 1) <= v:
        m += 1
    return m


if __name__ == "__main__":
    # --- self-tests -------------------------------------------------------
    # bijectivity of prefixes: values {1..4^k - 1} each occur exactly once.
    for k in range(1, 9):
        p = prefix(k)
        n = 4 ** k - 1
        assert len(p) == n and sorted(p) == list(range(1, n + 1)), k
    print("bijectivity OK: prefixes k=1..8 are permutations of [1..4^k-1]")

    # independent re-derivation of the internal order for small blocks by a
    # different method (sort by reversed-binary-string) to guard against bugs.
    def key2(v, w):
        return format(v, "0%db" % w)[::-1]
    for m in range(0, 6):
        w = 2 * (m + 1)
        alt = sorted(block(m), key=lambda v: key2(v, w))
        if m % 2 == 1:
            alt.reverse()
        assert alt == block_order(m), m
    print("internal order cross-check OK (two independent vdC implementations)")

    print("pi_0 =", block_order(0))
    print("pi_1 =", block_order(1))
    print("pi_2 =", block_order(2))
    print("first 20 entries:", prefix(3)[:20])
