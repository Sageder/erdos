/* P2_scan.c -- fast EXACT elimination scan for THE PIVOT.
 *
 * PIVOT: a covering system of Z, distinct moduli, every modulus in H\{2} = {m>=3 : 2m+1 prime}.
 * Any such covering has a finite lcm L; all moduli divide L; so it suffices to decide, for each L,
 *      S(L) = { m | L : m >= 3, 2m+1 prime }        (pivot pool on the lattice L)
 * and ask whether S(L) carries a covering.  Two PROVED necessary conditions are tested here:
 *
 *  (P1) BUDGET:  sum_{m in S(L)} 1/m > 1.
 *       (>= 1 is density; equality forces an exact cover, impossible with distinct moduli > 1.)
 *
 *  (P2) FIBER at a prime q:  with nu = nu_q, J = max_{m in S} nu(m), and for a residue
 *       assignment (b_m),  F_q(r) = sum_{m : b_m = r mod q^{nu(m)}} q^{nu(m)}/m   (r in Z/q^J),
 *       every covering has F_q(r) >= 1 for all r; hence
 *           Phi_q(S) := max_{assignments} min_r F_q(r)  >=  1.
 *       Phi_q is computed EXACTLY by branch and bound below.
 *
 * ALL ARITHMETIC IS EXACT INTEGER ARITHMETIC: every m divides L, so scale by L --
 * a term q^{nu(m)}/m becomes the integer (L/m)*q^{nu(m)}, and the threshold 1 becomes L.
 *
 * SCOPE DISCLAIMER (printed with every run): a KILL at L only says "no pivot covering has
 * lcm dividing L".  H\{2} is infinite; no finite list of killed lattices proves the pivot
 * negatively.  Route D's divergence barrier says a fixed finite prime set can never suffice.
 *
 * usage: ./P2_scan LMIN LMAX [--nodecap N] [--quiet]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

typedef long long ll;

static unsigned char *isp;     /* primality of odd-ish index up to 2*LMAX+1 */
static long LMAX;

/* ---------------- exact Phi_q branch and bound ---------------- */
#define MAXI 128
#define MAXF (1<<20)

static int    n_items;
static ll     it_w[MAXI];      /* scaled weight  (L/m)*q^j                 */
static int    it_lv[MAXI];     /* level j = nu_q(m)                        */
static long   it_blk[MAXI];    /* q^(J-j) : #fibers this item covers       */
static long   it_nodes[MAXI];  /* q^j : #choices at its level              */
static ll     suf_w[MAXI+1], suf_cov[MAXI+1];
static ll    *cur;             /* current fiber values, length F           */
static long   NF;
static ll     THR;
static ll     nodecount, NODECAP;
static int    capped;

static int rec(int i, int symfree)
{
    if (++nodecount > NODECAP) { capped = 1; return 0; }
    ll mn = cur[0];
    for (long r = 1; r < NF; r++) if (cur[r] < mn) mn = cur[r];
    if (mn >= THR) return 1;
    if (i == n_items) return 0;
    ll deficit = 0, worst = 0;
    for (long r = 0; r < NF; r++) {
        if (cur[r] < THR) {
            deficit += THR - cur[r];
            if (THR - cur[r] > worst) worst = THR - cur[r];
        }
    }
    if (deficit > suf_cov[i]) return 0;      /* aggregate prune              */
    if (worst   > suf_w[i])   return 0;      /* per-fiber prune              */
    ll w = it_w[i]; long blk = it_blk[i], nn = it_nodes[i];
    long limit = symfree ? 1 : nn;
    for (long b = 0; b < limit; b++) {
        for (long t = b*blk; t < (b+1)*blk; t++) cur[t] += w;
        if (rec(i+1, 0)) return 1;
        if (capped) return 0;
        for (long t = b*blk; t < (b+1)*blk; t++) cur[t] -= w;
    }
    return 0;
}

/* returns 1 = Phi_q >= T holds, 0 = proved < T, -1 = node cap (unknown) */
static int phi_at_least(long L, const long *S, int ns, long q, ll Tnum)
{
    int J = 0;
    for (int i = 0; i < ns; i++) { long m = S[i], j = 0; while (m % q == 0) { m /= q; j++; }
                                   if (j > J) J = (int)j; }
    ll base = 0;
    if (J == 0) {
        for (int i = 0; i < ns; i++) base += L / S[i];
        return base >= Tnum;
    }
    long F = 1; for (int i = 0; i < J; i++) { F *= q; if (F > MAXF) return -1; }
    n_items = 0;
    for (int i = 0; i < ns; i++) {
        long m = S[i], j = 0, qp = 1;
        while (m % q == 0) { m /= q; j++; qp *= q; }
        if (j == 0) { base += L / S[i]; continue; }
        if (n_items >= MAXI) return -1;
        it_w[n_items]  = (ll)(L / S[i]) * qp;
        it_lv[n_items] = (int)j;
        long blk = 1; for (long t = j; t < J; t++) blk *= q;
        it_blk[n_items]   = blk;
        it_nodes[n_items] = qp;
        n_items++;
    }
    /* sort items by decreasing weight (insertion sort, n small) */
    for (int i = 1; i < n_items; i++)
        for (int k = i; k > 0 && it_w[k] > it_w[k-1]; k--) {
            ll tw = it_w[k]; it_w[k] = it_w[k-1]; it_w[k-1] = tw;
            int tl = it_lv[k]; it_lv[k] = it_lv[k-1]; it_lv[k-1] = tl;
            long tb = it_blk[k]; it_blk[k] = it_blk[k-1]; it_blk[k-1] = tb;
            long tn = it_nodes[k]; it_nodes[k] = it_nodes[k-1]; it_nodes[k-1] = tn;
        }
    suf_w[n_items] = suf_cov[n_items] = 0;
    for (int i = n_items - 1; i >= 0; i--) {
        suf_w[i]   = suf_w[i+1]   + it_w[i];
        suf_cov[i] = suf_cov[i+1] + it_w[i] * (ll)it_blk[i];
    }
    NF = F; THR = Tnum; nodecount = 0; capped = 0;
    cur = (ll*)malloc(sizeof(ll)*F);
    for (long r = 0; r < F; r++) cur[r] = base;
    int ok = rec(0, 1);
    free(cur);
    if (capped) return -1;
    return ok;
}

