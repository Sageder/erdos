#!/usr/bin/env python3
"""
(A) The (r, cap) envelope: max cap at fixed r, min r at fixed cap.
    A family with r bounded and cap -> infinity would PROVE Erdos 289 outright.
(B) The realised (delta r, delta cap) of local swap moves, and whether a
    (0,+1) move exists, i.e. capacity gain at no run-count cost.
(C) Long runs: where do they sit, how long can they be, what blocks them.
"""
import sys
from fractions import Fraction
from collections import Counter, defaultdict

sys.path.insert(0, "/home/user/erdos/attempts/wf-mining")
from stats import load, runs_of, stat
from mult import factor

S = load()
rows = [stat(U) for U in S]

print("=== (A) envelope: for each run count r, the max capacity attained ===")
maxcap = {}
argm = {}
for U, st in zip(S, rows):
    r = st["r"]
    if r not in maxcap or st["cap"] > maxcap[r]:
        maxcap[r] = st["cap"]
        argm[r] = (st["T"], st["N"], st["m"], st["L"])
print("   r  maxcap  cap-r   (T,N,|U|)")
for r in sorted(maxcap):
    t = argm[r]
    print("  %3d %6d %6d   (T=%d,N=%d,|U|=%d)  runs=%s" % (r, maxcap[r], maxcap[r] - r, t[0], t[1], t[2],
                                                          sorted(t[3], reverse=True)[:6]))

print("\n=== (B) local moves: (delta r, delta cap) achieved by small swaps ===")
FAR = [(U, st) for U, st in zip(S, rows)]
sets = [frozenset(U) for U, _ in FAR]
byT = defaultdict(list)
for i, (U, st) in enumerate(FAR):
    byT[st["T"]].append(i)
mv = Counter()
ex = {}
for T, idxs in byT.items():
    if len(idxs) > 900:
        idxs = idxs[:900]
    for a in range(len(idxs)):
        for b in range(len(idxs)):
            if a == b:
                continue
            i, j = idxs[a], idxs[b]
            X = sets[i] - sets[j]
            Y = sets[j] - sets[i]
            if not (1 <= len(X) + len(Y) <= 6):
                continue
            d = (FAR[j][1]["r"] - FAR[i][1]["r"], FAR[j][1]["cap"] - FAR[i][1]["cap"])
            mv[d] += 1
            if d not in ex:
                ex[d] = (tuple(sorted(X)), tuple(sorted(Y)), FAR[i][0], FAR[j][0])
print("   (dr, dcap) : count")
for d in sorted(mv):
    print("     %-10s : %d" % (str(d), mv[d]))
print("\n   witnesses for the capacity-positive, run-count-nonincreasing moves:")
for d in sorted(mv):
    if d[1] > 0 and d[0] <= 0:
        X, Y, U, V = ex[d]
        print("     dr=%+d dcap=%+d :  remove %s  insert %s" % (d[0], d[1], X, Y))
        print("        host U = %s" % (U,))
        print("        gives V = %s" % (V,))

print("\n=== (C) long runs ===")
longest = Counter()
where = defaultdict(list)
for U, st in zip(S, rows):
    for run in st["runs"]:
        L = len(run)
        longest[L] += 1
        if L >= 8:
            where[L].append((run[0], run[-1], st["T"], st["N"]))
print("   run length histogram:", dict(sorted(longest.items())))
for L in sorted(where, reverse=True)[:6]:
    seen = sorted(set((a, b) for a, b, _, _ in where[L]))
    print("   L=%2d : %d occurrences, distinct intervals %s" % (L, len(where[L]), seen[:10]))
    for a, b in seen[:4]:
        pr = [n for n in range(a, b + 1) if len(factor(n)) == 1 and list(factor(n).values())[0] == 1]
        print("        [%d,%d] : primes inside = %s ; position a/N ~ %s" % (a, b, pr, "-"))
