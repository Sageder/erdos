import sys
sys.path.insert(0, '/home/user/erdos/attempts/route-R23-refute')
from classorder import solve_classorder, classes_of, check
from verify import W1, W2

Ns = [int(x) for x in (sys.argv[1].split(',') if len(sys.argv) > 1 else
                       ["40", "60", "90", "130", "180", "250"])]
cfgs = []
for b in (4, 5):
    for hn, h in [("h=1", lambda M: 1), ("h=M+1", lambda M: M + 1)]:
        cfgs.append((f"W1 b={b} {hn}", b, lambda N, b=b, h=h: W1(N, b, h)[0]))
for b in (3, 4):
    cfgs.append((f"W2 b={b} tau=2,0", b, lambda N, b=b: W2(N, b, lambda K: 2 if K % 2 == 0 else 0)))

for tag, b, mk in cfgs:
    for N in Ns:
        t = mk(N)
        c = classes_of(t, N, b)
        res, perm = check(f"{tag} N={N}", c, N)
        if res in ("UNSAT", "UNKNOWN", "DISAGREE"):
            break
