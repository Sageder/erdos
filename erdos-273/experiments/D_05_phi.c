/* D_05_phi.c
 *
 * CLAIM TESTED.  For a finite S subset of H = {m>=2 : 2m+1 prime}, a prime q, and
 * e = nu_q(lcm S), define for a residue assignment (b_m mod q^{nu_q(m)}) the fiber budget
 *      F(r) = sum_{m in S, b_m = r mod q^{nu_q(m)}}  q^{nu_q(m)} / m        (r in Z_q)
 * and  Phi_q(S) = max over assignments of min over r of F(r).
 *
 * Proposition D2 + the parity split (Prop. D1) give the NECESSARY CONDITION
 *      Phi_q(S) >= 2   for every prime q
 * for S to be the (halved) modulus set of a covering system with distinct moduli in E.
 * Phi_q is monotone under S -> S', so testing S = D_H(L) = {m | L : m in H} rules out every
 * subset, i.e. every covering whose H-world lcm divides L.
 *
 * This program computes Phi_q(D_H(L)) EXACTLY (branch and bound over all placements) -- the
 * placement problem is: each modulus m with nu_q(m)=j is an item of weight q^j/m that must be
 * placed at one of the q^j nodes of depth j of the q-ary tree of depth e; the value of a leaf
 * is the sum of the weights on its root-to-leaf path; maximise the minimum leaf.
 *
 * Usage:  ./D_05_phi <q> <e> <nitems>  then nitems lines "<level> <weight>" on stdin,
 *         plus a first line "<flat>" = the total weight of level-0 items.
 *         Prints  PHI = <value>.
 *
 * CONCLUSION: see driver D_05_run.py.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

static int q, e, n;
static int nleaves;
static double flat;
static int    lev[4096];
static double wt[4096];
static double cur[4096];          /* leaf values */
static double best;               /* best min found so far */
static long long nodes = 0, nodecap = 0;
static int aborted = 0;
static double target = 0;   /* decision mode: stop as soon as min >= target */
static int hit = 0;

/* suffix bound tables: S[d][i] = sum_{k>=i} wt[k] * q^{e - max(lev[k], d)}  */
static double *S[32];
static int    powq[32];

static int cmpw(const void *a, const void *b){
    double x = *(const double*)a, y = *(const double*)b;
    return (x < y) - (x > y);
}

/* upper bound on the achievable min, given items [i, n) unassigned */
static double bound(int i){
    double ub = 1e18;
    for(int d = 0; d <= e; d++){
        int blk = powq[e - d];                 /* leaves per node at depth d */
        for(int v = 0; v < powq[d]; v++){
            double s = 0;
            for(int t = 0; t < blk; t++) s += cur[v * blk + t];
            double u = (s + S[d][i]) / blk;
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
        for(int l = 0; l < nleaves; l++) if(cur[l] < mn) mn = cur[l];
        if(mn > best) best = mn;
        if(target > 0 && mn >= target){ hit = 1; aborted = 1; }
        return;
    }
    if(bound(i) <= best + 1e-12) return;
    int j = lev[i], nn = powq[j], blk = powq[e - j];
    /* symmetry: the first item may be fixed at node 0 */
    int lim = (i == 0) ? 1 : nn;
    for(int v = 0; v < lim; v++){
        for(int t = 0; t < blk; t++) cur[v * blk + t] += wt[i];
        dfs(i + 1);
        for(int t = 0; t < blk; t++) cur[v * blk + t] -= wt[i];
        if(aborted) return;
    }
}

int main(int argc, char **argv){
    if(argc < 4){ fprintf(stderr, "usage: %s q e nitems [nodecap]\n", argv[0]); return 1; }
    q = atoi(argv[1]); e = atoi(argv[2]); n = atoi(argv[3]);
    nodecap = (argc > 4) ? atoll(argv[4]) : 0;
    target  = (argc > 5) ? atof(argv[5]) : 0;
    if(e > 30){ fprintf(stderr,"e too large\n"); return 1; }
    powq[0] = 1;
    for(int i = 1; i <= e + 1 && i < 32; i++){
        if(powq[i-1] > (1<<28)/q){ fprintf(stderr,"tree too big\n"); return 1; }
        powq[i] = powq[i-1] * q;
    }
    nleaves = powq[e];
    if(scanf("%lf", &flat) != 1) return 1;
    for(int i = 0; i < n; i++)
        if(scanf("%d %lf", &lev[i], &wt[i]) != 2) return 1;
    /* sort items by decreasing weight (stable enough) */
    for(int i = 0; i < n; i++) for(int k = i+1; k < n; k++)
        if(wt[k] > wt[i]){ double tw = wt[i]; wt[i]=wt[k]; wt[k]=tw;
                           int tl = lev[i]; lev[i]=lev[k]; lev[k]=tl; }
    for(int d = 0; d <= e; d++){
        S[d] = malloc(sizeof(double) * (n + 1));
        S[d][n] = 0;
        for(int i = n - 1; i >= 0; i--){
            int mx = lev[i] > d ? lev[i] : d;
            S[d][i] = S[d][i+1] + wt[i] * powq[e - mx];
        }
    }
    for(int l = 0; l < nleaves; l++) cur[l] = flat;
    best = (target > 0) ? target - 1e-9 : -1e18;
    dfs(0);
    if(target > 0){
        if(hit)          printf("PHI_GE %.9f nodes %lld\n", target, nodes);
        else if(aborted) printf("PHI_UNKNOWN nodecap nodes %lld\n", nodes);
        else             printf("PHI_LT %.9f nodes %lld\n", target, nodes);
    } else if(aborted)   printf("PHI_UNKNOWN nodecap best_so_far %.9f\n", best);
    else                 printf("PHI %.9f nodes %lld\n", best, nodes);
    return 0;
}
