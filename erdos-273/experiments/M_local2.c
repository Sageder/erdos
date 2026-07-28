/* M_local2.c — efficient greedy + coordinate-descent search for a covering system whose moduli
 * are DISTINCT divisors of L lying in E = {n >= 4 : n+1 prime}.
 *
 * Equivalent formulation being searched (this IS the whole problem for the given L):
 *   assign to every admissible divisor n of L one residue a_n in Z/n; ask that every residue of
 *   Z/L be covered.  Coverage is monotone in adding classes and the distinct-moduli convention
 *   permits one residue per modulus, so using EVERY admissible divisor is optimal; redundant
 *   classes can be deleted afterwards.  Because every n in E is even, an assignment automatically
 *   splits by residue parity into the two disjoint halved-world (H) subsystems.
 *
 * Improvement over M_local.c: the gain of EVERY residue of a modulus is computed in a SINGLE
 * linear pass over the cover array (bucket by r mod m), instead of one pass per residue.  Same
 * asymptotic cost O(L) per move but far better constants and cache behaviour, and it evaluates
 * all residues exactly rather than sampling.
 *
 * SEARCH ONLY: success yields a certificate (re-verified independently by
 * experiments/verify_certificate.py); failure proves NOTHING.  Use M_sat.py / M_sat2.py for
 * exact UNSAT verdicts.
 *
 * Usage: ./M_local2 <L> [--sweeps N] [--seed S] [--restarts R] [--out FILE] [--quiet]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static int64_t L;
static uint16_t *cov;
static int64_t uncovered;
#define MAXD 4096
static int64_t mods[MAXD], res[MAXD];
static int nmods;
static int64_t *gainbuf;

static uint64_t rs_ = 88172645463325252ULL;
static uint64_t rnd(void){ rs_^=rs_<<13; rs_^=rs_>>7; rs_^=rs_<<17; return rs_; }

static int is_prime(int64_t n){
    if(n<2) return 0; if(n%2==0) return n==2;
    for(int64_t d=3; d*d<=n; d+=2) if(n%d==0) return 0; return 1;
}
static void mark(int64_t a,int64_t m){ for(int64_t r=a;r<L;r+=m) if(cov[r]++==0) uncovered--; }
static void unmark(int64_t a,int64_t m){ for(int64_t r=a;r<L;r+=m) if(--cov[r]==0) uncovered++; }

/* best residue for modulus m, computed in one linear pass over the uncovered set */
static int64_t best_residue(int64_t m, int64_t *bestgain){
    memset(gainbuf, 0, m*sizeof(int64_t));
    int64_t r = 0;
    while(r + m <= L){                       /* unrolled: full blocks */
        for(int64_t j = 0; j < m; j++) if(cov[r+j]==0) gainbuf[j]++;
        r += m;
    }
    for(int64_t j = 0; r + j < L; j++) if(cov[r+j]==0) gainbuf[j]++;
    int64_t b = 0, bg = gainbuf[0];
    for(int64_t j = 1; j < m; j++) if(gainbuf[j] > bg){ bg = gainbuf[j]; b = j; }
    *bestgain = bg;
    return b;
}

