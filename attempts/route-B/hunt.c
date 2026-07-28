/* hunt.c -- randomised certificate hunter for  sum_{n in U} 1/n = 1, U legal.
 *
 * Same exact model and prunes as bsearch.c (see that file), but the DFS branch
 * order at each node is randomised and the search is run as a sequence of
 * restarts with a node budget, so that the certificates found are spread over
 * the whole solution set instead of the lexicographic prefix.
 *
 * A bias parameter q in [0,1] controls the probability of trying "take pos"
 * before "skip pos"; large q produces certificates with many elements (hence
 * many maximal runs, hence large k), small q produces sparse ones.
 *
 * usage: ./hunt seed budget bias_percent maxsol < universe.txt
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef unsigned __int128 u128;
typedef unsigned long long u64;

#define MAXN 2048
#define MAXP 400
#define WORDS 16

static int N, K;
static int allowed[MAXN];
static u128 L, w[MAXN], tail[MAXN + 2], Q[MAXN + 2];
static long long nodes = 0, nsol = 0, maxsol = 1000000, budget = 20000000;
static int chosen[MAXN], nch = 0;
static int primes[MAXP], np = 0;
static int pmod[MAXP], pcoef[MAXP][MAXN], xres[MAXP];
static u64 (*reach)[WORDS];
static int dprimes[MAXN][8], ndp[MAXN];
static int bias = 50;
static u64 rngstate;

static inline u64 rnd(void) {
    rngstate ^= rngstate << 13; rngstate ^= rngstate >> 7; rngstate ^= rngstate << 17;
    return rngstate;
}

static int nu(int n, int p) { int e = 0; while (n % p == 0) { n /= p; e++; } return e; }
static long long inv_mod(long long a, long long m) {
    long long g = m, x = 0, x1 = 1, a1 = a % m, t, q;
    while (a1) { q = g / a1; t = g - q * a1; g = a1; a1 = t; t = x - q * x1; x = x1; x1 = t; }
    return ((x % m) + m) % m;
}
static inline int bit(const u64 *bs, int i) { return (bs[i >> 6] >> (i & 63)) & 1ULL; }
static inline void setbit(u64 *bs, int i) { bs[i >> 6] |= 1ULL << (i & 63); }
static inline int checkp(int pi, int pos) {
    int m = pmod[pi]; int t = (m - xres[pi]) % m;
    return bit(reach[pi * (N + 2) + pos], t);
}

static void emit(void) {
    nsol++;
    printf("SOL");
    for (int i = 0; i < nch; i++) printf(" %d", chosen[i]);
    printf("\n"); fflush(stdout);
}

static int overbudget;

static void dfs(int pos, u128 R, int runlen) {
    if (++nodes > budget) { overbudget = 1; return; }
    if (nsol >= maxsol) { overbudget = 1; return; }
    if (R == 0) { if (runlen != 1) emit(); return; }
    if (pos > N) return;
    if (R > tail[pos]) return;
    if (R % Q[pos]) return;
    for (int i = 0; i < ndp[pos - 1]; i++) if (!checkp(dprimes[pos - 1][i], pos)) return;

    int canTake = allowed[pos] && w[pos] <= R;
    int canSkip = (runlen != 1);
    if (!canTake && !canSkip) return;
    int takeFirst = ((int)(rnd() % 100) < bias);

    for (int round = 0; round < 2 && !overbudget; round++) {
        int doTake = (round == 0) ? takeFirst : !takeFirst;
        if (doTake) {
            if (!canTake) continue;
            int save[8];
            for (int i = 0; i < ndp[pos]; i++) {
                int pi = dprimes[pos][i];
                save[i] = xres[pi];
                xres[pi] = (xres[pi] + pcoef[pi][pos]) % pmod[pi];
            }
            chosen[nch++] = pos;
            dfs(pos + 1, R - w[pos], runlen + 1);
            nch--;
            for (int i = 0; i < ndp[pos]; i++) xres[dprimes[pos][i]] = save[i];
        } else {
            if (!canSkip) continue;
            dfs(pos + 1, R, 0);
        }
    }
}

int main(int argc, char **argv) {
    u64 seed = argc > 1 ? strtoull(argv[1], 0, 10) : 1;
    budget = argc > 2 ? atoll(argv[2]) : 20000000;
    bias = argc > 3 ? atoi(argv[3]) : 50;
    maxsol = argc > 4 ? atoll(argv[4]) : 1000000;
    rngstate = seed * 6364136223846793005ULL + 1442695040888963407ULL;
    if (!rngstate) rngstate = 88172645463325252ULL;

    if (scanf("%d %d", &N, &K) != 2) return 1;
    memset(allowed, 0, sizeof allowed);
    for (int i = 0; i < K; i++) { int a; if (scanf("%d", &a) != 1) return 1; allowed[a] = 1; }
    for (int i = 2; i <= N; i++) {
        int isp = 1;
        for (int j = 2; j * j <= i; j++) if (i % j == 0) { isp = 0; break; }
        if (isp) primes[np++] = i;
    }
    L = 1;
    for (int pi = 0; pi < np; pi++) {
        int p = primes[pi], emax = 0;
        for (int n = 2; n <= N; n++) if (allowed[n]) { int e = nu(n, p); if (e > emax) emax = e; }
        for (int i = 0; i < emax; i++) L *= (u128)p;
    }
    for (int n = 2; n <= N; n++) w[n] = allowed[n] ? L / (u128)n : 0;
    tail[N + 1] = 0;
    for (int n = N; n >= 2; n--) tail[n] = tail[n + 1] + w[n];
    { u128 tot = tail[2];
      /* hard safety guard: every partial sum must fit in unsigned __int128 */
      int tb = 0; { u128 t = tot; while (t) { t >>= 1; tb++; } }
      if (tb >= 128) { fprintf(stderr, "ABORT: total weight needs %d bits, >= 128\n", tb); return 1; }
      fprintf(stderr, "total-weight bits = %d (safe)\n", tb); }
    for (int pos = 2; pos <= N + 1; pos++) {
        u128 q = 1;
        for (int pi = 0; pi < np; pi++) {
            int p = primes[pi];
            int eL = 0; { u128 t = L; while (t % (u128)p == 0) { t /= (u128)p; eL++; } }
            int maxe = 0;
            for (int n = pos; n <= N; n++) if (allowed[n]) { int e = nu(n, p); if (e > maxe) maxe = e; }
            for (int i = 0; i < eL - maxe; i++) q *= (u128)p;
        }
        Q[pos] = q;
    }
    reach = calloc((size_t)np * (N + 2), sizeof(u64) * WORDS);
    if (!reach) return 1;
    for (int i = 0; i < MAXN; i++) ndp[i] = 0;
    for (int pi = 0; pi < np; pi++) {
        int p = primes[pi], E = 0;
        for (int n = p; n <= N; n += p) if (allowed[n]) { int e = nu(n, p); if (e > E) E = e; }
        int m = 1; for (int i = 0; i < E; i++) m *= p;
        pmod[pi] = m;
        if (m > WORDS * 64) { fprintf(stderr, "modulus too big\n"); return 1; }
        for (int n = p; n <= N; n += p) if (allowed[n]) {
            int e = nu(n, p), pe = 1; for (int i = 0; i < e; i++) pe *= p;
            int q1 = 1; for (int i = 0; i < E - e; i++) q1 *= p;
            pcoef[pi][n] = (int)((long long)q1 * inv_mod(n / pe, m) % m);
            dprimes[n][ndp[n]++] = pi;
        }
        u64 *base = (u64 *)reach + (size_t)(pi * (N + 2) + N + 1) * WORDS;
        setbit(base, 0);
        for (int pos = N; pos >= 2; pos--) {
            u64 *cur = (u64 *)reach + (size_t)(pi * (N + 2) + pos) * WORDS;
            u64 *nxt = (u64 *)reach + (size_t)(pi * (N + 2) + pos + 1) * WORDS;
            memcpy(cur, nxt, sizeof(u64) * WORDS);
            if (allowed[pos] && pos % p == 0) {
                int c = pcoef[pi][pos];
                for (int r = 0; r < m; r++) if (bit(nxt, r)) setbit(cur, (r + c) % m);
            }
        }
    }
    long long restarts = 0;
    while (nsol < maxsol) {
        for (int pi = 0; pi < np; pi++) xres[pi] = 0;
        nodes = 0; overbudget = 0; nch = 0;
        dfs(2, L, 0);
        restarts++;
        if (restarts > 2000000) break;
        if (!overbudget && restarts > 200 && nsol == 0) break;  /* space exhausted */
    }
    fprintf(stderr, "restarts=%lld solutions=%lld\n", restarts, nsol);
    return 0;
}
