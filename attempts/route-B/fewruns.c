/* fewruns.c -- (derived from bsearch.c)
 * Exhaustive search RESTRICTED to legal U with at most RMAX maximal runs.
 * Extra exact bound: a U-run is always contained in one run of the universe A,
 * so a U with at most j runs left touches at most j runs of A; the heaviest j
 * runs of A at positions >= pos are the j earliest ones (weights decrease), so
 * runcap[pos][j] = sum of the first j universe runs from pos is a valid upper
 * bound on the sum still obtainable.  Used to prune.
 *
 * Motivation: P(k) needs a certificate with r <= k <= M, so ruling out all U
 * with r <= 6 rules out k <= 6.
 *
 * original header follows.
 * bsearch.c -- exhaustive DFS for  sum_{n in U} 1/n = 1,  U subset [2,N],
 * U with no isolated point, run over the REDUCED universe produced by reduce.py.
 *
 * Input (stdin):   N  K  a_1 a_2 ... a_K      (the reduced universe, increasing)
 * Exact arithmetic throughout: L = lcm(universe) as unsigned __int128,
 * weight w[n] = L/n, target sum of weights = L.
 *
 * Prunes
 *   (1) R > tail[pos]                      (cannot reach the target any more)
 *   (2) Q[pos] does not divide R           (top-level p-adic condition, as csearch.c)
 *   (3) per-prime p-adic reachability: with x_p = sum of p^{E_p}/n over already
 *       chosen multiples of n, the still-open multiples of p must be able to
 *       supply the residue -x_p mod p^{E_p}.  reach[p][pos] is the precomputed
 *       set of residues realisable by subsets of the universe multiples of p that
 *       are >= pos.  Checked only at pos where a multiple of p was just passed.
 *   Prune (3) strictly contains prune (2); both are kept, (2) is cheaper.
 *
 * usage: ./bsearch < universe.txt
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef unsigned __int128 u128;
typedef unsigned long long u64;

#define MAXN 2048
#define MAXP 400
#define WORDS 16                      /* 16*64 = 1024 residues max */

static int N, K;
static int allowed[MAXN];
static u128 L, w[MAXN], tail[MAXN + 2], Q[MAXN + 2];
static long long nodes = 0, nsol = 0, maxsol = 100;
static int chosen[MAXN], nch = 0;
static int primes[MAXP], np = 0;
static int jobid = 0, njobs = 1, splitpos = 0;
static int RMAX = 0;           /* 0 = unlimited */
static int nruns = 0;
static u128 *runcap;            /* runcap[pos*(RMAX+2)+j] */
static long long splitctr = 0;

/* per-prime p-adic data */
static int pmod[MAXP];                /* p^{E_p} */
static int pcoef[MAXP][MAXN];         /* p^{E_p}/n mod p^{E_p}, for p|n allowed */
static u64 (*reach)[WORDS];           /* reach[pi*(N+2)+pos][word] */
static int xres[MAXP];                /* current residue x_p */
static int dprimes[MAXN][8], ndp[MAXN];  /* primes dividing pos, for the check */

static void print_u128(u128 x) {
    char buf[64]; int i = 63; buf[i--] = 0;
    if (!x) { printf("0"); return; }
    while (x) { buf[i--] = '0' + (int)(x % 10); x /= 10; }
    printf("%s", buf + i + 1);
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
    int m = pmod[pi];
    int t = (m - xres[pi]) % m;
    return bit(reach[pi * (N + 2) + pos], t);
}

static void dfs(int pos, u128 R, int runlen) {
    nodes++;
    if (pos == splitpos) { if ((splitctr++ % njobs) != jobid) return; }
    if (R == 0) {
        if (runlen != 1) {
            nsol++;
            printf("SOL");
            for (int i = 0; i < nch; i++) printf(" %d", chosen[i]);
            printf("\n"); fflush(stdout);
            if (nsol >= maxsol) { printf("(solution cap reached)\n"); exit(0); }
        }
        return;
    }
    if (pos > N) return;
    if (R > tail[pos]) return;
    if (RMAX) {
        int j = RMAX - nruns + (runlen > 0 ? 1 : 0);
        if (j < 0) return;
        if (j > RMAX + 1) j = RMAX + 1;
        if (R > runcap[(size_t)pos * (RMAX + 2) + j]) return;
    }
    if (R % Q[pos]) return;
    /* prune (3): primes whose multiple pos-1 was just passed */
    for (int i = 0; i < ndp[pos - 1]; i++) {
        if (!checkp(dprimes[pos - 1][i], pos)) return;
    }
    if (allowed[pos] && w[pos] <= R) {
        int newrun = (runlen == 0);
        if (RMAX && newrun && nruns >= RMAX) goto skipbranch;
        nruns += newrun;
        int save[8];
        for (int i = 0; i < ndp[pos]; i++) {
            int pi = dprimes[pos][i];
            save[i] = xres[pi];
            xres[pi] = (xres[pi] + pcoef[pi][pos]) % pmod[pi];
        }
        chosen[nch++] = pos;
        dfs(pos + 1, R - w[pos], runlen + 1);
        nch--;
        nruns -= newrun;
        for (int i = 0; i < ndp[pos]; i++) xres[dprimes[pos][i]] = save[i];
    }
skipbranch:
    if (!(allowed[pos] && w[pos] <= R)) { if (runlen == 1) return; }
    if (runlen != 1) dfs(pos + 1, R, 0);
}

