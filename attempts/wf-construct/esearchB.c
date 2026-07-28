/* esearch.c -- EXACT arbitrary-precision search for legal block systems with a
 * prescribed reciprocal sum, inside a range [T,N].  No 128-bit ceiling.
 *
 * PROBLEM.  Given T <= N and a rational u/v > 0, decide/enumerate the sets
 *      W subset of a given universe A subset [T,N]
 * with NO ISOLATED POINT (every n in W has n-1 in W or n+1 in W, as integers)
 * and  sum_{n in W} 1/n = u/v  exactly.
 *
 * ------------------------------------------------------------------------
 * THE RESCALING (this is what removes the 128-bit ceiling AND makes the
 * pooled divisibility prune free)
 *
 * Let A = {e_0 < e_1 < ... < e_{cnt-1}} be the (pruned) universe and put
 *      L_i = lcm{ e_j : j >= i },        L_cnt = 1.
 * Along the DFS let S_i be the residual target after deciding indices < i.
 * S_i must be a sum of 1/e_j over a subset of {j >= i}, so L_i*S_i is a
 * NONNEGATIVE INTEGER.  The engine carries exactly that integer,
 *      X_i := S_i * L_i.
 * With  w_i := L_i/e_i  (an integer) and  g_i := L_i/L_{i+1}  one has
 *      take e_i :  X_{i+1} = (X_i - w_i)/g_i
 *      skip e_i :  X_{i+1} =  X_i      /g_i
 * and in both cases EXACT DIVISIBILITY BY g_i IS EXACTLY the pooled prune
 * "Q[i] | R" of the old fixed-scale engines (Q[i] = L_0/L_i, R = S_i*L_0):
 *      Q[i] | R  <=>  S_i*L_i in Z  <=>  X_i in Z.
 * Moreover g_i divides e_i (if p^a drops out of the lcm at i then e_i is the
 * unique remaining multiple of p^a, so p^a | e_i, and the p^a for distinct p
 * are coprime), hence g_i <= N always fits in a machine word: the prune is a
 * multiword-by-single-word division, never a big/big remainder.
 * Finally X_i <= Tail_i := (sum_{j>=i} 1/e_j) * L_i, and L_i collapses as i
 * grows, so the operand width SHRINKS with depth -- the deep, wide part of the
 * tree runs on one or two words.
 *
 * PRUNES KEPT
 *   (P1) 0 <= X_i <= Tail_i           (feasibility; Tail_i is exact)
 *   (P2) g_i | (X_i - [take] w_i)     (== the Rule-(P) pooled prune)
 *   (P3) endgame table over the top K indices (see below)
 *   plus the Rule-(P) + legality universe fixpoint, applied offline by prune.py.
 *
 * ENDGAME TABLE.  For each incoming legality state c in {0,1,2} we enumerate
 * every legal completion of the top K indices and store the 61-bit FINGERPRINT
 * (X mod P, P = 2^61-1) of its weight sum, sorted+deduped.  At the split the
 * DFS looks up its own fingerprint; a miss is a PROOF that no completion works
 * (fingerprints never produce false negatives), a hit triggers an EXACT
 * multiword completion which re-derives the solutions from scratch.  So the
 * engine is exact: fingerprints can only cost time, never correctness.
 *
 * usage:  ./esearch probfile [options]
 *   probfile:  line 1 "T N u v", line 2 "cnt", line 3 the cnt universe elements
 *              (this is what prune.py writes)
 *   -k K      endgame size in universe indices (default 0 = off)
 *   -c CAP    abort endgame build past CAP entries (default 8e7)
 *   -m M      stop after M solutions
 *   -j J -i I split the search tree J ways, run part I
 *   -d D      index at which the J-way split is taken (default 6)
 *   -R SEED   randomised restart mode with the given seed (finds certificates)
 *   -B B      node budget per restart in randomised mode (default 3e7)
 *   -t SECS   wall-clock limit
 *   -q        do not print solutions, only count
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>
#include "bigint.h"
#include "padicB.h"

#define MAXW 200            /* 12800 bits of headroom for lcm(universe)      */
#define MAXC 20000

