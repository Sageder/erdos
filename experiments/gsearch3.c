/* gsearch.c -- exhaustive search for a LEGAL block system with a PRESCRIBED sum.
 *
 * Find W subset [T,N] of integers, with no isolated point (so W is a disjoint
 * union of blocks of length >= 2), such that  sum_{n in W} 1/n = u/v  exactly.
 *
 * Exact integer arithmetic throughout: L = lcm(universe), weights w[n]=L/n,
 * target R0 = L*u/v (requires v | L, else no solution exists at all).
 *
 * Static prune (adapted two-attainer rule): if e = max_{n in W} nu_p(n) >= 1 is
 * attained by a UNIQUE element then nu_p(sum) = -e, so we must have
 * nu_p(u/v) = -e, i.e. e = nu_p(v).  Hence an element whose nu_p is the unique
 * maximum of the surviving universe can be deleted whenever that maximum differs
 * from nu_p(v).  Iterated to a fixed point.
 * Dynamic prune: Q[pos] | R, with Q[pos] = prod_p p^{nu_p(L)-maxe(p,pos)}.
 * Endgame table over the top TT positions, as in csearch2.c.
 *
 * usage: ./gsearch T N u v [TT] [maxsol]
 */
#include <stdio.h>
#include <stdlib.h>

typedef unsigned __int128 u128;

static int T0, N, TT, SPLIT;
static long long U_NUM, V_DEN;
static int allowed[600];
static u128 L, w[600], tail[602], Q[602];
static long long nodes = 0, nsol = 0, maxsol = 20;
static int chosen[600], nch = 0;
static int primes[600], np = 0;
static u128 *tab[3]; static long long tabn[3], tabcap[3];

static void print_u128(u128 x){char b[64];int i=63;b[i--]=0;if(!x){printf("0");return;}
    while(x){b[i--]='0'+(int)(x%10);x/=10;}printf("%s",b+i+1);}
static int nu(long long n,int p){int e=0;while(n%p==0){n/=p;e++;}return e;}

static void build_primes(void){for(int i=2;i<=N;i++){int q=1;for(int j=2;j*j<=i;j++)if(i%j==0){q=0;break;}if(q)primes[np++]=i;}}

static void build_universe(void){
    FILE *f=fopen(getenv("UNIV")?getenv("UNIV"):"nofile","r");
    if(f){for(int n=T0;n<=N;n++)allowed[n]=0; int x; while(fscanf(f,"%d",&x)==1) if(x>=T0&&x<=N) allowed[x]=1; fclose(f); return;}
    for(int n=T0;n<=N;n++) allowed[n]=1;
    int changed=1;
    while(changed){changed=0;
        for(int pi=0;pi<np;pi++){int p=primes[pi]; int fv=nu(V_DEN,p);
            for(;;){int emax=0,cnt=0;
                for(int n=T0;n<=N;n++) if(allowed[n]){int e=nu(n,p);
                    if(e>emax){emax=e;cnt=1;} else if(e==emax&&e>0) cnt++;}
                if(emax>=1&&cnt<2&&emax!=fv){
                    for(int n=T0;n<=N;n++) if(allowed[n]&&nu(n,p)==emax){allowed[n]=0;changed=1;}
                } else break;
            }}}
}
static void push(int c,u128 v){if(tabn[c]==tabcap[c]){tabcap[c]=tabcap[c]?tabcap[c]*2:1024;
    tab[c]=realloc(tab[c],tabcap[c]*sizeof(u128));if(!tab[c]){fprintf(stderr,"OOM\n");exit(1);}}
    tab[c][tabn[c]++]=v;}
static void gen(int c0,int pos,int c,u128 acc){
    if(pos>N){if(c!=1)push(c0,acc);return;}
    if(allowed[pos]) gen(c0,pos+1,c==0?1:2,acc+w[pos]); else if(c==1) return;
    if(c!=1) gen(c0,pos+1,0,acc);
}
static int cmp128(const void*a,const void*b){u128 x=*(const u128*)a,y=*(const u128*)b;return x<y?-1:(x>y?1:0);}
static int lookup(int c,u128 v){long long lo=0,hi=tabn[c]-1;while(lo<=hi){long long m=(lo+hi)/2;
    if(tab[c][m]==v)return 1; if(tab[c][m]<v)lo=m+1; else hi=m-1;} return 0;}
