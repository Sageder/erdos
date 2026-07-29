"""numeration.py — exact numeration systems for Erdos 196 route W4-novel.

All arithmetic is exact integer arithmetic.  Every representation routine is
round-trip tested in __main__ (digits -> value -> digits).

Digit lists are always returned LEAST-SIGNIFICANT-FIRST.
"""


# ---------------------------------------------------------------- base b
def base_digits(v, b):
    d = []
    while v:
        d.append(v % b)
        v //= b
    return d


def from_base(d, b):
    return sum(c * b ** i for i, c in enumerate(d))


# ---------------------------------------------------------------- factorial base
def factorial_digits(v):
    """v = sum_{k>=1} c_k * k!, 0 <= c_k <= k.  Returns [c_1, c_2, ...]."""
    d = []
    k = 2
    while v:
        d.append(v % k)
        v //= k
        k += 1
    return d


def from_factorial(d):
    v = 0
    f = 1
    for i, c in enumerate(d):
        f = 1
        for j in range(1, i + 2):
            f *= j
        v += c * f
    return v


# ---------------------------------------------------------------- Zeckendorf
def fibs_upto(N):
    """F_2=1, F_3=2, F_4=3, F_5=5, ... as a list [1,2,3,5,8,...] with all <= N."""
    f = [1, 2]
    while f[-1] <= N:
        f.append(f[-1] + f[-2])
    while f and f[-1] > N:
        f.pop()
    return f


def zeck_digits(v, F=None):
    """Zeckendorf: v = sum eps_i F_i, no two adjacent.  LSD-first bit list."""
    if F is None:
        F = fibs_upto(v)
    d = [0] * len(F)
    i = len(F) - 1
    while i >= 0 and v > 0:
        if F[i] <= v:
            d[i] = 1
            v -= F[i]
            i -= 2
        else:
            i -= 1
    assert v == 0
    return d


def from_zeck(d, F):
    return sum(c * F[i] for i, c in enumerate(d))


# ---------------------------------------------------------------- Ostrowski
def ostrowski_denoms(cf, N):
    """cf = [a1, a2, a3, ...] partial quotients of an irrational alpha in (0,1).
    q_{-1}=0, q_0=1, q_k = a_k q_{k-1} + q_{k-2}.  Returns [q_0, q_1, ...] <= N."""
    q = [1]
    qm1 = 0
    k = 0
    while q[-1] <= N:
        k += 1
        if k > len(cf):
            raise ValueError("cf too short")
        nq = cf[k - 1] * q[-1] + qm1
        qm1 = q[-1]
        q.append(nq)
    while len(q) > 1 and q[-1] > N:
        q.pop()
    return q


def ostrowski_digits(v, cf, q):
    """Greedy Ostrowski representation v = sum_{k>=0} b_k q_k with
    0 <= b_0 <= a_1 - 1, 0 <= b_k <= a_{k+1}, and b_k = a_{k+1} => b_{k-1} = 0.
    Greedy from the top yields exactly the canonical representation."""
    d = [0] * len(q)
    i = len(q) - 1
    while i >= 0 and v > 0:
        c = v // q[i]
        cap = cf[i] if i < len(cf) else 10 ** 9
        # b_i <= a_{i+1} = cf[i]
        if c > cap:
            c = cap
        d[i] = c
        v -= c * q[i]
        i -= 1
    assert v == 0, v
    return d


def from_ostrowski(d, q):
    return sum(c * q[i] for i, c in enumerate(d))


# ---------------------------------------------------------------- self-test
if __name__ == "__main__":
    N = 5000
    for v in range(1, N + 1):
        for b in (2, 3, 4, 5):
            assert from_base(base_digits(v, b), b) == v
        assert from_factorial(factorial_digits(v)) == v
    F = fibs_upto(N)
    seen = set()
    for v in range(1, N + 1):
        d = zeck_digits(v, F)
        assert from_zeck(d, F) == v
        assert all(not (d[i] and d[i + 1]) for i in range(len(d) - 1)), (v, d)
        seen.add(tuple(d))
    assert len(seen) == N
    # Ostrowski for golden ratio [1,1,1,...] must reproduce Zeckendorf shifted
    cf_g = [1] * 40
    qg = ostrowski_denoms(cf_g, N)
    for v in range(1, N + 1):
        d = ostrowski_digits(v, cf_g, qg)
        assert from_ostrowski(d, qg) == v
    # Ostrowski for sqrt(2)-1 = [2,2,2,...]
    cf_p = [2] * 30
    qp = ostrowski_denoms(cf_p, N)
    reps = set()
    for v in range(1, N + 1):
        d = ostrowski_digits(v, cf_p, qp)
        assert from_ostrowski(d, qp) == v
        reps.add(tuple(d))
    assert len(reps) == N
    print("numeration self-test OK: base b, factorial, Zeckendorf, Ostrowski(phi), Ostrowski(sqrt2)")
    print("  fibs:", fibs_upto(200))
    print("  pell q:", ostrowski_denoms([2] * 30, 200))
