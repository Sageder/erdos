"""reform.py -- route R22-C, the reformulation results.

Proposition C  (no fibre hypothesis at all).  Let c = j + t, j(v) = floor(log_b v),
t >= 0, finite fibres, classes emitted in increasing index order with ARBITRARY
within-class orders.  Let P = {p_n = r + q n : n >= 1} be an infinite AP.  Then

        pos_P(n)  <=  b^{ t(p_n) + 1 } * p_n / q  =  b^{ t(p_n)+1 } * ( n + r/q ).

In particular if t is BOUNDED on P by T_P, the AP-restriction has linear displacement
with constant b^{T_P+1}.  (Proof: p_m < p_n in position order => c(p_m) <= c(p_n)
=> j(p_m) <= c(p_n) => p_m < b^{j(p_n)+t(p_n)+1} <= b^{t(p_n)+1} p_n.)

Corollary C1 (global).  If t <= T on all of N, pos(v) <= b^{T+1} v for all v.

Consequence for the programme: for a geometric class architecture, design principle D1
("unbounded relative displacement along EVERY infinite AP") requires t to be UNBOUNDED
along every infinite AP.  Hence the load-bearing conjecture is

   R21-C'  :  condition (ii) forces t to be BOUNDED on some infinite AP,

which is strictly weaker than R21-C ("t CONSTANT on some infinite AP") and weaker than
"some AP is tame", and has exactly the same payoff.

Theorem D (fibre-design counting).  If |F_m| >= c1 * b^m for all m >= m0, then with
r := 2 + floor(log_b(2/c1)) the sublevel set L = {v : t(v) < r} satisfies
   |L  and  [b^{m-r+1}, b^{m+1})| >= (c1/2) b^m   for every m >= m0.
(So the strict geometric fibre design forces a bounded-delay set of positive density in
every b-adic window.)

Theorem E (the block-index-determined family is CLOSED).  If t(v) = g(j(v)) depends only
on the block index, then: (a) condition (ii) holds automatically for every g when b >= 3;
(b) if additionally every fibre is nonempty with |F_m| >= c1 b^m (m >= m0), then g is
BOUNDED, so by Corollary C1 the architecture has linear displacement.  Proof of (b):
write G(k) = k + g(k) >= k, psi(m) = max G^{-1}(m); the size hypothesis forces
psi(m) >= m - K with K = 1 + floor(log_b(1/c1)); psi is injective and psi(m) <= m, so
|[0,M] \\ im psi| <= m0 for every M, i.e. im psi omits at most m0 indices; on im psi,
g(psi(m)) = m - psi(m) <= K; hence g <= max(K, finitely many exceptions).
"""

import sys
sys.path.insert(0, '/home/user/erdos/experiments')
sys.path.insert(0, '/home/user/erdos/attempts/route-R22-prove-c')
from arch import blockindex, perm_from_arch, fibres, class_seq_violations, ap4_violations
from forcing_class import v2, vdc_key, ORDERS, build


def check_propC(N, b, tfun, oname, Qmax=6, show=False):
    """Verify the EXACT form of Proposition C:

        pos_P(n)  <=  #{ m >= 1 : p_m < b^{ c(p_n) + 1 } }            (exact)
                  <=  b^{t(p_n)+1} * (n - 1)  +  (b^{t(p_n)+1} - 1) * p_1 / q  +  1

    for every infinite AP P (here truncated to [1..N]).  All arithmetic is exact
    integer arithmetic; the second form is the linear-displacement statement.
    """
    c, within, perm, pos = build(N, b, tfun, ORDERS[oname])
    worst_ratio = 0.0
    bad_exact = bad_lin = tested = 0
    ex = []
    for q in range(1, Qmax + 1):
        for r in range(0, q):
            P = sorted(v for v in range(1, N + 1) if v % q == r % q)
            if len(P) < 8:
                continue
            p1 = P[0]
            order = sorted(P, key=lambda v: pos[v])
            rank = {v: i + 1 for i, v in enumerate(order)}
            for n, pn in enumerate(P, start=1):
                tested += 1
                lhs = rank[pn]
                B = b ** (c(pn) + 1)                       # exact integer
                exact = len([m for m in range(1, len(P) + 1) if p1 + (m - 1) * q < B])
                if lhs > exact:
                    bad_exact += 1
                    if show and len(ex) < 5:
                        ex.append(('exact', q, r, n, pn, lhs, exact))
                lin = b ** (tfun(pn) + 1) * (n - 1) + (b ** (tfun(pn) + 1) - 1) * p1 / q + 1
                if lhs > lin + 1e-9:
                    bad_lin += 1
                    if show and len(ex) < 5:
                        ex.append(('lin', q, r, n, pn, lhs, lin))
                worst_ratio = max(worst_ratio, lhs / n)
    return tested, bad_exact, bad_lin, round(worst_ratio, 3), ex


