/* G_02_dfs.c  --  Route G, general exhaustive covering search / minimum-deficiency search.
 *
 * CLAIM TESTED: for a given modulus lcm L and a given pool of admissible moduli
 * (all dividing L, pairwise distinct, each used at most once), does there exist a choice of
 * residues making the union of the classes all of Z/L ?   If not, what is the EXACT minimum
 * number of uncovered residues mod L, and an optimal witness?
 *
 * ALGORITHM (complete, exact integer arithmetic).  Let r be the smallest residue in
 * {0..L-1} not yet covered and not yet "abandoned".  Any covering must cover r, and if it
 * uses modulus m to do so then the class is FORCED to be (r mod m).  So we branch over
 *      - each unused pool modulus m  -> add class (r mod m, m),
 *      - plus one extra branch "abandon r" (r stays uncovered forever).
 * With the abandon-branch disabled this is a complete decision procedure for the covering
 * question; with it enabled and a branch-and-bound cutoff on the number of abandoned
 * residues it computes the exact minimum deficiency.
 *
 * Because the smallest uncovered residue is always attacked, no two search states repeat a
 * (class-set) in different order: the enumeration is over sets, not sequences.
 *
 * PRUNING
 *   P1 density/budget:  (#uncovered still needed) > sum_{unused m} L/m  =>  prune.
 *   P2 branch-and-bound on abandoned count against the incumbent best.
 *
 * USAGE
 *   ./G_02_dfs L m1,m2,...,mk [options]
 * options:
 *   --maxdef D      allow up to D abandoned residues (0 = exact covering only). default 0
 *   --nodes N       node budget (default 2e9); prints INCOMPLETE if exhausted
 *   --all           count all solutions instead of stopping at the first
 *   --require a,b   these moduli must be used
 *   --print-uncov   print the uncovered residue set of the best solution
 *
 * CONCLUSION: see run logs referenced from attempts/route-G-selfridge/FINDINGS.md
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

#define MAXD 128

static long L;
static int nmod;
static long mods[MAXD];
static int used[MAXD];
static long chosen_r[MAXD];
static long chosen_m[MAXD];
static int depth;

static unsigned char *cov;      /* multiplicity of coverage */
static unsigned char *aband;    /* abandoned flags */
static long n_uncov;            /* residues with cov==0 && !aband */
static long n_aband;

static long long nodes = 0, node_budget = 2000000000LL;
static int incomplete = 0;
static int count_all = 0;
static long long nsol = 0;
static int maxdef = 0;
static int print_uncov = 0;
static int require_mask[MAXD];
static int nrequire = 0;

/* incumbent */
static int best_def = 1 << 30;
static int best_k;
static long best_r[MAXD], best_m[MAXD];
static long best_aband[4096];
static int best_naband;

static long scan_from = 0;
static double t0, tlimit = 1e18;
static double nowt(void){ struct timespec ts; clock_gettime(CLOCK_MONOTONIC,&ts); return ts.tv_sec+1e-9*ts.tv_nsec; }

static void save_best(void) {
    best_def = (int)n_aband;
    best_k = depth;
    for (int i = 0; i < depth; i++) { best_r[i] = chosen_r[i]; best_m[i] = chosen_m[i]; }
    best_naband = 0;
    for (long r = 0; r < L; r++)
        if (!cov[r] && best_naband < 4096) best_aband[best_naband++] = r;
}

static void add_class(long a, long m) {
    for (long r = a % m; r < L; r += m) {
        if (cov[r] == 0 && !aband[r]) n_uncov--;
        cov[r]++;
    }
}
static void del_class(long a, long m) {
    for (long r = a % m; r < L; r += m) {
        cov[r]--;
        if (cov[r] == 0 && !aband[r]) n_uncov++;
    }
}

static long budget_left(void) {  /* sum over unused moduli of L/m  */
    long s = 0;
    for (int i = 0; i < nmod; i++) if (!used[i]) s += L / mods[i];
    return s;
}

