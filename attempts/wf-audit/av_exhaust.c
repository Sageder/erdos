/* av_exhaust.c -- Recon-3 independent exhaustive search.  Written from scratch;
 * shares no code with experiments/csearch*.c.
 *
 * Enumerates EVERY legal U subseteq [2,N] with sum_{n in U} 1/n = 1
 * (legal = no isolated point), in exact integer arithmetic over
 * L = lcm(2..N), weights w_n = L/n, target L.  unsigned __int128 only.
 *
 * Pruning (all necessary conditions, so the search stays exhaustive):
 *   P1  0 <= R  (we only subtract a weight when w_n <= R);
 *   P2  R <= suf[n] = sum_{m=2}^{n} w_m           (reachability);
 *   P3  D[n] | R  where D[n] = L / lcm(2..n)      (denominator condition:
 *       the remaining value is a sum of 1/m with m <= n, so its reduced
 *       denominator divides lcm(2..n); scaled by L this says D[n] | R).
 * Legality is enforced by carrying the length (capped at 2) of the run of
 * chosen elements ending at n+1.
 *
 * usage:  ./av_exhaust N
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef unsigned __int128 u128;

static int N;
static u128 L, w[512], suf[512], D[512];
static unsigned char pick[512];
static long long nodes = 0, nsol = 0;
static int minmax = 1 << 30;
static long long cnt_at_max[512];

static u128 ugcd(u128 a, u128 b) { while (b) { u128 t = a % b; a = b; b = t; } return a; }

static void print_u128(u128 x) {
    char buf[64]; int i = 0;
    if (!x) { printf("0"); return; }
    while (x) { buf[i++] = '0' + (int)(x % 10); x /= 10; }
    while (i--) putchar(buf[i]);
}

static void record(void) {
    int mx = 0, i;
    for (i = N; i >= 2; i--) if (pick[i]) { mx = i; break; }
    nsol++;
    if (mx < minmax) minmax = mx;
    cnt_at_max[mx]++;
    printf("SOL max=%d :", mx);
    for (i = 2; i <= N; i++) if (pick[i]) printf(" %d", i);
    printf("\n");
}

static void rec(int n, u128 R, int runlen) {
    nodes++;
    if (n < 2) { if (R == 0 && runlen != 1) record(); return; }
    if (R > suf[n]) return;
    if (R % D[n]) return;
    if (runlen != 1) { pick[n] = 0; rec(n - 1, R, 0); }
    if (w[n] <= R) {
        pick[n] = 1;
        rec(n - 1, R - w[n], runlen >= 2 ? 2 : runlen + 1);
        pick[n] = 0;
    }
}

int main(int argc, char **argv) {
    int n;
    N = (argc > 1) ? atoi(argv[1]) : 85;
    L = 1;
    for (n = 2; n <= N; n++) L = L / ugcd(L, (u128)n) * (u128)n;
    printf("N=%d  L=lcm(2..N)=", N); print_u128(L);
    { u128 t = L; int bits = 0; while (t) { bits++; t >>= 1; } printf("  (%d bits)\n", bits); }
    for (n = 2; n <= N; n++) w[n] = L / (u128)n;
    suf[1] = 0;
    for (n = 2; n <= N; n++) suf[n] = suf[n - 1] + w[n];
    /* D[n] = L / lcm(2..n) */
    { u128 lam = 1;
      D[1] = L;
      for (n = 2; n <= N; n++) { lam = lam / ugcd(lam, (u128)n) * (u128)n; D[n] = L / lam; } }
    /* sanity: sum of all weights must not have overflowed */
    if (suf[N] < w[2]) { printf("OVERFLOW in suffix sums\n"); return 1; }
    rec(N, L, 0);
    printf("nodes=%lld  solutions=%lld  min max(U)=%d\n", nodes, nsol,
           nsol ? minmax : -1);
    for (n = 2; n <= N; n++) if (cnt_at_max[n]) printf("  max(U)=%d : %lld solutions\n", n, cnt_at_max[n]);
    return 0;
}
