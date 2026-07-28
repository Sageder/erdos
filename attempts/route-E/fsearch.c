/* fsearch.c -- exact DFS for a LEGAL system with prescribed sum inside a window.
 *
 * Reads a *pre-pruned* universe (computed by universe.py, which applies the full
 * RULE A p-adic fixpoint + legality fixpoint) from a problem file:
 *
 *      line 1:  T N u v
 *      line 2:  cnt
 *      line 3:  n_1 n_2 ... n_cnt      (increasing, all in [T,N])
 *
 * and searches for W subset {n_1..n_cnt} with no isolated point (w.r.t. the
 * integers: n in W needs n-1 in W or n+1 in W) and  sum_{n in W} 1/n = u/v.
 *
 * ARITHMETIC: exact.  L = lcm(universe) * (denominator fixup), weights L/n,
 * target R0 = L*u/v, all in unsigned __int128.  Aborts if L >= 2^127.
 *
 * PRUNES
 *   (P1) 0 <= R <= tail[i]   (tail[i] = sum_{j>=i} L/n_j)
 *   (P2) Q[i] | R  where Q[i] = prod_p p^{nu_p(L) - max_{j>=i} nu_p(n_j)}.
 *        [proof: R must be a sub-sum of {L/n_j : j>=i}, and every such weight is
 *         divisible by Q[i].]
 *
 * MODES
 *   mode 0 : deterministic exhaustive DFS (include-first)
 *   mode 1 : randomised DFS with restarts (finds certificates fast);
 *            branch order randomised per node, node budget per restart.
 *
 * usage: ./fsearch probfile mode [maxsol] [budget] [seed]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef unsigned __int128 u128;

#define MAXN 200000
#define MAXC 20000

static int T0, Nhi, cnt;
static long long UNUM, VDEN;
static int el[MAXC], adj[MAXC];
static u128 L, w[MAXC], tail[MAXC + 1], Q[MAXC + 1];
static long long nodes = 0, nsol = 0, maxsol = 1;
static int chosen[MAXC], nch = 0;
static int *primes, np = 0;
static int mode = 0;
static long long budget = 0;   /* 0 = unlimited */
static unsigned long long rng_state = 88172645463325252ULL;

static unsigned long long xr(void) {
    rng_state ^= rng_state << 13; rng_state ^= rng_state >> 7; rng_state ^= rng_state << 17;
    return rng_state;
}

static void print_u128(u128 x) {
    char b[64]; int i = 63; b[i--] = 0;
    if (!x) { printf("0"); return; }
    while (x) { b[i--] = '0' + (int)(x % 10); x /= 10; }
    printf("%s", b + i + 1);
}
static int nu(long long n, int p) { int e = 0; while (n % p == 0) { n /= p; e++; } return e; }

static void build_primes(int N) {
    char *s = calloc(N + 1, 1);
    primes = malloc(sizeof(int) * (N + 1));
    for (int i = 2; i <= N; i++) if (!s[i]) { primes[np++] = i; for (long long j = (long long)i * i; j <= N; j += i) s[j] = 1; }
    free(s);
}

static void report(void) {
    nsol++;
    printf("SOL");
    for (int i = 0; i < nch; i++) printf(" %d", chosen[i]);
    printf("\n"); fflush(stdout);
}

static int hit_budget = 0;

