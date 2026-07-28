/* C_hcover2.c  --  Route C, Step 2 (C_hcover plus NO-GOOD recording).
 *
 * CLAIM TESTED.  Inside a fixed divisor lattice (every modulus must divide a given L):
 *   (i)   is there a covering system of Z with pairwise DISTINCT moduli, all in
 *         H = {m >= 2 : 2m+1 prime}  (equivalently: 2m in E = {p-1 : p >= 5 prime})?
 *   (ii)  the same while FORBIDDING a given list of moduli (e.g. 2, or 2 and 3);
 *   (iii) --pair : are there TWO such covering systems whose modulus sets are DISJOINT?
 *         By the Step-1 parity equivalence, (iii) SAT for some L is exactly a YES
 *         certificate for Erdos problem 273.
 *
 * ALGORITHM.  Exhaustive DFS on "cover the smallest uncovered residue".  If r is the
 * smallest uncovered residue then in any completion some unused modulus m covers it, and
 * the class is then FORCED to be r mod m.  Branching over the unused moduli is therefore
 * complete: UNSAT from this search means no covering exists with all moduli dividing L.
 *
 * DATA STRUCTURE.  The uncovered set is a sorted doubly linked list over [0,L) with an
 * undo stack: O(L) memory independent of depth, and the smallest uncovered residue is the
 * head.  Removing a class a mod m is done by whichever walk is cheaper: the class (L/m
 * steps) or the list (|U| steps).
 *
 * PRUNING
 *   P1  capacity:  |U| > sum over unused m of L/m                       -> prune
 *       (--pair)   |U_0|+|U_1| > sum over unused m of L/m               -> prune
 *                  (each modulus can serve at most one of the two systems)
 *   P2  exact best-class counts: when |U| <= HT, compute for every unused m the exact
 *       maximum number of elements of U inside one class mod m, and prune if the sum of
 *       those maxima is < |U|.  (--pair: sum of max(best_0, best_1) < |U_0|+|U_1|.)
 *   P3  reciprocal cap (--maxrecip R / --bb): prune when the reciprocal sum of the moduli
 *       chosen so far reaches R.  --bb turns this into branch-and-bound for the CHEAPEST
 *       covering (minimum sum of 1/m).
 *
 * EXACTNESS.  Exact 64-bit integer arithmetic.  Every solution is re-verified from scratch
 * by an independent full sweep of [0,L) before printing.
 *
 * NOTE (stated explicitly, as required): UNSAT for one divisor lattice L is NOT a proof
 * that no covering exists; it only rules out systems all of whose moduli divide L.
 *
 * CONCLUSION: printed per run; recorded in attempts/route-C-parity-H/FINDINGS.md.
 *
 * RUN LOG (question (ii): H-covering with distinct moduli avoiding the modulus 2):
 *   EXHAUSTIVE UNSAT proved for the divisor lattices L = 360 (165743 nodes),
 *   660 (88103), 720 (46021340), 810 (128879911).  Larger lattices did not finish.
 *   No H-covering avoiding 2 was found in ANY lattice searched (up to L = 10810800).
 *   REMINDER: UNSAT on one divisor lattice is NOT a proof of nonexistence in general.
 *
 * usage:
 *   ./C_hcover L [--world H|E] [--forbid a,b,c] [--pair] [--maxrecip R] [--bb]
 *              [--maxnodes N] [--all] [--order asc|desc|rand:SEED] [--ht T]
 *              [--maxmod M] [--timelimit SEC] [--quiet]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

typedef int64_t i64;

static i64 L;
static int world_H = 1;
static int pair_mode = 0;
static i64 maxnodes = 0;
static double maxrecip = 1e18;
static int find_all = 0, bb = 0;
static i64 HT = 250;
static double timelimit = 0;
static time_t t0;
static int quiet = 0;

#define MAXD 1024
static i64 mods[MAXD];
static int nmods;
static int used[MAXD];
static i64 cap_of[MAXD];

static i64 nodes = 0, nsol = 0, prunes_P2 = 0;
static double best_recip = 1e18;

static i64 ch_a[MAXD];
static int ch_m[MAXD], ch_sys[MAXD];
static int depth;
static double cur_recip;
static i64 cur_cap_left;
static i64 lowval[2] = {0, 0};     /* smallest allowed modulus VALUE, per system */
static int nclasses[2] = {0, 0};
static i64 capsum[2] = {0, 0};   /* sum of L/m over the moduli used by each system */
static int symbreak = 1;           /* translation symmetry break (on by default) */
static int evenonly = 0;         /* restrict to even moduli (E-side of the halving map) */
static i64 only_first = 0;         /* if set: system 0's smallest modulus must equal this */
static int randmode = 0;           /* randomized (1/m-weighted) candidate order per node */
static int restarts = 1;
static int candbuf[MAXD][MAXD];
/* NO-GOOD table.  When, at the smallest uncovered residue r, we branch over the candidate
 * moduli in a fixed order, the k-th branch may additionally ASSUME that none of the
 * candidates tried before it covers r (otherwise the solution is found in an earlier
 * branch).  We record those as forbidden residues.  This removes the factorial redundancy
 * of discovering the same set of classes in many different orders.  Completeness is kept:
 * in any solution, look at the FIRST candidate in our order whose class covers r. */
