"""
A_bruteforce_check.py

CLAIM TESTED: the SAT encoding of A_sat_cover.py is FAITHFUL.  For many small L and both
worlds and both modes, an independent exhaustive depth-first search ("cover the smallest
uncovered residue; the covering class is then forced for each candidate modulus") is run
and its SAT/UNSAT verdict is compared with the SAT solver's verdict.

The DFS is complete: any covering must cover the smallest uncovered residue r, hence some
unused modulus n has its class equal to r mod n.  Branching over the unused moduli is
therefore exhaustive.

CONCLUSION: printed; agreement on every tested instance is recorded in
attempts/route-A-satsearch/FINDINGS.md.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from A_common import D_E, D_H, D_V
from A_sat_cover import run


def dfs_exists(L, mods, relaxed=False):
    """Exhaustive search.  relaxed=True: residue 0 must stay UNcovered, all others covered."""
    cov = bytearray(L)
    if relaxed:
        cov[0] = 1                      # pretend covered so it is never selected
    used = [False] * len(mods)
    start = [0]

    def rec():
        r = 0
        while r < L and cov[r]:
            r += 1
        if r == L:
            return True
        for i, n in enumerate(mods):
            if used[i]:
                continue
            a = r % n
            if relaxed and a == 0:
                continue                # would cover residue 0
            touched = [j for j in range(a, L, n) if not cov[j]]
            if relaxed and any(j == 0 for j in range(a, L, n)):
                continue
            for j in touched:
                cov[j] = 1
            used[i] = True
            if rec():
                return True
            used[i] = False
            for j in touched:
                cov[j] = 0
        return False

    return rec()


if __name__ == "__main__":
    tests = []
    LS = ([int(x) for x in sys.argv[1].split(",")] if len(sys.argv) > 1 else
          [24, 36, 48, 60, 72, 90, 120, 144, 180, 240, 252, 360, 420, 504, 540, 720])
    WS = sys.argv[2].split(",") if len(sys.argv) > 2 else ["E", "H", "V"]
    for L in LS:
        for world in WS:
            for mode in ["full", "relaxed"]:
                tests.append((L, world, mode))
    agree = disagree = 0
    for L, world, mode in tests:
        mods = {"E": D_E, "H": D_H, "V": D_V}[world](L)
        if not mods:
            continue
        thr = 1.0 if mode == "full" else (L - 1.0) / L
        if sum(1.0 / m for m in mods) <= thr:
            continue                     # SAT side short-circuits on the density bound
        exp = dfs_exists(L, mods, relaxed=(mode == "relaxed"))
        out = run(L, world, mode, None, None, "weak", 6, 0, "cadical153", 120,
                  "/tmp/none_", tag="_bf")
        got = out["verdict"] == "SAT"
        ok = (exp == got)
        agree += ok
        disagree += (not ok)
        print(f"  CHECK L={L} world={world} mode={mode}: dfs={exp} sat={got} "
              f"{'AGREE' if ok else '*** DISAGREE ***'}")
    print(f"\nagree={agree} disagree={disagree}")
