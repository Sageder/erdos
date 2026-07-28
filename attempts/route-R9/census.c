/* census.c — Route R9: structural census of monotone-4AP-free permutations ("avoiders")
 * of [1..N], for Erdős problem 196.
 *
 * Core formulation (verified against brute force by validate.py):
 *   Build avoiders by inserting values in increasing order. Inserting value m=n+1
 *   (the current maximum) into an avoider of [1..n] can only create a monotone 4-AP
 *   whose largest term is m, i.e. (m-3d, m-2d, m-d, m) read at increasing positions
 *   (increasing orientation, m LAST) or (m, m-d, m-2d, m-3d) (decreasing, m FIRST).
 *   So each d forbids either a SUFFIX of insertion slots (if pos(m-3d)<pos(m-2d)<pos(m-d):
 *   forbid slots p >= pos(m-d)+1) or a PREFIX (if pos(m-3d)>pos(m-2d)>pos(m-d): forbid
 *   slots p <= pos(m-d)).  Hence the allowed slots form a contiguous interval [lo,hi].
 *   (Slots are 0-indexed: inserting at slot p places m before the element currently at
 *   index p; slot n = append.)
 *
 * By the restriction principle (delete value n+1 from an avoider of [1..n+1] to get an
 * avoider of [1..n]) this insertion tree contains EVERY avoider exactly once: it IS the
 * extension tree of deliverable 3.
 *
 * Modes:
 *   exact D STATSMAX   exact DFS to depth D. Prints per level n<=D: count of avoiders,
 *                      count of 3AP-free ones, dead ends (no valid insertion of n+1),
 *                      branching histogram; count(D+1) as sum of branchings at level D.
 *                      For 3<=n<=STATSMAX also full statistics histograms.
 *   dump N             print all avoiders of [1..N], one per line (space separated).
 *   sis NMAX B M SEED  sequential importance sampling: B batches of M samples each.
 *                      Unbiased estimator of count(n) for all n<=NMAX, plus weighted
 *                      (= uniform-over-avoiders) statistics per level.
 *   tame k L type num den budget
 *                      DFS over k-AP-free avoiders (k in {3,4,5}) restricted to the
 *                      "tame" subtree: type 'm': pos(v) <= floor(num*v/den) for all v;
 *                      type 'a': pos(v) <= v + num.  (pos 1-indexed.)  Depth up to L or
 *                      until a level has count 0, or node budget exceeded.
 *
 * All output is exact integer counts except mode sis (clearly labeled estimates).
 */
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>

typedef uint64_t u64;
typedef uint8_t u8;

#define MX 200        /* max depth+2; u8 values suffice to 255 */
#define RATB 100       /* ratio histogram bins, width 0.25 starting at 1.0 */
#define N3B 400        /* 3-AP-count histogram cap */

/* ------------------------------------------------------------------ exact DFS */
static int D, STATSMAX;

typedef struct {
    u64 cnt[MX], cnt3f[MX], dead[MX];
    u64 bhist[MX][MX];
    /* stats histograms: [n][value][has3AP? 0=3AP-free,1=has 3AP] */
    u64 h_lis[18][18][2], h_lds[18][18][2], h_disp[18][18][2];
    u64 h_pos1[18][18][2], h_posN[18][18][2], h_fix[18][18][2];
    u64 h_rat[18][RATB][2];
    u64 h_n3[18][N3B][2];
    double sum_rat[18][2];
    u64 sum_n3[18][2];
    u8 perm[18][18], pos[18][18];
    u64 asserts_failed;
    /* empirical phi: per level, minimum over avoiders of max_v pos(v)/v (1-indexed),
     * with an argmin example; minratio_ext restricts to extendable (b>=1) avoiders. */
    double minratio[18], minratio_ext[18];
    u8 argmin[18][18], argmin_ext[18][18];
} Ctx;

