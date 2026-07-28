"""
A_sat_cover.py   -- Route A, Erdos problem 273.

CLAIM TESTED (per invocation): for the given modulus L and "world" W in {E,H}, does there
exist a family of residue classes  a_n (mod n),  with the moduli n PAIRWISE DISTINCT,
each n a divisor of L lying in W, whose union is
      all of Z/L                          (mode = full)
   or Z/L minus the single residue 0       (mode = relaxed; then every a_n != 0 mod n)?

  W = E : n >= 4 and n+1 prime           (the moduli of Erdos 273 itself)
  W = H : m >= 2 and 2m+1 prime          (the "halved" world; by Lemma A1 an E-covering
          at L = 2*Lh is exactly a pair of DISJOINT H-coverings at Lh, so H-UNSAT at Lh
          implies E-UNSAT at 2*Lh)

ENCODING
  vars      x[n][a]  (n a modulus, a in Z/n)  = "class a mod n is one of the chosen classes"
  AMO       at most one a per n -- Sinz sequential (ladder) encoding, LINEAR size
  used[n]   <-> OR_a x[n][a]
  coverage  for each residue r that must be covered:  OR_n x[n][r mod n]
  symmetry  (mode=full only) translation r -> r+s maps solutions to solutions; sound break
            "the smallest USED modulus has residue 0":
              x[n_i][a] -> (used_1 v ... v used_{i-1})     for every a != 0
            applied only for the first --symtop moduli (for larger i the premise
            "all smaller moduli unused" is nearly vacuous and the clauses are huge).
            In mode=relaxed the translation symmetry is already used up by demanding that
            the uncovered residue be 0, so no break is added.

CONCLUSION: printed per run; SAT results are dumped as JSON certificates and must be
re-checked by the independent script A_verify_cert.py.  Recorded in
attempts/route-A-satsearch/FINDINGS.md.
"""
import argparse, json, os, sys, time, threading
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from A_common import D_E, D_H, D_V, budget, verify_cover, in_E as is_E_mod
from fractions import Fraction
from math import gcd


class CNFSink:
    """Streams clauses straight into a pysat solver, counting as it goes."""

    def __init__(self, solver):
        self.s = solver
        self.nclauses = 0
        self.nlits = 0

    def add(self, cl):
        self.s.add_clause(cl)
        self.nclauses += 1
        self.nlits += len(cl)

    def add_many(self, cls):
        add = self.s.add_clause
        n = 0
        for cl in cls:
            add(cl)
            n += 1
        self.nclauses += n
        self.nlits += n * len(cls[0]) if cls else 0


def minimal_hitting_sets(mods, threshold, smax=5, pool=14, maxsets=400):
    """All minimal S subset of the `pool` smallest moduli, |S| <= smax, with
       sum_{n in S} 1/n > threshold.
    Soundness of the clause derived from such an S: if a sub-family F of the moduli must
    satisfy sum_{n in F} 1/n >= h, and threshold = B - h with B = sum over ALL moduli,
    then sum over (all \\ S) = B - sum_S < h, so F cannot avoid S entirely."""
    from itertools import combinations
    cand = mods[:pool]
    found, fsets = [], []
    for size in range(1, smax + 1):
        for S in combinations(cand, size):
            SS = set(S)
            if any(f <= SS for f in fsets):
                continue
            if sum(Fraction(1, n) for n in S) > threshold:
                found.append(S)
                fsets.append(SS)
                if len(found) >= maxsets:
                    return found
    return found


