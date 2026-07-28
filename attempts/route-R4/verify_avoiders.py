"""verify_avoiders.py — independent verification of every saved avoider.

Reads avoiders/*.txt (lines "N=.. how=.. perm=c1,c2,..."), and for each entry checks,
independently of the search engines:
  (1) perm is a permutation of [1..N];
  (2) the displacement constraints of its class hold with EXACT rational arithmetic;
  (3) no monotone 4-AP, using the validated checker apcheck.has_monotone_kap_pos
      (validated against the literal brute-force definition in experiments/apcheck.py);
      additionally the literal brute-force checker itself for N <= 10.
Exit nonzero on any failure.  Also verifies avoiders/seq_*.txt (class Bp sequences,
distinct values, a(i) <= C*i, 4-AP-free via has_monotone_kap_general).
"""

import glob
import os
import sys
from fractions import Fraction

sys.path.insert(0, "/home/user/erdos/experiments")
from apcheck import has_monotone_kap_pos, has_monotone_kap_brute, has_monotone_kap_general

HERE = os.path.dirname(os.path.abspath(__file__))


def check_perm_file(fn):
    base = os.path.basename(fn)[:-4]          # e.g. A_2_1 or A_3_2_ceil
    parts = base.split("_")
    ceil = parts[-1] == "ceil"
    if ceil:
        parts = parts[:-1]
    cls, num, den = parts
    C = Fraction(int(num), int(den))
    n_checked = 0
    for line in open(fn):
        line = line.strip()
        if not line:
            continue
        parts = dict(p.split("=", 1) for p in line.split())
        N = int(parts["N"])
        perm = [int(x) for x in parts["perm"].split(",")]
        assert len(perm) == N and sorted(perm) == list(range(1, N + 1)), \
            f"{fn}: N={N} not a permutation"
        pos = {v: i + 1 for i, v in enumerate(perm)}
        num, den = C.numerator, C.denominator
        for v in range(1, N + 1):
            if cls in ("A", "C"):
                hi = -((-num * v) // den) if ceil else (num * v) // den
                assert pos[v] <= hi, f"{fn}: N={N} v={v} pos={pos[v]} violates pi(v)<=Cv ({'ceil' if ceil else 'floor'})"
            if cls in ("B", "C"):
                # floor: a(i) <= floor(C i);  ceil: a(i) <= ceil(C i)
                cap = -((-num * pos[v]) // den) if ceil else (num * pos[v]) // den
                assert v <= cap, f"{fn}: N={N} v={v} pos={pos[v]} violates a(i)<=Ci"
            if cls == "D" and v <= N // 2:
                assert pos[v] <= 2 * v, f"{fn}: N={N} v={v} pos={pos[v]} violates D"
        assert not has_monotone_kap_pos(perm, 4), f"{fn}: N={N} has monotone 4-AP!"
        if N <= 10:
            assert not has_monotone_kap_brute(perm, 4), f"{fn}: N={N} brute disagrees!"
        n_checked += 1
    return n_checked


def check_seq_file(fn):
    base = os.path.basename(fn)[:-4]          # seq_B_num_den
    _, cls, num, den = base.split("_")
    C = Fraction(int(num), int(den))
    n_checked = 0
    for line in open(fn):
        line = line.strip()
        if not line:
            continue
        parts = dict(p.split("=", 1) for p in line.split())
        N = int(parts["N"])
        seq = [int(x) for x in parts["perm"].split(",")]
        assert len(seq) == N and len(set(seq)) == N and min(seq) >= 1, \
            f"{fn}: N={N} not injective/positive"
        for i, v in enumerate(seq, start=1):
            assert Fraction(v) <= C * i, f"{fn}: N={N} i={i} a(i)={v} violates a(i)<=Ci"
        assert not has_monotone_kap_general(seq, 4), f"{fn}: N={N} has monotone 4-AP!"
        n_checked += 1
    return n_checked


if __name__ == "__main__":
    total = 0
    for fn in sorted(glob.glob(os.path.join(HERE, "avoiders", "*.txt"))):
        base = os.path.basename(fn)
        if base.startswith("seq_"):
            c = check_seq_file(fn)
        else:
            c = check_perm_file(fn)
        print(f"  {base}: {c} avoiders verified")
        total += c
    print(f"ALL {total} SAVED AVOIDERS INDEPENDENTLY VERIFIED "
          f"(permutation/injectivity + exact constraints + validated 4-AP checkers)")