static void collect_stats(Ctx *C, int n, int has3) {
    const u8 *pm = C->perm[n]; const u8 *ps = C->pos[n];
    int f = has3 ? 1 : 0;
    int up[18], dn[18]; int lis = 0, lds = 0;
    for (int i = 0; i < n; i++) {
        up[i] = 1; dn[i] = 1;
        for (int j = 0; j < i; j++) {
            if (pm[j] < pm[i] && up[j] + 1 > up[i]) up[i] = up[j] + 1;
            if (pm[j] > pm[i] && dn[j] + 1 > dn[i]) dn[i] = dn[j] + 1;
        }
        if (up[i] > lis) lis = up[i];
        if (dn[i] > lds) lds = dn[i];
    }
    C->h_lis[n][lis][f]++; C->h_lds[n][lds][f]++;
    int md = 0; double mr = 0;
    for (int v = 1; v <= n; v++) {
        int p1 = ps[v] + 1; int dd = p1 - v; if (dd < 0) dd = -dd;
        if (dd > md) md = dd;
        double r = (double)p1 / v; if (r > mr) mr = r;
    }
    C->h_disp[n][md][f]++;
    int rb = (int)((mr - 1.0) * 4.0 + 1e-9); if (rb >= RATB) rb = RATB - 1; if (rb < 0) rb = 0;
    C->h_rat[n][rb][f]++;
    C->sum_rat[n][f] += mr;
    C->h_pos1[n][ps[1] + 1][f]++; C->h_posN[n][ps[n] + 1][f]++;
    int fx = 0; for (int v = 1; v <= n; v++) if (ps[v] + 1 == v) fx++;
    C->h_fix[n][fx][f]++;
    int c3 = 0;
    for (int d = 1; 2 * d < n; d++)
        for (int x = 1; x + 2 * d <= n; x++) {
            int a = ps[x], b = ps[x + d], c = ps[x + 2 * d];
            if ((a < b && b < c) || (a > b && b > c)) c3++;
        }
    /* independent cross-check of the incremental has3 flag */
    if ((c3 > 0) != (has3 != 0)) C->asserts_failed++;
    int c3c = c3 >= N3B ? N3B - 1 : c3;
    C->h_n3[n][c3c][f]++; C->sum_n3[n][f] += (u64)c3;
}

static FILE *dumpf = NULL;
static int DUMPLEVEL = 0;

static void dfs(Ctx *C, int n, int has3) {
    C->cnt[n]++;
    if (!has3) C->cnt3f[n]++;
    if (DUMPLEVEL) {
        if (n == DUMPLEVEL) {
            for (int i = 0; i < n; i++) fprintf(dumpf, "%d%c", C->perm[n][i], i == n - 1 ? '\n' : ' ');
            return;
        }
    } else if (n >= 3 && n <= STATSMAX) collect_stats(C, n, has3);
    int m = n + 1, lo = 0, hi = n;
    const u8 *ps = C->pos[n];
    for (int d = 1; 3 * d < m; d++) {
        int a = ps[m - 3 * d], b = ps[m - 2 * d], c = ps[m - d];
        if (a < b) { if (b < c && c < hi) hi = c; }
        else if (b > c && c + 1 > lo) lo = c + 1;
        if (lo > hi) break;
    }
    int b = hi - lo + 1; if (b < 0) b = 0;
    if (!DUMPLEVEL) {
        C->bhist[n][b]++;
        if (n <= 15) { /* empirical phi tracking */
            double mr = 0;
            for (int v = 1; v <= n; v++) { double r = (double)(ps[v] + 1) / v; if (r > mr) mr = r; }
            if (mr < C->minratio[n]) { C->minratio[n] = mr; memcpy(C->argmin[n], C->perm[n], (size_t)n); }
            if (b >= 1 && mr < C->minratio_ext[n]) { C->minratio_ext[n] = mr; memcpy(C->argmin_ext[n], C->perm[n], (size_t)n); }
        }
        if (b == 0) { C->dead[n]++; return; }
        if (n == D) { C->cnt[n + 1] += (u64)b; return; }
    } else if (b == 0) return;
    for (int p = lo; p <= hi; p++) {
        int h3 = has3;
        if (!h3) {
            for (int d = 1; 2 * d < m; d++) {
                int a2 = ps[m - 2 * d], c2 = ps[m - d];
                if (a2 < c2) { if (p > c2) { h3 = 1; break; } }
                else if (p <= c2) { h3 = 1; break; }
            }
        }
        u8 *cp = C->perm[n + 1], *cq = C->pos[n + 1];
        memcpy(cp, C->perm[n], (size_t)p);
        cp[p] = (u8)m;
        memcpy(cp + p + 1, C->perm[n] + p, (size_t)(n - p));
        for (int v = 1; v <= n; v++) { int q = ps[v]; cq[v] = (u8)(q + (q >= p)); }
        cq[m] = (u8)p;
        dfs(C, n + 1, h3);
    }
}

static void print_hist_row(const char *name, int n, u64 h[][2], int maxi) {
    printf("  %-8s n=%2d :", name, n);
    for (int i = 0; i <= maxi; i++) {
        u64 t = h[i][0] + h[i][1];
        if (t) printf(" %d:%llu", i, (unsigned long long)t);
    }
    printf("\n");
    printf("  %-8s n=%2d (3AP-free only):", name, n);
    for (int i = 0; i <= maxi; i++) if (h[i][0]) printf(" %d:%llu", i, (unsigned long long)h[i][0]);
    printf("\n");
}

