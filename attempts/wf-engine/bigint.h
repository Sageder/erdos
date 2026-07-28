/* bigint.h -- minimal fixed-width unsigned multiword arithmetic.
 *
 * Numbers are little-endian arrays of uint64_t of a caller-supplied length nw.
 * Everything is EXACT integer arithmetic; no floating point appears anywhere.
 *
 * Only the operations the search needs are provided:
 *   compare, is-zero, add, subtract, multiply by a 64-bit scalar,
 *   divide by a 64-bit scalar (quotient + remainder), reduce mod a 64-bit scalar.
 *
 * On x86-64 the 128/64 division is the hardware DIVQ instruction; the portable
 * fallback uses unsigned __int128 (correct but slower, via __udivti3).
 */
#ifndef BIGINT_H
#define BIGINT_H

#include <stdint.h>
#include <string.h>

typedef uint64_t u64;
typedef unsigned __int128 u128;

/* q = (hi:lo)/d, *rem = (hi:lo)%d.  REQUIRES hi < d (no overflow). */
static inline u64 div128(u64 hi, u64 lo, u64 d, u64 *rem)
{
#if defined(__x86_64__)
    u64 q, r;
    __asm__("divq %4" : "=a"(q), "=d"(r) : "0"(lo), "1"(hi), "r"(d));
    *rem = r;
    return q;
#else
    u128 cur = ((u128)hi << 64) | lo;
    *rem = (u64)(cur % d);
    return (u64)(cur / d);
#endif
}

static inline void bset0(u64 *a, int nw) { memset(a, 0, (size_t)nw * 8); }
static inline void bcpyw(u64 *d, const u64 *s, int nw) { memcpy(d, s, (size_t)nw * 8); }

static inline int biszero(const u64 *a, int nw)
{
    for (int i = 0; i < nw; i++) if (a[i]) return 0;
    return 1;
}

/* -1, 0, +1 for a<b, a==b, a>b */
static inline int bcmpw(const u64 *a, const u64 *b, int nw)
{
    for (int i = nw - 1; i >= 0; i--) {
        if (a[i] != b[i]) return a[i] < b[i] ? -1 : 1;
    }
    return 0;
}

/* d = a + b (nw words, carry out discarded -- caller guarantees no overflow) */
static inline void baddw(u64 *d, const u64 *a, const u64 *b, int nw)
{
    unsigned char c = 0;
    for (int i = 0; i < nw; i++) {
        u64 s = a[i] + b[i];
        u64 t = s + c;
        c = (s < a[i]) | (t < s);
        d[i] = t;
    }
}

/* d = a - b, requires a >= b */
static inline void bsubw(u64 *d, const u64 *a, const u64 *b, int nw)
{
    unsigned char br = 0;
    for (int i = 0; i < nw; i++) {
        u64 s = a[i] - b[i];
        u64 t = s - br;
        br = (a[i] < b[i]) | (s < br);
        d[i] = t;
    }
}

/* a = a*m + add ; returns the carry out of the top word (0 means it fitted) */
static inline u64 bmulsmall(u64 *a, int nw, u64 m, u64 add)
{
    u64 carry = add;
    for (int i = 0; i < nw; i++) {
        u128 t = (u128)a[i] * m + carry;
        a[i] = (u64)t;
        carry = (u64)(t >> 64);
    }
    return carry;
}

/* d = a/dv, returns a%dv.  d may alias a. */
static inline u64 bdivsmall(u64 *d, const u64 *a, int nw, u64 dv)
{
    u64 r = 0;
    for (int i = nw - 1; i >= 0; i--) d[i] = div128(r, a[i], dv, &r);
    return r;
}

static inline u64 bmodsmall(const u64 *a, int nw, u64 dv)
{
    u64 r = 0, q;
    for (int i = nw - 1; i >= 0; i--) q = div128(r, a[i], dv, &r);
    (void)q;
    return r;
}

static inline int bwords(const u64 *a, int nw)
{
    int k = nw;
    while (k > 1 && a[k - 1] == 0) k--;
    return k;
}

static inline int bbits(const u64 *a, int nw)
{
    int k = bwords(a, nw);
    if (k == 1 && a[0] == 0) return 0;
    int b = (k - 1) * 64;
    u64 t = a[k - 1];
    while (t) { b++; t >>= 1; }
    return b;
}

/* decimal print */
static void bprint(const u64 *a, int nw)
{
    u64 tmp[512];
    int k = bwords(a, nw);
    if (k > 512) { printf("<too big>"); return; }
    bcpyw(tmp, a, k);
    char buf[16384];
    int pos = 16383;
    buf[pos] = 0;
    if (biszero(tmp, k)) { printf("0"); return; }
    while (!biszero(tmp, k)) {
        u64 r = bdivsmall(tmp, tmp, k, 1000000000ULL);
        k = bwords(tmp, k);
        for (int j = 0; j < 9; j++) { buf[--pos] = '0' + (int)(r % 10); r /= 10; }
    }
    while (buf[pos] == '0' && buf[pos + 1] != 0) pos++;
    printf("%s", buf + pos);
}

#endif /* BIGINT_H */
