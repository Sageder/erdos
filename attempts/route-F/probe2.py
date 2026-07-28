#!/usr/bin/env python3
"""probe2.py D ppcap timeout  x:y [x:y ...]   -- gadget rate with prime-power cap"""
import sys, os, time, subprocess
from fractions import Fraction
from math import gcd
from lib import smallest_prime_factors
from universe import prune, lcm_of
from mk import write_problem
HERE=os.path.dirname(os.path.abspath(__file__))
D=int(sys.argv[1]); Q=int(sys.argv[2]); TO=float(sys.argv[3]); specs=sys.argv[4:]
spf=smallest_prime_factors(max(int(s.split(':')[1]) for s in specs)+2)
for s in specs:
    x,y=(int(t) for t in s.split(':'))
    U=prune(x,y,D,spf,pp_cap=(Q or None))
    if len(U)<2: print("%-16s EMPTY"%s); continue
    L=lcm_of(U); lam=(L//gcd(L,D)).bit_length(); ms=sum(Fraction(1,n) for n in U)
    pf="pr%d.prob"%os.getpid(); of="pr%d.out"%os.getpid()
    write_problem(pf,U,D,None,Fraction(0),ms)
    t0=time.time()
    try: subprocess.run([os.path.join(HERE,"search"),pf,of,"2000","100000000000"],stderr=subprocess.DEVNULL,timeout=TO)
    except subprocess.TimeoutExpired: pass
    dt=time.time()-t0
    vs=[]
    for line in open(of):
        try: V=[int(t) for t in line.split()]
        except ValueError: continue
        vs.append(float(sum(Fraction(1,n) for n in V)))
    print("%-16s |U|=%-4d lam=%-4d maxsum=%.4f found=%-5d in %.1fs range=[%s,%s]"%(
        s,len(U),lam,float(ms),len(vs),dt,"%.4f"%min(vs) if vs else "-","%.4f"%max(vs) if vs else "-"))
    sys.stdout.flush()
    for f in (pf,of):
        try: os.remove(f)
        except OSError: pass
