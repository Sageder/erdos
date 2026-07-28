/* P2_exact2.c -- EXACT decision of THE PIVOT on every divisor lattice L in a range (v2 prunes).
 *
 * Same statement and same pipeline as P2_exact.c:
 *   pivot pool  S(L) = {m | L : m >= MINM, 2m+1 prime};  decide whether Z/L is covered by
 *   distinct-moduli classes drawn from S(L).  MINM = 3 bans the modulus 2 (THE PIVOT).
 *
 * Stage 1 budget > 1, stage 2 exact Phi_q >= 1 for q | L, stage 3 exhaustive search.
 * v2 strengthens stage 3 with three extra PROVED upper bounds on the coverage still achievable
 * from the untouched suffix {m_i, ..., m_n} (any of them may be used or skipped):
 *
 *  (P1) RS[i] = sum_{k>=i} L/m_k                                       (trivial)
 *  (P2) CAP:  u <= sum_{k>=i} min(L/m_k, u)   -- a single class can never cover more than the
 *       u residues that are still uncovered.
 *  (P3) MATCH: fix once and for all a MATCHING M_i of pairwise-coprime pairs inside {m_i..m_n}.
 *       For a pair (m,m') with gcd = 1 the classes always meet in L/(mm') residues; and if one of
 *       the two is skipped we lose its whole L/m >= L/(mm').  Since M_i is a matching these losses
 *       are attached to disjoint pairs, so
 *            achievable coverage <= RS[i] - sum_{(m,m') in M_i} L/(m m').
 *  (P4) EXACT-MAX (shallow nodes only, work-capped): for each remaining k compute
 *       c_k = max_b #{uncovered residues in b mod m_k}; then u <= sum_k c_k.  This accounts for
 *       the real overlap with everything already placed and is by far the strongest bound.
 *
 * Reductions (soundness argued in P2_mdfs.c): translation-orbit normalisation of b_{m_i} into
 * [0, gcd(lcm(used so far), m_i)), and dropping classes that cover nothing new (dominated by SKIP).
 *
 * SCOPE: infeasibility at L excludes pivot coverings with lcm dividing L only.
 * usage: ./P2_exact2 LMIN LMAX [--minm M] [--nodes N] [--work W] [--verbose]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef unsigned long long u64;
typedef long long ll;

static long MINM = 3;
static int VERBOSE = 0;

/* ---------------------------------------------------------------- exact Phi_q, threshold 1 */
#define MAXI 200
static int  n_items;
static ll   it_w[MAXI];
static long it_blk[MAXI], it_nodes[MAXI];
static ll   suf_w[MAXI+1], suf_cov[MAXI+1];
static ll  *fcur; static long NF; static ll THR;
static ll   fnodes, FNODECAP; static int fcapped;

static int frec(int i, int symfree)
{
    if (++fnodes > FNODECAP) { fcapped = 1; return 0; }
    ll mn = fcur[0];
    for (long r = 1; r < NF; r++) if (fcur[r] < mn) mn = fcur[r];
    if (mn >= THR) return 1;
    if (i == n_items) return 0;
    ll deficit = 0, worst = 0;
    for (long r = 0; r < NF; r++) if (fcur[r] < THR) {
        deficit += THR - fcur[r];
        if (THR - fcur[r] > worst) worst = THR - fcur[r];
    }
    if (deficit > suf_cov[i] || worst > suf_w[i]) return 0;
    ll w = it_w[i]; long blk = it_blk[i], lim = symfree ? 1 : it_nodes[i];
    for (long b = 0; b < lim; b++) {
        for (long t = b*blk; t < (b+1)*blk; t++) fcur[t] += w;
        if (frec(i+1, 0)) return 1;
        if (fcapped) return 0;
        for (long t = b*blk; t < (b+1)*blk; t++) fcur[t] -= w;
    }
    return 0;
}

static int phi_ge1(long L, const long *S, int ns, long q)
{
    int J = 0;
    for (int i = 0; i < ns; i++) { long m = S[i], j = 0; while (m % q == 0) { m /= q; j++; }
                                  if (j > J) J = (int)j; }
    ll base = 0;
    if (J == 0) { for (int i = 0; i < ns; i++) base += L/S[i]; return base >= L; }
    long F = 1; for (int i = 0; i < J; i++) { F *= q; if (F > (1L<<20)) return -1; }
    n_items = 0;
    for (int i = 0; i < ns; i++) {
        long m = S[i], j = 0, qp = 1;
        while (m % q == 0) { m /= q; j++; qp *= q; }
        if (j == 0) { base += L/S[i]; continue; }
        if (n_items >= MAXI) return -1;
        it_w[n_items] = (ll)(L/S[i])*qp;
        long blk = 1; for (long t = j; t < J; t++) blk *= q;
        it_blk[n_items] = blk; it_nodes[n_items] = qp; n_items++;
    }
    for (int i = 1; i < n_items; i++)
        for (int k = i; k > 0 && it_w[k] > it_w[k-1]; k--) {
            ll tw=it_w[k]; it_w[k]=it_w[k-1]; it_w[k-1]=tw;
            long tb=it_blk[k]; it_blk[k]=it_blk[k-1]; it_blk[k-1]=tb;
            long tn=it_nodes[k]; it_nodes[k]=it_nodes[k-1]; it_nodes[k-1]=tn;
        }
    suf_w[n_items]=suf_cov[n_items]=0;
    for (int i = n_items-1; i >= 0; i--) {
        suf_w[i]=suf_w[i+1]+it_w[i];
        suf_cov[i]=suf_cov[i+1]+it_w[i]*(ll)it_blk[i];
    }
    NF=F; THR=L; fnodes=0; fcapped=0;
    fcur = malloc(sizeof(ll)*F);
    for (long r=0;r<F;r++) fcur[r]=base;
    int ok = frec(0,1);
    free(fcur);
    return fcapped ? -1 : ok;
}