static void run_exact(int Din, int statsmax) {
    D = Din; STATSMAX = statsmax;
    static Ctx C;               /* zero-initialized, in BSS (large) */
    memset(&C, 0, sizeof C);
    for (int n = 0; n < 18; n++) C.minratio[n] = C.minratio_ext[n] = 1e18;
    C.perm[1][0] = 1; C.pos[1][1] = 0;
    dfs(&C, 1, 0);
    printf("== exact DFS to depth D=%d (STATSMAX=%d) ==\n", D, STATSMAX);
    printf("%-3s %20s %14s %12s %10s %s\n", "n", "count", "3AP-free", "dead-ends", "maxbranch", "");
    for (int n = 1; n <= D; n++) {
        int mb = 0; for (int b = 0; b < MX; b++) if (C.bhist[n][b]) mb = b;
        printf("%-3d %20llu %14llu %12llu %10d\n", n, (unsigned long long)C.cnt[n],
               (unsigned long long)C.cnt3f[n], (unsigned long long)C.dead[n], mb);
    }
    printf("%-3d %20llu   (children of level %d; = exact count at n=%d)\n",
           D + 1, (unsigned long long)C.cnt[D + 1], D, D + 1);
    printf("\n== empirical phi: minimum over avoiders of [1..n] of max_v pos(v)/v ==\n");
    for (int n = 1; n <= D && n <= 15; n++) {
        printf("n=%2d : min maxratio = %.6f (over all)  %.6f (over extendable)\n",
               n, C.minratio[n], C.minratio_ext[n]);
        printf("   argmin:");
        for (int i = 0; i < n; i++) printf(" %d", C.argmin[n][i]);
        printf("\n   argmin-extendable:");
        for (int i = 0; i < n; i++) printf(" %d", C.argmin_ext[n][i]);
        printf("\n");
    }
    printf("\n== branching histograms (n -> {b: #avoiders of [1..n] with exactly b valid insertions of n+1}) ==\n");
    for (int n = 1; n <= D; n++) {
        printf("n=%2d :", n);
        for (int b = 0; b < MX; b++) if (C.bhist[n][b]) printf(" %d:%llu", b, (unsigned long long)C.bhist[n][b]);
        printf("\n");
    }
    if (STATSMAX >= 3) {
        printf("\n== per-level statistics (all avoiders / 3AP-free subpopulation) ==\n");
        for (int n = 3; n <= STATSMAX && n <= D; n++) {
            printf("--- n=%d  (avoiders=%llu, of which 3AP-free=%llu) ---\n", n,
                   (unsigned long long)C.cnt[n], (unsigned long long)C.cnt3f[n]);
            print_hist_row("LIS", n, C.h_lis[n], n);
            print_hist_row("LDS", n, C.h_lds[n], n);
            print_hist_row("maxdisp", n, C.h_disp[n], n);
            print_hist_row("pos1", n, C.h_pos1[n], n);
            print_hist_row("posN", n, C.h_posN[n], n);
            print_hist_row("fixpts", n, C.h_fix[n], n);
            printf("  ratio-bins (bin i = maxratio in [1+i/4,1+(i+1)/4)) n=%2d :", n);
            for (int i = 0; i < RATB; i++) { u64 t = C.h_rat[n][i][0] + C.h_rat[n][i][1]; if (t) printf(" %d:%llu", i, (unsigned long long)t); }
            printf("\n");
            double tot = (double)C.cnt[n];
            printf("  mean maxratio = %.4f (3AP-free: %.4f)\n",
                   (C.sum_rat[n][0] + C.sum_rat[n][1]) / tot,
                   C.cnt3f[n] ? C.sum_rat[n][0] / (double)C.cnt3f[n] : 0.0);
            printf("  #3APs   n=%2d :", n);
            for (int i = 0; i < N3B; i++) { u64 t = C.h_n3[n][i][0] + C.h_n3[n][i][1]; if (t) printf(" %d:%llu", i, (unsigned long long)t); }
            printf("\n  mean #3APs = %.4f (over avoiders with >=1: %.4f)\n",
                   (double)(C.sum_n3[n][0] + C.sum_n3[n][1]) / tot,
                   (C.cnt[n] - C.cnt3f[n]) ? (double)C.sum_n3[n][1] / (double)(C.cnt[n] - C.cnt3f[n]) : 0.0);
        }
        printf("\ninternal cross-check failures (incremental 3AP flag vs direct count): %llu\n",
               (unsigned long long)C.asserts_failed);
    }
}

