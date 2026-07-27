/* fastseq.c — class Bp: injective sequences a(1..N), a(i) <= C*i, no monotone 4-AP.
 *
 * This is the exact finite object inherited by every position-prefix of an infinite
 * permutation (or injective sequence) satisfying a(i) <= C*i.  Existence is monotone
 * decreasing in N (prefixes), so a single exhaustive extinction at N is a certificate:
 * "no injective sequence of length N with a(i) <= C*i is monotone-4-AP-free", hence no
 * infinite permutation of N with a(i) <= C*i for all i avoids monotone 4-APs.
 *
 * Search by positions i=1..N.  Appending value w at the (current) last position can
 * only create a monotone 4-AP in which w is the LAST-position element, i.e. w is the
 * top of an increasing AP (need pi(w-3d)<pi(w-2d)<pi(w-d), all present) or the bottom
 * of a decreasing AP (need pi(w+3d)<pi(w+2d)<pi(w+d), all present).  Every monotone
 * 4-AP among placed values is caught when its last-position element is appended, so the
 * search is exact and complete (mirrors engine.search_seq_Bp, validated vs brute force).
 *
 * usage: ./fastseq N num den mode cap maxprint [order seed]
 *   order 0: ascending candidate values; 1: descending; 2: shuffled(seed)
 * output: RESULT N=%d cls=S C=%d/%d ... example=a(1),...,a(N)
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MAXN 2100
#define MAXV (8 * MAXN)

static int N, num, den, maxval;
static char mode;
static long long cap = 0, nodes = 0, cnt = 0;
static int exhaustive = 1;
static int posv[MAXV];               /* posv[w] = position of value w, 0 = absent */
static int seq[MAXN];
static long long maxprint = 0, printed = 0;
static int have_example = 0;
static int example[MAXN];
static int order_mode = 0;
static unsigned long long rngstate = 88172645463325252ULL;

static unsigned long long xrand(void) {
    rngstate ^= rngstate << 13; rngstate ^= rngstate >> 7; rngstate ^= rngstate << 17;
    return rngstate;
}

static void emit(void) {
    if (!have_example) { memcpy(example, seq, sizeof(int) * N); have_example = 1; }
    if (printed < maxprint) {
        printf("AVOIDER");
        for (int i = 0; i < N; i++) printf(" %d", seq[i]);
        printf("\n");
        printed++;
    }
}

static int safe(int w) {
    for (int d = 1; w - 3 * d >= 1; d++) {
        int p1 = posv[w - 3 * d];
        if (!p1) continue;
        int p2 = posv[w - 2 * d];
        if (!p2 || p2 <= p1) continue;
        int p3 = posv[w - d];
        if (p3 > p2) return 0;
    }
    for (int d = 1; w + 3 * d <= maxval; d++) {
        int p1 = posv[w + 3 * d];
        if (!p1) continue;
        int p2 = posv[w + 2 * d];
        if (!p2 || p2 <= p1) continue;
        int p3 = posv[w + d];
        if (p3 > p2) return 0;
    }
    return 1;
}

static int rec(int i) {
    if (i > N) { cnt++; emit(); return mode == 'e'; }
    if (cap && nodes > cap) { exhaustive = 0; return 1; }
    int top = (int)((long long)num * i / den);
    if (top > maxval) top = maxval;
    static int candbuf[64][MAXV / 4];
    int *cand = (i < 64) ? candbuf[i] : NULL;
    /* candidate order */
    if (order_mode == 0) {
        for (int w = 1; w <= top; w++) {
            if (posv[w] || !safe(w)) continue;
            posv[w] = i; seq[i - 1] = w; nodes++;
            if (rec(i + 1)) { posv[w] = 0; return 1; }
            posv[w] = 0;
        }
    } else if (order_mode == 1) {
        for (int w = top; w >= 1; w--) {
            if (posv[w] || !safe(w)) continue;
            posv[w] = i; seq[i - 1] = w; nodes++;
            if (rec(i + 1)) { posv[w] = 0; return 1; }
            posv[w] = 0;
        }
    } else {
        int nc = 0;
        int *c = cand ? cand : malloc(sizeof(int) * (top + 1));
        for (int w = 1; w <= top; w++) if (!posv[w]) c[nc++] = w;
        for (int j = nc - 1; j > 0; j--) { int k = (int)(xrand() % (unsigned)(j + 1)); int t = c[j]; c[j] = c[k]; c[k] = t; }
        for (int j = 0; j < nc; j++) {
            int w = c[j];
            if (!safe(w)) continue;
            posv[w] = i; seq[i - 1] = w; nodes++;
            if (rec(i + 1)) { posv[w] = 0; if (!cand) free(c); return 1; }
            posv[w] = 0;
        }
        if (!cand) free(c);
    }
    return 0;
}

int main(int argc, char **argv) {
    if (argc < 7) { fprintf(stderr, "usage: fastseq N num den mode cap maxprint [order seed]\n"); return 2; }
    N = atoi(argv[1]); num = atoi(argv[2]); den = atoi(argv[3]);
    mode = argv[4][0]; cap = atoll(argv[5]); maxprint = atoll(argv[6]);
    if (argc >= 8) order_mode = atoi(argv[7]);
    if (argc >= 9) rngstate = strtoull(argv[8], NULL, 10) * 2654435761ULL + 1442695040888963407ULL;
    if (N + 2 >= MAXN) { fprintf(stderr, "N too large\n"); return 2; }
    maxval = (int)((long long)num * N / den);
    if (maxval + 4 >= MAXV) { fprintf(stderr, "maxval too large\n"); return 2; }
    rec(1);
    printf("RESULT N=%d cls=S C=%d/%d mode=%c count=%lld nodes=%lld exhaustive=%d", N, num, den, mode, cnt, nodes, exhaustive);
    if (have_example) {
        printf(" example=");
        for (int i = 0; i < N; i++) printf(i ? ",%d" : "%d", example[i]);
    }
    printf("\n");
    return 0;
}
