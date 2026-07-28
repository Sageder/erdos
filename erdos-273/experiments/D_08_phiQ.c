/* D_08_phiQ.c   --  MULTI-PRIME fiber max-min  Phi_Q
 *
 * CLAIM.  Let Q = {q_1,...,q_t} be a set of primes, e_i = nu_{q_i}(lcm S), and for a residue
 * assignment (b_m) put, for r = (r_1,...,r_t) in prod_i Z_{q_i},
 *      F_Q(r) = sum_{m in S : b_m = r_i mod q_i^{nu_i(m)} for all i}  (prod_i q_i^{nu_i(m)}) / m .
 * PROOF that min_r F_Q(r) >= 1 for a covering system: the set {x = r_i mod q_i^{J_i} all i} is
 * an AP of modulus prod q_i^{J_i}; the class b_m mod m meets it iff b_m = r_i mod q_i^{nu_i(m)}
 * for all i, and then the intersection has relative density prod_i q_i^{nu_i(m)} / m.  Covering
 * forces the densities to sum to >= 1.
 * By the parity split (Prop. D1) an Erdos-273 covering is TWO DISJOINT coverings inside H, so
 *      Phi_Q(S) := max over assignments of min_r F_Q(r)   >=   2 .
 * Phi_Q is monotone in S and Phi_Q <= min_{q in Q} Phi_{q}: the multi-prime condition is
 * STRICTLY STRONGER than the one-prime condition.  For Q = all primes dividing lcm S it is
 * equivalent to the covering property itself, so this is a complete hierarchy.
 *
 * The optimisation: leaves = prod_i q_i^{e_i} cells; an item m has level vector
 * (nu_1(m),...,nu_t(m)), weight prod q_i^{nu_i}/m, and must be placed at one node of the
 * product tree, covering the corresponding "box" of leaves.  Maximise the minimum leaf.
 * Exact branch and bound.  Decision mode: with a target, answers  PHI_GE / PHI_LT.
 *
 * Usage: ./D_08_phiQ  t  q_1 e_1 ... q_t e_t  nitems nodecap target   < items
 *        stdin: first line "flat" (total weight of items with all nu_i = 0), then nitems
 *        lines "j_1 ... j_t weight".
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXT 4
#define MAXL 4096
#define MAXI 2048

static int t, q[MAXT], e[MAXT];
static int dimsize[MAXT];          /* q_i^{e_i} */
static int stride[MAXT];
static int NL;
static double flat;
static int n;
static int lev[MAXI][MAXT];
static double wt[MAXI];
static double cur[MAXL];
static double best, target = 0;
static long long nodes = 0, nodecap = 0;
static int aborted = 0, hit = 0;

/* placements of item i: nplace[i], and for each placement the list of leaves */
static int nplace[MAXI];
static int *plist[MAXI];           /* nplace[i] * blk[i] leaf indices */
static int blk[MAXI];

/* depth vectors for the bound */
static int ndv, dv[512][MAXT];
static double *SB[512];            /* SB[k][i] = suffix potential for depth vector k */
static int dvnodes[512], dvblk[512];

static int ipow(int a, int b){ int r = 1; while(b--) r *= a; return r; }

static void build_item(int i){
    int np = 1, bk = 1;
    for(int d = 0; d < t; d++){ np *= ipow(q[d], lev[i][d]); bk *= ipow(q[d], e[d]-lev[i][d]); }
    nplace[i] = np; blk[i] = bk;
    plist[i] = malloc(sizeof(int) * (size_t)np * bk);
    int idx[MAXT], v[MAXT];
    for(int p = 0; p < np; p++){
        int pp = p;
        for(int d = 0; d < t; d++){ int s = ipow(q[d], lev[i][d]); v[d] = pp % s; pp /= s; }
        /* enumerate leaves whose coord d = v[d] mod q_d^{lev} */
        int cnt = 0;
        for(int c = 0; c < bk; c++){
            int cc = c, leaf = 0;
            for(int d = 0; d < t; d++){
                int hi = ipow(q[d], e[d]-lev[i][d]);
                int k = cc % hi; cc /= hi;
                int coord = v[d] + k * ipow(q[d], lev[i][d]);
                leaf += coord * stride[d];
            }
            plist[i][p*bk + cnt++] = leaf;
        }
    }
}

static double boundf(int i){
    double ub = 1e18;
    for(int k = 0; k < ndv; k++){
        int nn = dvnodes[k], bk = dvblk[k];
        /* iterate nodes of this depth vector */
        int vv[MAXT];
        for(int p = 0; p < nn; p++){
            int pp = p, base = 0;
            for(int d = 0; d < t; d++){ int s = ipow(q[d], dv[k][d]); vv[d] = pp % s; pp /= s; }
            double s = 0;
            /* sum over leaves in this box */
            for(int c = 0; c < bk; c++){
                int cc = c, leaf = 0;
                for(int d = 0; d < t; d++){
                    int hi = ipow(q[d], e[d]-dv[k][d]);
                    int kk = cc % hi; cc /= hi;
                    leaf += (vv[d] + kk*ipow(q[d], dv[k][d])) * stride[d];
                }
                s += cur[leaf];
            }
            (void)base;
            double u = (s + SB[k][i]) / bk;
            if(u < ub) ub = u;
        }
    }
    return ub;
}

