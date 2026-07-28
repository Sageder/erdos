#!/usr/bin/env python3
"""
heuristic.py -- an honest local-global (circle-method style) heuristic for

    E(N) := # { U subset [2,N] : U legal (no isolated point), sum_{n in U} 1/n = 1 }.

THIS IS A HEURISTIC, NOT A PROOF.  The only unproved ingredient is the
independence of the p-adic conditions for different p, and the assumption that
inside the (very narrow) bulk window of the tilted measure the only integer
value of the sum is 1.  Everything else is an identity.

EXACT IDENTITY.  For any real t,
    E(N) = e^{t} * Z(t) * P_t( S(U) = 1 ),
where  Z(t) = sum over legal U of e^{-t S(U)},  S(U)=sum_{n in U}1/n, and P_t is
the tilted probability measure P_t(U) = e^{-t S(U)}/Z(t).
Choose t = t* so that E_{t*}[S] = 1.  Under P_{t*} the sum S concentrates at 1
with standard deviation sigma = O(N^{-1/2}); the only integer in the bulk is 1,
so
    P_{t*}(S = 1)  ~  P_{t*}( S in Z )  =  P_{t*}( nu_p(S) >= 0 for all p ).
The heuristic is to factor this as prod_p delta_p with
    delta_p := P_{t*}( nu_p(S) >= 0 ).
Each delta_p is computed EXACTLY (up to floating point) by a transfer-matrix DP,
because, with a = floor(log_p N) and n = p^{j_n} m_n,
    nu_p(S) >= 0  <=>  sum_{n in U} p^{a-j_n} * (m_n^{-1} mod p^a)  ==  0  (mod p^a),
a linear congruence in the indicator vector of U.  The DP state is
(legality-automaton state, residue mod p^a).

Legality automaton (positions scanned n = 2,3,...,N):
   s0 : previous position not chosen
   s1 : previous position chosen, current run has length 1  (must extend)
   s2 : previous position chosen, current run has length >= 2
   from s0: skip->s0, take->s1 ;  from s1: skip->DEAD, take->s2 ;
   from s2: skip->s0, take->s2 .  Accepting: s0, s2.

VALIDATION: with `--all` the legality automaton is replaced by the trivial
1-state automaton, so the same code predicts the number of ALL U subset [2,N]
with sum 1/n = 1, whose true values are known by brute force
(N=12:2, 15:5, 18:10, 20:21, 24:40, ...).  Agreement there is the test of the
whole machinery.
"""
import sys
import numpy as np

np.seterr(all='ignore')


def primes_upto(N):
    s = bytearray([1]) * (N + 1)
    s[0:2] = b"\x00\x00"
    i = 2
    while i * i <= N:
        if s[i]:
            s[i * i::i] = bytearray(len(s[i * i::i]))
        i += 1
    return [i for i in range(2, N + 1) if s[i]]


class Model:
    """legal=True -> no-isolated-point automaton; legal=False -> all subsets."""

    def __init__(self, N, legal=True, universe=None):
        self.N = N
        self.legal = legal
        self.ns = list(range(2, N + 1)) if universe is None else sorted(universe)
        self.nstate = 3 if legal else 1

    # ---------- log Z and inclusion marginals under the tilt ----------
    def forward_backward(self, t):
        N, ns = self.N, self.ns
        w = [np.exp(-t / n) for n in ns]
        if self.legal:
            # forward
            F = [np.array([1.0, 0.0, 0.0])]
            logscale = 0.0
            scales = [0.0]
            for i, n in enumerate(ns):
                f = F[-1]
                # gap handling: if ns is not contiguous, a non-neighbour breaks runs.
                nxt = np.zeros(3)
                nxt[0] += f[0] + f[2]           # skip
                nxt[1] += f[0] * w[i]           # take, start run
                nxt[2] += (f[1] + f[2]) * w[i]  # take, extend run
                s = nxt.sum()
                if s > 0:
                    nxt /= s
                logscale += np.log(s) if s > 0 else -np.inf
                F.append(nxt)
                scales.append(logscale)
                # if universe has a gap between ns[i] and ns[i+1] > 1, a run cannot
                # continue across the gap: state s1 must die, s2 -> s0.
                if i + 1 < len(ns) and ns[i + 1] != n + 1:
                    g = F[-1].copy()
                    g[0] = g[0] + g[2]
                    g[1] = 0.0
                    g[2] = 0.0
                    s = g.sum()
                    if s > 0:
                        g /= s
                    logscale += np.log(s) if s > 0 else -np.inf
                    F[-1] = g
                    scales[-1] = logscale
            acc = F[-1][0] + F[-1][2]
            logZ = scales[-1] + np.log(acc)
            # backward
            B = [None] * (len(ns) + 1)
            b = np.array([1.0, 0.0, 1.0])
            B[len(ns)] = b.copy()
            for i in range(len(ns) - 1, -1, -1):
                n = ns[i]
                bb = B[i + 1].copy()
                if i + 1 < len(ns) and ns[i + 1] != n + 1:
                    bb = np.array([bb[0], 0.0, bb[0]])
                nb = np.zeros(3)
                nb[0] = bb[0] + w[i] * bb[1]
                nb[1] = w[i] * bb[2]
                nb[2] = bb[0] + w[i] * bb[2]
                s = nb.sum()
                if s > 0:
                    nb /= s
                B[i] = nb
            # marginals q_n = P_t(n in U)
            q = []
            for i, n in enumerate(ns):
                f = F[i]
                bb = B[i + 1]
                if i + 1 < len(ns) and ns[i + 1] != n + 1:
                    bb = np.array([bb[0], 0.0, bb[0]])
                num = f[0] * w[i] * bb[1] + (f[1] + f[2]) * w[i] * bb[2]
                den = num + (f[0] + f[2]) * bb[0]
                q.append(num / den if den > 0 else 0.0)
            return logZ, np.array(q)
        else:
            logZ = float(np.sum(np.log1p(np.array(w))))
            q = np.array([wi / (1.0 + wi) for wi in w])
            return logZ, q

    def mean_S(self, t):
        _, q = self.forward_backward(t)
        return float(np.sum(q / np.array(self.ns, dtype=float)))

    def find_tstar(self, target=1.0):
        lo, hi = -50.0, 1.0
        # mean_S is decreasing in t
        while self.mean_S(hi) > target:
            hi *= 2
            if hi > 1e7:
                break
        while self.mean_S(lo) < target:
            lo *= 2
            if lo < -1e7:
                break
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            if self.mean_S(mid) > target:
                lo = mid
            else:
                hi = mid
        return 0.5 * (lo + hi)

    # ---------- delta_p ----------
    def delta_p(self, p, t):
        N, ns = self.N, self.ns
        a = 0
        while p ** (a + 1) <= N:
            a += 1
        if a == 0:
            return 1.0
        M = p ** a
        c = []
        for n in ns:
            j = 0
            m = n
            while m % p == 0:
                m //= p
                j += 1
            if j > a:                     # can't happen for n <= N
                return None
            c.append((p ** (a - j) * pow(m, -1, M)) % M)
        w = [np.exp(-t / n) for n in ns]
        if self.legal:
            D = np.zeros((3, M))
            D[0, 0] = 1.0
            for i, n in enumerate(ns):
                nxt = np.zeros((3, M))
                nxt[0] = D[0] + D[2]
                nxt[1] = np.roll(D[0], c[i]) * w[i]
                nxt[2] = (np.roll(D[1], c[i]) + np.roll(D[2], c[i])) * w[i]
                s = nxt.sum()
                if s > 0:
                    nxt /= s
                D = nxt
                if i + 1 < len(ns) and ns[i + 1] != n + 1:
                    D[0] = D[0] + D[2]
                    D[1] = 0.0
                    D[2] = 0.0
                    s = D.sum()
                    if s > 0:
                        D /= s
            acc = D[0] + D[2]
        else:
            D = np.zeros(M)
            D[0] = 1.0
            for i, n in enumerate(ns):
                D = D + np.roll(D, c[i]) * w[i]
                s = D.sum()
                if s > 0:
                    D /= s
            acc = D
        tot = acc.sum()
        return float(acc[0] / tot) if tot > 0 else 0.0


