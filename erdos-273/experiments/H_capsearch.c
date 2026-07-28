/* H_capsearch.c  --  Route H: exhaustive search for a covering system with a RECIPROCAL-SUM CAP.
 *
 * CLAIM TESTED.  Given a finite modulus list M (all dividing L) and a rational cap kappa,
 * is there a subset A of M and residues making A a covering system of Z with
 *        sum_{m in A} 1/m  <=  kappa   ?
 * The DFS is exhaustive, so "UNSAT" is a rigorous nonexistence statement for that (M, kappa).
 *
 * WHY THIS QUESTION.  (see FINDINGS.md)  By the parity equivalence, an E-covering with all
 * moduli <= 2Y is the same as TWO DISJOINT covering sets A, B inside H ∩ [2,Y]; by Lemma L5
 * both may be assumed inside M = R(Y); both have reciprocal sum > 1 (Davenport-Mirsky-
 * Newman-Rado) and they are disjoint, so each has reciprocal sum <= budget(M) - 1 =: kappa.
 * Hence: UNSAT here  ==>  no E-covering with all moduli <= 2Y.
 *
 * ALGORITHM.  Canonical DFS "cover the smallest uncovered residue r in [0,L)"; the residue of
 * the chosen modulus is forced to r mod m, so the search is complete.
 * PRUNING (all exact integer arithmetic; cap measured in units of residues, C = floor(kappa*L)):
 *   (P0) used  = sum_{m in A} L/m   must stay <= C.
 *   (P1) uncovered <= C - used            [every future class of modulus m adds <= L/m]
 *   (P2) uncovered <= sum_{m unused} L/m
 *   (P3) optional per-prime multiplicity requirement (--minmult q:c,...) used as a look-ahead:
 *        if the number of still-available multiples of q plus those already used is < c and
 *        at least one multiple of q is already used, prune.
 *
 * Usage:
 *   H_capsearch <L> --mods m1,m2,... --cap NUM/DEN [--maxnodes N] [--progress N]
 *                   [--minmult q:c,...] [--allsol]
 *
 * CONCLUSION: printed as RESULT: SAT/UNSAT/UNKNOWN, with node count.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

typedef __int128 i128;

static int64_t L;
static uint8_t *cov;
static int64_t uncovered;

#define MAXD 512
static int64_t mods[MAXD];
static int nmods;
static int used[MAXD];
static int64_t chosen_a[MAXD];
static int chosen_m[MAXD];
static int depth;
static int64_t cap_of[MAXD];
static int64_t free_capacity;
static int64_t used_capacity;
static int64_t C;                 /* floor(kappa * L) */

static int64_t nodes = 0, maxnodes = 0, progress_every = 0;
static int64_t nsol = 0;
static int allsol = 0;

/* per-prime minimum multiplicity requirements */
#define MAXP 32
static int64_t mmq[MAXP]; static int mmc[MAXP]; static int nmm = 0;

static int cmp64(const void*a,const void*b){
    int64_t x=*(const int64_t*)a,y=*(const int64_t*)b; return (x>y)-(x<y);
}

static void mark(int64_t a,int64_t m){ for(int64_t r=a;r<L;r+=m){ if(cov[r]++==0) uncovered--; } }
static void unmark(int64_t a,int64_t m){ for(int64_t r=a;r<L;r+=m){ if(--cov[r]==0) uncovered++; } }

static void print_solution(void){
    printf("SOLUTION k=%d  sum=%lld/%lld :",depth,(long long)used_capacity,(long long)L);
    for(int i=0;i<depth;i++) printf("  %lld mod %lld",(long long)chosen_a[i],(long long)mods[chosen_m[i]]);
    printf("\n"); fflush(stdout);
}

/* look-ahead on the per-prime multiplicity requirement */
static int minmult_ok(void){
    for(int j=0;j<nmm;j++){
        int64_t q=mmq[j]; int need=mmc[j];
        int have=0, avail=0;
        for(int i=0;i<nmods;i++) if(mods[i]%q==0){ if(used[i]) have++; else avail++; }
        if(have>0 && have+avail<need) return 0;
    }
    return 1;
}
static int minmult_final(void){
    for(int j=0;j<nmm;j++){
        int64_t q=mmq[j]; int need=mmc[j]; int have=0;
        for(int i=0;i<nmods;i++) if(mods[i]%q==0 && used[i]) have++;
        if(have>0 && have<need) return 0;
    }
    return 1;
}