def overlap_sets(hmods, bound, pool=18, smax=4, maxsets=3000, strict=False):
    """LEMMA A2 (forced-overlap bound).  Let a family of residue classes with moduli
    m_1,...,m_r (distinct, > 1) cover Z.  Its EXCESS  X := sum 1/m_i - 1  is >= 0 and is
    monotone: for any subfamily T,
            X  >=  sum_{m in T} 1/m  -  density( union_{m in T} A_m ).
    If the moduli in T are PAIRWISE COPRIME then, by CRT, the classes behave like
    independent events whatever the residues are, and
            density(union_{m in T} A_m) = 1 - prod_{m in T} (1 - 1/m)   exactly.
    Hence   X >= f(T) := sum_{m in T} 1/m - 1 + prod_{m in T}(1 - 1/m),
    and f is monotone increasing in T.
    So if f(T) exceeds the maximal admissible excess, the whole of T cannot belong to one
    and the same covering family.  Returns the minimal such T (as tuples of moduli)."""
    from itertools import combinations
    cand = hmods[:pool]
    found = []
    for size in range(2, smax + 1):
        for T in combinations(cand, size):
            if any(set(f) <= set(T) for f in found):
                continue
            ok = all(gcd(a, b) == 1 for a, b in combinations(T, 2))
            if not ok:
                continue
            s = sum(Fraction(1, m) for m in T)
            pr = Fraction(1)
            for m in T:
                pr *= Fraction(m - 1, m)
            if (s - 1 + pr > bound) if strict else (s - 1 + pr >= bound):
                found.append(T)
                if len(found) >= maxsets:
                    return found
    return found


