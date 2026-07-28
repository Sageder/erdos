import sys, time
sys.path.insert(0,'/home/user/erdos/experiments')
sys.path.insert(0,'/home/user/erdos/attempts/route-R20-vlogv')
sys.path.insert(0,'/home/user/erdos/attempts/route-R22-prove-b')
from classsat import solve_classes
from apcheck import has_monotone_kap_pos
from eager import head_class
cf = head_class(3, lambda m: m+1, lambda m: m)
for V0, W in [(9,81),(9,120),(9,160),(27,120),(27,180),(27,243),(27,320),
              (81,243),(81,320),(81,420),(81,560),(243,729),(243,900)]:
    L = W-V0+1
    cw = lambda i: cf(i+V0-1)
    t0=time.time(); res, perm, rounds = solve_classes(L, cw); dt=time.time()-t0
    ok = ""
    if res=="SAT":
        assert not has_monotone_kap_pos(perm,4); ok=" (model verified)"
    print(f"window [{V0}..{W}] L={L}: {res} ({dt:.0f}s, {rounds} rounds){ok}", flush=True)
