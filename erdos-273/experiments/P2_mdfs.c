/* P2_mdfs.c -- EXHAUSTIVE decision of the pivot on one lattice L, modulus-ordered DFS.
 *
 * Decide: is there a covering of Z/L by classes b (mod m), m in S(L) = {m | L : m >= MINM,
 * 2m+1 prime}, each m used at most once?   MINM = 3 bans the modulus 2 (THE PIVOT).
 *
 * SEARCH: process the moduli in INCREASING order m_1 < m_2 < ... < m_n.  For each in turn either
 * SKIP it or give it a class b (mod m_i).  Complete by construction.
 *
 * PRUNE (density / budget): after step i, let u = #uncovered residues of Z/L and
 * R_i = sum_{k > i} L/m_k the total coverage still purchasable.  Then u <= R_i is necessary.
 * With budget only ~1.2 this bites hard: every overlap between two used classes is charged
 * against the slack sum_{m in S} L/m - L.
 *
 * PRUNE (dominance): a class b for m_i that covers NO new residue is dominated by SKIP; drop it.
 *
 * SYMMETRY (exact, sound): translations x -> x + t map coverings to coverings and preserve the
 * pool.  Let g = lcm of the moduli USED so far.  Translations by multiples of g fix all classes
 * already placed, and shift b_{m_i} by the subgroup gcd(g, m_i) Z / m_i.  Hence WLOG
 *          b_{m_i}  in  [0, gcd(g, m_i))     whenever m_i is used.
 * Applied inductively along the fixed order this is a valid orbit normalisation: any covering
 * has a translate satisfying every one of these constraints.  (g = 1 at the start, so the first
 * used modulus always gets b = 0.)
 *
 * usage: ./P2_mdfs L [--minm M] [--nodes N] [--all]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef unsigned long long u64;
typedef long long ll;

static long L, NW, MINM = 3;
static int NOSYM = 0, NODOM = 0;
static long S[256]; static int ns;
static ll  RS[257];              /* RS[i] = sum_{k >= i} L/S[k]  */
static u64 *cov;
static int chosen_b[256];        /* -1 = skipped */
static ll nodes, NODECAP;
static int capped;
static int sol_b[256];

static long gcdl(long a, long b){ while(b){ long t=a%b; a=b; b=t; } return a; }

static int dfs(int i, long u, long g)
{
    if (++nodes > NODECAP) { capped = 1; return 0; }
    if (u == 0) { for (int k = 0; k < ns; k++) sol_b[k] = chosen_b[k]; return 1; }
    if (i == ns) return 0;
    if (u > RS[i]) return 0;                          /* density prune */
    u64 *c  = cov + (ll)i * NW;
    u64 *nc = cov + (ll)(i+1) * NW;
    long m = S[i];
    long lim = NOSYM ? m : gcdl(g, m);                /* symmetry-normalised range for b */
    for (long b = 0; b < lim; b++) {
        long gained = 0;
        memcpy(nc, c, sizeof(u64)*NW);
        for (long t = b; t < L; t += m) {
            u64 msk = 1ULL << (t & 63);
            if (!(nc[t>>6] & msk)) { nc[t>>6] |= msk; gained++; }
        }
        if (gained == 0 && !NODOM) continue;          /* dominated by SKIP */
        chosen_b[i] = (int)b;
        long ng = (g / gcdl(g, m)) * m;               /* lcm(g, m) */
        if (dfs(i+1, u - gained, ng)) return 1;
        if (capped) return 0;
    }
    chosen_b[i] = -1;                                 /* SKIP */
    memcpy(nc, c, sizeof(u64)*NW);
    return dfs(i+1, u, g);
}

int main(int argc, char **argv)
{
    setbuf(stdout, NULL);
    if (argc < 2) { printf("usage: P2_mdfs L [--minm M] [--nodes N]\n"); return 1; }
    L = atol(argv[1]); NODECAP = 400000000000LL;
    for (int i = 2; i < argc; i++) {
        if (!strcmp(argv[i],"--nodes") && i+1 < argc) NODECAP = atoll(argv[++i]);
        if (!strcmp(argv[i],"--minm")  && i+1 < argc) MINM   = atol(argv[++i]);
        if (!strcmp(argv[i],"--nosym")) NOSYM = 1;
        if (!strcmp(argv[i],"--nodom")) NODOM = 1;
    }
    long lim = 2*L + 2;
    unsigned char *isp = malloc(lim+1); memset(isp,1,lim+1); isp[0]=isp[1]=0;
    for (long i = 2; i*i <= lim; i++) if (isp[i]) for (long j=i*i;j<=lim;j+=i) isp[j]=0;
    ns = 0;
    for (long d = 1; d <= L; d++) if (L % d == 0 && d >= MINM && isp[2*d+1]) S[ns++] = d;
    RS[ns] = 0; for (int i = ns-1; i >= 0; i--) RS[i] = RS[i+1] + L/S[i];
    NW = (L + 63)/64;
    printf("# P2_mdfs L = %ld  minm = %ld  |S| = %d  budget = %lld/%ld = %.6f\n",
           L, MINM, ns, RS[0], L, (double)RS[0]/L);
    printf("# pool:"); for (int i=0;i<ns;i++) printf(" %ld", S[i]); printf("\n");
    if (RS[0] <= L) { printf("UNSAT (budget <= 1)\n"); return 0; }
    cov = calloc((size_t)(ns+2)*NW, sizeof(u64));
    /* mark the padding bits of the last word as covered so u counts only real residues */
    long pad = NW*64 - L;
    if (pad) cov[NW-1] |= (~0ULL) << (64 - pad);
    int found = dfs(0, L, 1);
    if (found) {
        printf("SAT :");
        for (int i = 0; i < ns; i++) if (sol_b[i] >= 0) printf(" %d(mod %ld)", sol_b[i], S[i]);
        printf("\nnodes = %lld\n", nodes);
    } else if (capped) {
        printf("CAP  node limit %lld reached -- UNDECIDED\n", NODECAP);
    } else {
        printf("UNSAT  exhaustive: Z/%ld admits no covering by distinct moduli from "
               "{m | %ld : m >= %ld, 2m+1 prime}.  nodes = %lld\n", L, L, MINM, nodes);
        printf("# SCOPE: rules out pivot coverings with lcm dividing %ld ONLY -- H\\{2} is "
               "infinite, so this is a lattice lemma, not a proof of the pivot.\n", L);
    }
    return 0;
}
