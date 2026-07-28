"""hand.py -- hand-designed candidate delays t, tested against condition (ii) and tameness.

Every candidate is checked with cond2 (three cross-validated implementations) and, when it
survives (ii), with the tameness report.  Output is the FAILURE LEDGER: the exact killing
4-AP for each candidate that dies.
"""
import sys
sys.path.insert(0, '/home/user/erdos/attempts/route-R23-refute')
from cond2 import blk, satisfies_ii, first_violation, tame_report, worst_tame


def v2(n):
    if n == 0:
        return 60
    k = 0
    while n % 2 == 0:
        n //= 2
        k += 1
    return k


def vp(n, p):
    if n == 0:
        return 60
    k = 0
    while n % p == 0:
        n //= p
        k += 1
    return k


# ---------------------------------------------------------------- candidate families
def make(name, f, N):
    t = [0] * (N + 1)
    for v in range(1, N + 1):
        t[v] = f(v)
    return name, t


def candidates(N, b):
    C = []
    C.append(make("v2(v)  [baseline, CORE R20-1a]", lambda v: v2(v), N))
    C.append(make("v2(v+1)", lambda v: v2(v + 1), N))
    C.append(make("v3(v)", lambda v: vp(v, 3), N))
    C.append(make("v5(v)", lambda v: vp(v, 5), N))
    C.append(make("1_{odd}", lambda v: v % 2, N))
    # block-shifted valuation: t(v) = v2(v + s_{j(v)})
    for tag, s in [("s_k=k", lambda k: k), ("s_k=2^k", lambda k: 2 ** k),
                   ("s_k=k^2", lambda k: k * k), ("s_k=3^k", lambda k: 3 ** k),
                   ("s_k=b^k(block start)", None)]:
        if s is None:
            C.append(make(f"v2(v - b^j(v)) [{tag}]",
                          lambda v: v2(v - b ** blk(v, b)), N))
        else:
            C.append(make(f"v2(v + s_j(v)) [{tag}]",
                          lambda v, s=s: v2(v + s(blk(v, b))), N))
    # capped valuation
    C.append(make("min(v2(v),1)", lambda v: min(v2(v), 1), N))
    C.append(make("min(v2(v),2)", lambda v: min(v2(v), 2), N))
    # 'MID' family of route R21 : digits h..h+k-1 of v (base 2) are zero
    for h in (1, 2, 3):
        for w in (1, 2):
            C.append(make(f"MID(h={h},w={w}) : t=0 iff bits {h}..{h+w-1} of v are 0",
                          lambda v, h=h, w=w: 0 if ((v >> h) & ((1 << w) - 1)) == 0 else 1, N))
    # interval-in-block designs
    C.append(make("t=1 iff v >= 2*b^j(v)  (top of block)",
                  lambda v: 1 if v >= 2 * b ** blk(v, b) else 0, N))
    C.append(make("t=1 iff v < 2*b^j(v)  (bottom of block)",
                  lambda v: 1 if v < 2 * b ** blk(v, b) else 0, N))
    # Sturmian (already refuted in CORE Remark 32b; kept as a control)
    F = (10946, 17711)  # golden-ratio convergent 17711/10946
    C.append(make("Sturmian beta=1/2 (control, expected FAIL)",
                  lambda v: 1 if (v * F[0]) % F[1] * 2 < F[1] else 0, N))
    # Thue-Morse
    C.append(make("Thue-Morse t(v)=popcount(v) mod 2", lambda v: bin(v).count('1') % 2, N))
    C.append(make("v2 of Thue-Morse-shifted?  v2(v ^ 1)", lambda v: v2(v ^ 1), N))
    return C


def run(N=4000, b=3, Q=12):
    print(f"=== hand candidates, N={N}, b={b} ===")
    print(f"{'candidate':52s} {'(ii)?':6s} {'first violation / worst tame AP'}")
    for name, t in candidates(N, b):
        fv = first_violation(t, N, b)
        if fv:
            x, d, orient, cs = fv
            print(f"{name:52s} {'FAIL':6s} x={x} d={d} {orient} vals="
                  f"{[x + i * d for i in range(4)]} classes={cs}")
        else:
            rows = tame_report(t, N, b, Q=Q)
            w = worst_tame(rows)
            ntame = sum(1 for r in rows if r['ndesc_tail'] == 0)
            print(f"{name:52s} {'OK':6s} tame APs (q<=%d, no tail c-descent): %d/%d ; "
                  "worst: q=%d r=%d maxrun_tail=%d ndesc_tail=%d tconst=%s"
                  % (Q, ntame, len(rows), w['q'], w['r'], w['maxrun_tail'],
                     w['ndesc_tail'], w['tconst_tail']))


if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 4000
    b = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    run(N, b)
