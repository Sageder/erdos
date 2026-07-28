"""farleft.py — verification of the FAR-LEFT REDUCTION of condition (ii).

Setting (CORE Props 29-30, Conjecture R21-C). Class architecture c = j + t with
j(v) = floor(log_b v), t : N -> Z>=0. Condition (ii): along every 4-AP the class sequence
is never strictly increasing and never strictly decreasing.

CLAIM (far-left reduction). Fix x >= 1. For every d large enough that
        j(x) + t(x) < j(x+d)                                        (FL)
(which holds for all d beyond a finite threshold, since t(x) is a fixed finite number and
j(x+d) -> infinity), write u_i = x + i*d for i = 1,2,3 and k = j(u_1). Then:

 (1) the DECREASING orientation is automatically satisfied -- (FL) makes c(x) smaller than
     c(u_1), so c(x) > c(u_1) is impossible; hence far-left APs constrain only the
     increasing orientation. This is a genuine asymmetry of the architecture.

 (2) the block pattern (j(u_1), j(u_2), j(u_3)) is one of (k,k,k), (k,k,k+1), (k,k+1,k+1)
     [block-gap lemma], and condition (ii) is EQUIVALENT, on these APs, to:
        (k,k,k)      : NOT ( t(u_1) <  t(u_2) <  t(u_3) )
        (k,k,k+1)    : NOT ( t(u_1) <  t(u_2) <= t(u_3) )
        (k,k+1,k+1)  : NOT ( t(u_1) <= t(u_2) <  t(u_3) )

 (3) Taking x = 1 (or any small x), u_1 = x+d, u_2 = x+2d, u_3 = x+3d with d ~ u_1, so the
     constrained triples are exactly the "geometric" triples (u, ~2u, ~3u). Condition (ii)
     therefore constrains t on every such triple, at every scale.

This script verifies (1), (2) and the block-gap lemma exhaustively over a large range, and
measures how many triples are actually constrained. Exact integer arithmetic throughout.
"""

import sys
sys.path.insert(0, '/home/user/erdos/experiments')


def blk(v, b):
    j, p = 0, 1
    while p * b <= v:
        p *= b
        j += 1
    return j


def check(b, V, tfun, name):
    """Verify (1) and (2) against the literal definition of (ii) on all far-left APs."""
    t = [0] * (V + 1)
    for v in range(1, V + 1):
        t[v] = tfun(v)
    c = [0] * (V + 1)
    for v in range(1, V + 1):
        c[v] = blk(v, b) + t[v]

    n_far, n_constrained, patterns = 0, 0, {}
    for x in range(1, 4):
        for d in range(1, (V - x) // 3 + 1):
            u = [x + i * d for i in range(4)]
            if u[3] > V:
                break
            if not (c[u[0]] < blk(u[1], b)):        # (FL)
                continue
            n_far += 1
            k = blk(u[1], b)
            pat = (blk(u[1], b) - k, blk(u[2], b) - k, blk(u[3], b) - k)
            assert pat in {(0, 0, 0), (0, 0, 1), (0, 1, 1)}, ("BLOCK-GAP VIOLATED", x, d, pat)
            patterns[pat] = patterns.get(pat, 0) + 1
            # (1) decreasing orientation must be impossible
            dec = c[u[0]] > c[u[1]] > c[u[2]] > c[u[3]]
            assert not dec, ("(1) VIOLATED: far-left AP decreasing", x, d)
            # (2) equivalence of (ii) with the t-only condition
            inc_actual = c[u[0]] < c[u[1]] < c[u[2]] < c[u[3]]
            t1, t2, t3 = t[u[1]], t[u[2]], t[u[3]]
            if pat == (0, 0, 0):
                inc_pred = (t1 < t2 < t3)
            elif pat == (0, 0, 1):
                inc_pred = (t1 < t2 <= t3)
            else:
                inc_pred = (t1 <= t2 < t3)
            assert inc_actual == inc_pred, ("(2) VIOLATED", x, d, pat, (t1, t2, t3),
                                            inc_actual, inc_pred)
            if inc_pred:
                n_constrained += 1
    return n_far, n_constrained, patterns


if __name__ == "__main__":
    import random
    rng = random.Random(196)
    V = 20000
    fams = [
        ("t = v2(v)            ", lambda v: (v & -v).bit_length() - 1),
        ("t = 0                ", lambda v: 0),
        ("t = v mod 3          ", lambda v: v % 3),
        ("t = random in [0,2]  ", lambda v: rng.randint(0, 2)),
        ("t = 1 if v odd       ", lambda v: v % 2),
    ]
    for b in (3, 4, 5):
        print(f"--- b = {b}")
        for name, f in fams:
            nf, nc, pats = check(b, V, f, name)
            tot = sum(pats.values())
            share = {p: f"{100*v/tot:.0f}%" for p, v in sorted(pats.items())}
            print(f"  {name}: far-left APs={nf:6d}  violating (ii)={nc:6d}"
                  f"  block patterns {share}", flush=True)
    print("\n(1) decreasing orientation impossible on far-left APs: VERIFIED on every case")
    print("(2) t-only characterisation matches the literal (ii): VERIFIED on every case")
    print("block-gap lemma (patterns only (k,k,k), (k,k,k+1), (k,k+1,k+1)): VERIFIED")
