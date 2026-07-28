"""verify_twopoint.py — exhaustive machine hunt for counterexamples to the candidate
TWO-POINT laws of route R13, over ALL monotone-4-AP-free permutations of [1..N], N<=10.

Each law is stated with ALL quantifiers explicit and with the exact side conditions
that make its finite shadow faithful (every value the law mentions must be <= N, and
every value the PROOF needs must be <= N -- these are different, and the difference is
where two candidates die).

Anchor classes on a board sigma of [1..N]:
   record  w : pos[w] < pos[v] for all v in (w, N]        (relaxation, see r13enum.py)
   ground  g : pos[g] > pos[v] for all v in [1, g)        (exact)

Reported per law: #firings (non-vacuity certificate) and #counterexamples.
A law with 0 counterexamples and a large firing count SURVIVES the hunt; a law with a
counterexample is DEAD in its local form and the witness is printed.
"""

import sys
from collections import defaultdict

sys.path.insert(0, "/home/user/erdos/attempts/route-R13-twopoint")
from r13enum import gen_avoiders, posarray, records, grounded  # noqa: E402

fire = defaultdict(int)
fail = defaultdict(int)
wit = {}


def rep(name, cond, board, info):
    fire[name] += 1
    if not cond:
        fail[name] += 1
        if name not in wit:
            wit[name] = (board, info)


