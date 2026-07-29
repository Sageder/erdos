"""conflict.py — a DIRECT combinatorial criterion for unrealizability of a class architecture.

Setting: class function c with finite fibres, classes emitted in increasing index order,
within-class orders free. Positions follow (class, within-class rank).

Analysis. Take a 4-AP t1<t2<t3<t4 with class sequence (c1,c2,c3,c4).
 * If the class sequence is NON-monotone (some strict rise and some strict fall), the
   positions are automatically non-monotone: no constraint.
 * If it is STRICTLY monotone, the positions are monotone whatever the within-class orders
   do: the architecture is dead there. That is exactly condition (ii).
 * If it is WEAKLY monotone with ties, the tied terms are ordered inside their class, and
   avoiding a monotone position sequence imposes a constraint on that order:
       weakly INCREASING with a tie at (t_i, t_{i+1}) :  demand pos(t_i) > pos(t_{i+1})
       weakly DECREASING with a tie at (t_i, t_{i+1}) :  demand pos(t_i) < pos(t_{i+1})
   (In the increasing orientation the AP is bad exactly when every step is non-decreasing in
   position, so the tie must be inverted; dually for decreasing.)

CRITERION. If some pair u < w with c(u) = c(w) is the tied adjacent pair of BOTH a weakly
increasing and a weakly decreasing 4-AP, the two demands are opposite and NO within-class
order can work: the architecture is unrealizable, regardless of every other choice.

This is a direct check — no solver — and when it fires it is a proof of death for that class
function. It also explains mechanically what Proposition 41's UNSAT results were detecting.

Usage: conflicts(c, N) returns the list of conflicting pairs with their witnessing APs.
"""

import sys
sys.path.insert(0, '/home/user/erdos/experiments')


def demands(c, N):
    """Collect within-class order demands from all 4-APs.
    Returns dict: (u,w) with u<w and c(u)==c(w) -> set of 'inv' (pos(u)>pos(w))
    and/or 'nat' (pos(u)<pos(w)), with a witnessing AP for each."""
    dem = {}
    for d in range(1, (N - 1) // 3 + 1):
        for x in range(1, N - 3 * d + 1):
            t = [x + i * d for i in range(4)]
            cs = [c[v] for v in t]
            ties = [i for i in range(3) if cs[i] == cs[i + 1]]
            if not ties:
                continue
            weak_inc = all(cs[i] <= cs[i + 1] for i in range(3))
            weak_dec = all(cs[i] >= cs[i + 1] for i in range(3))
            if not (weak_inc or weak_dec):
                continue
            if len(ties) != 1:
                # With two or more ties the requirement is a DISJUNCTION ("at least one tie
                # inverted"), not a conjunction — such APs give no unconditional demand.
                # Only single-tie APs force their pair. (This corrects the first version,
                # which treated every tie as individually demanded and therefore reported
                # spurious conflicts for every family, including ones that certainly admit
                # 4-AP-free realizations.)
                continue
            for i in ties:
                u, w = t[i], t[i + 1]
                key = (u, w)
                dem.setdefault(key, {})
                if weak_inc:
                    dem[key].setdefault('inv', (x, d))   # need pos(u) > pos(w)
                if weak_dec:
                    dem[key].setdefault('nat', (x, d))   # need pos(u) < pos(w)
    return dem


def conflicts(c, N):
    out = []
    for key, ds in demands(c, N).items():
        if 'inv' in ds and 'nat' in ds:
            out.append((key, ds['inv'], ds['nat']))
    return out


if __name__ == "__main__":
    from tension import blk
    import random
    b = 3
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 600

    def report(name, tfun):
        c = {v: blk(v, b) + tfun(v) for v in range(1, N + 1)}
        # first: does condition (ii) already fail?
        bad_ii = None
        for d in range(1, (N - 1) // 3 + 1):
            for x in range(1, N - 3 * d + 1):
                cs = [c[x + i * d] for i in range(4)]
                if cs[0] < cs[1] < cs[2] < cs[3] or cs[0] > cs[1] > cs[2] > cs[3]:
                    bad_ii = (x, d, cs); break
            if bad_ii: break
        dem = demands(c, N)
        con = conflicts(c, N)
        print(f"{name:26s}: (ii) {'FAILS at ' + str(bad_ii[:2]) if bad_ii else 'holds'}; "
              f"tied-pair demands = {len(dem)}; CONFLICTS = {len(con)}"
              + (f"  e.g. pair {con[0][0]} forced both ways by APs {con[0][1]} and {con[0][2]}"
                 if con else ""))

    report("t = 0", lambda v: 0)
    report("t = v2(v)", lambda v: (v & -v).bit_length() - 1)
    report("t = 1_odd", lambda v: v % 2)
    report("t = v mod 3", lambda v: v % 3)
    rng = random.Random(196)
    rnd = {v: rng.randint(0, 1) for v in range(1, N + 1)}
    report("t = random 0/1", lambda v: rnd[v])
    rnd2 = {v: rng.randint(0, 3) for v in range(1, N + 1)}
    report("t = random 0..3", lambda v: rnd2[v])
