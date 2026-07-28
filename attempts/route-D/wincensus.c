/* wincensus.c -- route-D, Q3.
 *
 * Enumerate EVERY U subset [T,X] with no isolated point and report every value
 *      rho = sum_{n in U} 1/n
 * whose denominator (in lowest terms) is <= DCAP.
 *
 * Exact integer arithmetic: L = lcm(T..X) (unsigned __int128), element n has
 * weight w[n] = L/n, a subset has integer sum S and value S/L; the reduced
 * denominator is L/gcd(S,L).
 *
 * PRUNE (p-adic, rigorous).  At position pos with partial sum S, every future
 * contribution F satisfies  nu_p(F) >= nu_p(L) - emax[p][pos]  where
 * emax[p][pos] = max nu_p(n) over n in [pos,X].  Hence if
 *      nu_p(S) < nu_p(L) - emax[p][pos]
 * then nu_p(S+F) = nu_p(S) and the final denominator contains
 * p^(nu_p(L)-nu_p(S)); that is allowed only if p^(nu_p(L)-nu_p(S)) <= DCAP.
 * Collecting over p: with
 *      Q[pos] = prod_p p^{ max(0, nu_p(L) - max(emax[p][pos], floor(log_p DCAP))) }
 * a node can be pruned unless  Q[pos] | S.
 *
 * usage: ./wincensus T X DCAP [maxprint]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef unsigned __int128 u128;

static int T, X, MAXPR = 200;
static u128 DCAP;
static u128 L, w[256], Q[258];
static long long nodes = 0, nfound = 0, nleaf = 0;
static int runs_a[128], runs_b[128], nruns = 0;
static int primes[256], np = 0;

static void print_u128(u128 x) {
    char buf[64]; int i = 63; buf[i--] = 0;
    if (!x) { printf("0"); return; }
    while (x) { buf[i--] = (char)('0' + (int)(x % 10)); x /= 10; }
    printf("%s", buf + i + 1);
}

static u128 gcd128(u128 a, u128 b) { while (b) { u128 t = a % b; a = b; b = t; } return a; }

static int nu(long long n, int p) { int e = 0; while (n % p == 0) { n /= p; e++; } return e; }

static void build(void) {
    for (int i = 2; i <= X; i++) {
        int isp = 1;
        for (int j = 2; j * j <= i; j++) if (i % j == 0) { isp = 0; break; }
        if (isp) primes[np++] = i;
    }
    L = 1;
    for (int n = T; n <= X; n++) {
        u128 g = gcd128(L, (u128)n); u128 f = (u128)n / g;
        if (f && L > (~(u128)0) / f / 8) { printf("OVERFLOW: lcm too big for u128\n"); exit(2); }
        L = L * f;
    }
    for (int n = T; n <= X; n++) w[n] = L / (u128)n;
    for (int pos = T; pos <= X + 1; pos++) {
        u128 q = 1;
        for (int pi = 0; pi < np; pi++) {
            int p = primes[pi];
            int nuL = 0; { u128 t = L; while (t % (u128)p == 0) { t /= (u128)p; nuL++; } }
            int emax = 0;
            for (int n = pos; n <= X; n++) { int e = nu(n, p); if (e > emax) emax = e; }
            int ecap = 0; { u128 t = 1; while (t * (u128)p <= DCAP) { t *= (u128)p; ecap++; } }
            int lim = emax > ecap ? emax : ecap;
            int ex = nuL - lim; if (ex < 0) ex = 0;
            for (int i = 0; i < ex; i++) q *= (u128)p;
        }
        Q[pos] = q;
    }
}

static void record(u128 S) {
    if (S == 0) return;
    u128 g = gcd128(S, L);
    u128 den = L / g;
    if (den > DCAP) return;
    nfound++;
    if (nfound <= MAXPR) {
        print_u128(S / g); printf("/"); print_u128(den);
        printf("   runs:");
        for (int i = 0; i < nruns; i++) printf(" [%d,%d]", runs_a[i], runs_b[i]);
        printf("\n");
        fflush(stdout);
    }
}

static void dfs(int pos, u128 S) {
    nodes++;
    if (Q[pos] && (S % Q[pos])) return;
    if (pos > X - 1) { nleaf++; record(S); return; }
    /* skip position pos */
    dfs(pos + 1, S);
    /* start a maximal run [pos, j], j >= pos+1, then a gap */
    u128 acc = w[pos];
    for (int j = pos + 1; j <= X; j++) {
        acc += w[j];
        runs_a[nruns] = pos; runs_b[nruns] = j; nruns++;
        dfs(j + 2 <= X + 1 ? j + 2 : X + 1, S + acc);
        nruns--;
    }
}

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: %s T X DCAP [maxprint]\n", argv[0]); return 1; }
    T = atoi(argv[1]); X = atoi(argv[2]);
    DCAP = (u128)strtoull(argv[3], NULL, 10);
    if (argc > 4) MAXPR = atoi(argv[4]);
    build();
    printf("window [%d,%d], DCAP=", T, X); print_u128(DCAP);
    printf("  L="); print_u128(L); printf("\n");
    dfs(T, 0);
    printf("nodes=%lld leaves=%lld values-with-small-denominator=%lld\n",
           nodes, nleaf, nfound);
    return 0;
}