static int T0, Nhi, cnt;
static long long UNUM = 1, VDEN = 1;
static int BIGMODE = 0;
static char BIGDEC[8192];
static int el[MAXC], adj[MAXC];
static int gdiv[MAXC];          /* g_i = L_i / L_{i+1}, divides e_i          */
static int nwp[MAXC + 1];       /* words needed for Tail_i (>=1), monotone   */
static int NW;                  /* stride = words(Tail_0)                    */
static u64 *Wv, *Tl, *Xs;       /* w_i, Tail_i, DFS stack: [i*NW ...]        */

static long long nodes = 0, nsol = 0, maxsol = (1LL << 60);
static int chosen[MAXC], nch = 0;
static int SPLITK = 0, SPLIT;   /* SPLIT = cnt - SPLITK                      */
static int inEmit = 0, quiet = 0;
static int nsplitw = 1, ipart = 0, splitdepth = 6;
static long long taskctr = 0;
static long long budget = 0, budleft = 0, tabcapmax = 80000000LL;
static int randmode = 0, stopflag = 0, takepct = 50;
static unsigned long long rng = 0x243F6A8885A308D3ULL;
static double tlimit = 0;
static clock_t t_start;
static time_t wall_start;

static const u64 FP = (1ULL << 61) - 1;   /* 2^61-1, prime */
static u64 *fpw;                          /* fingerprints of endgame weights */
static u64 *tab[3];
static long long tabn[3], tabcap[3];

static u64 Lroot[MAXW];         /* L_0     */
static u64 Lsplit[MAXW];        /* L_SPLIT */

static unsigned long long xr(void)
{
    rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
    return rng;
}
static inline u64 addfp(u64 a, u64 b) { u64 s = a + b; return s >= FP ? s - FP : s; }
static u64 gcd64(u64 a, u64 b) { while (b) { u64 t = a % b; a = b; b = t; } return a; }

/* ------------------------------------------------------------------ setup */

static void read_problem(const char *fn)
{
    FILE *f = fopen(fn, "r");
    if (!f) { fprintf(stderr, "cannot open %s\n", fn); exit(1); }
    if (fscanf(f, "%d %d %lld %lld", &T0, &Nhi, &UNUM, &VDEN) != 4) { fprintf(stderr, "bad header\n"); exit(1); }
    if (fscanf(f, "%d", &cnt) != 1) { fprintf(stderr, "bad count\n"); exit(1); }
    if (cnt > MAXC) { fprintf(stderr, "universe too large\n"); exit(1); }
    for (int i = 0; i < cnt; i++)
        if (fscanf(f, "%d", &el[i]) != 1) { fprintf(stderr, "bad element %d\n", i); exit(1); }
    char tok[32];
    if (fscanf(f, "%31s", tok) == 1 && !strcmp(tok, "BIG")) {
        BIGMODE = 1;
        if (fscanf(f, "%8191s", BIGDEC) != 1) { fprintf(stderr, "bad BIG X0\n"); exit(1); }
        int np = 0;
        if (fscanf(f, "%d", &np) != 1) { fprintf(stderr, "bad BIG np\n"); exit(1); }
        PA_ovr_n = np;
        if (np > 4096) { fprintf(stderr, "too many overrides\n"); exit(1); }
        for (int t = 0; t < np; t++)
            if (fscanf(f, "%d %lld", &PA_ovr_p[t], &PA_ovr_t[t]) != 2) { fprintf(stderr, "bad override\n"); exit(1); }
    }
    fclose(f);
    for (int i = 0; i < cnt; i++) adj[i] = (i + 1 < cnt && el[i + 1] == el[i] + 1);
}

