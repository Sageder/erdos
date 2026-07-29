"""decouple2.py — Proposition W4-2 (extended decoupling criterion, WITH class signs).

Architecture.  c : N -> Z>=0 with finite fibres; classes emitted in increasing index
order.  Inside class j, order by the base-2 level comparator with sign vector
s_j : levels -> {0,1}:
      for u < w in class j:   u precedes w   iff   bit_l(u) = s_j(l),  l = v_2(w-u).
(That is a linear order for every s_j -- it is lexicographic on the reversed binary
strings with the level-l digit order flipped when s_j(l)=1 -- and it is monotone-3-AP-free
on EVERY subset, since for a 3-AP with l = v_2(e) the two consecutive pairs have level-l
bits (a,1-a) and (1-a,a), so exactly one of the two steps ascends.)

PROPOSITION W4-2.  The resulting permutation of N is monotone-4-AP-free provided every
4-AP (t1,t2,t3,t4), with l := v_2(d), satisfies at least one of
   (a) three consecutive equal class values;
   (b) the class sequence is not weakly monotone;
   (c) c(t1)=c(t2) != c(t3)=c(t4)  and  s_{c(t1)}(l) != s_{c(t3)}(l).
Proof of (c): t3 = t1 + 2d and v_2(2d) = l+1 > l, so bit_l(t1) = bit_l(t3); hence
[t1 before t2] = [bit_l(t1)=s_A] and [t3 before t4] = [bit_l(t1)=s_B] differ.  The
increasing orientation needs both, the decreasing orientation needs neither.

SCOPE NOTE.  This is exactly the two-pair parity mechanism of CORE Theorem 21 (length 5),
but here the sign is carried by an ARBITRARY finite-fibre class function, not by a convex
block partition.  Transitivity is free because the classes are emitted in index order --
so REQUIREMENTS B5's conclusion ("transitivity forces the sign onto a convex partition")
applies only to signs that are arithmetic functions of the value.

This file hunts for counterexamples to W4-2 and measures which patterns remain dangerous.
"""
import random
import sys
from collections import Counter
sys.path.insert(0, "/home/user/erdos/attempts/route-W4-novel")
from apkit import pos_from_order, find_4aps


def v2(n):
    k = 0
    while n % 2 == 0:
        n //= 2
        k += 1
    return k


def sign_order(vals, s):
    """sort `vals` by the base-2 level comparator with sign vector s (list of bits)."""
    def key(v):
        # LSD-first binary digits, with the digit order flipped at every level l with
        # s[l]=1.  Leading zeros MUST also be flipped -- padding with a raw 0 was a real
        # encoding bug (it broke the comparator for values of different bit-lengths).
        b = []
        x = v
        for k in range(40):
            dg = x % 2
            x //= 2
            b.append(dg if not s[k] else 1 - dg)
        return tuple(b)
    return sorted(vals, key=key)


def build(cls, signs, N):
    groups = {}
    for v in range(1, N + 1):
        groups.setdefault(cls[v], []).append(v)
    out = []
    for j in sorted(groups):
        out.extend(sign_order(groups[j], signs[j]))
    return out


def classify(cls, signs, N):
    """for every 4-AP, say whether W4-2 covers it; return (all_covered, pattern counts)"""
    cnt = Counter()
    covered = True
    for d in range(1, (N - 1) // 3 + 1):
        l = v2(d)
        for x in range(1, N - 3 * d + 1):
            s = [cls[x + i * d] for i in range(4)]
            if (s[0] == s[1] == s[2]) or (s[1] == s[2] == s[3]):
                cnt["a:3-run"] += 1
                continue
            wi = s[0] <= s[1] <= s[2] <= s[3]
            wd = s[0] >= s[1] >= s[2] >= s[3]
            if not wi and not wd:
                cnt["b:non-monotone"] += 1
                continue
            if s[0] == s[1] and s[2] == s[3] and s[0] != s[2] and \
                    signs[s[0]][l] != signs[s[2]][l]:
                cnt["c:pair+pair opposite sign"] += 1
                continue
            cnt["DANGEROUS %s" % ("=".join("ABCD"[i] for i in range(4))
                                  if len(set(s)) == 4 else
                                  "".join("ABCD"["".join(map(str, sorted(set(s)))).index(
                                      str(y)) if False else sorted(set(s)).index(y)]
                                      for y in s))] += 1
            covered = False
    return covered, cnt


if __name__ == "__main__":
    rng = random.Random(4196)
    tested = covered_cnt = viol = 0
    for trial in range(6000):
        N = rng.randint(8, 30)
        style = rng.randrange(4)
        cls = [0] * (N + 1)
        if style == 0:
            M = rng.randint(1, N)
            for v in range(1, N + 1):
                cls[v] = rng.randrange(M)
        elif style == 1:
            L = rng.randint(1, 5)
            for v in range(1, N + 1):
                cls[v] = v // L
        elif style == 2:
            b = rng.choice([2, 3, 4])
            for v in range(1, N + 1):
                j, p = 0, 1
                while p * b <= v:
                    p *= b
                    j += 1
                cls[v] = j
        else:
            m = rng.randint(2, 4)
            L = rng.randint(m, 3 * m)
            for v in range(1, N + 1):
                cls[v] = (v // L) * m + (v % m)
        M = max(cls[1:]) + 1
        signs = [[rng.randrange(2) for _ in range(40)] for _ in range(M)]
        ok, _ = classify(cls, signs, N)
        order = build(cls, signs, N)
        pos = pos_from_order(order)
        hits = find_4aps(pos, N)
        tested += 1
        if ok:
            covered_cnt += 1
            if hits:
                viol += 1
                print("COUNTEREXAMPLE to W4-2:", N, cls[1:], hits[0])
    print(f"Prop W4-2: {tested} random class+sign configurations, criterion covered all "
          f"4-APs in {covered_cnt}, implication violations: {viol}")

    # Which patterns survive for the standard architectures?
    print()
    print("pattern census (which configurations are NOT covered by (a),(b),(c)):")
    N = 400
    for b in (3, 4, 5):
        cls = [0] * (N + 1)
        for v in range(1, N + 1):
            j, p = 0, 1
            while p * b <= v:
                p *= b
                j += 1
            cls[v] = j
        M = max(cls[1:]) + 1
        signs = [[j % 2] * 40 for j in range(M)]     # alternating block signs
        ok, cnt = classify(cls, signs, N)
        tot = sum(cnt.values())
        print(f"  blocks ratio {b}, alternating signs, N={N}: covered={ok}")
        for k, val in sorted(cnt.items(), key=lambda kv: -kv[1]):
            print(f"      {k:34s} {val:7d}  ({100*val/tot:5.1f}%)")
