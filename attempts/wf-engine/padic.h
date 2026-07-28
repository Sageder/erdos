/* padic.h -- DYNAMIC Rule-(P) lookahead: per-prime residue reachability.
 *
 * Rule (P).  If sum_{n in W} 1/n = u/v and E >= nu_p(n) for all n in W, then
 *      sum_{n in W, p | n} p^E/n  ==  p^E * u/v      (mod p^E),
 * every term with p not dividing n being divisible by p^E.  In GADGET mode the
 * value is only required to be a/D with a free, and p^E*a/D runs over all
 * multiples of p^{E-nu_p(D)}, so the congruence becomes
 *      sum_{n in W, p | n} p^E/n  ==  0             (mod p^{E-nu_p(D)}).
 *
 * The universe fixpoint (prune.py) uses this statically.  Here it is used
 * DYNAMICALLY, which is far stronger: taking E = max nu_p over the universe,
 * every modulus is p^E <= N, so for each tracked prime we can precompute the
 * full backward reachability table
 *      reach[k][r] = 1  iff  r is a subset sum, mod M_p, of the weights of the
 *                    multiples of p sitting at universe positions >= k
 * and test, at every DFS node, whether the residue still needed is reachable
 * from the multiples of p that are still ahead.  A failure prunes the whole
 * subtree.  Cost: only the primes dividing el[i] are touched at index i
 * (all other weights are 0), i.e. ~3 table lookups per node.
 *
 * Memory: sum_p (#multiples+1) * M_p bytes ~ N * pi(N), a few MB for N ~ 5000.
 *
 * All of this only ever PRUNES; the exact value test is done by the caller's
 * multiword arithmetic, so this module cannot introduce false solutions.
 */
#ifndef PADIC_H
#define PADIC_H

#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define PA_MAXP 4096

static int PA_np = 0;
static int PA_pr[PA_MAXP];
static long long PA_M[PA_MAXP];
static long long PA_tg[PA_MAXP];
static long long PA_s[PA_MAXP];
static int *PA_wi[PA_MAXP];        /* weight of universe index i (0 unless p|el[i]) */
static int *PA_ki[PA_MAXP];        /* # multiples of p at indices < i             */
static unsigned char *PA_re[PA_MAXP];
static int *PA_divc, **PA_divl;    /* tracked-prime slots dividing el[i]          */
static int PA_cnt;

static long long pa_inv(long long a, long long m)
{
    long long r0 = ((a % m) + m) % m, r1 = m, s0 = 1, s1 = 0;
    while (r1) {
        long long q = r0 / r1, t;
        t = r0 - q * r1; r0 = r1; r1 = t;
        t = s0 - q * s1; s0 = s1; s1 = t;
    }
    long long r = s0 % m;
    return r < 0 ? r + m : r;
}
static int pa_nu(long long n, int p) { int e = 0; while (n % p == 0) { n /= p; e++; } return e; }

