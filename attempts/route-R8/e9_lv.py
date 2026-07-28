"""e9_lv.py — reconstruction of a LeSaulnier--Vijay-type theorem (route R8 deliverable 3).

Construction W (two ascending streams, evens at double rate):
    W = 2, (1, 4, 6), (3, 8, 10), (5, 12, 14), (7, 16, 18), ...
i.e. after the initial '2', concatenate triples (2i-1, 4i, 4i+2) for i = 1, 2, 3, ...
Equivalently: odds ascending, evens ascending, with exactly floor(n/2) odds before the n-th
even.  CLAIM (machine-verified here; proved in REPORT.md): W is a permutation of N with NO
monotone 4-term AP of ODD common difference (both orientations).

Also: rate-vector search for the mod-4 generalization (kill all d not divisible by 4):
four ascending streams (residues 1,2,3,0 mod 4), class c emitted with rate r_c; exact
schedule: emit next element of the class minimizing (m_c + 1) / r_c (m_c = emitted count),
ties by smaller class index.  Search r in {1,2,4,8,16}^4, verify prefixes exactly.
"""

import sys
import os
from fractions import Fraction
from itertools import product

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "experiments"))
import numpy as np  # noqa: E402


def W_prefix(nterms):
    seq = [2]
    i = 1
    while len(seq) < nterms:
        seq.extend([2 * i - 1, 4 * i, 4 * i + 2])
        i += 1
    return seq[:nterms]


def monotone_4aps_dfilter(seq, dpred, limit=5):
    """Exact: all monotone 4-APs of the finite sequence with dpred(d); returns witnesses.
    seq must be a permutation of [1..N] (checked)."""
    n = len(seq)
    assert sorted(seq) == list(range(1, n + 1))
    pos = np.empty(n + 1, dtype=np.int64)
    pos[np.asarray(seq, dtype=np.int64)] = np.arange(n, dtype=np.int64)
    out = []
    for d in range(1, (n - 1) // 3 + 1):
        if not dpred(d):
            continue
        top = n - 3 * d
        c0, c1, c2, c3 = (pos[1 + j * d: top + j * d + 1] for j in range(4))
        inc = (c0 < c1) & (c1 < c2) & (c2 < c3)
        dec = (c0 > c1) & (c1 > c2) & (c2 > c3)
        for x0 in np.nonzero(inc | dec)[0]:
            out.append((int(x0) + 1, d, "+1" if inc[x0] else "-1"))
            if len(out) >= limit:
                return out
    return out


def truncate_to_perm(seq):
    """Longest prefix-closed value set: keep only values <= max covered initial interval,
    preserving order (needed since streams advance unevenly)."""
    have = set(seq)
    n = 0
    while (n + 1) in have:
        n += 1
    return [v for v in seq if v <= n]


def rate_schedule(rates, nterms):
    """Emit from 4 ascending streams (residues 1,2,3,0 -> values c, c+4, c+8, ...) with
    priorities (m_c+1)/r_c.  Exact fractions."""
    residues = [1, 2, 3, 4]  # class '0 mod 4' represented by values 4, 8, 12...
    counts = [0, 0, 0, 0]
    seq = []
    for _ in range(nterms):
        best, bi = None, None
        for ci in range(4):
            w = Fraction(counts[ci] + 1, rates[ci])
            if best is None or w < best:
                best, bi = w, ci
        v = residues[bi] + 4 * counts[bi]
        counts[bi] += 1
        seq.append(v)
    return seq


if __name__ == "__main__":
    # --- W construction ---
    for N in (1000, 5000, 20000):
        seq = W_prefix(N)
        seqp = truncate_to_perm(seq)
        wit = monotone_4aps_dfilter(seqp, lambda d: d % 2 == 1)
        print(f"W prefix (permutation of [1..{len(seqp)}]): monotone 4-APs with odd d: "
              f"{wit if wit else 'NONE'}")
    # sanity: W does contain even-d monotone 4-APs (it must; e.g. 2,4,6,8)
    seqp = truncate_to_perm(W_prefix(200))
    we = monotone_4aps_dfilter(seqp, lambda d: d % 2 == 0, limit=3)
    print(f"W: examples of even-d monotone 4-APs (expected to exist): {we}")

    # --- mod-4 rate search ---
    print("mod-4 rate-vector search (kill all d with d % 4 != 0), prefix ~ 2400:")
    found = []
    for rates in product([1, 2, 4, 8, 16], repeat=4):
        seq = rate_schedule(rates, 3000)
        seqp = truncate_to_perm(seq)
        if len(seqp) < 600:
            continue
        wit = monotone_4aps_dfilter(seqp, lambda d: d % 4 != 0, limit=1)
        if not wit:
            found.append((rates, len(seqp)))
            print(f"  rates {rates}: NO violating 4-AP on [1..{len(seqp)}]  *** CANDIDATE")
    if not found:
        print("  no single-level rate vector works (expected from the path analysis; "
              "the wrap-around class pair defeats geometric rates)")
