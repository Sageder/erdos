import random
bad=[]
for _ in range(300000):
    c=random.randint(1,50); s=random.randint(5,10**6); r=random.randint(c*s,2*c*s-1)
    m=c*r*s
    if not (m<=r*r<2*m): bad.append((c,r,s,m,r*r))
print("box => n+j <= r^2 < 2(n+j)  [i.e. sqrt(n+j)<=r<sqrt(2(n+j))] violations:",len(bad),bad[:3])