static void dfs(int i){
    if(aborted) return;
    if(nodecap && ++nodes > nodecap){ aborted = 1; return; }
    if(i == n){
        double mn = 1e18;
        for(int l = 0; l < NL; l++) if(cur[l] < mn) mn = cur[l];
        if(mn > best) best = mn;
        if(target > 0 && mn >= target){ hit = 1; aborted = 1; }
        return;
    }
    if(boundf(i) <= best + 1e-12) return;
    int np = (i == 0) ? 1 : nplace[i], bk = blk[i];
    /* greedy placement ordering: try the box with the smallest (min, sum) first.  This makes
       the leftmost DFS descent equal to the LPT greedy, so satisfiable instances are found
       immediately; it also improves pruning on unsatisfiable ones. */
    int ord[4096];
    double key1[4096], key2[4096];
    for(int p = 0; p < np; p++){
        int *L = plist[i] + (size_t)p*bk;
        double mn = 1e18, sm = 0;
        for(int c = 0; c < bk; c++){ double x = cur[L[c]]; sm += x; if(x < mn) mn = x; }
        key1[p] = mn; key2[p] = sm; ord[p] = p;
    }
    for(int a = 0; a < np; a++) for(int b = a+1; b < np; b++){
        int x = ord[a], y = ord[b];
        if(key1[y] < key1[x] || (key1[y] == key1[x] && key2[y] < key2[x])){ ord[a]=y; ord[b]=x; }
    }
    for(int pi = 0; pi < np; pi++){
        int p = ord[pi];
        int *L = plist[i] + (size_t)p*bk;
        for(int c = 0; c < bk; c++) cur[L[c]] += wt[i];
        dfs(i+1);
        for(int c = 0; c < bk; c++) cur[L[c]] -= wt[i];
        if(aborted) return;
    }
}

int main(int argc, char **argv){
    if(argc < 2) return 1;
    t = atoi(argv[1]);
    if(t > MAXT) return 1;
    for(int d = 0; d < t; d++){ q[d] = atoi(argv[2+2*d]); e[d] = atoi(argv[3+2*d]); }
    n = atoi(argv[2+2*t]);
    nodecap = atoll(argv[3+2*t]);
    target = atof(argv[4+2*t]);
    NL = 1;
    for(int d = 0; d < t; d++){ dimsize[d] = ipow(q[d], e[d]); stride[d] = NL; NL *= dimsize[d]; }
    if(NL > MAXL){ fprintf(stderr,"NL=%d too big\n", NL); return 1; }
    if(scanf("%lf",&flat)!=1) return 1;
    for(int i = 0; i < n; i++){
        for(int d = 0; d < t; d++) if(scanf("%d",&lev[i][d])!=1) return 1;
        if(scanf("%lf",&wt[i])!=1) return 1;
    }
    /* sort by decreasing weight */
    for(int i = 0; i < n; i++) for(int k = i+1; k < n; k++) if(wt[k] > wt[i]){
        double tw = wt[i]; wt[i]=wt[k]; wt[k]=tw;
        for(int d = 0; d < t; d++){ int tl = lev[i][d]; lev[i][d]=lev[k][d]; lev[k][d]=tl; }
    }
    for(int i = 0; i < n; i++) build_item(i);
    /* depth vectors */
    ndv = 0;
    int dd[MAXT] = {0};
    while(1){
        for(int d = 0; d < t; d++) dv[ndv][d] = dd[d];
        int nn = 1, bk = 1;
        for(int d = 0; d < t; d++){ nn *= ipow(q[d], dd[d]); bk *= ipow(q[d], e[d]-dd[d]); }
        dvnodes[ndv] = nn; dvblk[ndv] = bk;
        ndv++;
        int d = 0;
        while(d < t && dd[d] == e[d]){ dd[d] = 0; d++; }
        if(d == t) break;
        dd[d]++;
        if(ndv >= 512) break;
    }
    for(int k = 0; k < ndv; k++){
        SB[k] = malloc(sizeof(double)*(n+1));
        SB[k][n] = 0;
        for(int i = n-1; i >= 0; i--){
            double c = 1;
            for(int d = 0; d < t; d++){
                int mx = lev[i][d] > dv[k][d] ? lev[i][d] : dv[k][d];
                c *= ipow(q[d], e[d]-mx);
            }
            SB[k][i] = SB[k][i+1] + wt[i]*c;
        }
    }
    for(int l = 0; l < NL; l++) cur[l] = flat;
    best = (target > 0) ? target - 1e-9 : -1e18;
    dfs(0);
    if(target > 0){
        if(hit)          printf("PHI_GE %.9f nodes %lld\n", target, nodes);
        else if(aborted) printf("PHI_UNKNOWN nodes %lld\n", nodes);
        else             printf("PHI_LT %.9f nodes %lld\n", target, nodes);
    } else if(aborted)   printf("PHI_UNKNOWN best_so_far %.9f\n", best);
    else                 printf("PHI %.9f nodes %lld\n", best, nodes);
    return 0;
}
