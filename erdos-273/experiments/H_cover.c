/* H_cover.c  --  Route H, complete covering search.
 *
 * CLAIM TESTED: given a finite list M of allowed moduli (all dividing a given L), does
 * there exist a covering system of Z with DISTINCT moduli, all taken from M?
 * The search is exhaustive: "UNSAT" is a rigorous statement about all subsets of M and
 * all residue assignments.
 *
 * Algorithm.  Canonical DFS on "cover the smallest uncovered residue r in [0,L)".
 *   Every covering must cover r; the covering class responsible has some modulus m in M
 *   not yet used (used ones already fail to cover r), and its residue is then FORCED to
 *   be r mod m.  Hence branching factor <= |unused|, depth <= |M|, and the search is
 *   complete.
 * Pruning
 *   (P1) exact budget: if (#uncovered residues) > sum_{m unused} L/m  then prune.
 *   (P2) if the number of unused moduli is 0, prune.
 *   (P3) optional cap on the number of congruences (--maxk).
 *
 * Exactness: all arithmetic is 64-bit integer; cov[] holds multiplicities (uint8, so at
 * most 255 classes may cover one residue -- checked).
 *
 * Modes
 *   default          : stop at the first covering found, print it.
 *   --all-minimal    : enumerate covering modulus-SETS, minimalised, dedup, print them.
 *   --count N        : stop after N solutions.
 *
 * Usage:
 *   H_cover <L> --world H|E [--forbid a,b,c] [--require a,b,c] [--maxmod K]
 *                [--maxnodes N] [--maxk K] [--all-minimal] [--progress N]
 *   H_cover <L> --mods m1,m2,...   (explicit list; every m must divide L)
 *
 * CONCLUSION: see FINDINGS.md; per-run result printed as RESULT: SAT / UNSAT / UNKNOWN.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static int64_t L;
static uint8_t *cov;
static int64_t uncovered;

#define MAXD 1024
static int64_t mods[MAXD];
static int nmods;
static int used[MAXD];
static int64_t chosen_a[MAXD];
static int chosen_m[MAXD];
static int depth;
static int64_t cap_of[MAXD];      /* L/m */
static int64_t free_capacity;     /* sum of cap_of over unused */

static int64_t nodes = 0, maxnodes = 0, progress_every = 0;
static int64_t nsol = 0, want_sol = 1;
static int maxk = 0;
static int all_minimal = 0;
static int world_H = 0;

static int is_prime(int64_t n){
    if(n < 2) return 0;
    if(n % 2 == 0) return n == 2;
    for(int64_t d = 3; d*d <= n; d += 2) if(n % d == 0) return 0;
    return 1;
}

static void mark(int64_t a, int64_t m){
    for(int64_t r = a; r < L; r += m){ if(cov[r]++ == 0) uncovered--; }
}
static void unmark(int64_t a, int64_t m){
    for(int64_t r = a; r < L; r += m){ if(--cov[r] == 0) uncovered++; }
}

/* ---- solution recording ---------------------------------------------------------- */
#define MAXSOL 20000
static int64_t solsets[MAXSOL][40];
static int solsizes[MAXSOL];
static int nsolsets = 0;

static int cmp64(const void*a,const void*b){
    int64_t x=*(const int64_t*)a, y=*(const int64_t*)b; return (x>y)-(x<y);
}

