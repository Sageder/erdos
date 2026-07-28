"""prefixfix.py — the class rule with an EXCEPTIONAL FINITE PREFIX.

Small values are where every scale-graded design dies first (route R3 saw the same: all 26
orderings died by value 24).  A rule is still a rule if it treats [1..K] by a hand-chosen
4-AP-free order placed first (class -1) and applies the asymptotic rule above K; the order
type is still omega.  This isolates the ASYMPTOTIC viability of a design from its
small-value accidents.
"""
import sys, itertools
sys.path.insert(0,'/home/user/erdos/attempts/route-R20-vlogv')
from framework import restrict, violations
from constructions import cls_delay, cls_block, w_sigma, logb, v2
from banded import make_banded

def with_prefix(c, K, prefkey):
    def cc(v):
        return -1 if v<=K else c(v)
    def kk(v, w):
        return (cc(v), prefkey(v) if v<=K else w(v))
    return cc, kk

if __name__=="__main__":
    M = int(sys.argv[1]) if len(sys.argv)>1 else 2000
    Ks = [0,8,16,24,32,48,64,96,128]
    fams = {}
    for b in (3,4,5,6,7):
        fams[f'CLS({b},a)']=(b, cls_delay(b, lambda a:a))
        fams[f'BLK({b})']=(b, cls_block(b))
    inners = {'sigma': w_sigma, 'desc': (lambda v:-v), 'asc': (lambda v:v)}
    best=[]
    for fn,(b,c) in fams.items():
        for K in Ks:
            for iname,inner in inners.items():
                for B in (2,3,4):
                    for pi in itertools.permutations(range(B)):
                        w = make_banded(b,B,pi,inner=inner)
                        cc,kk = with_prefix(c,K,w_sigma)
                        key = (lambda kk=kk,w=w: (lambda v: kk(v,w)))()
                        perm = restrict(key, M)
                        vio = violations(perm,4)
                        if not vio: best.append((10**9,fn,K,iname,B,pi,"SURVIVES"))
                        else:
                            x,d,s = vio[0]
                            best.append((x+3*d,fn,K,iname,B,pi,f"({x},{d},{s})"))
    best.sort(reverse=True)
    for mt,fn,K,iname,B,pi,info in best[:25]:
        tag = f"SURVIVES to {M}" if mt==10**9 else f"dies@{mt}"
        print(f"{fn:9s} K={K:3d} inner={iname:5s} B={B} pi={pi}  {tag:16s} {info}")
