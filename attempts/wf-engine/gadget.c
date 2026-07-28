/* gadget.c -- EXACT arbitrary-precision search for legal block systems in a
 * window [T,N] whose reciprocal sum has DENOMINATOR DIVIDING D and lies in a
 * prescribed value window [lo,hi].  ("gadget mode")
 *
 * Why: hitting one exact rational far out is a needle; hitting ANY rational of
 * the form a/D is a haystack of D targets at once.  Gadgets from pairwise
 * disjoint windows can then be glued (their union is legal, and the values add
 * as ordinary integers a_1+...+a_m = D over the common denominator D), which
 * turns "represent 1 far out" into an easy integer subset-sum.
 *
 * ARITHMETIC.  Same rescaling idea as esearch.c, but ACCUMULATING instead of
 * subtracting.  With A = {e_0<...<e_{cnt-1}} and
 *      K_i = lcm( D, e_i, e_{i+1}, ..., e_{cnt-1} ),      K_cnt = D,
 * a partial sum P_i = sum over chosen indices < i must satisfy den(P_i) | K_i
 * (because the final value has denominator | D and the remaining elements
 * contribute denominators | lcm(e_j, j>=i)).  The engine carries the exact
 * integer  Z_i := P_i * K_i.  With V_i := K_i/e_i and h_i := K_i/K_{i+1},
 *      Z_{i+1} = ( Z_i + [take] * V_i ) / h_i,
 * and exact divisibility by h_i IS the p-adic prune.  h_i divides e_i <= N, so
 * it always fits in a machine word.  At the end K_cnt = D and Z_cnt = a is the
 * numerator of the gadget value a/D.
 *
 * PRUNES.  With Tail'_i = (sum_{j>=i} 1/e_j) * K_i (exact),
 *      Z_i <= floor(hi*K_i)                       (cannot overshoot hi)
 *      Z_i >= ceil(lo*K_i) - Tail'_i              (cannot still reach lo)
 *      h_i | (Z_i + [take]*V_i)                   (p-adic)
 * plus the Rule-(P) gadget fixpoint applied offline by prune.py -D.
 *
 * problem file:  line 1 "T N u D"  (u ignored), line 2 cnt, line 3 the elements
 * usage: ./gadget probfile [-lo a/b] [-hi a/b] [-R seed] [-B budget] [-t secs]
 *                          [-m maxsol] [-q]
 * output: "G <a> <D> <n1> <n2> ..."   meaning sum 1/n_i = a/D exactly.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>
#include "bigint.h"
#include "padic.h"

#define MAXW 220
#define MAXC 20000

static int T0, Nhi, cnt;
static long long DDEN = 1, dummyU = 1;
static int el[MAXC], adj[MAXC];
static int hdiv[MAXC];
static int nwp[MAXC + 1];
static int NWG;
static u64 *Vv, *HiB, *LoB, *Zs;

static long long nodes = 0, nsol = 0, maxsol = (1LL << 60);
static int chosen[MAXC], nch = 0;
static int quiet = 0, randmode = 0, stopflag = 0, takepct = 50;
static long long budget = 30000000LL, budleft = 0;
static unsigned long long rng = 0x9E3779B97F4A7C15ULL;
static double tlimit = 0;
static time_t wall_start;
static clock_t t_start;
static long long LON = 0, LOD = 1, HIN = 1, HID = 1;   /* lo = LON/LOD etc. */

static unsigned long long xr(void)
{ rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17; return rng; }
static u64 gcd64(u64 a, u64 b) { while (b) { u64 t = a % b; a = b; b = t; } return a; }

static void read_problem(const char *fn)
{
    FILE *f = fopen(fn, "r");
    if (!f) { fprintf(stderr, "cannot open %s\n", fn); exit(1); }
    if (fscanf(f, "%d %d %lld %lld", &T0, &Nhi, &dummyU, &DDEN) != 4) { fprintf(stderr, "bad header\n"); exit(1); }
    if (fscanf(f, "%d", &cnt) != 1) { fprintf(stderr, "bad count\n"); exit(1); }
    if (cnt > MAXC) { fprintf(stderr, "universe too large\n"); exit(1); }
    for (int i = 0; i < cnt; i++)
        if (fscanf(f, "%d", &el[i]) != 1) { fprintf(stderr, "bad element\n"); exit(1); }
    fclose(f);
    for (int i = 0; i < cnt; i++) adj[i] = (i + 1 < cnt && el[i + 1] == el[i] + 1);
}

