"""sync_witnesses.py — propagate class-C avoiders to classes A, B, D (same C=2).

A permutation satisfying BOTH pi(v) <= 2v and a(i) <= 2i is simultaneously a witness for
class A (pi(v) <= 2v), class B (a(i) <= 2i) and class D (pi(v) <= 2v for v <= N/2).
Also, restricting a class-A avoider of [1..N] to values 1..N' (position order) gives a
class-A avoider of [1..N'] (positions only shrink; 4-AP-freeness inherited by the
restriction principle).  This script appends the largest class-C witnesses to the A/B/D
avoider files (marked how=from-C-class) so the existence tables reflect them.
Idempotent: skips lines already present.
"""

import os

HERE = os.path.dirname(os.path.abspath(__file__))
AVD = os.path.join(HERE, "avoiders")


def load_lines(fn):
    if not os.path.exists(fn):
        return []
    return [l.strip() for l in open(fn) if l.strip()]


def main():
    src = os.path.join(AVD, "C_2_1.txt")
    entries = []
    for line in load_lines(src):
        parts = dict(p.split("=", 1) for p in line.split())
        entries.append((int(parts["N"]), parts["perm"]))
    entries.sort()
    top = entries[-3:]          # largest three
    for cls in ("A", "B", "D"):
        fn = os.path.join(AVD, f"{cls}_2_1.txt")
        have = set(load_lines(fn))
        with open(fn, "a") as f:
            for N, perm in top:
                line = f"N={N} how=from-C-class perm={perm}"
                if line not in have:
                    f.write(line + "\n")
        print(f"{cls}_2_1.txt <- witnesses at N={[n for n, _ in top]}")


if __name__ == "__main__":
    main()
