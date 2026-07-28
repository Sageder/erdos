"""e4_zsat.py — SAT-guided construction of a Z-permutation (bijection Z -> Z, doubly infinite
sequence) with no monotone 5-AP; re-derivation target for Adenwalla's bound k <= 4 in Erdos 195.

Macro layout (alternating-scale slots): value blocks
    D_0' = {-1, 0, 1},   D_m = {v : 2^m <= |v| < 2^(m+1)}  (m >= 1)
slot order (position axis, left to right):
    ..., D_5, D_3, D_1, D_0', D_2, D_4, D_6, ...
i.e. slot index s(D_0') = 0, s(D_{2j}) = j (right), s(D_{2j-1}) = -j (left).
Within each slot the block is arranged by an unknown permutation (SAT variables on pair orders,
with transitivity).  Cross-slot position order is a constant determined by slot indices.

For every k-AP with all terms in the settled universe: clause "not all adjacent comparisons
increasing" and "not all decreasing" (cross pairs contribute constants; if a clause has no
literals and all constants line up monotone, the macro is refuted and we report the witness AP).

Solved incrementally: settle blocks D_0', D_1, ..., freezing earlier tau's; APs are activated
when all their terms lie in settled blocks.  Independent verification: assemble the two-sided
window and run the exact checker has_kap_vals_np.
"""

import sys
import os
import functools
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "experiments"))
from fastcheck import has_kap_vals_np  # noqa: E402
from zcheck import find_monotone_kaps  # noqa: E402

from pysat.solvers import Cadical153  # noqa: E402


def block_index(v):
    """m such that v in D_m (with D_0' = {-1,0,1} -> 0)."""
    a = abs(v)
    if a <= 1:
        return 0
    return a.bit_length() - 1


def slot_of_block(m):
    """slot index: even m -> m//2 (right side), odd m -> -((m+1)//2) (left side)."""
    return (m // 2) if m % 2 == 0 else -((m + 1) // 2)


def block_values(m):
    if m == 0:
        return [-1, 0, 1]
    lo, hi = 2 ** m, 2 ** (m + 1)
    return list(range(-hi + 1, -lo + 1)) + list(range(lo, hi))


class ZSat:
    def __init__(self, k=5):
        self.k = k
        self.frozen = {}      # block m -> tau list (position order within slot)
        self.frozen_pos = {}  # value -> (slot, index) for frozen blocks

    def pos_key_frozen(self, v):
        m = block_index(v)
        tau = self.frozen[m]
        return (slot_of_block(m), tau.index(v))

    def settle_next(self, m, verbose=True):
        """Solve block m given frozen blocks < m.  Returns True on success."""
        k = self.k
        vals = block_values(m)
        vid = {}
        ctr = [0]

        def var(u, v):
            # u, v in current block, u != v; canonical: (min, max) with sign of literal
            a, b = (u, v) if u < v else (v, u)
            if (a, b) not in vid:
                ctr[0] += 1
                vid[(a, b)] = ctr[0]
            lit = vid[(a, b)]
            return lit if (u, v) == (a, b) else -lit

        cnf = []
        for a, b, c in combinations(vals, 3):
            cnf.append([-var(a, b), -var(b, c), var(a, c)])
            cnf.append([var(a, b), var(b, c), -var(a, c)])

        # enumerate APs with all terms in settled universe (blocks <= m), at least one term in
        # block m (APs fully in earlier blocks were already handled).
        settled = set()
        for mm in range(m + 1):
            settled.update(block_values(mm))
        newvals = set(vals)
        universe = settled
        Vmax = max(universe)
        refuted = []
        # iterate over APs: choose d >= 1 and first term t so all terms in universe values
        # universe = {v: |v| <= Vmax} minus nothing (blocks tile all of [-Vmax, Vmax])
        for d in range(1, (2 * Vmax) // (k - 1) + 1):
            t0 = -Vmax
            t1 = Vmax - (k - 1) * d
            for t in range(t0, t1 + 1):
                terms = [t + j * d for j in range(k)]
                if not any(x in newvals for x in terms):
                    continue
                # adjacent comparisons
                inc_clause, dec_clause = [], []
                inc_const_ok = dec_const_ok = True
                for j in range(k - 1):
                    u, v = terms[j], terms[j + 1]
                    mu, mv = block_index(u), block_index(v)
                    if mu == mv == m:
                        inc_clause.append(-var(u, v))   # need pos(u) > pos(v) somewhere
                        dec_clause.append(var(u, v))
                    elif mu == mv:
                        # frozen block: constant comparison
                        pu, pv = self.pos_key_frozen(u), self.pos_key_frozen(v)
                        if pu < pv:
                            dec_const_ok = False
                        else:
                            inc_const_ok = False
                    else:
                        su, sv = slot_of_block(mu), slot_of_block(mv)
                        if su < sv:
                            dec_const_ok = False
                        else:
                            inc_const_ok = False
                if inc_const_ok:
                    if inc_clause:
                        cnf.append(inc_clause)
                    else:
                        refuted.append((t, d, "inc"))
                if dec_const_ok:
                    if dec_clause:
                        cnf.append(dec_clause)
                    else:
                        refuted.append((t, d, "dec"))
        if refuted:
            if verbose:
                print(f"  block {m}: MACRO REFUTED by APs with no free pair, e.g. "
                      f"{refuted[:6]}")
            return False
        with Cadical153(bootstrap_with=cnf) as s:
            if not s.solve():
                if verbose:
                    print(f"  block {m}: UNSAT")
                return False
            model = set(l for l in s.get_model() if l > 0)

        def cmp(u, v):
            if u == v:
                return 0
            a, b = (u, v) if u < v else (v, u)
            if (a, b) not in vid:
                before = True
            else:
                before = vid[(a, b)] in model
            if (u, v) == (a, b):
                return -1 if before else 1
            return 1 if before else -1

        tau = sorted(vals, key=functools.cmp_to_key(cmp))
        self.frozen[m] = tau
        for i, v in enumerate(tau):
            self.frozen_pos[v] = (slot_of_block(m), i)
        if verbose:
            show = tau if len(tau) <= 40 else tau[:20] + ["..."]
            print(f"  block {m} SAT: tau = {show}")
        return True

    def assemble_window(self):
        """Two-sided sequence: slots in increasing slot order, each with its tau."""
        ms = sorted(self.frozen)
        slots = sorted((slot_of_block(m), m) for m in ms)
        seq = []
        for s_, m in slots:
            seq.extend(self.frozen[m])
        return seq


if __name__ == "__main__":
    for k in (5, 4):
        print(f"=== Z alternating-scale macro, k={k} ===")
        zs = ZSat(k=k)
        okall = True
        for m in range(0, 9):
            ok = zs.settle_next(m)
            if not ok:
                okall = False
                break
        seq = zs.assemble_window()
        if len(zs.frozen) >= 4:
            bad = has_kap_vals_np(seq, k)
            print(f"  assembled window over blocks 0..{max(zs.frozen)} "
                  f"(|window|={len(seq)}): monotone {k}-AP present: {bad}")
            if bad:
                print("   e.g.:", find_monotone_kaps(seq, k, limit=5))
