"""oddcuts.py — diagnostic: the ODD-restriction of CLS(b,a).

In CLS(b,a) every odd value has class = block_b(v), so the induced order on the ODD
values is an in-order geometric block ordering.  Under o -> (o+1)/2 the odd values of
[b^j, b^{j+1}) become the interval [A_j, A_{j+1}) with A_j = (b^j+1)/2.  This script
decides by SAT (same lazy-transitivity engine, so UNSAT is a theorem for EVERY choice of
within-block orders) whether that in-order block system admits a 4-AP-free order.

If it dies at the same scale as CLS(b,a) itself, the death of CLS(b,a) is DIAGNOSED as
the AP-restriction failure (Prop. R20-2 / design principle D1).
"""
import sys, time
sys.path.insert(0,'/home/user/erdos/attempts/route-R20-vlogv')
sys.path.insert(0,'/home/user/erdos/experiments')
from classsat import solve_classes
from apcheck import has_monotone_kap_pos

def cuts_class(A):
    def c(n):
        j = 0
        while j+1 < len(A) and A[j+1] <= n:
            j += 1
        return j
    return c

if __name__ == "__main__":
    b = int(sys.argv[1]); Ns = [int(x) for x in sys.argv[2].split(',')]
    A = [ (b**j+1)//2 for j in range(0, 9) ]
    A = sorted(set(x for x in A if x>=1))
    print(f"b={b} odd-block cuts (in n-coordinates): {A}", flush=True)
    c = cuts_class(A)
    for N in Ns:
        t0=time.time(); res,w,rounds = solve_classes(N,c); dt=time.time()-t0
        extra = ""
        if res=="SAT":
            assert not has_monotone_kap_pos(w,4)
        print(f"oddblocks(b={b}) N={N} (odd values up to {2*N-1}): {res} ({dt:.0f}s, {rounds} rounds)", flush=True)
        if res!="SAT": break