/* gadget = 0: exact target u/v.  gadget = 1: value a/v with a free (v = D). */
static int padic_init(int cnt, const int *el, int Nhi, long long u, long long v, int gadget)
{
    PA_cnt = cnt;
    char *sv = calloc((size_t)Nhi + 2, 1);
    for (int i = 2; i <= Nhi; i++)
        if (!sv[i]) for (long long j = (long long)i * i; j <= Nhi; j += i) sv[j] = 1;
    PA_divc = calloc((size_t)cnt + 1, sizeof(int));
    PA_divl = calloc((size_t)cnt + 1, sizeof(int *));
    int *tmpslot = malloc(sizeof(int) * 64);
    int **acc = calloc((size_t)cnt + 1, sizeof(int *));
    for (int i = 0; i <= cnt; i++) acc[i] = calloc(64, sizeof(int));
    (void)tmpslot;

    for (int p = 2; p <= Nhi; p++) {
        if (sv[p]) continue;
        int E = 0, c = 0;
        for (int i = 0; i < cnt; i++) { int e = pa_nu(el[i], p); if (e > E) E = e; if (e) c++; }
        if (E == 0) continue;
        int f = pa_nu(v, p);
        long long M;
        if (gadget) {
            int Ep = E - f;
            if (Ep <= 0) continue;
            M = 1; for (int t = 0; t < Ep; t++) M *= p;
        } else {
            if (f > E) { free(sv); return -1; }        /* denominator unreachable */
            M = 1; for (int t = 0; t < E; t++) M *= p;
        }
        if (M == 1) continue;
        if (PA_np >= PA_MAXP) { fprintf(stderr, "too many tracked primes\n"); exit(1); }
        int j = PA_np++;
        PA_pr[j] = p; PA_M[j] = M; PA_s[j] = 0;
        PA_wi[j] = calloc((size_t)cnt, sizeof(int));
        PA_ki[j] = calloc((size_t)cnt + 1, sizeof(int));
        int *pos = malloc(sizeof(int) * (c + 1));
        int nc = 0;
        for (int i = 0; i < cnt; i++) {
            PA_ki[j][i] = nc;
            int e = pa_nu(el[i], p);
            if (e) {
                long long m = el[i]; for (int t = 0; t < e; t++) m /= p;
                long long pe = 1; for (int t = 0; t < E - e; t++) pe = pe * p % M;
                PA_wi[j][i] = (int)(pe % M * pa_inv(m, M) % M);
                pos[nc++] = i;
                if (PA_divc[i] < 64) acc[i][PA_divc[i]++] = j;
            }
        }
        PA_ki[j][cnt] = nc;
        /* target residue */
        if (gadget) PA_tg[j] = 0;
        else {
            long long vv = v; for (int t = 0; t < f; t++) vv /= p;
            long long pe = 1; for (int t = 0; t < E - f; t++) pe = pe * p % M;
            PA_tg[j] = pe % M * pa_inv(vv, M) % M * (u % M) % M;
        }
        /* backward reachability over positions nc..0 */
        PA_re[j] = calloc((size_t)(nc + 1) * M, 1);
        unsigned char *R = PA_re[j];
        R[(size_t)nc * M + 0] = 1;
        for (int k = nc - 1; k >= 0; k--) {
            long long x = PA_wi[j][pos[k]];
            unsigned char *cur = R + (size_t)k * M, *nx = R + (size_t)(k + 1) * M;
            for (long long r = 0; r < M; r++)
                if (nx[r]) { cur[r] = 1; cur[(r + x) % M] = 1; }
        }
        free(pos);
    }
    for (int i = 0; i <= cnt; i++) {
        PA_divl[i] = acc[i];
    }
    free(acc); free(sv);
    return 0;
}

static inline void padic_reset(void) { for (int j = 0; j < PA_np; j++) PA_s[j] = 0; }

/* call when index i is TAKEN */
static inline void padic_take(int i)
{
    for (int t = 0; t < PA_divc[i]; t++) {
        int j = PA_divl[i][t];
        PA_s[j] += PA_wi[j][i];
        if (PA_s[j] >= PA_M[j]) PA_s[j] -= PA_M[j];
    }
}
static inline void padic_untake(int i)
{
    for (int t = 0; t < PA_divc[i]; t++) {
        int j = PA_divl[i][t];
        PA_s[j] -= PA_wi[j][i];
        if (PA_s[j] < 0) PA_s[j] += PA_M[j];
    }
}
/* prune test on entering index i (0 <= i <= cnt): only primes touched at i-1
 * can have changed, so only those are re-tested. */
static inline int padic_ok(int i)
{
    if (i == 0) return 1;
    int q = i - 1;
    for (int t = 0; t < PA_divc[q]; t++) {
        int j = PA_divl[q][t];
        long long need = PA_tg[j] - PA_s[j];
        if (need < 0) need += PA_M[j];
        if (!PA_re[j][(size_t)PA_ki[j][i] * PA_M[j] + need]) return 0;
    }
    return 1;
}

#endif /* PADIC_H */
