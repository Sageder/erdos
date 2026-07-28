"""constructions.py — route R20 candidate orderings of N with superlinear displacement.

Architecture (see REPORT.md sec. 2):  an ordering is given by a key
        key(v) = ( c(v), w(v) )                     lexicographic
where c is a CLASS function with finite fibres (so the order has type omega) and w is a
within-class comparator key.  The class functions used all satisfy Lemma R20-1
(no 4-AP has a strictly monotone class sequence), which is what makes the design
non-vacuous; everything then depends on the within-class orders.

c-families
    CLS(b, rho) :  c(v) = floor(log_b v) + rho(v_2(v)),  b >= 3, rho strictly increasing.
                   "delay the 2-adically divisible values by rho(v_2) blocks".
    CLS3(b, rho3): the 3-adic analogue, c(v) = floor(log_b v) + rho(v_3(v)).
    BLK(b)      : c(v) = floor(log_b v)  (contiguous blocks; known dead, control).

w-families (global comparators, so they restrict consistently to every class)
    val, revval      : by value / by reversed value
    sigma            : the parity recursion comparator (R3 Lemma S) - no monotone 3-AP
                       on ANY subset of N
    tau_p            : base-3 lowest-differing-digit priority comparator (R3 Lemma T) -
                       no monotone 4-AP on ANY subset of N; p = the per-level priority
    sigma_odd/...    : variants keyed on the odd part
"""
import sys
import numpy as np

sys.path.insert(0, '/home/user/erdos/attempts/route-R20-vlogv')
from framework import restrict, violations, is_free, pos_array


# ------------------------------------------------------------------ helpers
def v2(n):
    return (n & -n).bit_length() - 1


def vp(n, p):
    k = 0
    while n % p == 0:
        n //= p
        k += 1
    return k


def logb(v, b):
    j, pw = 0, b
    while pw <= v:
        pw *= b
        j += 1
    return j


# ------------------------------------------------------------ class families
def cls_delay(b, rho):
    return lambda v: logb(v, b) + rho(v2(v))


def cls_delay3(b, rho):
    return lambda v: logb(v, b) + rho(vp(v, 3))


def cls_block(b):
    return lambda v: logb(v, b)


# ---------------------------------------------------- within-class key funcs
def w_val(v):
    return v


def w_revval(v):
    return -v


def _sigma_key(v, L=64):
    """R3 Lemma S comparator, as a sortable key: at the first level l where the parities
    of g^l differ (g(n)=ceil(n/2)), the ODD one comes first."""
    out = []
    n = v
    for _ in range(L):
        out.append(0 if (n & 1) else 1)      # odd -> 0 sorts first
        n = (n + 1) // 2
        if n == 1:
            break
    out.append(0)
    return tuple(out)


SIGMA_CACHE = {}


def w_sigma(v):
    r = SIGMA_CACHE.get(v)
    if r is None:
        r = _sigma_key(v)
        SIGMA_CACHE[v] = r
    return r


def make_w_tau(prios, L=40):
    """base-3 lowest-differing-digit comparator; prios[l] is a permutation of (0,1,2)
    giving the priority of digit d at level l (smaller = earlier)."""
    def w(v):
        out = []
        n = v
        for l in range(L):
            out.append(prios[l % len(prios)][n % 3])
            n //= 3
            if n == 0:
                break
        while len(out) < 3:
            out.append(prios[len(out) % len(prios)][0])
        return tuple(out)
    return w


def w_sigma_odd(v):
    """sigma comparator applied to the odd part, then by v_2."""
    return (_sigma_key(v >> v2(v)), v2(v))


def w_tau_nat(v):
    return make_w_tau([(0, 1, 2)])(v)


# ---------------------------------------------------------------- assembling
def make_key(c, w):
    return lambda v: (c(v), w(v))


def evaluate(name, key, M, show=4):
    perm = restrict(key, M)
    vio = violations(perm, 4)
    pos = pos_array(perm)
    if not vio:
        return (name, None, None)
    x, d, sign = vio[0]
    detail = [(x, d, sign, tuple(int(pos[x + i * d]) + 1 for i in range(4))) for x, d, sign in vio[:show]]
    return (name, x + 3 * d, detail)


CLASS_FAMILIES = {
    'CLS(3,a)': cls_delay(3, lambda a: a),
    'CLS(4,a)': cls_delay(4, lambda a: a),
    'CLS(5,a)': cls_delay(5, lambda a: a),
    'CLS(3,2a)': cls_delay(3, lambda a: 2 * a),
    'CLS3(3,a)': cls_delay3(3, lambda a: a),
    'CLS3(4,a)': cls_delay3(4, lambda a: a),
    'BLK(3)': cls_block(3),
    'BLK(4)': cls_block(4),
}

W_FAMILIES = {
    'val': w_val,
    'revval': w_revval,
    'sigma': w_sigma,
    'tau012': make_w_tau([(0, 1, 2)]),
    'tau021': make_w_tau([(0, 2, 1)]),
    'tau102': make_w_tau([(1, 0, 2)]),
    'tau120': make_w_tau([(1, 2, 0)]),
    'tau201': make_w_tau([(2, 0, 1)]),
    'tau210': make_w_tau([(2, 1, 0)]),
    'tau_alt': make_w_tau([(0, 1, 2), (1, 2, 0)]),
    'tau_alt2': make_w_tau([(0, 2, 1), (2, 1, 0)]),
    'sigma_odd': w_sigma_odd,
}


if __name__ == "__main__":
    M = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    rows = []
    for cn, c in CLASS_FAMILIES.items():
        for wn, w in W_FAMILIES.items():
            name = f"{cn} x {wn}"
            r = evaluate(name, make_key(c, w), M)
            rows.append(r)
    rows.sort(key=lambda r: (r[1] is not None, r[1] if r[1] is not None else 0))
    for name, mn, detail in rows:
        if mn is None:
            print(f"{name:26s}  SURVIVES to M={M}")
        else:
            ds = "; ".join(f"({x},{d},{s}) pos={p}" for x, d, s, p in detail)
            print(f"{name:26s}  dies at max-term {mn:5d}   {ds}")