/* --------------------------------------------------------------- exhaustive search, v2 prunes */
static long  L, NW;
static long  SS[256]; static int NS;
static ll    RS[257], UBM[257];      /* UBM[i] = RS[i] - matching correction */
static u64  *cov;
static long *undo; static long undo_top;
static int   chosen_b[256], sol_b[256];
static ll    snodes, SNODECAP; static int scapped;
static ll    WORK = 400000;
static int  *cnt;                    /* scratch for P4 */
static long *ulist;                  /* scratch list of uncovered residues */

static long gcdl(long a,long b){ while(b){long t=a%b;a=b;b=t;} return a; }

static int sdfs(int i, long u, long g)
{
    if (++snodes > SNODECAP) { scapped = 1; return 0; }
    if (u == 0) { for (int k=0;k<NS;k++) sol_b[k]=chosen_b[k]; return 1; }
    if (i == NS) return 0;
    if (u > RS[i] || u > UBM[i]) return 0;                       /* P1, P3 */
    { ll tot = 0;                                                /* P2 */
      for (int k = i; k < NS; k++) { ll c = L/SS[k]; tot += (c < u ? c : u); if (tot >= u) break; }
      if (tot < u) return 0; }
    if ((ll)(NS-i)*u <= WORK) {                                  /* P4 */
        long nu = 0;
        for (long w = 0; w < NW; w++) { u64 x = ~cov[w];
            while (x) { long t = (w<<6) + __builtin_ctzll(x); x &= x-1; if (t < L) ulist[nu++] = t; } }
        ll tot = 0;
        for (int k = i; k < NS && tot < u; k++) {
            long m = SS[k];
            memset(cnt, 0, sizeof(int)*m);
            long best = 0;
            for (long j = 0; j < nu; j++) { long v = ++cnt[ulist[j] % m]; if (v > best) best = v; }
            tot += best;
        }
        if (tot < u) return 0;
    }
    long m = SS[i], lim = gcdl(g,m);
    for (long b = 0; b < lim; b++) {
        long mark = undo_top, gained = 0;
        for (long t = b; t < L; t += m) { u64 msk = 1ULL<<(t&63);
            if (!(cov[t>>6]&msk)) { cov[t>>6]|=msk; undo[undo_top++]=t; gained++; } }
        if (gained) {
            chosen_b[i] = (int)b;
            if (sdfs(i+1, u-gained, (g/gcdl(g,m))*m)) return 1;
        }
        while (undo_top > mark) { long t = undo[--undo_top]; cov[t>>6] &= ~(1ULL<<(t&63)); }
        if (scapped) return 0;
    }
    chosen_b[i] = -1;
    return sdfs(i+1, u, g);
}

