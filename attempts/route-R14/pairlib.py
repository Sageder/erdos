"""
R14 measurement library (slice-based; cost  O(X loglog y)  not  O(pi(y) X)).

For a bound X and smoothness threshold y (always y = X^b, never n^b) produce the set
   S = { n <= X : n+1 and n+2 both y-smooth }
and exact per-prime data for the Erdos-727 k=2 criterion
   n in S_2  <=>  for all primes p:  kappa_p(n) >= 2( nu_p(n+1) + nu_p(n+2) ).
All arithmetic is exact (numpy int64 / python int); no floating point in any criterion.
"""
import numpy as np


def primes_upto(N):
    if N < 2:
        return np.array([], dtype=np.int64)
    sieve = np.ones(N + 1, dtype=bool)
    sieve[:2] = False
    for i in range(2, int(N ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i::i] = False
    return np.nonzero(sieve)[0].astype(np.int64)


def smooth_mask(X, y):
    """bool array sm, length X+3, sm[m] = (m is y-smooth) for m >= 1."""
    rem = np.arange(X + 3, dtype=np.int64)
    for p in primes_upto(y):
        p = int(p); pe = p
        while pe <= X + 2:
            rem[pe::pe] //= p
            pe *= p
    sm = (rem == 1)
    sm[0] = False
    return sm


def carries_vec(n, l):
    """#carries adding n+n in base l, vectorised over an int64 array n."""
    v = n.copy()
    c = np.zeros(len(n), dtype=np.int64)
    carry = np.zeros(len(n), dtype=np.int64)
    while v.any():
        carry = ((2 * (v % l) + carry) >= l).astype(np.int64)
        c += carry
        v //= l
    return c


def digitpoor_vec(V, l, jtrunc=None):
    """
    V = W-1 >= 0.  True iff doubling V base l with carry-in 1 makes no carry in
    digit positions 0..jtrunc-1 (jtrunc=None: all positions => the exact failure event).
    """
    v = V.copy()
    ok = (2 * (v % l) + 1 < l)
    v //= l
    i = 1
    while (jtrunc is None or i < jtrunc) and v.any():
        ok &= (2 * (v % l) < l)
        v //= l
        i += 1
    return ok


def multiples_slice(X, l, j):
    """
    All n in [1, X-2] with l | n+j, together with W = (n+j)/l.
    Returned as (n_array, W_array).  Cost O(X/l).
    """
    t = np.arange(1, X // l + 1, dtype=np.int64)
    n = l * t - j
    keep = (n >= 1) & (n <= X - 2)
    return n[keep], t[keep]


def pair_data(X, y, P0=4, want_full=False):
    """
    Full-length (index = n) arrays for the smooth-pair set.
      ispair       bool, length X   : n+1 and n+2 both y-smooth
      nfail_large  int8             : #{l>P0 : l|(n+1)(n+2), kappa_l(n) < 2 nu_l(n+j)}
      nfail_e1/e2  int8             : the parts with l||n+j  /  l^2|n+j
      omega_large  int8
      sqfree       bool             : l || n+j for every prime l > P0
      lpf1, lpf2   int64            : largest prime factor of n+1, n+2
      fail_lpf1/2  bool
      ok_small     bool             : criterion holds at every p <= P0
      perprime     dict l -> [#occurrences, #failures]
    """
    sm = smooth_mask(X, y)
    ispair = np.zeros(X, dtype=bool)
    ispair[1:X - 1] = sm[2:X] & sm[3:X + 1]     # index n; n+1=sm[n+1], n+2=sm[n+2]
    idxs = np.nonzero(ispair)[0]
    out = dict(X=X, y=y, ispair=ispair, n=idxs)
    L = X
    nfail = np.zeros(L, dtype=np.int8)
    nf_e1 = np.zeros(L, dtype=np.int8)
    nf_e2 = np.zeros(L, dtype=np.int8)
    omega = np.zeros(L, dtype=np.int8)
    sqfree = np.ones(L, dtype=bool)
    lpf = [np.zeros(L, dtype=np.int64), np.zeros(L, dtype=np.int64)]
    flpf = [np.zeros(L, dtype=bool), np.zeros(L, dtype=bool)]
    perprime = {}

    for l in primes_upto(y):
        l = int(l)
        if l <= P0:
            continue
        for j in (1, 2):
            n, W = multiples_slice(X, l, j)
            if len(n) == 0:
                continue
            keep = ispair[n]
            n = n[keep]; W = W[keep]
            if len(n) == 0:
                continue
            e = np.ones(len(n), dtype=np.int64)
            mm = W.copy()
            while True:
                more = (mm % l == 0)
                if not more.any():
                    break
                mm = np.where(more, mm // l, mm)
                e += more
            k = carries_vec(n, l)
            fail = k < 2 * e
            nfail[n] += fail
            nf_e1[n] += fail & (e == 1)
            nf_e2[n] += fail & (e >= 2)
            omega[n] += 1
            sqfree[n] &= (e == 1)
            lpf[j - 1][n] = l               # primes ascending => last write wins
            flpf[j - 1][n] = fail
            pp = perprime.setdefault(l, [0, 0])
            pp[0] += len(n); pp[1] += int(fail.sum())

    ok_small = np.ones(L, dtype=bool)
    nn = idxs
    if len(nn):
        for p in primes_upto(P0):
            p = int(p)
            dem = np.zeros(len(nn), dtype=np.int64)
            for j in (1, 2):
                mm = nn + j
                while True:
                    more = (mm % p == 0)
                    if not more.any():
                        break
                    mm = np.where(more, mm // p, mm)
                    dem += more
            ok_small[nn] &= (carries_vec(nn, p) >= 2 * dem)

    out.update(nfail_large=nfail, nfail_e1=nf_e1, nfail_e2=nf_e2, omega_large=omega,
               sqfree=sqfree, lpf1=lpf[0], lpf2=lpf[1], fail_lpf1=flpf[0],
               fail_lpf2=flpf[1], ok_small=ok_small, perprime=perprime)
    return out
