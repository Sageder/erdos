/* seqdfs.c — INDEPENDENT re-implementation of route R4's class "Bp"/"S":
 * injective SEQUENCES a(1..N) of distinct positive integers with
 *     a(i) <= floor(num*i/den)      for all i
 * and no monotone 4-term AP among their values (both orientations).
 *
 * WHY THIS CERTIFIES AN INFINITE THEOREM: if a : N -> N is a 4-AP-free
 * permutation with a(i) <= C*i for all i, then its POSITION PREFIX a(1..N) is
 * exactly such an object for every N.  So extinction at some N proves: no
 * 4-AP-free permutation of N satisfies a(i) <= C*i for all i.
 * (No compactness needed -- this is a direct restriction, unlike the value-side
 *  bound pos(v) <= C*v which needs CORE.md Lemma 6.)
 *
 * When w = a(i) is appended it occupies the LAST position, so it can only be
 *   - the largest term of an increasing 4-AP: need pos(w-3d)<pos(w-2d)<pos(w-d), or
 *   - the smallest term of a decreasing 4-AP: need pos(w+3d)<pos(w+2d)<pos(w+d).
 *
 * usage: ./seqdfs num den maxdepth [budget]
 */
#include <stdio.h>
#include <stdlib.h>

#define MAXV 4096

static int num, den, maxdepth, VMAX;
static long long budget = 200000000000LL, nodes = 0;
static long long levelcount[512], deadcount[512];
static int posv[MAXV + 8];      /* 0 = unused, else position (1-based) */

static void dfs(int i) /* a(1..i) already placed */
{
    nodes++;
    levelcount[i]++;
    if (i >= maxdepth) return;
    if (nodes > budget) { fprintf(stderr, "BUDGET EXCEEDED\n"); exit(2); }
    int i1 = i + 1;
    int hi = (int)(((long long)num * i1) / den);
    if (hi > VMAX) hi = VMAX;
    int any = 0;
    for (int w = 1; w <= hi; w++) {
        if (posv[w]) continue;
        int bad = 0;
        for (int d = 1; w - 3 * d >= 1; d++) {
            int p1 = posv[w - 3 * d], p2 = posv[w - 2 * d], p3 = posv[w - d];
            if (p1 && p2 && p3 && p1 < p2 && p2 < p3) { bad = 1; break; }
        }
        if (!bad) {
            for (int d = 1; w + 3 * d <= VMAX; d++) {
                int p1 = posv[w + 3 * d], p2 = posv[w + 2 * d], p3 = posv[w + d];
                if (p1 && p2 && p3 && p1 < p2 && p2 < p3) { bad = 1; break; }
            }
        }
        if (bad) continue;
        any = 1;
        posv[w] = i1;
        dfs(i1);
        posv[w] = 0;
    }
    if (!any) deadcount[i]++;
}

int main(int argc, char **argv)
{
    if (argc < 4) { fprintf(stderr, "usage: %s num den maxdepth [budget]\n", argv[0]); return 1; }
    num = atoi(argv[1]); den = atoi(argv[2]); maxdepth = atoi(argv[3]);
    if (argc > 4) budget = atoll(argv[4]);
    VMAX = (int)(((long long)num * maxdepth) / den) + 1;
    if (VMAX > MAXV) { fprintf(stderr, "VMAX too big\n"); return 1; }
    printf("== independent SEQUENCE DFS: k=4, a(i) <= floor(%d*i/%d), maxdepth=%d, VMAX=%d ==\n",
           num, den, maxdepth, VMAX);
    /* virtual root at i=0 */
    levelcount[0] = 1; nodes = 1;
    {
        int i1 = 1, hi = (int)(((long long)num * 1) / den);
        if (hi > VMAX) hi = VMAX;
        for (int w = 1; w <= hi; w++) { posv[w] = 1; dfs(1); posv[w] = 0; }
    }
    printf("i           count        dead\n");
    int extinct = -1;
    for (int i = 1; i <= maxdepth; i++) {
        printf("%-4d %15lld %11lld\n", i, levelcount[i], deadcount[i]);
        if (levelcount[i] == 0) { extinct = i; break; }
    }
    if (extinct > 0) printf("EXTINCT at i=%d\n", extinct);
    else printf("alive through i=%d\n", maxdepth);
    printf("total nodes visited: %lld\n", nodes);
    return 0;
}