/* backward pass computing g_i, w_i, Tail_i, L_0, L_SPLIT and the widths. */
static void build(void)
{
    static u64 L[MAXW], Tw[MAXW], tmp[MAXW];
    bset0(Lsplit, MAXW); Lsplit[0] = 1;
    for (int pass = 0; pass < 2; pass++) {
        bset0(L, MAXW); L[0] = 1;
        bset0(Tw, MAXW);
        if (pass == 1) {
            Wv = malloc((size_t)(cnt + 1) * NW * 8);
            Tl = malloc((size_t)(cnt + 1) * NW * 8);
            Xs = malloc((size_t)(cnt + 2) * NW * 8);
            if (!Wv || !Tl || !Xs) { fprintf(stderr, "OOM\n"); exit(1); }
            bset0(Tl + (size_t)cnt * NW, NW);
            nwp[cnt] = 1;
        }
        for (int i = cnt - 1; i >= 0; i--) {
            u64 r = bmodsmall(L, MAXW, (u64)el[i]);
            u64 g = (u64)el[i] / gcd64((u64)el[i], r);
            gdiv[i] = (int)g;
            if (bmulsmall(L, MAXW, g, 0)) { fprintf(stderr, "lcm overflow: raise MAXW\n"); exit(1); }
            bdivsmall(tmp, L, MAXW, (u64)el[i]);          /* w_i = L_i/e_i   */
            bmulsmall(Tw, MAXW, g, 0);                    /* Tail_i =        */
            baddw(Tw, Tw, tmp, MAXW);                      /*  Tail_{i+1}*g+w */
            if (pass == 1) {
                if (i == SPLIT) bcpyw(Lsplit, L, MAXW);
                bcpyw(Wv + (size_t)i * NW, tmp, NW);
                bcpyw(Tl + (size_t)i * NW, Tw, NW);
                nwp[i] = bwords(Tw, NW);
                if (nwp[i] < nwp[i + 1]) nwp[i] = nwp[i + 1];
            }
        }
        if (pass == 0) { NW = bwords(Tw, MAXW); bcpyw(Lroot, L, MAXW); }
    }
}

/* --------------------------------------------------------------- endgame */

static void push(int c, u64 v)
{
    if (tabn[c] == tabcap[c]) {
        if (tabcap[c] >= tabcapmax) { fprintf(stderr, "endgame table cap hit; lower -k\n"); exit(3); }
        tabcap[c] = tabcap[c] ? tabcap[c] * 2 : 4096;
        tab[c] = realloc(tab[c], (size_t)tabcap[c] * 8);
        if (!tab[c]) { fprintf(stderr, "OOM endgame\n"); exit(1); }
    }
    tab[c][tabn[c]++] = v;
}
static void gen(int c0, int i, int s, u64 acc)
{
    if (i == cnt) { if (s != 1) push(c0, acc); return; }
    int can = 1, nst = 0;
    if (s == 0) { if (!adj[i]) can = 0; else nst = 1; }
    else nst = adj[i] ? 2 : 0;
    if (can) gen(c0, i + 1, nst, addfp(acc, fpw[i]));
    if (s != 1) gen(c0, i + 1, 0, acc);
}
static int cmpu64(const void *a, const void *b)
{
    u64 x = *(const u64 *)a, y = *(const u64 *)b;
    return x < y ? -1 : (x > y ? 1 : 0);
}
static int lookup(int c, u64 v)
{
    long long lo = 0, hi = tabn[c] - 1;
    while (lo <= hi) {
        long long m = (lo + hi) >> 1;
        if (tab[c][m] == v) return 1;
        if (tab[c][m] < v) lo = m + 1; else hi = m - 1;
    }
    return 0;
}

/* ------------------------------------------------------------------- DFS */

static void report(void)
{
    nsol++;
    if (!quiet) {
        printf("SOL");
        for (int i = 0; i < nch; i++) printf(" %d", chosen[i]);
        printf("\n");
        fflush(stdout);
    }
    if (nsol >= maxsol) {
        printf("done(cap) nodes=%lld solutions=%lld cpu=%.1fs\n",
               nodes, nsol, (double)(clock() - t_start) / CLOCKS_PER_SEC);
        exit(0);
    }
    if (randmode) stopflag = 1;
}

/* child = (X [-w]) / g, written into Xs[(i+1)*NW] using nwc words.
 * returns 1 if the child is a legal nonneg integer that fits, else 0.       */
