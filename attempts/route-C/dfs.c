/* dfs.c -- exhaustive search for finite U subset of a GIVEN universe A subset [2,N]
 *   with sum_{n in U} 1/n = 1  and  at most `budget` isolated points
 *   (n in U is isolated iff n-1 notin U and n+1 notin U).
 *
 * budget = 0  <=>  "legal" sets of the problem (no isolated point).
 *
 * Exact integer arithmetic: L = lcm(A); element n has weight w[n] = L/n; we need
 * the chosen weights to sum to exactly L.  unsigned __int128 throughout; the
 * program aborts if L does not fit.
 *
 * PRUNES
 *   (i)  tail bound:   R <= sum of all remaining weights
 *   (ii) p-adic:       Q[pos] | R, where Q[pos] = prod_p p^{nu_p(L)-maxe[p][pos]}
 *                      and maxe[p][pos] = max nu_p(n) over n in A ∩ [pos,N].
 *                      (Necessary since nu_p(R/L) >= -maxe[p][pos].)
 *   (iii) isolated budget.
 *
 * INPUT (stdin):  N budget maxsol
 *                 k  a_1 a_2 ... a_k        (the universe, increasing)
 * OUTPUT: SOL lines, then "done nodes=... solutions=..."
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef unsigned __int128 u128;

static int N, budget;
static long long maxsol = 50;
static int allowed[4096];
static u128 L, w[4096], tail[4098], Q[4098];
static long long nodes = 0, nsol = 0;
static int chosen[4096], nch = 0;
static int primes[4096], np = 0;

static void print_u128(u128 x) {
    char buf[64]; int i = 63; buf[i--] = 0;
    if (!x) { printf("0"); return; }
    while (x) { buf[i--] = '0' + (int)(x % 10); x /= 10; }
    printf("%s", buf + i + 1);
}
static int nu(int n, int p) { int e = 0; while (n % p == 0) { n /= p; e++; } return e; }

static void report(void) {
    nsol++;
    printf("SOL");
    for (int i = 0; i < nch; i++) printf(" %d", chosen[i]);
    printf("\n"); fflush(stdout);
    if (nsol >= maxsol) { printf("(solution cap reached)\n"); fflush(stdout); exit(0); }
}

static void dfs(int pos, u128 R, int runlen, int iso) {
    nodes++;
    if (R == 0) {
        int extra = (runlen == 1) ? 1 : 0;
        if (iso + extra <= budget) report();
        return;
    }
    if (pos > N) return;
    if (R > tail[pos]) return;
    if (R % Q[pos]) return;
    if (allowed[pos] && w[pos] <= R) {
        chosen[nch++] = pos;
        dfs(pos + 1, R - w[pos], runlen + 1, iso);
        nch--;
    }
    int extra = (runlen == 1) ? 1 : 0;
    if (iso + extra <= budget) dfs(pos + 1, R, 0, iso + extra);
}

int main(void) {
    int k;
    if (scanf("%d %d %lld", &N, &budget, &maxsol) != 3) return 1;
    if (scanf("%d", &k) != 1) return 1;
    memset(allowed, 0, sizeof(allowed));
    for (int i = 0; i < k; i++) { int a; if (scanf("%d", &a) != 1) return 1; allowed[a] = 1; }

    for (int i = 2; i <= N; i++) {
        int isp = 1;
        for (int j = 2; j * j <= i; j++) if (i % j == 0) { isp = 0; break; }
        if (isp) primes[np++] = i;
    }
    /* L = lcm(A) */
    L = 1;
    for (int pi = 0; pi < np; pi++) {
        int p = primes[pi], emax = 0;
        for (int n = 2; n <= N; n++) if (allowed[n]) { int e = nu(n, p); if (e > emax) emax = e; }
        for (int i = 0; i < emax; i++) {
            u128 nl = L * (u128)p;
            if (nl / (u128)p != L) { fprintf(stderr, "L overflow\n"); return 2; }
            L = nl;
        }
    }
    fprintf(stderr, "N=%d budget=%d |A|=%d L=", N, budget, k);
    { u128 t=L; char buf[64]; int i=63; buf[i--]=0; if(!t) buf[i--]='0';
      while(t){buf[i--]='0'+(int)(t%10); t/=10;} fprintf(stderr,"%s\n", buf+i+1); }

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
    dfs(2, L, 0, 0);
    printf("done nodes=%lld solutions=%lld\n", nodes, nsol);
    return 0;
}
