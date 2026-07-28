/* P2_gap.c -- HOW CLOSE does the pivot pool get?  Exact maximum coverage on a lattice.
 *
 * For S(L) = {m | L : m >= MINM, 2m+1 prime} this computes EXACTLY
 *      gap(L) = min over choices of distinct-moduli classes from S(L) of #uncovered residues in Z/L
 * (gap = 0 would be a pivot certificate).  Branch and bound: same search as P2_exact2 but keeping
 * the best (smallest) uncovered count instead of stopping at 0, pruning a node when
 *      u - UB(i)  >=  best,      UB(i) = upper bound on further coverage from {m_i..m_n},
 * with UB the minimum of the same three proved bounds used in P2_exact2 (RS, per-class cap, and
 * the exact max-over-classes bound).  Translation normalisation and SKIP-dominance are valid for
 * maximum coverage exactly as for feasibility (coverage is translation invariant, and a class
 * covering nothing new can be deleted without lowering the coverage).
 *
 * Reporting gap(L)/L says how far the H\{2} pool is from covering -- a number, not a proof.
 * usage: ./P2_gap L [L2 ...] [--minm M] [--nodes N] [--work W]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef unsigned long long u64;
typedef long long ll;

static long L, NW, MINM = 3;
static long SS[512]; static int NS;
static ll   RS[513];
static u64 *cov;
static long *undo; static long undo_top;
static int  chosen_b[512], sol_b[512];
static ll   nodes, NODECAP; static int capped;
static ll   WORK = 2000000;
static int *cnt; static long *ulist;
static long best;

static long gcdl(long a,long b){ while(b){long t=a%b;a=b;b=t;} return a; }

static void rec(int i, long u, long g)
{
    if (++nodes > NODECAP) { capped = 1; return; }
    if (u < best) { best = u; for (int k=0;k<NS;k++) sol_b[k]=chosen_b[k];
                    printf("    ... best uncovered so far: %ld / %ld  (%.5f%%)\n",
                           best, L, 100.0*best/L); }
    if (best == 0 || i == NS) return;
    ll ub = RS[i];
    { ll tot = 0; for (int k=i;k<NS;k++){ ll c=L/SS[k]; tot += (c<u?c:u);} if (tot<ub) ub=tot; }
    if (u - ub >= best) return;
    if ((ll)(NS-i)*u <= WORK) {
        long nu = 0;
        for (long w=0; w<NW; w++) { u64 x=~cov[w];
            while (x) { long t=(w<<6)+__builtin_ctzll(x); x&=x-1; if (t<L) ulist[nu++]=t; } }
        ll tot = 0;
        for (int k=i;k<NS;k++) { long m=SS[k]; memset(cnt,0,sizeof(int)*m); long bst=0;
            for (long j=0;j<nu;j++){ long v=++cnt[ulist[j]%m]; if(v>bst) bst=v; } tot+=bst; }
        if (tot < ub) ub = tot;
        if (u - ub >= best) return;
    }
    long m = SS[i], lim = gcdl(g,m);
    for (long b = 0; b < lim; b++) {
        long mark = undo_top, gained = 0;
        for (long t = b; t < L; t += m) { u64 msk = 1ULL<<(t&63);
            if (!(cov[t>>6]&msk)) { cov[t>>6]|=msk; undo[undo_top++]=t; gained++; } }
        if (gained) { chosen_b[i]=(int)b; rec(i+1, u-gained, (g/gcdl(g,m))*m); }
        while (undo_top > mark) { long t=undo[--undo_top]; cov[t>>6] &= ~(1ULL<<(t&63)); }
        if (capped || best == 0) return;
    }
    chosen_b[i] = -1;
    rec(i+1, u, g);
}

int main(int argc, char **argv)
{
    setbuf(stdout, NULL);
    long Ls[64]; int nL = 0;
    NODECAP = 3000000000LL;
    for (int i = 1; i < argc; i++) {
        if (!strcmp(argv[i],"--minm") && i+1<argc) { MINM = atol(argv[++i]); continue; }
        if (!strcmp(argv[i],"--nodes") && i+1<argc) { NODECAP = atoll(argv[++i]); continue; }
        if (!strcmp(argv[i],"--work") && i+1<argc) { WORK = atoll(argv[++i]); continue; }
        Ls[nL++] = atol(argv[i]);
    }
    long MX = 0; for (int i=0;i<nL;i++) if (Ls[i] > MX) MX = Ls[i];
    long lim = 2*MX+2;
    unsigned char *isp = malloc(lim+1); memset(isp,1,lim+1); isp[0]=isp[1]=0;
    for (long i=2;i*i<=lim;i++) if (isp[i]) for (long j=i*i;j<=lim;j+=i) isp[j]=0;
    cnt = malloc(sizeof(int)*(MX+2)); ulist = malloc(sizeof(long)*(MX+2));
    for (int t = 0; t < nL; t++) {
        L = Ls[t];
        NS = 0; for (long d=1; d<=L; d++) if (L%d==0 && d>=MINM && isp[2*d+1]) SS[NS++]=d;
        RS[NS]=0; for (int i=NS-1;i>=0;i--) RS[i]=RS[i+1]+L/SS[i];
        NW = (L+63)/64;
        cov = calloc(NW,sizeof(u64)); undo = malloc(sizeof(long)*(L+2)); undo_top=0;
        long pad = NW*64-L; if (pad) cov[NW-1] |= (~0ULL) << (64-pad);
        best = L; nodes = 0; capped = 0;
        printf("L = %ld  minm = %ld  |S| = %d  budget = %.6f\n", L, MINM, NS, (double)RS[0]/L);
        rec(0, L, 1);
        if (capped) printf("  NODE CAP -- best found (upper bound on gap): %ld / %ld = %.5f%%\n",
                           best, L, 100.0*best/L);
        else {
            printf("  EXACT gap(%ld) = %ld uncovered out of %ld  (%.5f%% of Z/L unreachable)"
                   "   nodes = %lld\n", L, best, L, 100.0*best/L, nodes);
            printf("  optimum:");
            for (int i=0;i<NS;i++) if (sol_b[i]>=0) printf(" %d(mod %ld)", sol_b[i], SS[i]);
            printf("\n");
        }
        free(cov); free(undo);
    }
    return 0;
}