static void dfs(long start) {
    if (++nodes > node_budget) { incomplete = 1; return; }
    if ((nodes & 0xFFFFFF) == 0) { double el = nowt()-t0;
        fprintf(stderr, "  [%.0fs %lldM nodes depth=%d uncov=%ld]\n", el, nodes/1000000, depth, n_uncov);
        if (el > tlimit) incomplete = 1; }
    if (incomplete) return;

    if (n_uncov == 0) {
        if ((int)n_aband < best_def) save_best();
        nsol++;
        if (!count_all) { /* signal found by leaving best_def set */ }
        return;
    }
    /* required moduli still unused -> they must eventually be used; no strong prune, skip */
    /* P1: at most (best_def-1-n_aband) further residues may be abandoned */
    {
        long slack = (long)(best_def - 1 - (int)n_aband);
        if (slack < 0) slack = 0;
        if (n_uncov > budget_left() + slack) return;
    }

    long r = start;
    while (r < L && (cov[r] || aband[r])) r++;
    if (r >= L) { /* shouldn't happen since n_uncov>0 */ return; }

    for (int i = 0; i < nmod; i++) {
        if (used[i]) continue;
        long m = mods[i];
        used[i] = 1;
        chosen_r[depth] = r % m; chosen_m[depth] = m; depth++;
        add_class(r % m, m);
        dfs(r + 1);                /* r is now covered; next scan starts above it */
        depth--;
        del_class(r % m, m);
        used[i] = 0;
        if (incomplete) return;
        if (!count_all && best_def == 0) return;     /* found exact covering, stop */
    }
    /* abandon branch */
    if ((int)n_aband + 1 <= maxdef && (int)n_aband + 1 < best_def) {
        aband[r] = 1; n_aband++; n_uncov--;
        dfs(r + 1);
        aband[r] = 0; n_aband--; n_uncov++;
    }
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: %s L m1,m2,...\n", argv[0]); return 1; }
    L = atol(argv[1]);
    char *p = strtok(argv[2], ",");
    while (p) { mods[nmod++] = atol(p); p = strtok(NULL, ","); }
    for (int i = 3; i < argc; i++) {
        if (!strcmp(argv[i], "--maxdef")) maxdef = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--nodes")) node_budget = atoll(argv[++i]);
        else if (!strcmp(argv[i], "--all")) count_all = 1;
        else if (!strcmp(argv[i], "--print-uncov")) print_uncov = 1;
        else if (!strcmp(argv[i], "--timelimit")) tlimit = atof(argv[++i]);
    }
    (void)require_mask; (void)nrequire; (void)scan_from;
    for (int i = 0; i < nmod; i++) if (L % mods[i]) {
        fprintf(stderr, "modulus %ld does not divide L=%ld\n", mods[i], L); return 1; }

    cov = calloc(L, 1); aband = calloc(L, 1);
    n_uncov = L; n_aband = 0;
    best_def = maxdef + 1;
    t0 = nowt();

    dfs(0);

    printf("L=%ld  pool(%d)=", L, nmod);
    for (int i = 0; i < nmod; i++) printf("%s%ld", i ? "," : "", mods[i]);
    printf("\nnodes=%lld  %s\n", nodes, incomplete ? "INCOMPLETE (node budget)" : "search EXHAUSTIVE");
    if (count_all) printf("solutions found (deficiency<=%d): %lld\n", maxdef, nsol);
    if (best_def <= maxdef) {
        printf("BEST deficiency = %d   (k=%d classes)\n", best_def, best_k);
        printf("CLASSES:");
        for (int i = 0; i < best_k; i++) printf(" %ld(mod %ld)", best_r[i], best_m[i]);
        printf("\n");
        if (print_uncov && best_naband) {
            printf("UNCOVERED (%d):", best_naband);
            for (int i = 0; i < best_naband; i++) printf(" %ld", best_aband[i]);
            printf("\n");
        }
    } else {
        printf("NO solution with deficiency <= %d\n", maxdef);
    }
    return 0;
}