static inline int step(int i, int take, int nw, int nwc)
{
    static u64 buf[MAXW];
    const u64 *X = Xs + (size_t)i * NW;
    u64 g = (u64)gdiv[i];
    const u64 *src;
    if (take) {
        const u64 *w = Wv + (size_t)i * NW;
        if (bcmpw(X, w, nw) < 0) return 0;
        bsubw(buf, X, w, nw);
        src = buf;
    } else src = X;
    if (g != 1) {
        if (bdivsmall(buf, src, nw, g)) return 0;
        src = buf;
    }
    for (int t = nwc; t < nw; t++) if (src[t]) return 0;
    bcpyw(Xs + (size_t)(i + 1) * NW, src, nwc);
    return 1;
}

static void dfs(int i, int s)
{
    nodes++;
    if (randmode && !inEmit && --budleft <= 0) { stopflag = 1; return; }
    if ((nodes & 0xFFFFFF) == 0 && tlimit > 0 && !randmode) {
        if ((double)(time(NULL) - wall_start) > tlimit) {
            printf("TIMEOUT nodes=%lld solutions=%lld\n", nodes, nsol);
            fflush(stdout);
            exit(2);
        }
    }
    if (!padic_ok(i)) return;
    const u64 *X = Xs + (size_t)i * NW;
    int nw = nwp[i];
    if (biszero(X, nw)) { if (s != 1) report(); return; }
    if (i == cnt) return;
    if (bcmpw(X, Tl + (size_t)i * NW, nw) > 0) return;
    if (i == SPLIT && SPLITK > 0 && !inEmit) {
        if (!lookup(s, bmodsmall(X, nw, FP))) return;
        inEmit = 1;
        dfs(i, s);
        inEmit = 0;
        return;
    }
    if (i == splitdepth && nsplitw > 1 && !inEmit) {
        if ((taskctr++ % nsplitw) != ipart) return;
    }
    int nwc = nwp[i + 1];
    int cantake = 1, nst = 0;
    if (s == 0) { if (!adj[i]) cantake = 0; else nst = 1; }
    else nst = adj[i] ? 2 : 0;
    int canskip = (s != 1);
    int first = (randmode && !inEmit) ? (int)((xr() % 100) < (unsigned)takepct) : 1;

    for (int pass = 0; pass < 2; pass++) {
        int dotake = (pass == 0) ? first : !first;
        if (dotake) {
            if (cantake && step(i, 1, nw, nwc)) {
                chosen[nch++] = el[i];
                padic_take(i);
                dfs(i + 1, nst);
                padic_untake(i);
                nch--;
            }
        } else {
            if (canskip && step(i, 0, nw, nwc)) dfs(i + 1, 0);
        }
        if (stopflag) return;
    }
}

/* ------------------------------------------------------------------ main */

