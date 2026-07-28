#!/usr/bin/env python3
"""
Recon-3 independent audit.  Written from scratch; imports NOTHING from the repository.

Checks, in exact rational arithmetic only (fractions.Fraction + integers):

  (A) every line of experiments/ALLSOLS.txt is a genuine solution:
      strictly increasing integers >= 2, no isolated point, sum of reciprocals == 1;
  (B) every certificate of experiments/CERTIFICATES.txt is a genuine P(k) witness:
      exactly k blocks, each of length >= 2, pairwise disjoint, all elements >= 2,
      reciprocal sum == 1;
  (C) the coverage set  U_{solutions} [r(U), cap(U)]  and its gap structure;
  (D) the splitting lemma, verified concretely (constructively) for every run length
      L <= 200 and every admissible t;
  (E) Rule (P) as an identity check on every solution and every relevant prime;
  (F) the "top run is prime-free / lies in (N/2,N]" claim on every solution;
  (G) the two advertised identities (85-solution, 1/2-gadget).

Usage:  python3 av_check.py
"""

from fractions import Fraction
import sys, os, ast
from math import gcd

REPO = "/home/user/erdos"
ALLSOLS = os.path.join(REPO, "experiments", "ALLSOLS.txt")
CERTS = os.path.join(REPO, "experiments", "CERTIFICATES.txt")

# ---------------------------------------------------------------- primitives

def is_legal(sorted_elems):
    """no isolated point: every n has n-1 or n+1 present"""
    s = set(sorted_elems)
    return all((n - 1 in s) or (n + 1 in s) for n in s)

def runs(sorted_elems):
    """maximal runs of consecutive integers, as (start, length)"""
    out = []
    i = 0
    v = sorted_elems
    while i < len(v):
        j = i
        while j + 1 < len(v) and v[j + 1] == v[j] + 1:
            j += 1
        out.append((v[i], j - i + 1))
        i = j + 1
    return out

def recip_sum(elems):
    """exact sum of 1/n via integer arithmetic (num/den, no Fraction shortcuts)"""
    num, den = 0, 1
    for n in elems:
        num, den = num * n + den, den * n
        g = gcd(num, den)
        num //= g
        den //= g
    return Fraction(num, den)

def sieve(n):
    bs = bytearray([1]) * (n + 1)
    bs[0:2] = b"\x00\x00"
    i = 2
    while i * i <= n:
        if bs[i]:
            bs[i * i:: i] = bytearray(len(bs[i * i:: i]))
        i += 1
    return bs

def vp(n, p):
    e = 0
    while n % p == 0:
        n //= p
        e += 1
    return e

# ---------------------------------------------------------------- (A) corpus

def check_solutions():
    sols = []
    bad = []
    with open(ALLSOLS) as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if parts[0] != "SOL":
                bad.append((lineno, "bad prefix"))
                continue
            try:
                v = [int(x) for x in parts[1:]]
            except ValueError:
                bad.append((lineno, "non-integer token"))
                continue
            if any(v[i] >= v[i + 1] for i in range(len(v) - 1)):
                bad.append((lineno, "not strictly increasing"))
                continue
            if v[0] < 2:
                bad.append((lineno, "element < 2"))
                continue
            if not is_legal(v):
                bad.append((lineno, "isolated point"))
                continue
            s = recip_sum(v)
            if s != 1:
                bad.append((lineno, "sum = %s != 1" % s))
                continue
            sols.append(v)
    return sols, bad

# ---------------------------------------------------------------- (B) certs

