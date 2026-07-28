"""
F_smallX.py -- Route F, Erdos 273, task (b) quantitative refinement.

CLAIM TESTED: the doubling staircase of F_infimum.py achieves waste W = 4
(cost 1 + 4/L) for L = 3*2^a.  PROVED lower bound: W >= 2 (see FINDINGS §1).
Is W = 2 or W = 3 ever achievable?  This script decides it EXHAUSTIVELY for
every L up to a bound:

  For each L, moduli are distinct divisors > 1 of L, so the numbers L/n_i are
  DISTINCT PROPER divisors of L summing to L + W.  Necessary filter:
     (i)  sigma(L) - L >= L + 2      (L abundant enough), and
     (ii) some subset of the proper divisors of L sums to exactly L+2 or L+3.
  Then run the exact branch-and-bound (F_mincost) with waste cap 3.

Any L that passes the filter and returns NOSOL_UPTO 3 provably has X(L) >= 4.
Covering ALL L <= N therefore proves: every covering system with distinct
moduli and lcm <= N has sum 1/n_i >= 1 + 4/lcm.

CONCLUSION: printed; see FINDINGS.md.
"""
import subprocess, sys, os, time

BIN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "F_mincost")


def sigma_sieve(N):
    s = [0] * (N + 1)
    for d in range(1, N + 1):
        for m in range(d, N + 1, d):
            s[m] += d
    return s


def divisors(L):
    ds, i = [], 1
    while i * i <= L:
        if L % i == 0:
            ds.append(i)
            if i != L // i:
                ds.append(L // i)
        i += 1
    return sorted(ds)


def subset_hits(vals, targets, cap):
    """Is some subset of vals summing to a value in targets?  DP bitset."""
    reach = 1
    mask = (1 << (cap + 1)) - 1
    for v in vals:
        reach |= (reach << v) & mask
    return [t for t in targets if (reach >> t) & 1]


NODECAP = 40000000


def main():
    global NODECAP
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    NODECAP = int(sys.argv[2]) if len(sys.argv) > 2 else 40000000
    t0 = time.time()
    sig = sigma_sieve(N)
    tested = passed = 0
    hits = []
    unknown = []
    for L in range(2, N + 1):
        if sig[L] - L < L + 2:          # not enough divisor mass
            continue
        ds = divisors(L)
        proper = [d for d in ds if d < L]     # values L/n_i, n_i > 1
        tg = subset_hits(proper, [L + 2, L + 3], L + 3)
        if not tg:
            continue
        tested += 1
        mods = [d for d in ds if d > 1]
        cmd = [BIN, str(L), "3", str(NODECAP)] + [str(d) for d in mods]
        p = subprocess.run(cmd, capture_output=True, text=True)
        last = p.stdout.strip().splitlines()[-1]
        if last.startswith("X="):
            hits.append((L, last))
            print(f"!!! L={L}  {last}", flush=True)
        elif last.startswith("ABORT"):
            unknown.append(L)
            print(f"  ?  L={L} UNKNOWN (node cap)", flush=True)
        else:
            passed += 1
        if tested % 200 == 0:
            print(f"  ... L={L}, {tested} L tested, {time.time()-t0:.0f}s", flush=True)
    print(f"\nRange L <= {N}: {tested} L passed the arithmetic filter and were "
          f"searched exhaustively for waste <= 3.")
    print(f"  {passed} proved to have X(L) >= 4;  {len(hits)} with X(L) <= 3: {hits}")
    print(f"  {len(unknown)} UNKNOWN (hit the node cap): {unknown}")
    print(f"  total {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
