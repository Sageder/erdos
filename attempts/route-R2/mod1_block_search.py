"""mod1_block_search.py — Modification idea 1 (the serious one).

Scheme: keep block-major interval blocks B_m = [c_m, c_{m+1}) with ratio
c_{m+1}/c_m >= 4, but allow ARBITRARY internal orders pi_m.  A complete local
constraint analysis (REPORT.md, Prop. M1) shows the resulting permutation has
NO monotone 4-AP if and only if every pi_m avoids, inside its block [c, C)
(C = 4c, previous block start c' = c/4):

 A4    ascending  w, w+e, w+2e, w+3e            (all in block)
 D4    descending w+3e, w+2e, w+e, w            (all in block)
 A3T   ascending  w, w+e, w+2e     with tail  w+3e >= C
 A3H   ascending  w, w+e, w+2e     with head  1 <= w-e < c
 A2T   ascending  u, u+e           with head  1 <= u-e < c   and tail u+2e >= C
 A2H   ascending  u, u+e           with heads u-2e in [c', c), u-3e in [1, c')
                                   (two singleton heads in distinct earlier blocks)
 A2HH  ascending  u, u+e           with heads u-2e, u-3e in [c', c) forming an
                                   ASCENDING pair in pi_{m-1}   (shape (2,2))

All constraints except A2HH are independent of the other blocks, so:
  * if the A2HH-free system is UNSAT for some block, the whole scheme dies
    at that block regardless of all other choices;
  * if SAT, we search sequentially (choosing each pi_m, feeding its ascending
    pairs into the next block's A2HH).

This script does exact backtracking (exhaustive on failure) per block.
"""

import sys
import time


def search_block(c, mode="independent", prev_asc=frozenset(),
                 count_all=False, node_limit=None):
    """Backtracking search for a valid internal order of [c, 4c).

    mode 'independent': ignore A2HH (safe relaxation: UNSAT here => truly UNSAT).
    mode 'sequential' : include A2HH against prev_asc (ascending pairs of pi_{m-1}).
    Returns (status, data): ('SAT', order) / ('UNSAT', nodes) /
    ('UNKNOWN', nodes) if node_limit hit / ('COUNT', n_solutions).
    """
    C = 4 * c
    cp = c // 4 if c >= 4 else 0          # previous block start (c'=c/4); c=1 has none
    vals = list(range(c, C))
    size = len(vals)
    pos = {}
    order = []
    nodes = 0
    solutions = [] if count_all else None

    def ok_to_place(v):
        # v would occupy the next (rightmost) position: it is the LAST element
        # of any pattern it completes.
        # A4: v = w+3e largest of ascending 4-AP.
        e = 1
        while v - 3 * e >= c:
            a, b, cc = v - 3 * e, v - 2 * e, v - e
            if a in pos and b in pos and cc in pos and pos[a] < pos[b] < pos[cc]:
                return False
            e += 1
        # D4: v = w smallest, placed last, others descending before it.
        e = 1
        while v + 3 * e < C:
            a, b, cc = v + 3 * e, v + 2 * e, v + e
            if a in pos and b in pos and cc in pos and pos[a] < pos[b] < pos[cc]:
                return False
            e += 1
        # A3T / A3H: v = w+2e largest of ascending 3-AP.
        e = 1
        while v - 2 * e >= c:
            a, b = v - 2 * e, v - e
            if a in pos and b in pos and pos[a] < pos[b]:
                if v + e >= C:                     # tail exists (A3T)
                    return False
                if 1 <= v - 3 * e < c:             # head exists (A3H)
                    return False
            e += 1
        # A2T / A2H / A2HH: v = u+e completing ascending pair (u, v).
        e = 1
        while v - e >= c:
            u = v - e
            if u in pos:
                if 1 <= v - 2 * e < c and v + e >= C:              # A2T
                    return False
                if cp <= v - 2 * e < c and 1 <= v - 3 * e < cp:    # A2H
                    return False
                if mode == "sequential" and cp >= 1 \
                        and cp <= v - 3 * e and v - 2 * e < c \
                        and (v - 3 * e, v - 2 * e) in prev_asc:    # A2HH
                    return False
            e += 1
        return True

    remaining = set(vals)
    sys.setrecursionlimit(10000)

    def dfs():
        nonlocal nodes
        if node_limit is not None and nodes > node_limit:
            raise TimeoutError
        if not remaining:
            if count_all:
                solutions.append(list(order))
                return False        # keep searching
            return True
        # try larger values first (heuristic: descending-ish orders are safer)
        for v in sorted(remaining, reverse=True):
            nodes += 1
            if ok_to_place(v):
                remaining.discard(v)
                pos[v] = len(order)
                order.append(v)
                if dfs():
                    return True
                order.pop()
                del pos[v]
                remaining.add(v)
        return False

    try:
        found = dfs()
    except TimeoutError:
        return ("UNKNOWN", nodes)
    if count_all:
        return ("COUNT", solutions)
    if found:
        return ("SAT", list(order))
    return ("UNSAT", nodes)


