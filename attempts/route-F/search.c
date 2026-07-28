/* route-F search engine.
 *
 * Enumerate legal subsets U of a given universe n_0<...<n_{K-1} (legal = no
 * isolated point: U is a disjoint union of runs of consecutive integers of
 * length >= 2) subject to
 *    (i)  sum_{i in U} w[j][i]  ==  t[j]   (mod m[j])   for every j
 *    (ii) Sigma(U) in [LO,HI]   (fixed point, scale 2^50, directed rounding)
 *
 * (i) with m[j]=p^{E_p-nu_p(D)}, t[j]=0 encodes "denominator of Sigma(U)
 * divides D"; with m[j]=p^{E_p}, t[j]=(rho*L) mod m[j] it encodes Sigma(U)=rho.
 *
 * Prune: per-modulus arc consistency.  R[j][s] = { sum_{i in J} w[j][i] mod m[j]
 * : J subset of {s,...,K-1} } (all subsets -- a superset of the legal ones, so
 * the prune is sound).  Cut the node unless (t[j]-S[j]) mod m[j] is in R[j][s].
 *
 * Output is re-verified exactly, elsewhere, by verify.py.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

typedef unsigned long long u64;

static int K, NP;
static int *N;
static long long *Wc, *Wf, *SufMax;
static long long LO, HI;
static int *P, *M, *T;
static int **W;
static u64 ***R;          /* R[j][s] bitset over M[j] */
static int *nextStart;
static long long *S;      /* current residues */
static long long sumF, sumC;
static long long maxout, nout, nodes, nodecap;
static int *cur, ncur;
static FILE *fout;

static inline int getbit(u64 *b, int i) { return (b[i >> 6] >> (i & 63)) & 1ULL; }
static inline void setbit(u64 *b, int i) { b[i >> 6] |= 1ULL << (i & 63); }

static u64 *newbs(int m) {
    int nw = (m + 63) / 64;
    u64 *b = (u64 *)calloc(nw, sizeof(u64));
    return b;
}

static void build_reach(void) {
    R = (u64 ***)malloc(NP * sizeof(u64 **));
    for (int j = 0; j < NP; j++) {
        int m = M[j], nw = (m + 63) / 64;
        R[j] = (u64 **)malloc((K + 1) * sizeof(u64 *));
        u64 *b = newbs(m);
        setbit(b, 0);
        R[j][K] = b;
        for (int i = K - 1; i >= 0; i--) {
            int w = W[j][i];
            if (w == 0) { R[j][i] = R[j][i + 1]; continue; }
            u64 *prev = R[j][i + 1];
            u64 *nb = newbs(m);
            memcpy(nb, prev, nw * sizeof(u64));
            for (int r = 0; r < m; r++)
                if (getbit(prev, r)) setbit(nb, (r + w) % m);
            R[j][i] = nb;
        }
    }
}

static void emit(void) {
    nout++;
    for (int i = 0; i < ncur; i++) fprintf(fout, "%d%c", cur[i], i + 1 == ncur ? '\n' : ' ');
    fflush(fout);
}

static void addelt(int i) {
    cur[ncur++] = N[i];
    sumF += Wf[i]; sumC += Wc[i];
    for (int j = 0; j < NP; j++) {
        S[j] += W[j][i];
        if (S[j] >= M[j]) S[j] -= M[j];
    }
}
static void delelt(int i) {
    ncur--;
    sumF -= Wf[i]; sumC -= Wc[i];
    for (int j = 0; j < NP; j++) {
        S[j] -= W[j][i];
        if (S[j] < 0) S[j] += M[j];
    }
}

static void dfs(int s) {
    if (nout >= maxout) return;
    if (++nodes > nodecap) return;
    if (sumF > HI) return;
    for (int j = 0; j < NP; j++) {
        int need = (int)((T[j] - S[j]) % M[j]);
        if (need < 0) need += M[j];
        if (!getbit(R[j][s], need)) return;
    }
    if (sumC + (s < K ? SufMax[s] : 0) < LO) return;
    /* stop here? */
    if (ncur > 0 && sumC >= LO && sumF <= HI) {
        int ok = 1;
        for (int j = 0; j < NP; j++) if (S[j] != T[j]) { ok = 0; break; }
        if (ok) emit();
    }
    for (int a = s; a < K; a++) {
        if (sumC + SufMax[a] < LO) break;
        if (a + 1 >= K || N[a + 1] != N[a] + 1) continue;
        int added = 0;
        addelt(a); added++;
        int b = a + 1;
        while (b < K && N[b] == N[b - 1] + 1) {
            addelt(b); added++;
            if (sumF > HI) break;
            dfs(nextStart[b]);
            if (nout >= maxout || nodes > nodecap) break;
            b++;
        }
        for (int q = a + added - 1; q >= a; q--) delelt(q);
        if (nout >= maxout || nodes > nodecap) return;
    }
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: search prob out [maxout] [nodecap]\n"); return 2; }
    FILE *f = fopen(argv[1], "r");
    if (!f) { perror("open"); return 1; }
    fout = fopen(argv[2], "w");
    maxout = argc > 3 ? atoll(argv[3]) : 1000;
    nodecap = argc > 4 ? atoll(argv[4]) : 4000000000LL;

    if (fscanf(f, "%d", &K) != 1) return 1;
    N = malloc(K * sizeof(int));
    for (int i = 0; i < K; i++) fscanf(f, "%d", &N[i]);
    fscanf(f, "%d", &NP);
    P = malloc(NP * sizeof(int)); M = malloc(NP * sizeof(int)); T = malloc(NP * sizeof(int));
    W = malloc(NP * sizeof(int *));
    for (int j = 0; j < NP; j++) {
        fscanf(f, "%d %d %d", &P[j], &M[j], &T[j]);
        W[j] = malloc(K * sizeof(int));
        for (int i = 0; i < K; i++) fscanf(f, "%d", &W[j][i]);
    }
    long long lo, hi;
    fscanf(f, "%lld %lld", &lo, &hi);
    LO = lo; HI = hi;
    fclose(f);

    const long long SC = 1LL << 50;
    Wc = malloc(K * sizeof(long long)); Wf = malloc(K * sizeof(long long));
    SufMax = malloc((K + 1) * sizeof(long long));
    for (int i = 0; i < K; i++) { Wf[i] = SC / N[i]; Wc[i] = (SC + N[i] - 1) / N[i]; }
    SufMax[K] = 0;
    for (int i = K - 1; i >= 0; i--) SufMax[i] = SufMax[i + 1] + Wc[i];
    nextStart = malloc(K * sizeof(int));
    for (int i = 0; i < K; i++) {
        int j = i + 1;
        while (j < K && N[j] < N[i] + 2) j++;
        nextStart[i] = j;
    }
    S = calloc(NP, sizeof(long long));
    cur = malloc(K * sizeof(int));
    build_reach();
    dfs(0);
    fprintf(stderr, "nodes=%lld out=%lld%s\n", nodes, nout,
            nodes > nodecap ? " (NODECAP HIT: search NOT exhaustive)" : " (exhausted)");
    fclose(fout);
    return 0;
}
