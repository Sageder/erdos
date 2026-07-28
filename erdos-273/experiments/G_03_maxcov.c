/* G_03_maxcov.c -- Route G.  EXACT maximum-coverage search.
 *
 * CLAIM TESTED: given L and a pool of divisors of L (each usable at most once), what is the
 * EXACT maximum number of residues of Z/L that can be covered by choosing one residue class
 * per used modulus?   Equivalently the exact minimum size of the uncovered set.
 *
 * This complements G_02_dfs (which is tuned for deficiency 0 / tiny deficiency); here the
 * deficiency is large, so we enumerate residues modulus-by-modulus with the packing bound
 *      covered_now + sum_{unassigned m} L/m   <=   best   =>   prune.
 * Translation symmetry is quotiented by forcing the residue of the FIRST modulus to 0
 * (legitimate: translating every class by t is a bijection of solutions preserving coverage).
 *
 * Exact 64-bit / bitset arithmetic; no floating point anywhere.
 *
 * USAGE: ./G_03_maxcov L m1,m2,... [--timelimit S]
 * CONCLUSION: recorded in attempts/route-G-selfridge/FINDINGS.md
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

#define MAXD 64
static long L;
static int nmod;
static long mods[MAXD];
static long sz[MAXD];       /* L/m */
static long suffix[MAXD+1]; /* sum of sz[i..] */
static unsigned char *cov;
static long covered;
static long best = -1;
static long best_res[MAXD];
static int  best_used[MAXD];
static long cur_res[MAXD];
static int  cur_used[MAXD];
static double t0, tlimit = 1e18;
static long long nodes = 0;
static int timedout = 0;

static double now(void){ struct timespec ts; clock_gettime(CLOCK_MONOTONIC,&ts);
                         return ts.tv_sec + 1e-9*ts.tv_nsec; }

static long add_class(long a, long m){ long g=0; for(long r=a%m;r<L;r+=m){ if(!cov[r]) g++; cov[r]++; } return g; }
static void del_class(long a, long m){ for(long r=a%m;r<L;r+=m) cov[r]--; }

static void save(void){
    best = covered;
    for(int i=0;i<nmod;i++){ best_res[i]=cur_res[i]; best_used[i]=cur_used[i]; }
}

static void dfs(int i, int anyused){
    if((++nodes & 0xFFFFF)==0 && now()-t0>tlimit){ timedout=1; }
    if(timedout) return;
    if(covered > best) save();
    if(i==nmod) return;
    if(covered + suffix[i] <= best) return;          /* packing bound */
    long m = mods[i];
    long lo = 0, hi = m-1;
    if(!anyused) hi = 0;                              /* translation normalisation */
    for(long a=lo;a<=hi;a++){
        long g = add_class(a,m);
        covered += g; cur_res[i]=a; cur_used[i]=1;
        dfs(i+1,1);
        covered -= g; cur_used[i]=0;
        del_class(a,m);
        if(timedout) return;
    }
    /* skip this modulus */
    cur_used[i]=0; cur_res[i]=-1;
    dfs(i+1,anyused);
}

int main(int argc,char**argv){
    if(argc<3){ fprintf(stderr,"usage: %s L m1,m2,...\n",argv[0]); return 1; }
    L=atol(argv[1]);
    char*p=strtok(argv[2],","); while(p){ mods[nmod++]=atol(p); p=strtok(NULL,","); }
    for(int i=3;i<argc;i++) if(!strcmp(argv[i],"--timelimit")) tlimit=atof(argv[++i]);
    for(int i=0;i<nmod;i++){ if(L%mods[i]){fprintf(stderr,"bad modulus %ld\n",mods[i]);return 1;} sz[i]=L/mods[i]; }
    suffix[nmod]=0; for(int i=nmod-1;i>=0;i--) suffix[i]=suffix[i+1]+sz[i];
    cov=calloc(L,1); covered=0; best=-1;
    t0=now();
    dfs(0,0);
    printf("L=%ld pool(%d)=",L,nmod);
    for(int i=0;i<nmod;i++) printf("%s%ld",i?",":"",mods[i]);
    printf("\nnodes=%lld  %s\n",nodes,timedout?"TIMED OUT (bound is a LOWER bound on maxcov)":"EXHAUSTIVE");
    printf("packing bound sum L/m = %ld ; L = %ld\n", suffix[0], L);
    printf("MAX COVERED = %ld   MIN UNCOVERED = %ld\n", best, L-best);
    printf("CLASSES:");
    for(int i=0;i<nmod;i++) if(best_used[i]) printf(" %ld(mod %ld)",best_res[i],mods[i]);
    printf("\n");
    /* recompute uncovered set of the optimum */
    memset(cov,0,L);
    for(int i=0;i<nmod;i++) if(best_used[i]) add_class(best_res[i],mods[i]);
    long c=0; for(long r=0;r<L;r++) if(!cov[r]) c++;
    printf("verify uncovered count = %ld\n", c);
    if(c<=400){ printf("UNCOVERED SET:"); for(long r=0;r<L;r++) if(!cov[r]) printf(" %ld",r); printf("\n"); }
    return 0;
}
