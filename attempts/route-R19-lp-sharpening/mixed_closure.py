"""mixed_closure.py -- the TWO-ORIENTATION forcing closure (R19's main new tool).

CORE Theorem 16 (increasing orientation only):
   (I-step)  if u-2d >= 1 and pos(u-2d) < pos(u-d) < pos(u)   ["u open at d"]
             then pos(u+d) < pos(u).
   Reason: else (u-2d, u-d, u, u+d) is an INCREASING monotone 4-AP.

NEW dual rule, using the DECREASING orientation:
   (D-step)  if u-d >= 1 and pos(u+2d) < pos(u+d) < pos(u)    ["u co-open at d"]
             then pos(u-d) < pos(u).
   Reason: else (u+2d, u+d, u, u-d) read in increasing position order is a
   DECREASING monotone 4-AP (values u+2d, u+d, u, u-d, common difference -d).

Both rules produce PREDECESSORS of u.  The MIXED forcing digraph has, at u, the
up-edges u -> u+d (d an open scale, d <= (u-1)/2) and the down-edges u -> u-d
(d a co-open scale, 1 <= d <= u-1).  Out-degree at u is < 1.5u, so the digraph is
finitely branching, and the mixed closure Cl_pm(u) satisfies
      Cl_pm(u) \ {u}  subset  pred(u),      |Cl_pm(u)| <= pos(u).
Hence (Koenig, exactly as in Theorem 16(c)):
   196-YES  <=>  every monotone-4-AP-free permutation of N admits an infinite
                 MIXED forcing chain.

The triadic permutation (CORE Thm 14) satisfies the I-rule (it has no increasing
4-AP) but VIOLATES the D-rule, precisely because of its decreasing in-block runs --
this is the invariant asked for in R19 mission item (2).

Checks:
 (M1) exhaustive: on every monotone-4-AP-free permutation of [1..N], N <= 9, both
      steps hold and |Cl_pm(u)| <= pos(u).
 (M2) on the triadic permutation: the I-step holds everywhere, the D-step fails, and
      the mixed closure escapes pred(u) -- quantified.
 (M3) measurement of mixed closure sizes on SAT-found plain (both-orientation)
      avoiders, compared with the pure-increasing closures of Theorem 16.
"""

import sys
from itertools import permutations

sys.path.insert(0, "/home/user/erdos/experiments")
sys.path.insert(0, "/home/user/erdos/attempts/route-R19-lp-sharpening")
from apcheck import has_monotone_kap_pos
from r19lib import triadic, pos_array, has_inc_4ap, has_dec_4ap


def open_scales(pos, u, N):
    """I-rule triggers at u: d>=1, u-2d>=1, pos[u-2d]<pos[u-d]<pos[u]. Target u+d."""
    out = []
    d = 1
    while u - 2 * d >= 1:
        if pos[u - 2 * d] < pos[u - d] < pos[u]:
            out.append(d)
        d += 1
    return out


def coopen_scales(pos, u, N):
    """D-rule triggers at u: d>=1, u-d>=1, u+2d<=N, pos[u+2d]<pos[u+d]<pos[u].
    Target u-d."""
    out = []
    d = 1
    while u - d >= 1 and u + 2 * d <= N:
        if pos[u + 2 * d] < pos[u + d] < pos[u]:
            out.append(d)
        d += 1
    return out


def mixed_closure(pos, u0, N, use_I=True, use_D=True):
    seen = {u0}
    stack = [u0]
    while stack:
        u = stack.pop()
        tgts = []
        if use_I:
            tgts += [u + d for d in open_scales(pos, u, N) if u + d <= N]
        if use_D:
            tgts += [u - d for d in coopen_scales(pos, u, N)]
        for w in tgts:
            if 1 <= w <= N and w not in seen:
                seen.add(w)
                stack.append(w)
    return seen


