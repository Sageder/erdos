/* checkrules.c -- exhaustive verification of the named two-point rules W1..W7
 * on ALL monotone-4-AP-free permutations of [1..N], with exact side conditions.
 * usage: ./checkrules N
 * prints, per rule, (firings, violations).
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int N;
static int perm[40], pos[40], placed[40];
static long long nboards = 0;
#define NR 12
static const char *RN[NR] = {
 "W1  rec-gnd trisection : w in L, g in G, w<g, 3|(g-w), s=(g-w)/3  =>  pos(w+2s)<pos(w+s)",
 "W2  rec-gnd bisection  : w in L, g in G, w<g, 2|(g-w), s=(g-w)/2  =>  (w,w+s,g) increasing",
 "W2a rec-gnd bis. + L1  : ... and g+s<=N                           =>  pos(g+s)<pos(g)",
 "W2b rec-gnd bis. + L2  : ... and w-s>=1                           =>  pos(w)<pos(w-s)",
 "W3  gnd-gnd bisection  : g<g' in G, 2|(g'-g), s=(g'-g)/2, g-s>=1  =>  pos(g+s)<pos(g)",
 "W4  rec-rec bisection  : w<w' in L, 2|(w'-w), s=(w'-w)/2, w'+s<=N =>  pos(w')<pos(w+s)",
 "W5  gnd-gnd m=1  (L1)  : g<g' in G, g'<2g, 2g'-g<=N               =>  pos(2g'-g)<pos(g')",
 "W6  rec-rec m=1  (L1)  : w<w' in L, 3w'-2w<=N                     =>  pos(3w'-2w)<pos(2w'-w)",
 "W6b rec-rec m=1  (L2)  : w<w' in L, 2w-w'>=1, 2w'-w<=N            =>  pos(w)<pos(2w-w')",
 "W7  rec-precedes-gnd   : g in G, w in L, g<w<2g, 2w-g<=N          =>  pos(w)<pos(g)",
 "C1  count (from W7)    : g in G                                   =>  pos(g) >= g + #{w in L: g<w<2g, 2w-g<=N}",
 "C4  count (from W7)    : w in L                                   =>  pos(w) <= w - #{g in G: w/2<g<w, 2w-g<=N}"};
static long long fire[NR], viol[NR];
static int isrec[40], isgnd[40];

static void hit(int r,int ok){ fire[r]++; if(!ok) viol[r]++; }

static void process(void){
    nboards++;
    int i,v,mx=0,mp=0;
    for(i=1;i<=N;i++){ v=perm[i]; isrec[v]=(v>mx); if(v>mx) mx=v; }
    for(v=1;v<=N;v++){ isgnd[v]=(pos[v]>mp); if(pos[v]>mp) mp=pos[v]; }

    int w,g,s;
    /* rec x gnd */
    for(w=1;w<=N;w++){ if(!isrec[w]) continue;
      for(g=w+1;g<=N;g++){ if(!isgnd[g]) continue;
        int D=g-w;
        if(D%3==0){ s=D/3; hit(0, pos[w+2*s]<pos[w+s]); }
        if(D%2==0){ s=D/2;
            hit(1, pos[w]<pos[w+s] && pos[w+s]<pos[g]);
            if(g+s<=N) hit(2, pos[g+s]<pos[g]);
            if(w-s>=1) hit(3, pos[w]<pos[w-s]);
        }
      }
    }
    /* gnd x gnd */
    for(g=1;g<=N;g++){ if(!isgnd[g]) continue;
      int g2;
      for(g2=g+1;g2<=N;g2++){ if(!isgnd[g2]) continue;
        int D=g2-g;
        if(D%2==0){ s=D/2; if(g-s>=1) hit(4, pos[g+s]<pos[g]); }
        if(g2<2*g && 2*g2-g<=N) hit(6, pos[2*g2-g]<pos[g2]);
      }
    }
    /* rec x rec */
    for(w=1;w<=N;w++){ if(!isrec[w]) continue;
      int w2;
      for(w2=w+1;w2<=N;w2++){ if(!isrec[w2]) continue;
        int D=w2-w;
        if(D%2==0){ s=D/2; if(w2+s<=N) hit(5, pos[w2]<pos[w+s]); }
        if(3*w2-2*w<=N) hit(7, pos[3*w2-2*w]<pos[2*w2-w]);
        if(2*w-w2>=1 && 2*w2-w<=N) hit(8, pos[w]<pos[2*w-w2]);
      }
    }
    /* counting corollaries */
    for(g=1;g<=N;g++){ if(!isgnd[g]) continue; int c=0,x;
        for(x=g+1;x<2*g&&x<=N;x++) if(isrec[x]&&2*x-g<=N) c++;
        hit(10, pos[g] >= g + c); }
    for(w=1;w<=N;w++){ if(!isrec[w]) continue; int c=0,x;
        for(x=w/2+1;x<w;x++) if(isgnd[x]&&2*w-x<=N&&x*2>w) c++;
        hit(11, pos[w] <= w - c); }
    /* gnd below rec */
    for(g=1;g<=N;g++){ if(!isgnd[g]) continue;
      for(w=g+1;w<2*g && w<=N;w++){ if(!isrec[w]) continue;
        if(2*w-g<=N) hit(9, pos[w]<pos[g]);
      }
    }
}

static int ok(int x){
    int d;
    for(d=1;x-3*d>=1;d++) if(placed[x-d]&&placed[x-2*d]&&placed[x-3*d]&&
        pos[x-3*d]<pos[x-2*d]&&pos[x-2*d]<pos[x-d]) return 0;
    for(d=1;x+3*d<=N;d++) if(placed[x+d]&&placed[x+2*d]&&placed[x+3*d]&&
        pos[x+3*d]<pos[x+2*d]&&pos[x+2*d]<pos[x+d]) return 0;
    return 1;
}
static void rec(int t){
    if(t>N){ process(); return; }
    int x;
    for(x=1;x<=N;x++) if(!placed[x]&&ok(x)){ placed[x]=1;pos[x]=t;perm[t]=x; rec(t+1); placed[x]=0; }
}
int main(int argc,char**argv){
    N=atoi(argv[1]);
    memset(fire,0,sizeof(fire)); memset(viol,0,sizeof(viol));
    rec(1);
    printf("N=%d  boards=%lld\n",N,nboards);
    int r;
    for(r=0;r<NR;r++)
        printf("  %-3s fires %12lld  violations %lld   | %s\n",
               "", fire[r], viol[r], RN[r]);
    return 0;
}
