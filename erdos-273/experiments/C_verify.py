"""
C_verify.py -- Route C: independent, from-scratch verification of every certificate this
route produced.  Nothing is imported from the search code; primality, distinctness and
coverage are all recomputed here in exact integer arithmetic.

CLAIM TESTED, for each stored certificate:
  (a) every modulus m satisfies 2m+1 prime  (i.e. m in H, equivalently 2m in E);
  (b) the moduli are pairwise distinct and > 1;
  (c) the classes cover every residue mod L = lcm(moduli)  -- exhaustive sweep;
  (d) the classes cover a window of NEGATIVE integers as well (two-sided classes);
  (e) the E-image (moduli 2m, residues 2b+j) has n+1 prime for every modulus n.

CONCLUSION (printed): all stored certificates verify.  These certify only that SINGLE
H-coverings exist; problem 273 needs TWO with DISJOINT modulus sets, which was NOT found.
"""
from math import lcm
from sympy import isprime

CERTS = {
 "L=360, 12 moduli, cheapest found (recip 1.488889)":
   [(0,2),(1,3),(3,6),(5,8),(2,9),(2,15),(5,18),(9,20),(5,30),(35,36),(71,90),(113,120)],
 "L=360, 13 moduli (recip 1.688889)":
   [(0,2),(1,3),(3,5),(5,6),(1,8),(6,9),(6,15),(9,18),(19,20),(15,30),(3,36),(57,90),(69,120)],
 "L=2520, 22 moduli (recip 1.897619)":
   [(0,2),(1,3),(3,5),(5,6),(1,8),(6,9),(7,14),(12,15),(3,18),(5,20),(15,21),(15,30),
    (31,35),(9,36),(55,56),(18,63),(81,90),(9,105),(39,120),(59,140),(27,168),(159,210)],
 "L=27720, 28 moduli (recip 2.062771)":
   [(0,2),(1,3),(3,5),(5,6),(1,8),(6,9),(10,11),(13,14),(9,15),(9,18),(15,20),(0,21),
    (15,30),(27,33),(12,35),(21,36),(31,44),(3,56),(12,63),(57,90),(3,99),(81,105),
    (51,120),(71,140),(6,165),(135,168),(183,198),(171,210)],
}

def check(name, cl):
    mods=[m for _a,m in cl]
    assert len(set(mods))==len(mods), "repeated modulus"
    assert all(m>1 for m in mods)
    bad=[m for m in mods if not isprime(2*m+1)]
    assert not bad, f"moduli not in H: {bad}"
    L=1
    for m in mods: L=lcm(L,m)
    cov=bytearray(L)
    for a,m in cl:
        for x in range(a%m,L,m): cov[x]=1
    miss=[x for x in range(L) if not cov[x]]
    assert not miss, f"uncovered residues mod {L}: {miss[:10]}"
    for x in range(-6000,0):
        assert any((x-a)%m==0 for a,m in cl), x
    r=sum(1/m for _a,m in cl)
    Emods=[2*m for m in mods]
    assert all(isprime(n+1) for n in Emods)
    print(f"  {name}")
    print(f"     lcm = {L}, {len(cl)} classes, sum 1/m = {r:.6f}")
    print(f"     H-moduli {sorted(mods)}")
    print(f"     E-image moduli 2m = {sorted(Emods)}  (all n+1 prime)")
    print(f"     covers every residue mod {L}: YES;  covers [-6000,-1]: YES")

print("independent verification of Route C certificates")
for k,v in CERTS.items(): check(k,v)
print("ALL CERTIFICATES VERIFIED.")
print()
print("NOTE: each of these is a covering system of Z with distinct moduli in H.")
print("Its E-image {2m} covers only ONE parity class of Z.  Problem 273 needs a SECOND")
print("H-covering whose modulus set is DISJOINT from the first; none was found.")

# ------------------------------------------------------------------------------
# RUN LOG (results of this route's searches; see C_out/ for raw output)
#   (i)   H-coverings EXIST: verified certificates above (L = 360, 2520, 27720).
#         cheapest found: sum 1/m = 1.488889, moduli {2,3,6,8,9,15,18,20,30,36,90,120}.
#   (ii)  H-covering avoiding modulus 2: NONE FOUND in any lattice searched
#         (L = 360, 720, 1260, 2520, 5040, 27720, 151200, 360360, 720720, 2162160,
#          10810800).  EXHAUSTIVE UNSAT proved only for L = 360 (183312 nodes).
#         Avoiding 2 and 3: not reached.
#   (iii) two DISJOINT H-coverings (= problem 273): NONE FOUND; no exhaustive verdict
#         completed for any lattice with B_H(L) > 2.
# CAVEAT: UNSAT for one divisor lattice L is NOT a proof of nonexistence in general.
