/* mine2.c -- two-point forced-relation miner on t-EXTENDABLE boards.
 *
 * usage: ./mine2 M N
 *   enumerates ALL monotone-4-AP-free permutations of [1..M], restricts each to the
 *   values [1..N] (in position order) and mines forced two-point relations on the
 *   RESTRICTION.  With M = N this is mine.c.  With M > N the mined boards are exactly
 *   the restrictions of (M-N)-extendable avoiders -- the only boards that a
 *   monotone-4-AP-free permutation of N can produce at level N (necessary condition).
 *
 * A relation forced on (M-N)-extendable boards but NOT on all N-boards is a CANDIDATE
 * window-determined statement that is true for every infinite avoider yet false for
 * some finite one; such a statement is exactly what the two-point-supply hunt needs.
 * It is a candidate only -- forcing at one (M,N) is not a proof.
 *
 * Bucketing identical to mine.c.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int M, N;
static int perm[40], pos[40], placed[40];
static long long nboards = 0;

#define NT 4
#define NORD 2
#define NRAT 3
#define NCONS 2
#define MMAX 3
#define NSL 9

static inline int bidx(int tp,int tq,int ord,int rat,int cons,int m,int kmin,int kmax){
    int a = kmin + 2, b = kmax - m;
    return ((((((tp*NT + tq)*NORD + ord)*NRAT + rat)*NCONS + cons)*MMAX + (m-1))*3 + a)*3 + b;
}
#define NBUCK (NT*NT*NORD*NRAT*NCONS*MMAX*3*3)

static long long bcount[NBUCK];
static unsigned char seenLT[NBUCK][NSL][NSL];
static int isrec[40], isgnd[40], rpos[40], recpref[40];

static void process(void){
    nboards++;
    int i,v,t=0;
    /* restriction of the board to values [1..N], in position order */
    for(i=1;i<=M;i++){ v = perm[i]; if(v<=N) rpos[v] = ++t; }
    int mx = 0;
    /* records / grounded OF THE RESTRICTION */
    { int order[40]; for(v=1;v<=N;v++) order[rpos[v]] = v;
      for(i=1;i<=N;i++){ v=order[i]; isrec[v] = (v>mx); if(v>mx) mx=v; } }
    int mp = 0;
    for(v=1;v<=N;v++){ isgnd[v] = (rpos[v] > mp); if(rpos[v] > mp) mp = rpos[v]; }
    recpref[0]=0;
    for(v=1;v<=N;v++) recpref[v] = recpref[v-1] + isrec[v];

    int p,q;
    for(p=1;p<=N;p++) for(q=p+1;q<=N;q++){
        int D = q-p;
        int tp = 2*isgnd[p] + isrec[p];
        int tq = 2*isgnd[q] + isrec[q];
        int ord = (rpos[p] < rpos[q]) ? 1 : 0;
        int rat = (q < 2*p) ? 0 : ((q < 3*p) ? 1 : 2);
        int cons = (isrec[p] && isrec[q] && (recpref[q-1]-recpref[p]==0)) ? 1 : 0;
        int m;
        for(m=1;m<=MMAX;m++){
            if(D % m) continue;
            int s = D/m;
            int kmin = -2, kmax = m+2;
            while(p + kmin*s < 1) kmin++;
            while(p + kmax*s > N) kmax--;
            int bi = bidx(tp,tq,ord,rat,cons,m,kmin,kmax);
            bcount[bi]++;
            int k1,k2;
            for(k1=kmin;k1<=kmax;k1++){
                int v1 = p + k1*s;
                for(k2=k1+1;k2<=kmax;k2++){
                    int v2 = p + k2*s;
                    if(rpos[v1] < rpos[v2]) seenLT[bi][k1+2][k2+2] = 1;
                    else                    seenLT[bi][k2+2][k1+2] = 1;
                }
            }
        }
    }
}

static int ok(int w){
    int d;
    for(d=1; w-3*d>=1; d++)
        if(placed[w-d] && placed[w-2*d] && placed[w-3*d] &&
           pos[w-3*d] < pos[w-2*d] && pos[w-2*d] < pos[w-d]) return 0;
    for(d=1; w+3*d<=M; d++)
        if(placed[w+d] && placed[w+2*d] && placed[w+3*d] &&
           pos[w+3*d] < pos[w+2*d] && pos[w+2*d] < pos[w+d]) return 0;
    return 1;
}

static void rec(int t){
    if(t > M){ process(); return; }
    int w;
    for(w=1;w<=M;w++)
        if(!placed[w] && ok(w)){
            placed[w]=1; pos[w]=t; perm[t]=w;
            rec(t+1);
            placed[w]=0;
        }
}

int main(int argc,char**argv){
    M = atoi(argv[1]); N = atoi(argv[2]);
    memset(bcount,0,sizeof(bcount)); memset(seenLT,0,sizeof(seenLT));
    rec(1);
    fprintf(stderr,"M=%d N=%d boards=%lld\n",M,N,nboards);
    printf("#M %d N %d boards %lld\n",M,N,nboards);
    int tp,tq,ord,rat,cons,m,a,b;
    for(tp=0;tp<NT;tp++)for(tq=0;tq<NT;tq++)for(ord=0;ord<NORD;ord++)
    for(rat=0;rat<NRAT;rat++)for(cons=0;cons<NCONS;cons++)for(m=1;m<=MMAX;m++)
    for(a=0;a<3;a++)for(b=0;b<3;b++){
        int kmin=a-2, kmax=m+b;
        int bi = bidx(tp,tq,ord,rat,cons,m,kmin,kmax);
        if(!bcount[bi]) continue;
        printf("B %d %d %d %d %d %d %d %d %lld ",tp,tq,ord,rat,cons,m,kmin,kmax,bcount[bi]);
        int k1,k2;
        for(k1=kmin;k1<=kmax;k1++)for(k2=kmin;k2<=kmax;k2++){
            if(k1==k2) continue;
            if(seenLT[bi][k1+2][k2+2]) printf("%d,%d;",k1,k2);
        }
        printf("\n");
    }
    return 0;
}
