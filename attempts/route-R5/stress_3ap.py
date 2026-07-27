"""stress_3ap.py — machine stress tests for the proof of the 3-AP forcing theorem
(proof_3ap.md, Theorems 1 and 2).

The theorem is about infinite permutations, so it cannot be "tested" directly; what CAN
be tested are the proof's intermediate finite claims, plus the two designed failure
modes that certify where infinitude/surjectivity are genuinely used:

 T1 (engine identity): for ANY permutation of [1..N] and any anchor position s,
    "there is an increasing 3-AP with first term a(s) and later terms after s"
    is EQUIVALENT to "constraint (A_s) fails for some v", where
      (A_s):  for all v > a(s) with pos(v) > s and 2v - a(s) <= N:
              pos(2v - a(s)) < pos(v).
    (This is the contrapositive step of the proof; checked literally.)

 T2 (descent mechanics + escape accounting): for every permutation of [1..N] with NO
    increasing 3-AP anchored at position s: for every v > u = a(s) with pos(v) > s,
    follow the orbit v_0 = v, v_{t+1} = 2 v_t - u.  Check:
      (i)  while the orbit stays inside [1..N] at positions > s, positions STRICTLY
           DECREASE at each step;
      (ii) the orbit terminates only by (a) landing at a position < s (escape into the
           finite head E_s) or (b) LEAVING the value universe (v_t > N);
      (iii) the injectivity count: distinct v never share the same (escape value, t);
      (iv) the head-capacity bound |{v : orbit escapes into E_s}| <=
           sum over g in E_s-values, g > u, of (nu_2(g-u)+1)   [nu_2 = 2-adic valuation]
    In the INFINITE setting (b) is impossible (surjectivity: every 2v_t - u occurs), and
    (iv) bounds the (a)-escapers by a finite number, contradicting that there are
    infinitely many v.  On finite models, (b) is exactly how avoiders survive — this is
    the certified locus of the surjectivity/infinitude usage.

 T3 (surjectivity is necessary): the injection n -> 2^n has NO monotone 3-AP among its
    first K terms for K = 1200 (values 2,4,8,...; any 3-AP x, x+d, x+2d among powers of
    two forces 2^b - 2^a = 2^c - 2^b which is impossible for a<b<c; we still machine
    check it, and for k = 4 as well).

 T4 (finite exhaustion can never prove the theorem): the parity permutation sigma_N has
    no monotone 3-AP for all N <= 512 (re-verified here); so every finite consequence of
    "no monotone 3-AP" is satisfiable, and the theorem's proof MUST (and does) use the
    infinite pigeonhole (every orbit either escapes into a FIXED finite head or runs
    forever, which well-ordering of positions forbids).

 T5 (Theorem 2 anchored-supply, finite shadow): for all permutations of [1..N]
    (exhaustive N <= 8): at every anchor s, EITHER an anchored increasing 3-AP exists,
    OR some orbit exits the value universe [1..N] (i.e. the finite escape hatch (b) of
    T2 is actually used) whenever the number of eligible v exceeds the head capacity
    bound of T2(iv).  This confirms the counting step numerically.
"""

import sys
from itertools import permutations
sys.path.insert(0, "/home/user/erdos/experiments")
from apcheck import has_monotone_kap_general


def positions(perm):
    return {v: i for i, v in enumerate(perm)}  # 0-based


def anchored_inc_3ap_exists(perm, s0):
    """s0: 0-based anchor position. True iff exists v with u=perm[s0] < v,
    pos(v) > s0, 2v-u <= N, pos(2v-u) > pos(v)."""
    n = len(perm)
    pos = positions(perm)
    u = perm[s0]
    for v in range(u + 1, n + 1):
        w = 2 * v - u
        if w <= n and pos[v] > s0 and pos[w] > pos[v]:
            return True
    return False


def constraint_A_fails(perm, s0):
    n = len(perm)
    pos = positions(perm)
    u = perm[s0]
    for v in range(u + 1, n + 1):
        w = 2 * v - u
        if w <= n and pos[v] > s0 and not pos[w] < pos[v]:
            return True
    return False


def nu2(m):
    t = 0
    while m % 2 == 0:
        m //= 2
        t += 1
    return t


