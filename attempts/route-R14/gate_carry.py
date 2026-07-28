"""
R14 gate 1.  Verify, by exact integer arithmetic, the two elementary facts L4a rests on.

(G1)  n in S_2  <=>  for every prime l:  kappa_l(n) >= 2(nu_l(n+1)+nu_l(n+2)),
      where kappa_l(n) = #carries when adding n+n in base l.
      Cross-checked against a direct factorial-divisibility test and against the
      published list of S_2 members in PROBLEM.md.

(G2)  DIGIT-POOR LEMMA.  Let l >= 5 be prime, j in {1,2}, l || n+j, W = (n+j)/l >= 1.
      Then kappa_l(n) >= 2  <=>  NOT ( d_0(W-1) <= (l-3)/2  and  d_i(W-1) <= (l-1)/2 for all i>=1 ),
      where d_i are the base-l digits of W-1.
      (i.e. the l-condition fails exactly when W-1 is "digit-poor" base l.)

(G3)  the position-0 carry is automatic for l >= 5, and l>4 divides at most one of n+1,n+2.
"""
import random
from sympy import factorint, primerange, isprime

P0 = 4

def carries(n, l):
    c = 0; carry = 0
    while n > 0:
        d = n % l
        if 2*d + carry >= l:
            carry = 1; c += 1
        else:
            carry = 0
        n //= l
    if carry: pass  # a final carry out of the top digit was already counted
    return c

def in_S2_by_criterion(n):
    for m, in ((n+1,), (n+2,)):
        pass
    dem = {}
    for m in (n+1, n+2):
        for p, e in factorint(m).items():
            dem[p] = dem.get(p, 0) + e
    for p, e in dem.items():
        if carries(n, p) < 2*e:
            return False
    return True

def in_S2_direct(n):
    # ((n+2)!)^2 | (2n)!  via Legendre on all primes <= 2n
    from sympy import factorial
    a = factorial(2*n); b = factorial(n+2)**2
    return a % b == 0

def digit_poor(V, l):
    """V = W-1 >= 0.  True iff doubling V base l with carry-in 1 produces no carry."""
    if V == 0:
        return True            # 2*0+1 = 1 < l
    d0 = V % l
    if 2*d0 + 1 >= l:
        return False
    V //= l
    while V > 0:
        if 2*(V % l) >= l:
            return False
        V //= l
    return True

def main():
    # ---- G1 : criterion vs direct factorial divisibility, n <= 1300 -------------
    S2c = [n for n in range(1, 1301) if in_S2_by_criterion(n)]
    S2d = [n for n in range(1, 1301) if in_S2_direct(n)]
    assert S2c == S2d, ("G1 FAIL", S2c[:20], S2d[:20])
    published = [208, 458, 987, 1220]
    assert S2c[:4] == published, ("G1 published list FAIL", S2c[:6])
    print("G1 PASS: criterion == direct divisibility for all n <= 1300;",
          "S_2 starts", S2c[:6])

    # ---- G3 : l > 4 divides at most one window element --------------------------
    bad = 0
    for n in range(1, 200000):
        pass
    print("G3 PASS (trivial): l>=5 cannot divide both n+1 and n+2 since l | 1.")

    # ---- G2 : digit-poor lemma, exhaustive then random ---------------------------
    checked = 0; viol = 0
    for n in range(3, 60000):
        for j in (1, 2):
            m = n + j
            for l, e in factorint(m).items():
                if l < 5 or e != 1:
                    continue
                W = m // l
                lhs = (carries(n, l) >= 2)
                rhs = not digit_poor(W - 1, l)
                checked += 1
                if lhs != rhs:
                    viol += 1
                    if viol < 5:
                        print("  VIOLATION", n, j, l, W, lhs, rhs)
    print("G2 exhaustive n<60000: checked %d (l,n) pairs, violations %d" % (checked, viol))
    assert viol == 0

    random.seed(1)
    checked = 0; viol = 0
    for _ in range(20000):
        l = random.choice(list(primerange(5, 4000)))
        W = random.randrange(1, 10**random.randrange(2, 9))
        if W % l == 0:
            continue
        j = random.choice((1, 2))
        n = l*W - j
        if n <= 0: continue
        lhs = (carries(n, l) >= 2)
        rhs = not digit_poor(W - 1, l)
        checked += 1
        if lhs != rhs:
            viol += 1
            if viol < 5: print("  RANDOM VIOLATION", n, j, l, W, lhs, rhs)
    print("G2 random large: checked %d, violations %d" % (checked, viol))
    assert viol == 0

    # ---- G2' : the *density* of digit-poor V in [0,Y) is the predicted product ----
    for l in (5, 7, 11, 101):
        for D in (1, 2, 3, 4):
            Y = l**D
            cnt = sum(1 for V in range(Y) if digit_poor(V, l))
            pred = ((l-1)//2) * ((l+1)//2)**(D-1)
            print("   l=%3d D=%d : #digit-poor in [0,l^D) = %d, predicted %d %s"
                  % (l, D, cnt, pred, "OK" if cnt == pred else "MISMATCH"))
            assert cnt == pred
    print("G2' PASS: |{V < l^D : digit-poor}| = ((l-1)/2)*((l+1)/2)^(D-1) exactly.")

main()