static void report(void){nsol++;printf("SOL");for(int i=0;i<nch;i++)printf(" %d",chosen[i]);
    printf("\n");fflush(stdout); if(nsol>=maxsol){printf("(cap)\n");exit(0);} }
static int emit(int pos,int c,u128 R){
    if(pos>N){if(c!=1&&R==0){report();return 1;}return 0;}
    if(allowed[pos]&&w[pos]<=R){chosen[nch++]=pos; if(emit(pos+1,c==0?1:2,R-w[pos])){nch--;return 1;} nch--;}
    else if(c==1) return 0;
    if(c!=1) return emit(pos+1,0,R);
    return 0;
}
static void dfs(int pos,u128 R,int runlen){
    nodes++;
    if(R==0){if(runlen!=1)report();return;}
    if(pos>N)return;
    if(R>tail[pos])return;
    if(R%Q[pos])return;
    if(pos==SPLIT){int c=runlen==0?0:(runlen==1?1:2); if(lookup(c,R)) emit(pos,c,R); return;}
    if(allowed[pos]&&w[pos]<=R){chosen[nch++]=pos;dfs(pos+1,R-w[pos],runlen+1);nch--;}
    else if(runlen==1)return;
    if(runlen!=1)dfs(pos+1,R,0);
}
int main(int argc,char**argv){
    T0=atoi(argv[1]); N=atoi(argv[2]); U_NUM=atoll(argv[3]); V_DEN=atoll(argv[4]);
    TT=argc>5?atoi(argv[5]):40; if(argc>6) maxsol=atoll(argv[6]);
    build_primes(); build_universe();
    L=1;
    for(int pi=0;pi<np;pi++){int p=primes[pi],emax=0;
        for(int n=T0;n<=N;n++) if(allowed[n]){int e=nu(n,p);if(e>emax)emax=e;}
        int fv=nu(V_DEN,p); if(fv>emax) emax=fv;          /* ensure v | L */
        for(int i=0;i<emax;i++) L*=(u128)p;}
    /* v must divide L */
    { long long vv=V_DEN; for(int pi=0;pi<np;pi++){int p=primes[pi];while(vv%p==0)vv/=p;}
      if(vv!=1){printf("target denominator has a prime factor > N: no solution\n");return 0;} }
    if(L%(u128)V_DEN){printf("v does not divide L: no solution\n");return 0;}
    printf("T=%d N=%d target=%lld/%lld  L=",T0,N,U_NUM,V_DEN); print_u128(L); printf("\n");
    for(int n=T0;n<=N;n++) w[n]=allowed[n]?L/(u128)n:0;
    tail[N+1]=0; for(int n=N;n>=T0;n--) tail[n]=tail[n+1]+w[n];
    for(int n=T0-1;n>=2;n--) tail[n]=tail[T0];
    for(int pos=T0;pos<=N+1;pos++){u128 q=1;
        for(int pi=0;pi<np;pi++){int p=primes[pi];int eL=0;{u128 t=L;while(t%(u128)p==0){t/=(u128)p;eL++;}}
            int maxe=0; for(int n=pos;n<=N;n++) if(allowed[n]){int e=nu(n,p);if(e>maxe)maxe=e;}
            int f=eL-maxe; for(int i=0;i<f;i++) q*=(u128)p;}
        Q[pos]=q;}
    SPLIT=N-TT+1; if(SPLIT<T0+1) SPLIT=T0+1;
    for(int c=0;c<3;c++){tabn[c]=tabcap[c]=0;tab[c]=NULL;gen(c,SPLIT,c,0);
        qsort(tab[c],tabn[c],sizeof(u128),cmp128);
        long long m=0;for(long long i=0;i<tabn[c];i++) if(i==0||tab[c][i]!=tab[c][i-1]) tab[c][m++]=tab[c][i];
        tabn[c]=m;}
    printf("  endgame sizes: %lld %lld %lld\n",tabn[0],tabn[1],tabn[2]); fflush(stdout);
    u128 R0=(L/(u128)V_DEN)*(u128)U_NUM;
    dfs(T0,R0,0);
    printf("done T=%d N=%d target=%lld/%lld nodes=%lld solutions=%lld\n",T0,N,U_NUM,V_DEN,nodes,nsol);
    return 0;
}
