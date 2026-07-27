"""asym_exhaust.py — EXHAUSTIVE existence of permutations of [1..N] with no decreasing
monotone 3-AP and no increasing monotone 4-AP. Full backtracking DFS over positions of
values 1..N placed in increasing value order, interval pruning as in asym_strategy.py.
Reports EXISTS / EXTINCT (exhaustive) per N, with node counts.
Extinction is inherited upward: restriction of a witness of [1..N+1] to [1..N] is a
witness (both forbidden patterns are preserved under value-restriction... more precisely
any dec-3AP/inc-4AP of the restriction is one of the parent, so witness parents restrict
to witnesses).
"""
import sys
sys.setrecursionlimit(100000)

def exists_witness(N, node_cap=None):
    pos = [0] * (N + 1)
    occupied = [False] * (N + 2)
    nodes = 0
    def rec(v):
        nonlocal nodes
        if v > N:
            return True
        nodes += 1
        if node_cap and nodes > node_cap:
            raise TimeoutError
        lo, hi = 0, N + 1
        for d in range(1, (v - 1) // 2 + 1):
            if pos[v - 2 * d] > pos[v - d]:
                if pos[v - d] > lo: lo = pos[v - d]
        for d in range(1, (v - 1) // 3 + 1):
            if pos[v - 3 * d] < pos[v - 2 * d] < pos[v - d]:
                if pos[v - d] < hi: hi = pos[v - d]
        for p in range(lo + 1, hi):
            if not occupied[p]:
                occupied[p] = True; pos[v] = p
                if rec(v + 1):
                    return True
                occupied[p] = False; pos[v] = 0
        return False
    r = rec(1)
    return r, nodes

if __name__ == "__main__":
    import time
    for N in range(20, 41):
        t0 = time.time()
        try:
            r, nodes = exists_witness(N, node_cap=200_000_000)
            print(f"N={N}: {'EXISTS' if r else 'EXTINCT (exhaustive)'}  nodes={nodes}  ({time.time()-t0:.1f}s)", flush=True)
            if not r:
                print("THEOREM: no permutation of [1..%d] avoids both dec-3APs and inc-4APs; inherited for all larger N." % N)
                break
        except TimeoutError:
            print(f"N={N}: node cap hit ({time.time()-t0:.1f}s) — inconclusive", flush=True)
            break
