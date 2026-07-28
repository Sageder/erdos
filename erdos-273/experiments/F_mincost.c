/* F_mincost.c -- Route F, Erdos problem 273.
 *
 * CLAIM TESTED:  exact value of
 *    X(L,W) = min over covering systems of Z with PAIRWISE DISTINCT moduli,
 *             all moduli > 1, dividing L, and lying in the world W, of
 *             Waste := sum_i (L/n_i) - L  =  sum_{r mod L} (mult(r)-1).
 * Then  min sum_i 1/n_i  =  1 + X(L,W)/L   exactly (all integer arithmetic).
 *
 * METHOD: iterative deepening on Wmax; DFS branching on the SMALLEST uncovered
 * residue r (complete: any covering must contain the class r mod d for some
 * unused admissible d); prune as soon as accumulated waste exceeds Wmax
 * (waste is monotone non-decreasing) and when the residual reciprocal budget
 * of the unused moduli cannot cover the remaining residues.
 *
 * USAGE: F_mincost L wmax_cap m1 m2 m3 ...      (moduli given explicitly)
 * Prints, for each Wmax = 0..wmax_cap, either UNSAT or the first system found.
 *
 * CONCLUSION: recorded in attempts/route-F-efficiency/FINDINGS.md.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static int L, NW, ND;
static int ds[4096], cnt[4096];
static uint64_t lastmask;
static uint64_t *base_[4096];
static uint64_t **cov, **scr;
static int used[4096];
static int sol_d[4096], sol_a[4096], sol_len;
static long long nodes, nodecap;
static int MAXD;

static void shl(uint64_t *dst, const uint64_t *src, int a) {
    int ws = a >> 6, bs = a & 63;
    if (bs == 0) {
        for (int w = NW - 1; w >= ws; w--) dst[w] = src[w - ws];
        for (int w = ws - 1; w >= 0; w--) dst[w] = 0;
    } else {
        for (int w = NW - 1; w >= 0; w--) {
            int s = w - ws;
            uint64_t v = 0;
            if (s >= 0) {
                v = src[s] << bs;
                if (s > 0) v |= src[s - 1] >> (64 - bs);
            }
            dst[w] = v;
        }
    }
}

static int dfs(int depth, int ncov, int waste, int wmax, long long budget) {
    nodes++;
    if (nodecap && nodes > nodecap) return -1;   /* abort */
    if (ncov == L) { sol_len = depth; return 1; }
    if (budget < (long long)(L - ncov)) return 0;
    if (depth >= MAXD) return 0;
    uint64_t *c = cov[depth];
    int r = -1;
    for (int w = 0; w < NW; w++) {
        uint64_t t = ~c[w];
        if (w == NW - 1) t &= lastmask;
        if (t) { r = w * 64 + __builtin_ctzll(t); break; }
    }
    if (r < 0) { sol_len = depth; return 1; }
    uint64_t *s = scr[depth];
    uint64_t *nc = cov[depth + 1];
    for (int i = 0; i < ND; i++) {
        if (used[i]) continue;
        int a = r % ds[i];
        shl(s, base_[i], a);
        int ov = 0;
        for (int w = 0; w < NW; w++) ov += __builtin_popcountll(s[w] & c[w]);
        int nw = waste + ov;
        if (nw > wmax) continue;
        for (int w = 0; w < NW; w++) nc[w] = c[w] | s[w];
        used[i] = 1; sol_d[depth] = ds[i]; sol_a[depth] = a;
        int res = dfs(depth + 1, ncov + cnt[i] - ov, nw, wmax, budget - cnt[i]);
        used[i] = 0;
        if (res != 0) return res;
        nc = cov[depth + 1];   /* restore (unchanged, but be explicit) */
    }
    return 0;
}

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: %s L wmaxcap [nodecap] m1 m2 ...\n", argv[0]); return 1; }
    L = atoi(argv[1]);
    int wcap = atoi(argv[2]);
    nodecap = atoll(argv[3]);
    ND = argc - 4;
    for (int i = 0; i < ND; i++) { ds[i] = atoi(argv[i + 4]); cnt[i] = L / ds[i]; }
    NW = (L + 63) / 64;
    int rem = L & 63;
    lastmask = rem ? ((uint64_t)1 << rem) - 1 : ~(uint64_t)0;
    long long total = 0;
    for (int i = 0; i < ND; i++) total += cnt[i];
    MAXD = ND + 1;
    for (int i = 0; i < ND; i++) {
        base_[i] = calloc(NW, 8);
        for (int j = 0; j < L; j += ds[i]) base_[i][j >> 6] |= (uint64_t)1 << (j & 63);
    }
    cov = malloc((MAXD + 2) * sizeof(uint64_t *));
    scr = malloc((MAXD + 2) * sizeof(uint64_t *));
    for (int i = 0; i <= MAXD + 1; i++) { cov[i] = calloc(NW, 8); scr[i] = calloc(NW, 8); }
    if (total < L) { printf("BUDGET_INFEASIBLE total=%lld L=%d\n", total, L); return 0; }
    /* wcap < 0 means: run the SINGLE decision problem "waste <= -wcap ?" */
    int wstart = 0;
    if (wcap < 0) { wstart = -wcap; wcap = -wcap; }
    for (int wmax = wstart; wmax <= wcap; wmax++) {
        nodes = 0;
        memset(cov[0], 0, NW * 8);
        memset(used, 0, sizeof(int) * ND);
        int res = dfs(0, 0, 0, wmax, total);
        if (res == 1) {
            printf("X=%d nodes=%lld system=", wmax, nodes);
            for (int i = 0; i < sol_len; i++) printf("%d/%d ", sol_a[i], sol_d[i]);
            printf("\n");
            return 0;
        } else if (res == -1) {
            printf("ABORT_NODECAP wmax=%d nodes=%lld\n", wmax, nodes);
            return 2;
        }
        printf("  wmax=%d UNSAT nodes=%lld\n", wmax, nodes); fflush(stdout);
    }
    printf("NOSOL_UPTO %d\n", wcap);
    return 3;
}
