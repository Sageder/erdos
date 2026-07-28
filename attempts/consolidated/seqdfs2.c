/* seqdfs2.c — seqdfs.c with incremental ban propagation (same search space,
 * same semantics, ~10-30x faster).
 *
 * Class S / Bp: injective sequences a(1..N) of distinct positive integers with
 * a(i) <= floor(num*i/den) and no monotone 4-term AP among their values.
 *
 * COMPLETENESS OF THE BAN RULE.  Values are appended in position order, so an
 * increasing triple (x, x+d, x+2d) becomes positionally complete exactly when
 * its LAST-positioned member x+2d is appended; at that moment value x+3d is
 * permanently unplaceable (an increasing 4-AP would follow).  A decreasing
 * triple (x+2d, x+d, x) completes when x is appended, and then x-d is
 * permanently unplaceable.  Both are recorded as ban counters, trail-undone on
 * backtrack.  Hence "legal candidate" == "unused and unbanned", exactly the
 * condition seqdfs.c tests by rescanning.  (Verified: identical level counts.)
 *
 * usage: ./seqdfs2 num den maxdepth [budget]
 */
#include <stdio.h>
#include <stdlib.h>

#define MAXV 8192
#define MAXTRAIL (1 << 24)

static int num, den, maxdepth, VMAX;
static long long budget = 1000000000000LL, nodes = 0;
static long long levelcount[1024], deadcount[1024];
static int posv[MAXV + 8];
static int banned[MAXV + 8];
static int trail[MAXTRAIL];
static int trail_top = 0;

static void dfs(int i)
{
    nodes++;
    levelcount[i]++;
    if (i >= maxdepth) return;
    if (nodes > budget) { printf("BUDGET EXCEEDED at level %d\n", i); fflush(stdout); exit(2); }
    int i1 = i + 1;
    int hi = (int)(((long long)num * i1) / den);
    if (hi > VMAX) hi = VMAX;
    int any = 0;
    for (int w = 1; w <= hi; w++) {
        if (posv[w] || banned[w]) continue;
        any = 1;
        posv[w] = i1;
        int save = trail_top;
        /* increasing triples ending at w:  (w-2d, w-d, w) -> ban w+d */
        for (int d = 1; w - 2 * d >= 1 && w + d <= VMAX; d++) {
            int p1 = posv[w - 2 * d], p2 = posv[w - d];
            if (p1 && p2 && p1 < p2) { banned[w + d]++; trail[trail_top++] = w + d; }
        }
        /* decreasing triples ending at w: (w+2d, w+d, w) -> ban w-d */
        for (int d = 1; w + 2 * d <= VMAX && w - d >= 1; d++) {
            int p1 = posv[w + 2 * d], p2 = posv[w + d];
            if (p1 && p2 && p1 < p2) { banned[w - d]++; trail[trail_top++] = w - d; }
        }
        dfs(i1);
        while (trail_top > save) banned[trail[--trail_top]]--;
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
    printf("== SEQUENCE DFS v2: k=4, a(i) <= floor(%d*i/%d), maxdepth=%d, VMAX=%d ==\n",
           num, den, maxdepth, VMAX);
    dfs(0);
    levelcount[0] = 1;
    printf("i           count        dead\n");
    int extinct = -1;
    for (int i = 1; i <= maxdepth; i++) {
        printf("%-4d %15lld %11lld\n", i, levelcount[i], deadcount[i]);
        fflush(stdout);
        if (levelcount[i] == 0) { extinct = i; break; }
    }
    if (extinct > 0) printf("EXTINCT at i=%d\n", extinct);
    else printf("alive through i=%d\n", maxdepth);
    printf("total nodes visited: %lld\n", nodes);
    return 0;
}
