/* mine.c -- exhaustive two-point forced-relation miner for Erdos 196.
 *
 * Enumerates ALL monotone-4-AP-free permutations of [1..N] (same DFS prune as
 * attempts/route-R5/enum_avoiders.py, whose soundness argument is: in any monotone
 * 4-AP the LATEST-positioned element is the largest value (increasing orientation)
 * or the smallest value (decreasing orientation); so the AP is detected exactly when
 * that element is appended).
 *
 * For every board and every ordered pair of values p < q it buckets the pair by
 *   (type(p), type(q), order(p,q), ratio class, m, window), where
 *     type(v)  = 2*[v grounded] + [v record]      (record = running maximum,
 *                                                  grounded = all smaller values earlier)
 *     order    = [pos(p) < pos(q)]
 *     ratio    = 0 if q < 2p, 1 if 2p <= q < 3p, 2 if q >= 3p
 *     m        = number of steps: the AP line through p,q with step s = (q-p)/m
 *     window   = (kmin, kmax) of in-range slots p + k*s, k in [-2, m+2]
 * and records, for every ordered slot pair, whether pos(p+k1*s) < pos(p+k2*s) was
 * ever seen and whether > was ever seen.  A relation seen in only one direction over
 * ALL boards is a candidate universally forced relation.
 *
 * Also tracks the "consecutive records" bit (both records, none strictly between).
 *
 * Output: text, one line per (bucket, forced relation).
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int N;
static int perm[32], pos[32], placed[32];
static long long nboards = 0;

/* ---- bucket space ---- */
#define NT 4        /* type 0..3 */
#define NORD 2
#define NRAT 3
#define NCONS 2
#define MMAX 3
#define NSL 9       /* slots for k = -2 .. 6 ; index = k+2 */

/* bucket index */
static inline int bidx(int tp,int tq,int ord,int rat,int cons,int m,int kmin,int kmax){
    /* kmin in [-2..0] -> 0..2 ; kmax in [m..m+2] -> 0..2 */
    int a = kmin + 2;      /* 0..2 */
    int b = kmax - m;      /* 0..2 */
    return ((((((tp*NT + tq)*NORD + ord)*NRAT + rat)*NCONS + cons)*MMAX + (m-1))*3 + a)*3 + b;
}
#define NBUCK (NT*NT*NORD*NRAT*NCONS*MMAX*3*3)

static long long bcount[NBUCK];
static unsigned char seenLT[NBUCK][NSL][NSL];  /* pos(slot i) < pos(slot j) seen */

static int isrec[32], isgnd[32];

static void process(void){
    nboards++;
    int i,v;
    /* records and grounded */
    int mx = 0;
    for(i=1;i<=N;i++){ v = perm[i]; isrec[v] = (v > mx); if(v>mx) mx = v; }
    /* grounded: pos(g) > pos(v) for all v < g  <=>  pos(g) > max_{v<g} pos(v) */
    int mp = 0;
    for(v=1;v<=N;v++){ isgnd[v] = (pos[v] > mp); if(pos[v] > mp) mp = pos[v]; }
    /* record-count prefix for "consecutive records" test */
    static int recpref[32];
    recpref[0]=0;
    for(v=1;v<=N;v++) recpref[v] = recpref[v-1] + isrec[v];

    int p,q;
    for(p=1;p<=N;p++) for(q=p+1;q<=N;q++){
        int D = q-p;
        int tp = 2*isgnd[p] + isrec[p];
        int tq = 2*isgnd[q] + isrec[q];
        int ord = (pos[p] < pos[q]) ? 1 : 0;
        int rat = (q < 2*p) ? 0 : ((q < 3*p) ? 1 : 2);
        int cons = (isrec[p] && isrec[q] && (recpref[q-1]-recpref[p]==0)) ? 1 : 0;
        int m;
        for(m=1;m<=MMAX;m++){
            if(D % m) continue;
            int s = D/m;
            if(s < 1) continue;
            int kmin = -2, kmax = m+2;
            while(p + kmin*s < 1) kmin++;
            while(p + kmax*s > N) kmax--;
            if(kmax < m) continue;      /* q itself must be in range: always true */
            if(kmin > 0) continue;      /* p must be in range: always true */
            int bi = bidx(tp,tq,ord,rat,cons,m,kmin,kmax);
            bcount[bi]++;
            int k1,k2;
            for(k1=kmin;k1<=kmax;k1++){
                int v1 = p + k1*s;
                for(k2=k1+1;k2<=kmax;k2++){
                    int v2 = p + k2*s;
                    int i1 = k1+2, i2 = k2+2;
                    if(pos[v1] < pos[v2]) seenLT[bi][i1][i2] = 1;
                    else                  seenLT[bi][i2][i1] = 1;
                }
            }
        }
    }
}

/* incremental 4-AP check: can value w be appended at position t? */
static int ok(int w){
    int d;
    for(d=1; w-3*d>=1; d++){
        if(placed[w-d] && placed[w-2*d] && placed[w-3*d] &&
           pos[w-3*d] < pos[w-2*d] && pos[w-2*d] < pos[w-d]) return 0;
    }
    for(d=1; w+3*d<=N; d++){
        if(placed[w+d] && placed[w+2*d] && placed[w+3*d] &&
           pos[w+3*d] < pos[w+2*d] && pos[w+2*d] < pos[w+d]) return 0;
    }
    return 1;
}

static void rec(int t){
    if(t > N){ process(); return; }
    int w;
    for(w=1;w<=N;w++){
        if(!placed[w] && ok(w)){
            placed[w]=1; pos[w]=t; perm[t]=w;
            rec(t+1);
            placed[w]=0;
        }
    }
}

int main(int argc,char**argv){
    N = atoi(argv[1]);
    memset(bcount,0,sizeof(bcount));
    memset(seenLT,0,sizeof(seenLT));
    rec(1);
    fprintf(stderr,"N=%d boards=%lld\n",N,nboards);
    printf("#N %d boards %lld\n",N,nboards);
    /* dump: for each nonempty bucket, forced relations */
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
            int i1=k1+2,i2=k2+2;
            if(seenLT[bi][i1][i2]) printf("%d,%d;",k1,k2);
        }
        printf("\n");
    }
    return 0;
}