static u64 Kroot[MAXW];

static void build(void)
{
    static u64 K[MAXW], Tw[MAXW], tmp[MAXW], hb[MAXW], lb[MAXW];
    for (int pass = 0; pass < 2; pass++) {
        bset0(K, MAXW); K[0] = (u64)DDEN;
        bset0(Tw, MAXW);
        if (pass == 1) {
            Vv  = malloc((size_t)(cnt + 1) * NWG * 8);
            HiB = malloc((size_t)(cnt + 1) * NWG * 8);
            LoB = malloc((size_t)(cnt + 1) * NWG * 8);
            Zs  = malloc((size_t)(cnt + 2) * NWG * 8);
            if (!Vv || !HiB || !LoB || !Zs) { fprintf(stderr, "OOM\n"); exit(1); }
        }
        /* terminal level i = cnt : K = D, Tail' = 0 */
        for (int i = cnt; i >= 0; i--) {
            if (i < cnt) {
                u64 r = bmodsmall(K, MAXW, (u64)el[i]);
                u64 h = (u64)el[i] / gcd64((u64)el[i], r);
                hdiv[i] = (int)h;
                if (bmulsmall(K, MAXW, h, 0)) { fprintf(stderr, "K overflow: raise MAXW\n"); exit(1); }
                bdivsmall(tmp, K, MAXW, (u64)el[i]);      /* V_i = K_i/e_i */
                bmulsmall(Tw, MAXW, h, 0);
                baddw(Tw, Tw, tmp, MAXW);                 /* Tail'_i       */
            } else {
                bset0(tmp, MAXW);
            }
            /* HiB = floor(hi*K), LoB = max(0, ceil(lo*K) - Tail') */
            bcpyw(hb, K, MAXW);
            if (bmulsmall(hb, MAXW, (u64)HIN, 0)) { fprintf(stderr, "hi overflow\n"); exit(1); }
            bdivsmall(hb, hb, MAXW, (u64)HID);
            bcpyw(lb, K, MAXW);
            if (bmulsmall(lb, MAXW, (u64)LON, (u64)LOD - 1)) { fprintf(stderr, "lo overflow\n"); exit(1); }
            bdivsmall(lb, lb, MAXW, (u64)LOD);
            if (bcmpw(lb, Tw, MAXW) <= 0) bset0(lb, MAXW); else bsubw(lb, lb, Tw, MAXW);
            if (pass == 0) {
                int q = bwords(hb, MAXW) + 1;
                if (q > NWG) NWG = q;
                if (i == 0) bcpyw(Kroot, K, MAXW);
            } else {
                nwp[i] = bwords(hb, NWG) + 1;
                if (nwp[i] > NWG) nwp[i] = NWG;
                if (i < cnt && nwp[i] < nwp[i + 1]) nwp[i] = nwp[i + 1];
                bcpyw(HiB + (size_t)i * NWG, hb, NWG);
                bcpyw(LoB + (size_t)i * NWG, lb, NWG);
                if (i < cnt) bcpyw(Vv + (size_t)i * NWG, tmp, NWG);
            }
        }
        if (pass == 0 && NWG > MAXW) { fprintf(stderr, "NWG > MAXW\n"); exit(1); }
    }
}

static void report(int i)
{
    nsol++;
    if (!quiet) {
        printf("G ");
        bprint(Zs + (size_t)i * NWG, nwp[i]);
        printf(" %lld", DDEN);
        for (int t = 0; t < nch; t++) printf(" %d", chosen[t]);
        printf("\n");
        fflush(stdout);
    }
    if (nsol >= maxsol) {
        printf("done(cap) nodes=%lld gadgets=%lld cpu=%.1fs\n",
               nodes, nsol, (double)(clock() - t_start) / CLOCKS_PER_SEC);
        exit(0);
    }
}

static inline int step(int i, int take, int nw, int nwc)
{
    static u64 buf[MAXW];
    const u64 *Z = Zs + (size_t)i * NWG;
    u64 h = (u64)hdiv[i];
    const u64 *src;
    if (take) { baddw(buf, Z, Vv + (size_t)i * NWG, nw); src = buf; }
    else src = Z;
    if (h != 1) { if (bdivsmall(buf, src, nw, h)) return 0; src = buf; }
    for (int t = nwc; t < nw; t++) if (src[t]) return 0;
    bcpyw(Zs + (size_t)(i + 1) * NWG, src, nwc);
    return 1;
}

