"""headtail.py — is the profile wall driven by the INITIAL SEGMENT or by the tail?

phi_{K,C}(v) = C*v for v <= K, unconstrained above.  If the wall for a small K equals the
wall for the full linear profile, then the asymptotic SHAPE of phi is irrelevant to finite
extinction and the 'v log v vs linear' question is not what finite walls measure.
"""
import sys, time
sys.path.insert(0,'/home/user/erdos/attempts/route-R20-vlogv')
sys.path.insert(0,'/home/user/erdos/experiments')
from profile_sat import solve_profile, verify
from apcheck import has_monotone_kap_pos

def phiKC(K,C):
    return lambda v: (max(1,int(C*v)) if v<=K else 10**9)

if __name__ == "__main__":
    C = float(sys.argv[1]); Ks=[int(x) for x in sys.argv[2].split(',')]
    Ns=[int(x) for x in sys.argv[3].split(',')]
    for K in Ks:
        for N in Ns:
            phi = phiKC(K,C)
            t0=time.time(); res,p,r = solve_profile(N, phi); dt=time.time()-t0
            if res=="SAT":
                assert not has_monotone_kap_pos(p,4)
                pos={v:i+1 for i,v in enumerate(p)}
                assert all(pos[v]<=C*v for v in range(1,min(K,N)+1))
            print(f"C={C} K={K} N={N}: {res} ({dt:.0f}s, {r} rounds)", flush=True)
            if res!="SAT": break
