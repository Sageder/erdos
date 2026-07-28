"""mus.py -- distil the head-delay UNSAT to a minimal set of VALUES (single-deletion
minimal).  Every verdict is taken with two solvers that must agree.
"""
import sys
sys.path.insert(0, '/home/user/erdos/attempts/route-R22-prove-b')
from window import verdict_set
from eager import head_class

if __name__ == "__main__":
    b = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    N = int(sys.argv[2]) if len(sys.argv) > 2 else 90
    cf = head_class(b, lambda m: m + 1, lambda m: m)
    S = list(range(1, N + 1))
    v0, _ = verdict_set(S, cf)
    assert v0 == 'UNSAT', v0
    changed = True
    while changed:
        changed = False
        for v in list(S):
            T = [u for u in S if u != v]
            if len(T) >= 4 and verdict_set(T, cf)[0] == 'UNSAT':
                S = T
                changed = True
    print(f"b={b}, start [1..{N}] -> single-deletion-minimal UNSAT set ({len(S)} values):")
    print("   values :", S)
    print("   classes:", [cf(v) for v in S])