static void run_dump(int N) {
    static Ctx C; memset(&C, 0, sizeof C);
    DUMPLEVEL = N; dumpf = stdout; D = N; STATSMAX = 0;
    C.perm[1][0] = 1; C.pos[1][1] = 0;
    dfs(&C, 1, 0);
}

/* ------------------------------------------------------------------ SIS sampling */
static u64 sm_state;
static inline u64 sm_next(void) {
    u64 z = (sm_state += 0x9e3779b97f4a7c15ULL);
    z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL;
    z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL;
    return z ^ (z >> 31);
}

static void run_sis(int NMAX, int B, long M, u64 seed) {
    if (NMAX >= MX - 2) { fprintf(stderr, "NMAX too large\n"); exit(1); }
    double *bw = calloc((size_t)B * (NMAX + 2), sizeof(double));       /* batch sums of W_n */
    double *bdead = calloc((size_t)B * (NMAX + 2), sizeof(double));    /* sum W_n * 1{dead at n} */
    double *bt2 = calloc((size_t)B * (NMAX + 2), sizeof(double));      /* sum W_n * 1{maxratio<=2} */
    double *bt3 = calloc((size_t)B * (NMAX + 2), sizeof(double));
    double *bt4 = calloc((size_t)B * (NMAX + 2), sizeof(double));
    double *bpos1 = calloc((size_t)B * (NMAX + 2), sizeof(double));    /* sum W_n * pos(1) */
    double *brat = calloc((size_t)B * (NMAX + 2), sizeof(double));     /* sum W_n * maxratio */
    u8 pm[MX], ps[MX];
    printf("== SIS: %d batches x %ld samples, seed=%llu, NMAX=%d ==\n", B, M, (unsigned long long)seed, NMAX);
    for (int bt = 0; bt < B; bt++) {
        sm_state = seed + 0x1000000ULL * (u64)(bt + 1);
        double *W = bw + (size_t)bt * (NMAX + 2);
        double *Dd = bdead + (size_t)bt * (NMAX + 2);
        double *T2 = bt2 + (size_t)bt * (NMAX + 2), *T3 = bt3 + (size_t)bt * (NMAX + 2), *T4 = bt4 + (size_t)bt * (NMAX + 2);
        double *P1 = bpos1 + (size_t)bt * (NMAX + 2), *RT = brat + (size_t)bt * (NMAX + 2);
        for (long s = 0; s < M; s++) {
            pm[0] = 1; ps[1] = 0;
            double w = 1.0;
            for (int n = 1; n <= NMAX; n++) {
                /* level-n functionals with weight w = prod b_1..b_{n-1} */
                W[n] += w;
                double mr = 0; for (int v = 1; v <= n; v++) { double r = (double)(ps[v] + 1) / v; if (r > mr) mr = r; }
                if (mr <= 2.0) T2[n] += w;
                if (mr <= 3.0) T3[n] += w;
                if (mr <= 4.0) T4[n] += w;
                P1[n] += w * (ps[1] + 1);
                RT[n] += w * mr;
                int m = n + 1, lo = 0, hi = n;
                for (int d = 1; 3 * d < m; d++) {
                    int a = ps[m - 3 * d], b2 = ps[m - 2 * d], c = ps[m - d];
                    if (a < b2) { if (b2 < c && c < hi) hi = c; }
                    else if (b2 > c && c + 1 > lo) lo = c + 1;
                    if (lo > hi) break;
                }
                int b = hi - lo + 1; if (b < 0) b = 0;
                if (b == 0) { Dd[n] += w; break; }
                if (n == NMAX) break;
                int p = lo + (int)(sm_next() % (u64)b);
                w *= (double)b;
                memmove(pm + p + 1, pm + p, (size_t)(n - p));
                pm[p] = (u8)m;
                for (int v = 1; v <= n; v++) ps[v] += (ps[v] >= p);
                ps[m] = (u8)p;
            }
        }
    }
    /* report: per level, estimate count(n) = mean over batches of (batch sum / M) */
    printf("%-3s %16s %13s %9s | %10s %10s %10s %10s %10s %10s\n",
           "n", "est_count", "stderr", "rel", "deadfrac", "P(r<=2)", "P(r<=3)", "P(r<=4)", "E[pos1]", "E[maxrat]");
    for (int n = 1; n <= NMAX; n++) {
        double mean = 0, m2 = 0;
        double td = 0, tw = 0, t2 = 0, t3 = 0, t4 = 0, p1 = 0, rt = 0;
        for (int bt = 0; bt < B; bt++) {
            double v = bw[(size_t)bt * (NMAX + 2) + n] / (double)M;
            mean += v; m2 += v * v;
            tw += bw[(size_t)bt * (NMAX + 2) + n];
            td += bdead[(size_t)bt * (NMAX + 2) + n];
            t2 += bt2[(size_t)bt * (NMAX + 2) + n];
            t3 += bt3[(size_t)bt * (NMAX + 2) + n];
            t4 += bt4[(size_t)bt * (NMAX + 2) + n];
            p1 += bpos1[(size_t)bt * (NMAX + 2) + n];
            rt += brat[(size_t)bt * (NMAX + 2) + n];
        }
        mean /= B;
        double var = (m2 / B - mean * mean) * (double)B / (double)(B - 1);
        double se = sqrt(var / B);
        printf("%-3d %16.6e %13.3e %8.4f%% | %10.3e %10.3e %10.3e %10.3e %10.4f %10.4f\n",
               n, mean, se, mean > 0 ? 100.0 * se / mean : 0.0,
               tw > 0 ? td / tw : 0.0, tw > 0 ? t2 / tw : 0.0, tw > 0 ? t3 / tw : 0.0, tw > 0 ? t4 / tw : 0.0,
               tw > 0 ? p1 / tw : 0.0, tw > 0 ? rt / tw : 0.0);
    }
    free(bw); free(bdead); free(bt2); free(bt3); free(bt4); free(bpos1); free(brat);
}

