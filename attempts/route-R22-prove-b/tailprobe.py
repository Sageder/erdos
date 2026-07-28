"""tailprobe.py -- route R22: are the head-delay UNSATs a SMALL-BLOCK artifact?

CORE.md Lemma 24 / Corollary 26: every VALUE-TAIL {V0, V0+1, ...} of a monotone-4-AP-free
permutation of N is, after the shift v -> v-V0+1 (an affine bijection carrying 4-APs to
4-APs), again a monotone-4-AP-free permutation of N.  So a necessary condition for an
architecture to be viable is: for every V0 and every W, the class architecture restricted
to the window [V0..W] admits a 4-AP-free within-class order.

The window is relabelled 1..L and handed to route R20's validated CEGAR class solver;
its UNSATs are re-verified here with the eager encoding + 3 solvers when L is small
enough (see eager.py / `recheck`).
"""

import sys, time
sys.path.insert(0, '/home/user/erdos/experiments')
sys.path.insert(0, '/home/user/erdos/attempts/route-R20-vlogv')
sys.path.insert(0, '/home/user/erdos/attempts/route-R22-prove-b')
from classsat import solve_classes                                    # noqa: E402
from apcheck import has_monotone_kap_pos                              # noqa: E402
from arch import blk                                                  # noqa: E402
from eager import run as eager_run                                    # noqa: E402


def head_class(b, s_of_m, K_of_m):
    def c(v):
        m = blk(v, b)
        return m + (K_of_m(m) if v < b ** m + s_of_m(m) else 0)
    return c


def window_test(cf, V0, W, tag, recheck_limit=300):
    L = W - V0 + 1
    cw = lambda i: cf(i + V0 - 1)
    t0 = time.time()
    res, perm, rounds = solve_classes(L, cw)
    dt = time.time() - t0
    extra = ""
    if res == "SAT":
        assert not has_monotone_kap_pos(perm, 4)
        pos = {v: i + 1 for i, v in enumerate(perm)}
        extra = f"  maxpos/idx={max(pos[v] / v for v in range(1, L + 1)):.2f}"
    print(f"{tag}  window [{V0}..{W}] (L={L}): {res} ({dt:.0f}s, {rounds} rounds){extra}",
          flush=True)
    if res == "UNSAT" and L <= recheck_limit:
        eager_run(L, cw, f"   re-verify {tag} [{V0}..{W}]")
    return res


if __name__ == "__main__":
    B = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    cf = head_class(B, lambda m: m + 1, lambda m: m)
    tag = f"HEAD({B},s=m+1,K=m)"
    starts = [1, B ** 2, B ** 3, B ** 4] if B == 3 else [1, B ** 2, B ** 3]
    for V0 in starts:
        for mult in (3, 6, 9, 12, 18, 27):
            W = V0 * mult
            if W - V0 + 1 < 20 or W - V0 + 1 > 700:
                continue
            r = window_test(cf, V0, W, tag)
            if r != 'SAT':
                break
