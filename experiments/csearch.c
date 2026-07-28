/* csearch.c -- exhaustive search for finite U subset [2,N] with
 *   sum_{n in U} 1/n = 1   and   U has no isolated point
 *   (equivalently U is a disjoint union of blocks of length >= 2).
 *
 * Exact integer arithmetic: fix L = lcm(allowed universe); element n has
 * weight w[n] = L/n; we need sum of weights = L.
 *
 * PRUNE (p-adic, necessary condition):
 *   if sum_{n in U} 1/n = 1 and e := max_{n in U} nu_p(n) >= 1 then at least
 *   two elements attain nu_p = e.  Consequence used twice:
 *   (a) static: iteratively delete n whose nu_p(n) is the unique maximum;
 *   (b) dynamic: with remaining fraction R/L at position pos, we need
 *       nu_p(R/L) >= -maxe[p][pos] where maxe[p][pos] = max nu_p over allowed
 *       n in [pos,N].  Collecting over p this is the single condition
 *       Q[pos] | R,  Q[pos] = prod_p p^{nu_p(L) - maxe[p][pos]}.
 *
 * usage: ./csearch N [maxsolutions]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef unsigned __int128 u128;

static int N;
static int allowed[300];
static u128 L, w[300], tail[302], Q[302];
static long long nodes = 0, nsol = 0, maxsol = 20;
static int chosen[300], nch = 0;
static int primes[300], np = 0;

static void print_u128(u128 x) {
    char buf[64]; int i = 63; buf[i--] = 0;
    if (!x) { printf("0"); return; }
    while (x) { buf[i--] = '0' + (int)(x % 10); x /= 10; }
    printf("%s", buf + i + 1);
}

static int nu(int n, int p) { int e = 0; while (n % p == 0) { n /= p; e++; } return e; }

static void build_primes(void) {
    for (int i = 2; i <= N; i++) {
        int isp = 1;
        for (int j = 2; j * j <= i; j++) if (i % j == 0) { isp = 0; break; }
        if (isp) primes[np++] = i;
    }
}

static void build_universe(void) {
    for (int n = 2; n <= N; n++) allowed[n] = 1;
    int changed = 1;
    while (changed) {
        changed = 0;
        for (int pi = 0; pi < np; pi++) {
            int p = primes[pi];
            for (;;) {
                int emax = 0, cnt = 0;
                for (int n = 2; n <= N; n++) if (allowed[n]) {
                    int e = nu(n, p);
                    if (e > emax) { emax = e; cnt = 1; }
                    else if (e == emax && e > 0) cnt++;
                }
                if (emax >= 1 && cnt < 2) {
                    for (int n = 2; n <= N; n++)
                        if (allowed[n] && nu(n, p) == emax) { allowed[n] = 0; changed = 1; }
                } else break;
            }
        }
    }
}

static void dfs(int pos, u128 R, int runlen) {
    nodes++;
    if (R == 0) {
        if (runlen != 1) {
            nsol++;
            printf("SOL");
            for (int i = 0; i < nch; i++) printf(" %d", chosen[i]);
            printf("\n"); fflush(stdout);
            if (nsol >= maxsol) { printf("(solution cap reached)\n"); exit(0); }
        }
        return;
    }
    if (pos > N) return;
    if (R > tail[pos]) return;
    if (R % Q[pos]) return;
    if (allowed[pos] && w[pos] <= R) {
        chosen[nch++] = pos;
        dfs(pos + 1, R - w[pos], runlen + 1);
        nch--;
    } else if (runlen == 1) return;
    if (runlen != 1) dfs(pos + 1, R, 0);
}

int main(int argc, char **argv) {
    N = argc > 1 ? atoi(argv[1]) : 60;
    if (argc > 2) maxsol = atoll(argv[2]);
    build_primes();
    build_universe();

    /* L = lcm of allowed universe */
    L = 1;
    for (int pi = 0; pi < np; pi++) {
        int p = primes[pi], emax = 0;
        for (int n = 2; n <= N; n++) if (allowed[n]) { int e = nu(n, p); if (e > emax) emax = e; }
        for (int i = 0; i < emax; i++) L *= (u128)p;
    }
    printf("N=%d  universe:", N);
    for (int n = 2; n <= N; n++) if (allowed[n]) printf(" %d", n);
    printf("\nbanned:");
    for (int n = 2; n <= N; n++) if (!allowed[n]) printf(" %d", n);
    printf("\nL="); print_u128(L); printf("\n");

    for (int n = 2; n <= N; n++) w[n] = allowed[n] ? L / (u128)n : 0;
    tail[N + 1] = 0;
    for (int n = N; n >= 2; n--) tail[n] = tail[n + 1] + w[n];

    for (int pos = 2; pos <= N + 1; pos++) {
        u128 q = 1;
        for (int pi = 0; pi < np; pi++) {
            int p = primes[pi];
            int eL = 0; { u128 t = L; while (t % (u128)p == 0) { t /= (u128)p; eL++; } }
            int maxe = 0;
            for (int n = pos; n <= N; n++) if (allowed[n]) { int e = nu(n, p); if (e > maxe) maxe = e; }
            for (int i = 0; i < eL - maxe; i++) q *= (u128)p;
        }
        Q[pos] = q;
    }

    dfs(2, L, 0);
    printf("done nodes=%lld solutions=%lld\n", nodes, nsol);
    return 0;
}
