"""
QA: re-verify, from scratch and independently of the code that produced them, EVERY certificate
claimed anywhere in this repo. Checks distinctness, admissibility (2m+1 prime in the H-world,
n+1 prime and n >= 4 in the E-world) and coverage by a full mod-lcm sweep.
CONCLUSION (last run): all H-world certificates valid; the E-world half-certificates cover exactly
one parity class, as claimed. See NOTES.md.
"""
from math import lcm
from fractions import Fraction
from sympy import isprime

H_CERTS = {
 "route A / L=180 (cost 14/9)":
   [(2,0),(3,2),(5,0),(6,3),(9,7),(15,4),(18,1),(20,7),(30,1),(36,13),(90,13)],
 "route F / L=288 (cost 65/48, cheapest found)":
   [(2,0),(3,1),(6,3),(8,5),(9,2),(18,17),(36,23),(48,41),(96,17),(288,257)],
 "route C / L=360 (cost 67/45)":
   [(2,0),(3,1),(6,3),(8,5),(9,2),(15,2),(18,5),(20,9),(30,5),(36,35),(90,71),(120,113)],
}

def verify_H(pairs, label):
    mods = [m for m, _ in pairs]
    assert len(set(mods)) == len(mods), (label, "repeated modulus")
    assert all(m >= 2 and isprime(2*m+1) for m in mods), (label, "modulus not in H")
    L = 1
    for m in mods: L = lcm(L, m)
    cov = bytearray(L)
    for m, a in pairs:
        for r in range(a % m, L, m): cov[r] = 1
    assert cov.count(0) == 0, (label, "does not cover Z")
    cost = sum(Fraction(1, m) for m in mods)
    print(f"  OK  {label:<46} L={L:<6} cost={cost} = {float(cost):.5f}")

def verify_E_half(pairs, label):
    """an E-world system must cover EXACTLY one parity class"""
    mods = [n for n, _ in pairs]
    assert len(set(mods)) == len(mods)
    assert all(n >= 4 and isprime(n+1) for n in mods), (label, "modulus not in E")
    L = 1
    for n in mods: L = lcm(L, n)
    cov = bytearray(L)
    for n, a in pairs:
        for r in range(a % n, L, n): cov[r] = 1
    got = set(r for r in range(L) if cov[r])
    for j in (0, 1):
        if got == set(range(j, L, 2)):
            print(f"  OK  {label:<46} L={L:<6} covers exactly the integers = {j} (mod 2)")
            return
    raise AssertionError((label, "does not cover exactly one parity class"))

if __name__ == "__main__":
    print("H-world certificates:")
    for k, v in H_CERTS.items(): verify_H(v, k)
    print("E-world half-certificates:")
    verify_E_half([(2*m, (2*a) % (2*m)) for m, a in H_CERTS["route F / L=288 (cost 65/48, cheapest found)"]],
                  "lift of the 65/48 system (cost 65/96)")
    verify_E_half([(2*m, (2*a+1) % (2*m)) for m, a in H_CERTS["route A / L=180 (cost 14/9)"]],
                  "odd lift of the 14/9 system")
    print("\nALL CERTIFICATES VALID.")
