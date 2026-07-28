"""local.py — exact local structure of condition (ii) for c = j_b + t.

Conventions (PROBLEM.md / CORE.md):
  b >= 3 integer, j(v) = floor(log_b v) = largest j with b^j <= v  (EXACT integer arithmetic).
  t : [1..N] -> Z>=0,  c = j + t.
  (ii): for every 4-AP (x, x+d, x+2d, x+3d) with x>=1, d>=1, the sequence
        (c0,c1,c2,c3) is neither strictly increasing nor strictly decreasing.

Everything here is exact integer arithmetic; no floats.
"""


def jblk(v, b):
    """floor(log_b v), exact."""
    assert v >= 1 and b >= 2
    j, p = 0, 1
    while p * b <= v:
        p *= b
        j += 1
    return j


def jtable(N, b):
    """J[v] = jblk(v,b) for v in 0..N (J[0] unused)."""
    J = [0] * (N + 1)
    j, nxt = 0, b
    for v in range(1, N + 1):
        while v >= nxt:
            j += 1
            nxt *= b
        J[v] = j
    return J


def four_aps(N):
    for d in range(1, (N - 1) // 3 + 1):
        for x in range(1, N - 3 * d + 1):
            yield x, d


def check_ii(t, b, N, J=None):
    """t is a 0-indexed-by-value list with t[v] defined for 1..N.
    Returns None if (ii) holds on [1..N], else the first violation."""
    if J is None:
        J = jtable(N, b)
    for x, d in four_aps(N):
        v = (x, x + d, x + 2 * d, x + 3 * d)
        c = tuple(J[u] + t[u] for u in v)
        if c[0] < c[1] < c[2] < c[3]:
            return ('inc', x, d, v, c)
        if c[0] > c[1] > c[2] > c[3]:
            return ('dec', x, d, v, c)
    return None


def all_ii_violations(t, b, N, J=None, cap=20):
    if J is None:
        J = jtable(N, b)
    out = []
    for x, d in four_aps(N):
        v = (x, x + d, x + 2 * d, x + 3 * d)
        c = tuple(J[u] + t[u] for u in v)
        if c[0] < c[1] < c[2] < c[3]:
            out.append(('inc', x, d, v, c))
        elif c[0] > c[1] > c[2] > c[3]:
            out.append(('dec', x, d, v, c))
        if len(out) >= cap:
            break
    return out


# ---------------------------------------------------------------- delta patterns ----
def delta_census(N, b):
    """Which (d0,d1,d2) block-increment patterns actually occur?  Confirms
    Lemma A: d1 + d2 <= 1 always, d0 unbounded."""
    from collections import Counter
    J = jtable(N, b)
    cnt = Counter()
    for x, d in four_aps(N):
        d0 = J[x + d] - J[x]
        d1 = J[x + 2 * d] - J[x + d]
        d2 = J[x + 3 * d] - J[x + 2 * d]
        cnt[(min(d0, 3), d1, d2)] += 1
    return cnt


if __name__ == "__main__":
    import sys
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    for b in (3, 4, 5, 10):
        cnt = delta_census(N, b)
        bad = [k for k in cnt if k[1] + k[2] > 1]
        print(f"b={b} N={N}: patterns (d0 capped at 3, d1, d2) -> count")
        for k in sorted(cnt):
            print("   ", k, cnt[k])
        print("   violations of d1+d2<=1:", bad)
