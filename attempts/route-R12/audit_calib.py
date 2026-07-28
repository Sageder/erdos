from audit_core import *
# calibration: reproduce PROBLEM.md sanity data with the DIRECT definition
S1=[n for n in range(1,442) if in_S_direct(n,1)]
print("k=1 first15:",S1[:15]); print("k=1 count<=441:",len(S1))
S2=[n for n in range(1,4001) if in_S_direct(n,2)]
print("k=2 first20:",S2[:20])
S3=[n for n in range(1,60001) if in_S_direct(n,3)]
print("k=3 first8:",S3[:8],"count<=6e4:",len(S3))
S4=[n for n in range(1,60001) if in_S_direct(n,4)]
print("k=4 <=6e4:",S4)
# cross-check the three alternative criteria on a range
bad=[]
for n in range(1,3000):
    for k in (1,2,3):
        a=in_S_direct(n,k); b=in_S_digitsum(n,k); c=in_S_ladder_criterion(n,k); d=in_S_product(n,k) if n>=k else None
        if not(a==b==c) or (d is not None and d!=a): bad.append((n,k,a,b,c,d))
print("criterion mismatches:",bad[:10],"total",len(bad))
