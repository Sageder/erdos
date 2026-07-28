"""
analyze.py -- read certificate files, re-verify each with Fraction, and report:
  * how many distinct certificates,
  * the multiset of maximal run lengths of each,
  * the k-interval [r, M] each certificate realises via the splitting lemma
    (r = #runs, M = sum floor(L_i/2)), and the union of those intervals,
  * the certificates with the largest M and the widest interval.
"""
import sys, re
from fractions import Fraction
from collections import Counter


REJECT = []


def load(files):
    seen = {}
    for fn in files:
        with open(fn) as f:
            for line in f:
                if not line.startswith("SOL"):
                    continue
                U = tuple(sorted(int(x) for x in re.findall(r"\d+", line[3:])))
                if U in seen:
                    continue
                # A file may be truncated mid-line while a search is still running;
                # such a line is silently dropped (counted), never accepted.
                S = set(U)
                if (len(S) != len(U) or any(n < 2 for n in U)
                        or any((n - 1) not in S and (n + 1) not in S for n in U)
                        or sum(Fraction(1, n) for n in U) != 1):
                    REJECT.append((fn, U))
                    continue
                runs = []
                cur = [U[0]]
                for x in U[1:]:
                    if x == cur[-1] + 1:
                        cur.append(x)
                    else:
                        runs.append(cur); cur = [x]
                runs.append(cur)
                lens = tuple(sorted((len(r) for r in runs), reverse=True))
                seen[U] = lens
    return seen


def main():
    seen = load(sys.argv[1:])
    print(f"{len(seen)} distinct verified certificates "
          f"({len(REJECT)} malformed/partial lines dropped)")
    cover = set()
    best_M = (0, None)
    best_width = (-1, None)
    lenmultisets = Counter()
    maxel = Counter()
    for U, lens in seen.items():
        r = len(lens)
        M = sum(l // 2 for l in lens)
        cover |= set(range(r, M + 1))
        if M > best_M[0]:
            best_M = (M, U)
        if M - r > best_width[0]:
            best_width = (M - r, U)
        lenmultisets[lens] += 1
        maxel[max(U)] += 1
    ks = sorted(cover)
    print(f"k values realised by these certificates: {ks}")
    # contiguity
    if ks:
        gaps = [k for k in range(ks[0], ks[-1] + 1) if k not in cover]
        print(f"range [{ks[0]},{ks[-1]}], missing inside: {gaps}")
    print(f"largest M = {best_M[0]} by U={best_M[1]}")
    print(f"widest interval M-r = {best_width[0]} by U={best_width[1]}")
    print(f"\nmost common run-length multisets:")
    for lens, c in lenmultisets.most_common(15):
        print(f"   {lens}  x{c}")
    print(f"\ndistinct run-length multisets: {len(lenmultisets)}")
    print(f"max(U) distribution (top 15): {maxel.most_common(15)}")


if __name__ == "__main__":
    main()
