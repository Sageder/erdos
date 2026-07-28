/* B_node.c  --  Route B (recursive / hierarchical construction), core node solver.
 *
 * CLAIM TESTED
 * ------------
 * At a node of the Route-B tree we must cover one residue class  r (mod D)  of Z using only
 * moduli that are multiples of D.  Rescaling x = r + D*y turns this into the finite problem
 *
 *      cover  Z/M  \  (hole)   by residue classes b_f (mod f) with DISTINCT moduli f | M,
 *      f >= 2, where f is admissible iff  D*f + 1  is prime  (so that D*f lies in E).
 *
 * The optional HOLE is a residue class  c (mod M')  with M' | M.  Leaving exactly that hole
 * uncovered is the "chain step" of Route B: the leftover class becomes the single child node,
 * of node-modulus  D*M'.   hole M'=0 means "cover everything" (a terminal node).
 *
 * Algorithm
 *   Phase 1 randomised greedy on the explicit uncovered list: repeatedly pick an unused
 *     modulus f (random, weight 1/f^bias) and give it the residue killing the most uncovered
 *     elements; the score can be tilted by f^alpha to favour cheap (large-f) coverage.
 *   Phase 2 annealing polish on a multiplicity array cov[].
 *   Phase 3 redundancy pruning: drop used moduli (smallest f first) whose removal does not
 *     increase the uncovered count -- this MINIMISES the weight sum 1/f actually consumed.
 *   Phase 4 (--exact) complete DFS "cover the smallest uncovered residue, branch over unused
 *     moduli": if it exhausts without success, NO covering exists for this (M, pool, hole).
 *
 * All arithmetic exact 64-bit.  Output: BEST <uncovered> WEIGHT <sum 1/f> then the (f,b) list.
 *
 * CONCLUSION: see run logs and attempts/route-B-recursive/FINDINGS.md
 *
 * stdin:   M
 *          h                 (number of holes)
 *          Mprime_i c_i      (hole i: the class c_i mod Mprime_i), i=1..h
 *          k
 *          f_1 ... f_k
 * usage:   ./B_node [--restarts N] [--anneal N] [--seed S] [--target T] [--exact]
 *                   [--dfslimit N] [--quiet]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <math.h>

static int64_t M;
static int NH; static int64_t HMp[16], HCc[16];
static int K;
static int64_t *F;
static uint8_t *cov;        /* multiplicity; hole residues get a permanent +1 */
static uint8_t *base;       /* 1 on hole residues */
static int32_t *unc;
static int64_t nunc;
static int64_t n_target;    /* number of residues that must be covered */
static int32_t *cnt;
static int64_t maxf;

static int   *bestb, *curb, *used_best, *used_cur;
static int64_t best_unc;

static uint64_t rng_s = 88172645463325252ULL;
static inline uint64_t rnd(void){ rng_s ^= rng_s<<13; rng_s ^= rng_s>>7; rng_s ^= rng_s<<17; return rng_s; }
static inline double rnd01(void){ return (double)(rnd()>>11) * (1.0/9007199254740992.0); }
static inline int in_hole(int64_t x){ for(int h=0;h<NH;h++) if((x%HMp[h])==HCc[h]) return 1; return 0; }

/* ---------------- phase 1 ---------------------------------------------------------------- */
static int64_t greedy(double bias, double alpha, int *outb, int *outused)
{
    int64_t i, w=0;
    for(i=0;i<M;i++) if(!in_hole(i)) unc[w++]=(int32_t)i;
    nunc=w;
    for(int j=0;j<K;j++){ outused[j]=0; outb[j]=-1; }

    int remaining=K;
    while(remaining>0 && nunc>0){
        double tot=0;
        for(int j=0;j<K;j++) if(!outused[j]) tot += exp(-bias*log((double)F[j]));
        double pick=rnd01()*tot, acc=0; int sel=-1;
        for(int j=0;j<K;j++) if(!outused[j]){ acc += exp(-bias*log((double)F[j])); if(acc>=pick){ sel=j; break; } }
        if(sel<0) for(int j=0;j<K;j++) if(!outused[j]){ sel=j; break; }

        int64_t f=F[sel];
        memset(cnt,0,sizeof(int32_t)*f);
        for(i=0;i<nunc;i++) cnt[ unc[i]%f ]++;
        int64_t bA=0; int32_t bC=-1; int ties=0;
        for(int64_t a=0;a<f;a++){
            if(cnt[a]>bC){ bC=cnt[a]; bA=a; ties=1; }
            else if(cnt[a]==bC){ ties++; if(rnd()%(uint64_t)ties==0) bA=a; }
        }
        (void)alpha;
        outb[sel]=(int)bA; outused[sel]=1; remaining--;
        if(bC>0){ int64_t v=0; for(i=0;i<nunc;i++) if(unc[i]%f!=bA) unc[v++]=unc[i]; nunc=v; }
    }
    return nunc;
}