static int dfs(int64_t start){
    nodes++;
    if(progress_every && nodes%progress_every==0)
        fprintf(stderr,"[prog] nodes=%lld depth=%d unc=%lld used=%lld/%lld\n",
                (long long)nodes,depth,(long long)uncovered,(long long)used_capacity,(long long)C);
    if(maxnodes && nodes>maxnodes) return -1;
    if(uncovered==0){
        if(minmult_final()){ nsol++; print_solution(); if(!allsol) return 1; }
        return 0;
    }
    if(uncovered > C - used_capacity) return 0;   /* P1 (implies P0) */
    if(uncovered > free_capacity) return 0;       /* P2 */
    if(!minmult_ok()) return 0;                   /* P3 */

    int64_t r=start; while(r<L && cov[r]) r++;
    if(r>=L) return 0;

    for(int i=0;i<nmods;i++){
        if(used[i]) continue;
        if(used_capacity + cap_of[i] > C) continue;      /* P0 */
        int64_t m=mods[i], a=r%m;
        used[i]=1; free_capacity-=cap_of[i]; used_capacity+=cap_of[i];
        chosen_a[depth]=a; chosen_m[depth]=i; depth++;
        mark(a,m);
        int res=dfs(r);
        unmark(a,m);
        depth--; used[i]=0; free_capacity+=cap_of[i]; used_capacity-=cap_of[i];
        if(res) return res;
    }
    return 0;
}

int main(int argc,char**argv){
    if(argc<2){ fprintf(stderr,"usage: %s <L> --mods list --cap NUM/DEN [...]\n",argv[0]); return 1; }
    L=atoll(argv[1]);
    int64_t capnum=0,capden=1;
    for(int i=2;i<argc;i++){
        if(!strcmp(argv[i],"--mods")&&i+1<argc){
            char*s=strdup(argv[i+1]),*t=strtok(s,","); while(t){ mods[nmods++]=atoll(t); t=strtok(NULL,","); } i++; }
        else if(!strcmp(argv[i],"--cap")&&i+1<argc){ sscanf(argv[i+1],"%lld/%lld",(long long*)&capnum,(long long*)&capden); i++; }
        else if(!strcmp(argv[i],"--maxnodes")&&i+1<argc){ maxnodes=atoll(argv[i+1]); i++; }
        else if(!strcmp(argv[i],"--progress")&&i+1<argc){ progress_every=atoll(argv[i+1]); i++; }
        else if(!strcmp(argv[i],"--allsol")){ allsol=1; }
        else if(!strcmp(argv[i],"--minmult")&&i+1<argc){
            char*s=strdup(argv[i+1]),*t=strtok(s,",");
            while(t){ int64_t q; int c; sscanf(t,"%lld:%d",(long long*)&q,&c); mmq[nmm]=q; mmc[nmm]=c; nmm++; t=strtok(NULL,","); }
            i++; }
        else { fprintf(stderr,"unknown arg %s\n",argv[i]); return 1; }
    }
    if(!nmods||!capnum){ fprintf(stderr,"need --mods and --cap\n"); return 1; }
    qsort(mods,nmods,sizeof(int64_t),cmp64);
    for(int i=0;i<nmods;i++) if(L%mods[i]){ fprintf(stderr,"modulus %lld ∤ L\n",(long long)mods[i]); return 1; }

    /* C = floor(kappa*L) with kappa = capnum/capden */
    C = (int64_t)(( (i128)capnum * (i128)L ) / (i128)capden);

    cov=calloc(L,1); if(!cov){ fprintf(stderr,"alloc fail\n"); return 1; }
    uncovered=L; free_capacity=0; used_capacity=0;
    for(int i=0;i<nmods;i++){ cap_of[i]=L/mods[i]; free_capacity+=cap_of[i]; }

    double bud=0; for(int i=0;i<nmods;i++) bud+=1.0/(double)mods[i];
    printf("L=%lld  #mods=%d  budget=%.6f  cap=%lld/%lld=%.6f  C=%lld (C/L=%.6f)\n",
           (long long)L,nmods,bud,(long long)capnum,(long long)capden,
           (double)capnum/(double)capden,(long long)C,(double)C/(double)L);
    printf("mods:"); for(int i=0;i<nmods;i++) printf(" %lld",(long long)mods[i]); printf("\n");
    for(int j=0;j<nmm;j++) printf("minmult: q=%lld needs >= %d multiples (if any used)\n",(long long)mmq[j],mmc[j]);
    fflush(stdout);

    if(free_capacity <= C){
        /* even using EVERYTHING the budget stays under cap; no info, but note it */
        printf("note: total budget <= cap, cap is not binding\n");
    }

    int res=dfs(0);
    if(res==1) printf("RESULT: SAT (nodes=%lld)\n",(long long)nodes);
    else if(res==-1) printf("RESULT: UNKNOWN (node limit %lld, nodes=%lld)\n",(long long)maxnodes,(long long)nodes);
    else if(nsol>0) printf("RESULT: SAT with %lld solutions, exhausted (nodes=%lld)\n",(long long)nsol,(long long)nodes);
    else printf("RESULT: UNSAT (exhaustive; nodes=%lld)\n",(long long)nodes);
    return 0;
}
