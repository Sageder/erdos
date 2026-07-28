"""cpsat_profile.py — CP-SAT model for phi-bounded monotone-4-AP-free permutations of
[1..N].  Used to push the alpha-wall measurement alpha*(N) to larger N than the
lazy-transitivity CEGAR reaches.

Model: integer pos[v] in [1, min(phi(v), N)], AllDifferent, and for every (x,e) with
x+3e <= N a pair of clauses over reified literals b[u,w] <=> pos[u] < pos[w].
Every SAT answer is decoded and re-verified with the trusted checker apcheck.py and
against the profile; UNSAT/INFEASIBLE is a theorem modulo solver correctness.
"""
import sys, math, time
sys.path.insert(0, '/home/user/erdos/experiments')
from apcheck import has_monotone_kap_pos
from ortools.sat.python import cp_model


def phi_vlogv(alpha):
    return lambda v: max(1, math.ceil(alpha * v * math.log2(2 * v)))


def phi_lin(C):
    return lambda v: max(1, int(C * v))


def solve(N, phi, workers=4, tl=600.0, log=False):
    m = cp_model.CpModel()
    pos = {}
    for v in range(1, N + 1):
        ub = min(int(phi(v)), N)
        if ub < 1:
            return "INFEASIBLE-PROFILE", None
        pos[v] = m.NewIntVar(1, ub, f"p{v}")
    m.AddAllDifferent([pos[v] for v in range(1, N + 1)])
    lit = {}

    def bef(u, w):
        """literal for pos[u] < pos[w]"""
        k = (u, w)
        if k in lit:
            return lit[k]
        rk = (w, u)
        if rk in lit:
            lit[k] = lit[rk].Not()
            return lit[k]
        b = m.NewBoolVar(f"b{u}_{w}")
        m.Add(pos[u] < pos[w]).OnlyEnforceIf(b)
        m.Add(pos[u] > pos[w]).OnlyEnforceIf(b.Not())
        lit[k] = b
        return b

    for e in range(1, (N - 1) // 3 + 1):
        for x in range(1, N - 3 * e + 1):
            a = [bef(x + k * e, x + (k + 1) * e) for k in range(3)]
            m.AddBoolOr([a[0].Not(), a[1].Not(), a[2].Not()])
            m.AddBoolOr([a[0], a[1], a[2]])
    s = cp_model.CpSolver()
    s.parameters.num_search_workers = workers
    s.parameters.max_time_in_seconds = tl
    s.parameters.log_search_progress = log
    r = s.Solve(m)
    if r == cp_model.OPTIMAL or r == cp_model.FEASIBLE:
        p = {v: s.Value(pos[v]) for v in range(1, N + 1)}
        perm = [v for v, _ in sorted(p.items(), key=lambda kv: kv[1])]
        assert sorted(perm) == list(range(1, N + 1))
        assert not has_monotone_kap_pos(perm, 4), "model is not an avoider!"
        assert all(p[v] <= phi(v) for v in range(1, N + 1)), "profile violated"
        return "SAT", perm
    if r == cp_model.INFEASIBLE:
        return "UNSAT", None
    return "UNKNOWN", None


if __name__ == "__main__":
    mode = sys.argv[1]
    vals = [float(x) for x in sys.argv[2].split(',')]
    Ns = [int(x) for x in sys.argv[3].split(',')]
    tl = float(sys.argv[4]) if len(sys.argv) > 4 else 600.0
    for a in vals:
        phi = phi_vlogv(a) if mode == "alpha" else phi_lin(a)
        for N in Ns:
            t0 = time.time()
            res, perm = solve(N, phi, tl=tl)
            dt = time.time() - t0
            tag = "vlogv alpha" if mode == "alpha" else "linear C"
            print(f"{tag}={a} N={N}: {res} ({dt:.0f}s)", flush=True)
            if res == "SAT":
                with open(f"/home/user/erdos/attempts/route-R20-vlogv/cw_{mode}{a}_N{N}.txt", "w") as f:
                    f.write(repr(perm))
            else:
                break
