/* pairhunt.c -- find legal U whose maximal runs ALL have length exactly 2, i.e.
 *      U = {a_1,a_1+1} u ... u {a_k,a_k+1},   a_{i+1} >= a_i + 3,
 *      sum_i (1/a_i + 1/(a_i+1)) = 1.
 * Such a U has r = k maximal runs and M = sum floor(L_i/2) = k, so by the splitting
 * lemma it realises EXACTLY the value k -- which makes it the right object for
 * deciding, for one specific k, whether P(k) holds.
 *
 * RESTRICTED CLASS: this program searches only the "all runs of length 2" class.
 * A negative answer here is NOT a proof that P(k) fails.
 *
 * Exact arithmetic: L = lcm(reduced universe) as unsigned __int128,
 * pair weight wp[a] = L/a + L/(a+1); target sum of chosen wp = L.
 *
 * Prunes: R must lie between the min and the max attainable with exactly j pairs
 * from position >= a (both precomputed by exact DP), plus the p-adic reachability
 * prune of bsearch.c.
 *
 * usage: ./pairsearch kmin kmax maxsolperk < universe.txt
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
static u128 L, wp[MAXN];
static int isPairStart[MAXN];
static int MAXJ;
static u128 *mxs, *mns;          /* [a*(MAXJ+1)+j] */
static const u128 INF = ~(u128)0;

static int primes[MAXP], np = 0;
static int pmod[MAXP], pcoef[MAXP][MAXN], xres[MAXP];
static u64 (*reach)[WORDS];
static int dprimes[MAXN][8], ndp[MAXN];

static int chosen[MAXN], nch;
static long long nodes, nsol, maxsol;
static int targetK;
static u64 rngstate;
static long long budget;
static int bias;
static int overbudget;
static inline u64 rnd(void) {
    rngstate ^= rngstate << 13; rngstate ^= rngstate >> 7; rngstate ^= rngstate << 17;
    return rngstate;
}

static void print_u128(u128 x) {
    char b[64]; int i = 63; b[i--] = 0;
    if (!x) { printf("0"); return; }
    while (x) { b[i--] = '0' + (int)(x % 10); x /= 10; }
    printf("%s", b + i + 1);
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
#define MX(a,j) mxs[(size_t)(a)*(MAXJ+1)+(j)]
#define MN(a,j) mns[(size_t)(a)*(MAXJ+1)+(j)]

static void dfs(int a, u128 R, int j) {
    if (++nodes > budget) { overbudget = 1; return; }
    if (j == 0) {
        if (R == 0) {
            nsol++;
            printf("SOL");
            for (int i = 0; i < nch; i++) printf(" %d %d", chosen[i], chosen[i] + 1);
            printf("\n"); fflush(stdout);
            if (nsol >= maxsol) overbudget = 1;
        }
        return;
    }
    if (a > N) return;
    if (overbudget) return;
    if (MX(a, j) < R) return;
    if (MN(a, j) > R) return;
    /* p-adic checks: positions a-1,a-2,a-3 may have been passed since last check */
    for (int t = a - 1; t >= a - 3 && t >= 2; t--)
        for (int i = 0; i < ndp[t]; i++)
            if (!checkp(dprimes[t][i], a)) return;

    int canTake = isPairStart[a] && wp[a] <= R;
    int takeFirst = ((int)(rnd() % 100) < bias);
    for (int round = 0; round < 2 && !overbudget; round++) {
        int doTake = (round == 0) ? takeFirst : !takeFirst;
        if (doTake) {
            if (!canTake) continue;
            int sv[32], nsv = 0;
            for (int d = 0; d < 2; d++) {
                int n = a + d;
                for (int i = 0; i < ndp[n]; i++) {
                    int pi = dprimes[n][i];
                    sv[nsv++] = pi; sv[nsv++] = xres[pi];
                    xres[pi] = (xres[pi] + pcoef[pi][n]) % pmod[pi];
                }
            }
            chosen[nch++] = a;
            dfs(a + 3, R - wp[a], j - 1);
            nch--;
            for (int i = nsv - 2; i >= 0; i -= 2) xres[sv[i]] = sv[i + 1];
        } else {
            dfs(a + 1, R, j);
        }
    }
}

int main(int argc, char **argv) {
    int kmin = argc > 1 ? atoi(argv[1]) : 1;
    int kmax = argc > 2 ? atoi(argv[2]) : 60;
    maxsol = argc > 3 ? atoll(argv[3]) : 1;
    budget = argc > 4 ? atoll(argv[4]) : 3000000;
    bias = argc > 5 ? atoi(argv[5]) : 50;
    u64 seed = argc > 6 ? strtoull(argv[6], 0, 10) : 1;
    long long restartcap = argc > 7 ? atoll(argv[7]) : 400;
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
    for (int a = 2; a + 1 <= N; a++) {
        isPairStart[a] = allowed[a] && allowed[a + 1];
        if (isPairStart[a]) wp[a] = L / (u128)a + L / (u128)(a + 1);
    }
    { u128 tot = 0; for (int a = 2; a + 1 <= N; a++) if (isPairStart[a]) tot += wp[a];
      int tb = 0; { u128 t = tot; while (t) { t >>= 1; tb++; } }
      if (tb >= 128) { fprintf(stderr, "ABORT: total weight needs %d bits\n", tb); return 1; } }
    MAXJ = N / 3 + 2;
    mxs = malloc(sizeof(u128) * (size_t)(N + 12) * (MAXJ + 1));
    mns = malloc(sizeof(u128) * (size_t)(N + 12) * (MAXJ + 1));
    if (!mxs || !mns) { fprintf(stderr, "oom\n"); return 1; }
    for (int a = N + 9; a >= 2; a--) {
        for (int j = 0; j <= MAXJ; j++) {
            if (j == 0) { MX(a, j) = 0; MN(a, j) = 0; continue; }
            if (a > N) { MX(a, j) = 0; MN(a, j) = INF; continue; }
            u128 bx = MX(a + 1, j), bn = MN(a + 1, j);
            if (isPairStart[a]) {
                u128 sx = MX(a + 3, j - 1);
                if (j - 1 == 0 || sx != 0) { u128 cx = wp[a] + sx; if (cx > bx) bx = cx; }
                u128 sn = MN(a + 3, j - 1);
                if (sn != INF) { u128 cn = wp[a] + sn; if (cn < bn) bn = cn; }
            }
            MX(a, j) = bx; MN(a, j) = bn;
        }
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
        setbit((u64 *)reach + (size_t)(pi * (N + 2) + N + 1) * WORDS, 0);
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

    printf("# N=%d |A|=%d L=", N, K); print_u128(L); printf("\n");
    for (int k = kmin; k <= kmax && k <= MAXJ; k++) {
        nsol = 0;
        long long tot = 0, rs = 0;
        for (rs = 0; rs < restartcap && nsol < maxsol; rs++) {
            for (int pi = 0; pi < np; pi++) xres[pi] = 0;
            nodes = 0; nch = 0; overbudget = 0; targetK = k;
            dfs(2, L, k);
            tot += nodes;
            if (!overbudget) break;   /* whole pairs-class space exhausted */
        }
        printf("# k=%d pairs: found=%lld restarts=%lld nodes=%lld %s\n", k, nsol, rs, tot,
               (nsol == 0 && rs < restartcap) ? "EXHAUSTED-NONE-in-pairs-class" :
               (nsol == 0 ? "not-found(budget)" : ""));
        fflush(stdout);
    }
    return 0;
}
