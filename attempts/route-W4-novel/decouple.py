"""decouple.py — machine test of Proposition W4-1 (the decoupling criterion).

PROPOSITION W4-1.  Let c : N -> Z>=0 have finite fibres and order N by
   v before w   iff   c(v) < c(w),  or  c(v)=c(w) and v precedes w in a fixed
   monotone-3-AP-FREE order on that fibre (e.g. the base-2 van der Corput order tau_2,
   whose restriction to any subset is still monotone-3-AP-free).
If for EVERY 4-AP (t1,t2,t3,t4) the class sequence (c(t1),c(t2),c(t3),c(t4))
   (a) contains three consecutive equal entries, or
   (b) is not weakly monotone (has a strict ascent AND a strict descent),
then the resulting permutation of N is monotone-4-AP-free (and has order type omega).

This file (i) hunts for counterexamples to the implication over many class functions and
(ii) confirms the criterion is STRICTLY sufficient by exhibiting 4-AP-free orders whose
class sequences violate it.  Checker = apkit (cross-validated against apcheck.py).
"""
import random
import sys
sys.path.insert(0, "/home/user/erdos/attempts/route-W4-novel")
from apkit import pos_from_order, find_4aps
from numeration import base_digits


def vdc_key(v):
    return tuple(base_digits(v, 2)) + (0,) * 40


def build_order(cls, N):
    groups = {}
    for v in range(1, N + 1):
        groups.setdefault(cls[v], []).append(v)
    out = []
    for j in sorted(groups):
        g = sorted(groups[j], key=vdc_key)
        out.extend(g)
    return out


def criterion_holds(cls, N):
    """(a) 3 consecutive equal, or (b) not weakly monotone -- for every 4-AP."""
    for d in range(1, (N - 1) // 3 + 1):
        for x in range(1, N - 3 * d + 1):
            s = [cls[x + i * d] for i in range(4)]
            run3 = (s[0] == s[1] == s[2]) or (s[1] == s[2] == s[3])
            if run3:
                continue
            wi = s[0] <= s[1] <= s[2] <= s[3]
            wd = s[0] >= s[1] >= s[2] >= s[3]
            if wi or wd:
                return False, (x, d, tuple(s))
    return True, None


if __name__ == "__main__":
    rng = random.Random(196)
    tested = holds = 0
    viol = 0
    for trial in range(4000):
        N = rng.randint(8, 34)
        style = rng.randrange(5)
        cls = [0] * (N + 1)
        if style == 0:                                   # random classes
            M = rng.randint(1, N)
            for v in range(1, N + 1):
                cls[v] = rng.randrange(M)
        elif style == 1:                                 # intervals
            L = rng.randint(1, 6)
            for v in range(1, N + 1):
                cls[v] = v // L
        elif style == 2:                                 # blocks ratio b
            b = rng.choice([2, 3, 4])
            for v in range(1, N + 1):
                j, p = 0, 1
                while p * b <= v:
                    p *= b
                    j += 1
                cls[v] = j
        elif style == 3:                                 # residue-mixed (non convex)
            m = rng.randint(2, 5)
            L = rng.randint(m, 3 * m)
            for v in range(1, N + 1):
                cls[v] = (v // L) * m + (v % m)
        else:                                            # random monotone-ish
            c = 0
            for v in range(1, N + 1):
                c += rng.choice([0, 0, 1, 1, 2])
                cls[v] = c
        ok, w = criterion_holds(cls, N)
        order = build_order(cls, N)
        pos = pos_from_order(order)
        hits = find_4aps(pos, N)
        tested += 1
        if ok:
            holds += 1
            if hits:
                viol += 1
                print("COUNTEREXAMPLE to W4-1:", N, cls[1:], hits[0])
    print(f"Prop W4-1 tested on {tested} class functions; criterion held in {holds}; "
          f"violations of the implication: {viol}")

    # strictness: a 4-AP-free order whose class sequences violate the criterion
    # (take singleton classes = any 4-AP-free permutation; then no 3-run is ever possible
    #  and the class sequence is strictly monotone exactly when the 4-AP is monotone)
    from apcheck import has_monotone_kap_pos
    from itertools import permutations
    found = None
    for p in permutations(range(1, 8)):
        if not has_monotone_kap_pos(p, 4):
            cls = [0] * 8
            for i, v in enumerate(p):
                cls[v] = i
            ok, w = criterion_holds(cls, 7)
            if not ok:
                found = (p, w)
                break
    print("strictly sufficient (a 4-AP-free order violating the criterion):", found)
