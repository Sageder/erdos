"""classlemma.py — machine verification of Lemma R20-1 (the class-monotonicity lemma).

Lemma R20-1.  Let b >= 3, let rho : Z_{>=0} -> Z_{>=0} be STRICTLY increasing, put
    j(v) = floor(log_b v),   c(v) = j(v) + rho(v_2(v)).
Then for every 4-AP (x, x+d, x+2d, x+3d) (x,d >= 1) the class sequence
    (c(x), c(x+d), c(x+2d), c(x+3d))
is neither strictly increasing nor strictly decreasing.

Consequence: in the ordering "classes in increasing index order, arbitrary order inside a
class", NO monotone 4-AP is forced by the coarse structure alone; every monotone 4-AP must
contain an adjacent pair lying in a COMMON class, and is killed as soon as one such pair is
inverted (increasing orientation) resp. kept (decreasing orientation).

This script (a) verifies the lemma exhaustively for x+3d <= LIMIT over several (b, rho),
(b) verifies the failure of the lemma when rho is only weakly increasing (sharpness),
(c) reports class sizes / the induced displacement profile.
"""
import sys, math

def v2(n):
    return (n & -n).bit_length() - 1

def logb(v, b):
    j = 0
    p = b
    while p <= v:
        p *= b
        j += 1
    return j

def make_c(b, rho):
    return lambda v: logb(v, b) + rho(v2(v))

def check(b, rho, LIMIT, label):
    c = make_c(b, rho)
    C = [0] * (LIMIT + 1)
    for v in range(1, LIMIT + 1):
        C[v] = c(v)
    bad = []
    for d in range(1, LIMIT // 3 + 1):
        for x in range(1, LIMIT - 3 * d + 1):
            a, b1, b2, b3 = C[x], C[x + d], C[x + 2 * d], C[x + 3 * d]
            if a < b1 < b2 < b3 or a > b1 > b2 > b3:
                bad.append((x, d, (a, b1, b2, b3)))
                if len(bad) > 5:
                    return bad
    return bad

if __name__ == "__main__":
    LIMIT = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
    tests = [
        ("b=3, rho(a)=a", 3, lambda a: a),
        ("b=4, rho(a)=a", 4, lambda a: a),
        ("b=5, rho(a)=a", 5, lambda a: a),
        ("b=3, rho(a)=2a", 3, lambda a: 2 * a),
        ("b=3, rho(a)=a+a//2", 3, lambda a: a + a // 2),
        # sharpness: b = 2 violates the block-gap lemma
        ("b=2, rho(a)=a  (EXPECTED FAIL: L2 needs b>=3)", 2, lambda a: a),
        # sharpness: weakly increasing rho
        ("b=3, rho=floor(a/2) (EXPECTED FAIL: rho not strict)", 3, lambda a: a // 2),
        ("b=3, rho=0 (contiguous blocks; EXPECTED OK, no delay)", 3, lambda a: 0),
    ]
    for label, b, rho in tests:
        bad = check(b, rho, LIMIT, label)
        if bad:
            print(f"{label}: FAILS, e.g. " + "; ".join(
                f"x={x},d={d},classes={cs}" for x, d, cs in bad[:3]))
        else:
            print(f"{label}: no strictly monotone class-sequence for x+3d <= {LIMIT}  OK")
    # profile of the b=3, rho(a)=a scheme
    b, rho = 3, (lambda a: a)
    c = make_c(b, rho)
    M = 200000
    from collections import Counter
    cnt = Counter(c(v) for v in range(1, M + 1))
    cum = {}
    s = 0
    for k in sorted(cnt):
        s += cnt[k]
        cum[k] = s
    print("\nclass sizes (b=3, rho(a)=a), values <= %d:" % M)
    for k in sorted(cnt)[:14]:
        print(f"   class {k}: size {cnt[k]}  cumulative {cum[k]}")
    worst = max(((cum[c(v)] / v, v) for v in range(1, M + 1)))
    print(f"max_v (cumulative class end)/v = {worst[0]:.1f} at v={worst[1]} "
          f"(v_2={v2(worst[1])})")