def run(N, legal=True, verbose=False, universe=None):
    m = Model(N, legal, universe)
    t = m.find_tstar(1.0)
    logZ, q = m.forward_backward(t)
    mean = float(np.sum(q / np.array(m.ns, dtype=float)))
    var = float(np.sum(q * (1 - q) / np.array(m.ns, dtype=float) ** 2))
    logE = t + logZ
    terms = []
    for p in primes_upto(N):
        d = m.delta_p(p, t)
        if d is None or d <= 0:
            terms.append((p, -np.inf))
            logE = -np.inf
            break
        terms.append((p, float(np.log(d))))
        logE += np.log(d)
    if verbose:
        print(f"  t*={t:.6f}  logZ={logZ:.6f}  mean_S={mean:.10f} sigma={var**0.5:.5f}")
        worst = sorted(terms, key=lambda z: z[1])[:12]
        print("  smallest log delta_p:", [(p, round(v, 3)) for p, v in worst])
        print("  sum_p log delta_p =", round(sum(v for _, v in terms), 4))
    return logE, t, logZ, terms


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "validate"
    if mode == "validate":
        truth = {12: 2, 15: 5, 18: 10, 20: 21, 24: 40}
        print("VALIDATION: all subsets of [2,N] with sum 1/n = 1")
        print(" N   true count   heuristic")
        for N in [12, 15, 18, 20, 24, 30, 40, 50, 60, 80]:
            logE, t, logZ, terms = run(N, legal=False)
            print(f"{N:3d}  {truth.get(N,'?'):>10}   {np.exp(logE):12.4g}   (t*={t:.3f})")
    elif mode == "pruned":
        # same heuristic but conditioned on the PROVED necessary condition
        # U subset A_N (the RULE A+B fixpoint).  This removes the deterministic
        # part of the p-adic constraints from the "random" model, so the
        # independence assumption is applied only to what is left.
        sys.path.insert(0, '/home/user/erdos/attempts/route-C')
        from prune import prune
        lo, hi, step = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
        print("HEURISTIC for LEGAL sets on the PRUNED universe A_N")
        print("    N   |A_N|   t*      log10 E(N)        E(N)")
        for N in range(lo, hi + 1, step):
            A = prune(N, True)
            if not A:
                print(f"{N:5d}  {0:5d}   ---      -inf            0   (universe empty)")
                continue
            try:
                logE, t, logZ, terms = run(N, legal=True, universe=A)
            except Exception as ex:
                print(f"{N:5d}  ERROR {ex}")
                continue
            print(f"{N:5d}  {len(A):5d}  {t:8.3f}  {logE/np.log(10):10.3f}  "
                  f"{np.exp(logE):12.4g}", flush=True)
    else:
        lo, hi, step = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
        print("HEURISTIC for LEGAL sets:  N, log10 E(N), E(N)")
        for N in range(lo, hi + 1, step):
            logE, t, logZ, terms = run(N, legal=True, verbose=(N % (5 * step) == 0))
            print(f"{N:5d}  log10E={logE/np.log(10):10.3f}   E={np.exp(logE):12.4g}"
                  f"   t*={t:9.3f}", flush=True)
