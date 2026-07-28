/* tamedfs_k.c — same as tamedfs.c but for general AP length k >= 3.
 *
 * Enumerates all permutations of [1..N] with no monotone k-term AP subject to
 * pos(v) <= floor(num*v/den), by inserting values in increasing order.
 * When the maximum value m is inserted, a monotone k-AP with largest term m is
 * (m-(k-1)d, ..., m-d, m); it is increasing iff the first k-1 terms are
 * positionally increasing and m comes after m-d, decreasing iff the first k-1
 * are positionally decreasing and m comes before m-d.  Children therefore form
 * a contiguous rank interval (generalised CORE.md Lemma 8).
 *
 * PURPOSE: calibrate the k=4 extinction law N*(C) against k=5, where an infinite
 * avoider IS known (CORE.md Theorem 21 / route R2 "Construction A", which has
 * sup_v pos(v)/v = 4).  So N*_5(C) must be +infinity for C >= 4.
 *
 * usage: ./tamedfs_k k num den maxdepth [budget]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXN 256

static int K, num, den, maxdepth;
static long long budget = 200000000000LL;
static long long levelcount[MAXN + 2];
static long long nodes = 0;
static int phi[MAXN + 2];
static int arr[MAXN + 2], posv[MAXN + 2], slack[MAXN + 2];

static void dfs(int n)
{
    nodes++;
    levelcount[n]++;
    if (n >= maxdepth) return;
    if (nodes > budget) { printf("BUDGET EXCEEDED at level %d\n", n); fflush(stdout); exit(2); }

    int m = n + 1;
    int lo = 0, hi = n;
    for (int d = 1; m - (K - 1) * d >= 1; d++) {
        int inc = 1, dec = 1;
        int prev = posv[m - (K - 1) * d];
        for (int j = K - 2; j >= 1; j--) {
            int cur = posv[m - j * d];
            if (!(prev < cur)) inc = 0;
            if (!(prev > cur)) dec = 0;
            prev = cur;
        }
        int p_last = posv[m - d];
        if (inc) { if (p_last < hi) hi = p_last; }        /* m must precede m-d */
        else if (dec) { if (p_last + 1 > lo) lo = p_last + 1; }
    }
    if (phi[m] - 1 < hi) hi = phi[m] - 1;
    for (int j = n - 1; j >= 0; j--)
        if (slack[j] == 0) { if (j + 1 > lo) lo = j + 1; break; }

    for (int r = lo; r <= hi; r++) {
        memmove(arr + r + 1, arr + r, (size_t)(n - r) * sizeof(int));
        arr[r] = m;
        for (int j = r; j <= n; j++) { posv[arr[j]] = j; slack[j] = phi[arr[j]] - (j + 1); }
        dfs(n + 1);
        memmove(arr + r, arr + r + 1, (size_t)(n - r) * sizeof(int));
        for (int j = r; j < n; j++) { posv[arr[j]] = j; slack[j] = phi[arr[j]] - (j + 1); }
    }
}

int main(int argc, char **argv)
{
    if (argc < 5) { fprintf(stderr, "usage: %s k num den maxdepth [budget]\n", argv[0]); return 1; }
    K = atoi(argv[1]); num = atoi(argv[2]); den = atoi(argv[3]); maxdepth = atoi(argv[4]);
    if (argc > 5) budget = atoll(argv[5]);
    if (maxdepth > MAXN) maxdepth = MAXN;
    for (int v = 1; v <= maxdepth + 1; v++) {
        long long t = ((long long)num * v) / den;
        phi[v] = (t > MAXN) ? MAXN : (int)t;
    }
    if (phi[1] < 1) { printf("k=%d C=%d/%d: EXTINCT at n=1\n", K, num, den); return 0; }
    arr[0] = 1; posv[1] = 0; slack[0] = phi[1] - 1;
    dfs(1);
    int extinct = -1, alive = 0;
    for (int n = 1; n <= maxdepth; n++) {
        if (levelcount[n] == 0) { extinct = n; break; }
        alive = n;
    }
    if (extinct > 0)
        printf("k=%d C=%d/%d (%.4f): EXTINCT at n=%d (alive through %d), nodes=%lld\n",
               K, num, den, (double)num / den, extinct, alive, nodes);
    else
        printf("k=%d C=%d/%d (%.4f): ALIVE through n=%d (no extinction <= maxdepth), nodes=%lld\n",
               K, num, den, (double)num / den, alive, nodes);
    return 0;
}
