"""banded.py -- the EXPLICIT within-block rule for the R1 corridor, solver-free.

MOTIVATION (proved, no search):  let W < U < V be cuts of a monotone-4-AP-free
permutation of N, and T = (U,V] the top block.

  Lemma FI (forced inversion).  For U < p < q <= V, if  W < 2p-q <= U  and
  1 <= 3p-2q <= W, then q precedes p.
  Proof: put d = q-p, c = p-d = 2p-q, so c-d = 3p-2q.  Then (c-d, c, p, q) is a
  4-AP with difference d; c-d <= W puts it in block [1,W], W < c <= U puts c in
  (W,U], and p,q are in T.  Blocks are laid out in increasing order, so
  pos(c-d) < pos(c) < pos(p).  If also pos(p) < pos(q) the four values would be an
  increasing monotone 4-AP.  Hence q precedes p.  []

  Solving the inequalities: for every p in (U, 2U-1] the forced targets are
      q in [ max(2p-U, ceil((3p-W)/2)), min(2p-W-1, floor((3p-1)/2)) ],
  an interval of about (W+1)/2 integers sitting just below 3p/2.

So EVERY p in the lower half of T must be preceded by the ~W/2 values just below
1.5p.  The cheapest order shape that does this is a DESCENDING BAND structure with
band ratio just under 3/2: cut T at s_0 = U < s_1 < s_2 < ... with s_{i+1} = ceil(
rho * s_i), rho slightly below 3/2, and emit the bands in DECREASING index order;
inside each band use a monotone-3-AP-free order (the parity recursion sigma), which
kills every in-band monotone 4-AP and every in-band increasing 3-AP at once.

That is Rule B below.  It is exactly the "banded: top fraction first, most of the
constrained pair family inverted" structure R1 reported in its ratio-5 witness, made
into a closed form.
"""

import sys
sys.path.insert(0, "/home/user/erdos/experiments")


# --------------------------------------------------------------------------- #
# sigma: the parity recursion -- a monotone-3-AP-free order of {1..n}
# (odds first in sigma-order, then evens in sigma-order; standard construction).

def sigma_order(n):
    if n <= 1:
        return list(range(1, n + 1))
    odds = sigma_order((n + 1) // 2)
    evens = sigma_order(n // 2)
    return [2 * i - 1 for i in odds] + [2 * i for i in evens]


def sigma_on(lo, hi):
    """sigma order of the integer interval [lo,hi]."""
    return [lo - 1 + i for i in sigma_order(hi - lo + 1)]


# --------------------------------------------------------------------------- #
# Rule B

def bands(lo, hi, rho_num=3, rho_den=2):
    """Band boundaries lo = s_0 < s_1 < ... < s_k = hi with s_{i+1} ~ rho * s_i."""
    s = [lo]
    while s[-1] < hi:
        nxt = (s[-1] * rho_num) // rho_den
        if nxt <= s[-1]:
            nxt = s[-1] + 1
        s.append(min(nxt, hi))
    return s


def rule_B_block(lo, hi, rho_num=3, rho_den=2, inner=sigma_on, descending=True):
    """Order of the block [lo,hi] under Rule B."""
    s = bands(lo - 1, hi, rho_num, rho_den)
    segs = [(s[i] + 1, s[i + 1]) for i in range(len(s) - 1)]
    if descending:
        segs = segs[::-1]
    out = []
    for a, b in segs:
        out.extend(inner(a, b))
    return out


def rule_B_permutation(cuts, **kw):
    """The full in-order block permutation of [1..V] induced by Rule B."""
    out = []
    prev = 0
    for c in cuts:
        out.extend(rule_B_block(prev + 1, c, **kw))
        prev = c
    return out


# --------------------------------------------------------------------------- #

def report(cuts, **kw):
    from apcheck import has_monotone_kap_general, has_monotone_kap_pos
    seq = rule_B_permutation(cuts, **kw)
    V = cuts[-1]
    assert sorted(seq) == list(range(1, V + 1))
    bad4 = has_monotone_kap_general(seq, 4)
    pos = {v: i for i, v in enumerate(seq)}
    # first violating 4-AP, and first C2 violation
    first4 = None
    for d in range(1, (V - 1) // 3 + 1):
        for x in range(1, V - 3 * d + 1):
            ps = [pos[x + j * d] for j in range(4)]
            if all(ps[j] < ps[j + 1] for j in range(3)):
                first4 = ('inc', x, d); break
            if all(ps[j] > ps[j + 1] for j in range(3)):
                first4 = ('dec', x, d); break
        if first4:
            break
    firstC2 = None
    for d in range(1, (V - 1) // 2 + 1):
        for x in range(1, V - 2 * d + 1):
            if x + 3 * d > V and pos[x] < pos[x + d] < pos[x + 2 * d]:
                firstC2 = (x, d); break
        if firstC2:
            break
    print(f"cuts={cuts} rho={kw.get('rho_num',3)}/{kw.get('rho_den',2)}  "
          f"4AP={'YES ' + str(first4) if bad4 else 'none'}   "
          f"C2={'violated ' + str(firstC2) if firstC2 else 'clean'}")
    return seq


if __name__ == "__main__":
    for rn, rd in [(3, 2), (7, 5), (2, 1), (5, 2), (3, 1), (4, 1)]:
        report([1, 2, 4, 10, 46, 136], rho_num=rn, rho_den=rd)
    print()
    for cuts in ([1, 2, 4, 10, 46], [1, 2, 4, 10, 46, 136],
                 [5, 25, 125], [5, 25, 125, 625], [4, 20, 100, 500]):
        report(cuts)