int main(int argc,char**argv){
    setbuf(stdout,NULL);
    if(argc<2){fprintf(stderr,"usage: %s <L> [--sweeps N] [--seed S] [--restarts R] [--out F]\n",argv[0]);return 1;}
    L=atoll(argv[1]);
    int64_t sweeps=60, restarts=1; const char*outf=NULL; int quiet=0;
    for(int i=2;i<argc;i++){
        if(!strcmp(argv[i],"--sweeps")&&i+1<argc) sweeps=atoll(argv[++i]);
        else if(!strcmp(argv[i],"--seed")&&i+1<argc) rs_=atoll(argv[++i])*2862933555777941757ULL+3037000493ULL;
        else if(!strcmp(argv[i],"--restarts")&&i+1<argc) restarts=atoll(argv[++i]);
        else if(!strcmp(argv[i],"--out")&&i+1<argc) outf=argv[++i];
        else if(!strcmp(argv[i],"--quiet")) quiet=1;
    }
    for(int64_t d=1;d*d<=L;d++){
        if(L%d) continue;
        int64_t c[2]={d,L/d};
        for(int t=0;t<2;t++){
            if(t==1&&c[0]==c[1]) continue;
            int64_t x=c[t];
            if(x>=4&&is_prime(x+1)){ if(nmods>=MAXD){fprintf(stderr,"MAXD\n");return 1;} mods[nmods++]=x; }
        }
    }
    for(int i=0;i<nmods;i++) for(int j=i+1;j<nmods;j++) if(mods[j]<mods[i]){int64_t t=mods[i];mods[i]=mods[j];mods[j]=t;}
    double budget=0; for(int i=0;i<nmods;i++) budget+=1.0/(double)mods[i];
    printf("L = %lld   #admissible divisors = %d   budget f(L) = %.6f   slack (f-1)L = %.0f\n",
           (long long)L,nmods,budget,(budget-1.0)*(double)L);
    if(budget<=1.0){ printf("RESULT: IMPOSSIBLE for this L (f(L) <= 1)\n"); return 0; }
    cov=calloc(L,sizeof(uint16_t));
    gainbuf=malloc((mods[nmods-1]+1)*sizeof(int64_t));
    if(!cov||!gainbuf){fprintf(stderr,"alloc failed\n");return 1;}

    int64_t globalbest=L;
    for(int64_t rst=0;rst<restarts;rst++){
        memset(cov,0,L*sizeof(uint16_t)); uncovered=L;
        for(int i=0;i<nmods;i++){                       /* greedy init, increasing modulus */
            int64_t bg,b=best_residue(mods[i],&bg);
            if(rst>0 && (rnd()%100)<20) b=(int64_t)(rnd()%(uint64_t)mods[i]);
            res[i]=b; mark(b,mods[i]);
        }
        if(!quiet) printf("  restart %lld: greedy -> uncovered %lld (%.4f%%)\n",
                          (long long)rst,(long long)uncovered,100.0*uncovered/L);
        int64_t prev=-1;
        for(int64_t s=0;s<sweeps && uncovered>0;s++){    /* coordinate-descent sweeps */
            int ord[MAXD]; for(int i=0;i<nmods;i++) ord[i]=i;
            for(int i=nmods-1;i>0;i--){int j=(int)(rnd()%(uint64_t)(i+1));int t=ord[i];ord[i]=ord[j];ord[j]=t;}
            for(int t=0;t<nmods && uncovered>0;t++){
                int i=ord[t]; int64_t m=mods[i];
                unmark(res[i],m);
                int64_t bg,b=best_residue(m,&bg);
                res[i]=b; mark(b,m);
            }
            if(!quiet) printf("    sweep %lld: uncovered %lld (%.4f%%)\n",
                              (long long)s,(long long)uncovered,100.0*uncovered/L);
            if(uncovered==prev) break;                  /* converged */
            prev=uncovered;
        }
        if(uncovered<globalbest) globalbest=uncovered;
        if(uncovered==0){
            printf("SUCCESS: complete covering found for L = %lld\n",(long long)L);
            FILE*fp=outf?fopen(outf,"w"):stdout;
            fprintf(fp,"# covering system, all moduli divisors of L = %lld, all of the form p-1 (p>=5 prime)\n",(long long)L);
            for(int i=0;i<nmods;i++) fprintf(fp,"%lld %lld\n",(long long)res[i],(long long)mods[i]);
            if(outf){fclose(fp);printf("wrote %s\n",outf);}
            return 0;
        }
    }
    printf("RESULT: no covering found; best uncovered = %lld (%.4f%%). This PROVES NOTHING.\n",
           (long long)globalbest,100.0*globalbest/L);
    return 0;
}