def check_certificates():
    res = []
    bad = []
    with open(CERTS) as f:
        for line in f:
            line = line.strip()
            if not line.startswith("k="):
                continue
            head, blocks_txt = line.split("VERIFIED")
            k = int(head.split("k=")[1].split("max=")[0].strip())
            blocks = ast.literal_eval(blocks_txt.strip())
            # exactly k blocks
            if len(blocks) != k:
                bad.append((k, "block count %d != %d" % (len(blocks), k)))
                continue
            ok = True
            for (a, b) in blocks:
                if not (isinstance(a, int) and isinstance(b, int)):
                    bad.append((k, "non-integer endpoint")); ok = False; break
                if a < 2:
                    bad.append((k, "element < 2 in block (%d,%d)" % (a, b))); ok = False; break
                if b - a + 1 < 2:
                    bad.append((k, "block (%d,%d) length < 2" % (a, b))); ok = False; break
            if not ok:
                continue
            srt = sorted(blocks)
            for i in range(len(srt) - 1):
                if not srt[i][1] < srt[i + 1][0]:
                    bad.append((k, "blocks %s %s overlap" % (srt[i], srt[i + 1]))); ok = False; break
            if not ok:
                continue
            elems = [n for (a, b) in blocks for n in range(a, b + 1)]
            if len(set(elems)) != len(elems):
                bad.append((k, "repeated element")); continue
            s = recip_sum(elems)
            if s != 1:
                bad.append((k, "sum %s != 1" % s)); continue
            res.append((k, max(elems), min(elems), len(blocks)))
    return res, bad

# ------------------------------------------------------- (D) splitting lemma

def split_run(a, b, t):
    """partition [a,b] into t adjacent blocks each of length >= 2 (constructive)"""
    L = b - a + 1
    assert 1 <= t <= L // 2
    out = []
    cur = a
    for i in range(t - 1):
        out.append((cur, cur + 1))
        cur += 2
    out.append((cur, b))
    return out