def handle(perm):
    N = len(perm)
    pos = posarray(perm)
    R = records(pos, N)
    G = grounded(pos, N)

    # ---------- (a) both points records ----------
    for i, p in enumerate(R):
        for q in R[i + 1:]:
            D = q - p
            # TP1: (p,q,2q-p) is an increasing 3-AP.  Needs 2q-p <= N.
            if 2 * q - p <= N:
                rep("TP1 rec-rec ascent  (p,q,2q-p) increasing",
                    pos[p] < pos[q] < pos[2 * q - p], perm, (p, q))
            # TP1': L1 consequence pos(3q-2p) < pos(2q-p).  Needs 3q-2p <= N.
            if 3 * q - 2 * p <= N:
                rep("TP1' rec-rec L1     pos(3q-2p) < pos(2q-p)",
                    pos[3 * q - 2 * p] < pos[2 * q - p], perm, (p, q))
            # TP2 (CRM): 2 | (q-p) and the PROOF needs q + (q-p)/2 <= N.
            if D % 2 == 0:
                m = p + D // 2
                if q + D // 2 <= N:
                    rep("TP2 rec-rec midpoint  pos((p+q)/2) > pos(q)   [proof needs (3q-p)/2<=N]",
                        pos[m] > pos[q], perm, (p, q))
                # same law WITHOUT the proof-side condition (only m,q <= N):
                rep("TP2w rec-rec midpoint  pos((p+q)/2) > pos(q)   [no proof-side cond]",
                    pos[m] > pos[q], perm, (p, q))

    # ---------- (b) one record and one grounded ----------
    for w in R:
        for g in G:
            if g <= w:
                continue
            D = g - w
            # TP3 sandwich
            for v in range(w + 1, g):
                rep("TP3 rec-gnd sandwich  pos(w)<pos(v)<pos(g) for all v in (w,g)",
                    pos[w] < pos[v] < pos[g], perm, (w, g, v))
            # TP4 halving: (w,(w+g)/2,g) increasing
            if D % 2 == 0:
                rep("TP4 rec-gnd halving   (w,(w+g)/2,g) is an increasing 3-AP",
                    pos[w] < pos[w + D // 2] < pos[g], perm, (w, g))
                # its L1 consequence, needs g + D/2 <= N
                if g + D // 2 <= N:
                    rep("TP4' rec-gnd halving L1  pos(g+(g-w)/2) < pos(g)",
                        pos[g + D // 2] < pos[g], perm, (w, g))
                # its L2 consequence, needs w - D/2 >= 1
                if w - D // 2 >= 1:
                    rep("TP4'' rec-gnd halving L2 pos(w-(g-w)/2) > pos(w)",
                        pos[w - D // 2] > pos[w], perm, (w, g))
            # TP5 thirds: unique pattern pos(w)<pos(w+2d)<pos(w+d)<pos(g)
            if D % 3 == 0:
                d = D // 3
                rep("TP5 rec-gnd thirds    pos(w)<pos(w+2d)<pos(w+d)<pos(g), d=(g-w)/3",
                    pos[w] < pos[w + 2 * d] < pos[w + d] < pos[g], perm, (w, g))

    # ---------- (c) two consecutive records ----------
    for p, q in zip(R, R[1:]):
        D = q - p
        if D % 2 == 0:
            m = p + D // 2
            rep("TP2c consec-rec midpoint  pos((p+q)/2) > pos(q)  [no proof-side cond]",
                pos[m] > pos[q], perm, (p, q))
        # no record strictly between: every v in (p,q) is preceded by a larger value
        for v in range(p + 1, q):
            rep("TPc-nr consec-rec  every v in (p,q) has a larger predecessor",
                any(pos[u] < pos[v] for u in range(v + 1, N + 1)), perm, (p, q, v))

    # ---------- two grounded ----------
    for i, g in enumerate(G):
        for h in G[i + 1:]:
            E = h - g
            if 2 * g - h >= 1:
                rep("TP6 gnd-gnd ascent  (2g-h,g,h) is an increasing 3-AP",
                    pos[2 * g - h] < pos[g] < pos[h], perm, (g, h))
                if 2 * h - g <= N:
                    rep("TP6' gnd-gnd L1     pos(2h-g) < pos(h)",
                        pos[2 * h - g] < pos[h], perm, (g, h))
            if E % 2 == 0 and g - E // 2 >= 1:
                rep("TP7 gnd-gnd midpoint  pos((g+h)/2) < pos(g)  [needs g-(h-g)/2 >= 1]",
                    pos[g + E // 2] < pos[g], perm, (g, h))
            if E % 2 == 0:
                rep("TP7w gnd-gnd midpoint  pos((g+h)/2) < pos(g)  [no side cond]",
                    pos[g + E // 2] < pos[g], perm, (g, h))

    # ---------- one-point controls (known theorems) ----------
    for w in R:  # F1 = Theorem 44: no increasing 3-AP ends at a record
        d = 1
        while w - 2 * d >= 1:
            if w + d <= N:          # PROOF-side condition (the 4th AP term must be on the board)
                rep("F1 (Thm44) no increasing 3-AP ends at a record [proof needs w+d<=N]",
                    not (pos[w - 2 * d] < pos[w - d] < pos[w]), perm, (w, d))
            rep("F1w (Thm44) same, WITHOUT the proof-side condition",
                not (pos[w - 2 * d] < pos[w - d] < pos[w]), perm, (w, d))
            d += 1
    for g in G:  # F2 (dual): no increasing 3-AP starts at a grounded value with step < g
        d = 1
        while d < g and g + 2 * d <= N:
            rep("F2 (dual) no increasing 3-AP (g,g+d,g+2d) with g grounded and d < g",
                not (pos[g] < pos[g + d] < pos[g + 2 * d]), perm, (g, d))
            d += 1

    # ---------- NF-RR reduction: restrict to the AP through two records ----------
    for i, p in enumerate(R):
        for q in R[i + 1:]:
            D = q - p
            P = list(range(p, N + 1, D))
            if len(P) < 3:
                continue
            order = sorted(P, key=lambda v: pos[v])
            rep("NF-RR reduction: in a|_{p+D N_0} the first two values are p, q",
                order[0] == p and order[1] == q, perm, (p, q))

    # ---------- HYPOTHESIS-NECESSITY CONTROLS ----------
    # (does the law survive if one anchor class is weakened to "arbitrary value"?)
    for w in R:
        for u in range(w + 1, N + 1):
            if (u - w) % 2 == 0:
                rep("CTRL-1 rec + ARBITRARY u: (w,(w+u)/2,u) increasing  [TP4 with g -> any]",
                    pos[w] < pos[w + (u - w) // 2] < pos[u], perm, (w, u))
            if (u - w) % 3 == 0:
                d = (u - w) // 3
                rep("CTRL-2 rec + ARBITRARY u: pos(w+2d)<pos(w+d), d=(u-w)/3  [TP5 with g -> any]",
                    pos[w + 2 * d] < pos[w + d], perm, (w, u))
    for g in G:
        for u in range(1, g):
            if 2 * u - g >= 1 and (g - u) >= 1:
                rep("CTRL-3 ARBITRARY u + gnd g: (2u-g,u,g) increasing  [TP6 with the lower g -> any]",
                    pos[2 * u - g] < pos[u] < pos[g], perm, (u, g))
    for i, p in enumerate(R):
        for q in R[i + 1:]:
            D = q - p
            for k in range(3, 7):
                if D % k == 0:
                    d = D // k
                    rep(f"CTRL-4 rec-rec k={k} section: pos(q-d) > pos(q), d=(q-p)/{k}",
                        pos[q - d] > pos[q], perm, (p, q))

    # ---------- k-section of a record-grounded sandwich ----------
    for w in R:
        for g in G:
            if g <= w:
                continue
            D = g - w
            if D % 4 == 0:
                d = D // 4
                if g + 2 * d <= N:
                    rep("TP8 rec-gnd quarters: pos(g+2d) < pos(g), d=(g-w)/4",
                        pos[g + 2 * d] < pos[g], perm, (w, g))
                rep("TP8b rec-gnd quarters: NOT pos(w+d)<pos(w+2d)<pos(w+3d)",
                    not (pos[w + d] < pos[w + 2 * d] < pos[w + 3 * d]), perm, (w, g))

    # ---------- (d) staircase-flavoured control: two tops of increasing 3-APs ----------
    tops = []
    for x in range(1, N + 1):
        d = 1
        while x + 2 * d <= N:
            if pos[x] < pos[x + d] < pos[x + 2 * d]:
                tops.append(x + 2 * d)
            d += 1
    tops = sorted(set(tops))
    for i, p in enumerate(tops):
        for q in tops[i + 1:]:
            if 2 * q - p <= N:
                rep("TPd two 3-AP tops: (p,q,2q-p) increasing  [CANDIDATE]",
                    pos[p] < pos[q] < pos[2 * q - p], perm, (p, q))
            if 2 * q - p <= N:
                rep("TPd' two 3-AP tops: pos(q) < pos(2q-p)  [CANDIDATE]",
                    pos[q] < pos[2 * q - p], perm, (p, q))


if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 9
    gen_avoiders(N, handle)
    print(f"=== exhaustive over ALL monotone-4-AP-free permutations of [1..{N}] ===")
    for name in sorted(fire):
        status = "SURVIVES" if fail[name] == 0 else "DEAD"
        extra = ""
        if fail[name]:
            b, info = wit[name]
            extra = f"   witness perm={b} at {info}"
        print(f"[{status:8s}] fires={fire[name]:10d} fails={fail[name]:9d}  {name}{extra}")
