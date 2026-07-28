/* s6_target.c -- exhaustive search for a legal U subset [A,N] with
 *                sum_{n in U} 1/n = T   (T given exactly, as T*L where L=lcm(universe))
 *
 * Input file format (produced by mkuniverse2.py):
 *      N A
 *      L        (decimal, fits in u128)
 *      R0       (decimal = T*L, fits in u128)
 *      n1 n2 n3 ...          (the sieved universe)
 *
 * usage:  ./s6_target file [maxsol]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef unsigned __int128 u128;

static int N, A;
static int allowed[8192];
static u128 L, R0, w[8192], tail[8194], Q[8194];
static long long nodes = 0, nsol = 0, maxsol = 1000000000LL;
static int chosen[8192], nch = 0;

static void print_u128(u128 x) {
    char buf[64]; int i = 63; buf[i--] = 0;
    if (!x) { printf("0"); return; }
    while (x) { buf[i--] = (char)('0' + (int)(x % 10)); x /= 10; }
    printf("%s", buf + i + 1);
}
static u128 parse_u128(const char *s) {
    u128 v = 0;
    while (*s >= '0' && *s <= '9') { v = v * 10 + (u128)(*s - '0'); s++; }
    return v;
}
static int nu(long long n, int p) { int e = 0; while (n % p == 0) { n /= p; e++; } return e; }

static void emit(void) {
    nsol++;
    if (nsol > maxsol) { printf("done nodes=%lld solutions=%lld (CAPPED)\n", nodes, nsol); exit(0); }
    printf("SOLUTION:");
    for (int i = 0; i < nch; i++) printf(" %d", chosen[i]);
    printf("\n"); fflush(stdout);
}

static void dfs(int pos, u128 R, int runlen) {
    nodes++;
    if (R == 0) { if (runlen != 1) emit(); return; }
    if (pos > N) return;
    if (R > tail[pos]) return;
    if (R % Q[pos]) return;
    if (allowed[pos] && w[pos] <= R) {
        chosen[nch++] = pos;
        dfs(pos + 1, R - w[pos], runlen + 1);
        nch--;
    } else if (runlen == 1) return;
    if (runlen != 1) dfs(pos + 1, R, 0);
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: %s file [maxsol]\n", argv[0]); return 1; }
    if (argc > 2) maxsol = atoll(argv[2]);
    FILE *f = fopen(argv[1], "r");
    if (!f) { perror("open"); return 1; }
    char buf[4096];
    if (fscanf(f, "%d %d", &N, &A) != 2) return 1;
    if (fscanf(f, "%4095s", buf) != 1) return 1; L = parse_u128(buf);
    if (fscanf(f, "%4095s", buf) != 1) return 1; R0 = parse_u128(buf);
    memset(allowed, 0, sizeof(allowed));
    int n, cnt = 0;
    while (fscanf(f, "%d", &n) == 1) { allowed[n] = 1; cnt++; }
    fclose(f);
    if (cnt == 0) { printf("empty universe -> NO SOLUTION\n"); return 0; }

    for (n = A; n <= N; n++) w[n] = allowed[n] ? L / (u128)n : (u128)0;
    tail[N + 1] = 0;
    for (n = N; n >= A; n--) tail[n] = tail[n + 1] + w[n];

    int primes[8192], np = 0;
    for (int i = 2; i <= N; i++) {
        int isp = 1;
        for (int j = 2; (long long)j * j <= i; j++) if (i % j == 0) { isp = 0; break; }
        if (isp) primes[np++] = i;
    }
    int nuL[8192];
    for (int pi = 0; pi < np; pi++) {
        int p = primes[pi]; int e = 0; u128 t = L;
        while (t % (u128)p == 0) { t /= (u128)p; e++; }
        nuL[pi] = e;
    }
    int maxe[8192];
    for (int pi = 0; pi < np; pi++) maxe[pi] = 0;
    Q[N + 1] = L;
    for (n = N; n >= A; n--) {
        if (allowed[n]) {
            for (int pi = 0; pi < np; pi++) {
                int p = primes[pi];
                if (n % p) continue;
                int e = nu(n, p);
                if (e > maxe[pi]) maxe[pi] = e;
            }
        }
        u128 q = 1;
        for (int pi = 0; pi < np; pi++) {
            int d = nuL[pi] - maxe[pi];
            for (int k = 0; k < d; k++) q *= (u128)primes[pi];
        }
        Q[n] = q;
    }
    printf("N=%d A=%d universe=%d L=", N, A, cnt); print_u128(L);
    printf(" R0="); print_u128(R0); printf("\n"); fflush(stdout);
    if (R0 > tail[A]) { printf("target exceeds tail -> NO SOLUTION\n"); return 0; }
    dfs(A, R0, 0);
    printf("done nodes=%lld solutions=%lld\n", nodes, nsol);
    return 0;
}
