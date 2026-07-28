/* tamedfs.c — INDEPENDENT re-implementation of route R9's "tame" complete DFS.
 *
 * Enumerates ALL permutations sigma of [1..N] with no monotone 4-term AP
 * (both orientations) subject to pos(v) <= floor(num*v/den) for all v, by
 * inserting values 1,2,...,N in increasing order (CORE.md Lemma 8 interval
 * theorem: children form a contiguous interval).
 *
 * Validity of level-wise pruning: positions only increase as larger values are
 * inserted, so a profile-bounded avoider of [1..N] restricts to a
 * profile-bounded avoider of [1..n] for every n <= N (CORE.md Lemma 6).
 *
 * Usage: ./tamedfs num den maxdepth [budget]
 * Prints per-level node counts and the extinction level.
 *
 * Independent of route-R9/census.c (written from the mathematical spec).
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXN 128

static int num, den, maxdepth;
static long long budget = 200000000000LL;
static long long levelcount[MAXN + 2];
static long long deadcount[MAXN + 2];
static long long nodes = 0;
static int phi[MAXN + 2];

/* arr[j] = value at rank j (0-indexed);  posv[v] = rank of value v */
static int arr[MAXN + 2];
static int posv[MAXN + 2];
static int slack[MAXN + 2]; /* slack[j] = phi[arr[j]] - (j+1) >= 0 */

static void dfs(int n) /* current node holds values 1..n */
{
    nodes++;
    levelcount[n]++;
    if (n >= maxdepth) return;
    if (nodes > budget) { fprintf(stderr, "BUDGET EXCEEDED\n"); exit(2); }

    int m = n + 1;

    /* 4-AP interval (Lemma 8), in insertion-rank coordinates */
    int lo = 0, hi = n; /* rank r in [lo,hi] */
    for (int d = 1; m - 3 * d >= 1; d++) {
        int p1 = posv[m - 3 * d], p2 = posv[m - 2 * d], p3 = posv[m - d];
        if (p1 < p2 && p2 < p3) {         /* inc-step: m must precede m-d  => r <= p3 */
            if (p3 < hi) hi = p3;
        } else if (p1 > p2 && p2 > p3) {  /* dec-step: m must follow m-d   => r >= p3+1 */
            if (p3 + 1 > lo) lo = p3 + 1;
        }
    }
    /* displacement of m itself: pos(m) = r+1 <= phi[m] */
    if (phi[m] - 1 < hi) hi = phi[m] - 1;
    /* displacement of the incumbents: every j >= r shifts up by one, needs slack>=1 */
    for (int j = n - 1; j >= 0; j--) {
        if (slack[j] == 0) { if (j + 1 > lo) lo = j + 1; break; }
    }

    int any = 0;
    for (int r = lo; r <= hi; r++) {
        any = 1;
        /* insert */
        memmove(arr + r + 1, arr + r, (size_t)(n - r) * sizeof(int));
        arr[r] = m;
        for (int j = r; j <= n; j++) { posv[arr[j]] = j; slack[j] = phi[arr[j]] - (j + 1); }
        dfs(n + 1);
        /* undo */
        memmove(arr + r, arr + r + 1, (size_t)(n - r) * sizeof(int));
        for (int j = r; j < n; j++) { posv[arr[j]] = j; slack[j] = phi[arr[j]] - (j + 1); }
    }
    if (!any) deadcount[n]++;
}

int main(int argc, char **argv)
{
    if (argc < 4) { fprintf(stderr, "usage: %s num den maxdepth [budget]\n", argv[0]); return 1; }
    num = atoi(argv[1]); den = atoi(argv[2]); maxdepth = atoi(argv[3]);
    if (argc > 4) budget = atoll(argv[4]);
    if (maxdepth > MAXN) maxdepth = MAXN;
    for (int v = 1; v <= maxdepth + 1; v++) phi[v] = (int)(((long long)num * v) / den);

    printf("== independent tame DFS: k=4, pos(v) <= floor(%d*v/%d), maxdepth=%d ==\n",
           num, den, maxdepth);
    if (phi[1] < 1) { printf("EXTINCT at n=1 (phi(1)<1)\n"); return 0; }
    arr[0] = 1; posv[1] = 0; slack[0] = phi[1] - 1;
    dfs(1);

    printf("n           count        dead\n");
    int extinct = -1;
    for (int n = 1; n <= maxdepth; n++) {
        printf("%-4d %15lld %11lld\n", n, levelcount[n], deadcount[n]);
        if (levelcount[n] == 0) { extinct = n; break; }
    }
    if (extinct > 0) printf("EXTINCT at n=%d\n", extinct);
    else printf("alive through n=%d (no extinction within maxdepth)\n", maxdepth);
    printf("total nodes visited: %lld\n", nodes);
    return 0;
}