/* ------------------------------------------------------------------ tame DFS */
static int TK, TL; static char TTYPE; static long TNUM, TDEN;
static u64 tbudget, tnodes;
static u64 tcnt[MX], tdead[MX];
static int tmaxb[MX];
static u8 tperm[MX][MX], tpos[MX][MX];
static int budget_hit = 0;

static inline int bound_int(int v) {
    if (TTYPE == 'm') return (int)(((long)TNUM * v) / TDEN);
    return v + (int)TNUM;
}

static void tdfs(int n) {
    if (++tnodes > tbudget) {
        if (!budget_hit) {  /* report where in the tree the abort happened */
            printf("BUDGET ABORT at level %d, current permutation:", n);
            for (int i = 0; i < n; i++) printf(" %d", tperm[n][i]);
            printf("\n");
        }
        budget_hit = 1; return;
    }
    tcnt[n]++;
    if (n == TL) return;
    int m = n + 1, lo = 0, hi = n;
    const u8 *ps = tpos[n];
    /* k-AP constraint: terms m-(K-1)d .. m-d must not be monotone with m appended */
    for (int d = 1; (TK - 1) * d < m; d++) {
        int inc = 1, dec = 1;
        int prev = ps[m - (TK - 1) * d];
        for (int j = TK - 2; j >= 1; j--) {
            int q = ps[m - j * d];
            if (!(prev < q)) inc = 0;
            if (!(prev > q)) dec = 0;
            prev = q;
        }
        int c = ps[m - d];
        if (inc && c < hi) hi = c;
        if (dec && c + 1 > lo) lo = c + 1;
        if (lo > hi) break;
    }
    /* tameness: p+1 <= bound(m); shifted values (pos>=p) need slack>=1 */
    int pmax = bound_int(m) - 1; if (pmax > n) pmax = n;
    if (pmax < hi) hi = pmax;
    for (int v = 1; v <= n; v++)
        if (ps[v] + 1 == bound_int(v) && ps[v] + 1 > lo) lo = ps[v] + 1;
    int b = hi - lo + 1; if (b < 0) b = 0;
    if (b > tmaxb[n]) tmaxb[n] = b;
    if (b == 0) { tdead[n]++; return; }
    for (int p = lo; p <= hi; p++) {
        u8 *cp = tperm[n + 1], *cq = tpos[n + 1];
        memcpy(cp, tperm[n], (size_t)p);
        cp[p] = (u8)m;
        memcpy(cp + p + 1, tperm[n] + p, (size_t)(n - p));
        for (int v = 1; v <= n; v++) { int q = ps[v]; cq[v] = (u8)(q + (q >= p)); }
        cq[m] = (u8)p;
        tdfs(n + 1);
        if (budget_hit) return;
    }
}