static void dfs(int i, int s)
{
    nodes++;
    if (randmode && --budleft <= 0) { stopflag = 1; return; }
    if ((nodes & 0xFFFFFF) == 0 && tlimit > 0 && !randmode) {
        if ((double)(time(NULL) - wall_start) > tlimit) {
            printf("TIMEOUT nodes=%lld gadgets=%lld\n", nodes, nsol); fflush(stdout); exit(2);
        }
    }
    if (!padic_ok(i)) return;
    const u64 *Z = Zs + (size_t)i * NWG;
    int nw = nwp[i];
    if (bcmpw(Z, HiB + (size_t)i * NWG, nw) > 0) return;
    if (bcmpw(Z, LoB + (size_t)i * NWG, nw) < 0) return;
    if (i == cnt) { if (s != 1 && !biszero(Z, nw)) report(i); return; }
    int nwc = nwp[i + 1];
    int cantake = 1, nst = 0;
    if (s == 0) { if (!adj[i]) cantake = 0; else nst = 1; }
    else nst = adj[i] ? 2 : 0;
    int canskip = (s != 1);
    int first = randmode ? (int)((xr() % 100) < (unsigned)takepct) : 1;
    for (int pass = 0; pass < 2; pass++) {
        int dotake = (pass == 0) ? first : !first;
        if (dotake) {
            if (cantake && step(i, 1, nw, nwc)) { chosen[nch++] = el[i]; padic_take(i); dfs(i + 1, nst); padic_untake(i); nch--; }
        } else {
            if (canskip && step(i, 0, nw, nwc)) dfs(i + 1, 0);
        }
        if (stopflag) return;
    }
}

static void parse_rat(const char *s, long long *n, long long *d)
{
    const char *sl = strchr(s, '/');
    if (sl) { *n = atoll(s); *d = atoll(sl + 1); }
    else { *n = atoll(s); *d = 1; }
}

int main(int argc, char **argv)
{
    if (argc < 2) { fprintf(stderr, "usage: gadget probfile [-lo a/b] [-hi a/b] [-R seed] [-B budget] [-t secs] [-m M] [-q]\n"); return 1; }
    read_problem(argv[1]);
    for (int a = 2; a < argc; a++) {
        if (!strcmp(argv[a], "-lo")) parse_rat(argv[++a], &LON, &LOD);
        else if (!strcmp(argv[a], "-hi")) parse_rat(argv[++a], &HIN, &HID);
        else if (!strcmp(argv[a], "-R")) { randmode = 1; rng = (unsigned long long)atoll(argv[++a]) * 6364136223846793005ULL + 1442695040888963407ULL; }
        else if (!strcmp(argv[a], "-B")) budget = atoll(argv[++a]);
        else if (!strcmp(argv[a], "-p")) takepct = atoi(argv[++a]);
        else if (!strcmp(argv[a], "-t")) tlimit = atof(argv[++a]);
        else if (!strcmp(argv[a], "-m")) maxsol = atoll(argv[++a]);
        else if (!strcmp(argv[a], "-q")) quiet = 1;
        else { fprintf(stderr, "unknown option %s\n", argv[a]); return 1; }
    }
    t_start = clock(); wall_start = time(NULL);
    if (cnt == 0) { printf("empty universe\ndone nodes=0 gadgets=0\n"); return 0; }
    build();
    padic_init(cnt, el, Nhi, 1, DDEN, 1);
    printf("T=%d N=%d D=%lld |A|=%d lcm(D,A) bits=%d words=%d  value window [%lld/%lld,%lld/%lld]\n",
           T0, Nhi, DDEN, cnt, bbits(Kroot, MAXW), NWG, LON, LOD, HIN, HID);
    fflush(stdout);
    bset0(Zs, NWG);
    if (!randmode) {
        dfs(0, 0);
        printf("done nodes=%lld gadgets=%lld cpu=%.1fs\n",
               nodes, nsol, (double)(clock() - t_start) / CLOCKS_PER_SEC);
    } else {
        long long restarts = 0;
        for (;;) {
            stopflag = 0; budleft = budget; nch = 0; padic_reset(); bset0(Zs, NWG);
            restarts++;
            dfs(0, 0);
            if (tlimit > 0 && (double)(time(NULL) - wall_start) > tlimit) break;
        }
        printf("done(random) restarts=%lld nodes=%lld gadgets=%lld cpu=%.1fs\n",
               restarts, nodes, nsol, (double)(clock() - t_start) / CLOCKS_PER_SEC);
    }
    return 0;
}