/* ---------------- phase 2 ---------------------------------------------------------------- */
static void build_cov(int *b,int *used)
{
    memcpy(cov,base,M);
    int64_t u=n_target;
    for(int j=0;j<K;j++) if(used[j] && b[j]>=0){
        int64_t f=F[j];
        for(int64_t x=b[j]; x<M; x+=f){ if(cov[x]++==0) u--; }
    }
    nunc=u;
}
static inline void apply_mod(int j,int nb)
{
    int64_t f=F[j], ob=curb[j], d=0;
    if(ob>=0) for(int64_t x=ob;x<M;x+=f){ if(--cov[x]==0) d++; }
    for(int64_t x=nb;x<M;x+=f){ if(cov[x]++==0) d--; }
    curb[j]=nb; nunc+=d;
}

/* ---------------- phase 3: redundancy pruning -------------------------------------------- */
static void prune(int *b,int *used)
{
    build_cov(b,used);
    int64_t u0=nunc;
    for(int j=0;j<K;j++){          /* F ascending: drop the most expensive moduli first */
        if(!used[j]||b[j]<0) continue;
        int64_t f=F[j], d=0;
        for(int64_t x=b[j];x<M;x+=f){ if(--cov[x]==0) d++; }
        if(d==0){ used[j]=0; }     /* redundant */
        else { for(int64_t x=b[j];x<M;x+=f) cov[x]++; }
    }
    build_cov(b,used);
    if(nunc!=u0){ fprintf(stderr,"prune bug %lld %lld\n",(long long)u0,(long long)nunc); }
}

/* ---------------- phase 4: exact DFS ------------------------------------------------------ */
static int64_t dfs_nodes=0, dfs_limit=0;
static int *dfs_used,*dfs_b;
static int64_t dfs_uncov; static int dfs_found=0;
static int64_t smallest_uncovered(void){ for(int64_t x=0;x<M;x++) if(!cov[x]) return x; return -1; }
static double capacity(void){ double c=0; for(int j=0;j<K;j++) if(!dfs_used[j]) c+=(double)M/(double)F[j]; return c; }
static void dfs(void)
{
    if(dfs_found) return;
    if(dfs_limit && ++dfs_nodes>dfs_limit) return;
    if(dfs_uncov==0){ dfs_found=1; return; }
    if(capacity() < (double)dfs_uncov) return;
    int64_t x=smallest_uncovered();
    for(int j=0;j<K;j++){
        if(dfs_used[j]) continue;
        int64_t f=F[j], a=x%f, d=0;
        for(int64_t y=a;y<M;y+=f){ if(cov[y]++==0) d++; }
        dfs_uncov-=d; dfs_used[j]=1; dfs_b[j]=(int)a;
        dfs();
        if(dfs_found) return;
        dfs_used[j]=0; dfs_uncov+=d;
        for(int64_t y=a;y<M;y+=f) cov[y]--;
    }
}

