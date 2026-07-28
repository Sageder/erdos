import numpy as np
X=4_000_000
spf=np.zeros(X+3,dtype=np.int32)
for i in range(2,int((X+2)**0.5)+1):
    if spf[i]==0:
        seg=spf[i*i::i]; spf[i*i::i]=np.where(seg==0,i,seg)
for i in range(2,X+3):
    if spf[i]==0: spf[i]=i
def P(m):
    p=1
    while m>1:
        q=int(spf[m]); p=max(p,q)
        while m%q==0: m//=q
    return p
lo=1000; hi=X//2
pairs=0; agree=0
for n in range(lo,hi):
    p=P(n)
    if not (n**0.40 < p <= n**0.50): continue
    if n%(p*p)==0: continue
    if P(2*n)!=p: continue     # isolate: same large prime, band membership unchanged
    c1 = ((n//p -1)%p) >= (p-1)//2
    c2 = ((2*n//p -1)%p) >= (p-1)//2
    pairs+=1; agree += (c1==c2)
print("n with same largest prime p for n and 2n, p in band:", pairs)
print("fraction where C_p(n) == C_p(2n):  %.4f   (stability would require ->1)"%(agree/pairs))
