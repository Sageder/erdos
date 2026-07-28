/* av_exhaust_up.c -- second independent engine, ASCENDING order (different prune
 * structure from av_exhaust.c) used as a cross-check of the N<=85 result.
 *
 * Position n runs 2..N.  R = remaining scaled value.  Necessary conditions:
 *   P1  w_n <= R when picking;
 *   P2  R <= sufup[n] = sum_{m=n}^{N} w_m;
 *   P3  Dup[n] | R, Dup[n] = L / lcm(n..N)   (remaining value uses denominators in [n,N]);
 *   legality: carry length (capped 2) of the run ending at n-1; when leaving a run of
 *   length 1 we must not close it.
 * usage: ./av_exhaust_up N
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef unsigned __int128 u128;
static int N;
static u128 L, w[512], sufup[512], Dup[512];
static unsigned char pick[512];
static long long nodes = 0, nsol = 0;
static u128 ugcd(u128 a, u128 b) { while (b) { u128 t = a % b; a = b; b = t; } return a; }
static void record(void) {
    int i, mx = 0;
    for (i = N; i >= 2; i--) if (pick[i]) { mx = i; break; }
    nsol++;
    printf("SOL max=%d :", mx);
    for (i = 2; i <= N; i++) if (pick[i]) printf(" %d", i);
    printf("\n");
}
static void rec(int n, u128 R, int runlen) {
    nodes++;
    if (n > N) { if (R == 0 && runlen != 1) record(); return; }
    if (R > sufup[n]) return;
    if (R % Dup[n]) return;
    if (runlen != 1) { pick[n] = 0; rec(n + 1, R, 0); }
    if (w[n] <= R) { pick[n] = 1; rec(n + 1, R - w[n], runlen >= 2 ? 2 : runlen + 1); pick[n] = 0; }
}
int main(int argc, char **argv) {
    int n;
    N = (argc > 1) ? atoi(argv[1]) : 85;
    L = 1;
    for (n = 2; n <= N; n++) L = L / ugcd(L, (u128)n) * (u128)n;
    for (n = 2; n <= N; n++) w[n] = L / (u128)n;
    sufup[N + 1] = 0;
    for (n = N; n >= 2; n--) sufup[n] = sufup[n + 1] + w[n];
    { u128 lam; int m;
      for (n = 2; n <= N + 1; n++) {
          lam = 1;
          for (m = n; m <= N; m++) lam = lam / ugcd(lam, (u128)m) * (u128)m;
          Dup[n] = L / lam;
      } }
    rec(2, L, 0);
    printf("ASC N=%d nodes=%lld solutions=%lld\n", N, nodes, nsol);
    return 0;
}
