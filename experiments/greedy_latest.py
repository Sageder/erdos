"""greedy_latest.py — the canonical online construction suggested by CORE.md Lemma 8 +
Theorem 16.

Values arrive in increasing order v = 1, 2, 3, ...; each is inserted into the current
linear order. By Lemma 8 the ONLY constraints when inserting v (the largest value so
far) are, for every d >= 1 with v - 3d >= 1:
  (inc)  if (v-3d, v-2d, v-d) is positionally increasing  ->  v must go BEFORE v-d
  (dec)  if (v-3d, v-2d, v-d) is positionally decreasing  ->  v must go AFTER  v-d
so the admissible slots form the open interval (Lo(v), Hi(v)).

STRATEGY "latest": insert v at the last admissible slot (just before the Hi-witness, or
at the very end when there is no inc-constraint). This is the strategy that minimizes
how far forward values are pushed, i.e. the one most favourable to order type omega
(Theorem 16: a value is pushed before x only when FORCED, and the set of forced jumpers
over x is exactly the forcing closure of the values at or before x).

What this script measures:
  - does the process ever get STUCK (Lo >= Hi, i.e. an X-configuration of Lemma 10)?
  - do the positions of small values STABILIZE (necessary and sufficient for order
    type omega in the limit of this process)?
  - the displacement profile pos(v)/v and the closure statistics.
IMPORTANT: even if positions appear to stabilize over a finite run, that is EVIDENCE
only; order type omega is an infinite statement.

Every prefix produced is verified 4-AP-free with the trusted checker.
"""

import sys
sys.path.insert(0, '/home/user/erdos/experiments')
from apcheck import has_monotone_kap_pos


def run(N, strategy="latest", verify_every=0, track=(1, 2, 3, 4, 5, 6, 7, 8)):
    """Returns (order, stuck_at, history) where order is the list of values in position
    order, stuck_at is None or the value at which no slot existed, and history records
    the positions of the tracked values after each insertion milestone."""
    order = []          # values in position order
    idx = {}            # value -> current index in `order`
    history = []
    stuck_at = None

    for v in range(1, N + 1):
        lo, hi = -1, len(order)          # slot bounds: insert index s with lo < s <= hi
        d = 1
        while v - 3 * d >= 1:
            a, b, c = idx[v - 3 * d], idx[v - 2 * d], idx[v - d]
            if a < b < c:
                if c < hi:
                    hi = c               # v strictly before v-d
            elif a > b > c:
                if c > lo:
                    lo = c               # v strictly after v-d
            d += 1
        if strategy == "latest":
            slot = hi
        elif strategy == "earliest":
            slot = lo + 1
        else:
            slot = (lo + 1 + hi) // 2
        if lo + 1 > hi:                     # no admissible slot: X-configuration
            stuck_at = v
            break
        slot = max(lo + 1, min(slot, hi))   # clamp into the admissible window
        order.insert(slot, v)
        for i in range(slot, len(order)):   # reindex the shifted tail
            idx[order[i]] = i
        if v in (10, 100, 500, 1000, 2000, 4000, 8000) or v == N:
            history.append((v, {t: idx[t] + 1 for t in track if t in idx}))
        if verify_every and v % verify_every == 0:
            assert not has_monotone_kap_pos(order, 4), f"4-AP created at v={v}"
    return order, stuck_at, history


if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    for strat in ("latest", "earliest", "mid"):
        order, stuck, hist = run(N, strategy=strat, verify_every=0)
        placed = len(order)
        ok = not has_monotone_kap_pos(order, 4) if placed == max(order or [0]) else None
        print(f"\n=== strategy={strat}: placed {placed} values"
              + (f", STUCK at v={stuck}" if stuck else ", never stuck"))
        if placed:
            # verify the prefix is a genuine 4-AP-free permutation of [1..placed]
            assert sorted(order) == list(range(1, placed + 1))
            assert not has_monotone_kap_pos(order, 4), "checker disagrees!"
            print(f"    verified: permutation of [1..{placed}], no monotone 4-AP")
            idx = {v: i + 1 for i, v in enumerate(order)}
            print("    position history of small values:")
            for v, d in hist:
                print(f"      after v={v}: " + ", ".join(f"pos({t})={p}" for t, p in sorted(d.items())))
            disp = max((idx[v] / v, v) for v in order)
            print(f"    max pos(v)/v = {disp[0]:.2f} at v={disp[1]}")
            print(f"    first 24 in position order: {order[:24]}")