int main(int argc,char**argv)
{
    int restarts=200, anneal=0, exact=0, quiet=0; int64_t target=0;
    for(int i=1;i<argc;i++){
        if(!strcmp(argv[i],"--restarts")) restarts=atoi(argv[++i]);
        else if(!strcmp(argv[i],"--anneal")) anneal=atoi(argv[++i]);
        else if(!strcmp(argv[i],"--seed")) rng_s=strtoull(argv[++i],0,10)*2862933555777941757ULL+3037000493ULL;
        else if(!strcmp(argv[i],"--target")) target=atoll(argv[++i]);
        else if(!strcmp(argv[i],"--exact")) exact=1;
        else if(!strcmp(argv[i],"--dfslimit")) dfs_limit=atoll(argv[++i]);
        else if(!strcmp(argv[i],"--quiet")) quiet=1;
    }
    long long t1,t2,t3;
    if(scanf("%lld",&t1)!=1) return 1; M=t1;
    if(scanf("%d",&NH)!=1) return 1;
    for(int h=0;h<NH;h++){ if(scanf("%lld %lld",&t2,&t3)!=2) return 1; HMp[h]=t2; HCc[h]=t3%t2; }
    if(scanf("%d",&K)!=1) return 1;
    F=malloc(sizeof(int64_t)*K);
    for(int j=0;j<K;j++){ long long t; if(scanf("%lld",&t)!=1) return 1; F[j]=t; }
    maxf=0; for(int j=0;j<K;j++) if(F[j]>maxf) maxf=F[j];
    cov=malloc(M); base=malloc(M); unc=malloc(sizeof(int32_t)*M); cnt=malloc(sizeof(int32_t)*(maxf+1));
    bestb=malloc(sizeof(int)*K); curb=malloc(sizeof(int)*K);
    used_best=calloc(K,sizeof(int)); used_cur=calloc(K,sizeof(int));
    dfs_used=calloc(K,sizeof(int)); dfs_b=calloc(K,sizeof(int));
    if(!cov||!base||!unc||!cnt){ fprintf(stderr,"alloc fail\n"); return 2; }
    memset(base,0,M); n_target=M;
    for(int h=0;h<NH;h++){ for(int64_t x=HCc[h];x<M;x+=HMp[h]) base[x]=1; }
    n_target=0; for(int64_t x=0;x<M;x++) if(!base[x]) n_target++;
    best_unc=M+1;

    double biases[6]={0.0,0.3,0.6,1.0,1.5,2.0};
    double best_w=1e18;
    for(int r=0;r<restarts;r++){
        int64_t u=greedy(biases[r%6],0.0,curb,used_cur);
        if(u>target){
            if(u<best_unc && best_w>1e17){
                best_unc=u; memcpy(bestb,curb,sizeof(int)*K); memcpy(used_best,used_cur,sizeof(int)*K);
                if(!quiet) fprintf(stderr,"[greedy r=%d] uncovered=%lld (dens %.4g)\n",r,(long long)u,(double)u/M);
            }
            continue;
        }
        /* candidate solution: prune it and score by weight */
        prune(curb,used_cur);
        double w=0; for(int j=0;j<K;j++) if(used_cur[j]) w+=1.0/F[j];
        if(u<best_unc || (u==best_unc && w<best_w)){
            best_unc=u; best_w=w;
            memcpy(bestb,curb,sizeof(int)*K); memcpy(used_best,used_cur,sizeof(int)*K);
            if(!quiet) fprintf(stderr,"[greedy r=%d] uncovered=%lld weight=%.6f\n",r,(long long)u,w);
        }
    }
    if(anneal && best_unc>target){
        memcpy(curb,bestb,sizeof(int)*K); memcpy(used_cur,used_best,sizeof(int)*K);
        for(int j=0;j<K;j++) if(!used_cur[j]||curb[j]<0){ used_cur[j]=1; curb[j]=(int)(rnd()%F[j]); }
        build_cov(curb,used_cur);
        if(nunc<best_unc){ best_unc=nunc; memcpy(bestb,curb,sizeof(int)*K); memcpy(used_best,used_cur,sizeof(int)*K); }
        double T0=3.0;
        for(int it=0; it<anneal && best_unc>target; it++){
            double T=T0*(1.0-(double)it/anneal)+1e-3;
            int j=(int)(rnd()%(uint64_t)K); int64_t f=F[j];
            int ob=curb[j]; int nb=(int)(rnd()%(uint64_t)f);
            if(nb==ob) continue;
            int64_t before=nunc; apply_mod(j,nb); int64_t after=nunc;
            if(after<=before || rnd01()<exp(-(double)(after-before)/T)){
                if(after<best_unc){
                    best_unc=after; memcpy(bestb,curb,sizeof(int)*K); memcpy(used_best,used_cur,sizeof(int)*K);
                    if(!quiet) fprintf(stderr,"[anneal %d] uncovered=%lld\n",it,(long long)after);
                }
            } else apply_mod(j,ob);
        }
    }

    if(exact){
        memcpy(cov,base,M); dfs_uncov=n_target; memset(dfs_used,0,sizeof(int)*K);
        dfs_nodes=0; dfs_found=0; dfs();
        printf("EXACT %s nodes=%lld\n", dfs_found?"FOUND":((dfs_limit&&dfs_nodes>dfs_limit)?"LIMIT":"UNSAT"),
               (long long)dfs_nodes);
        if(dfs_found){
            double w=0; for(int j=0;j<K;j++) if(dfs_used[j]) w+=1.0/F[j];
            printf("BEST 0  M %lld  K %d  WEIGHT %.6f\nCERT\n",(long long)M,K,w);
            for(int j=0;j<K;j++) if(dfs_used[j]) printf("%lld %d\n",(long long)F[j],dfs_b[j]);
        }
        return 0;
    }

    if(best_w>1e17) prune(bestb,used_best);
    double w=0; int nm=0;
    for(int j=0;j<K;j++) if(used_best[j]){ w+=1.0/F[j]; nm++; }
    printf("BEST %lld  M %lld  K %d  USED %d  WEIGHT %.6f\n",(long long)best_unc,(long long)M,K,nm,w);
    printf("CERT\n");
    for(int j=0;j<K;j++) if(used_best[j]) printf("%lld %d\n",(long long)F[j],bestb[j]);
    return 0;
}
