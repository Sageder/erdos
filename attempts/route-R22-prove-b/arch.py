"""arch.py -- route R22 (angle B) core library.

Setting (mission / CORE.md Prop 29, Cor 30, Conj R21-C).
A CLASS ARCHITECTURE is a class function c : N -> Z_{>=0} with finite fibres
F_j = c^{-1}(j), classes emitted in increasing index order, arbitrary order inside a
class.  Here c(v) = m(v) + t(v) with m(v) = floor(log_b v) the block index,
B_m = [b^m, b^{m+1}), and t : N -> Z_{>=0} the DELAY.

Condition (ii): along every 4-AP (x, x+d, x+2d, x+3d) the class sequence
(c_0,c_1,c_2,c_3) is neither strictly increasing nor strictly decreasing.

Everything here is exact integer arithmetic.  Two independent implementations of the
(ii)-checker are provided and cross-validated against each other and against known
positive/negative controls from route R20.
"""

import sys
import numpy as np

sys.path.insert(0, '/home/user/erdos/experiments')


# ---------------------------------------------------------------- block index

def blk(v, b):
    """floor(log_b v) by exact integer arithmetic (no floats)."""
    assert v >= 1 and b >= 2
    m, p = 0, 1
    while p * b <= v:
        p *= b
        m += 1
    return m


def blk_array(M, b):
    """blk[v] for v = 0..M (blk[0] unused, set 0)."""
    out = np.zeros(M + 1, dtype=np.int64)
    m, lo = 0, 1
    while lo <= M:
        hi = min(M, lo * b - 1)
        out[lo:hi + 1] = m
        m += 1
        lo *= b
    return out


def block_bounds(m, b):
    return b ** m, b ** (m + 1) - 1          # inclusive


# ------------------------------------------------- condition (ii) : checker A

def four_aps(M):
    """All 4-APs (x, x+d, x+2d, x+3d) with largest term <= M."""
    for d in range(1, (M - 1) // 3 + 1):
        for x in range(1, M - 3 * d + 1):
            yield (x, x + d, x + 2 * d, x + 3 * d)


def check_ii_slow(c, M):
    """Literal scan over all 4-APs with largest term <= M.  c is a 0-indexed list/array
    with c[v] defined for 1 <= v <= M.  Returns None if (ii) holds, else a witness."""
    for (a, b_, cc, dd) in four_aps(M):
        s = (int(c[a]), int(c[b_]), int(c[cc]), int(c[dd]))
        if s[0] < s[1] < s[2] < s[3]:
            return ('inc', a, b_ - a, s)
        if s[0] > s[1] > s[2] > s[3]:
            return ('dec', a, b_ - a, s)
    return None


# ------------------------------------------------- condition (ii) : checker B

def check_ii_fast(c, M):
    """Vectorised, independent implementation (numpy).  Same contract as check_ii_slow.
    Iterates over d; for each d compares the four shifted slices at once."""
    cv = np.asarray(c, dtype=np.int64)
    for d in range(1, (M - 1) // 3 + 1):
        n = M - 3 * d
        c0 = cv[1:n + 1]
        c1 = cv[1 + d:n + 1 + d]
        c2 = cv[1 + 2 * d:n + 1 + 2 * d]
        c3 = cv[1 + 3 * d:n + 1 + 3 * d]
        inc = (c0 < c1) & (c1 < c2) & (c2 < c3)
        if inc.any():
            x = int(np.flatnonzero(inc)[0]) + 1
            return ('inc', x, d, (int(cv[x]), int(cv[x + d]), int(cv[x + 2 * d]), int(cv[x + 3 * d])))
        dec = (c0 > c1) & (c1 > c2) & (c2 > c3)
        if dec.any():
            x = int(np.flatnonzero(dec)[0]) + 1
            return ('dec', x, d, (int(cv[x]), int(cv[x + d]), int(cv[x + 2 * d]), int(cv[x + 3 * d])))
    return None


def count_ii_violations(c, M):
    """Total number of 4-APs with strictly monotone class sequence (both orientations)."""
    cv = np.asarray(c, dtype=np.int64)
    tot_inc = tot_dec = 0
    for d in range(1, (M - 1) // 3 + 1):
        n = M - 3 * d
        c0 = cv[1:n + 1]
        c1 = cv[1 + d:n + 1 + d]
        c2 = cv[1 + 2 * d:n + 1 + 2 * d]
        c3 = cv[1 + 3 * d:n + 1 + 3 * d]
        tot_inc += int(((c0 < c1) & (c1 < c2) & (c2 < c3)).sum())
        tot_dec += int(((c0 > c1) & (c1 > c2) & (c2 > c3)).sum())
    return tot_inc, tot_dec


# ---------------------------------------------------------------- delays

def delay_head(M, b, s_of_m, K_of_m):
    """The route-R22 HEAD-DELAY family.

        t(v) = K_m  if  b^m <= v < b^m + s_m   (v in the 'head' H_m of block B_m)
        t(v) = 0    otherwise,          m = floor(log_b v).

    Returns arrays (t, c) indexed 1..M (index 0 unused)."""
    t = np.zeros(M + 1, dtype=np.int64)
    mm = blk_array(M, b)
    m, lo = 0, 1
    while lo <= M:
        s = s_of_m(m)
        assert 1 <= s <= (b - 1) * b ** m, (m, s)
        hi = min(M, lo + s - 1)
        t[lo:hi + 1] = K_of_m(m)
        m += 1
        lo *= b
    c = mm + t
    c[0] = 0
    return t, c


def delay_from_t(M, b, tfun):
    t = np.zeros(M + 1, dtype=np.int64)
    for v in range(1, M + 1):
        t[v] = tfun(v)
    c = blk_array(M, b) + t
    c[0] = 0
    return t, c


def v2(n):
    k = 0
    while n % 2 == 0:
        n //= 2
        k += 1
    return k


def v3(n):
    k = 0
    while n % 3 == 0:
        n //= 3
        k += 1
    return k


# ---------------------------------------------------------------- fibre budget

def fibre_sizes(c, M, Jmax=None):
    """|F_j ∩ [1..M]| for j = 0..Jmax."""
    cv = np.asarray(c, dtype=np.int64)[1:M + 1]
    if Jmax is None:
        Jmax = int(cv.max())
    return np.bincount(cv, minlength=Jmax + 1)[:Jmax + 1]


def budget_identity_check(t, b, M):
    """Verify Lemma B1 exactly, for every J with b^{J+1}-1 <= M:

        S_J := #{v : c(v) <= J}  =  (b^{J+1} - 1)  -  sum_{k>=1} N_{J+1-k}(k),
        N_m(k) := #{v in B_m : t(v) >= k}.

    Returns list of (J, S_J, rhs, ok)."""
    tv = np.asarray(t, dtype=np.int64)
    mm = blk_array(M, b)
    c = mm + tv
    out = []
    J = 0
    while b ** (J + 1) - 1 <= M:
        S = int((c[1:M + 1] <= J).sum())
        rhs = b ** (J + 1) - 1
        for k in range(1, J + 2):
            m = J + 1 - k
            lo, hi = block_bounds(m, b)
            rhs -= int((tv[lo:hi + 1] >= k).sum())
        out.append((J, S, rhs, S == rhs))
        J += 1
    return out
