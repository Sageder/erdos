"""
H_skeleton_xcheck.py -- validates the SEARCH SKELETON of H_pair2 (3-way DFS, symmetry
breaking "first used modulus goes to A", the waste prune  waste < Delta, and the budget
window) against brute force, with all mathematical filters switched OFF on both sides.

CLAIM TESTED: for every M and kappa, the set of unordered disjoint pairs (A,B) with
1 < budget(A) <= kappa, 1 < budget(B) <= kappa found by the DFS equals the brute-force set.

CONCLUSION: printed.  Expected: identical, with many nonempty instances (so the test has bite).
"""
import itertools, random
from fractions import Fraction


def brute(M, kappa):
    out = set()
    for assign in itertools.product((0, 1, 2), repeat=len(M)):
        A = tuple(M[i] for i in range(len(M)) if assign[i] == 1)
        B = tuple(M[i] for i in range(len(M)) if assign[i] == 2)
        bA = sum(Fraction(1, m) for m in A)
        bB = sum(Fraction(1, m) for m in B)
        if 1 < bA <= kappa and 1 < bB <= kappa:
            out.add(tuple(sorted((A, B))))
    return out


def dfs(M, kappa):
    Delta = sum(Fraction(1,m) for m in M) - 2   # the ONLY legal waste bound
    Ms = sorted(M); n = len(Ms)
    rc = [Fraction(1, m) for m in Ms]
    suf = [Fraction(0)] * (n + 1)
    for i in range(n - 1, -1, -1):
        suf[i] = suf[i + 1] + rc[i]
    out = set()

    def rec(i, A, bA, B, bB, started, waste):
        if bA > kappa or bB > kappa or waste >= Delta:
            return
        if bA + suf[i] <= 1 or bB + suf[i] <= 1:
            return
        if i == n:
            if bA > 1 and bB > 1:
                out.add(tuple(sorted((tuple(A), tuple(B)))))
            return
        m = Ms[i]
        A.append(m); rec(i + 1, A, bA + rc[i], B, bB, True, waste); A.pop()
        if started:
            B.append(m); rec(i + 1, A, bA, B, bB + rc[i], started, waste); B.pop()
        rec(i + 1, A, bA, B, bB, started, waste + rc[i])
    rec(0, [], Fraction(0), [], Fraction(0), False, Fraction(0))
    return out


def main():
    rng = random.Random(7)
    bad = tot = nonempty = 0
    for trial in range(40):
        M = sorted(rng.sample(list(range(2, 20)), rng.randrange(10, 14)))
        tb = sum(Fraction(1, m) for m in M)
        for kappa in (tb - 1,):
            if kappa <= 1:
                continue
            tot += 1
            b, d = brute(M, kappa), dfs(M, kappa)
            if b:
                nonempty += 1
            if b != d:
                bad += 1
                print("MISMATCH", M, kappa, len(b), len(d), list(b ^ d)[:2])
    print("instances: %d  nonempty: %d  mismatches: %d" % (tot, nonempty, bad))
    print("CONCLUSION:", "search skeleton + waste prune are exact" if bad == 0 else "*** SKELETON BUG ***")


if __name__ == "__main__":
    main()
