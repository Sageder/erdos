/* fast.c — Route R4 fast backtracking engine (C port of engine.py semantics).
 *
 * Search for monotone-4-AP-free permutations of [1..N] under displacement constraints.
 * Classes (C = num/den exact rational):
 *   A : pi(v) <= floor(C*v)
 *   B : a(i) <= C*i  <=>  pi(v) >= ceil(v/C)
 *   C : both
 *   D : pi(v) <= 2v for v <= N/2
 * Values are placed in increasing order v=1..N; when placing v the AP-safety region is an
 * interval [L,U]: for each d with v-3d>=1, if pi(v-3d)<pi(v-2d)<pi(v-d) then p<=pi(v-d)-1,
 * if pi(v-3d)>pi(v-2d)>pi(v-d) then p>=pi(v-d)+1.  (See engine.py docstring for the proof
 * that every monotone 4-AP is caught exactly when its largest element is placed.)
 *
 * Pruning (necessary conditions only — completeness preserved):
 *   - Hall lookahead on deadlines (classes A,C,D): for k=1..K, free positions <= hi(v+k)
 *     must be >= k.
 *   - Hall lookahead on fillability (classes B,C): the k-th smallest free position p_k
 *     must satisfy floor(C*p_k) - v >= k (else p_k can never be filled).
 *
 * usage: ./fast N cls num den mode cap maxprint [order seed]
 *   mode: e = exists (stop at first avoider), c = count all
 *   cap:  node cap (0 = none); if hit, exhaustive=0 in output
 *   maxprint: print up to this many avoiders as lines "AVOIDER p1 p2 ... pN" (a(1)..a(N))
 *   order: 0 ascending positions (default), 1 descending, 2 shuffled with seed
 * output last line: RESULT N=%d cls=%c C=%d/%d mode=%c count=%lld nodes=%lld exhaustive=%d
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MAXN 4100

static int N, num, den;
static char cls, mode;
static long long cap = 0, nodes = 0, cnt = 0;
static int exhaustive = 1;
static int lo[MAXN], hi[MAXN];
static int posv[MAXN];               /* posv[v] = position of value v */
static unsigned char used[MAXN];
static long long maxprint = 0, printed = 0;
static int have_example = 0;
static int example[MAXN];
static int K = 12;
static int order_mode = 0;
static unsigned long long rngstate = 88172645463325252ULL;

/* Fenwick over used positions */
static int fen[MAXN];
static void fen_add(int i, int d) { for (; i <= N; i += i & (-i)) fen[i] += d; }
static int fen_sum(int i) { int s = 0; if (i > N) i = N; for (; i > 0; i -= i & (-i)) s += fen[i]; return s; }
static int free_le(int t) { if (t <= 0) return 0; if (t > N) t = N; return t - fen_sum(t); }

/* doubly linked list of free positions: nxt[0] = first free, sentinel N+1 */
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
    int L = lo[v], U = hi[v];
    int dm = (v - 1) / 3;
    for (int d = 1; d <= dm; d++) {
        int p1 = posv[v - 3 * d], p2 = posv[v - 2 * d], p3 = posv[v - d];
        if (p1 < p2) {
            if (p2 < p3 && p3 - 1 < U) { U = p3 - 1; if (L > U) return 0; }
        } else {
            if (p2 > p3 && p3 + 1 > L) { L = p3 + 1; if (L > U) return 0; }
        }
    }
    int cand[MAXN]; int nc = 0;
    for (int p = L; p <= U; p++) if (!used[p]) cand[nc++] = p;
    if (order_mode == 1) { for (int i = 0; i < nc / 2; i++) { int t = cand[i]; cand[i] = cand[nc - 1 - i]; cand[nc - 1 - i] = t; } }
    else if (order_mode == 2) { for (int i = nc - 1; i > 0; i--) { int j = (int)(xrand() % (unsigned)(i + 1)); int t = cand[i]; cand[i] = cand[j]; cand[j] = t; } }
    for (int ci = 0; ci < nc; ci++) {
        int p = cand[ci];
        used[p] = 1; posv[v] = p; fen_add(p, 1); ll_remove(p);
        nodes++;
        int ok = 1;
        if (cls == 'A' || cls == 'C' || cls == 'D') {           /* deadline Hall */
            for (int k = 1; k <= K && v + k <= N; k++) {
                if (free_le(hi[v + k]) < k) { ok = 0; break; }
            }
        }
        if (ok && (cls == 'B' || cls == 'C')) {                  /* fillability Hall */
            int p1 = nxt[0], k = 1;
            while (k <= K && p1 != N + 1) {
                if ((long long)p1 * num / den - v < k) { ok = 0; break; }
                p1 = nxt[p1]; k++;
            }
        }
        if (ok && rec(v + 1)) {
            used[p] = 0; fen_add(p, -1); ll_restore(p);
            return 1;
        }
        used[p] = 0; fen_add(p, -1); ll_restore(p);
    }
    return 0;
}

int main(int argc, char **argv) {
    if (argc < 8) { fprintf(stderr, "usage: fast N cls num den mode cap maxprint [order seed]\n"); return 2; }
    N = atoi(argv[1]); cls = argv[2][0]; num = atoi(argv[3]); den = atoi(argv[4]);
    mode = argv[5][0]; cap = atoll(argv[6]); maxprint = atoll(argv[7]);
    if (argc >= 9) order_mode = atoi(argv[8]);
    if (argc >= 10) rngstate = strtoull(argv[9], NULL, 10) * 2654435761ULL + 1442695040888963407ULL;
    if (N + 2 >= MAXN) { fprintf(stderr, "N too large\n"); return 2; }
    for (int v = 1; v <= N; v++) {
        lo[v] = 1; hi[v] = N;
        if (cls == 'A' || cls == 'C') { long long h = (long long)num * v / den; if (h < N) hi[v] = (int)h; }
        if (cls == 'B' || cls == 'C') { long long l = ((long long)v * den + num - 1) / num; lo[v] = (int)l; }
        if (cls == 'D' && v <= N / 2) { if (2 * v < N) hi[v] = 2 * v; }
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