static unsigned char *forb;        /* forb[off[i] + a] = 1  means  a_i != a */
static i64 *off;
static int32_t *fstack; static i64 ftop = 0;

/* ---------------- uncovered set: sorted doubly linked list + undo stack ---------------- */
typedef struct {
    int32_t *nxt, *prv, *undo;
    unsigned char *in;
    int32_t head;
    i64 n, utop;
} Uset;
static Uset S0, S1;

static void uset_init(Uset *u) {
    u->nxt = malloc((size_t)(L + 2) * 4);
    u->prv = malloc((size_t)(L + 2) * 4);
    u->undo = malloc((size_t)(L + 2) * 4);
    u->in = malloc((size_t)(L + 2));
    if (!u->nxt || !u->prv || !u->undo || !u->in) { fprintf(stderr, "alloc fail\n"); exit(1); }
    for (i64 x = 0; x < L; x++) { u->nxt[x] = (int32_t)(x + 1); u->prv[x] = (int32_t)(x - 1); u->in[x] = 1; }
    u->nxt[L] = (int32_t)L; u->prv[L] = (int32_t)(L - 1); u->in[L] = 0;
    u->head = 0; u->n = L; u->utop = 0;
}
static inline void uset_remove(Uset *u, i64 x) {
    int32_t p = u->prv[x], nx = u->nxt[x];
    if (p < 0) { u->head = nx; u->prv[nx] = -1; }
    else { u->nxt[p] = nx; u->prv[nx] = p; }
    u->in[x] = 0;
    u->undo[u->utop++] = (int32_t)x;
    u->n--;
}
static void uset_restore(Uset *u, i64 to) {
    while (u->utop > to) {
        int32_t x = u->undo[--u->utop];
        int32_t p = u->prv[x], nx = u->nxt[x];
        if (p < 0) u->head = x; else u->nxt[p] = x;
        u->prv[nx] = x;
        u->in[x] = 1;
        u->n++;
    }
}

static int is_prime(i64 n) {
    if (n < 2) return 0;
    if (n % 2 == 0) return n == 2;
    for (i64 d = 3; d * d <= n; d += 2) if (n % d == 0) return 0;
    return 1;
}
/* world_H: 1 = H (2x+1 prime), 0 = E (x+1 prime, x>=4), 2 = A (all divisors > 1) */
static int in_world(i64 x) {
    if (world_H == 2) return x >= 2;
    return world_H ? (x >= 2 && is_prime(2 * x + 1)) : (x >= 4 && is_prime(x + 1));
}

static int verify(int sys) {
    unsigned char *c = calloc(L, 1);
    if (!c) { fprintf(stderr, "verify alloc fail\n"); exit(1); }
    for (int i = 0; i < depth; i++) {
        if (pair_mode && ch_sys[i] != sys) continue;
        i64 m = mods[ch_m[i]], a = ((ch_a[i] % m) + m) % m;
        for (i64 x = a; x < L; x += m) c[x] = 1;
    }
    i64 bad = -1;
    for (i64 x = 0; x < L; x++) if (!c[x]) { bad = x; break; }
    free(c);
    return bad < 0;
}

