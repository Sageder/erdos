import sys
sys.path.insert(0,'/home/user/erdos/attempts/route-R22-prove-b')
sys.path.insert(0,'/home/user/erdos/experiments')
from scan_heads import first_unsat
from eager import head_class
from arch import blk, v2
for b in (3,4,5,6,7,9):
    cf = head_class(b, lambda m: m+1, lambda m: m)
    print(f"HEAD b={b} s=m+1 K=m : first UNSAT N = {first_unsat(cf, 8, 320)}", flush=True)
for b in (3,4,5,6,7,9):
    cf = lambda v,b=b: blk(v,b)
    print(f"BLK({b}) pure block layout: first UNSAT N = {first_unsat(cf, 8, 320)}", flush=True)
for b in (3,5):
    cf = lambda v,b=b: blk(v,b)+v2(v)
    print(f"CLS({b},a) R20 control    : first UNSAT N = {first_unsat(cf, 8, 320)}", flush=True)