def build(solver, L, mods, mode, sym, symtop, chain, verbose=True, halfbudget=True,
          world="E"):
    """Returns (base, nvars, sink).  DIMACS var for (i,a) is base[i]+a+1."""
    sink = CNFSink(solver)
    k = len(mods)
    base, off = [0] * k, 0
    for i, n in enumerate(mods):
        base[i] = off
        off += n
    nv = off

    def X(i, a):
        return base[i] + (a % mods[i]) + 1

    t0 = time.time()

    if mode == "relaxed":                       # residue 0 of Z/L must stay uncovered
        for i in range(k):
            sink.add([-X(i, 0)])

    used = [0] * k
    for i, n in enumerate(mods):
        s0 = nv
        nv += n - 1

        def S(j, s0=s0):
            return s0 + j                       # S(1)..S(n-1)

        sink.add([-X(i, 0), S(1)])
        for j in range(1, n - 1):
            sink.add([-X(i, j), S(j + 1)])
            sink.add([-S(j), S(j + 1)])
            sink.add([-X(i, j), -S(j)])
        sink.add([-X(i, n - 1), -S(n - 1)])
        nv += 1
        u = nv
        used[i] = u
        for a in range(n):
            sink.add([-X(i, a), u])             # x -> used
        sink.add([-u] + [X(i, a) for a in range(n)])   # used -> OR x
    if verbose:
        print(f"    [build] AMO+used: {sink.nclauses} cls, {nv} vars, "
              f"{time.time()-t0:.1f}s", flush=True)

    if sym != "none" and mode == "full":
        for i in range(min(k, symtop)):
            pre = [used[j] for j in range(i)]
            for a in range(1, mods[i]):
                sink.add([-X(i, a)] + pre)
        if chain > 0:
            # after a_{n_j}=0 the surviving translations are the multiples of n_j, so the
            # SECOND smallest used modulus n_kk may be normalised to a < gcd(n_j,n_kk).
            for j in range(min(chain, k)):
                for kk in range(j + 1, min(chain, k)):
                    g = gcd(mods[j], mods[kk])
                    pre = ([used[t] for t in range(j)] +
                           [used[t] for t in range(j + 1, kk)])
                    for a in range(g, mods[kk]):
                        sink.add([-X(kk, a), -used[j]] + pre)
        if verbose:
            print(f"    [build] +symmetry: {sink.nclauses} cls, "
                  f"{time.time()-t0:.1f}s", flush=True)

    # ---------------- implied budget clauses (Lemma A1 / density) ----------------
    # world E: a class a mod n meets only integers of the parity of a, so the moduli used
    #          with EVEN residue must cover all even residues of Z/L: sum 2/n >= 1, i.e.
    #          sum 1/n >= 1/2; likewise for odd.  (mode relaxed: the even side only has to
    #          cover L/2 - 1 of the L/2 even residues, threshold 1/2 - 1/L.)
    # world H: the single family must satisfy sum 1/m >= 1 (>= 1 - 1/L when relaxed).
    nbud = 0
    if halfbudget:
        B = budget(mods)
        world_E = (world in ("E", "V"))
        # ---- GLOBAL budget clauses (valid in every world): the whole chosen family must
        # satisfy sum 1/n >= h_glob, so for any S with sum_{n not in S} 1/n < h_glob some
        # element of S must be used.  With B only slightly above 1 these are often UNITS.
        h_glob = 1 if mode == "full" else Fraction(L - 1, L)
        for S in minimal_hitting_sets(mods, B - h_glob, smax=4, pool=min(len(mods), 24)):
            cl = [used[mods.index(n)] for n in S]
            assert budget([n for n in mods if n not in S]) < h_glob   # soundness check
            sink.add(cl)
            nbud += 1
        if world_E:
            P = [[0, 0] for _ in range(k)]
            for i, n in enumerate(mods):
                for c in (0, 1):
                    nv += 1
                    P[i][c] = nv
                for a in range(n):
                    sink.add([-X(i, a), P[i][a % 2]])
                for c in (0, 1):
                    sink.add([-P[i][c]] + [X(i, a) for a in range(c, n, 2)])
                sink.add([-P[i][0], -P[i][1]])
            hs = [Fraction(1, 2) - (Fraction(1, L) if mode == "relaxed" else 0),
                  Fraction(1, 2)]
            for c in (0, 1):
                for S in minimal_hitting_sets(mods, B - hs[c]):
                    assert budget([n for n in mods if n not in S]) < hs[c]
                    sink.add([P[mods.index(n)][c] for n in S])
                    nbud += 1
            # --- Lemma A2 overlap clauses.  In H-units each half satisfies
            #     sum_{m in M_c} 1/m > 1 and the two halves are disjoint inside D_H, so
            #     sum_{M_c} 1/m < B_H - 1 = 2B - 1, i.e. excess_c < 2B - 2.
            if True:
                # excess bound.  full: sum_{M_c} 1/m > 1 for both halves and they are
                # disjoint inside D_H, so excess_c < B_H - 2 = 2B - 2.
                # relaxed: the even half only has to cover Z/(L/2) minus one point, so its
                # required density is 1 - 2/L and both bounds loosen by 2/L.
                xb = 2 * B - 2 + (Fraction(2, L) if mode == "relaxed" else 0)
                hm = [n // 2 for n in mods]
                pos = {m: i for i, m in enumerate(hm)}
                nov = 0
                for T in overlap_sets(hm, xb):
                    for c in (0, 1):
                        sink.add([-P[pos[m]][c] for m in T])
                        nov += 1
                if verbose:
                    print(f"    [build] +overlap(A2): {nov} clauses "
                          f"(excess bound {float(xb):.5f})", flush=True)
                nbud += nov
        else:
            # world H: single covering family, excess = sum 1/m - 1 <= B - 1.
            if True:
                xb = B - 1 + (Fraction(1, L) if mode == "relaxed" else 0)
                pos = {m: i for i, m in enumerate(mods)}
                nov = 0
                for T in overlap_sets(mods, xb, strict=True):
                    sink.add([-used[pos[m]] for m in T])
                    nov += 1
                if verbose:
                    print(f"    [build] +overlap(A2): {nov} clauses "
                          f"(excess bound {float(xb):.5f})", flush=True)
                nbud += nov
        if verbose:
            print(f"    [build] +budget: {nbud} implied clauses, "
                  f"{sink.nclauses} cls total, {time.time()-t0:.1f}s", flush=True)

    lo = 1 if mode == "relaxed" else 0
    CH = 1 << 16
    marr = np.array(mods, dtype=np.int64)
    barr = np.array(base, dtype=np.int64) + 1
    r = lo
    while r < L:
        hi = min(L, r + CH)
        rs = np.arange(r, hi, dtype=np.int64)
        lits = (rs[:, None] % marr[None, :]) + barr[None, :]
        sink.add_many(lits.tolist())
        r = hi
    if verbose:
        print(f"    [build] +coverage: {sink.nclauses} cls, {sink.nlits} lits, "
              f"{nv} vars, {time.time()-t0:.1f}s", flush=True)
    return base, nv, sink



def solve_cover(L, mods, mode="full", timeout=300, solver_name="cadical153",
                halfbudget=True, world="H", verbose=False):
    """Decide directly: can Z/L (minus {0} if mode=relaxed) be covered by residue classes
    with DISTINCT moduli taken from the explicit list `mods` (all dividing L)?
    Returns (verdict, classes) with verdict in {"SAT","UNSAT","TIMEOUT"}.
    This is the sub-oracle used by the split-CEGAR driver A_split_cegar.py."""
    from pysat.solvers import Solver
    mods = sorted(set(mods))
    if not mods:
        return "UNSAT", None
    thr = Fraction(1) if mode == "full" else Fraction(L - 1, L)
    if budget(mods) <= thr:
        return "UNSAT", None
    s = Solver(name=solver_name)
    base, nv, sink = build(s, L, mods, mode, "weak", 6, 0, verbose=verbose,
                           halfbudget=halfbudget, world=world)
    timer = None
    if timeout:
        timer = threading.Timer(timeout, s.interrupt)
        timer.start()
    try:
        r = s.solve_limited(expect_interrupt=True) if timeout else s.solve()
    finally:
        if timer:
            timer.cancel()
    if r is None:
        s.delete()
        return "TIMEOUT", None
    if not r:
        s.delete()
        return "UNSAT", None
    pos = set(l for l in s.get_model() if l > 0)
    classes = []
    for i, n in enumerate(mods):
        for a in range(n):
            if base[i] + a + 1 in pos:
                classes.append((n, a))
                break
    s.delete()
    return "SAT", classes


def run(L, world, mode, cap, minblock, sym, symtop, chain, solver_name, timeout, outdir,
        require=None, forbid=None, tag="", halfbudget=True):
    D = {"E": D_E, "H": D_H, "V": D_V}[world](L)
    full_budget = budget(D)
    mods = [n for n in D
            if (cap is None or n <= cap) and (minblock is None or L // n >= minblock)]
    if forbid:
        mods = [n for n in mods if n not in forbid]
    dropped = [n for n in D if n not in mods]
    tail = budget(dropped)
    b = budget(mods)
    print(f"=== L={L}  world={world}  mode={mode}  solver={solver_name} {tag}")
    print(f"    |D_{world}(L)| = {len(D)}   full budget = {float(full_budget):.5f}")
    print(f"    kept {len(mods)} moduli (cap={cap}, minblock={minblock}); "
          f"budget kept = {float(b):.5f}; dropped-tail sum = {float(tail):.6f}")
    print(f"    moduli = {mods if len(mods)<=45 else str(mods[:45])+' ...'}", flush=True)
    res_d = dict(L=L, world=world, mode=mode, nmods=len(mods), moduli=mods,
                 budget=float(b), full_budget=float(full_budget),
                 dropped_tail=float(tail), cap=cap, minblock=minblock,
                 sym=sym, chain=chain, solver=solver_name)
    # density threshold.  full mode: a covering of Z/L needs sum 1/n >= 1, strict by
    # Davenport-Mirsky-Newman-Rado (no exact cover by distinct moduli > 1).
    # relaxed mode: the classes cover L-1 residues, so sum 1/n >= (L-1)/L; in world E the
    # odd half is a genuine covering so the inequality is again strict.
    thr = Fraction(1) if mode == "full" else Fraction(L - 1, L)
    if b <= thr:
        print(f"    >>> budget {float(b):.6f} <= {float(thr):.6f} : UNSAT by the density "
              f"bound, no SAT call needed.")
        res_d.update(verdict="UNSAT(density)", build_time=0.0, solve_time=0.0)
        return res_d

    from pysat.solvers import Solver
    s = Solver(name=solver_name)
    t0 = time.time()
    base, nv, sink = build(s, L, mods, mode, sym, symtop, chain,
                           halfbudget=halfbudget, world=world)
    if require:
        for n in require:
            i = mods.index(n)
            s.add_clause([base[i] + a + 1 for a in range(n)])
    build_t = time.time() - t0
    print(f"    build {build_t:.1f}s  vars={nv} clauses={sink.nclauses} "
          f"lits={sink.nlits}", flush=True)

    timer = None
    if timeout:
        timer = threading.Timer(timeout, s.interrupt)
        timer.start()
    t1 = time.time()
    try:
        r = s.solve_limited(expect_interrupt=True) if timeout else s.solve()
    finally:
        if timer:
            timer.cancel()
    solve_t = time.time() - t1
    res_d.update(build_time=build_t, solve_time=solve_t, vars=nv,
                 clauses=sink.nclauses, lits=sink.nlits)

    if r is None:
        res_d["verdict"] = "TIMEOUT"
        print(f"    >>> TIMEOUT after {solve_t:.1f}s")
    elif r:
        model = s.get_model()
        pos = set(l for l in model if l > 0)
        classes = []
        for i, n in enumerate(mods):
            for a in range(n):
                if base[i] + a + 1 in pos:
                    classes.append((n, a))
                    break
        ok, msg = verify_cover(L, classes, world=world, relaxed=(mode == "relaxed"))
        res_d["verdict"] = "SAT" if ok else "SAT-BUT-BAD"
        res_d["classes"] = classes
        res_d["inline_check"] = msg
        print(f"    >>> SAT in {solve_t:.1f}s with {len(classes)} classes; "
              f"inline check: {msg}")
        print(f"    classes = {classes}")
        os.makedirs(outdir, exist_ok=True)
        fn = os.path.join(outdir, f"cert_{world}_{mode}_L{L}{tag}.json")
        with open(fn, "w") as f:
            json.dump(res_d, f, indent=1)
        print(f"    certificate written to {fn}")
    else:
        res_d["verdict"] = "UNSAT"
        print(f"    >>> UNSAT in {solve_t:.1f}s "
              f"(rigorous for the kept modulus set only)")
    s.delete()
    return res_d


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--L", type=int, required=True)
    ap.add_argument("--world", choices=["E", "H", "V"], default="E")
    ap.add_argument("--mode", choices=["full", "relaxed"], default="full")
    ap.add_argument("--cap", type=int, default=None)
    ap.add_argument("--minblock", type=int, default=None)
    ap.add_argument("--sym", choices=["none", "weak"], default="weak")
    ap.add_argument("--symtop", type=int, default=6)
    ap.add_argument("--chain", type=int, default=0)
    ap.add_argument("--nobudget", action="store_true")
    ap.add_argument("--solver", default="cadical153")
    ap.add_argument("--timeout", type=float, default=1200)
    ap.add_argument("--tag", default="")
    ap.add_argument("--outdir",
                    default="/home/user/erdos/erdos-273/attempts/route-A-satsearch/certs")
    ap.add_argument("--require", default="")
    ap.add_argument("--forbid", default="")
    a = ap.parse_args()
    req = [int(x) for x in a.require.split(",") if x.strip()]
    frb = [int(x) for x in a.forbid.split(",") if x.strip()]
    out = run(a.L, a.world, a.mode, a.cap, a.minblock, a.sym, a.symtop, a.chain,
              a.solver, a.timeout, a.outdir, req, frb, a.tag,
              halfbudget=not a.nobudget)
    print(json.dumps({k: v for k, v in out.items()
                      if k not in ("classes", "moduli")}, indent=1))
