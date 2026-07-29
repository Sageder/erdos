"""validate.py -- cross-validation of wsys.py against raw enumeration and against
the trusted checkers in /home/user/erdos/experiments/apcheck.py, plus reproduction
of published route-R1 / route-R1-final verdicts.
"""
import sys, itertools, time
sys.path.insert(0, "/home/user/erdos/experiments")
sys.path.insert(0, "/home/user/erdos/attempts/route-W4-accel")
from apcheck import has_monotone_kap_general
import wsys


def brute(cuts, M):
    """Raw enumeration over ALL in-order block layouts of [1..M]; returns True iff
    some layout has no monotone 4-AP (apcheck ground truth) and no C2 violation."""
    Vk = cuts[-1]
    blocks = []
    lo = 1
    for c in list(cuts) + ([M] if M > Vk else []):
        blocks.append(list(range(lo, c + 1)))
        lo = c + 1
    c2 = [(x, d) for d in range(1, Vk // 2 + 1)
          for x in range(1, Vk - 2 * d + 1) if x + 3 * d > M]
    for combo in itertools.product(*[itertools.permutations(b) for b in blocks]):
        seq = [v for part in combo for v in part]
        if has_monotone_kap_general(seq, 4):
            continue
        pos = {v: i for i, v in enumerate(seq)}
        if any(pos[x] < pos[x + d] < pos[x + 2 * d] for x, d in c2):
            continue
        return True, seq
    return False, None


def main():
    print("== A. raw-enumeration validation (small cut sets, all in-order layouts) ==")
    tested = mism = 0
    cases = []
    for M in range(4, 11):
        for k in (1, 2, 3):
            for cuts in itertools.combinations(range(1, M + 1), k):
                if cuts[-1] > M:
                    continue
                blocks = []
                lo = 1
                for c in list(cuts) + ([M] if M > cuts[-1] else []):
                    blocks.append(c - lo + 1)
                    lo = c + 1
                prod = 1
                for b in blocks:
                    prod *= _fact(b)
                if prod > 200000:
                    continue
                cases.append((cuts, M))
    for cuts, M in cases:
        bs, w = brute(cuts, M)
        S = wsys.Sys(cuts, M)
        v, _ = wsys.solve_eager(S)
        sat = (v == 'SAT')
        tested += 1
        if sat != bs:
            mism += 1
            print(f"  MISMATCH cuts={cuts} M={M}: brute={bs} sat={v}")
    print(f"  {tested} cut/horizon systems, {mism} mismatches")

    print("== B. reproduce published verdicts (route-R1 / final AUDIT) ==")
    pub = [((8, 26, 80), None, 'UNSAT'), ((8, 26, 76), None, 'SAT'),
           ((4, 16, 56), None, 'UNSAT'), ((4, 16, 68), None, 'SAT'),
           ((2, 4, 10), None, 'SAT'), ((4, 10, 28), None, 'SAT'),
           ((1, 2, 4, 10, 28), None, 'SAT'), ((10, 28, 82), None, 'UNSAT'),
           ((9, 28, 82), None, 'UNSAT'), ((8, 28, 82), None, 'SAT'),
           ((11, 31, 91), None, 'UNSAT'), ((8, 26, 130), None, 'SAT'),
           ((9, 26, 130), None, 'UNSAT'), ((16, 46, 136), None, 'UNSAT'),
           ((10, 46, 136), None, 'SAT'), ((1, 5, 6, 16, 46), None, 'SAT'),
           ((1, 7, 8, 22, 64), None, 'SAT'), ((2, 8, 26, 76), None, 'SAT'),
           ((1, 2, 4, 10, 28, 82), None, 'UNSAT')]
    bad = 0
    for cuts, M, exp in pub:
        t0 = time.time()
        S = wsys.Sys(cuts, M)
        v, o = wsys.solve_eager(S) if cuts[-1] <= 90 else wsys.solve_lazy(S)
        if v == 'GEOM_DEAD':
            v = 'UNSAT'
        ok = (v == exp)
        extra = ''
        if v == 'SAT':
            wsys.verify(cuts, cuts[-1], o)
            extra = ' witness verified'
        print(f"  {list(cuts)} M={cuts[-1]}: {v} (expect {exp}) "
              f"{'OK' if ok else '*** DISAGREE'}{extra} [{time.time()-t0:.0f}s]")
        bad += (not ok)
    print(f"  disagreements: {bad}")

    print("== C. CP-SAT (second encoding) spot agreement ==")
    for cuts in [(8, 26, 80), (8, 26, 76), (10, 28, 82), (8, 28, 82), (2, 4, 10)]:
        S = wsys.Sys(cuts)
        a, _ = wsys.solve_eager(S)
        b, _ = wsys.solve_cpsat(S, tlimit=300)
        print(f"  {list(cuts)}: sat={a} cpsat={b} {'OK' if a == b else '*** DISAGREE'}")


def _fact(n):
    r = 1
    for i in range(2, n + 1):
        r *= i
    return r


if __name__ == '__main__':
    main()
