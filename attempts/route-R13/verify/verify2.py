from math import gcd
from itertools import combinations
# (i) search minimal sets with gcd(a,b)=|a-b|
def search(k,limit):
    best=None
    for comb in combinations(range(1,limit),k):
        if all(gcd(a,b)==b-a for a,b in combinations(comb,2)):
            return comb
    return None
for k in range(2,6):
    s=search(k, 200 if k<5 else 700)
    print("k=",k,"example:",s)
    if s:
        for a,b in combinations(s,2):
            g=b-a; print("   pair",a,b,"g",g,"nu_i,nu_j",a//g,b//g,"diff1:",b//g-a//g==1)