def audit_board(perm, use_I=True, use_D=True):
    """Returns (max closure size, max closure/pos ratio); raises on a violation."""
    N = len(perm)
    pos = pos_array(perm)
    worst = 0
    for u in range(1, N + 1):
        if use_I:
            for d in open_scales(pos, u, N):
                if u + d <= N:
                    assert pos[u + d] < pos[u], ("I-STEP VIOLATION", perm, u, d)
        if use_D:
            for d in coopen_scales(pos, u, N):
                assert pos[u - d] < pos[u], ("D-STEP VIOLATION", perm, u, d)
        cl = mixed_closure(pos, u, N, use_I, use_D)
        for w in cl:
            if w != u:
                assert pos[w] < pos[u], ("CLOSURE VIOLATION", perm, u, w)
        assert len(cl) <= pos[u], ("CLOSURE SIZE VIOLATION", perm, u, len(cl), pos[u])
        worst = max(worst, len(cl))
    return worst


def triadic_report(N):
    """M2: on triadic, count D-step violations and closure escapes."""
    perm = triadic(N)
    pos = pos_array(perm)
    assert not has_inc_4ap(perm)
    iviol = dviol = 0
    trig_I = trig_D = 0
    for u in range(1, N + 1):
        for d in open_scales(pos, u, N):
            if u + d <= N:
                trig_I += 1
                if not pos[u + d] < pos[u]:
                    iviol += 1
        for d in coopen_scales(pos, u, N):
            trig_D += 1
            if not pos[u - d] < pos[u]:
                dviol += 1
    # how badly does the mixed closure escape pred(u)?
    escapes = 0
    worst_ratio = 0.0
    for u in range(1, N + 1):
        cl = mixed_closure(pos, u, N, True, True)
        bad = sum(1 for w in cl if w != u and pos[w] > pos[u])
        if bad:
            escapes += 1
        worst_ratio = max(worst_ratio, len(cl) / pos[u])
    return dict(N=N, I_triggers=trig_I, I_violations=iviol,
                D_triggers=trig_D, D_violations=dviol,
                closure_escapes=escapes, max_size_over_pos=worst_ratio)


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"

    if mode in ("all", "M1"):
        print("== M1: exhaustive audit of I-step, D-step, mixed closure on ALL "
              "monotone-4-AP-free permutations of [1..N] ==")
        for N in range(4, 10):
            cnt = 0
            worst = 0
            for p in permutations(range(1, N + 1)):
                if has_monotone_kap_pos(p, 4):
                    continue
                cnt += 1
                worst = max(worst, audit_board(list(p)))
            print(f"  N={N}: {cnt:7d} avoiders, I+D+closure PASS, "
                  f"max mixed closure = {worst}", flush=True)

    if mode in ("all", "M2"):
        print("\n== M2: triadic (no increasing 4-AP; has decreasing 4-APs) ==")
        for N in (26, 80, 242, 728, 2186):
            r = triadic_report(N)
            print(f"  N={r['N']:5d}: I-triggers={r['I_triggers']:7d} violations={r['I_violations']}"
                  f" | D-triggers={r['D_triggers']:7d} violations={r['D_violations']:7d}"
                  f" | u with escaping mixed closure = {r['closure_escapes']}/{r['N']}"
                  f" | max |Cl_pm(u)|/pos(u) = {r['max_size_over_pos']:.3f}", flush=True)
        print("  -> the D-step is violated by triadic at a positive rate: this is an"
              " invariant that triadic fails ONLY through its decreasing in-block runs.")

    if mode in ("all", "M3"):
        print("\n== M3: mixed vs increasing-only closures on SAT-found PLAIN avoiders ==")
        from sat_order import solve
        for N in (40, 60, 80, 100, 130, 160):
            sat, perm = solve(N, inc4=True, dec4=True)
            assert sat and not has_monotone_kap_pos(perm, 4)
            pos = pos_array(perm)
            audit_board(perm)                      # both rules must hold
            inc_sizes, mix_sizes = [], []
            for u in range(1, N + 1):
                inc_sizes.append(len(mixed_closure(pos, u, N, True, False)))
                mix_sizes.append(len(mixed_closure(pos, u, N, True, True)))
            print(f"  N={N:4d}: max |Cl_inc| = {max(inc_sizes):4d}, "
                  f"max |Cl_pm| = {max(mix_sizes):4d}  "
                  f"(mean {sum(mix_sizes)/N:6.1f} vs {sum(inc_sizes)/N:6.1f}); "
                  f"sum|Cl_pm| / (N(N+1)/2) = {sum(mix_sizes)/(N*(N+1)/2):.3f}", flush=True)