int main(int argc, char **argv)
{
    if (argc < 2) {
        fprintf(stderr, "usage: esearch probfile [-k K] [-c CAP] [-m M] [-j J -i I]"
                        " [-d D] [-R seed] [-B budget] [-t secs] [-q]\n");
        return 1;
    }
    read_problem(argv[1]);
    int maxsol_set = 0;
    for (int a = 2; a < argc; a++) {
        if (!strcmp(argv[a], "-k")) SPLITK = atoi(argv[++a]);
        else if (!strcmp(argv[a], "-c")) tabcapmax = atoll(argv[++a]);
        else if (!strcmp(argv[a], "-m")) { maxsol = atoll(argv[++a]); maxsol_set = 1; }
        else if (!strcmp(argv[a], "-j")) nsplitw = atoi(argv[++a]);
        else if (!strcmp(argv[a], "-i")) ipart = atoi(argv[++a]);
        else if (!strcmp(argv[a], "-d")) splitdepth = atoi(argv[++a]);
        else if (!strcmp(argv[a], "-R")) { randmode = 1;
            rng = (unsigned long long)atoll(argv[++a]) * 2862933555777941757ULL + 3037000493ULL; }
        else if (!strcmp(argv[a], "-B")) budget = atoll(argv[++a]);
        else if (!strcmp(argv[a], "-p")) takepct = atoi(argv[++a]);
        else if (!strcmp(argv[a], "-t")) tlimit = atof(argv[++a]);
        else if (!strcmp(argv[a], "-q")) quiet = 1;
        else { fprintf(stderr, "unknown option %s\n", argv[a]); return 1; }
    }
    if (budget == 0) budget = 30000000LL;
    if (randmode && !maxsol_set) maxsol = 1;
    if (SPLITK > cnt) SPLITK = cnt;
    SPLIT = cnt - SPLITK;
    t_start = clock(); wall_start = time(NULL);

    if (cnt == 0) {
        printf("T=%d N=%d target=%lld/%lld |A|=0 (empty universe)\n", T0, Nhi, UNUM, VDEN);
        printf("done nodes=0 solutions=0 cpu=0.0s\n");
        return 0;
    }
    build();
    if (padic_init(cnt, el, Nhi, UNUM, VDEN, 0) < 0) {
        printf("target denominator unreachable: NO SOLUTION\ndone nodes=0 solutions=0 cpu=0.0s\n");
        return 0;
    }

    printf("T=%d N=%d target=%lld/%lld |A|=%d  lcm bits=%d  words=%d\n",
           T0, Nhi, UNUM, VDEN, cnt, bbits(Lroot, MAXW), NW);
    fflush(stdout);

    static u64 X0[MAXW];
    if (BIGMODE) {
        bset0(X0, MAXW);
        for (const char *cp = BIGDEC; *cp; cp++) {
            if (*cp < '0' || *cp > '9') { fprintf(stderr, "bad decimal\n"); return 1; }
            if (bmulsmall(X0, MAXW, 10ULL, (u64)(*cp - '0'))) { fprintf(stderr, "X0 overflow\n"); return 1; }
        }
    } else {
    if (bdivsmall(X0, Lroot, MAXW, (u64)VDEN)) {
        printf("v does not divide lcm(A): NO SOLUTION\ndone nodes=0 solutions=0 cpu=0.0s\n");
        return 0;
    }
    if (bmulsmall(X0, MAXW, (u64)UNUM, 0)) { fprintf(stderr, "target overflow\n"); return 1; }
    }
    if (bcmpw(X0, Tl, nwp[0]) > 0) {
        printf("target exceeds total universe sum: NO SOLUTION\ndone nodes=0 solutions=0 cpu=0.0s\n");
        return 0;
    }
    bcpyw(Xs, X0, NW);

    if (SPLITK > 0) {
        fpw = malloc((size_t)cnt * 8);
        static u64 tmp[MAXW];
        for (int i = SPLIT; i < cnt; i++) {
            bdivsmall(tmp, Lsplit, MAXW, (u64)el[i]);
            fpw[i] = bmodsmall(tmp, MAXW, FP);
        }
        for (int c = 0; c < 3; c++) {
            tabn[c] = tabcap[c] = 0; tab[c] = NULL;
            gen(c, SPLIT, c, 0);
            qsort(tab[c], tabn[c], 8, cmpu64);
            long long m = 0;
            for (long long t = 0; t < tabn[c]; t++)
                if (t == 0 || tab[c][t] != tab[c][t - 1]) tab[c][m++] = tab[c][t];
            tabn[c] = m;
        }
        printf("  endgame at index %d (element %d): distinct sums %lld %lld %lld  (%.1fs)\n",
               SPLIT, el[SPLIT], tabn[0], tabn[1], tabn[2],
               (double)(clock() - t_start) / CLOCKS_PER_SEC);
        fflush(stdout);
    }

    if (!randmode) {
        dfs(0, 0);
        printf("done nodes=%lld solutions=%lld cpu=%.1fs\n",
               nodes, nsol, (double)(clock() - t_start) / CLOCKS_PER_SEC);
    } else {
        long long restarts = 0;
        for (;;) {
            stopflag = 0; budleft = budget; nch = 0; padic_reset();
            bcpyw(Xs, X0, NW);
            restarts++;
            dfs(0, 0);
            if (nsol > 0) break;
            if (tlimit > 0 && (double)(time(NULL) - wall_start) > tlimit) {
                printf("RESTART-TIMEOUT restarts=%lld nodes=%lld cpu=%.1fs\n",
                       restarts, nodes, (double)(clock() - t_start) / CLOCKS_PER_SEC);
                return 2;
            }
        }
        printf("done(random) restarts=%lld nodes=%lld solutions=%lld cpu=%.1fs\n",
               restarts, nodes, nsol, (double)(clock() - t_start) / CLOCKS_PER_SEC);
    }
    return 0;
}