/* returns 1 if we should stop the whole search */
static int dfs(int i, u128 R, int runlen) {
    nodes++;
    if (budget && nodes > budget) { hit_budget = 1; return 1; }
    if (i > 0 && !adj[i]) { if (runlen == 1) return 0; runlen = 0; }
    if (i == cnt) {
        if (runlen != 1 && R == 0) { report(); if (nsol >= maxsol) return 1; }
        return 0;
    }
    if (R > tail[i]) return 0;
    if (R % Q[i]) return 0;
    int order = 0;
    if (mode == 1) order = (int)(xr() & 1);
    for (int t = 0; t < 2; t++) {
        int take = (t == 0) ? (order == 0) : (order == 1);
        if (take) {
            if (w[i] <= R) { chosen[nch++] = el[i]; int s = dfs(i + 1, R - w[i], runlen + 1); nch--; if (s) return 1; }
        } else {
            if (runlen != 1) { int s = dfs(i + 1, R, 0); if (s) return 1; }
        }
    }
    return 0;
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: %s probfile mode [maxsol] [budget] [seed]\n", argv[0]); return 1; }
    FILE *f = fopen(argv[1], "r");
    if (!f) { perror("open"); return 1; }
    if (fscanf(f, "%d %d %lld %lld", &T0, &Nhi, &UNUM, &VDEN) != 4) return 1;
    if (fscanf(f, "%d", &cnt) != 1) return 1;
    for (int i = 0; i < cnt; i++) if (fscanf(f, "%d", &el[i]) != 1) return 1;
    fclose(f);
    mode = atoi(argv[2]);
    if (argc > 3) maxsol = atoll(argv[3]);
    if (argc > 4) budget = atoll(argv[4]);
    if (argc > 5) rng_state = strtoull(argv[5], NULL, 10) * 2862933555777941757ULL + 3037000493ULL;

    adj[0] = 0;
    for (int i = 1; i < cnt; i++) adj[i] = (el[i] == el[i - 1] + 1);

    build_primes(Nhi > 2 ? Nhi : 3);
    /* L */
    L = 1;
    double logL = 0.0;
    for (int pi = 0; pi < np; pi++) {
        int p = primes[pi], emax = 0;
        for (int i = 0; i < cnt; i++) { int e = nu(el[i], p); if (e > emax) emax = e; }
        int fv = nu(VDEN, p); if (fv > emax) emax = fv;
        for (int k = 0; k < emax; k++) { logL += 0.6931471805599453 * 0 + 0; }
        for (int k = 0; k < emax; k++) L *= (u128)p;
        (void)logL;
    }
    { long long vv = VDEN; for (int pi = 0; pi < np; pi++) { int p = primes[pi]; while (vv % p == 0) vv /= p; }
      if (vv != 1) { printf("target denominator has a prime factor > N: NO SOLUTION\n"); return 0; } }
    if (L >> 126) { printf("L too large for u128 -- use the CRT engine\n"); return 2; }
    printf("# T=%d N=%d target=%lld/%lld |univ|=%d L=", T0, Nhi, UNUM, VDEN, cnt); print_u128(L); printf("\n");
    for (int i = 0; i < cnt; i++) w[i] = L / (u128)el[i];
    tail[cnt] = 0;
    for (int i = cnt - 1; i >= 0; i--) tail[i] = tail[i + 1] + w[i];
    for (int i = 0; i <= cnt; i++) {
        u128 q = 1;
        for (int pi = 0; pi < np; pi++) {
            int p = primes[pi];
            int eL = 0; { u128 t = L; while (t % (u128)p == 0) { t /= (u128)p; eL++; } }
            if (!eL) continue;
            int maxe = 0;
            for (int j = i; j < cnt; j++) { int e = nu(el[j], p); if (e > maxe) maxe = e; }
            int fexp = eL - maxe;
            for (int k = 0; k < fexp; k++) q *= (u128)p;
        }
        Q[i] = q;
    }
    u128 R0 = (L / (u128)VDEN) * (u128)UNUM;
    if (R0 > tail[0]) { printf("# target exceeds total available sum: NO SOLUTION\n"); }

    if (mode == 0) {
        dfs(0, R0, 0);
        printf("# done exhaustive nodes=%lld solutions=%lld\n", nodes, nsol);
    } else {
        long long restarts = 0, totnodes = 0;
        while (nsol < maxsol) {
            nodes = 0; hit_budget = 0; nch = 0;
            int s = dfs(0, R0, 0);
            totnodes += nodes; restarts++;
            if (s && !hit_budget) break;               /* found enough */
            if (!hit_budget) {                         /* full tree explored: exhaustive */
                printf("# tree exhausted in randomised mode: solutions=%lld nodes=%lld\n", nsol, totnodes);
                break;
            }
            if (restarts % 50 == 0) { printf("# restarts=%lld totnodes=%lld\n", restarts, totnodes); fflush(stdout); }
            if (restarts > 2000000) break;
        }
        printf("# done randomised restarts=%lld totnodes=%lld solutions=%lld\n", restarts, totnodes, nsol);
    }
    return 0;
}