int main(int argc, char **argv)
{
    setbuf(stdout, NULL);
    long LMIN = 6, LMAX = 30000;
    SNODECAP = 2000000000LL; FNODECAP = 20000000LL;
    if (argc > 1) LMIN = atol(argv[1]);
    if (argc > 2) LMAX = atol(argv[2]);
    for (int i = 3; i < argc; i++) {
        if (!strcmp(argv[i],"--minm") && i+1<argc) MINM = atol(argv[++i]);
        if (!strcmp(argv[i],"--nodes") && i+1<argc) SNODECAP = atoll(argv[++i]);
        if (!strcmp(argv[i],"--work") && i+1<argc) WORK = atoll(argv[++i]);
        if (!strcmp(argv[i],"--verbose")) VERBOSE = 1;
    }
    long lim = 2*LMAX+2;
    unsigned char *isp = malloc(lim+1); memset(isp,1,lim+1); isp[0]=isp[1]=0;
    for (long i=2;i*i<=lim;i++) if (isp[i]) for (long j=i*i;j<=lim;j+=i) isp[j]=0;
    unsigned char *inH = malloc(LMAX+1);
    for (long m=0;m<=LMAX;m++) inH[m] = (m>=MINM && isp[2*m+1]);
    double *bud = calloc(LMAX+1,sizeof(double));
    for (long m=MINM;m<=LMAX;m++) if (inH[m]) { double r=1.0/m; for (long t=m;t<=LMAX;t+=m) bud[t]+=r; }
    cnt   = malloc(sizeof(int)*(LMAX+2));
    ulist = malloc(sizeof(long)*(LMAX+2));

    printf("# P2_exact2  L in [%ld,%ld]  minm = %ld  nodecap %lld  work %lld\n",
           LMIN, LMAX, MINM, SNODECAP, WORK);
    printf("# minm=3 is THE PIVOT (modulus 2 banned). SCOPE: infeasibility at L excludes pivot\n"
           "# coverings with lcm | L only; H\\{2} is infinite so this is never a proof of the pivot.\n");
    long ncand=0, nfib=0, nsearch=0, ncap=0, nsat=0;
    ll worst_nodes = 0; long worst_L = 0;
    long S[8192];
    for (L = LMIN; L <= LMAX; L++) {
        if (bud[L] <= 1.0) continue;
        int ns = 0; ll sb = 0;
        for (long d = 1; d*d <= L; d++) if (L % d == 0) { long e = L/d;
            if (inH[d]) { S[ns++]=d; sb += L/d; }
            if (e!=d && inH[e]) { S[ns++]=e; sb += L/e; } }
        if (!ns || sb <= (ll)L) continue;
        ncand++;
        for (int i=1;i<ns;i++) for (int k=i;k>0&&S[k]<S[k-1];k--){long t=S[k];S[k]=S[k-1];S[k-1]=t;}
        int killed = 0; long killq = 0, t = L;
        for (long q = 2; q*q <= t; q++) if (t % q == 0) {
            while (t % q == 0) t /= q;
            if (phi_ge1(L, S, ns, q) == 0) { killed = 1; killq = q; break; } }
        if (!killed && t > 1 && phi_ge1(L, S, ns, t) == 0) { killed=1; killq=t; }
        if (killed) { nfib++;
            if (VERBOSE) printf("  L=%-8ld |S|=%3d bud %.5f  INFEASIBLE (Phi_%ld < 1)\n",L,ns,bud[L],killq);
            continue; }
        NS = ns; for (int i=0;i<ns;i++) SS[i]=S[i];
        RS[NS]=0; for (int i=NS-1;i>=0;i--) RS[i]=RS[i+1]+L/SS[i];
        /* greedy matching correction per suffix */
        for (int i = 0; i <= NS; i++) UBM[i] = RS[i];
        for (int i = 0; i < NS; i++) {
            char taken[256]; memset(taken,0,sizeof(taken));
            ll corr = 0;
            for (;;) {
                ll best = 0; int ba=-1, bb=-1;
                for (int a=i;a<NS;a++) if (!taken[a]) for (int c=a+1;c<NS;c++) if (!taken[c])
                    if (gcdl(SS[a],SS[c])==1) { ll v = (ll)L/(SS[a]*SS[c]);
                        if (v > best) { best=v; ba=a; bb=c; } }
                if (best <= 0) break;
                corr += best; taken[ba]=taken[bb]=1;
            }
            UBM[i] = RS[i] - corr;
        }
        NW = (L+63)/64;
        cov = calloc(NW, sizeof(u64));
        undo = malloc(sizeof(long)*(L+2)); undo_top = 0;
        long pad = NW*64 - L; if (pad) cov[NW-1] |= (~0ULL) << (64-pad);
        snodes = 0; scapped = 0;
        int found = sdfs(0, L, 1);
        if (snodes > worst_nodes) { worst_nodes = snodes; worst_L = L; }
        if (found) { nsat++;
            printf("*** SAT *** L = %ld  |S| = %d  budget %.6f  PIVOT CERTIFICATE:", L, ns, bud[L]);
            for (int i=0;i<NS;i++) if (sol_b[i]>=0) printf(" %d(mod %ld)", sol_b[i], SS[i]);
            printf("\n");
        } else if (scapped) { ncap++;
            printf("  L=%-8ld |S|=%3d bud %.5f  NODE CAP -- UNDECIDED\n", L, ns, bud[L]);
        } else { nsearch++;
            printf("  L=%-8ld |S|=%3d bud %.5f  INFEASIBLE by exhaustive search (%lld nodes)\n",
                   L, ns, bud[L], snodes); }
        free(cov); free(undo);
    }
    printf("\n# range [%ld,%ld]: candidates = %ld ; fiber-infeasible = %ld ; search-infeasible = %ld ;"
           " node caps = %ld ; SAT = %ld\n", LMIN, LMAX, ncand, nfib, nsearch, ncap, nsat);
    printf("# hardest search: L = %ld with %lld nodes\n", worst_L, worst_nodes);
    return 0;
}