static void run_tame(int k, int L, char type, long num, long den, u64 budget) {
    if (L >= MX - 2) { fprintf(stderr, "L too large\n"); exit(1); }
    TK = k; TL = L; TTYPE = type; TNUM = num; TDEN = den; tbudget = budget; tnodes = 0;
    memset(tcnt, 0, sizeof tcnt); memset(tdead, 0, sizeof tdead); memset(tmaxb, 0, sizeof tmaxb);
    budget_hit = 0;
    if (bound_int(1) < 1) { printf("bound(1)<1: empty tree\n"); return; }
    tperm[1][0] = 1; tpos[1][1] = 0;
    tdfs(1);
    printf("== tame DFS: k=%d, constraint pos(v) <= %s, depth<=%d, budget=%llu%s ==\n",
           k, type == 'm' ? "floor(num*v/den)" : "v+K", L, (unsigned long long)budget,
           budget_hit ? "  [BUDGET EXCEEDED - counts are partial lower bounds]" : "");
    printf("   (num=%ld den=%ld)\n", num, den);
    printf("%-3s %16s %12s %8s\n", "n", "tame_count", "tame_dead", "maxbranch");
    int lastnz = 0;
    for (int n = 1; n <= L; n++) {
        if (tcnt[n]) lastnz = n;
        if (tcnt[n] || n <= lastnz + 1)
            printf("%-3d %16llu %12llu %8d\n", n, (unsigned long long)tcnt[n],
                   (unsigned long long)tdead[n], tmaxb[n]);
        if (!tcnt[n]) { printf("EXTINCT at n=%d (no tame avoiders)\n", n); break; }
    }
    if (!budget_hit && tcnt[L]) printf("SURVIVES to depth L=%d with count %llu\n", L, (unsigned long long)tcnt[L]);
    printf("total nodes visited: %llu\n", (unsigned long long)tnodes);
}

/* ------------------------------------------------------------------ dive mode:
 * random restarts down the tame tree; unbiased view of reachable depth independent
 * of DFS (lexicographic) order.  Child chosen uniformly among tame-allowed slots. */
static void run_dive(int k, int L, char type, long num, long den, long M, u64 seed) {
    TK = k; TTYPE = type; TNUM = num; TDEN = den;
    u64 depth_hist[MX]; memset(depth_hist, 0, sizeof depth_hist);
    int best = 0; u8 bestp[MX];
    u8 pm[MX], ps[MX];
    sm_state = seed;
    for (long s = 0; s < M; s++) {
        pm[0] = 1; ps[1] = 0;
        int n = 1;
        while (n < L) {
            int m = n + 1, lo = 0, hi = n;
            for (int d = 1; (TK - 1) * d < m; d++) {
                int inc = 1, dec = 1;
                int prev = ps[m - (TK - 1) * d];
                for (int j = TK - 2; j >= 1; j--) {
                    int q = ps[m - j * d];
                    if (!(prev < q)) inc = 0;
                    if (!(prev > q)) dec = 0;
                    prev = q;
                }
                int c = ps[m - d];
                if (inc && c < hi) hi = c;
                if (dec && c + 1 > lo) lo = c + 1;
                if (lo > hi) break;
            }
            int pmax = bound_int(m) - 1; if (pmax > n) pmax = n;
            if (pmax < hi) hi = pmax;
            for (int v = 1; v <= n; v++)
                if (ps[v] + 1 == bound_int(v) && ps[v] + 1 > lo) lo = ps[v] + 1;
            int b = hi - lo + 1; if (b < 0) b = 0;
            if (b == 0) break;
            int p = lo + (int)(sm_next() % (u64)b);
            memmove(pm + p + 1, pm + p, (size_t)(n - p));
            pm[p] = (u8)m;
            for (int v = 1; v <= n; v++) ps[v] += (ps[v] >= p);
            ps[m] = (u8)p;
            n++;
        }
        depth_hist[n]++;
        if (n > best) { best = n; memcpy(bestp, pm, (size_t)n); }
    }
    printf("== dive: k=%d, %s (num=%ld den=%ld), L=%d, M=%ld dives, seed=%llu ==\n",
           k, type == 'm' ? "pos(v)<=floor(num*v/den)" : "pos(v)<=v+K", num, den, L, M,
           (unsigned long long)seed);
    printf("reached-depth histogram:");
    for (int n = 0; n < MX; n++) if (depth_hist[n]) printf(" %d:%llu", n, (unsigned long long)depth_hist[n]);
    printf("\nmax depth reached: %d\n", best);
    printf("deepest permutation found:");
    for (int i = 0; i < best; i++) printf(" %d", bestp[i]);
    printf("\n");
}

/* ------------------------------------------------------------------ tsis mode:
 * SIS restricted to the tame tree: unbiased estimator of the number of tame
 * k-AP-free avoiders at every level n <= NMAX, with batch error bars. */
