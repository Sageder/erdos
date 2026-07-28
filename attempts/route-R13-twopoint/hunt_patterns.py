"""hunt_patterns.py — EXHAUSTIVE two-point configuration hunt (route R13).

For every monotone-4-AP-free permutation of [1..N], every ordered pair (p,q), p<q,
drawn from a prescribed pair of "anchor classes", and every arithmetic progression
of length L in {3,4} that contains BOTH p and q at prescribed index positions (i<j),
we record the positional PATTERN of the progression (the relative order of
pos(t_1),...,pos(t_L)).

A pattern that is never realised, over all boards and all admissible (p,q), is a
CANDIDATE two-point forcing law: "for anchors p in S, q in T at AP-indices (i,j),
the configuration cannot look like <pattern>".

Anchor classes:
   R = sigma_N-records          (relaxation of genuine records; see enum.py header)
   G = grounded values          (exact)
   A = all values               (control: exclusions here are pure 4-AP-freeness)
   Rc = consecutive records     (q is the record right after p)
   Gc = consecutive grounded

Output: for each (classes, L, (i,j)) the realised-pattern set, its size, the firing
count, and the excluded patterns.
"""

import sys
from itertools import permutations as iperm
from collections import defaultdict

sys.path.insert(0, "/home/user/erdos/attempts/route-R13-twopoint")
from r13enum import gen_avoiders, posarray, records, grounded  # noqa: E402

PATS3 = list(iperm(range(3)))
PATS4 = list(iperm(range(4)))


def rank_pattern(vals):
    order = sorted(range(len(vals)), key=lambda i: vals[i])
    r = [0] * len(vals)
    for k, i in enumerate(order):
        r[i] = k
    return tuple(r)


def index_pairs(L):
    return [(i, j) for i in range(L) for j in range(i + 1, L)]


def run(N, verbose=True):
    realised = defaultdict(set)   # (cls, L, (i,j)) -> set of patterns
    fires = defaultdict(int)

    def handle(perm):
        pos = posarray(perm)
        R = records(pos, N)
        G = grounded(pos, N)
        Rset, Gset = set(R), set(G)
        Rcons = set(zip(R, R[1:]))
        Gcons = set(zip(G, G[1:]))
        A = list(range(1, N + 1))

        classes = {
            "RR": [(p, q) for p in R for q in R if p < q],
            "RG": [(p, q) for p in R for q in G if p < q],
            "GR": [(p, q) for p in G for q in R if p < q],
            "GG": [(p, q) for p in G for q in G if p < q],
            "RA": [(p, q) for p in R for q in A if p < q],
            "AG": [(p, q) for p in A for q in G if p < q],
            "AA": [(p, q) for p in A for q in A if p < q],
            "RcRc": sorted(Rcons),
            "GcGc": sorted(Gcons),
        }
        for cls, pairs in classes.items():
            for (p, q) in pairs:
                D = q - p
                for L in (3, 4):
                    for (i, j) in index_pairs(L):
                        gap = j - i
                        if D % gap:
                            continue
                        d = D // gap
                        x = p - i * d
                        if x < 1:
                            continue
                        top = x + (L - 1) * d
                        if top > N:
                            continue
                        pat = rank_pattern([pos[x + t * d] for t in range(L)])
                        key = (cls, L, i, j)
                        realised[key].add(pat)
                        fires[key] += 1
        _ = (Rset, Gset)

    gen_avoiders(N, handle)
    return realised, fires


if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 9
    realised, fires = run(N)
    print(f"=== N = {N} ===")
    for key in sorted(realised):
        cls, L, i, j = key
        allp = set(PATS3 if L == 3 else PATS4)
        miss = sorted(allp - realised[key])
        print(f"{cls:5s} L={L} idx=({i},{j})  fires={fires[key]:9d} "
              f"realised={len(realised[key]):2d}/{len(allp)}  excluded={miss}")
