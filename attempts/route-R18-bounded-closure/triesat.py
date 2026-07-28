"""triesat.py — the TRIE-COMPARATOR reduction: layered permutations whose blocks are
ordered by a binary trie comparator, for which monotone-4-AP-freeness collapses to a
2-SAT system over one boolean per trie node.

LEMMA R18.5 (binary trie comparator kills every monotone 3-AP).
Fix, for every level l >= 0 and every residue r mod 2^l, a bit f_{l,r}.  Define
    u <_f w   iff   f_{l,r} = bit_l(u),  where l = lowest bit at which u,w differ and
                    r = u mod 2^l  (= w mod 2^l).
This is a strict total order on N (it is a lexicographic order on the reversed-and-XORed
bit strings).  For EVERY subset S of N the induced order has NO monotone 3-AP.
Proof.  Let (x, x+d, x+2d), v = v2(d), r = x mod 2^v, a = bit_v(x).  Since d = 2^v d'
with d' odd, x and x+d first differ at level v, and so do x+d and x+2d; both pairs have
residue r mod 2^v.  bit_v(x+d) = 1-a, bit_v(x+2d) = a.  So "x before x+d" <=> f_{v,r}=a
and "x+d before x+2d" <=> f_{v,r}=1-a: exactly one of the two holds, so the triple is
neither positionally increasing nor positionally decreasing.  QED
(This is the comparator form of the parity permutation; the base-3 analogue is R3's
Lemma T, which only kills 4-APs.)

CONSTRUCTION Phi(cuts, f).  Blocks B_j = [c_j, c_{j+1}) listed in increasing order; inside
B_j order by the trie comparator with flips f^{(j)}.  Order type omega is automatic.

THEOREM R18.6 (collapse).  Assume the cut sequence has ratio >= 3 (so blocks.py's
[1+1+1+1] pattern is impossible).  Then Phi(cuts, f) is monotone-4-AP-free iff for every
AP (x, x+d, x+2d, x+3d) the following holds, with v = v2(d), r = x mod 2^v, a = bit_v(x):

  shape [4], [3+1], [1+3]  : nothing (Lemma R18.5 already kills these)
  shape [1+1+2], block l   : f^{(l)}_{v,r} = 1-a      (unit)
  shape [1+2+1], block k   : f^{(k)}_{v,r} = a        (unit)
  shape [2+1+1], block j   : f^{(j)}_{v,r} = 1-a      (unit; vacuous for ratio >= 2)
  shape [2+2], blocks j<k  : NOT( f^{(j)}_{v,r} = a  AND  f^{(k)}_{v,r} = a )   (binary)

Proof.  Combine blocks.py's Theorem R18.4 with Lemma R18.5 and the identities
bit_v(x+d) = 1-a, bit_v(x+2d) = a, bit_v(x+3d) = 1-a and
(x+d) mod 2^v = (x+2d) mod 2^v = (x+3d) mod 2^v = r  (d = 2^v d', so adding d flips bit v
and leaves bits < v alone).  Each "u before w" appearing in R18.4 is thus the single
literal [f_{v,r} = bit_v(u)].  QED

So the design question becomes a finite 2-SAT instance per block-pair, checkable to
N = 10^5 in seconds.  Everything is re-verified against apcheck at the end.
"""

import sys, time
import numpy as np
sys.path.insert(0, '/home/user/erdos/experiments')
sys.path.insert(0, '/home/user/erdos/attempts/route-R18-bounded-closure')
from apcheck import has_monotone_kap_pos, has_monotone_kap_general  # noqa: E402


# ------------------------------------------------------------------ comparator

def trie_key(v, flips_j, L):
    """Sort key realising the trie comparator: at level l (low->high) the branch taken is
    bit_l(v) XOR (1 - f_{l, v mod 2^l})... we simply build the reversed string of
    (bit_l(v) == f_{l,r} ? 0 : 1) which is 0 when v goes first."""
    key = []
    for l in range(L):
        r = v & ((1 << l) - 1)
        b = (v >> l) & 1
        f = flips_j.get((l, r), 0)
        key.append(0 if b == f else 1)
    # level 0 is consulted FIRST, i.e. it is the most significant component
    return tuple(key)