def check_corC1(N, b, tfun, oname):
    c, within, perm, pos = build(N, b, tfun, ORDERS[oname])
    T = max(tfun(v) for v in range(1, N + 1))
    bad = sum(1 for v in range(1, N + 1) if pos[v] > b ** (T + 1) * v)
    worst = max(pos[v] / v for v in range(1, N + 1))
    return T, bad, round(worst, 3), b ** (T + 1)


def theoremE_family(b, Kmax, gens):
    """For t = g(j): report whether all fibres are nonempty & geometric, and whether g
    is bounded.  Exhibits the equivalence claimed in Theorem E."""
    out = []
    for name, g in gens:
        G = [k + g(k) for k in range(Kmax)]
        # fibre F_m gets block k iff G(k) == m; |F_m| ~ b^{max preimage}
        pre = {}
        for k, m in enumerate(G):
            pre.setdefault(m, []).append(k)
        ms = [m for m in range(max(G) + 1)]
        empty = [m for m in range(1, min(max(G), Kmax)) if m not in pre]
        ratios = []
        for m in range(1, min(max(G), Kmax)):
            if m in pre:
                ratios.append(max(pre[m]) - m)   # log_b(|F_m| / b^m) up to O(1)
        out.append((name, max(g(k) for k in range(Kmax)),
                    len(empty), (min(ratios) if ratios else None)))
    return out


if __name__ == "__main__":
    print("=" * 100)
    print("PROPOSITION C  (AP-restricted displacement bound; NO fibre hypothesis)")
    print("=" * 100)
    print(f"{'b':>2} {'t':>7} {'order':>11} {'N':>5} {'tested':>8} {'bad(exact)':>11} "
          f"{'bad(linear)':>12} {'max pos_P(n)/n':>15}")
    for b in (3, 4, 5):
        for tname, tfun in (('0', lambda v: 0), ('v2', v2), ('1_odd', lambda v: v % 2),
                            ('v2+1_od', lambda v: v2(v) + v % 2)):
            for oname in ('decreasing', 'vdc', 'increasing'):
                tested, be, bl, wr, ex = check_propC(400, b, tfun, oname, show=True)
                print(f"{b:>2} {tname:>7} {oname:>11} {400:>5} {tested:>8} {be:>11} {bl:>12} {wr:>15}")
                if ex:
                    print("      examples:", ex[:3])
    print()
    print("=" * 100)
    print("COROLLARY C1  (global linear displacement for bounded delay: pos(v) <= b^{T+1} v)")
    print("=" * 100)
    print(f"{'b':>2} {'t':>9} {'order':>11} {'N':>5} {'T':>3} {'violations':>11} "
          f"{'max pos/v':>10} {'bound b^(T+1)':>14}")
    for b in (3, 4, 5):
        for tname, tfun in (('0', lambda v: 0), ('1_odd', lambda v: v % 2),
                            ('v2cap3', lambda v: min(v2(v), 3))):
            for oname in ('decreasing', 'vdc'):
                T, bad, worst, bd = check_corC1(600, b, tfun, oname)
                print(f"{b:>2} {tname:>9} {oname:>11} {600:>5} {T:>3} {bad:>11} {worst:>10} {bd:>14}")
    print()
    print("=" * 100)
    print("THEOREM E  (t = g(block index)):  strict geometric fibre design <=> g bounded")
    print("=" * 100)
    print(f"{'g':>18} {'max g on [0,K)':>15} {'#empty fibres':>14} {'min(maxpre(m)-m)':>18}")
    gens = [
        ('g == 0', lambda k: 0),
        ('g == 3', lambda k: 3),
        ('g = k  (c=2j)', lambda k: k),
        ('g = k//2', lambda k: k // 2),
        ('g = isqrt(k)', lambda k: int(k ** 0.5)),
        ('g = k mod 2', lambda k: k % 2),
        ('g = 5 - min(k,5)', lambda k: 5 - min(k, 5)),
        ('holes 0,4,20,100', lambda k: {0: 4, 4: 16, 20: 80}.get(k, 0)),
    ]
    for name, mx, nempty, minr in theoremE_family(3, 40, gens):
        print(f"{name:>18} {mx:>15} {nempty:>14} {str(minr):>18}")
    print()
    print("Reading: 'min(maxpre(m)-m)' is the worst log_b-deficiency of a fibre; a strict")
    print("geometric design needs #empty fibres = 0 AND that quantity bounded below.  Every")
    print("unbounded g in the table fails one of the two -- as Theorem E says it must.")
