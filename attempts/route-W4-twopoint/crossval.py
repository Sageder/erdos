"""crossval.py -- independent Python re-implementation of the W-rule checks and the
counting corollaries C1-C3, cross-validated against experiments/apcheck.py.

Two independent enumerations are used:
  (i) the literal N!-filter with apcheck.has_monotone_kap_brute (ground truth, N<=8),
 (ii) route-R5's validated DFS enumerator enum_avoiders.gen_avoiders (N<=10).
Both must give identical firing/violation counts.
"""
import sys
from itertools import permutations
sys.path.insert(0, "/home/user/erdos/experiments")
sys.path.insert(0, "/home/user/erdos/attempts/route-R5")
from apcheck import has_monotone_kap_brute, has_monotone_kap_pos
import enum_avoiders

RULES = ["W1", "W2", "W2a", "W2b", "W3", "W4", "W5", "W6", "W6b", "W7",
         "C1", "C2", "C3"]


def spines(perm, N):
    pos = [0] * (N + 2)
    for i, v in enumerate(perm):
        pos[v] = i + 1
    rec, gnd = set(), set()
    mx = 0
    for v in perm:
        if v > mx:
            rec.add(v)
            mx = v
    mp = 0
    for v in range(1, N + 1):
        if pos[v] > mp:
            gnd.add(v)
            mp = pos[v]
    return pos, rec, gnd


def check(perm, N, fire, viol):
    pos, L, G = spines(perm, N)

    def hit(r, ok):
        fire[r] += 1
        if not ok:
            viol[r] += 1
    for w in sorted(L):
        for g in sorted(G):
            if g <= w:
                continue
            D = g - w
            if D % 3 == 0:
                s = D // 3
                hit("W1", pos[w + 2 * s] < pos[w + s])
            if D % 2 == 0:
                s = D // 2
                hit("W2", pos[w] < pos[w + s] < pos[g])
                if g + s <= N:
                    hit("W2a", pos[g + s] < pos[g])
                if w - s >= 1:
                    hit("W2b", pos[w] < pos[w - s])
    for g in sorted(G):
        for g2 in sorted(G):
            if g2 <= g:
                continue
            D = g2 - g
            if D % 2 == 0 and g - D // 2 >= 1:
                hit("W3", pos[g + D // 2] < pos[g])
            if g2 < 2 * g and 2 * g2 - g <= N:
                hit("W5", pos[2 * g2 - g] < pos[g2])
    for w in sorted(L):
        for w2 in sorted(L):
            if w2 <= w:
                continue
            D = w2 - w
            if D % 2 == 0 and w2 + D // 2 <= N:
                hit("W4", pos[w2] < pos[w + D // 2])
            if 3 * w2 - 2 * w <= N:
                hit("W6", pos[3 * w2 - 2 * w] < pos[2 * w2 - w])
            if 2 * w - w2 >= 1 and 2 * w2 - w <= N:
                hit("W6b", pos[w] < pos[2 * w - w2])
    for g in sorted(G):
        for w in sorted(L):
            if g < w < 2 * g and 2 * w - g <= N:
                hit("W7", pos[w] < pos[g])
    # counting corollaries (only where the board is large enough for the rule used)
    for g in sorted(G):
        recs = [w for w in L if g < w < 2 * g and 2 * w - g <= N]
        hit("C1", pos[g] >= g + len(recs))
        gs = [g2 for g2 in G if g < g2 < 3 * g and (g2 - g) % 2 == 0 and g - (g2 - g) // 2 >= 1]
        hit("C3", pos[g] >= g + len(gs))
    for w2 in sorted(L):
        ws = [w for w in L if w < w2 and (w2 - w) % 2 == 0 and w2 + (w2 - w) // 2 <= N]
        hit("C2", pos[w2] <= w2 - len(ws))


def run(N, brute):
    fire = {r: 0 for r in RULES}
    viol = {r: 0 for r in RULES}
    nb = 0
    if brute:
        for p in permutations(range(1, N + 1)):
            if has_monotone_kap_brute(p, 4):
                continue
            nb += 1
            check(p, N, fire, viol)
    else:
        boards = []
        enum_avoiders.gen_avoiders(N, boards.append)
        for p in boards:
            assert not has_monotone_kap_pos(p, 4)
            nb += 1
            check(p, N, fire, viol)
    return nb, fire, viol


if __name__ == '__main__':
    for N in (6, 7, 8):
        nb1, f1, v1 = run(N, True)
        nb2, f2, v2 = run(N, False)
        assert (nb1, f1, v1) == (nb2, f2, v2), (N, nb1, nb2, f1, f2)
        print(f"N={N} boards={nb1} (brute==DFS)  " +
              "  ".join(f"{r}:{f1[r]}/{v1[r]}" for r in RULES))
    for N in (9, 10):
        nb, f, v = run(N, False)
        print(f"N={N} boards={nb}  " + "  ".join(f"{r}:{f[r]}/{v[r]}" for r in RULES))
    print("format rule:fires/violations")
