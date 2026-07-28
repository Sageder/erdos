/* collide.c -- search for two DIFFERENT blocks with the SAME reciprocal sum:
 *      H(a,b) = H(c,d),   2 <= a < b <= N,  2 <= c < d <= N,  (a,b) != (c,d).
 *
 * WHY: if such a pair exists with (d-c) > (b-a), then inside any solution the
 * block [a,b] may be replaced by [c,d] (when [c,d] is disjoint from the rest),
 * leaving the sum and the run count unchanged but RAISING the capacity
 * floor((d-c+1)/2) - floor((b-a+1)/2) >= 1.  That is a "+1 block" move.
 *
 * Method: exact fingerprints.  Work in F_P with P a 62-bit prime; the prefix
 * S(n) = sum_{j=2}^n j^{-1} mod P gives H(a,b) = S(b)-S(a-1).  Equal rationals
 * give equal fingerprints, so every true collision is found (no false negatives).
 * Two independent primes make a false positive essentially impossible; every
 * reported hit is re-verified exactly in Python afterwards.
 *
 * usage: ./collide N        (only blocks with H(a,b) <= 1 are stored)
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef unsigned long long u64;
typedef __uint128_t u128;

static const u64 P1 = 4611686018427387847ULL;   /* prime */
static const u64 P2 = 4611686018427388039ULL;   /* prime */

static u64 mulmod(u64 a, u64 b, u64 m) { return (u64)((u128)a * b % m); }
static u64 powmod(u64 a, u64 e, u64 m) { u64 r = 1; a %= m; while (e) { if (e & 1) r = mulmod(r, a, m); a = mulmod(a, a, m); e >>= 1; } return r; }
static u64 invmod(u64 a, u64 m) { return powmod(a, m - 2, m); }

typedef struct { u64 f1, f2; int a, b; } Rec;
static int cmpRec(const void *x, const void *y) {
    const Rec *p = x, *q = y;
    if (p->f1 != q->f1) return p->f1 < q->f1 ? -1 : 1;
    if (p->f2 != q->f2) return p->f2 < q->f2 ? -1 : 1;
    return 0;
}

int main(int argc, char **argv) {
    int N = argc > 1 ? atoi(argv[1]) : 2000;
    u64 *S1 = malloc((N + 2) * sizeof(u64)), *S2 = malloc((N + 2) * sizeof(u64));
    double *Sd = malloc((N + 2) * sizeof(double));
    S1[1] = S2[1] = 0; Sd[1] = 0;
    for (int n = 2; n <= N; n++) {
        S1[n] = (S1[n - 1] + invmod(n, P1)) % P1;
        S2[n] = (S2[n - 1] + invmod(n, P2)) % P2;
        Sd[n] = Sd[n - 1] + 1.0 / n;
    }
    long long cap = 1, cnt = 0;
    for (int a = 2; a <= N; a++) for (int b = a + 1; b <= N; b++) { if (Sd[b] - Sd[a - 1] > 1.0) break; cap++; }
    Rec *R = malloc(cap * sizeof(Rec));
    for (int a = 2; a <= N; a++) {
        for (int b = a + 1; b <= N; b++) {
            if (Sd[b] - Sd[a - 1] > 1.0) break;
            R[cnt].f1 = (S1[b] + P1 - S1[a - 1]) % P1;
            R[cnt].f2 = (S2[b] + P2 - S2[a - 1]) % P2;
            R[cnt].a = a; R[cnt].b = b; cnt++;
        }
    }
    printf("N=%d blocks stored=%lld\n", N, cnt);
    qsort(R, cnt, sizeof(Rec), cmpRec);
    long long hits = 0;
    for (long long i = 1; i < cnt; i++) {
        if (R[i].f1 == R[i - 1].f1 && R[i].f2 == R[i - 1].f2) {
            printf("COLLIDE [%d,%d] and [%d,%d]\n", R[i - 1].a, R[i - 1].b, R[i].a, R[i].b);
            if (++hits > 200) { printf("(cap)\n"); break; }
        }
    }
    printf("done: %lld collisions\n", hits);
    return 0;
}
