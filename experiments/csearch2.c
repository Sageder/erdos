/* csearch2.c -- exhaustive search for legal U subset [2,N] with sum 1/n = 1,
 * accelerated by an ENDGAME TABLE for the top T positions.
 *
 * legal U : U subset Z_{>=2}, no isolated point (every n in U has a neighbour in U).
 *
 * Exact integer arithmetic.  L = lcm(allowed universe), w[n] = L/n, target L.
 * Prunes: (i) R <= tail[pos];  (ii) Q[pos] | R  (p-adic two-attainer condition,
 * see PROBLEM.md B2);  (iii) for pos == split, table lookup of R.
 *
 * Endgame: for s = N-T+1, and each incoming run-state c in {0,1,2}
 *   (0 = previous position not in U, 1 = previous in U with current run length 1,
 *    2 = previous in U with current run length >= 2),
 * tabulate every achievable value of sum_{n in U, n>=s} w[n] over legal completions.
 * Sorted + deduped; the main DFS then does a binary search at pos == s.
 *
 * usage: ./csearch2 N T [maxsol] [nsplit ipart]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef unsigned __int128 u128;

static int N, T, SPLIT;
static int allowed[400];
static u128 L, w[400], tail[402], Q[402];
static long long nodes = 0, nsol = 0, maxsol = 5;
static int chosen[400], nch = 0;
static int primes[400], np = 0;
static int nsplitw = 1, ipart = 0;   /* work splitting */
static long long taskctr = 0;

static u128 *tab[3];
static long long tabn[3], tabcap[3];

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
                    if (e > emax) { emax = e; cnt = 1; } else if (e == emax && e > 0) cnt++;
                }
                if (emax >= 1 && cnt < 2) {
                    for (int n = 2; n <= N; n++)
                        if (allowed[n] && nu(n, p) == emax) { allowed[n] = 0; changed = 1; }
                } else break;
            }
        }
    }
}

static void push(int c, u128 v) {
    if (tabn[c] == tabcap[c]) {
        tabcap[c] = tabcap[c] ? tabcap[c] * 2 : 1024;
        tab[c] = realloc(tab[c], tabcap[c] * sizeof(u128));
        if (!tab[c]) { fprintf(stderr, "OOM\n"); exit(1); }
    }
    tab[c][tabn[c]++] = v;
}
static void gen(int c0, int pos, int c, u128 acc) {
    if (pos > N) { if (c != 1) push(c0, acc); return; }
    if (allowed[pos]) gen(c0, pos + 1, c == 0 ? 1 : 2, acc + w[pos]);
    else if (c == 1) return;
    if (c != 1) gen(c0, pos + 1, 0, acc);
}
static int cmp128(const void *a, const void *b) {
    u128 x = *(const u128 *)a, y = *(const u128 *)b;
    return x < y ? -1 : (x > y ? 1 : 0);
}
static int lookup(int c, u128 v) {
    long long lo = 0, hi = tabn[c] - 1;
    while (lo <= hi) { long long mid = (lo + hi) / 2;
        if (tab[c][mid] == v) return 1;
        if (tab[c][mid] < v) lo = mid + 1; else hi = mid - 1; }
    return 0;
}

static void report(void) {
    nsol++;
    printf("SOL");
    for (int i = 0; i < nch; i++) printf(" %d", chosen[i]);
    printf("\n"); fflush(stdout);
    if (nsol >= maxsol) { printf("(solution cap reached)\n"); exit(0); }
}
/* complete the endgame explicitly once a hit is known, so we can print it */
static int emit(int pos, int c, u128 R) {
    if (pos > N) { if (c != 1 && R == 0) { report(); return 1; } return 0; }
    if (allowed[pos] && w[pos] <= R) {
        chosen[nch++] = pos;
        if (emit(pos + 1, c == 0 ? 1 : 2, R - w[pos])) { nch--; return 1; }
        nch--;
    } else if (c == 1) return 0;
    if (c != 1) return emit(pos + 1, 0, R);
    return 0;
}

static void dfs(int pos, u128 R, int runlen) {
    nodes++;
    if (R == 0) { if (runlen != 1) report(); return; }
    if (pos > N) return;
    if (R > tail[pos]) return;
    if (R % Q[pos]) return;
    if (pos == SPLIT) {
        int c = runlen == 0 ? 0 : (runlen == 1 ? 1 : 2);
        if (lookup(c, R)) emit(pos, c, R);
        return;
    }
    if (pos == 12 && nsplitw > 1) { if ((taskctr++ % nsplitw) != ipart) return; }
    if (allowed[pos] && w[pos] <= R) {
        chosen[nch++] = pos;
        dfs(pos + 1, R - w[pos], runlen + 1);
        nch--;
    } else if (runlen == 1) return;
    if (runlen != 1) dfs(pos + 1, R, 0);
}

int main(int argc, char **argv) {
    N = argc > 1 ? atoi(argv[1]) : 90;
    T = argc > 2 ? atoi(argv[2]) : 28;
    if (argc > 3) maxsol = atoll(argv[3]);
    if (argc > 5) { nsplitw = atoi(argv[4]); ipart = atoi(argv[5]); }
    build_primes(); build_universe();
    L = 1;
    for (int pi = 0; pi < np; pi++) {
        int p = primes[pi], emax = 0;
        for (int n = 2; n <= N; n++) if (allowed[n]) { int e = nu(n, p); if (e > emax) emax = e; }
        for (int i = 0; i < emax; i++) L *= (u128)p;
    }
    printf("N=%d T=%d  L=", N, T); print_u128(L); printf("\n");
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
    SPLIT = N - T + 1;
    if (SPLIT < 3) SPLIT = 3;
    for (int c = 0; c < 3; c++) {
        tabn[c] = tabcap[c] = 0; tab[c] = NULL;
        gen(c, SPLIT, c, 0);
        qsort(tab[c], tabn[c], sizeof(u128), cmp128);
        long long m = 0;
        for (long long i = 0; i < tabn[c]; i++) if (i == 0 || tab[c][i] != tab[c][i - 1]) tab[c][m++] = tab[c][i];
        printf("  endgame c=%d: %lld distinct sums\n", c, m);
        tabn[c] = m;
    }
    fflush(stdout);
    dfs(2, L, 0);
    printf("done N=%d nodes=%lld solutions=%lld\n", N, nodes, nsol);
    return 0;
}