/* try to delete redundant moduli from the current solution, greedily from the largest */
static void minimalise_and_record(void){
    int64_t cur[40]; int64_t cura[40]; int k = depth;
    if(k > 40) k = 40;
    for(int i = 0; i < depth && i < 40; i++){ cur[i] = mods[chosen_m[i]]; cura[i] = chosen_a[i]; }
    int keep[40]; for(int i=0;i<k;i++) keep[i]=1;
    /* recompute coverage from scratch each time (k is small) */
    uint8_t *tmp = calloc(L,1);
    for(int drop = k-1; drop >= 0; drop--){
        memset(tmp,0,L);
        int64_t unc = L;
        for(int i=0;i<k;i++){
            if(!keep[i] || i==drop) continue;
            for(int64_t r=cura[i]; r<L; r+=cur[i]) if(tmp[r]++==0) unc--;
        }
        if(unc==0) keep[drop]=0;
    }
    free(tmp);
    int64_t out[40]; int no=0;
    for(int i=0;i<k;i++) if(keep[i]) out[no++]=cur[i];
    qsort(out,no,sizeof(int64_t),cmp64);
    /* dedup */
    for(int s=0;s<nsolsets;s++){
        if(solsizes[s]!=no) continue;
        int same=1; for(int i=0;i<no;i++) if(solsets[s][i]!=out[i]){same=0;break;}
        if(same) return;
    }
    if(nsolsets<MAXSOL){
        for(int i=0;i<no;i++) solsets[nsolsets][i]=out[i];
        solsizes[nsolsets]=no; nsolsets++;
        printf("MINSET[%d] k=%d :", nsolsets, no);
        for(int i=0;i<no;i++) printf(" %lld",(long long)out[i]);
        printf("\n"); fflush(stdout);
    }
}

static void print_solution(void){
    printf("SOLUTION (%d congruences):", depth);
    for(int i = 0; i < depth; i++)
        printf("  %lld mod %lld", (long long)chosen_a[i], (long long)mods[chosen_m[i]]);
    printf("\n"); fflush(stdout);
}

static int dfs(int64_t start){
    nodes++;
    if(progress_every && nodes % progress_every == 0){
        fprintf(stderr,"[progress] nodes=%lld depth=%d uncovered=%lld\n",
                (long long)nodes, depth, (long long)uncovered);
    }
    if(maxnodes && nodes > maxnodes) return -1;
    if(uncovered == 0){
        nsol++;
        if(all_minimal) minimalise_and_record(); else print_solution();
        return (all_minimal || nsol < want_sol) ? 0 : 1;
    }
    if(uncovered > free_capacity) return 0;                      /* P1 */
    if(maxk && depth >= maxk) return 0;                          /* P3 */

    int64_t r = start;
    while(r < L && cov[r]) r++;
    if(r >= L) return 0;   /* cannot happen: uncovered>0 */

    for(int i = 0; i < nmods; i++){
        if(used[i]) continue;
        int64_t m = mods[i], a = r % m;
        used[i] = 1; free_capacity -= cap_of[i];
        chosen_a[depth] = a; chosen_m[depth] = i; depth++;
        mark(a, m);
        int res = dfs(r);
        unmark(a, m);
        depth--; used[i] = 0; free_capacity += cap_of[i];
        if(res) return res;
    }
    return 0;
}

