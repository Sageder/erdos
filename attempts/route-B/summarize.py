"""
summarize.py -- final consolidation.

Re-verifies every certificate in the given files with fractions.Fraction and emits
  certificates_all.txt   one line per distinct certificate:
                         max |U| r M  runlengths  U
  kcoverage.txt          for every realisable k, one explicit witness certificate
  runlengths.txt         the distinct multisets of maximal run lengths, with counts
"""
import sys, re
from fractions import Fraction
from collections import Counter


def runs_of(U):
    runs = []
    cur = [U[0]]
    for x in U[1:]:
        if x == cur[-1] + 1:
            cur.append(x)
        else:
            runs.append(cur); cur = [x]
    runs.append(cur)
    return runs


def main(files):
    certs = {}
    dropped = 0
    for fn in files:
        for line in open(fn):
            if not line.startswith("SOL"):
                continue
            U = tuple(sorted(int(x) for x in re.findall(r"\d+", line[3:])))
            if U in certs:
                continue
            S = set(U)
            if (len(S) != len(U) or any(n < 2 for n in U)
                    or any((n - 1) not in S and (n + 1) not in S for n in U)
                    or sum(Fraction(1, n) for n in U) != 1):
                dropped += 1
                continue
            rs = runs_of(list(U))
            lens = tuple(sorted((len(r) for r in rs), reverse=True))
            certs[U] = lens
    print(f"{len(certs)} distinct certificates re-verified with Fraction "
          f"({dropped} malformed lines dropped)")

    with open("certificates_all.txt", "w") as f:
        f.write("# max(U)  |U|  r  M  runlengths  U    "
                "(all verified: sum 1/n == 1, elements >= 2, no isolated point)\n")
        for U in sorted(certs, key=lambda u: (max(u), len(u), u)):
            lens = certs[U]
            r = len(lens); M = sum(l // 2 for l in lens)
            f.write(f"{max(U)} {len(U)} {r} {M} {','.join(map(str, lens))} "
                    f"{' '.join(map(str, U))}\n")

    # k coverage with witnesses (prefer the witness with the smallest max(U))
    wit = {}
    for U, lens in certs.items():
        r = len(lens); M = sum(l // 2 for l in lens)
        for k in range(r, M + 1):
            if k not in wit or max(U) < max(wit[k]):
                wit[k] = U
    ks = sorted(wit)
    gaps = [k for k in range(ks[0], ks[-1] + 1) if k not in wit]
    with open("kcoverage.txt", "w") as f:
        f.write(f"# k realisable by an explicit verified certificate: "
                f"{ks[0]}..{ks[-1]}, gaps {gaps}\n")
        f.write("# k  r  M  max(U)  runlengths  U\n")
        for k in ks:
            U = wit[k]; lens = certs[U]
            r = len(lens); M = sum(l // 2 for l in lens)
            f.write(f"{k} {r} {M} {max(U)} {','.join(map(str, lens))} "
                    f"{' '.join(map(str, U))}\n")
    print(f"k coverage: {ks[0]}..{ks[-1]}  gaps={gaps}")

    cnt = Counter(certs.values())
    with open("runlengths.txt", "w") as f:
        f.write(f"# {len(cnt)} distinct multisets of maximal run lengths\n")
        f.write("# count  multiset\n")
        for lens, c in sorted(cnt.items(), key=lambda kv: (-kv[1], kv[0])):
            f.write(f"{c} {','.join(map(str, lens))}\n")
    print(f"{len(cnt)} distinct run-length multisets")
    mx = max(certs, key=lambda u: sum(l // 2 for l in certs[u]))
    print(f"largest M = {sum(l//2 for l in certs[mx])} (|U|={len(mx)}, max={max(mx)})")


if __name__ == "__main__":
    main(sys.argv[1:])
