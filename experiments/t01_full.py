"""t01_full.py — DECISIVE test of Conjecture R21-C at T=1 with the FULL condition (ii).

t : [1..N] -> {0,1}, c(v) = floor(log_b v) + t(v). For a 4-AP (x,x+d,x+2d,x+3d) with
block indices j_1<=...<=j_4 (j non-decreasing), write D_i = j_{i+1} - j_i >= 0. Then
  c_i <  c_{i+1}  <=>  t_i - t_{i+1} < D_i
      D_i = 0 : t_i=0 and t_{i+1}=1
      D_i = 1 : NOT(t_i=1 and t_{i+1}=0)
      D_i >= 2: always true
  c_i >  c_{i+1}  <=>  t_i - t_{i+1} > D_i
      D_i = 0 : t_i=1 and t_{i+1}=0
      D_i >= 1: impossible
Condition (ii) forbids all three steps increasing, and all three decreasing.

Added constraints, as before:
 (B) positive descent rate along every AP of step <= Q (finite proxy for "no tame AP";
     the earlier second-half-only proxy was degenerate and is not used),
 (C) no level set is a union of residue classes mod m for m <= M.
UNSAT is a finite theorem supporting R21-C at T=1; SAT is a genuine refutation lead.
"""
import sys, time
sys.path.insert(0, '/home/user/erdos/experiments')
from farleft import blk
from pysat.solvers import Cadical195, Glucose42
from pysat.formula import IDPool


def build(N, b=3, Q=6, M=8, L=12):
    pool = IDPool(); T = lambda v: pool.id(('t', v)); cl = []
    def step_inc(i, j, D, tag):
        """Return a literal equivalent to 'c(i) < c(j)'."""
        if D >= 2: return None                      # always true
        z = pool.id(('inc', tag))
        if D == 1:   # z <=> NOT(t_i and not t_j)
            cl.append([-z, -T(i), T(j)])
            cl.append([z, T(i)]); cl.append([z, -T(j)])
        else:        # D == 0 : z <=> (not t_i) and t_j
            cl.append([-z, -T(i)]); cl.append([-z, T(j)])
            cl.append([z, T(i), -T(j)])
        return z
    def step_dec(i, j, D, tag):
        """Literal equivalent to 'c(i) > c(j)'; impossible unless D == 0."""
        if D >= 1: return False
        z = pool.id(('dec', tag))
        cl.append([-z, T(i)]); cl.append([-z, -T(j)])
        cl.append([z, -T(i), T(j)])
        return z
    nap = 0
    for d in range(1, N // 3 + 1):
        for x in range(1, N - 3 * d + 1):
            u = [x + i * d for i in range(4)]
            js = [blk(v, b) for v in u]
            Ds = [js[i + 1] - js[i] for i in range(3)]
            nap += 1
            # increasing: steps with D>=2 are ALWAYS increasing, so they contribute
            # nothing to the conjunction; forbid the conjunction of the remaining ones.
            incs = [step_inc(u[i], u[i + 1], Ds[i], (x, d, i)) for i in range(3)]
            rem = [z for z in incs if z is not None]
            cl.append([-z for z in rem])            # empty clause if ALL steps forced
            # decreasing: a step with D>=1 can never decrease, so the conjunction is
            # unsatisfiable and needs no clause; only all-D=0 APs constrain.
            decs = [step_dec(u[i], u[i + 1], Ds[i], (x, d, i)) for i in range(3)]
            if all(z is not False for z in decs):
                cl.append([-z for z in decs])
    for q in range(1, Q + 1):                        # (B)
        for r in range(1, q + 1):
            P = list(range(r, N + 1, q))
            if len(P) < L + 2: continue
            for s0 in range(0, len(P) - L):
                W = P[s0:s0 + L]; lits = []
                for i in range(len(W) - 1):
                    z = pool.id(('ds', q, r, s0, i))
                    cl.append([-z, T(W[i])]); cl.append([-z, -T(W[i + 1])]); lits.append(z)
                cl.append(lits)
    for m in range(2, M + 1):                        # (C)
        sp = []
        for r in range(m):
            cls = [v for v in range(1, N + 1) if v % m == r]
            if len(cls) < 2: continue
            s = pool.id(('sp', m, r))
            cl.append([-s] + [-T(v) for v in cls]); cl.append([-s] + [T(v) for v in cls])
            sp.append(s)
        if sp: cl.append(sp)
    return cl, pool, T, nap


if __name__ == "__main__":
    for N in (150, 300, 600, 1200, 2400):
        t0 = time.time(); cl, pool, T, nap = build(N)
        S = Cadical195(bootstrap_with=cl); sat = S.solve()
        model = set(S.get_model()) if sat else None; S.delete()
        dt = time.time() - t0
        if sat:
            tv = [0] + [1 if T(v) in model else 0 for v in range(1, N + 1)]
            # independently re-verify the model against the literal definition of (ii)
            c = [blk(v, 3) + tv[v] for v in range(N + 1)]
            bad = None
            for d in range(1, N // 3 + 1):
                for x in range(1, N - 3 * d + 1):
                    s = [c[x + i * d] for i in range(4)]
                    if s[0] < s[1] < s[2] < s[3] or s[0] > s[1] > s[2] > s[3]:
                        bad = (x, d, s); break
                if bad: break
            print(f"N={N}: SAT ({dt:.0f}s, {nap} APs)  |Z|={sum(1 for v in range(1,N+1) if tv[v]==0)}"
                  f"  re-verified against literal (ii): {'OK' if not bad else f'FAILED {bad}'}", flush=True)
        else:
            r2 = Glucose42(bootstrap_with=cl).solve()
            print(f"N={N}: UNSAT ({dt:.0f}s, {nap} APs); glucose agrees: {not r2}", flush=True)
            print("   ==> FINITE THEOREM supporting R21-C at T=1.", flush=True)
            break
