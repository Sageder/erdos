"""xval.py — cross-validation of decide.py against the exact integer checker,
then the exhaustive annulus scan.

Theorem used: decide(tau)=None  =>  condition (ii) holds for ALL integers.
So a disagreement "decide clean but integer violated" is FATAL and must not occur.
The reverse ("decide finds a violation, integers clean up to N") is expected whenever
the violating region only contains integer points at scales beyond N.
"""
import sys, random
from fractions import Fraction as F
sys.path.insert(0, '/home/user/erdos/attempts/route-R22-prove-a')
from decide import decide, annulus                                    # noqa: E402
from local import jtable                                              # noqa: E402


def tau_eval(tau, b, v, J):
    """t(v) = tau(v / b^{J[v]}), exact."""
    P = F(b) ** J[v]
    val = tau[0][1]
    for (s, x) in tau:
        if F(v) >= F(s) * P:
            val = x
        else:
            break
    return val


def int_first_violation(tau, b, N, J):
    t = [0] * (N + 1)
    for v in range(1, N + 1):
        t[v] = tau_eval(tau, b, v, J)
    for d in range(1, (N - 1) // 3 + 1):
        for x in range(1, N - 3 * d + 1):
            a, bb, cc, dd = x, x + d, x + 2 * d, x + 3 * d
            c0 = J[a] + t[a]; c1 = J[bb] + t[bb]
            c2 = J[cc] + t[cc]; c3 = J[dd] + t[dd]
            if c0 < c1 < c2 < c3:
                return ('inc', x, d, (c0, c1, c2, c3))
            if c0 > c1 > c2 > c3:
                return ('dec', x, d, (c0, c1, c2, c3))
    return None


def random_tau(b, rng, T=2, npieces=3, den=6):
    pts = sorted({F(rng.randint(den + 1, den * b - 1), den) for _ in range(npieces)})
    tau = [(F(1), rng.randint(0, T))]
    for p in pts:
        tau.append((p, rng.randint(0, T)))
    return tau


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else 'xval'
    if mode == 'xval':
        b = 3
        N = int(sys.argv[2]) if len(sys.argv) > 2 else 6000
        J = jtable(N, b)
        rng = random.Random(4242)
        fatal = 0
        agree = 0
        conly = 0
        for it in range(120):
            tau = random_tau(b, rng)
            w = decide(tau, b)
            iv = int_first_violation(tau, b, N, J)
            if w is None and iv is not None:
                fatal += 1
                print("FATAL:", tau, iv)
            elif (w is None) == (iv is None):
                agree += 1
            else:
                conly += 1
        print(f"b=3 N={N}: agree {agree}, decide-only-violation {conly}, FATAL {fatal}")
    elif mode == 'annuli':
        for b in (3, 4, 5, 6, 8):
            good = []
            tot = 0
            dens = [1, 2, 3, 4, 5, 6, 7, 8]
            seen = set()
            for da in dens:
                for na in range(da, b * da):
                    A = F(na, da)
                    if not (1 <= A < b):
                        continue
                    for db in dens:
                        for nb in range(db, b * db + 1):
                            B = F(nb, db)
                            if not (A < B <= b):
                                continue
                            if (A, B) in seen:
                                continue
                            seen.add((A, B))
                            if A == 1 and B == b:
                                continue          # tau constant
                            tot += 1
                            if decide(annulus(A, B, b), b) is None:
                                good.append((A, B))
            print(f"b={b}: {len(good)}/{tot} annuli 1<=A<B<=b satisfy (CONT)")
            for g in good[:30]:
                print("     A =", g[0], "B =", g[1],
                      " interior-descent(non-tame)?", g[1] < b)