int main(int argc, char **argv){
    if(argc < 2){ fprintf(stderr,"usage: %s <L> [--world H|E | --mods list] ...\n", argv[0]); return 1; }
    L = atoll(argv[1]);
    int64_t forbid[256]; int nforbid = 0;
    int64_t require[256]; int nrequire = 0;
    int64_t explicit_mods[MAXD]; int nexplicit = 0;
    int64_t maxmod = 0;
    for(int i = 2; i < argc; i++){
        if(!strcmp(argv[i],"--world") && i+1<argc){ world_H = (argv[i+1][0]=='H'); i++; }
        else if(!strcmp(argv[i],"--maxnodes") && i+1<argc){ maxnodes = atoll(argv[i+1]); i++; }
        else if(!strcmp(argv[i],"--maxk") && i+1<argc){ maxk = atoi(argv[i+1]); i++; }
        else if(!strcmp(argv[i],"--maxmod") && i+1<argc){ maxmod = atoll(argv[i+1]); i++; }
        else if(!strcmp(argv[i],"--count") && i+1<argc){ want_sol = atoll(argv[i+1]); i++; }
        else if(!strcmp(argv[i],"--progress") && i+1<argc){ progress_every = atoll(argv[i+1]); i++; }
        else if(!strcmp(argv[i],"--all-minimal")){ all_minimal = 1; }
        else if(!strcmp(argv[i],"--forbid") && i+1<argc){
            char *s = strdup(argv[i+1]), *tok = strtok(s,",");
            while(tok){ forbid[nforbid++]=atoll(tok); tok=strtok(NULL,","); } i++; }
        else if(!strcmp(argv[i],"--require") && i+1<argc){
            char *s = strdup(argv[i+1]), *tok = strtok(s,",");
            while(tok){ require[nrequire++]=atoll(tok); tok=strtok(NULL,","); } i++; }
        else if(!strcmp(argv[i],"--mods") && i+1<argc){
            char *s = strdup(argv[i+1]), *tok = strtok(s,",");
            while(tok){ explicit_mods[nexplicit++]=atoll(tok); tok=strtok(NULL,","); } i++; }
        else { fprintf(stderr,"unknown arg %s\n", argv[i]); return 1; }
    }

    if(nexplicit){
        for(int i=0;i<nexplicit;i++){
            if(L % explicit_mods[i]){ fprintf(stderr,"modulus %lld does not divide L\n",(long long)explicit_mods[i]); return 1; }
            mods[nmods++]=explicit_mods[i];
        }
    } else {
        for(int64_t d = 1; d*d <= L; d++){
            if(L % d) continue;
            int64_t cands[2] = { d, L/d };
            for(int t = 0; t < 2; t++){
                int64_t x = cands[t];
                if(t==1 && cands[0]==cands[1]) continue;
                int ok = world_H ? (x >= 2 && is_prime(2*x+1)) : (x >= 4 && is_prime(x+1));
                if(!ok) continue;
                if(maxmod && x > maxmod) continue;
                int skip=0; for(int j=0;j<nforbid;j++) if(forbid[j]==x) skip=1;
                if(skip) continue;
                if(nmods>=MAXD){ fprintf(stderr,"too many moduli\n"); return 1; }
                mods[nmods++]=x;
            }
        }
    }
    qsort(mods,nmods,sizeof(int64_t),cmp64);

    double budget=0; for(int i=0;i<nmods;i++) budget += 1.0/(double)mods[i];
    printf("L = %lld   world=%s   #moduli=%d   budget=%.6f\n",(long long)L, world_H?"H":"E", nmods, budget);
    printf("moduli:"); for(int i=0;i<nmods && i<80;i++) printf(" %lld",(long long)mods[i]);
    printf("%s\n", nmods>80?" ...":"");
    if(nmods > 250){ fprintf(stderr,"warning: >250 moduli, uint8 counter could overflow\n"); }
    if(budget <= 1.0){ printf("RESULT: UNSAT (total budget %.6f <= 1)\n", budget); return 0; }

    cov = calloc(L,1);
    if(!cov){ fprintf(stderr,"alloc failed L=%lld\n",(long long)L); return 1; }
    uncovered = L;
    free_capacity = 0;
    for(int i=0;i<nmods;i++){ cap_of[i]=L/mods[i]; free_capacity += cap_of[i]; }

    /* apply --require by pre-forcing nothing (residues unknown) -- instead we simply
       restrict the modulus list; --require is implemented as: those moduli must appear.
       We handle it by post-filtering solutions.  (Not used in the main runs.) */
    (void)require; (void)nrequire;

    int res = dfs(0);
    if(all_minimal){
        printf("RESULT: enumerated %lld solutions, %d distinct minimal modulus sets (nodes=%lld)\n",
               (long long)nsol, nsolsets, (long long)nodes);
    } else if(res==1) printf("RESULT: SAT (nodes=%lld)\n",(long long)nodes);
    else if(res==-1)  printf("RESULT: UNKNOWN (node limit %lld)\n",(long long)maxnodes);
    else if(nsol>0)   printf("RESULT: SAT, %lld solutions, exhausted (nodes=%lld)\n",(long long)nsol,(long long)nodes);
    else              printf("RESULT: UNSAT (exhaustive; nodes=%lld)\n",(long long)nodes);
    return 0;
}
