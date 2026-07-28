/* search.c -- exact search for LEGAL systems inside a far-out window [T,N].
 *
 *  MODE 1 (exact) :  find W subset universe, legal, with sum_{n in W} 1/n = u/v.
 *  MODE 0 (gadget):  find W subset universe, legal, whose reciprocal sum has
 *                    DENOMINATOR DIVIDING a prescribed D = prod_p p^{f_p}.
 *
 * =====================  ARITHMETIC  =====================
 * L := lcm(universe), enlarged if necessary so that v | L.  Write L = prod p^{E_p}.
 * For W subset universe put S(W) := sum_{n in W} L/n, an integer, so that
 * sum_{n in W} 1/n = S(W)/L.  We NEVER form L.  For each prime p we work with
 * the modulus  m_p := p^{max(0, E_p - f_p)}  (f_p = 0 in mode 1), a machine word
 * because m_p <= p^{E_p} <= max(N, v).
 *   MODE 1: the condition S = R0 := (L/v)*u  is equivalent to S = R0 mod p^{E_p}
 *           for every p (CRT), since 0 <= S,R0 < L is guaranteed by the size prune.
 *   MODE 0: denominator of S/L divides D  <==>  (L/D) | S  <==>  for every p,
 *           S = 0 mod p^{E_p-f_p}.
 * Everything is exact integer arithmetic.  The only auxiliary data are INTEGER
 * fixed-point bounds (scale 2^96, directed rounding) used for a conservative
 * size prune in mode 1.  No floating point anywhere.
 *
 * KEY OBSERVATION.  nu_p(L/n) = E_p - nu_p(n), so L/n = 0 mod m_p unless
 * nu_p(n) > f_p.  Only those elements move s_p.
 *
 * =====================  PRUNES (both proved)  =====================
 * (P1) size (mode 1 only): 0 <= rho - (partial sum) <= sum of 1/n over the
 *      remaining universe; checked with conservative integer bounds.
 * (P2) per-prime ARC CONSISTENCY.  For a prime p and position i put
 *          A(p,i) := { sum_{j in J} (L/n_j) mod m_p : J subset {i,...,cnt-1} },
 *      computed once by a backward subset-sum DP mod m_p.  Any completion adds
 *      an element of A(p,i) to s_p, so we may prune unless
 *          (target_p - s_p) mod m_p   lies in   A(p,i).
 *      This is strictly stronger than the classical "gcd of the remaining
 *      weights divides the remaining target" prune.  A(p,i) changes only at the
 *      positions i that move s_p, so the test is done only there.
 *
 * LEGALITY: W has no isolated point (n in W => n-1 in W or n+1 in W).
 *
 * PROBLEM FILE
 *      line 1:  T N mode u v
 *      line 2:  nf                         number of (p,f_p) pairs
 *      line 3:  p1 f1 p2 f2 ...            the allowed denominator D
 *      line 4:  cnt
 *      line 5:  n_1 ... n_cnt              the pruned universe (increasing)
 *
 * usage:  ./search probfile nsol budget seed
 *      nsol   : stop after this many results (0 = exhaust the tree)
 *      budget : nodes per randomised restart (0 = deterministic exhaustive)
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef __int128 i128;
typedef unsigned __int128 u128;

#define MAXC 40000
#define MAXP 900

static int T0, Nhi, cnt, mode;
static long long UNUM = 1, VDEN = 1;
static int el[MAXC], adj[MAXC];
static int np = 0, pr[MAXP];
static long long md[MAXP], tgt[MAXP];
static long long *wres[MAXP];
static unsigned char *reach[MAXP];
static int *mrem[MAXP];
static long long s[MAXP];
static int chkcnt[MAXC + 1], *chk[MAXC + 1];
static int chosen[MAXC], nch = 0;
static int fexp[100000];                 /* f_p indexed by prime */

static i128 SC;
static i128 rlo[MAXC], rhi[MAXC], tailmax[MAXC + 1];
static long long nodes = 0, nsolfound = 0, maxsol = 1, budget = 0;
static unsigned long long rs = 987654321987654321ULL;
static int hitb = 0;