static void print_solution(void) {
    double r0 = 0, r1 = 0;
    printf("SOLUTION  (%d classes)\n", depth);
    for (int s = 0; s <= (pair_mode ? 1 : 0); s++) {
        printf("  system %d moduli:", s);
        for (int i = 0; i < depth; i++) if (!pair_mode || ch_sys[i] == s)
            printf(" %lld", (long long)mods[ch_m[i]]);
        printf("\n  system %d classes:", s);
        for (int i = 0; i < depth; i++) if (!pair_mode || ch_sys[i] == s) {
            printf("  %lld mod %lld", (long long)ch_a[i], (long long)mods[ch_m[i]]);
            if (s == 0) r0 += 1.0 / (double)mods[ch_m[i]]; else r1 += 1.0 / (double)mods[ch_m[i]];
        }
        printf("\n");
    }
    printf("  recip sums: %.6f", r0);
    if (pair_mode) printf(" , %.6f", r1);
    printf("   total %.6f\n", r0 + r1);
    for (int i = 0; i < depth; i++) for (int j = i + 1; j < depth; j++)
        if (ch_m[i] == ch_m[j]) printf("  *** DISTINCTNESS VIOLATION ***\n");
    int ok = verify(0) && (!pair_mode || verify(1));
    printf("  independent full-period re-verification: %s\n", ok ? "PASS" : "*** FAIL ***");
    fflush(stdout);
}

/* ---- exact max-class-count via open-addressing table with generation stamps ---- */
static i64 *hkey; static int32_t *hcnt; static uint32_t *hgen; static uint32_t hcur = 0;
static i64 hsize = 0;
static void htab_init(i64 cap) {
    hsize = 16; while (hsize < 4 * cap) hsize <<= 1;
    hkey = malloc(hsize * sizeof(i64));
    hcnt = malloc(hsize * 4);
    hgen = calloc(hsize, 4);
    if (!hkey || !hcnt || !hgen) { fprintf(stderr, "htab alloc fail\n"); exit(1); }
}
/* exact maximum number of elements of the array v[0..n) lying in one class mod m */
static i64 max_class_arr(const int32_t *v, i64 n, i64 m) {
    if (++hcur == 0) { memset(hgen, 0, hsize * 4); hcur = 1; }
    i64 best = 0;
    for (i64 t = 0; t < n; t++) {
        i64 k = v[t] % m;
        i64 h = (i64)(((uint64_t)k * 0x9E3779B97F4A7C15ULL) & (uint64_t)(hsize - 1));
        while (1) {
            if (hgen[h] != hcur) { hgen[h] = hcur; hkey[h] = k; hcnt[h] = 1; if (best < 1) best = 1; break; }
            if (hkey[h] == k) { if (++hcnt[h] > best) best = hcnt[h]; break; }
            h = (h + 1) & (hsize - 1);
        }
    }
    return best;
}
static int32_t *scr0 = NULL, *scr1 = NULL;
static i64 gather(Uset *u, int32_t *dst) {
    i64 c = 0;
    for (int32_t x = u->head; x < (int32_t)L; x = u->nxt[x]) dst[c++] = x;
    return c;
}

static int timeup(void) { return timelimit && (double)(time(NULL) - t0) > timelimit; }

