/* btarget.c -- route-D, Q3.
 *
 * EXHAUSTIVE decision: is there U subset [T,X] with no isolated point and
 *      sum_{n in U} 1/n = p/q  ?
 * (equivalently: is p/q in B(T) with all elements <= X ?)
 *
 * Exact integer arithmetic.  L = lcm(T..X) (unsigned __int128); the target is
 * the integer  TGT = L*p/q  (we require q | L, else the answer is trivially no);
 * element n has weight w[n] = L/n; we need a no-isolated-point U with
 * sum of weights = TGT.
 *
 * PRUNES (all rigorous):
 *   * tail:   0 <= R <= sum_{n=pos}^{X} w[n]
 *   * p-adic: with R the remaining integer target and pos the first free
 *     position, every future contribution F has nu_p(F) >= nu_p(L)-emax[p][pos]
 *     where emax[p][pos] = max nu_p(n), pos<=n<=X.  Since F must equal R,
 *     nu_p(R) >= nu_p(L)-emax[p][pos] for every p, i.e.  Q[pos] | R  with
 *          Q[pos] = prod_p p^{max(0, nu_p(L)-emax[p][pos])}.
 *
 * usage: ./btarget T X p q [maxsolutions]
 */
#include <stdio.h>
#include <stdlib.h>

typedef unsigned __int128 u128;

static int T, X, MAXSOL = 5;
static u128 L, w[300], tail[302], Q[302], TGT;
static long long nodes = 0, nsol = 0;
static int runs_a[200], runs_b[200], nruns = 0;
static int primes[300], np = 0;

static void print_u128(u128 x) {
    char b[64]; int i = 63; b[i--] = 0;
    if (!x) { printf("0"); return; }
    while (x) { b[i--] = (char)('0' + (int)(x % 10)); x /= 10; }
    printf("%s", b + i + 1);
}
static u128 gcd128(u128 a, u128 b) { while (b) { u128 t = a % b; a = b; b = t; } return a; }
static int nu(long long n, int p) { int e = 0; while (n % p == 0) { n /= p; e++; } return e; }

int main(int argc, char **argv) {
    if (argc < 5) { fprintf(stderr, "usage: %s T X p q [maxsol]\n", argv[0]); return 1; }
    T = atoi(argv[1]); X = atoi(argv[2]);
    unsigned long long P = strtoull(argv[3], NULL, 10), Qd = strtoull(argv[4], NULL, 10);
    if (argc > 5) MAXSOL = atoi(argv[5]);

    for (int i = 2; i <= X; i++) {
        int isp = 1;
        for (int j = 2; j * j <= i; j++) if (i % j == 0) { isp = 0; break; }
        if (isp) primes[np++] = i;
    }
    L = 1;
    for (int n = T; n <= X; n++) {
        u128 g = gcd128(L, (u128)n); u128 f = (u128)n / g;
        if (f && L > (~(u128)0) / f / 8) { printf("OVERFLOW: lcm(%d..%d) too big for u128 (reduce X)\n", T, X); return 2; }
        L = L * f;
    }
    for (int n = T; n <= X; n++) w[n] = L / (u128)n;
    tail[X + 1] = 0;
    for (int n = X; n >= T; n--) tail[n] = tail[n + 1] + w[n];
    if (L % (u128)Qd) {
        printf("q=%llu does not divide lcm(%d..%d): NO solution in the box\n", Qd, T, X);
        return 0;
    }
    TGT = L / (u128)Qd * (u128)P;
    for (int pos = T; pos <= X + 1; pos++) {
        u128 q = 1;
        for (int pi = 0; pi < np; pi++) {
            int p = primes[pi];
            int nuL = 0; { u128 t = L; while (t % (u128)p == 0) { t /= (u128)p; nuL++; } }
            int emax = 0;
            for (int n = pos; n <= X; n++) { int e = nu(n, p); if (e > emax) emax = e; }
            int ex = nuL - emax; if (ex < 0) ex = 0;
            for (int i = 0; i < ex; i++) q *= (u128)p;
        }
        Q[pos] = q;
    }
    printf("T=%d X=%d target=%llu/%llu  L=", T, X, P, Qd); print_u128(L); printf("\n");

    /* iterative DFS via recursion */
    void dfs(int pos, u128 R) {
        nodes++;
        if (R == 0) {
            nsol++;
            printf("SOLUTION runs:");
            for (int i = 0; i < nruns; i++) printf(" [%d,%d]", runs_a[i], runs_b[i]);
            printf("\n"); fflush(stdout);
            return;
        }
        if (pos > X - 1) return;
        if (R > tail[pos]) return;
        if (Q[pos] && (R % Q[pos])) return;
        u128 acc = w[pos];
        for (int j = pos + 1; j <= X; j++) {
            acc += w[j];
            if (acc > R) break;
            runs_a[nruns] = pos; runs_b[nruns] = j; nruns++;
            dfs(j + 2 <= X + 1 ? j + 2 : X + 1, R - acc);
            nruns--;
            if (nsol >= MAXSOL) return;
        }
        /* skip pos */
        dfs(pos + 1, R);
    }
    dfs(T, TGT);
    printf("done nodes=%lld solutions=%lld\n", nodes, nsol);
    return 0;
}
