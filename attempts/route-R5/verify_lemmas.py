"""verify_lemmas.py — machine verification of the R5 structural lemmas on ALL
monotone-4-AP-free permutations of [1..N] (finite avoiders).

Rationale: any hypothetical infinite 4-AP-free permutation restricts (values 1..N in
position order) to a finite 4-AP-free permutation of [1..N].  Hence every lemma below,
being a FINITELY-STATED implication about a 4-AP-free permutation, must hold for all
finite avoiders; a finite counterexample would kill the lemma (and its proof).
Conversely, machine success here does NOT prove the lemmas — the proofs are in
lemmas_4apfree.md — it stress-tests them.

Conventions: perm[i] = value at position i+1; pos[v] = 0-based position of value v.
"inc(x,d)" = increasing monotone 3-AP: pos[x] < pos[x+d] < pos[x+2d].
"dec(x,d)" = decreasing monotone 3-AP: pos[x+2d] < pos[x+d] < pos[x]
             (values x+2d, x+d, x read in position order — values decreasing).

Lemmas checked (all under the standing hypothesis: perm is monotone-4-AP-free; every
side condition like x+3d <= N makes the statement finitely evaluable):

 L1  (up-block):    inc(x,d) & x+3d<=N  =>  pos[x+3d] < pos[x+2d]
 L2  (down-block):  inc(x,d) & x-d>=1   =>  pos[x-d]  > pos[x]
 L3a (dual up):     dec(x,d) & x+3d<=N  =>  pos[x+3d] > pos[x+2d]
 L3b (dual down):   dec(x,d) & x-d>=1   =>  pos[x-d]  < pos[x]
 L4a (no shifted abutting pair, inc):  x+3d<=N => NOT( inc(x,d) & inc(x+d,d) )
 L4b (no end-abutting pair, inc):      x+4d<=N => NOT( inc(x,d) & inc(x+2d,d) )
 L5  (top-anchor gap g=2, inc):        x+6d<=N => NOT( inc(x,d) & inc(x+2d,2d) )
 L6  (conditional cascade): inc(x,d) & x-d>=1 & x+3d<=N
        & pos[x-d]<pos[x+d] & pos[x+3d]>pos[x+d]
        =>  [ x+5d<=N => pos[x+5d]<pos[x+3d] ]  and  [ x-3d>=1 => pos[x-3d]>pos[x-d] ]
 L7  (2d-ladder):  inc(x,d) & x+6d<=N & pos[x+4d]>pos[x+2d]  =>  pos[x+6d]<pos[x+4d]
 L8  (no inc 2d-arrival): inc(x,d) & x-4d>=1 => NOT( pos[x-4d]<pos[x-2d]<pos[x] )
 L4b'(dec dual of L4b):  x+4d<=N => NOT( dec(x,d) & dec(x+2d,d) )
 L5' (dec dual of L5):   x+6d<=N => NOT( dec(x,d) & dec(x+2d,2d) )
 L7' (dec dual of L7): dec(x,d) & x+6d<=N & pos[x+4d]<pos[x+2d] => pos[x+6d]>pos[x+4d]
 L8' (dec dual of L8): dec(x,d) & x-4d>=1 => NOT( pos[x]<pos[x-2d]<pos[x-4d] )

Each lemma also gets a firing counter (number of instances where its hypothesis held)
to certify non-vacuity of the test.
"""

import sys
from collections import Counter
sys.path.insert(0, "/home/user/erdos/attempts/route-R5")
from enum_avoiders import gen_avoiders

FIRE = Counter()
FAIL = []


def check(perm):
    n = len(perm)
    pos = [0] * (n + 1)
    for i, v in enumerate(perm):
        pos[v] = i
    for d in range(1, (n - 1) // 2 + 1):
        for x in range(1, n - 2 * d + 1):
            p0, p1, p2 = pos[x], pos[x + d], pos[x + 2 * d]
            inc = p0 < p1 < p2
            dec = p0 > p1 > p2
            if not (inc or dec):
                continue
            if inc:
                if x + 3 * d <= n:
                    FIRE['L1'] += 1
                    if not pos[x + 3 * d] < p2:
                        FAIL.append(('L1', perm, x, d))
                    FIRE['L4a'] += 1
                    if p1 < p2 < pos[x + 3 * d]:  # inc(x+d,d) too
                        FAIL.append(('L4a', perm, x, d))
                if x - d >= 1:
                    FIRE['L2'] += 1
                    if not pos[x - d] > p0:
                        FAIL.append(('L2', perm, x, d))
                if x + 4 * d <= n:
                    FIRE['L4b'] += 1
                    if p2 < pos[x + 3 * d] < pos[x + 4 * d]:
                        FAIL.append(('L4b', perm, x, d))
                if x + 6 * d <= n:
                    FIRE['L5'] += 1
                    if p2 < pos[x + 4 * d] < pos[x + 6 * d]:
                        FAIL.append(('L5', perm, x, d))
                    if pos[x + 4 * d] > p2:
                        FIRE['L7'] += 1
                        if not pos[x + 6 * d] < pos[x + 4 * d]:
                            FAIL.append(('L7', perm, x, d))
                if x - d >= 1 and x + 3 * d <= n and \
                        pos[x - d] < p1 and pos[x + 3 * d] > p1:
                    FIRE['L6'] += 1
                    if x + 5 * d <= n and not pos[x + 5 * d] < pos[x + 3 * d]:
                        FAIL.append(('L6up', perm, x, d))
                    if x - 3 * d >= 1 and not pos[x - 3 * d] > pos[x - d]:
                        FAIL.append(('L6dn', perm, x, d))
                if x - 4 * d >= 1:
                    FIRE['L8'] += 1
                    if pos[x - 4 * d] < pos[x - 2 * d] < p0:
                        FAIL.append(('L8', perm, x, d))
            else:  # dec
                if x + 3 * d <= n:
                    FIRE['L3a'] += 1
                    if not pos[x + 3 * d] > p2:
                        FAIL.append(('L3a', perm, x, d))
                if x - d >= 1:
                    FIRE['L3b'] += 1
                    if not pos[x - d] < p0:
                        FAIL.append(('L3b', perm, x, d))
                if x + 4 * d <= n:
                    FIRE['L4bd'] += 1
                    if pos[x + 4 * d] < pos[x + 3 * d] < p2:
                        FAIL.append(("L4b'", perm, x, d))
                if x + 6 * d <= n:
                    FIRE['L5d'] += 1
                    if pos[x + 6 * d] < pos[x + 4 * d] < p2:
                        FAIL.append(("L5'", perm, x, d))
                    if pos[x + 4 * d] < p2:
                        FIRE['L7d'] += 1
                        if not pos[x + 6 * d] > pos[x + 4 * d]:
                            FAIL.append(("L7'", perm, x, d))
                if x - 4 * d >= 1:
                    FIRE['L8d'] += 1
                    if p0 < pos[x - 2 * d] < pos[x - 4 * d]:
                        FAIL.append(("L8'", perm, x, d))


if __name__ == "__main__":
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    for n in range(3, nmax + 1):
        cnt = [0]

        def cb(p):
            cnt[0] += 1
            check(p)

        gen_avoiders(n, cb)
        print(f"N={n}: {cnt[0]} avoiders checked, failures so far: {len(FAIL)}",
              flush=True)
    print("firing counts:", dict(sorted(FIRE.items())))
    if FAIL:
        print("FAILURES:")
        for f in FAIL[:20]:
            print(f)
    else:
        print(f"ALL LEMMAS PASS on all 4-AP-free permutations up to N={nmax}.")
