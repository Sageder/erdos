from audit_core import in_S_ladder_criterion
c=0
S=[]
for n in range(1,200001):
    if in_S_ladder_criterion(n,2): c+=1; S.append(n)
print("|S_2 cap [1,2e5]| =",c)
