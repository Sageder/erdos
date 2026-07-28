"""lowverify.py -- second encoding + second/third solver for the LOWER-profile UNSATs.

Order variables o_{u,w} (u<w) = 'u before w', full transitivity, 4-AP constraints, and a
cardinality constraint  #{u != v : u before v} >= ceil(gamma*v) - 1  for every v
(sequential-counter encoding from pysat).  Independent of the CP-SAT model in lowprofile.py.
"""
import sys
from fractions import Fraction
from itertools import combinations
sys.path.insert(0,'/home/user/erdos/experiments')
from pysat.formula import IDPool, CNF
from pysat.card import CardEnc, EncType
from pysat.solvers import Solver
from apcheck import has_monotone_kap_pos

def run(N, gamma, solvers=('cadical195','glucose4','minisat22')):
    pool = IDPool()
    o = {}
    for u,w in combinations(range(1,N+1),2):
        o[(u,w)] = pool.id(('o',u,w))
    def lit(u,w):                     # 'u before w'
        return o[(u,w)] if u<w else -o[(w,u)]
    cnf = CNF()
    for u,w,z in combinations(range(1,N+1),3):
        a,b,c = lit(u,w), lit(w,z), lit(u,z)
        cnf.append([-a,-b,c]); cnf.append([a,b,-c])
    for e in range(1,(N-1)//3+1):
        for x in range(1,N-3*e+1):
            L=[lit(x+k*e,x+(k+1)*e) for k in range(3)]
            cnf.append([-l for l in L]); cnf.append(list(L))
    for v in range(1,N+1):
        need = -(-(gamma.numerator*v)//gamma.denominator) - 1
        if need <= 0: continue
        lits=[lit(u,v) for u in range(1,N+1) if u!=v]
        if need > len(lits): return 'UNSAT(trivial)'
        cnf.extend(CardEnc.atleast(lits=lits, bound=need, vpool=pool,
                                   encoding=EncType.seqcounter).clauses)
    outs=[]
    for s in solvers:
        with Solver(name=s, bootstrap_with=cnf.clauses) as S:
            sat=S.solve(); mdl=S.get_model() if sat else None
        outs.append('SAT' if sat else 'UNSAT')
        if sat:
            ms=set(mdl)
            import functools
            def cmp(u,w):
                if u==w: return 0
                b = (o[(u,w)] in ms) if u<w else (o[(w,u)] not in ms)
                return -1 if b else 1
            perm=sorted(range(1,N+1), key=functools.cmp_to_key(cmp))
            pos={v:i+1 for i,v in enumerate(perm)}
            assert not has_monotone_kap_pos(perm,4)
            assert all(pos[v]*gamma.denominator >= gamma.numerator*v for v in range(1,N+1))
    assert len(set(outs))==1, ('DISAGREE',N,gamma,outs)
    return outs[0]

if __name__=="__main__":
    for g,Ns in ((Fraction(3,4),[16,20]), (Fraction(2,3),[16,20]),
                 (Fraction(3,5),[20,30,40]), (Fraction(1,2),[40,60])):
        for N in Ns:
            print(f"gamma={g} N={N}: {run(N,g)}  (3 solvers agree)", flush=True)
