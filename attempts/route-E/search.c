/* search.c -- exact search for LEGAL systems inside a far-out window [T,N].
 *
 *  MODE 1 (exact):   find W subset universe, legal, with sum_{n in W} 1/n = u/v.
 *  MODE 0 (gadget):  find W subset universe, legal, whose reciprocal sum has a
 *                    B-SMOOTH DENOMINATOR (no value prescribed).
 *
 * =====================  ARITHMETIC  =====================
 * L := lcm(universe)  (times the extra prime powers needed so that v | L).
 * L = prod_p p^{E_p}.  For W subset universe let S(W) = sum_{n in W} L/n, so
 * sum_{n in W} 1/n = S(W)/L.  We NEVER form L: we track S only through its
 * residues  s_p := S mod p^{E_p}, one machine word per prime.
 *   - MODE 1 target:  S = R0 := (L/v)*u,  i.e. s_p = R0 mod p^{E_p} for all p.
 *   - MODE 0 target:  s_p = 0 for every p > B (nothing required for p <= B).
 * Everything is exact integer arithmetic; the only auxiliary floating-free
 * "magnitude" data is a pair of INTEGER fixed-point bounds (scale 2^96) with
 * directed rounding, used solely for the (conservative) size prune.
 *
 * KEY OBSERVATION.  If p^{E_p} || L and p does not divide n, then p^{E_p} | L/n,
 * so s_p is only moved by the elements divisible by p.  Hence the constraint at
 * p involves only the multiples of p.
 *
 * =====================  PRUNES (all proved)  =====================
 * (P1) size:  0 <= rho - (partial sum) <= sum of 1/n over the remaining
 *      universe.  Checked with conservative integer fixed-point bounds.
 * (P2) per-prime ARC CONSISTENCY.  For a prime p and a position i let
 *          A(p,i) := { sum_{j in J} (L/n_j) mod p^{E_p} : J subset {j>=i} }
 *      (a subset-sum reachability set mod p^{E_p}, computed once by a backward
 *      DP; only the multiples of p contribute).  A completion of the current
 *      partial choice must add an element of A(p,i) to s_p and land on the
 *      target, so we prune unless  (target_p - s_p) mod p^{E_p}  lies in A(p,i).
 *      This is strictly stronger than the usual "Q[i] divides R" prune, which
 *      is the special case "A(p,i) is contained in p^{E_p-m} Z".
 *      A(p,i) changes only at positions i with p | n_i, and s_p changes only
 *      when a multiple of p is taken, so the test is performed only at those
 *      positions -- O(few) work per node.
 *
 * LEGALITY: W has no isolated point; enforced along the scan (runlen state).
 *
 * usage:  ./search probfile mode nsol budget seed
 *   probfile:   line1 "T N B u v"  ; line2 cnt ; line3 the pruned universe
 *   mode:       0 = gadget (smooth denominator), 1 = exact target u/v
 *   nsol:       stop after this many results (0 = all: exhaustive)
 *   budget:     nodes per randomised restart (0 = exhaustive, no restarts)
 *   seed:       rng seed
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef __int128 i128;
typedef unsigned __int128 u128;

#define MAXC 40000
#define MAXP 800

static int T0, Nhi, Bs, cnt, mode;
static long long UNUM, VDEN;
static int el[MAXC], adj[MAXC];
static int np = 0, pr[MAXP], Ep[MAXP];
static long long q[MAXP], tgt[MAXP];
static long long *wres[MAXP];        /* (L/n_i) mod q_j, indexed by i */
static unsigned char *reach[MAXP];   /* reach[j][k*q_j + r] : r in A(p_j, pos with k remaining multiples) */
static int *mrem[MAXP];              /* mrem[j][i] = #multiples of p_j at positions >= i */
static long long s[MAXP];
static int chkcnt[MAXC + 1], *chk[MAXC + 1];
static int chosen[MAXC], nch = 0;

