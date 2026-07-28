/* fast2.c — Route R4 strong engine: dynamic bound propagation + Hall lookahead.
 *
 * Same search space and semantics as fast.c / engine.py (see those headers), but the
 * AP constraints are PROPAGATED EARLY: when value w is placed at position p, for each
 * d>=1 with w-2d>=1 and w+d<=N, writing p1=pi(w-2d), p2=pi(w-d):
 *   p1<p2<p  (increasing triple w-2d,w-d,w)  => future value w+d must go at pos <= p-1
 *   p1>p2>p  (decreasing triple)             => future value w+d must go at pos >= p+1
 * These tighten dynamic bounds dynlo/dynhi of the future value w+d (trail-undone on
 * backtrack).  Since every monotone-triple constraint on v is created when v-d is placed,
 * at placement time of v the interval [dynlo[v], dynhi[v]] already contains ALL AP
 * constraints — equivalent to fast.c's recomputation, provably the same search tree
 * modulo extra pruning:
 *   - immediate fail if some future value's interval empties,
 *   - Hall lookahead: for k=1..K, with M_k = max_{j<=k} dynhi[v+j], require
 *     (#free positions <= M_k) >= k; symmetric fillability check for lower bounds.
 * All pruning conditions are necessary conditions, so exhaustive results are unchanged.
 *
 * usage: ./fast2 N cls num den mode cap maxprint [order seed]  (same CLI as fast.c)
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MAXN 4100
#define MAXTRAIL (1 << 22)

static int N, num, den;
static char cls, mode;
static long long cap = 0, nodes = 0, cnt = 0;
static int exhaustive = 1;
static int dynlo[MAXN], dynhi[MAXN];
static int posv[MAXN];
static unsigned char used[MAXN];
static long long maxprint = 0, printed = 0;
static int have_example = 0;
static int example[MAXN];
static int K = 16;
static int order_mode = 0;
static char round_mode = 'f';   /* f: hi=floor(Cv) (R4 convention); c: hi=ceil(Cv) (sat_order.py "plain profile") */
static unsigned long long rngstate = 88172645463325252ULL;

/* trail for dyn bound changes: packed records (is_hi, w, old) */
static int trail_w[MAXTRAIL]; static int trail_old[MAXTRAIL]; static unsigned char trail_hi[MAXTRAIL];
static int trail_top = 0;

static int fen[MAXN];
static void fen_add(int i, int d) { for (; i <= N; i += i & (-i)) fen[i] += d; }
static int fen_sum(int i) { int s = 0; for (; i > 0; i -= i & (-i)) s += fen[i]; return s; }
static int free_le(int t) { if (t <= 0) return 0; if (t > N) t = N; return t - fen_sum(t); }

static int nxt[MAXN], prv[MAXN];
static void ll_remove(int p) { nxt[prv[p]] = nxt[p]; prv[nxt[p]] = prv[p]; }
static void ll_restore(int p) { nxt[prv[p]] = p; prv[nxt[p]] = p; }

static unsigned long long xrand(void) {
    rngstate ^= rngstate << 13; rngstate ^= rngstate >> 7; rngstate ^= rngstate << 17;
    return rngstate;
}

static void emit(void) {
    int perm[MAXN];
    for (int w = 1; w <= N; w++) perm[posv[w] - 1] = w;
    if (!have_example) { memcpy(example, perm, sizeof(int) * N); have_example = 1; }
    if (printed < maxprint) {
        printf("AVOIDER");
        for (int i = 0; i < N; i++) printf(" %d", perm[i]);
        printf("\n");
        printed++;
    }
}

