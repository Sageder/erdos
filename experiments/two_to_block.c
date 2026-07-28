/* two_to_block.c -- for each target rational p/q given on the command line,
 * decide whether p/q = H(c,d) = sum_{n=c}^{d} 1/n for some block with c >= CMIN.
 *
 * WHY: if n1, n2 are elements of a solution that can be deleted while keeping it
 * legal, and 1/n1 + 1/n2 = H(c,d) with c above everything used so far, then
 * deleting n1, n2 and inserting the block [c,d] gives another solution with ONE
 * MORE block and a much larger capacity (the block is long).  Iterating that move
 * drives the block count to infinity.
 *
 * Method: for each c we binary-search the unique candidate d using long double
 * prefix sums, then confirm with two independent 62-bit modular fingerprints of
 * the exact rational.  Fingerprint equality is necessary for true equality, so
 * there are no false negatives; hits are re-verified exactly in Python.
 *
 * usage: ./two_to_block CMIN CMAX  p1 q1 p2 q2 ...
 */
#include <stdio.h>
#include <stdlib.h>

typedef unsigned long long u64;
typedef __uint128_t u128;
static const u64 P1 = 4611686018427387847ULL, P2 = 4611686018427388039ULL;
static u64 mulmod(u64 a, u64 b, u64 m) { return (u64)((u128)a * b % m); }
static u64 powmod(u64 a, u64 e, u64 m) { u64 r = 1; a %= m; while (e) { if (e & 1) r = mulmod(r, a, m); a = mulmod(a, a, m); e >>= 1; } return r; }
static u64 inv(u64 a, u64 m) { return powmod(a % m, m - 2, m); }

int main(int argc, char **argv) {
    long long CMIN = atoll(argv[1]), CMAX = atoll(argv[2]);
    int nt = (argc - 3) / 2;
    long long *pp = malloc(nt * sizeof(long long)), *qq = malloc(nt * sizeof(long long));
    for (int i = 0; i < nt; i++) { pp[i] = atoll(argv[3 + 2 * i]); qq[i] = atoll(argv[4 + 2 * i]); }

    long long M = CMAX + 2;
    long double *S = malloc(M * sizeof(long double));
    u64 *F1 = malloc(M * sizeof(u64)), *F2 = malloc(M * sizeof(u64));
    S[1] = 0; F1[1] = F2[1] = 0;
    for (long long n = 2; n < M; n++) {
        S[n] = S[n - 1] + 1.0L / (long double)n;
        F1[n] = (F1[n - 1] + inv(n, P1)) % P1;
        F2[n] = (F2[n - 1] + inv(n, P2)) % P2;
    }
    long long hits = 0;
    for (int i = 0; i < nt; i++) {
        long double tgt = (long double)pp[i] / (long double)qq[i];
        u64 t1 = mulmod(pp[i] % P1, inv(qq[i], P1), P1);
        u64 t2 = mulmod(pp[i] % P2, inv(qq[i], P2), P2);
        for (long long c = CMIN; c + 1 < M; c++) {
            /* smallest d >= c+1 with S[d]-S[c-1] >= tgt */
            long long lo = c + 1, hi = M - 1, d = -1;
            if (S[hi] - S[c - 1] < tgt) break;      /* range exhausted for this c */
            while (lo <= hi) { long long mid = (lo + hi) / 2;
                if (S[mid] - S[c - 1] >= tgt - 1e-17L) { d = mid; hi = mid - 1; } else lo = mid + 1; }
            if (d < c + 1) continue;
            for (long long dd = d - 1; dd <= d + 1; dd++) {
                if (dd < c + 1 || dd >= M) continue;
                u64 g1 = (F1[dd] + P1 - F1[c - 1]) % P1, g2 = (F2[dd] + P2 - F2[c - 1]) % P2;
                if (g1 == t1 && g2 == t2) {
                    printf("HIT  %lld/%lld = H(%lld,%lld)\n", pp[i], qq[i], c, dd);
                    hits++;
                }
            }
        }
    }
    printf("done: %lld hits over %d targets, c in [%lld,%lld]\n", hits, nt, CMIN, CMAX);
    return 0;
}
