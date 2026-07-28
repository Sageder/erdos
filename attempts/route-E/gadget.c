/* gadget.c -- find LEGAL systems inside a window whose reciprocal sum has a
 *             B-SMOOTH DENOMINATOR (no exact value prescribed).
 *
 * Input problem file:
 *      line 1:  T N B
 *      line 2:  cnt
 *      line 3:  n_1 ... n_cnt      (the pruned universe, increasing)
 *
 * Let L = lcm(universe) = prod_p p^{E_p}, D = prod_{p<=B} p^{E_p} (the B-smooth
 * part) and M = L/D = prod_{p>B} p^{E_p}.  For W subset universe put
 * S(W) = sum_{n in W} L/n, so sum_{n in W} 1/n = S(W)/L.  The denominator of
 * that fraction divides D  <==>  M | S(W).
 *
 * The engine therefore only has to track S mod p^{E_p} for the primes p > B --
 * every such modulus is <= N, i.e. a machine word.  NO big integers, NO floats.
 *
 * PRUNE (proved).  Fix a position i.  Every remaining weight L/n_j (j >= i) is
 * divisible by p^{E_p - m_p(i)} where m_p(i) = max_{j>=i} nu_p(n_j).  Hence the
 * yet-to-be-added part of S is  = 0 mod p^{E_p-m_p(i)}, so the partial sum must
 * satisfy   S_partial = 0  (mod p^{E_p - m_p(i)})   for every prime p > B.
 * At i = cnt this is exactly M | S.
 *
 * LEGALITY: no isolated point, enforced along the scan.
 *
 * usage: ./gadget probfile nsol budget seed [minlen]
 *        nsol   : stop after this many gadgets
 *        budget : nodes per randomised restart
 *        seed   : rng seed
 *        minlen : only report gadgets with >= minlen elements (default 2)
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXC 8000
#define MAXP 600

static int T0, Nhi, B, cnt;
static int el[MAXC], adj[MAXC];
static int np = 0, pr[MAXP], Ep[MAXP];
static long long q[MAXP];                 /* p^{E_p} */
static long long *wres[MAXP];             /* (L/n_i) mod q_p */
static long long *dv[MAXP];               /* p^{E_p - m_p(i)} */
static long long s[MAXP];
static int chosen[MAXC], nch = 0;
static long long nodes = 0, nsolfound = 0, maxsol = 100, budget = 1000000;
static int minlen = 2;
static unsigned long long rs = 1234567891234567ULL;
static int hitb = 0;

