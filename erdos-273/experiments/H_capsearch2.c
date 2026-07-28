/* H_capsearch2.c -- Route H: exhaustive "is there a covering system with reciprocal sum <= kappa"
 * search, with a DYNAMICALLY GROWING modulus (lcm of the classes chosen so far).
 *
 * CLAIM TESTED.  Given a finite modulus list M and a rational cap kappa = capnum/D (D = lcm(M)),
 * does there exist A ⊆ M with residues making it a covering system of Z with sum_{m in A} 1/m
 * <= kappa?   The DFS is exhaustive; "UNSAT" is a rigorous nonexistence statement for (M,kappa).
 *
 * WHY (see FINDINGS.md).  E-covering with all moduli <= 2Y  <=>  two DISJOINT covering sets
 * A,B ⊆ H ∩ [2,Y];  Lemma L5 puts both inside M = R(Y);  Davenport-Mirsky-Newman-Rado gives
 * budget(A),budget(B) > 1; disjointness gives budget(A) <= budget(M) - 1 =: kappa.
 * So UNSAT here => THEOREM: no E-covering with all moduli <= 2Y.
 *
 * REPRESENTATION.  cov[] holds coverage multiplicities modulo curL = lcm(chosen moduli).  When a
 * new modulus m is chosen, curL grows to lcm(curL,m); the array is TILED (periodic extension),
 * which is exact because the covered set is periodic mod the old curL.  Undo = unmark + reset curL.
 *
 * PRUNING (exact integer arithmetic, D = lcm(M) as common denominator for reciprocals):
 *   (P0) usedNum + D/m <= capnum                      [budget cap]
 *   (P1) uncovered*D <= (capnum - usedNum)*curL       [remaining excess must pay for the hole]
 *   (P2) uncovered*D <= freeNum*curL                  [unused moduli must be able to fill it]
 *   (P3) --minmult q:c  : if any multiple of q is used, at least c must end up used.
 *
 * Usage: H_capsearch2 --mods m1,... --cap NUM   (cap = NUM/D, D=lcm(mods), printed)
 *        [--capfrac A/B] [--maxnodes N] [--progress N] [--minmult q:c,...] [--maxL X] [--allsol]
 *
 * CONCLUSION: RESULT: SAT / UNSAT / UNKNOWN printed with node count.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

typedef __int128 i128;

#define MAXD 512
static int64_t mods[MAXD]; static int nmods;
static int used[MAXD];
static int64_t recip[MAXD];      /* D/m */
static int64_t chosen_a[MAXD], chosen_mod[MAXD]; static int depth;
static int64_t D;                /* lcm of all mods */
static int64_t capnum;           /* cap = capnum / D */
static int64_t usedNum, freeNum;
static uint8_t *cov; static int64_t curL, uncovered, maxL_alloc;
static int64_t nodes=0, maxnodes=0, progress_every=0, nsol=0;
static int allsol=0;
#define MAXP 32
static int64_t mmq[MAXP]; static int mmc[MAXP]; static int nmm=0;

static int64_t gcd64(int64_t a,int64_t b){ while(b){ int64_t t=a%b; a=b; b=t; } return a; }
static int64_t lcm64(int64_t a,int64_t b){ return a/gcd64(a,b)*b; }
static int cmp64(const void*a,const void*b){ int64_t x=*(const int64_t*)a,y=*(const int64_t*)b; return (x>y)-(x<y); }

static void print_solution(void){
    printf("SOLUTION k=%d  sum=%lld/%lld = %.9f :",depth,(long long)usedNum,(long long)D,(double)usedNum/(double)D);
    for(int i=0;i<depth;i++) printf("  %lld mod %lld",(long long)chosen_a[i],(long long)chosen_mod[i]);
    printf("\n"); fflush(stdout);
}