static i128 SC;                      /* 2^96 */
static i128 rlo[MAXC], rhi[MAXC];    /* floor/ceil of SC/n_i */
static i128 tailmax[MAXC + 1];
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
    long long old_r = a % m, r = m, old_s = 1, sc = 0;
    while (r != 0) { long long qq = old_r / r, t;
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
    if (mode == 1) {
        if (hi < 0) return 0;
        if (lo > tailmax[i]) return 0;
    }
    for (int t = 0; t < chkcnt[i]; t++) {
        int j = chk[i][t];
        long long need = tgt[j] - s[j]; if (need < 0) need += q[j];
        if (!reach[j][(long long)mrem[j][i] * q[j] + need]) return 0;
    }
    if (i == cnt) {
        if (runlen != 1 && nch > 0) {
            if (mode == 1) {
                /* residues already force  rho - sum  to be an integer; the size
                   bounds force |rho - sum| < 1/2, hence rho - sum = 0. */
                if (lo > SC / 2 || hi < -(SC / 2)) return 0;
            }
            report();
            if (maxsol && nsolfound >= maxsol) return 1;
        }
        return 0;
    }
    int order = (int)(xr() & 1);
    for (int t = 0; t < 2; t++) {
        int take = (t == 0) ? (order == 0) : (order == 1);
        if (take) {
            for (int j = 0; j < np; j++) if (wres[j][i]) { s[j] += wres[j][i]; if (s[j] >= q[j]) s[j] -= q[j]; }
            chosen[nch++] = el[i];
            int st = dfs(i + 1, runlen + 1, lo - rhi[i], hi - rlo[i]);
            nch--;
            for (int j = 0; j < np; j++) if (wres[j][i]) { s[j] -= wres[j][i]; if (s[j] < 0) s[j] += q[j]; }
            if (st) return 1;
        } else {
            if (runlen != 1) { if (dfs(i + 1, 0, lo, hi)) return 1; }
        }
    }
    return 0;
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: %s probfile mode [nsol budget seed]\n", argv[0]); return 1; }
    FILE *f = fopen(argv[1], "r");
    if (!f) { perror("open"); return 1; }
    if (fscanf(f, "%d %d %d %lld %lld", &T0, &Nhi, &Bs, &UNUM, &VDEN) != 5) { fprintf(stderr, "bad header\n"); return 1; }
    if (fscanf(f, "%d", &cnt) != 1) return 1;
    for (int i = 0; i < cnt; i++) if (fscanf(f, "%d", &el[i]) != 1) return 1;
    fclose(f);
    mode = atoi(argv[2]);
    if (argc > 3) maxsol = atoll(argv[3]);
    if (argc > 4) budget = atoll(argv[4]);
    if (argc > 5) rs = strtoull(argv[5], NULL, 10) * 6364136223846793005ULL + 1442695040888963407ULL;

    adj[0] = 0;
    for (int i = 1; i < cnt; i++) adj[i] = (el[i] == el[i - 1] + 1);

    /* --- all primes with E_p >= 1 (needed for L), and the tracked subset --- */
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
      if (mode == 1 && vv != 1) { printf("# target denominator has a prime factor with no room: NO SOLUTION\n"); return 0; } }
    for (int k = 0; k < npa; k++) {
        if (mode == 0 && pra[k] <= Bs) continue;
        pr[np] = pra[k]; Ep[np] = Epa[k];
        long long qq = 1; for (int t = 0; t < Epa[k]; t++) qq *= pra[k];
        q[np] = qq; np++;
    }
    printf("# T=%d N=%d B=%d mode=%d |univ|=%d target=%lld/%lld tracked primes=%d\n",
           T0, Nhi, Bs, mode, cnt, UNUM, VDEN, np);

    /* --- weights mod q_j and targets --- */
    for (int j = 0; j < np; j++) {
        long long qj = q[j];
        long long cof = 1 % qj;
        for (int k = 0; k < npa; k++) { if (pra[k] == pr[j]) continue; cof = mulmod(cof, pw(pra[k], Epa[k], qj), qj); }
        wres[j] = malloc(sizeof(long long) * cnt);
        for (int i = 0; i < cnt; i++) {
            int a = nu(el[i], pr[j]);
            long long m = el[i]; for (int t = 0; t < a; t++) m /= pr[j];
            long long x = mulmod(cof, inv_mod(m % qj, qj), qj);
            x = mulmod(x, pw(pr[j], Ep[j] - a, qj), qj);
            wres[j][i] = x;
        }
        if (mode == 1) {
            int a = nu(VDEN, pr[j]);
            long long m = VDEN; for (int t = 0; t < a; t++) m /= pr[j];
            long long x = mulmod(cof, inv_mod(m % qj, qj), qj);      /* (L/v) mod qj, part 1 */
            x = mulmod(x, pw(pr[j], Ep[j] - a, qj), qj);
            tgt[j] = mulmod(x, UNUM % qj, qj);
        } else tgt[j] = 0;
    }

    /* --- reachability tables --- */
    for (int j = 0; j < np; j++) {
        long long qj = q[j];
        mrem[j] = malloc(sizeof(int) * (cnt + 1));
        mrem[j][cnt] = 0;
        for (int i = cnt - 1; i >= 0; i--) mrem[j][i] = mrem[j][i + 1] + (wres[j][i] != 0);
        int K = mrem[j][0];
        reach[j] = calloc((size_t)(K + 1) * qj, 1);
        reach[j][0 * qj + 0] = 1;                        /* k=0 remaining: only 0 */
        int k = 0;
        for (int i = cnt - 1; i >= 0; i--) {
            if (!wres[j][i]) continue;
            long long wv = wres[j][i];
            unsigned char *cur = reach[j] + (size_t)k * qj;
            unsigned char *nx = reach[j] + (size_t)(k + 1) * qj;
            for (long long r = 0; r < qj; r++) if (cur[r]) { nx[r] = 1; long long r2 = r + wv; if (r2 >= qj) r2 -= qj; nx[r2] = 1; }
            k++;
        }
    }
    /* --- check lists --- */
    for (int i = 0; i <= cnt; i++) {
        int tmp[MAXP], c = 0;
        for (int j = 0; j < np; j++) {
            int need = 0;
            if (i < cnt && wres[j][i]) need = 1;
            if (i > 0 && wres[j][i - 1]) need = 1;
            if (i == 0) need = 1;
            if (need) tmp[c++] = j;
        }
        chkcnt[i] = c; chk[i] = malloc(sizeof(int) * (c > 0 ? c : 1));
        memcpy(chk[i], tmp, sizeof(int) * c);
    }

    /* --- fixed-point magnitudes --- */
    SC = ((i128)1) << 96;
    for (int i = 0; i < cnt; i++) { i128 a = SC / el[i]; rlo[i] = a; rhi[i] = (SC % el[i]) ? a + 1 : a; }
    tailmax[cnt] = 0;
    for (int i = cnt - 1; i >= 0; i--) tailmax[i] = tailmax[i + 1] + rhi[i];
    i128 lo0 = 0, hi0 = 0;
    if (mode == 1) { u128 t = (u128)SC * (u128)UNUM; lo0 = (i128)(t / (u128)VDEN); hi0 = (t % (u128)VDEN) ? lo0 + 1 : lo0; }

    long long restarts = 0, tot = 0;
    if (!budget) {
        for (int j = 0; j < np; j++) s[j] = 0;
        dfs(0, 0, lo0, hi0);
        printf("# done EXHAUSTIVE nodes=%lld results=%lld\n", nodes, nsolfound);
    } else {
        while (!maxsol || nsolfound < maxsol) {
            nodes = 0; hitb = 0; nch = 0;
            for (int j = 0; j < np; j++) s[j] = 0;
            int st = dfs(0, 0, lo0, hi0);
            tot += nodes; restarts++;
            if (st && !hitb) break;
            if (!hitb) { printf("# tree exhausted: results=%lld nodes=%lld\n", nsolfound, tot); break; }
            if (restarts > 100000000LL) break;
        }
        printf("# done restarts=%lld nodes=%lld results=%lld\n", restarts, tot, nsolfound);
    }
    return 0;
}
