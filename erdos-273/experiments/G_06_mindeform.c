/* G_06_mindeform.c -- Route G, "minimal deformation" of a classical covering template.
 *
 * CLAIM TESTED: fix an lcm L.  Among ALL covering systems of Z with distinct moduli > 1 all
 * dividing L, what is the MINIMUM number of moduli that are INADMISSIBLE (i.e. not of the
 * form p-1 with p prime; in the halved world: not of the form (p-1)/2)?
 * That number is the exact "deformation distance" from the classical divisor-lattice
 * templates mod L to the admissible world.  Zero would solve Erdos 273 at that L.
 *
 * ALGORITHM: complete DFS on "cover the smallest uncovered residue" (the class is then
 * FORCED once the modulus is chosen), branch-and-bound on the number of inadmissible moduli
 * used, plus the density prune  #uncovered > sum_{unused m} L/m.
 * Every arithmetic operation is exact integer arithmetic.
 *
 * USAGE: ./G_06_mindeform L  m1:c1,m2:c2,...   [--cap C] [--nodes N]
 *        cost c is 0 (admissible) or 1 (inadmissible); --cap C initialises the incumbent
 *        (search only for solutions with cost < C).
 *
 * CONCLUSION: recorded in attempts/route-G-selfridge/FINDINGS.md
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

#define MAXD 256
static long L;
static int nmod;
static long mods[MAXD];
static int  cost[MAXD];
static int  used[MAXD];
static long cr[MAXD], cm[MAXD];
static int  cc[MAXD];
static int depth;
static unsigned char *cov;
static long n_uncov;
static long long nodes = 0, node_budget = 4000000000LL;
static int incomplete = 0;
static int best = 1<<30, best_k;
static long best_r[MAXD], best_m[MAXD];
static long budget_all;
static double t0, tlimit = 1e18;
static double now(void){ struct timespec ts; clock_gettime(CLOCK_MONOTONIC,&ts);
                         return ts.tv_sec + 1e-9*ts.tv_nsec; }

static void add_class(long a,long m){ for(long r=a%m;r<L;r+=m){ if(!cov[r]) n_uncov--; cov[r]++; } }
static void del_class(long a,long m){ for(long r=a%m;r<L;r+=m){ cov[r]--; if(!cov[r]) n_uncov++; } }

static void dfs(long start,int curcost,long budget){
    if(++nodes>node_budget){ incomplete=1; return; }
    if((nodes & 0xFFFFF)==0 && now()-t0>tlimit){ incomplete=1; }
    if(incomplete) return;
    if(n_uncov==0){
        if(curcost<best){ best=curcost; best_k=depth;
            for(int i=0;i<depth;i++){best_r[i]=cr[i];best_m[i]=cm[i];}
            fprintf(stderr,"  [improved: cost=%d k=%d]\n",best,best_k); }
        return;
    }
    if(curcost>=best) return;
    if(n_uncov>budget) return;
    long r=start; while(r<L && cov[r]) r++;
    if(r>=L) return;
    for(int i=0;i<nmod;i++){
        if(used[i]) continue;
        if(curcost+cost[i]>=best && cost[i]>0) continue;
        long m=mods[i];
        used[i]=1; cr[depth]=r%m; cm[depth]=m; cc[depth]=cost[i]; depth++;
        add_class(r%m,m);
        dfs(r+1,curcost+cost[i],budget-L/m);
        depth--; del_class(r%m,m); used[i]=0;
        if(incomplete) return;
        if(best==0) return;
    }
}

int main(int argc,char**argv){
    if(argc<3){fprintf(stderr,"usage: %s L m:c,m:c,...\n",argv[0]);return 1;}
    L=atol(argv[1]);
    char*p=strtok(argv[2],",");
    while(p){ char*q=strchr(p,':'); mods[nmod]=atol(p); cost[nmod]= q?atoi(q+1):0; nmod++; p=strtok(NULL,","); }
    for(int i=3;i<argc;i++){
        if(!strcmp(argv[i],"--cap")) best=atoi(argv[++i]);
        else if(!strcmp(argv[i],"--nodes")) node_budget=atoll(argv[++i]);
        else if(!strcmp(argv[i],"--timelimit")) tlimit=atof(argv[++i]);
    }
    for(int i=0;i<nmod;i++) if(L%mods[i]){fprintf(stderr,"bad modulus %ld\n",mods[i]);return 1;}
    budget_all=0; for(int i=0;i<nmod;i++) budget_all+=L/mods[i];
    cov=calloc(L,1); n_uncov=L; t0=now();
    dfs(0,0,budget_all);
    printf("L=%ld  #moduli=%d  budget sum L/m=%ld (=%.5f L)\n",L,nmod,budget_all,(double)budget_all/L);
    printf("nodes=%lld %s\n",nodes,incomplete?"INCOMPLETE":"EXHAUSTIVE");
    if(best<(1<<30)){
        printf("MIN #inadmissible moduli = %d   (k=%d classes)\n",best,best_k);
        printf("SYSTEM:");
        for(int i=0;i<best_k;i++) printf(" %ld(mod %ld)",best_r[i],best_m[i]);
        printf("\n");
    } else printf("no covering found below cap\n");
    return 0;
}