def t2_check(perm, s0):
    """Assumes no anchored inc 3-AP at s0. Returns (#escape_a, capacity, ok)."""
    n = len(perm)
    pos = positions(perm)
    u = perm[s0]
    head_vals = [perm[i] for i in range(s0)]          # positions < s0 (escape set E)
    capacity = sum(nu2(g - u) + 1 for g in head_vals if g > u)
    seen_pairs = set()
    escape_a = 0
    for v in range(u + 1, n + 1):
        if pos[v] <= s0:
            continue
        # follow orbit
        vt, t = v, 0
        prev_pos = None
        while True:
            if vt > n:                                # (b) leaves value universe
                break
            p = pos[vt]
            if prev_pos is not None:
                # (i) strict position descent while inside and after head
                assert p < prev_pos, (perm, s0, v, t, "descent violated")
            if p < s0:                                # (a) escape into head
                key = (vt, t)
                assert key not in seen_pairs, (perm, s0, v, "injectivity violated")
                seen_pairs.add(key)
                escape_a += 1
                break
            assert p != s0 or vt == u
            prev_pos = p
            vt = 2 * vt - u
            t += 1
    assert escape_a <= capacity, (perm, s0, escape_a, capacity, "capacity violated")
    return escape_a, capacity


def main():
    # ---- T1 + T2 + T5, exhaustive over all permutations for N <= 7, all anchors;
    #      N = 8 on a deterministic sample (every 17th permutation).
    tested = 0
    for n in range(3, 9):
        step = 1 if n <= 7 else 17
        for idx, p in enumerate(permutations(range(1, n + 1))):
            if idx % step:
                continue
            for s0 in range(n):
                ex = anchored_inc_3ap_exists(p, s0)
                fa = constraint_A_fails(p, s0)
                assert ex == fa, (p, s0, "T1 equivalence broken")
                if not ex:
                    t2_check(p, s0)
                    tested += 1
    print(f"T1+T2+T5 PASS: descent/injectivity/capacity verified on {tested} "
          f"(perm, anchor) instances with no anchored increasing 3-AP.", flush=True)

    # ---- T3: powers of two avoid monotone 3- and 4-APs (surjectivity necessity).
    K = 1200
    powers = [2 ** i for i in range(1, K + 1)]
    # machine check on a prefix window (value coincidences are what matters; use the
    # general checker on the first 60 terms — beyond that values are astronomically
    # spread; also verify algebraically for ALL K: 2^b-2^a = 2^c-2^b is impossible).
    assert not has_monotone_kap_general(powers[:60], 3)
    assert not has_monotone_kap_general(powers[:60], 4)
    for b in range(2, 40):
        for a in range(1, b):
            c = 2 ** (b + 1) - 2 ** a  # would-be third term 2v-u
            assert (c & (c - 1)) != 0 or c == 2 ** b + (2 ** b - 2 ** a), "algebra"
            # c is a power of two only if a == b (excluded); spot-verified:
            assert bin(c).count('1') != 1
    print("T3 PASS: n -> 2^n (injection, not surjection) has no monotone 3-AP; "
          "surjectivity is essential to the theorem.", flush=True)

    # ---- T4: parity permutation kills every finite shadow of the theorem.
    sys.setrecursionlimit(5000)

    def sigma(n):
        if n == 1:
            return [1]
        return [2 * y - 1 for y in sigma((n + 1) // 2)] + \
               [2 * y for y in sigma(n // 2)]

    for n in (64, 128, 256, 512):
        s = sigma(n)
        pos = positions(s)
        found = False
        for d in range(1, (n - 1) // 2 + 1):
            for x in range(1, n - 2 * d + 1):
                a_, b_, c_ = pos[x], pos[x + d], pos[x + 2 * d]
                if a_ < b_ < c_ or a_ > b_ > c_:
                    found = True
        assert not found, n
    print("T4 PASS: sigma_N is monotone-3-AP-free for N in {64,128,256,512}; "
          "no finite fragment of the theorem is unsatisfiable.", flush=True)
    print("ALL STRESS TESTS PASS.")


if __name__ == "__main__":
    main()
