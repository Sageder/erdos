/* s5_exhaust.c -- exhaustive search for a legal U subset [2,N] with sum 1/n = 1,
 *                 using the q-sieved universe produced by s4_qsieve.py.
 *
 * Exact integer arithmetic: L = lcm(universe) (fits comfortably in 128 bits for
 * the sieved universes), weight w[n] = L/n, target L.
 *
 * Pruning
 *   (1) remaining R must satisfy 0 <= R <= tail[pos]  (tail = sum of all weights
 *       of allowed positions >= pos).
 *   (2) legality: a run that has just started (runlen==1) must be continued.
 *   (3) p-adic:  Q[pos] | R, with Q[pos] = prod_p p^{max(0, nu_p(L) - maxe_p(pos))}
 *       and maxe_p(pos) = max nu_p(n) over allowed n in [pos,N].  This is exactly
 *       "the denominator of the remaining fraction must be realisable from [pos,N]".
 *
 * usage:  ./s5_exhaust universe_file        (file: first line N, then allowed n's)
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef unsigned __int128 u128;

static int N;
static int allowed[4096];
static u128 L, w[4096], tail[4098], Q[4098];
static long long nodes = 0, nsol = 0, maxsol = 1000000000LL;
static int chosen[4096], nch = 0;

static void print_u128(u128 x) {
    char buf[64]; int i = 63; buf[i--] = 0;
    if (!x) { printf("0"); return; }
    while (x) { buf[i--] = (char)('0' + (int)(x % 10)); x /= 10; }
    printf("%s", buf + i + 1);
}

static int nu(long long n, int p) { int e = 0; while (n % p == 0) { n /= p; e++; } return e; }

static u128 gcd128(u128 a, u128 b) { while (b) { u128 t = a % b; a = b; b = t; } return a; }

static void emit(void) {
    nsol++;
    if (nsol > maxsol) { printf("done nodes=%lld solutions=%lld (CAPPED)\n", nodes, nsol); exit(0); }
    printf("SOLUTION:");
    for (int i = 0; i < nch; i++) printf(" %d", chosen[i]);
    printf("\n");
    fflush(stdout);
}

static void dfs(int pos, u128 R, int runlen) {
    nodes++;
    if (R == 0) { if (runlen != 1) emit(); return; }
    if (pos > N) return;
    if (R > tail[pos]) return;
    if (R % Q[pos]) return;
    if (allowed[pos] && w[pos] <= R) {
        chosen[nch++] = pos;
        dfs(pos + 1, R - w[pos], runlen + 1);
        nch--;
    } else if (runlen == 1) {
        return;                     /* forced to continue the run but cannot */
    }
    if (runlen != 1) dfs(pos + 1, R, 0);
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: %s universe_file [maxsol]\n", argv[0]); return 1; }
    if (argc > 2) maxsol = atoll(argv[2]);
    FILE *f = fopen(argv[1], "r");
    if (!f) { perror("open"); return 1; }
    if (fscanf(f, "%d", &N) != 1) return 1;
    memset(allowed, 0, sizeof(allowed));
    int n, cnt = 0;
    while (fscanf(f, "%d", &n) == 1) { allowed[n] = 1; cnt++; }
    fclose(f);

    L = 1;
    for (n = 2; n <= N; n++) if (allowed[n]) { u128 g = gcd128(L, (u128)n); L = L / g * (u128)n; }

    for (n = 2; n <= N; n++) w[n] = allowed[n] ? L / (u128)n : (u128)0;

    tail[N + 1] = 0;
    for (n = N; n >= 2; n--) tail[n] = tail[n + 1] + w[n];

    /* primes up to N */
    int primes[4096], np = 0;
    for (int i = 2; i <= N; i++) {
        int isp = 1;
        for (int j = 2; (long long)j * j <= i; j++) if (i % j == 0) { isp = 0; break; }
        if (isp) primes[np++] = i;
    }
    /* nu_p(L) */
    int nuL[4096];
    for (int pi = 0; pi < np; pi++) {
        int p = primes[pi]; int e = 0; u128 t = L;
        while (t % (u128)p == 0) { t /= (u128)p; e++; }
        nuL[pi] = e;
    }
    /* maxe_p(pos), scanning pos downwards; then Q[pos] */
    int maxe[4096];
    for (int pi = 0; pi < np; pi++) maxe[pi] = 0;
    for (n = N + 1; n <= N + 2; n++) Q[n] = L;   /* nothing available */
    /* Q[N+1] = prod p^{nu_p(L)} = L  */
    for (n = N; n >= 2; n--) {
        if (allowed[n]) {
            for (int pi = 0; pi < np; pi++) {
                int p = primes[pi];
                if (n % p) continue;
                int e = nu(n, p);
                if (e > maxe[pi]) maxe[pi] = e;
            }
        }
        u128 q = 1;
        for (int pi = 0; pi < np; pi++) {
            int d = nuL[pi] - maxe[pi];
            for (int k = 0; k < d; k++) q *= (u128)primes[pi];
        }
        Q[n] = q;
    }

    printf("N=%d universe=%d L=", N, cnt); print_u128(L); printf("\n");
    fflush(stdout);
    dfs(2, L, 0);
    printf("done nodes=%lld solutions=%lld\n", nodes, nsol);
    return 0;
}
