"""Generative regeneration of Lemma R_2 solutions: n+1 = r1*s1 (c1=1, odd), boxes+residue."""
from audit_core import *
from audit_Rk import smooth_part, cond_ii, lemmaRk_hyp
from sympy import primerange, isprime
import sys
S=int(sys.argv[1]) if len(sys.argv)>1 else 3000
pr=list(primerange(5,S))
prset=set(primerange(5,2*S+5))
hits=[];fp=[];hits_noii=[];fp_noii=[]
for s in pr:
    lo=s+(s+1)//2
    for r in range(max(lo,s+1),2*s):
        if r==s or not isprime(r): continue
        if (r%s) < (s+1)//2: continue
        n=r*s-1
        if n%2!=0: continue          # n+1=rs odd -> n even
        if lemmaRk_hyp(n,2,require_ii=False):
            hits_noii.append(n)
            if not in_S_ladder_criterion(n,2): fp_noii.append(n)
        if lemmaRk_hyp(n,2):
            hits.append(n)
            if not in_S_ladder_criterion(n,2): fp.append(n)
print("s up to",S,"=> n up to ~",2*S*S)
print("FULL Lemma R_2 (with cond (ii)): #hits =",len(hits),"falsepos =",len(fp))
print("  hits:",sorted(hits)[:40])
print("WITHOUT cond (ii): #hits =",len(hits_noii),"falsepos =",len(fp_noii))
print("  falsepos:",sorted(fp_noii)[:40])
print("  hits:",sorted(hits_noii)[:40])
