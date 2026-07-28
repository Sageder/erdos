"""Independent audit re-implementation (does NOT import route-R17 code except apcheck)."""
import sys
from itertools import permutations
sys.path.insert(0, '/home/user/erdos/experiments')
from apcheck import has_monotone_kap_pos


def pos_of(p):
    N = len(p)
    pos = [0] * (N + 2)
    for i, v in enumerate(p):
        pos[v] = i + 1
    return pos


def audit(N):
    tot = 0
    # R17.1
    rec_open_inside = 0     # record open at d with w+d <= N  -> must be 0
    rec_open_edge = 0       # record open at d with w+d > N   -> "artifact"
    rec_open_edge_boards = 0
    # R17.4 : w record, v prec w, d=w-v => 2w-v open at scale d, and (if in range) 3w-2v prec 2w-v
    r4_inst = 0
    r4_bad_open = 0
    r4_bad_force = 0
    # R17.5 : w record, w-d prec w, w+2d<=N => w+2d prec w+d
    r5_inst = 0
    r5_bad = 0
    # R17.6' anchored doubling
    r6_inst = 0
    r6_bad = 0
    # R17.3 : u open at d => u+d not open at d nor at d/2
    r3_inst = 0
    r3_bad = 0
    for p in permutations(range(1, N + 1)):
        if has_monotone_kap_pos(p, 4):
            continue
        tot += 1
        pos = pos_of(p)
        # records
        best = 0
        rec = []
        for v in p:
            if v > best:
                rec.append(v)
                best = v
        recs = set(rec)
        edgeflag = False
        for w in range(1, N + 1):
            for d in range(1, (w - 1) // 2 + 1):
                if pos[w - 2 * d] < pos[w - d] < pos[w]:
                    if w in recs:
                        if w + d <= N:
                            rec_open_inside += 1
                        else:
                            rec_open_edge += 1
                            edgeflag = True
                    # R17.3
                    if w + d <= N:
                        u2 = w + d
                        r3_inst += 1
                        # open at d?
                        if u2 - 2 * d >= 1 and pos[u2 - 2 * d] < pos[u2 - d] < pos[u2]:
                            r3_bad += 1
                        if d % 2 == 0:
                            f = d // 2
                            if u2 - 2 * f >= 1 and pos[u2 - 2 * f] < pos[u2 - f] < pos[u2]:
                                r3_bad += 1
        if edgeflag:
            rec_open_edge_boards += 1
        # R17.4
        for w in recs:
            for v in range(1, w):
                if pos[v] < pos[w]:
                    d = w - v
                    u = 2 * w - v
                    if u <= N:
                        r4_inst += 1
                        if not (pos[u - 2 * d] < pos[u - d] < pos[u]):
                            r4_bad_open += 1
                        if u + d <= N and not (pos[u + d] < pos[u]):
                            r4_bad_force += 1
        # R17.5
        for w in recs:
            for d in range(1, w):
                if w - d >= 1 and pos[w - d] < pos[w] and w + 2 * d <= N:
                    r5_inst += 1
                    if not (pos[w + 2 * d] < pos[w + d]):
                        r5_bad += 1
        # R17.6'
        for m in range(2, N):
            for d in range(1, m):
                # find max K with m-2^j d>=1, m+2^j d<=N, and anchored condition
                K = -1
                j = 0
                while True:
                    s = (2 ** j) * d
                    if m - s < 1 or m + s > N:
                        break
                    if pos[m - s] < pos[m] < pos[m + s]:
                        K = j
                        j += 1
                    else:
                        break
                if K >= 0:
                    r6_inst += 1
                    chain = [m + (2 ** j) * d for j in range(0, K + 2) if m + (2 ** j) * d <= N]
                    for i in range(len(chain) - 1):
                        if not pos[chain[i + 1]] < pos[chain[i]]:
                            r6_bad += 1
                    if len(chain) > pos[chain[0]]:
                        r6_bad += 1
    print(f"N={N} avoiders={tot}")
    print(f"  R17.1 records open with w+d<=N (must be 0): {rec_open_inside}"
          f" ; edge artifacts (w+d>N): {rec_open_edge} on {rec_open_edge_boards} boards")
    print(f"  R17.3 instances={r3_inst} violations={r3_bad}")
    print(f"  R17.4 instances={r4_inst} bad-open={r4_bad_open} bad-force={r4_bad_force}")
    print(f"  R17.5 instances={r5_inst} violations={r5_bad}")
    print(f"  R17.6' anchored runs={r6_inst} violations={r6_bad}", flush=True)
    return dict(tot=tot, edge=rec_open_edge, inside=rec_open_inside, r4=r4_inst, r5=r5_inst, r6=r6_inst)


if __name__ == "__main__":
    Nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 9
    T = dict(tot=0, edge=0, inside=0, r4=0, r5=0, r6=0)
    for N in range(4, Nmax + 1):
        r = audit(N)
        for k in T:
            T[k] += r[k]
    print("TOTALS N=4..%d:" % Nmax, T)
