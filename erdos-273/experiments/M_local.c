/* M_local.c  —  greedy + local-search / annealing finder for covering systems whose moduli are
 * DISTINCT divisors of L lying in E = {n >= 4 : n+1 prime}.
 *
 * CLAIM TESTED: for a given L, can Z/L be covered (or covered except a few residues) by classes
 * a_n mod n, one residue per admissible divisor n of L?
 *
 * KEY OBSERVATION making this formulation exact: coverage is MONOTONE in adding classes, and the
 * distinct-moduli convention allows at most one residue per modulus.  Hence there is no loss in
 * assigning a residue to EVERY admissible divisor of L: if some assignment covers Z/L, a covering
 * system exists (afterwards redundant classes may simply be deleted).  So the search space is the
 * product of Z/n over the admissible divisors n, and the objective is the number of uncovered
 * residues, to be driven to 0.
 *
 * This is a SEARCH heuristic: success is a certificate (independently re-verified elsewhere),
 * failure proves NOTHING.  Use M_sat.py for exact UNSAT verdicts.
 *
 * Usage: ./M_local <L> [--iters N] [--seed S] [--restarts R] [--target T] [--out FILE]
 *        --target T : stop when uncovered <= T (default 0)
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static int64_t L;
static uint16_t *cov;
static int64_t uncovered;

#define MAXD 4096
static int64_t mods[MAXD];
static int64_t res[MAXD];      /* current residue, -1 = unassigned */
static int nmods;

static uint64_t rng_s;
static uint64_t rnd(void){ rng_s ^= rng_s<<13; rng_s ^= rng_s>>7; rng_s ^= rng_s<<17; return rng_s; }

static int is_prime(int64_t n){
    if(n < 2) return 0;
    if(n % 2 == 0) return n == 2;
    for(int64_t d = 3; d*d <= n; d += 2) if(n % d == 0) return 0;
    return 1;
}

static void mark(int64_t a, int64_t m){
    for(int64_t r = a; r < L; r += m) if(cov[r]++ == 0) uncovered--;
}
static void unmark(int64_t a, int64_t m){
    for(int64_t r = a; r < L; r += m) if(--cov[r] == 0) uncovered++;
}
/* how many currently-uncovered residues would class a mod m newly cover? */
static int64_t gain(int64_t a, int64_t m){
    int64_t g = 0;
    for(int64_t r = a; r < L; r += m) if(cov[r] == 0) g++;
    return g;
}

int main(int argc, char **argv){
    setbuf(stdout, NULL);
    if(argc < 2){ fprintf(stderr,"usage: %s <L> [--iters N] [--seed S] [--restarts R] [--target T] [--out F]\n",argv[0]); return 1; }
    L = atoll(argv[1]);
    int64_t iters = 2000000, restarts = 1, target = 0;
    rng_s = 88172645463325252ULL;
    const char *outf = NULL;
    for(int i = 2; i < argc; i++){
        if(!strcmp(argv[i],"--iters")   && i+1<argc) iters   = atoll(argv[++i]);
        else if(!strcmp(argv[i],"--seed")&& i+1<argc) rng_s  = atoll(argv[++i]) * 2862933555777941757ULL + 3037000493ULL;
        else if(!strcmp(argv[i],"--restarts")&&i+1<argc) restarts = atoll(argv[++i]);
        else if(!strcmp(argv[i],"--target")&&i+1<argc) target = atoll(argv[++i]);
        else if(!strcmp(argv[i],"--out") && i+1<argc) outf = argv[++i];
    }
    for(int64_t d = 1; d*d <= L; d++){
        if(L % d) continue;
        int64_t c[2] = {d, L/d};
        for(int t = 0; t < 2; t++){
            if(t==1 && c[0]==c[1]) continue;
            int64_t x = c[t];
            if(x >= 4 && is_prime(x+1)){ if(nmods>=MAXD){fprintf(stderr,"MAXD\n");return 1;} mods[nmods++] = x; }
        }
    }
    for(int i=0;i<nmods;i++) for(int j=i+1;j<nmods;j++) if(mods[j]<mods[i]){int64_t t=mods[i];mods[i]=mods[j];mods[j]=t;}
    double budget=0; for(int i=0;i<nmods;i++) budget += 1.0/(double)mods[i];
    printf("L = %lld   #admissible divisors = %d   budget = %.6f   overlap budget (f-1)L = %.1f\n",
           (long long)L, nmods, budget, (budget-1.0)*(double)L);
    if(budget <= 1.0){ printf("RESULT: IMPOSSIBLE for this L (budget <= 1)\n"); return 0; }

    cov = calloc(L, sizeof(uint16_t));
    if(!cov){ fprintf(stderr,"alloc failed\n"); return 1; }

    int64_t bestever = L;
    for(int64_t rs = 0; rs < restarts; rs++){
        memset(cov, 0, L*sizeof(uint16_t));
        uncovered = L;
        /* greedy init: increasing modulus, residue maximising newly-covered count
           (for large moduli, sample residues instead of scanning all) */
        for(int i = 0; i < nmods; i++){
            int64_t m = mods[i], best = -1, bg = -1;
            int64_t tries = m <= 4096 ? m : 4096;
            for(int64_t t = 0; t < tries; t++){
                int64_t a = (m <= 4096) ? t : (int64_t)(rnd() % (uint64_t)m);
                int64_t g = gain(a, m);
                if(g > bg){ bg = g; best = a; }
            }
            if(rs > 0 && (rnd() % 100) < 15) best = (int64_t)(rnd() % (uint64_t)m); /* diversify */
            res[i] = best; mark(best, m);
        }
        printf("  restart %lld: after greedy, uncovered = %lld (%.4f%%)\n",
               (long long)rs, (long long)uncovered, 100.0*uncovered/L);
        int64_t best_local = uncovered;
        /* local search: repeatedly reassign one modulus to its best residue */
        for(int64_t it = 0; it < iters && uncovered > target; it++){
            int i = (int)(rnd() % (uint64_t)nmods);
            int64_t m = mods[i];
            unmark(res[i], m);
            int64_t best = res[i], bg = -1;
            int64_t tries = m <= 2048 ? m : 2048;
            for(int64_t t = 0; t < tries; t++){
                int64_t a = (m <= 2048) ? t : (int64_t)(rnd() % (uint64_t)m);
                int64_t g = gain(a, m);
                if(g > bg){ bg = g; best = a; }
            }
            /* occasional sideways/uphill move to escape plateaus */
            if((rnd() % 1000) < 5) best = (int64_t)(rnd() % (uint64_t)m);
            res[i] = best; mark(best, m);
            if(uncovered < best_local){
                best_local = uncovered;
                if(best_local < bestever){
                    bestever = best_local;
                    printf("    it %-10lld uncovered = %lld\n", (long long)it, (long long)uncovered);
                }
            }
        }
        printf("  restart %lld: final uncovered = %lld\n", (long long)rs, (long long)uncovered);
        if(uncovered <= target){
            printf("SUCCESS: uncovered = %lld <= target %lld\n", (long long)uncovered, (long long)target);
            FILE *fp = outf ? fopen(outf,"w") : stdout;
            fprintf(fp, "# L = %lld  uncovered = %lld\n", (long long)L, (long long)uncovered);
            for(int i = 0; i < nmods; i++) fprintf(fp, "%lld %lld\n", (long long)res[i], (long long)mods[i]);
            if(outf){ fclose(fp); printf("wrote %s\n", outf); }
            return 0;
        }
    }
    printf("RESULT: no cover found (best uncovered over all restarts = %lld). Proves nothing.\n",
           (long long)bestever);
    return 0;
}