static void run_tsis(int k, int NMAX, char type, long num, long den, int B, long M, u64 seed) {
    TK = k; TTYPE = type; TNUM = num; TDEN = den;
    double *bw = calloc((size_t)B * (NMAX + 2), sizeof(double));
    u8 pm[MX], ps[MX];
    for (int bt = 0; bt < B; bt++) {
        sm_state = seed + 0x1000000ULL * (u64)(bt + 1);
        double *W = bw + (size_t)bt * (NMAX + 2);
        for (long s = 0; s < M; s++) {
            pm[0] = 1; ps[1] = 0;
            double w = 1.0;
            for (int n = 1; n <= NMAX; n++) {
                W[n] += w;
                if (n == NMAX) break;
                int m = n + 1, lo = 0, hi = n;
                for (int d = 1; (TK - 1) * d < m; d++) {
                    int inc = 1, dec = 1;
                    int prev = ps[m - (TK - 1) * d];
                    for (int j = TK - 2; j >= 1; j--) {
                        int q = ps[m - j * d];
                        if (!(prev < q)) inc = 0;
                        if (!(prev > q)) dec = 0;
                        prev = q;
                    }
                    int c = ps[m - d];
                    if (inc && c < hi) hi = c;
                    if (dec && c + 1 > lo) lo = c + 1;
                    if (lo > hi) break;
                }
                int pmax = bound_int(m) - 1; if (pmax > n) pmax = n;
                if (pmax < hi) hi = pmax;
                for (int v = 1; v <= n; v++)
                    if (ps[v] + 1 == bound_int(v) && ps[v] + 1 > lo) lo = ps[v] + 1;
                int b = hi - lo + 1; if (b < 0) b = 0;
                if (b == 0) break;
                int p = lo + (int)(sm_next() % (u64)b);
                w *= (double)b;
                memmove(pm + p + 1, pm + p, (size_t)(n - p));
                pm[p] = (u8)m;
                for (int v = 1; v <= n; v++) ps[v] += (ps[v] >= p);
                ps[m] = (u8)p;
            }
        }
    }
    printf("== tsis: k=%d, %s (num=%ld den=%ld), %d batches x %ld, seed=%llu ==\n",
           k, type == 'm' ? "pos(v)<=floor(num*v/den)" : "pos(v)<=v+K", num, den, B, M,
           (unsigned long long)seed);
    printf("%-3s %16s %13s %10s\n", "n", "est_tame_count", "stderr", "rel");
    for (int n = 1; n <= NMAX; n++) {
        double mean = 0, m2 = 0;
        for (int bt = 0; bt < B; bt++) {
            double v = bw[(size_t)bt * (NMAX + 2) + n] / (double)M;
            mean += v; m2 += v * v;
        }
        mean /= B;
        double var = (m2 / B - mean * mean) * (double)B / (double)(B - 1);
        double se = sqrt(var / B);
        printf("%-3d %16.6e %13.3e %9.3f%%\n", n, mean, se, mean > 0 ? 100.0 * se / mean : 0.0);
        if (mean == 0.0 && n > 5) { printf("(no surviving samples beyond n=%d)\n", n); break; }
    }
    free(bw);
}

/* ------------------------------------------------------------------ beam mode:
 * wide beam search down the tame tree.  Exact level widths until the first
 * subsampling event; thereafter lower-bound evidence.  Reservoir sampling keeps
 * the beam uniform among generated children. */