static unsigned long long xr(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
static int nu(long long n, int p) { int e = 0; while (n % p == 0) { n /= p; e++; } return e; }
static long long mulmod(long long a, long long b, long long m) { return (long long)((i128)a * b % m); }
static long long pw(long long a, long long e, long long m) {
    long long r = 1 % m; a %= m;
    while (e) { if (e & 1) r = mulmod(r, a, m); a = mulmod(a, a, m); e >>= 1; }
    return r;
}
static long long inv_mod(long long a, long long m) {
    long long old_r = ((a % m) + m) % m, r = m, old_s = 1, sc = 0, t;
    while (r != 0) { long long qq = old_r / r;
        t = old_r - qq * r; old_r = r; r = t;
        t = old_s - qq * sc; old_s = sc; sc = t; }
    long long res = old_s % m; if (res < 0) res += m; return res;
}

static void report(void) {
    nsolfound++;
    printf(mode ? "SOL" : "G");
    for (int i = 0; i < nch; i++) printf(" %d", chosen[i]);
    printf("\n"); fflush(stdout);
}

static int dfs(int i, int runlen, i128 lo, i128 hi) {
    nodes++;
    if (budget && nodes > budget) { hitb = 1; return 1; }
    if (i > 0 && !adj[i]) { if (runlen == 1) return 0; runlen = 0; }
    if (mode == 1) { if (hi < 0) return 0; if (lo > tailmax[i]) return 0; }
    for (int t = 0; t < chkcnt[i]; t++) {
        int j = chk[i][t];
        long long need = tgt[j] - s[j]; if (need < 0) need += md[j];
        if (!reach[j][(size_t)mrem[j][i] * md[j] + need]) return 0;
    }
    if (i == cnt) {
        if (runlen != 1 && nch > 0) {
            if (mode == 1 && (lo > SC / 2 || hi < -(SC / 2))) return 0;
            report();
            if (maxsol && nsolfound >= maxsol) return 1;
        }
        return 0;
    }
    int order = (int)(xr() & 1);
    for (int t = 0; t < 2; t++) {
        int take = (t == 0) ? (order == 0) : (order == 1);
        if (take) {
            for (int j = 0; j < np; j++) if (wres[j][i]) { s[j] += wres[j][i]; if (s[j] >= md[j]) s[j] -= md[j]; }
            chosen[nch++] = el[i];
            int st = dfs(i + 1, runlen + 1, lo - rhi[i], hi - rlo[i]);
            nch--;
            for (int j = 0; j < np; j++) if (wres[j][i]) { s[j] -= wres[j][i]; if (s[j] < 0) s[j] += md[j]; }
            if (st) return 1;
        } else {
            if (runlen != 1) { if (dfs(i + 1, 0, lo, hi)) return 1; }
        }
    }
    return 0;
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: %s probfile [nsol budget seed]\n", argv[0]); return 1; }
    FILE *f = fopen(argv[1], "r");
    if (!f) { perror("open"); return 1; }
    if (fscanf(f, "%d %d %d %lld %lld", &T0, &Nhi, &mode, &UNUM, &VDEN) != 5) { fprintf(stderr, "bad header\n"); return 1; }
    int nf; if (fscanf(f, "%d", &nf) != 1) return 1;
    for (int k = 0; k < nf; k++) { int p, e; if (fscanf(f, "%d %d", &p, &e) != 2) return 1; fexp[p] = e; }
    if (fscanf(f, "%d", &cnt) != 1) return 1;
    for (int i = 0; i < cnt; i++) if (fscanf(f, "%d", &el[i]) != 1) return 1;
    fclose(f);
    if (argc > 2) maxsol = atoll(argv[2]);
    if (argc > 3) budget = atoll(argv[3]);
    if (argc > 4) rs = strtoull(argv[4], NULL, 10) * 6364136223846793005ULL + 1442695040888963407ULL;

    adj[0] = 0;
    for (int i = 1; i < cnt; i++) adj[i] = (el[i] == el[i - 1] + 1);

    char *sv = calloc(Nhi + 2, 1);
    for (int i = 2; i <= Nhi; i++) if (!sv[i]) for (long long jj = (long long)i * i; jj <= Nhi; jj += i) sv[jj] = 1;
    static int pra[MAXP], Epa[MAXP]; int npa = 0;
    for (int p = 2; p <= Nhi; p++) {
        if (sv[p]) continue;
        int emax = 0;
        for (int i = 0; i < cnt; i++) { int e = nu(el[i], p); if (e > emax) emax = e; }
        int fv = nu(VDEN, p); if (mode == 1 && fv > emax) emax = fv;
        if (emax == 0) continue;
        pra[npa] = p; Epa[npa] = emax; npa++;
    }
    { long long vv = VDEN; for (int k = 0; k < npa; k++) while (vv % pra[k] == 0) vv /= pra[k];
      if (mode == 1 && vv != 1) { printf("# target denominator has an unusable prime factor: NO SOLUTION\n"); return 0; } }
    for (int k = 0; k < npa; k++) {
        int p = pra[k], ex = Epa[k] - (mode == 1 ? 0 : fexp[p]);
        if (ex <= 0) continue;
        long long qq = 1; for (int t = 0; t < ex; t++) qq *= p;
        pr[np] = p; md[np] = qq; np++;
    }
    printf("# T=%d N=%d mode=%d |univ|=%d target=%lld/%lld tracked primes=%d\n",
           T0, Nhi, mode, cnt, UNUM, VDEN, np);

    for (int j = 0; j < np; j++) {
        long long mj = md[j];
        int p = pr[j], Ej = 0;
        for (int k = 0; k < npa; k++) if (pra[k] == p) Ej = Epa[k];
        long long cof = 1 % mj;
        for (int k = 0; k < npa; k++) { if (pra[k] == p) continue; cof = mulmod(cof, pw(pra[k], Epa[k], mj), mj); }
        wres[j] = malloc(sizeof(long long) * cnt);
        for (int i = 0; i < cnt; i++) {
            int a = nu(el[i], p);
            long long m = el[i]; for (int t = 0; t < a; t++) m /= p;
            long long x = mulmod(cof, inv_mod(m % mj, mj), mj);
            x = mulmod(x, pw(p, Ej - a, mj), mj);
            wres[j][i] = x;
        }
        if (mode == 1) {
            int a = nu(VDEN, p);
            long long m = VDEN; for (int t = 0; t < a; t++) m /= p;
            long long x = mulmod(cof, inv_mod(m % mj, mj), mj);
            x = mulmod(x, pw(p, Ej - a, mj), mj);
            tgt[j] = mulmod(x, UNUM % mj, mj);
        } else tgt[j] = 0;
    }

    for (int j = 0; j < np; j++) {
        long long mj = md[j];
        mrem[j] = malloc(sizeof(int) * (cnt + 1));
        mrem[j][cnt] = 0;
        for (int i = cnt - 1; i >= 0; i--) mrem[j][i] = mrem[j][i + 1] + (wres[j][i] != 0);
        int K = mrem[j][0];
        reach[j] = calloc((size_t)(K + 1) * mj, 1);
        if (!reach[j]) { fprintf(stderr, "OOM reach\n"); return 1; }
        reach[j][0] = 1;
        int k = 0;
        for (int i = cnt - 1; i >= 0; i--) {
            if (!wres[j][i]) continue;
            long long wv = wres[j][i];
            unsigned char *cur = reach[j] + (size_t)k * mj;
            unsigned char *nx = reach[j] + (size_t)(k + 1) * mj;
            for (long long r = 0; r < mj; r++) if (cur[r]) { nx[r] = 1; long long r2 = r + wv; if (r2 >= mj) r2 -= mj; nx[r2] = 1; }
            k++;
        }
    }
    for (int i = 0; i <= cnt; i++) {
        static int tmp[MAXP]; int c = 0;
        for (int j = 0; j < np; j++) {
            int need = (i == 0);
            if (i < cnt && wres[j][i]) need = 1;
            if (i > 0 && wres[j][i - 1]) need = 1;
            if (need) tmp[c++] = j;
        }
        chkcnt[i] = c; chk[i] = malloc(sizeof(int) * (c > 0 ? c : 1));
        memcpy(chk[i], tmp, sizeof(int) * c);
    }
    free(sv);

    SC = ((i128)1) << 96;
    for (int i = 0; i < cnt; i++) { i128 a = SC / el[i]; rlo[i] = a; rhi[i] = (SC % el[i]) ? a + 1 : a; }
    tailmax[cnt] = 0;
    for (int i = cnt - 1; i >= 0; i--) tailmax[i] = tailmax[i + 1] + rhi[i];
    i128 lo0 = 0, hi0 = 0;
    if (mode == 1) { u128 t = (u128)SC * (u128)UNUM; lo0 = (i128)(t / (u128)VDEN); hi0 = (t % (u128)VDEN) ? lo0 + 1 : lo0; }

    if (!budget) {
        for (int j = 0; j < np; j++) s[j] = 0;
        dfs(0, 0, lo0, hi0);
        printf("# done EXHAUSTIVE nodes=%lld results=%lld\n", nodes, nsolfound);
    } else {
        long long restarts = 0, tot = 0;
        while (!maxsol || nsolfound < maxsol) {
            nodes = 0; hitb = 0; nch = 0;
            for (int j = 0; j < np; j++) s[j] = 0;
            int st = dfs(0, 0, lo0, hi0);
            tot += nodes; restarts++;
            if (st && !hitb) break;
            if (!hitb) { printf("# tree exhausted: results=%lld nodes=%lld\n", nsolfound, tot); break; }
            if (restarts > 1000000000LL) break;
        }
        printf("# done restarts=%lld nodes=%lld results=%lld\n", restarts, tot, nsolfound);
    }
    return 0;
}
