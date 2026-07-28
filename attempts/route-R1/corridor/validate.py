"""validate.py -- cross-validation of cutcore.py.

(1) brute_oracle (literal definition, trusted apcheck) vs solve_eager vs solve_cpsat
    on EVERY cut set with max <= 9 whose block factorial product is small.
(2) reproduce the published R1 / R1-audit verdicts.
"""
import itertools
import math
import sys

sys.path.insert(0, "/home/user/erdos/attempts/route-R1/corridor")
from cutcore import brute_oracle, solve_eager, solve_cpsat, verify, blocks_of

MAXV = 9
CAP = 400000

def all_cutsets(maxv):
    out = []
    for k in range(1, maxv + 1):
        for S in itertools.combinations(range(1, maxv + 1), k):
            bl = blocks_of(S)
            work = 1
            for lo, hi in bl:
                work *= math.factorial(hi - lo + 1)
            if work <= CAP:
                out.append(list(S))
    return out

def main():
    sets = all_cutsets(MAXV)
    print(f"# cross-validating {len(sets)} cut sets with max <= {MAXV}")
    bad = 0
    nsat = 0
    for S in sets:
        rb, wb = brute_oracle(S)
        re_, we = solve_eager(S)
        rc, wc = solve_cpsat(S)
        if not (rb == re_ == rc):
            print(f"MISMATCH {S}: brute={rb} eager={re_} cpsat={rc}")
            bad += 1
            continue
        if rb == 'SAT':
            nsat += 1
            verify(S, wb)
            verify(S, we)
            verify(S, wc)
    print(f"# mismatches: {bad}   (SAT: {nsat}, UNSAT: {len(sets)-nsat})")

    print("\n# published verdicts (R1 REPORT + R1/final AUDIT)")
    EXPECT = {
        (8, 26, 80): 'UNSAT', (8, 26, 76): 'SAT', (4, 16, 56): 'UNSAT',
        (4, 16, 68): 'SAT', (2, 4, 10): 'SAT', (4, 10, 28): 'SAT',
        (1, 2, 4, 10, 28): 'SAT', (1, 2, 4, 10, 28, 82): 'UNSAT',
        (1, 2, 4, 10, 28, 83): 'UNSAT', (1, 3, 4, 10, 28, 82): 'UNSAT',
        (1, 2, 4, 10, 30, 88): 'UNSAT',
        (10, 28, 82): 'UNSAT', (4, 10, 28, 82): 'UNSAT', (2, 10, 28, 82): 'UNSAT',
        (11, 31, 91): 'UNSAT', (12, 34, 100): 'UNSAT', (13, 37, 109): 'UNSAT',
        (10, 29, 85): 'UNSAT', (10, 30, 88): 'UNSAT', (16, 46, 136): 'UNSAT',
        (1, 2, 4): 'SAT', (3, 4, 10): 'SAT', (5, 6, 16): 'SAT',
        (6, 16, 46): 'SAT', (7, 8, 22): 'SAT', (8, 22, 64): 'SAT',
        (5, 13, 37): 'SAT',
        (8, 27, 79): 'SAT', (9, 27, 79): 'UNSAT',
        (8, 28, 82): 'SAT', (9, 28, 82): 'UNSAT',
        (8, 26, 130): 'SAT', (9, 26, 130): 'UNSAT',
        (8, 28, 140): 'SAT', (9, 28, 140): 'UNSAT',
        (9, 28, 150): 'UNSAT', (10, 28, 150): 'UNSAT',
        (7, 20, 100): 'SAT', (8, 20, 100): 'UNSAT',
        (1, 5, 6, 16, 46): 'SAT', (1, 7, 8, 22, 64): 'SAT',
        (2, 8, 26, 76): 'SAT', (2, 8, 26, 140): 'SAT',
        (5, 25, 125): 'SAT',
    }
    agree = dis = 0
    for S, exp in sorted(EXPECT.items(), key=lambda kv: kv[0][-1]):
        r, w = solve_eager(list(S))
        ok = (r == exp)
        if r == 'SAT':
            verify(list(S), w)
        print(f"  {list(S)}: eager={r} expected={exp} {'OK' if ok else '*** DISAGREE'}")
        agree += ok
        dis += (not ok)
    print(f"# agree {agree}, disagree {dis}")

if __name__ == "__main__":
    main()
