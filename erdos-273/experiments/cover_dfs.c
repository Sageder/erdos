/* cover_dfs.c
 *
 * CLAIM TESTED: does there exist a covering system of Z with DISTINCT moduli, all of them
 * divisors of a given L and all of the form p-1 (p >= 5 prime)?   [E-world]
 * Optionally the same question in the "halved" H-world (moduli m with 2m+1 prime).
 *
 * Algorithm: exhaustive DFS on "cover the SMALLEST uncovered residue".  Every uncovered
 * residue must be covered by some unused modulus m, and then the residue class is forced
 * (a = r mod m).  So the branching factor is at most the number of unused moduli and the
 * search is complete: if it returns UNSAT, no covering with moduli dividing L exists.
 *
 * Pruning:
 *   (P1) budget:   #uncovered  >  sum over unused m of  L/m     =>  prune
 *   (P2) modulus m can only be tried if it is unused.
 *
 * Exactness: all arithmetic is exact 64-bit integer; the cover array counts multiplicities.
 *
 * Usage:  ./cover_dfs <L> [--world E|H] [--maxnodes N] [--first-only] [--forbid m1,m2,...]
 *                      [--require m1,m2,...]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static int64_t L;
static uint8_t *cov;      /* cov[r] = number of chosen classes covering r */
static int64_t uncovered;

#define MAXD 512
static int64_t mods[MAXD];
static int nmods;
static int used[MAXD];
static int64_t chosen_a[MAXD];
static int chosen_m[MAXD];
static int depth;

static int64_t nodes = 0, maxnodes = 0;
static int found = 0;
static int world_H = 0;

static int is_prime(int64_t n){
    if(n < 2) return 0;
    if(n % 2 == 0) return n == 2;
    for(int64_t d = 3; d*d <= n; d += 2) if(n % d == 0) return 0;
    return 1;
}

/* remaining reciprocal budget of unused moduli, as a count of residues they could cover */
static double remaining_capacity(void){
    double c = 0;
    for(int i = 0; i < nmods; i++) if(!used[i]) c += (double)L / (double)mods[i];
    return c;
}

static void mark(int64_t a, int64_t m){
    for(int64_t r = a; r < L; r += m){ if(cov[r]++ == 0) uncovered--; }
}
static void unmark(int64_t a, int64_t m){
    for(int64_t r = a; r < L; r += m){ if(--cov[r] == 0) uncovered++; }
}

static void print_solution(void){
    printf("SOLUTION (%d congruences):\n", depth);
    for(int i = 0; i < depth; i++)
        printf("   %lld mod %lld\n", (long long)chosen_a[i], (long long)mods[chosen_m[i]]);
    fflush(stdout);
}

static int dfs(int64_t start){
    nodes++;
    if(maxnodes && nodes > maxnodes) return -1;   /* budget exhausted */
    if(uncovered == 0){ found = 1; print_solution(); return 1; }
    if((double)uncovered > remaining_capacity() + 1e-9) return 0;   /* P1 */

    int64_t r = start;
    while(r < L && cov[r]) r++;
    if(r >= L){ found = 1; print_solution(); return 1; }

    for(int i = 0; i < nmods; i++){
        if(used[i]) continue;
        int64_t m = mods[i], a = r % m;
        used[i] = 1; chosen_a[depth] = a; chosen_m[depth] = i; depth++;
        mark(a, m);
        int res = dfs(r);
        unmark(a, m);
        depth--; used[i] = 0;
        if(res) return res;
    }
    return 0;
}

int main(int argc, char **argv){
    setbuf(stdout, NULL);
    if(argc < 2){ fprintf(stderr,"usage: %s <L> [--world E|H] [--maxnodes N]\n", argv[0]); return 1; }
    L = atoll(argv[1]);
    int64_t forbid[64]; int nforbid = 0;
    for(int i = 2; i < argc; i++){
        if(!strcmp(argv[i],"--world") && i+1 < argc){ world_H = (argv[i+1][0]=='H'); i++; }
        else if(!strcmp(argv[i],"--maxnodes") && i+1 < argc){ maxnodes = atoll(argv[i+1]); i++; }
        else if(!strcmp(argv[i],"--forbid") && i+1 < argc){
            char *s = strdup(argv[i+1]), *tok = strtok(s, ",");
            while(tok){ forbid[nforbid++] = atoll(tok); tok = strtok(NULL, ","); }
            i++;
        }
    }

    /* build the modulus list: divisors d of L with d >= (E: 4, H: 2) and (E: d+1, H: 2d+1) prime */
    for(int64_t d = 1; d*d <= L; d++){
        if(L % d) continue;
        int64_t cands[2] = { d, L/d };
        for(int t = 0; t < 2; t++){
            int64_t x = cands[t];
            if(t == 1 && cands[0] == cands[1]) continue;
            int ok = world_H ? (x >= 2 && is_prime(2*x+1)) : (x >= 4 && is_prime(x+1));
            if(!ok) continue;
            int skip = 0;
            for(int j = 0; j < nforbid; j++) if(forbid[j] == x) skip = 1;
            if(skip) continue;
            if(nmods >= MAXD){ fprintf(stderr,"too many moduli\n"); return 1; }
            mods[nmods++] = x;
        }
    }
    /* sort ascending */
    for(int i = 0; i < nmods; i++) for(int j = i+1; j < nmods; j++)
        if(mods[j] < mods[i]){ int64_t t = mods[i]; mods[i] = mods[j]; mods[j] = t; }

    double budget = 0; for(int i = 0; i < nmods; i++) budget += 1.0/(double)mods[i];
    printf("L = %lld   world = %s   #moduli = %d   budget = %.6f\n",
           (long long)L, world_H?"H":"E", nmods, budget);
    printf("moduli:"); for(int i = 0; i < nmods && i < 60; i++) printf(" %lld",(long long)mods[i]);
    printf("%s\n", nmods>60?" ...":"");
    if(nmods > 255){ fprintf(stderr,"cover counts could overflow uint8\n"); return 1; }
    if(budget <= 1.0){ printf("RESULT: UNSAT (budget <= 1: sum of 1/n over ALL available moduli is %.6f)\n", budget); return 0; }

    cov = calloc(L, 1);
    if(!cov){ fprintf(stderr,"alloc failed for L=%lld\n",(long long)L); return 1; }
    uncovered = L;

    int res = dfs(0);
    if(res == 1)       printf("RESULT: SAT   (nodes = %lld)\n", (long long)nodes);
    else if(res == -1) printf("RESULT: UNKNOWN (node limit %lld reached)\n", (long long)maxnodes);
    else               printf("RESULT: UNSAT (exhaustive; nodes = %lld)\n", (long long)nodes);
    return 0;
}
