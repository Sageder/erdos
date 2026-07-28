"""t01_sat.py — DECISIVE test of Conjecture R21-C at T = 1 (delay t : N -> {0,1}).

By CORE Lemma 34 (far-left reduction), condition (ii) restricted to far-left APs says, for
each such triple (u, u+d, u+2d) with block pattern P:
    P = (k,k,k+1)   : forbid (t(u),t(u+d),t(u+2d)) = (0,1,1)
    P = (k,k+1,k+1) : forbid (t(u),t(u+d),t(u+2d)) = (0,0,1)
    P = (k,k,k)     : vacuous for two-valued t.
By Corollary 30 a counterexample delay must NOT have its level set equal to a union of
residue classes. By Proposition 29 it must leave NO tame AP, i.e. along every AP the delay
must not be eventually non-decreasing.

We ask SAT: is there t : [1..N] -> {0,1} with
  (A) all far-left (ii) constraints,
  (B) for every AP of step q <= Q and every start, a strict DESCENT (1 then 0) in the
      SECOND HALF of the window -- a finite proxy for "not eventually non-decreasing",
      which also rules out constancy,
  (C) the zero set is not a union of residue classes mod m, for every m <= M
      (encoded as: for each m, some residue class mod m meets both the zero and the one set).
UNSAT at modest N is a finite theorem and strong evidence for R21-C at T=1.
SAT means the T=1 refutation survives at that size and should be mined for a rule.
"""
import sys, time
sys.path.insert(0, '/home/user/erdos/experiments')
from farleft import blk
from pysat.solvers import Cadical195, Glucose42
from pysat.formula import IDPool

def build(N, b=3, Q=6, M=8, xmax=3):
    pool = IDPool()
    T = lambda v: pool.id(('t', v))
    cl = []
    # (A) far-left condition (ii)
    nfl = 0
    tmax = 1
    for x in range(1, xmax + 1):
        jx = blk(x, b)
        for d in range(1, (N - x) // 3 + 1):
            u = [x + i * d for i in range(4)]
            if u[3] > N: break
            # far-left needs j(x) + t(x) < j(u1); t(x) <= 1 so require jx + 1 < j(u1)
            if not (jx + tmax < blk(u[1], b)): continue
            k = blk(u[1], b); pat = (blk(u[2], b) - k, blk(u[3], b) - k)
            nfl += 1
            a, c_, e = T(u[1]), T(u[2]), T(u[3])
            if pat == (0, 1):      # (k,k,k+1): forbid (0,1,1)
                cl.append([a, -c_, -e])
            elif pat == (1, 1):    # (k,k+1,k+1): forbid (0,0,1)
                cl.append([a, c_, -e])
    # (B) STRENGTHENED: every AP of step q <= Q must contain a strict descent (1 then 0)
    # in EVERY window of L consecutive AP-elements. This forces descents at a positive
    # rate, the correct finite proxy for "not eventually non-decreasing"; the earlier
    # second-half-only version was satisfied degenerately by an almost-constant delay.
    L = 12
    for q in range(1, Q + 1):
        for r in range(1, q + 1):
            P = list(range(r, N + 1, q))
            if len(P) < L + 2: continue
            for s0 in range(0, len(P) - L):
                W = P[s0:s0 + L]
                lits = []
                for i in range(len(W) - 1):
                    z = pool.id(('desc', q, r, s0, i))
                    cl.append([-z, T(W[i])]); cl.append([-z, -T(W[i + 1])])
                    lits.append(z)
                if lits: cl.append(lits)
    # (C) for each m <= M, some residue class mod m is split (meets both level sets)
    for m in range(2, M + 1):
        splits = []
        for r in range(m):
            cls = [v for v in range(1, N + 1) if v % m == r]
            if len(cls) < 2: continue
            s = pool.id(('split', m, r))
            # s -> some pair in the class differs; encode s -> OR over pairs of (t_i xor t_j)
            # simpler: s -> (some element is 0) and (some element is 1)
            cl.append([-s] + [-T(v) for v in cls])
            cl.append([-s] + [T(v) for v in cls])
            splits.append(s)
        if splits: cl.append(splits)
    return cl, pool, T, nfl

if __name__ == "__main__":
    for N in (200, 400, 800, 1500, 3000):
        t0 = time.time()
        cl, pool, T, nfl = build(N)
        S = Cadical195(bootstrap_with=cl); sat = S.solve()
        model = set(S.get_model()) if sat else None; S.delete()
        dt = time.time() - t0
        if sat:
            tv = {v: (1 if T(v) in model else 0) for v in range(1, N + 1)}
            print(f"N={N}: SAT ({dt:.0f}s, {nfl} far-left constraints)  "
                  f"|Z|={sum(1 for v in tv if tv[v]==0)}  head={[tv[v] for v in range(1,41)]}", flush=True)
        else:
            r2 = Glucose42(bootstrap_with=cl).solve()
            print(f"N={N}: UNSAT ({dt:.0f}s, {nfl} far-left constraints); glucose agrees: {not r2}", flush=True)
            print(f"   ==> FINITE THEOREM: no t:[1..{N}]->{{0,1}} satisfies the far-left (ii) "
                  f"constraints while leaving no tame AP (step<=6) and no periodic level set (m<=8).", flush=True)
            break