int main(int argc, char **argv) {
    if (argc > 1) maxsol = atoll(argv[1]);
    if (argc > 2) RMAX = atoi(argv[2]);
    if (argc > 5) { jobid = atoi(argv[3]); njobs = atoi(argv[4]); splitpos = atoi(argv[5]); }
    if (scanf("%d %d", &N, &K) != 2) { fprintf(stderr, "bad input\n"); return 1; }
    memset(allowed, 0, sizeof allowed);
    for (int i = 0; i < K; i++) { int a; scanf("%d", &a); allowed[a] = 1; }

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
    printf("N=%d |A|=%d L=", N, K); print_u128(L);
    { u128 t = L; int b = 0; while (t) { t >>= 1; b++; } printf(" (%d bits)\n", b); }

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

    /* per-prime tables */
    reach = calloc((size_t)np * (N + 2), sizeof(u64) * WORDS);
    if (!reach) { fprintf(stderr, "oom\n"); return 1; }
    for (int i = 0; i < MAXN; i++) ndp[i] = 0;
    for (int pi = 0; pi < np; pi++) {
        int p = primes[pi], E = 0;
        for (int n = p; n <= N; n += p) if (allowed[n]) { int e = nu(n, p); if (e > E) E = e; }
        int m = 1; for (int i = 0; i < E; i++) m *= p;
        pmod[pi] = m;
        if (m > WORDS * 64) { fprintf(stderr, "modulus too big p=%d m=%d\n", p, m); return 1; }
        for (int n = p; n <= N; n += p) if (allowed[n]) {
            int e = nu(n, p), pe = 1; for (int i = 0; i < e; i++) pe *= p;
            int q1 = 1; for (int i = 0; i < E - e; i++) q1 *= p;
            pcoef[pi][n] = (int)((long long)q1 * inv_mod(n / pe, m) % m);
            ndp[n] = ndp[n]; dprimes[n][ndp[n]++] = pi;
        }
        /* reach[pi][pos] = residues realisable from allowed multiples of p that are >= pos */
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

    if (RMAX) {
        runcap = calloc((size_t)(N + 3) * (RMAX + 2), sizeof(u128));
        for (int pos = N + 1; pos >= 2; pos--)
            for (int j = 0; j <= RMAX + 1; j++) {
                if (j == 0 || pos > N) { runcap[(size_t)pos*(RMAX+2)+j] = 0; continue; }
                /* [a,b] = first universe run at or after pos (a = pos if allowed) */
                int a = pos; while (a <= N && !allowed[a]) a++;
                if (a > N) { runcap[(size_t)pos*(RMAX+2)+j] = 0; continue; }
                int b = a; while (b + 1 <= N && allowed[b + 1]) b++;
                u128 s = 0; for (int t = a; t <= b; t++) s += w[t];
                int nxt = (b + 2 <= N + 1) ? b + 2 : N + 1;
                /* CORRECT bound: a LATER universe run may be heavier than this one,
                   so we must take the max of "skip this run" and "use it fully". */
                u128 skipv = runcap[(size_t)nxt*(RMAX+2)+j];
                u128 usev  = s + runcap[(size_t)nxt*(RMAX+2)+(j-1)];
                runcap[(size_t)pos*(RMAX+2)+j] = skipv > usev ? skipv : usev;
            }
    }
    for (int pi = 0; pi < np; pi++) xres[pi] = 0;
    dfs(2, L, 0);
    printf("done RMAX=%d job=%d/%d nodes=%lld solutions=%lld\n", RMAX, jobid, njobs, nodes, nsol);
    return 0;
}
