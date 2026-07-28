"""
H_theorem.py -- single self-contained audit of the two theorems of route H.

CLAIM TESTED / CERTIFIED:
  T2.  There is no covering system of Z with distinct moduli, all of the form p-1 (p >= 5
       prime), and all <= 254.                      [pure reciprocal-sum after Lemma L5]
  T3.  The same with 254 replaced by 724.           [+ exhaustive family enumeration]

The script re-derives every ingredient from scratch, in exact rational arithmetic:
  step 1  E = 2H;
  step 2  R(Y) = the Lemma-L5 fixpoint of H ∩ [2,Y];
  step 3  budget(R(127)) <= 2  and  budget(R(128)) > 2      -> T2 and its optimality;
  step 4  for every Y <= 362 with budget(R(Y)) > 2, the exhaustive disjoint-pair enumeration
          of H_pair.py returns the EMPTY list                -> T3.

CONCLUSION: printed.  Run time a few minutes.
"""
from fractions import Fraction
from sympy import isprime
from H_reduce import H_upto, reduce_set, budget
import H_pair
import sys


def main():
    # step 1
    X = 800
    E = [n for n in range(4, X + 1) if isprime(n + 1)]
    H = [m for m in range(2, X // 2 + 1) if isprime(2 * m + 1)]
    assert E == [2 * m for m in H if 2 * m <= X]
    print("step 1: E ∩ [4,%d] = 2·(H ∩ [2,%d])   OK" % (X, X // 2))

    # step 3
    b127 = budget(reduce_set(H_upto(127))[0])
    b128 = budget(reduce_set(H_upto(128))[0])
    assert b127 <= 2 < b128, (b127, b128)
    print("step 3: budget(R(127)) = %s = %.9f <= 2 ;  budget(R(128)) = %.9f > 2"
          % (b127, float(b127), float(b128)))
    print("        ==> THEOREM T2: no E-covering with all moduli <= 254.")

    # step 4
    bad = []
    Ys = sorted({Y for Y in range(128, 363)})
    # budget(R(Y)) is constant on long stretches; test one Y per distinct value, taking the
    # LARGEST Y of each stretch (that is the strongest statement, and it implies the rest)
    reps = {}
    for Y in Ys:
        b = budget(reduce_set(H_upto(Y))[0])
        reps[b] = Y
    print("step 4: %d distinct values of budget(R(Y)) for 128 <= Y <= 362" % len(reps))
    for b, Y in sorted(reps.items()):
        n, pairs = H_pair.analyse(Y, verbose=False)
        print("   Y=%-4d budget=%.9f  surviving families: %d" % (Y, float(b), n))
        sys.stdout.flush()
        if n:
            bad.append(Y)
    if bad:
        print("*** families survive at Y =", bad, " -- T3 NOT established")
    else:
        print("        ==> THEOREM T3: no covering system of Z with distinct moduli, all of")
        print("            the form p-1 (p prime >= 5), and all <= 724.")
    print()
    print("SCOPE: both theorems bound the moduli.  E is infinite; nothing here decides 273.")


if __name__ == "__main__":
    main()
