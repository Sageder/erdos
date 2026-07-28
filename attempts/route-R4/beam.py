"""beam.py — insertion beam search: cheap existence frontier-pusher (classes A/C/B/D).

Fact used: if tau is a monotone-4-AP-free permutation of [1..N] then deleting value N
(and closing the position gap) gives a monotone-4-AP-free permutation of [1..N-1]; the
new maximum N can only be the LARGEST value of any 4-AP, so inserting N at slot p into
an avoider sigma of [1..N-1] creates an avoider of [1..N] iff
  - for every d>=1 with N-3d>=1: if pos(N-3d)<pos(N-2d)<pos(N-d) then p <= pos(N-d)
    (positions in sigma; insertion at p <= q means N precedes the value at old slot q);
    if pos(N-3d)>pos(N-2d)>pos(N-d) then p > pos(N-d);
  - class bounds on p for value N;
  - shifted values keep their bounds (class A: pos <= Cv can break for values at the
    wall -> require p > their positions; class B: v <= C*pos only improves on shift).
Sound (every emitted permutation is verified-constructible); NOT complete for fixed
beam width — used only for EXISTS claims.  Every found avoider re-checked by the
validated apcheck checker before saving.

usage: python3 beam.py cls num den N_target [width] [round]
Seeds from avoiders/<cls>_<num>_<den>[<_ceil>].txt largest-N entries.
Appends new avoiders (largest N reached, plus every 25th level) to the same file.
"""

import os
import random
import sys
from fractions import Fraction

sys.path.insert(0, "/home/user/erdos/experiments")
from apcheck import has_monotone_kap_pos

HERE = os.path.dirname(os.path.abspath(__file__))
AVD = os.path.join(HERE, "avoiders")


def bounds(v, cls, num, den, N, rnd):
    lo, hi = 1, N
    if cls in ("A", "C"):
        h = (num * v + den - 1) // den if rnd == "c" else (num * v) // den
        hi = min(hi, h)
    if cls in ("B", "C"):
        lo = den * (v - 1) // num + 1 if rnd == "c" else -((-v * den) // num)
    if cls == "D" and v <= N // 2:
        hi = min(hi, 2 * v)
    return lo, hi


def children(perm, cls, num, den, rnd):
    """All valid insertion slots for value N = len(perm)+1.  Slot p in 1..N means
    N is placed before the element currently at position p (p=N: append)."""
    N = len(perm) + 1
    pos = {v: i + 1 for i, v in enumerate(perm)}
    L, U = bounds(N, cls, num, den, N, rnd)
    # AP interval constraints (N is the largest AP element)
    d = 1
    while N - 3 * d >= 1:
        p1, p2, p3 = pos[N - 3 * d], pos[N - 2 * d], pos[N - d]
        if p1 < p2 < p3:
            U = min(U, p3)          # insert at p <= p3 puts N before value N-d
        elif p1 > p2 > p3:
            L = max(L, p3 + 1)
        if L > U:
            return []
        d += 1
    # shifted values must keep upper bounds: values with old pos >= p get pos+1
    if cls in ("A", "C", "D"):
        for v in range(1, N):
            lo_v, hi_v = bounds(v, cls, num, den, N, rnd)
            if pos[v] > hi_v:               # violates new-N bound even unshifted (class D)
                return []
            if pos[v] + 1 > hi_v:           # would break if shifted
                L = max(L, pos[v] + 1)
        if L > U:
            return []
    out = []
    for p in range(L, U + 1):
        out.append(perm[:p - 1] + (N,) + perm[p - 1:])
    return out


def seed_file(cls, num, den, rnd):
    suf = "_ceil" if rnd == "c" else ""
    return os.path.join(AVD, f"{cls}_{num}_{den}{suf}.txt")


def main():
    cls = sys.argv[1]
    num, den = int(sys.argv[2]), int(sys.argv[3])
    n_target = int(sys.argv[4])
    width = int(sys.argv[5]) if len(sys.argv) > 5 else 4000
    rnd = sys.argv[6] if len(sys.argv) > 6 else "f"
    rng = random.Random(196)
    fn = seed_file(cls, num, den, rnd)
    seeds = []
    best_n = 0
    for line in open(fn):
        parts = dict(p.split("=", 1) for p in line.split())
        n = int(parts["N"])
        if n > best_n:
            best_n, seeds = n, []
        if n == best_n:
            seeds.append(tuple(int(x) for x in parts["perm"].split(",")))
    beam = sorted(set(seeds))
    print(f"seeding from {len(beam)} avoiders at N={best_n}", flush=True)
    N = best_n
    while N < n_target and beam:
        nxt = []
        seen = set()
        for parent in beam:
            for ch in children(parent, cls, num, den, rnd):
                if ch not in seen:
                    seen.add(ch)
                    nxt.append(ch)
        N += 1
        if not nxt:
            print(f"beam died at N={N} (no valid insertion for any of {len(beam)} parents)",
                  flush=True)
            beam = []
            break
        if len(nxt) > width:
            nxt = rng.sample(nxt, width)
        beam = sorted(nxt)
        if N % 10 == 0 or N == n_target:
            print(f"N={N}: beam {len(beam)}", flush=True)
        if N % 25 == 0 or N == n_target:
            ex = beam[0]
            assert not has_monotone_kap_pos(list(ex), 4)
            with open(fn, "a") as f:
                f.write(f"N={N} how=beam-w{width} perm=" + ",".join(map(str, ex)) + "\n")
    if beam:
        print(f"reached N={N} with {len(beam)} avoiders; saved examples", flush=True)


if __name__ == "__main__":
    main()