static int minmult_ok(void){
    for(int j=0;j<nmm;j++){
        int64_t q=mmq[j]; int need=mmc[j]; int have=0,avail=0;
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
        fprintf(stderr,"[prog] nodes=%lld d=%d curL=%lld unc=%lld used=%lld/%lld cap=%lld\n",
            (long long)nodes,depth,(long long)curL,(long long)uncovered,
            (long long)usedNum,(long long)D,(long long)capnum);
    if(maxnodes && nodes>maxnodes) return -1;
    if(uncovered==0){
        if(minmult_final()){ nsol++; print_solution(); if(!allsol) return 1; }
        return 0;
    }
    if((i128)uncovered*(i128)D > (i128)(capnum-usedNum)*(i128)curL) return 0;   /* P1 */
    if((i128)uncovered*(i128)D > (i128)freeNum*(i128)curL) return 0;            /* P2 */
    if(!minmult_ok()) return 0;                                                 /* P3 */

    int64_t r=start; while(r<curL && cov[r]) r++;
    if(r>=curL) return 0;

    for(int i=0;i<nmods;i++){
        if(used[i]) continue;
        if(usedNum + recip[i] > capnum) continue;                               /* P0 */
        int64_t m=mods[i];
        int64_t newL=lcm64(curL,m);
        if(newL>maxL_alloc) continue;   /* should not happen: newL | D <= maxL_alloc */
        int64_t oldL=curL, oldUnc=uncovered;
        if(newL!=curL){
            int64_t f=newL/curL;
            for(int64_t t=1;t<f;t++) memcpy(cov+t*curL,cov,curL);
            uncovered*=f; curL=newL;
        }
        int64_t a=r%m;
        for(int64_t t=a;t<curL;t+=m){ if(cov[t]++==0) uncovered--; }
        used[i]=1; freeNum-=recip[i]; usedNum+=recip[i];
        chosen_a[depth]=a; chosen_mod[depth]=m; depth++;
        int res=dfs(r);
        depth--; used[i]=0; freeNum+=recip[i]; usedNum-=recip[i];
        for(int64_t t=a;t<curL;t+=m){ --cov[t]; }
        curL=oldL; uncovered=oldUnc;
        if(res) return res;
    }
    return 0;
}

int main(int argc,char**argv){
    int64_t capA=0,capB=1; int have_capfrac=0;
    for(int i=1;i<argc;i++){
        if(!strcmp(argv[i],"--mods")&&i+1<argc){
            char*s=strdup(argv[i+1]),*t=strtok(s,","); while(t){ mods[nmods++]=atoll(t); t=strtok(NULL,","); } i++; }
        else if(!strcmp(argv[i],"--cap")&&i+1<argc){ capnum=atoll(argv[i+1]); i++; }
        else if(!strcmp(argv[i],"--capfrac")&&i+1<argc){ sscanf(argv[i+1],"%lld/%lld",(long long*)&capA,(long long*)&capB); have_capfrac=1; i++; }
        else if(!strcmp(argv[i],"--maxnodes")&&i+1<argc){ maxnodes=atoll(argv[i+1]); i++; }
        else if(!strcmp(argv[i],"--progress")&&i+1<argc){ progress_every=atoll(argv[i+1]); i++; }
        else if(!strcmp(argv[i],"--allsol")){ allsol=1; }
        else if(!strcmp(argv[i],"--minmult")&&i+1<argc){
            char*s=strdup(argv[i+1]),*t=strtok(s,",");
            while(t){ long long q; int c; sscanf(t,"%lld:%d",&q,&c); mmq[nmm]=q; mmc[nmm]=c; nmm++; t=strtok(NULL,","); } i++; }
        else { fprintf(stderr,"unknown arg %s\n",argv[i]); return 1; }
    }
    if(!nmods){ fprintf(stderr,"need --mods\n"); return 1; }
    qsort(mods,nmods,sizeof(int64_t),cmp64);
    D=1; for(int i=0;i<nmods;i++) D=lcm64(D,mods[i]);
    for(int i=0;i<nmods;i++) recip[i]=D/mods[i];
    if(have_capfrac) capnum=(int64_t)(((i128)capA*(i128)D)/(i128)capB);
    if(!capnum){ fprintf(stderr,"need --cap or --capfrac\n"); return 1; }

    maxL_alloc=D;
    cov=calloc(maxL_alloc,1);
    if(!cov){ fprintf(stderr,"alloc fail for D=%lld\n",(long long)D); return 1; }
    curL=1; cov[0]=0; uncovered=1;
    usedNum=0; freeNum=0; for(int i=0;i<nmods;i++) freeNum+=recip[i];

    double bud=0; for(int i=0;i<nmods;i++) bud+=1.0/(double)mods[i];
    printf("#mods=%d  D=lcm=%lld  budget=%.9f  cap=%lld/%lld=%.9f\n",
           nmods,(long long)D,bud,(long long)capnum,(long long)D,(double)capnum/(double)D);
    printf("mods:"); for(int i=0;i<nmods;i++) printf(" %lld",(long long)mods[i]); printf("\n");
    for(int j=0;j<nmm;j++) printf("minmult q=%lld -> %d\n",(long long)mmq[j],mmc[j]);
    fflush(stdout);

    int res=dfs(0);
    if(res==1) printf("RESULT: SAT (nodes=%lld)\n",(long long)nodes);
    else if(res==-1) printf("RESULT: UNKNOWN (node limit; nodes=%lld)\n",(long long)nodes);
    else if(nsol>0) printf("RESULT: SAT %lld solutions exhausted (nodes=%lld)\n",(long long)nsol,(long long)nodes);
    else printf("RESULT: UNSAT (exhaustive; nodes=%lld)\n",(long long)nodes);
    return 0;
}
