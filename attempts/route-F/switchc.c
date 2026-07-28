/* route-F: SWITCH finder.
 *
 * Reads the same problem file as search.c (universe, moduli m_j, weights w_j).
 * Enumerates legal subsets U of the universe (DFS over runs), computes the
 * residue vector S_j(U) = sum_{i in U} w[j][i] mod m[j], and looks for two
 * DISTINCT legal subsets A,B with the SAME residue vector.  Then
 *      Sigma(B) - Sigma(A)  has denominator dividing D,
 * i.e. (A,B) is a SWITCH.  (The moduli encode exactly the condition
 * "denominator of Sigma divides D"; equal residue vectors <=> the difference
 * satisfies it.)
 *
 * This is the birthday search: 2^{2*Lambda} ordered pairs against 2^{lambda}
 * residue vectors, versus 2^{Lambda} against 2^{lambda} for gadgets.
 *
 * usage: switchc prob out maxsubsets
 * Output: one line per collision:  "A: ...  |  B: ..."   (verified elsewhere)
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

typedef unsigned long long u64;
static int K, NP;
static int *N;
static int *M, *T, **W;
static long long *S;
static int *nextStart;
static u64 curmask[2];
static long long nsub, maxsub;
static long long cursum;
static long long *Wf;

typedef struct { u64 key; long long sum; u64 m0, m1; } Ent;
static Ent *tab;

static u64 hashvec(void) {
    u64 h = 1469598103934665603ULL;
    for (int j = 0; j < NP; j++) {
        u64 v = (u64)S[j];
        for (int b = 0; b < 8; b++) { h ^= (v >> (8 * b)) & 0xff; h *= 1099511628211ULL; }
    }
    return h ? h : 1;
}

static void record(void) {
    if (nsub >= maxsub) return;
    tab[nsub].key = hashvec();
    tab[nsub].sum = cursum;
    tab[nsub].m0 = curmask[0];
    tab[nsub].m1 = curmask[1];
    nsub++;
}

static void addelt(int i) {
    curmask[i >> 6] |= 1ULL << (i & 63);
    cursum += Wf[i];
    for (int j = 0; j < NP; j++) { S[j] += W[j][i]; if (S[j] >= M[j]) S[j] -= M[j]; }
}
static void delelt(int i) {
    curmask[i >> 6] &= ~(1ULL << (i & 63));
    cursum -= Wf[i];
    for (int j = 0; j < NP; j++) { S[j] -= W[j][i]; if (S[j] < 0) S[j] += M[j]; }
}

static void dfs(int s) {
    if (nsub >= maxsub) return;
    record();
    for (int a = s; a < K; a++) {
        if (a + 1 >= K || N[a + 1] != N[a] + 1) continue;
        int added = 0;
        addelt(a); added++;
        int b = a + 1;
        while (b < K && N[b] == N[b - 1] + 1) {
            addelt(b); added++;
            dfs(nextStart[b]);
            if (nsub >= maxsub) break;
            b++;
        }
        for (int q = a + added - 1; q >= a; q--) delelt(q);
        if (nsub >= maxsub) return;
    }
}

static int cmpe(const void *x, const void *y) {
    const Ent *a = x, *b = y;
    if (a->key != b->key) return a->key < b->key ? -1 : 1;
    if (a->sum != b->sum) return a->sum < b->sum ? -1 : 1;
    return 0;
}

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: switchc prob out maxsubsets\n"); return 2; }
    FILE *f = fopen(argv[1], "r");
    if (!f) { perror("open"); return 1; }
    if (fscanf(f, "%d", &K) != 1) return 1;
    if (K > 128) { fprintf(stderr, "K>128 unsupported\n"); return 1; }
    N = malloc(K * sizeof(int));
    for (int i = 0; i < K; i++) if (fscanf(f, "%d", &N[i]) != 1) return 1;
    if (fscanf(f, "%d", &NP) != 1) return 1;
    M = malloc(NP * sizeof(int)); T = malloc(NP * sizeof(int)); W = malloc(NP * sizeof(int *));
    int p;
    for (int j = 0; j < NP; j++) {
        if (fscanf(f, "%d %d %d", &p, &M[j], &T[j]) != 3) return 1;
        W[j] = malloc(K * sizeof(int));
        for (int i = 0; i < K; i++) if (fscanf(f, "%d", &W[j][i]) != 1) return 1;
    }
    fclose(f);
    maxsub = atoll(argv[3]);
    tab = malloc(maxsub * sizeof(Ent));
    if (!tab) { fprintf(stderr, "alloc failed\n"); return 1; }
    S = calloc(NP, sizeof(long long));
    nextStart = malloc(K * sizeof(int));
    for (int i = 0; i < K; i++) { int j = i + 1; while (j < K && N[j] < N[i] + 2) j++; nextStart[i] = j; }
    Wf = malloc(K * sizeof(long long));
    { const long long SC = 1LL << 50; for (int i = 0; i < K; i++) Wf[i] = SC / N[i]; }
    dfs(0);
    fprintf(stderr, "enumerated %lld legal subsets%s\n", nsub,
            nsub >= maxsub ? " (cap hit)" : " (all)");
    qsort(tab, nsub, sizeof(Ent), cmpe);
    FILE *g = fopen(argv[2], "w");
    long long ncol = 0;
    for (long long i = 1; i < nsub; i++) {
        if (tab[i].key != tab[i - 1].key) continue;
        if (tab[i].m0 == tab[i - 1].m0 && tab[i].m1 == tab[i - 1].m1) continue;
        for (int q = 0; q < 2; q++) {
            u64 m0 = q ? tab[i].m0 : tab[i - 1].m0, m1 = q ? tab[i].m1 : tab[i - 1].m1;
            for (int t = 0; t < K; t++)
                if ((t < 64 ? (m0 >> t) : (m1 >> (t - 64))) & 1ULL) fprintf(g, "%d ", N[t]);
            fprintf(g, q ? "\n" : "| ");
        }
        ncol++;
    }
    fprintf(stderr, "collisions=%lld\n", ncol);
    fclose(g);
    return 0;
}
