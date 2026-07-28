#!/usr/bin/env python3
"""Sound (lossless) pruning of the candidate universe for
   "legal U contained in [x,y] with denominator(Sigma(U)) dividing D".

RULE A (PROVED).  Let U be any finite set of integers >= 2 with
denom(Sigma(U)) | D.  Fix a prime p, put f = nu_p(D) and
E = max{nu_p(n) : n in U} (E = -inf if p divides no element).  If E > f then
        sum_{n in U, nu_p(n)=E}  p^E / n   ==  0   (mod p).
Proof.  p^E*Sigma(U) = sum_{n} p^E/n.  A term with nu_p(n)=E equals 1/m_n with
m_n = n/p^E coprime to p, a p-adic unit; a term with nu_p(n) < E is p^{E-nu_p(n)}
times a p-adic unit, hence == 0 mod p.  On the other hand
nu_p(p^E Sigma(U)) = E + nu_p(Sigma(U)) >= E - f >= 1.  Reducing mod p gives the
claim.  (Note m_n^{-1} mod p is what "p^E/n mod p" means.)                    []

RULE L (legality).  If n is alive but neither n-1 nor n+1 is, delete n.

Deletion rule derived from RULE A: at the current top level E (> f) for p, an
alive element n with nu_p(n)=E can occur in an admissible U with top level
exactly E only if it lies in some nonempty subset J of the alive top-level
elements with sum_{k in J} p^E/k == 0 (mod p).  If no such J contains n, and n
cannot be at a lower level (its nu_p IS E), then n can only be used together with
an element of higher nu_p -- but there is none alive.  So n is deleted.

Both rules only delete elements lying in no admissible U, so the fixpoint is
sound: every legal U in [x,y] with denom(Sigma(U)) | D is inside the fixpoint.
"""
import sys
from math import gcd
from lib import smallest_prime_factors


def nu(n, p):
    e = 0
    while n % p == 0:
        n //= p
        e += 1
    return e


def _good_elements(ws, p):
    """ws: list of residues mod p (the values p^E/n mod p).  Return the set of
    indices i such that some nonempty subset J containing i has sum == 0 mod p."""
    k = len(ws)
    full = (1 << p) - 1

    def shift(mask, s):
        s %= p
        if s == 0:
            return mask
        return ((mask << s) | (mask >> (p - s))) & full

    pre = [0] * (k + 1)
    pre[0] = 1  # only residue 0 reachable by empty subset
    for i in range(k):
        pre[i + 1] = pre[i] | shift(pre[i], ws[i])
    suf = [0] * (k + 1)
    suf[k] = 1
    for i in range(k - 1, -1, -1):
        suf[i] = suf[i + 1] | shift(suf[i + 1], ws[i])
    good = set()
    for i in range(k):
        need = (-ws[i]) % p
        # need a in pre[i], b in suf[i+1] with a+b == need
        a_mask = pre[i]
        b_mask = suf[i + 1]
        # test: exists a with bit a set in a_mask and bit (need-a) set in b_mask
        rev = 0
        m = b_mask
        # build mask of (need - b) for b in b_mask  == reverse-and-shift
        # do it directly (p is small)
        while m:
            b = (m & -m).bit_length() - 1
            m &= m - 1
            rev |= 1 << ((need - b) % p)
        if a_mask & rev:
            good.add(i)
    return good


def prune(x, y, D, spf, prime_cap=None, extra_ban=(), max_level=32, pp_cap=None):
    """prime_cap: keep only prime_cap-smooth n.
    pp_cap: keep only n all of whose prime powers p^{nu_p(n)} are <= pp_cap
            UNLESS p^{nu_p(n)} divides D (those cost no lambda bits)."""
    alive = set(range(x, y + 1))
    if pp_cap is not None:
        for n in list(alive):
            m = n
            while m > 1:
                p = spf[m]
                e = 0
                while m % p == 0:
                    m //= p
                    e += 1
                if p ** e > pp_cap and D % (p ** e) != 0:
                    alive.discard(n)
                    break
    if prime_cap is not None:
        for n in list(alive):
            m = n
            while m > 1:
                p = spf[m]
                if p > prime_cap:
                    alive.discard(n)
                    break
                while m % p == 0:
                    m //= p
    for n in extra_ban:
        alive.discard(n)
    primes = [p for p in range(2, y + 1) if spf[p] == p]
    changed = True
    while changed:
        changed = False
        while True:
            drop = [n for n in alive if (n - 1) not in alive and (n + 1) not in alive]
            if not drop:
                break
            for n in drop:
                alive.discard(n)
            changed = True
        if not alive:
            break
        for p in primes:
            f = nu(D, p) if D % p == 0 else 0
            while True:
                lev = {}
                for n in alive:
                    if n % p == 0:
                        lev.setdefault(nu(n, p), []).append(n)
                if not lev:
                    break
                E = max(lev)
                if E <= f:
                    break
                top = sorted(lev[E])
                if len(top) > max_level:
                    break
                pe = p ** E
                ws = [pow(n // pe, p - 2, p) % p for n in top]  # (p^E/n) mod p
                good = _good_elements(ws, p)
                bad = [top[i] for i in range(len(top)) if i not in good]
                if not bad:
                    break
                for n in bad:
                    alive.discard(n)
                changed = True
    return sorted(alive)


def lcm_of(alive):
    L = 1
    for n in alive:
        L = L // gcd(L, n) * n
    return L


if __name__ == "__main__":
    x = int(sys.argv[1]); y = int(sys.argv[2]); D = int(sys.argv[3])
    cap = int(sys.argv[4]) if len(sys.argv) > 4 else None
    spf = smallest_prime_factors(y + 2)
    A = prune(x, y, D, spf, prime_cap=cap)
    L = lcm_of(A)
    from fractions import Fraction
    ms = sum(Fraction(1, n) for n in A) if A else Fraction(0)
    print("[%d,%d] D=%d cap=%s : |U|=%d  log2 L=%d  log2(L/gcd(L,D))=%d  maxsum=%.4f"
          % (x, y, D, cap, len(A), L.bit_length(),
             (L // gcd(L, D)).bit_length(), float(ms)))
    if len(A) < 400:
        print(" ".join(map(str, A)))