static void run_beam(int k, int L, char type, long num, long den, long CAP, u64 seed) {
    TK = k; TTYPE = type; TNUM = num; TDEN = den;
    sm_state = seed;
    size_t stride = MX;
    u8 *cur = malloc((size_t)CAP * stride), *nxt = malloc((size_t)CAP * stride);
    if (!cur || !nxt) { fprintf(stderr, "beam alloc failed\n"); exit(1); }
    long ncur = 1; cur[0] = 1;
    int exact = 1;
    printf("== beam: k=%d, %s (num=%ld den=%ld), cap=%ld, seed=%llu ==\n",
           k, type == 'm' ? "pos(v)<=floor(num*v/den)" : "pos(v)<=v+K", num, den, CAP,
           (unsigned long long)seed);
    u8 ps[MX];
    for (int n = 1; n < L && ncur > 0; n++) {
        long gen = 0, kept = 0;
        for (long i = 0; i < ncur; i++) {
            u8 *pm = cur + (size_t)i * stride;
            for (int j = 0; j < n; j++) ps[pm[j]] = (u8)j;
            int m = n + 1, lo = 0, hi = n;
            for (int d = 1; (TK - 1) * d < m; d++) {
                int inc = 1, dec = 1;
                int prev = ps[m - (TK - 1) * d];
                for (int j = TK - 2; j >= 1; j--) {
                    int q = ps[m - j * d];
                    if (!(prev < q)) inc = 0;
                    if (!(prev > q)) dec = 0;
                    prev = q;
                }
                int c = ps[m - d];
                if (inc && c < hi) hi = c;
                if (dec && c + 1 > lo) lo = c + 1;
                if (lo > hi) break;
            }
            int pmax = bound_int(m) - 1; if (pmax > n) pmax = n;
            if (pmax < hi) hi = pmax;
            for (int v = 1; v <= n; v++)
                if (ps[v] + 1 == bound_int(v) && ps[v] + 1 > lo) lo = ps[v] + 1;
            for (int p = lo; p <= hi; p++) {
                gen++;
                long slot;
                if (kept < CAP) slot = kept++;
                else {
                    u64 r = sm_next() % (u64)gen;
                    if (r >= (u64)CAP) continue;
                    slot = (long)r;
                }
                u8 *cp = nxt + (size_t)slot * stride;
                memcpy(cp, pm, (size_t)p);
                cp[p] = (u8)m;
                memcpy(cp + p + 1, pm + p, (size_t)(n - p));
            }
        }
        if (gen > CAP) exact = 0;
        printf("level %2d -> %2d : children generated %ld%s%s\n", n, n + 1, gen,
               exact ? " (EXACT width)" : " (from subsampled beam: lower-bound evidence)",
               gen > CAP ? " [subsampled to cap]" : "");
        u8 *t = cur; cur = nxt; nxt = t;
        ncur = kept;
        if (ncur == 0) { printf("beam EXTINCT after level %d\n", n); break; }
        if (n + 1 == L) {
            printf("beam reached depth L=%d with %ld nodes; example:", L, ncur);
            for (int j = 0; j < L; j++) printf(" %d", cur[j]);
            printf("\n");
        }
    }
    free(cur); free(nxt);
}

/* ------------------------------------------------------------------ main */
int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: census exact|dump|sis|tame ...\n"); return 1; }
    if (!strcmp(argv[1], "exact")) {
        int d = atoi(argv[2]), sm = atoi(argv[3]);
        if (d < 1 || d > 15) { fprintf(stderr, "D in 1..15\n"); return 1; }
        if (sm > 15) sm = 15;
        run_exact(d, sm);
    } else if (!strcmp(argv[1], "dump")) {
        int N = atoi(argv[2]);
        if (N < 1 || N > 12) { fprintf(stderr, "dump N in 1..12\n"); return 1; }
        run_dump(N);
    } else if (!strcmp(argv[1], "sis")) {
        int nmax = atoi(argv[2]), B = atoi(argv[3]); long M = atol(argv[4]);
        u64 seed = strtoull(argv[5], NULL, 10);
        run_sis(nmax, B, M, seed);
    } else if (!strcmp(argv[1], "tame")) {
        int k = atoi(argv[2]), L = atoi(argv[3]); char type = argv[4][0];
        long num = atol(argv[5]), den = atol(argv[6]);
        u64 budget = strtoull(argv[7], NULL, 10);
        run_tame(k, L, type, num, den, budget);
    } else if (!strcmp(argv[1], "tsis")) {
        int k = atoi(argv[2]), nmax = atoi(argv[3]); char type = argv[4][0];
        long num = atol(argv[5]), den = atol(argv[6]);
        int B = atoi(argv[7]); long M = atol(argv[8]); u64 seed = strtoull(argv[9], NULL, 10);
        if (nmax >= MX - 2) { fprintf(stderr, "NMAX too large\n"); return 1; }
        run_tsis(k, nmax, type, num, den, B, M, seed);
    } else if (!strcmp(argv[1], "beam")) {
        int k = atoi(argv[2]), L = atoi(argv[3]); char type = argv[4][0];
        long num = atol(argv[5]), den = atol(argv[6]);
        long cap = atol(argv[7]); u64 seed = strtoull(argv[8], NULL, 10);
        if (L >= MX - 2) { fprintf(stderr, "L too large\n"); return 1; }
        run_beam(k, L, type, num, den, cap, seed);
    } else if (!strcmp(argv[1], "dive")) {
        int k = atoi(argv[2]), L = atoi(argv[3]); char type = argv[4][0];
        long num = atol(argv[5]), den = atol(argv[6]);
        long M = atol(argv[7]); u64 seed = strtoull(argv[8], NULL, 10);
        if (L >= MX - 2) { fprintf(stderr, "L too large\n"); return 1; }
        run_dive(k, L, type, num, den, M, seed);
    } else { fprintf(stderr, "unknown mode\n"); return 1; }
    return 0;
}
