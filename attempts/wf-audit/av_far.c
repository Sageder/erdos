/* av_far.c -- Recon-3 independent search for a SOLUTION WITH ALL ELEMENTS >= T
 * (a direct empirical test of CRUX).  Reads a pruned universe (sorted ascending)
 * from stdin: first line m, second line the m values.
 *
 * Exact integer arithmetic over L = lcm(universe), target L, weights L/v.
 * unsigned __int128 only; aborts if lcm exceeds 127 bits.
 *
 * Descending DFS with:
 *   P1 0 <= R;  P2 R <= suf[i];  P3 D[i] | R with D[i] = L / lcm(v_0..v_i);
 *   legality carried as the length (capped 2) of the run of chosen elements
 *   ending at v[i]+1.
 *
 * usage: ./av_far [maxsol] < universe.txt
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef unsigned __int128 u128;

static int m, v[4096];
static u128 L, w[4096], suf[4096], D[4096];
static unsigned char pick[4096];
static long long nodes = 0, nsol = 0, maxsol = 5;

static u128 ugcd(u128 a, u128 b) { while (b) { u128 t = a % b; a = b; b = t; } return a; }
static void pr128(u128 x) { char b[64]; int i = 0; if (!x) { printf("0"); return; }
    while (x) { b[i++] = '0' + (int)(x % 10); x /= 10; } while (i--) putchar(b[i]); }

static void record(void) {
    int i; nsol++;
    printf("SOL");
    for (i = 0; i < m; i++) if (pick[i]) printf(" %d", v[i]);
    printf("\n"); fflush(stdout);
}

/* runlen = length (capped 2) of the run of chosen elements ending at v[i]+1,
 * 0 if v[i]+1 is not chosen / not adjacent. */
static void rec(int i, u128 R, int runlen) {
    nodes++;
    if (i < 0) { if (R == 0 && runlen != 1) record(); return; }
    if (R > suf[i]) return;
    if (R % D[i]) return;
    int below = (i > 0 && v[i - 1] == v[i] - 1);
    if (runlen == 1) {                    /* v[i] is forced */
        if (w[i] > R) return;
        pick[i] = 1;
        rec(i - 1, R - w[i], below ? 2 : 0);
        pick[i] = 0;
        return;
    }
    /* skip v[i] */
    rec(i - 1, R, 0);
    if (nsol >= maxsol) return;
    /* take v[i] */
    if (w[i] <= R) {
        int len = (runlen == 0) ? 1 : 2;   /* length of the run containing v[i] */
        pick[i] = 1;
        if (below) rec(i - 1, R - w[i], len);
        else if (len >= 2) rec(i - 1, R - w[i], 0);
        /* len==1 and no lower neighbour: isolated point, dead */
        pick[i] = 0;
    }
}

int main(int argc, char **argv) {
    int i;
    if (argc > 1) maxsol = atoll(argv[1]);
    if (scanf("%d", &m) != 1) return 1;
    for (i = 0; i < m; i++) if (scanf("%d", &v[i]) != 1) return 1;
    L = 1;
    for (i = 0; i < m; i++) L = L / ugcd(L, (u128)v[i]) * (u128)v[i];
    { u128 t = L; int bits = 0; while (t) { bits++; t >>= 1; }
      printf("m=%d L=", m); pr128(L); printf(" (%d bits)\n", bits);
      if (bits > 120) { printf("LCM TOO BIG\n"); return 2; } }
    for (i = 0; i < m; i++) w[i] = L / (u128)v[i];
    suf[0] = w[0];
    for (i = 1; i < m; i++) suf[i] = suf[i - 1] + w[i];
    { u128 lam = 1;
      for (i = 0; i < m; i++) { lam = lam / ugcd(lam, (u128)v[i]) * (u128)v[i]; D[i] = L / lam; } }
    if (suf[m - 1] < L) { printf("universe cannot reach 1 (sum < 1)\n"); return 0; }
    rec(m - 1, L, 0);
    printf("nodes=%lld solutions=%lld\n", nodes, nsol);
    return 0;
}