/* ---------------- main scan ---------------- */
int main(int argc, char **argv)
{
    setbuf(stdout, NULL);
    long LMIN = 6; LMAX = 30000; NODECAP = 20000000; int quiet = 0;
    if (argc > 1) LMIN = atol(argv[1]);
    if (argc > 2) LMAX = atol(argv[2]);
    for (int i = 3; i < argc; i++) {
        if (!strcmp(argv[i], "--nodecap") && i+1 < argc) NODECAP = atoll(argv[++i]);
        if (!strcmp(argv[i], "--quiet")) quiet = 1;
    }
    long lim = 2*LMAX + 2;
    isp = (unsigned char*)malloc(lim+1);
    memset(isp, 1, lim+1); isp[0] = isp[1] = 0;
    for (long i = 2; i*i <= lim; i++) if (isp[i]) for (long j = i*i; j <= lim; j += i) isp[j] = 0;
    unsigned char *inH = (unsigned char*)malloc(LMAX+1);
    for (long m = 0; m <= LMAX; m++) inH[m] = (m >= 3 && isp[2*m+1]) ? 1 : 0;

    /* budget sieve in double, to find candidates cheaply; exact recheck per candidate */
    double *bud = (double*)calloc(LMAX+1, sizeof(double));
    for (long m = 3; m <= LMAX; m++) if (inH[m]) { double r = 1.0/m;
        for (long L = m; L <= LMAX; L += m) bud[L] += r; }

    printf("# P2 pivot elimination scan, lattices L in [%ld, %ld]\n", LMIN, LMAX);
    printf("# pool S(L) = {m | L : m>=3, 2m+1 prime};  tests: budget>1 and Phi_q>=1 for q | L\n");
    printf("# SCOPE: a KILL only rules out pivot coverings whose lcm divides L. Not a proof for H\\{2}.\n");

    long ncand = 0, nkill = 0, ncap = 0, nsurv = 0;
    long S[4096];
    for (long L = LMIN; L <= LMAX; L++) {
        if (bud[L] <= 1.0000000001) {
            if (bud[L] <= 1.0) continue;      /* budget kill (double, safe margin below) */
        }
        /* exact pool + exact budget */
        int ns = 0; ll sb = 0;
        for (long d = 1; (ll)d*d <= (ll)L; d++) if (L % d == 0) {
            long e = L/d;
            if (inH[d]) { S[ns++] = d; sb += L/d; }
            if (e != d && inH[e]) { S[ns++] = e; sb += L/e; }
        }
        if (ns == 0 || sb <= (ll)L) continue;
        ncand++;
        /* exact fiber tests at every prime q | L */
        int verdict = 0; long killq = 0, capq = 0;
        long t = L;
        for (long q = 2; q*q <= t; q++) if (t % q == 0) {
            while (t % q == 0) t /= q;
            int r = phi_at_least(L, S, ns, q, (ll)L);
            if (r == 0) { verdict = 1; killq = q; break; }
            if (r < 0)  { capq = q; }
        }
        if (!verdict && t > 1) {
            int r = phi_at_least(L, S, ns, t, (ll)L);
            if (r == 0) { verdict = 1; killq = t; }
            else if (r < 0) capq = t;
        }
        if (verdict) { nkill++; if (!quiet) printf("  L = %-8ld |S| = %3d budget %.5f  KILL Phi_%ld < 1\n",
                                                   L, ns, bud[L], killq); }
        else if (capq) { ncap++; printf("  L = %-8ld |S| = %3d budget %.5f  NODECAP q=%ld -> UNDECIDED\n",
                                        L, ns, bud[L], capq); }
        else { nsurv++; printf("  L = %-8ld |S| = %3d budget %.5f  SURVIVES ->  needs SAT   pool:",
                               L, ns, bud[L]);
               for (int i = 0; i < ns; i++) printf(" %ld", S[i]); printf("\n"); }
    }
    printf("\n# candidates(budget>1) = %ld ; fiber-killed = %ld ; nodecap = %ld ; SURVIVORS = %ld\n",
           ncand, nkill, ncap, nsurv);
    return 0;
}
