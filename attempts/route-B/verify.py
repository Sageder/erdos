"""
verify.py -- INDEPENDENT verifier for Erdos 289 certificates.

Reads lines of the form "SOL n1 n2 n3 ..." (or a bare space/comma separated list of
integers) from the files given on the command line (or stdin) and checks, using
fractions.Fraction only -- no floats, no reuse of any search code:

  (1) every element is an integer >= 2,
  (2) the elements are distinct,
  (3) no isolated point: for every n in U, n-1 in U or n+1 in U,
  (4) sum_{n in U} 1/n == 1   exactly, as a Fraction.

Then prints the maximal run decomposition and the multiset of run lengths, plus
r = #runs and M = sum floor(L_i/2), so that P(k) holds for every k in [r, M].
"""
import sys, re
from fractions import Fraction


def check(U):
    errs = []
    if len(set(U)) != len(U):
        errs.append("repeated element")
    U = sorted(set(U))
    for n in U:
        if not isinstance(n, int) or n < 2:
            errs.append(f"element {n} not an integer >= 2")
    S = set(U)
    for n in U:
        if (n - 1) not in S and (n + 1) not in S:
            errs.append(f"isolated point {n}")
    tot = Fraction(0)
    for n in U:
        tot += Fraction(1, n)
    if tot != 1:
        errs.append(f"sum is {tot}, not 1")
    # runs
    runs = []
    cur = [U[0]]
    for x in U[1:]:
        if x == cur[-1] + 1:
            cur.append(x)
        else:
            runs.append(cur)
            cur = [x]
    runs.append(cur)
    lens = [len(r) for r in runs]
    return errs, runs, lens, tot


def main():
    texts = []
    if len(sys.argv) > 1:
        for fn in sys.argv[1:]:
            with open(fn) as f:
                texts.append(f.read())
    else:
        texts.append(sys.stdin.read())
    seen = set()
    nok = 0
    nbad = 0
    for text in texts:
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            if line.startswith("SOL"):
                line = line[3:]
            nums = re.findall(r"-?\d+", line)
            if not nums:
                continue
            U = [int(x) for x in nums]
            if len(U) < 2:
                continue
            key = tuple(sorted(U))
            if key in seen:
                continue
            seen.add(key)
            errs, runs, lens, tot = check(U)
            if errs:
                nbad += 1
                print("INVALID:", U)
                for e in errs:
                    print("   ", e)
            else:
                nok += 1
                r = len(runs)
                M = sum(l // 2 for l in lens)
                print(f"VALID  |U|={len(U)} max={max(U)} runs={r} "
                      f"lens={sorted(lens, reverse=True)} k-range=[{r},{M}] "
                      f"U={sorted(U)}")
    print(f"\n{nok} valid certificates, {nbad} invalid.")
    return 0 if nbad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