static int dfs(void) {
    nodes++;
    if ((nodes & 0x3FFF) == 0) {
        if (!quiet) { fprintf(stderr, "\r  nodes=%lld d=%d |U0|=%lld |U1|=%lld p2=%lld    ",
                              (long long)nodes, depth, (long long)S0.n,
                              (long long)(pair_mode ? S1.n : 0), (long long)prunes_P2);
                      fflush(stderr); }
        if (timeup()) return -1;
    }
    if (maxnodes && nodes > maxnodes) return -1;

    i64 need = S0.n + (pair_mode ? S1.n : 0);
    if (need == 0) {
        nsol++;
        if (cur_recip < best_recip) best_recip = cur_recip;
        print_solution();
        if (bb) { maxrecip = cur_recip - 1e-12; return 0; }
        return find_all ? 0 : 1;
    }
    if (need > cur_cap_left) return 0;
    if (cur_recip >= maxrecip) return 0;
    /* P4 (exact integer, Davenport-Mirsky-Newman-Rado): a covering system with pairwise
     * distinct moduli > 1 has sum 1/m > 1 strictly, i.e. sum L/m > L.  An incomplete
     * system can only reach capsum[j] + cur_cap_left, so prune when that is <= L.
     * In pair mode the unused capacity is SHARED, giving the joint bound as well. */
    {
        int nsys = pair_mode ? 2 : 1;
        for (int j = 0; j < nsys; j++) {
            i64 nj = j ? S1.n : S0.n;
            if (nj > 0 && capsum[j] + cur_cap_left <= L) return 0;
        }
        if (pair_mode && (S0.n > 0 || S1.n > 0) &&
            capsum[0] + capsum[1] + cur_cap_left <= 2 * L) return 0;
    }

    /* P2: sum over unused m of the exact best-class count must be >= |U| (per system, and
     * jointly in pair mode since a modulus can serve only one system). */
    {
        i64 g0 = -1, g1 = -1;
        if (S0.n > 0 && S0.n <= HT) g0 = gather(&S0, scr0);
        if (pair_mode && S1.n > 0 && S1.n <= HT) g1 = gather(&S1, scr1);
        int usable = (S0.n == 0 || g0 >= 0) && (!pair_mode || S1.n == 0 || g1 >= 0);
        if (usable && (g0 >= 0 || g1 >= 0)) {
            i64 tot = 0;
            for (int i = 0; i < nmods && tot < need; i++) {
                if (used[i]) continue;
                i64 m = mods[i], cap = L / m;
                i64 b0 = 0, b1 = 0;
                if (S0.n > 0) b0 = (g0 >= 0) ? max_class_arr(scr0, g0, m)
                                             : (cap < S0.n ? cap : S0.n);
                if (pair_mode && S1.n > 0) b1 = (g1 >= 0) ? max_class_arr(scr1, g1, m)
                                                          : (cap < S1.n ? cap : S1.n);
                tot += (b0 > b1 ? b0 : b1);
            }
            if (tot < need) { prunes_P2++; return 0; }
        }
    }

    int sys = 0;
    if (pair_mode) {
        if (S0.n == 0) sys = 1;
        else if (S1.n == 0) sys = 0;
        else sys = (S1.n > S0.n) ? 1 : 0;
    }
    Uset *u = sys ? &S1 : &S0;
    i64 r = u->head;
    int first = (nclasses[sys] == 0);

    /* candidate order at this node */
    int *cand = candbuf[depth];
    int ncand = 0;
    for (int i = 0; i < nmods; i++) {
        if (used[i]) continue;
        if (mods[i] < lowval[sys]) continue;
        if (only_first && sys == 0 && first && mods[i] != only_first) continue;
        cand[ncand++] = i;
    }
    if (randmode) {   /* weighted random permutation: weight 1/m (small moduli first) */
        for (int k = 0; k < ncand; k++) {
            double tot = 0;
            for (int t = k; t < ncand; t++) tot += 1.0 / (double)mods[cand[t]];
            double x = ((double)rand() / ((double)RAND_MAX + 1.0)) * tot, acc = 0;
            int pick = ncand - 1;
            for (int t = k; t < ncand; t++) { acc += 1.0 / (double)mods[cand[t]];
                                              if (acc >= x) { pick = t; break; } }
            int tmp = cand[k]; cand[k] = cand[pick]; cand[pick] = tmp;
        }
    }

    i64 fmark = ftop;
    for (int ci = 0; ci < ncand; ci++) {
        int i = cand[ci];
        i64 m = mods[i], a = r % m;
        if (forb[off[i] + a]) continue;      /* no-good: this branch already excluded */
        i64 mark = u->utop;
        i64 save_low = lowval[sys];
        if (symbreak && first) lowval[sys] = mods[i]; /* the FIRST class of a system may be
                                                 * assumed to use its SMALLEST modulus:
                                                 * translate the system so that this class
                                                 * is 0 mod m (it already is, since r = 0). */
        if (L / m < u->n) { for (i64 x = a; x < L; x += m) if (u->in[x]) uset_remove(u, x); }
        else { int32_t x = u->head; while (x < (int32_t)L) { int32_t nx = u->nxt[x];
                   if (x % m == a) uset_remove(u, x); x = nx; } }
        used[i] = sys + 1;
        ch_a[depth] = a; ch_m[depth] = i; ch_sys[depth] = sys; depth++;
        nclasses[sys]++;
        capsum[sys] += cap_of[i];
        cur_recip += 1.0 / (double)m;
        cur_cap_left -= cap_of[i];

        int res = dfs();

        cur_cap_left += cap_of[i];
        cur_recip -= 1.0 / (double)m;
        nclasses[sys]--;
        capsum[sys] -= cap_of[i];
        depth--; used[i] = 0;
        lowval[sys] = save_low;
        uset_restore(u, mark);
        if (res) { while (ftop > fmark) { forb[fstack[--ftop]] = 0; } return res; }
        /* moving on to the next candidate: assume this one does NOT cover r */
        forb[off[i] + a] = 1; fstack[ftop++] = (int32_t)(off[i] + a);
    }
    while (ftop > fmark) forb[fstack[--ftop]] = 0;
    return 0;
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: %s L [opts]\n", argv[0]); return 1; }
    L = atoll(argv[1]);
    i64 forbid[512]; int nforbid = 0;
    i64 maxmod = 0;
    const char *order = "asc";
    for (int i = 2; i < argc; i++) {
        if (!strcmp(argv[i], "--world") && i + 1 < argc) { char c = argv[++i][0]; world_H = (c=='H')?1:((c=='A')?2:0); }
        else if (!strcmp(argv[i], "--forbid") && i + 1 < argc) {
            char *s = strdup(argv[++i]), *tok = strtok(s, ",");
            while (tok) { forbid[nforbid++] = atoll(tok); tok = strtok(NULL, ","); }
        }
        else if (!strcmp(argv[i], "--pair")) pair_mode = 1;
        else if (!strcmp(argv[i], "--bb")) { bb = 1; find_all = 1; }
        else if (!strcmp(argv[i], "--maxrecip") && i + 1 < argc) maxrecip = atof(argv[++i]);
        else if (!strcmp(argv[i], "--maxnodes") && i + 1 < argc) maxnodes = atoll(argv[++i]);
        else if (!strcmp(argv[i], "--all")) find_all = 1;
        else if (!strcmp(argv[i], "--ht") && i + 1 < argc) HT = atoll(argv[++i]);
        else if (!strcmp(argv[i], "--maxmod") && i + 1 < argc) maxmod = atoll(argv[++i]);
        else if (!strcmp(argv[i], "--order") && i + 1 < argc) order = argv[++i];
        else if (!strcmp(argv[i], "--timelimit") && i + 1 < argc) timelimit = atof(argv[++i]);
        else if (!strcmp(argv[i], "--quiet")) quiet = 1;
        else if (!strcmp(argv[i], "--nosym")) symbreak = 0;
        else if (!strcmp(argv[i], "--evenonly")) evenonly = 1;
        else if (!strcmp(argv[i], "--rand") && i + 1 < argc) { randmode = 1; srand((unsigned)atoi(argv[++i])); }
        else if (!strcmp(argv[i], "--restarts") && i + 1 < argc) restarts = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--only") && i + 1 < argc) only_first = atoll(argv[++i]);
        else { fprintf(stderr, "unknown option %s\n", argv[i]); return 1; }
    }

    for (i64 d = 1; d * d <= L; d++) {
        if (L % d) continue;
        i64 cands[2] = { d, L / d };
        for (int t = 0; t < 2; t++) {
            if (t == 1 && cands[0] == cands[1]) continue;
            i64 x = cands[t];
            if (!in_world(x)) continue;
            if (evenonly && (x % 2)) continue;
            if (maxmod && x > maxmod) continue;
            int skip = 0;
            for (int j = 0; j < nforbid; j++) if (forbid[j] == x) skip = 1;
            if (skip) continue;
            if (nmods >= MAXD) { fprintf(stderr, "too many moduli\n"); return 1; }
            mods[nmods++] = x;
        }
    }
    for (int i = 0; i < nmods; i++) for (int j = i + 1; j < nmods; j++)
        if (mods[j] < mods[i]) { i64 t = mods[i]; mods[i] = mods[j]; mods[j] = t; }
    if (!strcmp(order, "desc")) {
        for (int i = 0, j = nmods - 1; i < j; i++, j--) { i64 t = mods[i]; mods[i] = mods[j]; mods[j] = t; }
    } else if (!strncmp(order, "rand:", 5)) {
        srand((unsigned)atoi(order + 5));
        for (int i = nmods - 1; i > 0; i--) { int j = rand() % (i + 1); i64 t = mods[i]; mods[i] = mods[j]; mods[j] = t; }
    }

    double budget = 0;
    for (int i = 0; i < nmods; i++) { budget += 1.0 / (double)mods[i]; cap_of[i] = L / mods[i]; }
    printf("L = %lld   world = %s   pair = %d   #moduli = %d   budget = %.6f\n",
           (long long)L, world_H ? "H" : "E", pair_mode, nmods, budget);
    printf("moduli:");
    for (int i = 0; i < nmods && i < 250; i++) printf(" %lld", (long long)mods[i]);
    printf("%s\n", nmods > 250 ? " ..." : "");
    fflush(stdout);
    if (budget <= (pair_mode ? 2.0 : 1.0)) {
        printf("RESULT: UNSAT (reciprocal budget %.6f <= %d; each system needs sum 1/m > 1)\n",
               budget, pair_mode ? 2 : 1);
        return 0;
    }

    off = malloc((size_t)(nmods + 1) * sizeof(i64));
    i64 tot = 0;
    for (int i = 0; i < nmods; i++) { off[i] = tot; tot += mods[i]; }
    forb = calloc((size_t)tot + 1, 1);
    fstack = malloc(((size_t)tot + 1) * 4);
    if (!off || !forb || !fstack) { fprintf(stderr, "no-good alloc fail\n"); return 1; }
    uset_init(&S0);
    if (pair_mode) uset_init(&S1);
    htab_init(HT + 4);
    scr0 = malloc((size_t)(HT + 4) * 4);
    scr1 = malloc((size_t)(HT + 4) * 4);
    if (!scr0 || !scr1) { fprintf(stderr, "scratch alloc fail\n"); return 1; }
    cur_cap_left = 0;
    for (int i = 0; i < nmods; i++) cur_cap_left += cap_of[i];
    cur_recip = 0; depth = 0;
    t0 = time(NULL);

    int res = 0;
    for (int rst = 0; rst < restarts; rst++) {
        res = dfs();
        if (res != -1 || !randmode) break;
        /* restart: clear state */
        uset_restore(&S0, 0);
        if (pair_mode) uset_restore(&S1, 0);
        for (int i = 0; i < nmods; i++) used[i] = 0;
        depth = 0; nclasses[0] = nclasses[1] = 0; lowval[0] = lowval[1] = 0;
        capsum[0] = capsum[1] = 0;
        cur_recip = 0; cur_cap_left = 0;
        for (int i = 0; i < nmods; i++) cur_cap_left += cap_of[i];
        nodes = 0;
        if (!quiet) fprintf(stderr, "\n[restart %d]\n", rst + 1);
        if (timeup()) break;
    }
    fprintf(stderr, "\n");
    if (res == -1)      printf("RESULT: UNKNOWN (node/time budget exhausted; nodes = %lld)\n", (long long)nodes);
    else if (nsol > 0)  printf("RESULT: SAT (%lld solution(s); nodes = %lld; best recip %.6f)\n",
                               (long long)nsol, (long long)nodes, best_recip);
    else                printf("RESULT: UNSAT (exhaustive over this divisor lattice; nodes = %lld)\n",
                               (long long)nodes);
    printf("CAVEAT: this settles only systems all of whose moduli divide L = %lld.\n", (long long)L);
    return 0;
}