def order_block(vals, flips_j, L):
    return sorted(vals, key=lambda v: trie_key(v, flips_j, L))


# ------------------------------------------------------------------ constraints

def collect(cuts, N):
    """Vectorised sweep over all APs (x,d) with x+3d <= N.
    Returns (units, binaries, fatal) where
      units    : dict (j,v,r) -> set of required bit values
      binaries : list of ((j,v,r), (k,v,r), a)  meaning NOT(F1==a AND F2==a)
      fatal    : count of [1+1+1+1] patterns."""
    cutarr = np.array(cuts, dtype=np.int64)
    units = {}
    binaries = []
    fatal = 0

    def blk(arr):
        return np.searchsorted(cutarr, arr, side='right') - 1

    for d in range(1, (N - 1) // 3 + 1):
        x = np.arange(1, N - 3 * d + 1, dtype=np.int64)
        if x.size == 0:
            break
        b0, b1, b2, b3 = blk(x), blk(x + d), blk(x + 2 * d), blk(x + 3 * d)
        v = int(d & -d).bit_length() - 1          # v2(d)
        mask = (1 << v) - 1
        r = x & mask
        a = (x >> v) & 1
        s01, s12, s23 = (b0 == b1), (b1 == b2), (b2 == b3)
        # shape classification from the equality pattern of consecutive blocks
        # [4]: 111 ; [3+1]:110 ; [1+3]:011 ; [2+2]:101 ; [2+1+1]:100 ; [1+2+1]:010 ;
        # [1+1+2]:001 ; [1+1+1+1]:000
        sel = (~s01) & (~s12) & (~s23)
        fatal += int(sel.sum())
        for name, cond, blkarr, val in (
            ("1+1+2", (~s01) & (~s12) & s23, b2, 1 - a),
            ("1+2+1", (~s01) & s12 & (~s23), b1, a),
            ("2+1+1", s01 & (~s12) & (~s23), b0, 1 - a),
        ):
            idx = np.nonzero(cond)[0]
            if idx.size:
                for i in idx:
                    key = (int(blkarr[i]), v, int(r[i]))
                    units.setdefault(key, set()).add(int(val[i]))
        idx = np.nonzero(s01 & (~s12) & s23)[0]   # [2+2]
        for i in idx:
            binaries.append(((int(b0[i]), v, int(r[i])), (int(b2[i]), v, int(r[i])),
                             int(a[i])))
    return units, binaries, fatal


def solve_flips(units, binaries):
    """Unit propagation + 2-SAT.  Returns (ok, assignment dict node->bit, conflicts)."""
    assign = {}
    conflicts = []
    for key, vals in units.items():
        if len(vals) > 1:
            conflicts.append(('unit-clash', key))
        else:
            assign[key] = next(iter(vals))
    if conflicts:
        return False, assign, conflicts
    # binaries: NOT(F1==a AND F2==a)
    from pysat.solvers import Cadical195
    from pysat.formula import IDPool
    pool = IDPool()
    cl = []
    nodes = set(assign) | {n for (n1, n2, _) in binaries for n in (n1, n2)}
    for n in nodes:
        pool.id(n)
    for n, b in assign.items():
        cl.append([pool.id(n) if b == 1 else -pool.id(n)])
    for (n1, n2, a) in binaries:
        # F==a  is literal (+id if a==1 else -id)
        l1 = pool.id(n1) if a == 1 else -pool.id(n1)
        l2 = pool.id(n2) if a == 1 else -pool.id(n2)
        cl.append([-l1, -l2])
    S = Cadical195(bootstrap_with=cl)
    ok = S.solve()
    out = {}
    if ok:
        model = set(S.get_model())
        for n in nodes:
            out[n] = 1 if pool.id(n) in model else 0
    S.delete()
    return ok, out, ([] if ok else [('2sat-unsat',)])


def build_perm(cuts, N, assign):
    """Assemble the permutation of [1..N] from the flip assignment."""
    L = max(1, N.bit_length())
    per_block = {}
    for v in range(1, N + 1):
        j = int(np.searchsorted(np.array(cuts), v, side='right')) - 1
        per_block.setdefault(j, []).append(v)
    perm = []
    for j in sorted(per_block):
        fj = {(l, r): b for (jj, l, r), b in assign.items() if jj == j}
        perm.extend(order_block(per_block[j], fj, L))
    return perm


def geom_cuts(r, top):
    c = [1]
    while c[-1] <= top:
        c.append(c[-1] * r)
    return c


# ------------------------------------------------------------------ self-tests

def _selftest():
    import random
    rng = random.Random(4242)
    # Lemma R18.5 : trie comparator is 3-AP-free on every subset
    for _ in range(300):
        L = 8
        flips = {(l, r): rng.randint(0, 1) for l in range(L) for r in range(1 << l)}
        S = rng.sample(range(1, 1 << L), rng.randint(6, 40))
        o = order_block(sorted(S), flips, L)
        assert not has_monotone_kap_general(o, 3), (flips, S, o)
    print("SELFTEST R18.5 OK: 300 random trie comparators x random subsets -> no monotone 3-AP")
    # R18.6 : collapse agrees with the trusted 4-AP checker
    from blocks import check_orders
    ntest = 0
    for _ in range(60):
        r = rng.choice([3, 4, 5])
        N = rng.randint(30, 200)
        cuts = geom_cuts(r, N)
        units, binaries, fatal = collect(cuts, N)
        ok, assign, _ = solve_flips(units, binaries)
        # random completion of unconstrained nodes, then check the theorem's prediction
        L = max(1, N.bit_length())
        for _ in range(4):
            full = dict(assign)
            for l in range(L):
                for rr in range(1 << l):
                    for j in range(len(cuts)):
                        full.setdefault((j, l, rr), rng.randint(0, 1))
            perm = build_perm(cuts, N, full)
            pred_ok = ok and fatal == 0
            actual_ok = not has_monotone_kap_pos(perm, 4)
            if pred_ok:
                assert actual_ok, ("R18.6 predicted 4-AP-free but checker found a 4-AP",
                                   r, N)
            ntest += 1
    print(f"SELFTEST R18.6 OK: {ntest} (cuts,N,flips) instances; every satisfying flip "
          f"assignment yields a genuinely monotone-4-AP-free layered permutation.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "selftest":
        _selftest()
        sys.exit()
    rs = [int(x) for x in (sys.argv[1].split(',') if len(sys.argv) > 1 else ['3', '4', '5', '6', '8'])]
    N = int(sys.argv[2]) if len(sys.argv) > 2 else 2000
    for r in rs:
        cuts = geom_cuts(r, N)
        t0 = time.time()
        units, binaries, fatal = collect(cuts, N)
        ok, assign, conf = solve_flips(units, binaries)
        dt = time.time() - t0
        print(f"ratio {r}: cuts={[c for c in cuts if c<=N]} N={N} fatal={fatal} "
              f"#units={len(units)} #binaries={len(binaries)} -> "
              f"{'FEASIBLE' if (ok and fatal==0) else 'INFEASIBLE'} "
              f"({conf[:2] if conf else ''}) [{dt:.1f}s]", flush=True)
        if ok and fatal == 0:
            perm = build_perm(cuts, N, assign)
            assert sorted(perm) == list(range(1, N + 1))
            assert not has_monotone_kap_pos(perm, 4), "CHECKER DISAGREES"
            print(f"   VERIFIED 4-AP-free by apcheck at N={N}", flush=True)
