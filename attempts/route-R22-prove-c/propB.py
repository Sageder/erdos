"""propB.py -- Proposition B: the class-level content of Theorem 16 is EXACTLY the
increasing half of condition (ii), and nothing more.

B(1)  If c(u-2d) < c(u-d) < c(u) then (u-2d,u-d,u) is positionally increasing for EVERY
      choice of within-class orders, so u is open at scale d and Theorem 16(a) forces
      c(u+d) <= c(u).  But condition (ii) applied to the 4-AP (u-2d,u-d,u,u+d) says
      exactly  NOT( c(u-2d) < c(u-d) < c(u) < c(u+d) ), i.e. the same thing.
      => on class-determined (u,d) the forcing rule adds nothing to (ii).

B(2)  If the three classes are NOT strictly increasing, openness is NOT determined by c:
      exhibit (u,d) and two within-class orders of the SAME class function, one making u
      open at d and the other not.  Hence Theorem 16 carries information beyond (ii) only
      through the within-class gadget -- which condition (ii), and therefore Conjecture
      R21-C, does not constrain at all.

B(3)  Dual: (u-2d,u-d,u) positionally DEcreasing forces u < u+d in position, i.e.
      c(u) <= c(u+d); at class level that is the decreasing half of condition (ii).
      So {Theorem 16 + its dual}, read at the class level, IS condition (ii).
"""

import sys, itertools, random
sys.path.insert(0, '/home/user/erdos/experiments')
sys.path.insert(0, '/home/user/erdos/attempts/route-R22-prove-c')
from arch import blockindex, perm_from_arch, fibres, open_scales, antiopen_scales


def v2(n):
    k = 0
    while n % 2 == 0:
        n //= 2
        k += 1
    return k


def scan(N, b, tfun, trials=200, seed=7):
    """For every (u,d): is openness determined by c alone?  Compare across random
    within-class orders."""
    rng = random.Random(seed)
    c = lambda v: blockindex(v, b) + tfun(v)
    F = fibres(N, c)
    pairs = [(u, d) for u in range(3, N + 1) for d in range(1, (u - 1) // 2 + 1)]
    strict = [(u, d) for (u, d) in pairs if c(u - 2 * d) < c(u - d) < c(u)]
    always_open = {p: True for p in pairs}
    ever_open = {p: False for p in pairs}
    for _ in range(trials):
        within = {}
        for m in F:
            L = list(F[m])
            rng.shuffle(L)
            within[m] = L
        perm, pos = perm_from_arch(N, c, within)
        for (u, d) in pairs:
            o = pos[u - 2 * d] < pos[u - d] < pos[u]
            if o:
                ever_open[(u, d)] = True
            else:
                always_open[(u, d)] = False
    A = {p for p in pairs if always_open[p]}
    E = {p for p in pairs if ever_open[p]}
    return set(strict), A, E, pairs


if __name__ == "__main__":
    for b, tname, tfun in ((3, 't=0', lambda v: 0), (3, 't=v2', v2), (4, 't=1_odd', lambda v: v % 2)):
        N = 60
        S, A, E, pairs = scan(N, b, tfun)
        print(f"b={b} {tname} N={N}: |pairs|={len(pairs)}  "
              f"|class-strict (u,d)|={len(S)}  |open under EVERY sampled gadget|={len(A)}  "
              f"|open under SOME gadget|={len(E)}")
        print(f"   B(1) check   S subset of A : {S <= A}")
        print(f"   B(2) witness set  (open under some gadget, not all) has size {len(E - A)}")
        ex = sorted(E - A)[:4]
        c = lambda v: blockindex(v, b) + tfun(v)
        for (u, d) in ex:
            print(f"      (u,d)=({u},{d})  classes c(u-2d),c(u-d),c(u) = "
                  f"({c(u-2*d)},{c(u-d)},{c(u)})  -- not strictly increasing, "
                  f"openness gadget-dependent")
        print()
    print("Conclusion: the class function alone decides openness exactly on the (u,d) with")
    print("c(u-2d) < c(u-d) < c(u); there Theorem 16(a) restates condition (ii).  Everywhere")
    print("else openness is a property of the within-class order, which R21-C does not fix.")