def check_splitting(maxL=200):
    for L in range(2, maxL + 1):
        for t in range(1, L // 2 + 1):
            parts = split_run(10 ** 6, 10 ** 6 + L - 1, t)
            assert len(parts) == t
            assert all(y - x + 1 >= 2 for (x, y) in parts)
            assert parts[0][0] == 10 ** 6 and parts[-1][1] == 10 ** 6 + L - 1
            for i in range(t - 1):
                assert parts[i][1] + 1 == parts[i + 1][0]
        # t = L//2 + 1 must be impossible: t blocks of length >=2 need 2t <= L
        assert 2 * (L // 2 + 1) > L
    return True

# ------------------------------------------------------------ (E) Rule (P)

def check_ruleP(sols, limit=None):
    """for every solution U and every prime p dividing some element:
       nu_p( sum_{n in U, p|n} 1/n ) >= 0, and >= 2 elements attain the max nu_p."""
    viol = []
    for idx, v in enumerate(sols if limit is None else sols[:limit]):
        N = max(v)
        pr = sieve(N)
        for p in range(2, N + 1):
            if not pr[p]:
                continue
            mult = [n for n in v if n % p == 0]
            if not mult:
                continue
            E = max(vp(n, p) for n in mult)
            top = [n for n in mult if vp(n, p) == E]
            if len(top) < 2:
                viol.append((idx, p, "unique top attainer"))
            S = recip_sum(mult)          # exact
            num, den = S.numerator, S.denominator
            if den % p == 0:
                viol.append((idx, p, "nu_p(S_p) < 0"))
            # the mod-p^E form: p^E * S_p must be a p-adic integer, i.e. p does not divide
            # the denominator of p^E*S_p ; equivalent to the above.
    return viol

# ----------------------------------------------- (F) top run prime-free

def check_toprun(sols):
    viol = []
    for idx, v in enumerate(sols):
        N = max(v)
        pr = sieve(N)
        rr = runs(v)
        c, L = rr[-1][0], rr[-1][1]
        assert c + L - 1 == N
        if not (2 * c > N):
            viol.append((idx, "top run starts at %d <= N/2 = %g" % (c, N / 2)))
        if any(pr[x] for x in range(c, N + 1)):
            viol.append((idx, "prime in top run [%d,%d]" % (c, N)))
    return viol

# ---------------------------------------------------------------- main

def main():
    print("=" * 72)
    print("(A) corpus check:", ALLSOLS)
    sols, bad = check_solutions()
    print("    lines accepted as solutions :", len(sols))
    print("    rejected                    :", len(bad))
    for b in bad[:10]:
        print("      REJECT", b)
    dedup = set(tuple(v) for v in sols)
    print("    distinct solutions          :", len(dedup))
    print("    min over solutions of max(U):", min(max(v) for v in sols))
    print("    max over solutions of max(U):", max(max(v) for v in sols))
    print("    largest min(U) in corpus    :", max(min(v) for v in sols))

    print("=" * 72)
    print("(B) certificate check:", CERTS)
    res, badc = check_certificates()
    ks = sorted(k for (k, _, _, _) in res)
    print("    certificates verified :", len(res))
    print("    k values              :", ks[0], "...", ks[-1], "contiguous:",
          ks == list(range(ks[0], ks[-1] + 1)))
    print("    failures              :", badc)

    print("=" * 72)
    print("(C) coverage of [r(U), cap(U)] over the corpus")
    cover = set()
    pairs = []
    for v in sols:
        rr = runs(v)
        r = len(rr)
        cap = sum(L // 2 for (_, L) in rr)
        pairs.append((r, cap, max(v), min(v), len(v)))
        cover.update(range(r, cap + 1))
    lo, hi = min(cover), max(cover)
    missing = [k for k in range(lo, hi + 1) if k not in cover]
    print("    min r over corpus     :", min(p[0] for p in pairs))
    print("    max cap over corpus   :", max(p[1] for p in pairs))
    print("    covered k range       :", lo, "..", hi)
    print("    holes inside range    :", missing[:40], "(total %d)" % len(missing))
    contiguous_top = lo - 1
    for k in range(lo, hi + 1):
        if k in cover:
            contiguous_top = k
        else:
            break
    print("    contiguous from %d up to: %d" % (lo, contiguous_top))
    # how many solutions have r == cap (interval is a single point)?
    npoint = sum(1 for p in pairs if p[0] == p[1])
    print("    solutions with r == cap (singleton interval): %d / %d = %.3f"
          % (npoint, len(pairs), npoint / len(pairs)))
    import statistics
    ratios = [p[0] / p[1] for p in pairs]
    print("    r/cap: min %.4f  median %.4f  max %.4f"
          % (min(ratios), statistics.median(ratios), max(ratios)))

    print("=" * 72)
    print("(D) splitting lemma constructive check for L <= 200 :", check_splitting())

    print("=" * 72)
    print("(E) Rule (P) on the first 400 solutions")
    viol = check_ruleP(sols, limit=400)
    print("    violations:", viol[:10], "count", len(viol))

    print("=" * 72)
    print("(F) top-run prime-free on ALL solutions")
    tv = check_toprun(sols)
    print("    violations:", tv[:10], "count", len(tv))

    print("=" * 72)
    print("(G) advertised identities")
    U85 = [5, 6, 14, 15, 17, 18, 20, 21, 22, 27, 28, 33, 34, 44, 45, 54, 55, 84, 85]
    print("    85-solution sum =", recip_sum(U85), " legal:", is_legal(U85),
          " runs:", runs(U85))
    G = [6, 7, 20, 21, 44, 45, 77, 78, 90, 91]
    print("    1/2-gadget  sum =", recip_sum(G), " legal:", is_legal(G),
          " runs:", runs(G))
    print("    r,cap of gadget =", len(runs(G)), sum(L // 2 for (_, L) in runs(G)))
    # PROBLEM.md B5 identities
    print("    1/3+1/4+1/5+1/6+1/20 =", recip_sum([3, 4, 5, 6, 20]))
    print("    1/2+1/3+1/10+1/15    =", recip_sum([2, 3, 10, 15]))
    print("    1/2+..+1/6+1/20      =", recip_sum([2, 3, 4, 5, 6, 20]))

if __name__ == "__main__":
    main()
