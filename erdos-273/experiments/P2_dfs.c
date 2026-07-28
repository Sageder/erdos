/* P2_dfs.c -- EXHAUSTIVE, INDEPENDENT decision of the pivot on one lattice L.
 *
 * Question: is there a covering of Z/L by classes b (mod m), m ranging over
 *      S(L) = { m | L : m >= 3, 2m+1 prime }        (each m used at most once)
 * i.e. a covering system of Z with distinct moduli in H\{2} = {m>=3 : 2m+1 prime}, lcm | L.
 *
 * METHOD (no SAT, no external library -- an independent second opinion):
 *   canonical DFS on the SMALLEST UNCOVERED RESIDUE r.  Any covering must cover r, so branch
 *   over which unused modulus m covers it; the class is then forced to be b = r mod m.
 *
 * COMPLETENESS + REDUNDANCY ELIMINATION ("branch and exclude"):
 *   at a node with smallest uncovered residue r we try the unused moduli m_1 < m_2 < ... in turn.
 *   After branch i fails, EVERY covering extending the current partial assignment has
 *   b_{m_i} != r (mod m_i); so we add that as a permanent no-good for the whole remainder of this
 *   node's subtree (undone on backtrack).  This is sound (branch i explored exactly the coverings
 *   in which m_i covers r) and removes the huge redundancy of reaching the same covering by
 *   different orders.
 *
 * PRUNES:
 *   (1) coverage: #uncovered  <=  sum over unused m of L/m .
 *   (2) local: the moduli still allowed to cover r must exist, and their total coverage must
 *       reach the uncovered count.
 *
 * exit: prints SAT with the certificate, or UNSAT (exhaustive), or CAP (node limit hit).
 * usage: ./P2_dfs L [--nodes N]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef unsigned long long u64;
typedef long long ll;

static long L, NW;
static long S[256]; static int ns;
static u64 *cov;
static unsigned char *forb[256];     /* forb[i][b] = 1  =>  modulus S[i] may not take class b */
static int used[256];
static int chosen_m[256], chosen_b[256];
static ll nodes, NODECAP; static long MINM = 3;
static int capped;
static int sol_m[256], sol_b[256], sol_len;

static long uncovered_count(u64 *c)
{
    long u = 0;
    for (long w = 0; w < NW; w++) u += __builtin_popcountll(~c[w]);
    return u - (NW*64 - L);
}

static long first_uncovered(u64 *c)
{
    for (long w = 0; w < NW; w++) {
        u64 x = ~c[w];
        if (w == NW-1) { long pad = NW*64 - L; if (pad) x &= (~0ULL) >> pad; }
        if (x) return w*64 + __builtin_ctzll(x);
    }
    return -1;
}

static int dfs(int d, ll rem_cover)
{
    if (++nodes > NODECAP) { capped = 1; return 0; }
    u64 *c = cov + (ll)d * NW;
    long r = first_uncovered(c);
    if (r < 0) { sol_len = d;
                 for (int i = 0; i < d; i++) { sol_m[i] = chosen_m[i]; sol_b[i] = chosen_b[i]; }
                 return 1; }
    long u = uncovered_count(c);
    if (rem_cover < u) return 0;                     /* prune (1) */
    u64 *nc = cov + (ll)(d+1) * NW;
    int marked[256], nmark = 0;
    for (int i = 0; i < ns; i++) {
        if (used[i]) continue;
        long m = S[i], b = r % m;
        if (forb[i][b]) continue;
        memcpy(nc, c, sizeof(u64)*NW);
        for (long t = b; t < L; t += m) nc[t>>6] |= 1ULL << (t & 63);
        used[i] = 1; chosen_m[d] = (int)m; chosen_b[d] = (int)b;
        int ok = dfs(d+1, rem_cover - L/m);
        used[i] = 0;
        if (ok) { for (int k = 0; k < nmark; k++) forb[marked[k]][r % S[marked[k]]] = 0; return 1; }
        if (capped) { for (int k = 0; k < nmark; k++) forb[marked[k]][r % S[marked[k]]] = 0; return 0; }
        forb[i][b] = 1; marked[nmark++] = i;         /* no-good: m_i does not cover r */
    }
    for (int k = 0; k < nmark; k++) forb[marked[k]][r % S[marked[k]]] = 0;
    return 0;
}

int main(int argc, char **argv)
{
    setbuf(stdout, NULL);
    if (argc < 2) { printf("usage: P2_dfs L [--nodes N]\n"); return 1; }
    L = atol(argv[1]); NODECAP = 200000000000LL;
    for (int i = 2; i < argc; i++) { if (!strcmp(argv[i],"--nodes") && i+1 < argc) NODECAP = atoll(argv[++i]); if (!strcmp(argv[i],"--minm") && i+1 < argc) MINM = atol(argv[++i]); }
    long lim = 2*L + 2;
    unsigned char *isp = malloc(lim+1); memset(isp,1,lim+1); isp[0]=isp[1]=0;
    for (long i = 2; i*i <= lim; i++) if (isp[i]) for (long j=i*i;j<=lim;j+=i) isp[j]=0;
    ns = 0; ll rem = 0;
    for (long d = 1; d <= L; d++) if (L % d == 0 && d >= MINM && isp[2*d+1]) { S[ns++] = d; rem += L/d; }
    for (int i = 1; i < ns; i++) for (int k = i; k > 0 && S[k] < S[k-1]; k--) { long t=S[k];S[k]=S[k-1];S[k-1]=t; }
    NW = (L + 63)/64;
    printf("# P2_dfs  L = %ld  |S| = %d  scaled budget = %lld / %ld = %.6f\n", L, ns, rem, L, (double)rem/L);
    printf("# pool:"); for (int i=0;i<ns;i++) printf(" %ld", S[i]); printf("\n");
    if (rem <= L) { printf("UNSAT (budget <= 1)\n"); return 0; }
    cov = calloc((size_t)(ns+2)*NW, sizeof(u64));
    for (int i = 0; i < ns; i++) forb[i] = calloc(S[i], 1);
    int found = dfs(0, rem);
    if (found) {
        printf("SAT  %d classes:", sol_len);
        for (int i = 0; i < sol_len; i++) printf(" %d(mod %d)", sol_b[i], sol_m[i]);
        printf("\nnodes = %lld\n", nodes);
    } else if (capped) {
        printf("CAP  node limit %lld reached -- UNDECIDED\n", NODECAP);
    } else {
        printf("UNSAT  exhaustive: no covering of Z/%ld from H\\{2} divisors.  nodes = %lld\n", L, nodes);
        printf("# SCOPE: this rules out pivot coverings with lcm dividing %ld ONLY.\n", L);
    }
    return 0;
}
