"""t01_scan.py — does the T=1 constraint system survive as N grows, and does the zero set
densify as Proposition 38 predicts? Full condition (ii) + positive descent rate along every
AP of step <= Q + no level set periodic mod m <= M. Every SAT model is re-verified against
the literal definition of (ii)."""
import sys, time
sys.path.insert(0, '/home/user/erdos/experiments')
from t01_full import build
from farleft import blk
from pysat.solvers import Cadical195, Glucose42

for N in (150, 200, 260, 340, 440, 570, 740):
    t0 = time.time()
    cl, pool, T, nap = build(N, Q=4, M=6, L=8)
    S = Cadical195(bootstrap_with=cl); sat = S.solve()
    model = set(S.get_model()) if sat else None; S.delete()
    dt = time.time() - t0
    if sat:
        tv = [0] + [1 if T(v) in model else 0 for v in range(1, N + 1)]
        c = [blk(v, 3) + tv[v] for v in range(N + 1)]
        bad = None
        for d in range(1, N // 3 + 1):
            for x in range(1, N - 3 * d + 1):
                s = [c[x + i * d] for i in range(4)]
                if s[0] < s[1] < s[2] < s[3] or s[0] > s[1] > s[2] > s[3]:
                    bad = (x, d, s); break
            if bad: break
        z = sum(1 for v in range(1, N + 1) if tv[v] == 0)
        print(f"N={N}: SAT ({dt:.0f}s) |Z|={z} density={z/N:.3f} "
              f"recheck={'OK' if not bad else 'FAILED ' + str(bad)}", flush=True)
    else:
        g = Glucose42(bootstrap_with=cl).solve()
        print(f"N={N}: UNSAT ({dt:.0f}s); glucose agrees: {not g}", flush=True)
        print("   ==> finite theorem at T=1 with these parameters.", flush=True)
        break
