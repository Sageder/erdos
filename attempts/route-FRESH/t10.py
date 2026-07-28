"""The 'single base point' reduction and why it FAILS.

If a is 4-AP-free with a(1)=1 (normalisation Lemma 5) then p(1)<p(1+e) for all e,
so the 4-AP (1,1+e,1+2e,1+3e) forces:  NOT [ g(e) < g(2e) < g(3e) ],  g(e):=p(1+e).
So Erdos 196 = YES would follow from:
   (R)  every bijection g of N (order type omega) has some e with g(e)<g(2e)<g(3e).
CLAIM: (R) is FALSE.  Explicit counterexample below: write e = 2^a 3^b m, gcd(m,6)=1,
and order N by the antidiagonal rule on (a,b): by a+b ascending, ties by b DESCENDING,
then by m ascending; dovetailed into order type omega.
Then g(e)<g(2e) (antidiag a+b+1) and g(3e)<g(2e) (same antidiag, larger b first).
"""
def key(e):
    a=0; m=e
    while m%2==0: m//=2; a+=1
    b=0
    while m%3==0: m//=3; b+=1
    return (a,b,m)

def omega_order(E):
    """produce an order-type-omega enumeration of [1..E] refining the rule."""
    items=[]
    for e in range(1,E+1):
        a,b,m=key(e)
        # dovetail: stage = max(m, a+b) makes every element appear at a finite stage
        items.append((max(m,a+b), a+b, -b, m, e))
    items.sort()
    return [it[-1] for it in items]

for E in (200, 2000, 20000):
    order=omega_order(E)
    g={e:i for i,e in enumerate(order)}
    bad=[e for e in range(1,E//3+1) if g[e]<g[2*e]<g[3*e]]
    # also check it is a genuine "no 3 in a row" style order: report basic sanity
    print(f"E={E}: violations of (R) among e<=E/3: {len(bad)}   (0 = (R) is false)")
# and check the pure lattice rule ignoring dovetailing, on the (a,b) lattice
bad=0
for a in range(30):
    for b in range(30):
        F=lambda x,y: (x+y, -y)
        if F(a,b)<F(a+1,b)<F(a,b+1): bad+=1
print("pure lattice rule violations on 30x30:", bad)