static unsigned long long xr(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
static int nu(long long n, int p) { int e = 0; while (n % p == 0) { n /= p; e++; } return e; }
static long long pw(long long a, long long e, long long m) {
    long long r = 1 % m; a %= m;
    while (e) { if (e & 1) r = (__int128)r * a % m; a = (__int128)a * a % m; e >>= 1; }
    return r;
}
static long long inv_mod(long long a, long long m) {
    /* m = p^k, a coprime to p: extended euclid */
    long long g = m, x = 0, x1 = 1, a1 = a % m;
    long long b = m;
    /* iterative extended gcd */
    long long old_r = a1, r = b, old_s = 1, sc = 0;
    while (r != 0) { long long qq = old_r / r; long long t = old_r - qq * r; old_r = r; r = t;
                     t = old_s - qq * sc; old_s = sc; sc = t; }
    (void)g; (void)x; (void)x1;
    long long res = old_s % m; if (res < 0) res += m;
    return res;
}

static void report(void) {
    if (nch < minlen) return;
    nsolfound++;
    printf("G");
    for (int i = 0; i < nch; i++) printf(" %d", chosen[i]);
    printf("\n"); fflush(stdout);
}

static int dfs(int i, int runlen) {
    nodes++;
    if (nodes > budget) { hitb = 1; return 1; }
    if (i > 0 && !adj[i]) { if (runlen == 1) return 0; runlen = 0; }
    for (int j = 0; j < np; j++) if (s[j] % dv[j][i]) return 0;
    if (i == cnt) {
        if (runlen != 1) { report(); if (nsolfound >= maxsol) return 1; }
        return 0;
    }
    int order = (int)(xr() & 1);
    for (int t = 0; t < 2; t++) {
        int take = (t == 0) ? (order == 0) : (order == 1);
        if (take) {
            for (int j = 0; j < np; j++) { s[j] += wres[j][i]; if (s[j] >= q[j]) s[j] -= q[j]; }
            chosen[nch++] = el[i];
            int st = dfs(i + 1, runlen + 1);
            nch--;
            for (int j = 0; j < np; j++) { s[j] -= wres[j][i]; if (s[j] < 0) s[j] += q[j]; }
            if (st) return 1;
        } else {
            if (runlen != 1) { if (dfs(i + 1, 0)) return 1; }
        }
    }
    return 0;
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: %s probfile [nsol budget seed minlen]\n", argv[0]); return 1; }
    FILE *f = fopen(argv[1], "r");
    if (!f) { perror("open"); return 1; }
    if (fscanf(f, "%d %d %d", &T0, &Nhi, &B) != 3) return 1;
    if (fscanf(f, "%d", &cnt) != 1) return 1;
    for (int i = 0; i < cnt; i++) if (fscanf(f, "%d", &el[i]) != 1) return 1;
    fclose(f);
    if (argc > 2) maxsol = atoll(argv[2]);
    if (argc > 3) budget = atoll(argv[3]);
    if (argc > 4) rs = strtoull(argv[4], NULL, 10) * 6364136223846793005ULL + 1442695040888963407ULL;
    if (argc > 5) minlen = atoi(argv[5]);

    adj[0] = 0;
    for (int i = 1; i < cnt; i++) adj[i] = (el[i] == el[i - 1] + 1);

    /* primes > B with a multiple in the universe */
    char *sv = calloc(Nhi + 1, 1);
    for (int i = 2; i <= Nhi; i++) if (!sv[i]) { for (long long j = (long long)i * i; j <= Nhi; j += i) sv[j] = 1; }
    for (int p = B + 1; p <= Nhi; p++) {
        if (sv[p]) continue;
        int emax = 0;
        for (int i = 0; i < cnt; i++) { int e = nu(el[i], p); if (e > emax) emax = e; }
        if (emax == 0) continue;
        pr[np] = p; Ep[np] = emax;
        long long qq = 1; for (int k = 0; k < emax; k++) qq *= p;
        q[np] = qq; np++;
        if (np >= MAXP) { fprintf(stderr, "too many primes\n"); return 1; }
    }
    /* also collect the smooth primes to know D (for reporting only) */
    printf("# T=%d N=%d B=%d |univ|=%d  rough primes(np)=%d :", T0, Nhi, B, cnt, np);
    for (int j = 0; j < np; j++) printf(" %d^%d", pr[j], Ep[j]);
    printf("\n");

    /* wres[j][i] = (L/n_i) mod q_j.
       L/n = prod_{p'} p'^{E_{p'} - a_{p'}}.  Mod q_j = p_j^{E_j}:
         = [ (L / p_j^{E_j}) mod q_j ] * inv( (n / p_j^{a_j}) mod q_j ) * p_j^{E_j - a_j}.
       (L / p_j^{E_j}) mod q_j is computed as a product over all other primes,
       including the smooth ones. */
    /* need E_p for ALL primes (smooth ones too) */
    int npa = 0; static int pra[MAXP], Epa[MAXP];
    for (int p = 2; p <= Nhi; p++) {
        if (sv[p]) continue;
        int emax = 0;
        for (int i = 0; i < cnt; i++) { int e = nu(el[i], p); if (e > emax) emax = e; }
        if (emax == 0) continue;
        pra[npa] = p; Epa[npa] = emax; npa++;
    }
    for (int j = 0; j < np; j++) {
        wres[j] = malloc(sizeof(long long) * cnt);
        dv[j] = malloc(sizeof(long long) * (cnt + 1));
        long long qj = q[j];
        long long cof = 1 % qj;
        for (int k = 0; k < npa; k++) {
            if (pra[k] == pr[j]) continue;
            cof = (__int128)cof * pw(pra[k], Epa[k], qj) % qj;
        }
        for (int i = 0; i < cnt; i++) {
            int a = nu(el[i], pr[j]);
            long long m = el[i];
            for (int k = 0; k < a; k++) m /= pr[j];
            long long t = (__int128)cof * inv_mod(m % qj, qj) % qj;
            t = (__int128)t * pw(pr[j], Epa[0] * 0 + (Ep[j] - a), qj) % qj;
            wres[j][i] = t;
        }
        for (int i = 0; i <= cnt; i++) {
            int me = 0;
            for (int k = i; k < cnt; k++) { int e = nu(el[k], pr[j]); if (e > me) me = e; }
            long long d = 1; for (int k = 0; k < Ep[j] - me; k++) d *= pr[j];
            dv[j][i] = d;
        }
    }
    free(sv);

    long long restarts = 0, tot = 0;
    while (nsolfound < maxsol) {
        nodes = 0; hitb = 0; nch = 0;
        for (int j = 0; j < np; j++) s[j] = 0;
        int st = dfs(0, 0);
        tot += nodes; restarts++;
        if (st && !hitb) break;
        if (!hitb) { printf("# tree exhausted, gadgets=%lld nodes=%lld\n", nsolfound, tot); break; }
        if (restarts > 20000000) break;
    }
    printf("# done restarts=%lld nodes=%lld gadgets=%lld\n", restarts, tot, nsolfound);
    return 0;
}