def asc_pairs(order):
    p = {v: i for i, v in enumerate(order)}
    return frozenset((a, b) for a in order for b in order
                     if a < b and p[a] < p[b])


def verify_no_4ap_prefix(orders, starts):
    """Independent verification: build the concatenated prefix from the found
    block orders and run the validated 4-AP checker on it."""
    sys.path.insert(0, "/home/user/erdos/attempts/route-R2")
    from checkers import find_monotone_kap
    pref = []
    for o in orders:
        pref.extend(o)
    n = len(pref)
    assert sorted(pref) == list(range(1, n + 1))
    return find_monotone_kap(pref, 4), pref


if __name__ == "__main__":
    out = []

    def log(s):
        print(s, flush=True)
        out.append(s)

    # ---- Stage 1: block-independent satisfiability, c = 4^m --------------
    for m, c in enumerate([1, 4, 16, 64]):
        t0 = time.time()
        limit = 2 * 10 ** 8 if c == 64 else None
        status, data = search_block(c, mode="independent", node_limit=limit)
        dt = time.time() - t0
        if status == "SAT":
            log("block m=%d  [%d,%d): SAT (independent constraints), "
                "example order found in %.1fs" % (m, c, 4 * c, dt))
            log("   pi = %s" % (data,))
        else:
            log("block m=%d  [%d,%d): %s after %s nodes (%.1fs)"
                % (m, c, 4 * c, status, data, dt))

    # ---- Stage 2: sequential construction with A2HH ----------------------
    log("")
    log("sequential mode (A2HH active, feeding ascending pairs forward):")
    orders = []
    prev = frozenset()
    ok = True
    for m, c in enumerate([1, 4, 16, 64]):
        t0 = time.time()
        limit = 2 * 10 ** 8 if c == 64 else None
        status, data = search_block(c, mode="sequential", prev_asc=prev,
                                    node_limit=limit)
        dt = time.time() - t0
        if status != "SAT":
            log("block m=%d: %s (%s nodes, %.1fs) -- sequential chain stops"
                % (m, status, data, dt))
            ok = False
            break
        log("block m=%d: SAT sequentially (%.1fs); pi_%d = %s%s"
            % (m, dt, m, data[:16], "..." if len(data) > 16 else ""))
        orders.append(data)
        prev = asc_pairs(data)

    if orders:
        w, pref = verify_no_4ap_prefix(orders, None)
        log("")
        log("independent recheck of concatenated prefix (N=%d) with validated "
            "checker: monotone 4-AP: %s" % (len(pref),
            "NONE" if w is None else "FOUND %r  <-- constraint model WRONG" % (w,)))
        with open("/home/user/erdos/attempts/route-R2/mod1_prefix.txt", "w") as f:
            f.write(" ".join(map(str, pref)) + "\n")

    with open("/home/user/erdos/attempts/route-R2/mod1_output.txt", "w") as f:
        f.write("\n".join(out) + "\n")