static int rec(int v) {
    if (v > N) { cnt++; emit(); return mode == 'e'; }
    if (cap && nodes > cap) { exhaustive = 0; return 1; }
    int L = dynlo[v], U = dynhi[v];
    if (L > U) return 0;
    int cand[MAXN]; int nc = 0;
    for (int p = L; p <= U; p++) if (!used[p]) cand[nc++] = p;
    if (order_mode == 1) { for (int i = 0; i < nc / 2; i++) { int t = cand[i]; cand[i] = cand[nc-1-i]; cand[nc-1-i] = t; } }
    else if (order_mode == 2) { for (int i = nc - 1; i > 0; i--) { int j = (int)(xrand() % (unsigned)(i + 1)); int t = cand[i]; cand[i] = cand[j]; cand[j] = t; } }
    for (int ci = 0; ci < nc; ci++) {
        int p = cand[ci];
        used[p] = 1; posv[v] = p; fen_add(p, 1); ll_remove(p);
        nodes++;
        int save_trail = trail_top;
        int ok = 1;
        /* propagate: triples (v-2d, v-d, v) -> bound on v+d */
        int dmax = (v - 1) / 2; if (dmax > N - v) dmax = N - v;
        for (int d = 1; d <= dmax; d++) {
            int p1 = posv[v - 2 * d], p2 = posv[v - d];
            if (p1 < p2) {
                if (p2 < p && p - 1 < dynhi[v + d]) {
                    trail_w[trail_top] = v + d; trail_old[trail_top] = dynhi[v + d]; trail_hi[trail_top++] = 1;
                    dynhi[v + d] = p - 1;
                    if (dynlo[v + d] > p - 1) { ok = 0; break; }
                }
            } else {
                if (p2 > p && p + 1 > dynlo[v + d]) {
                    trail_w[trail_top] = v + d; trail_old[trail_top] = dynlo[v + d]; trail_hi[trail_top++] = 0;
                    dynlo[v + d] = p + 1;
                    if (dynhi[v + d] < p + 1) { ok = 0; break; }
                }
            }
        }
        if (ok) {                                   /* Hall deadline lookahead */
            int mx = 0;
            for (int k = 1; k <= K && v + k <= N; k++) {
                int h = dynhi[v + k]; if (h > mx) mx = h;
                if (free_le(mx) < k) { ok = 0; break; }
            }
        }
        if (ok && (cls == 'B' || cls == 'C')) {      /* fillability lookahead */
            int q = nxt[0], k = 1;
            while (k <= K && q != N + 1) {
                long long hifill = (round_mode == 'c') ? ((long long)q * num + den - 1) / den
                                                       : (long long)q * num / den;
                if (hifill - v < k) { ok = 0; break; }
                q = nxt[q]; k++;
            }
        }
        if (ok && rec(v + 1)) {
            while (trail_top > save_trail) { trail_top--; if (trail_hi[trail_top]) dynhi[trail_w[trail_top]] = trail_old[trail_top]; else dynlo[trail_w[trail_top]] = trail_old[trail_top]; }
            used[p] = 0; fen_add(p, -1); ll_restore(p);
            return 1;
        }
        while (trail_top > save_trail) { trail_top--; if (trail_hi[trail_top]) dynhi[trail_w[trail_top]] = trail_old[trail_top]; else dynlo[trail_w[trail_top]] = trail_old[trail_top]; }
        used[p] = 0; fen_add(p, -1); ll_restore(p);
    }
    return 0;
}

int main(int argc, char **argv) {
    if (argc < 8) { fprintf(stderr, "usage: fast2 N cls num den mode cap maxprint [order seed]\n"); return 2; }
    N = atoi(argv[1]); cls = argv[2][0]; num = atoi(argv[3]); den = atoi(argv[4]);
    mode = argv[5][0]; cap = atoll(argv[6]); maxprint = atoll(argv[7]);
    if (argc >= 9) order_mode = atoi(argv[8]);
    if (argc >= 10) rngstate = strtoull(argv[9], NULL, 10) * 2654435761ULL + 1442695040888963407ULL;
    if (argc >= 11) round_mode = argv[10][0];
    if (N + 2 >= MAXN) { fprintf(stderr, "N too large\n"); return 2; }
    for (int v = 1; v <= N; v++) {
        dynlo[v] = 1; dynhi[v] = N;
        if (cls == 'A' || cls == 'C') {
            long long h = (round_mode == 'c') ? ((long long)num * v + den - 1) / den
                                              : (long long)num * v / den;
            if (h < N) dynhi[v] = (int)h;
        }
        if (cls == 'B' || cls == 'C') {
            /* round f: a(i) <= floor(Ci)  => lo(v) = ceil(v*den/num)
               round c: a(i) <= ceil(Ci)   => lo(v) = floor(den*(v-1)/num) + 1 */
            dynlo[v] = (round_mode == 'c') ? (int)((long long)den * (v - 1) / num + 1)
                                           : (int)(((long long)v * den + num - 1) / num);
        }
        if (cls == 'D' && v <= N / 2 && 2 * v < N) dynhi[v] = 2 * v;
    }
    for (int p = 0; p <= N + 1; p++) { nxt[p] = p + 1; prv[p] = p - 1; }
    rec(1);
    printf("RESULT N=%d cls=%c C=%d/%d mode=%c count=%lld nodes=%lld exhaustive=%d", N, cls, num, den, mode, cnt, nodes, exhaustive);
    if (have_example) {
        printf(" example=");
        for (int i = 0; i < N; i++) printf(i ? ",%d" : "%d", example[i]);
    }
    printf("\n");
    return 0;
}
