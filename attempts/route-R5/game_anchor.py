"""game_anchor.py — the anchored-supply game for route R5, machine experiments.

The game (formalized in REPORT.md §Game).  A hypothetical 4-AP-free permutation is the
Adversary.  The Prover knows:
  (S)  anchored supply (Theorem 2, proof_3ap.md): for every value u and every modulus
       m >= 1 there EXISTS a step e, m | e, with (u, u+e, u+2e) an increasing 3-AP
       whose two later terms sit at positions after pos(u);
  (B)  4-AP blocking (L1/L2/L3 of lemmas_4apfree.md).
A Prover move: pick an already-mentioned value u and a modulus m (a multiple of the
grid unit); the Adversary answers with a step e = g*m (g >= 1 an integer of its
choice), committing to the order facts  P(u) < P(u+e) < P(u+2e)  plus the blocking
facts  P(u+3e) < P(u+2e)  and  P(u-e) > P(u)  (the latter only when u-e is known to
exist).  The Adversary must keep the accumulated finite constraint set consistent with
SOME linear order having no monotone 4-AP among mentioned values.  Prover wins if some
finite constraint set becomes inconsistent.

Experiments here:
 G1 (self-test): the OrderSAT encoding is cross-validated against literal enumeration
    of all linear orders on small windows (same SAT/UNSAT verdict and model counts).
 G2 (top-anchor gap, machine proof of the small-g exclusions): at the top of an
    increasing 3-AP, in the same modulus, the Adversary CANNOT answer g=1 or g=2
    (UNSAT), but g=3 is consistent (SAT).  This is the Chain Lemma step (L9).
 G3 (base-anchor gaps): the same question at the BASE value x of the 3-AP: which
    single answers are excluded?
 G4 (generic escape, demo of the Generic Escape Proposition): random play in which the
    Adversary always answers with a far-out generic g stays consistent — verified by
    SAT at every step over many random games.  (The Proposition PROVES this for all
    depths; the demo is a sanity check of the proof's bookkeeping.)
"""

import random
from itertools import permutations as itperms
from solver_minimal import OrderSAT, aps_within


def brute_count(offsets, base_tris, blocked=True, kmin_top=None):
    """Literal enumeration ground truth: count linear orders (as position-orders)
    satisfying: every tri in base_tris increasing; no monotone 4-AP; kmin."""
    n = len(offsets)
    tris3 = aps_within(offsets, 3)
    aps4 = aps_within(offsets, 4)
    cnt = 0
    for order in itperms(offsets):
        P = {c: t for t, c in enumerate(order)}
        okflag = all(P[a] < P[b] < P[c] for a, b, c in base_tris)
        if okflag and blocked:
            for a, b, c, d in aps4:
                if P[a] < P[b] < P[c] < P[d] or P[a] > P[b] > P[c] > P[d]:
                    okflag = False
                    break
        if okflag and kmin_top is not None:
            for a, b, c in tris3:
                if c != kmin_top and P[a] < P[b] < P[c] and P[c] < P[kmin_top]:
                    okflag = False
                    break
        cnt += okflag
    return cnt


def sat_count(offsets, base_tris, blocked=True, kmin_top=None):
    S = OrderSAT(offsets)
    if blocked:
        S.add_blocked4()
    for tri in base_tris:
        S.add_base(tri)
    if kmin_top is not None:
        S.add_kmin(kmin_top)
    # enumerate models projected onto the order variables = linear orders
    from pysat.solvers import Glucose42
    cnt = 0
    with Glucose42(bootstrap_with=S.clauses) as s:
        while s.solve():
            cnt += 1
            model = s.get_model()
            # block this total order (its projection to the o-variables)
            block = [-l for l in model if abs(l) in set(S.varmap.values())]
            s.add_clause(block)
    return cnt


def g1_selftest():
    rng = random.Random(196)
    for trial in range(40):
        n = rng.randint(4, 6)
        offs = sorted(rng.sample(range(0, 9), n))
        base = None
        # pick a base triple = any AP inside if exists, else skip base
        tris = aps_within(offs, 3)
        base_tris = [rng.choice(tris)] if tris and rng.random() < .8 else []
        kt = base_tris[0][2] if base_tris and rng.random() < .6 else None
        bc = brute_count(offs, base_tris, kmin_top=kt)
        sc = sat_count(offs, base_tris, kmin_top=kt)
        assert bc == sc, (offs, base_tris, kt, bc, sc)
    print("G1 PASS: OrderSAT encoding == literal enumeration on 40 random windows "
          "(model counts agree).")


def consistent(offsets, tris_inc, extra_lt=()):
    """SAT check: no monotone 4-AP among offsets + given increasing triples +
    extra strict order facts (a,b) meaning P_a < P_b."""
    S = OrderSAT(offsets)
    S.add_blocked4()
    for tri in tris_inc:
        S.add_base(tri)
    for a, b in extra_lt:
        S.clauses.append([S.var(a, b)])
    return S.solve()


def g2_topanchor():
    print("G2: top-anchor responses at the top value x+2d, modulus d "
          "(offsets in units of d):")
    for g in range(1, 7):
        offs = sorted(set([0, 1, 2, 3] + [2 + g, 2 + 2 * g, 2 + 3 * g]))
        # facts: base (0,1,2) increasing; response (2, 2+g, 2+2g) increasing;
        # blocking of both is implied by blocked4 on the window.
        sat = consistent(offs, [(0, 1, 2), (2, 2 + g, 2 + 2 * g)])
        print(f"    g={g}: {'consistent (SAT)' if sat else 'EXCLUDED (UNSAT)'}")


def g3_baseanchor():
    print("G3: base-anchor responses at the base value x, modulus d:")
    for g in range(1, 7):
        offs = sorted(set([0, 1, 2, 3] + [g, 2 * g, 3 * g]))
        sat = consistent(offs, [(0, 1, 2), (0, g, 2 * g)])
        print(f"    g={g}: {'consistent (SAT)' if sat else 'EXCLUDED (UNSAT)'}")
    print("G3b: base-anchor at x, modulus 2d (responses e=2gd):")
    for g in range(1, 5):
        offs = sorted(set([0, 1, 2, 3] + [2 * g, 4 * g, 6 * g]))
        sat = consistent(offs, [(0, 1, 2), (0, 2 * g, 4 * g)])
        print(f"    g={g} (e={2*g}d): {'consistent' if sat else 'EXCLUDED'}")


def g4_generic_demo():
    rng = random.Random(4)
    games = 0
    for trial in range(200):
        offs = [0, 1, 2, 3]
        tris = [(0, 1, 2)]
        ok = True
        for rounds in range(6):
            # Prover: anchor at a random known offset
            u = rng.choice(offs)
            span = max(offs) - min(offs)
            g = span * 2 + 1 + rng.randint(1, 5)     # generic large step
            new = [u + g, u + 2 * g, u + 3 * g]
            offs = sorted(set(offs + new))
            tris = tris + [(u, u + g, u + 2 * g)]
            if not consistent(offs, tris):
                ok = False
                break
        assert ok, ("generic escape failed", offs, tris)
        games += 1
    print(f"G4 PASS: {games} random 6-round games with generic Adversary answers all "
          "stayed consistent (as the Generic Escape Proposition predicts).")


if __name__ == "__main__":
    g1_selftest()
    g2_topanchor()
    g3_baseanchor()
    g4_generic_demo()
