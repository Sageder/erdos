"""reach.py -- Reach(s) = sup{ N : some monotone-K-AP-free permutation of [1..N]
   begins with the sequence s }.   (Restriction to [1..N-1] shows the set of good
   N is down-closed, so Reach is well defined and binary-searchable.)
   KEY: a monotone-4-AP-free permutation of N with first |s| values s  =>  Reach(s)=oo.
"""
import sys
from pysat.formula import CNF
from pysat.solvers import Solver
from sat import build_cnf, model_to_perm

_cache = {}
def _base(N, K):
    if (N,K) not in _cache:
        _cache[(N,K)] = build_cnf(N,K)
    return _cache[(N,K)]

def prefix_units(s, N, y):
    u = []
    for i in range(len(s)-1):
        u.append(y(s[i], s[i+1]))
    ss = set(s)
    for v in range(1, N+1):
        if v not in ss:
            u.append(y(s[-1], v))
    return u

def sat_prefix(s, N, K=4, solver='cd15', want_perm=False):
    cnf, pool, y, _ = _base(N,K)
    with Solver(name=solver, bootstrap_with=cnf.clauses) as S:
        ok = S.solve(assumptions=prefix_units(s,N,y))
        if ok and want_perm:
            return model_to_perm(S.get_model(), N, y)
        return ok

def reach(s, K=4, cap=200, solver='cd15'):
    lo = max(s)
    if not sat_prefix(s, lo, K, solver): return lo-1
    hi = lo
    while hi < cap and sat_prefix(s, min(2*hi,cap), K, solver):
        hi = min(2*hi, cap)
        if hi >= cap: return cap  # ">= cap"
    lo2, hi2 = hi, min(2*hi,cap)
    while lo2+1 < hi2:
        mid=(lo2+hi2)//2
        if sat_prefix(s, mid, K, solver): lo2=mid
        else: hi2=mid
    return lo2
