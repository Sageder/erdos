"""patterns.py — machine check of pattern-completeness for geometric blocks.

Claim tested: for the partition B_j = [r^{j-1}, r^j) with integer ratio r >= 3, every
4-AP (x, x+d, x+2d, x+3d) of positive integers has block pattern (nondecreasing block
indices b1<=b2<=b3<=b4) belonging to:
  A    (b,b,b,b)
  B1   (b,b,b,b+1)
  B1'  (a,b,b,b)      a<b
  B2   (b,b,b+1,b+1)
  B3   (a,b,b,b+1)    a<b
  B4   (a,b,b+1,b+1)  a<b
and that for r = 2 (and equal-size blocks) additional patterns occur, including
4 distinct blocks (which are automatically monotone when blocks are laid out in
increasing order). Exhaustive scan for all APs with x+3d <= r^K.
"""

import sys
from collections import Counter

def blockidx(v, r):
    b = 0
    t = r
    while v >= t:
        t *= r
        b += 1
    return b

def scan(r, K):
    V = r ** K
    allowed = set()
    seen = Counter()
    examples = {}
    for d in range(1, (V - 1) // 3 + 1):
        for x in range(1, V - 3 * d + 1):
            bs = tuple(blockidx(x + k * d, r) for k in range(4))
            b1, b2, b3, b4 = bs
            if b1 == b2 == b3 == b4:
                lab = 'A'
            elif b1 == b2 == b3 and b4 == b3 + 1:
                lab = 'B1'
            elif b2 == b3 == b4 and b1 < b2:
                lab = "B1'"
            elif b1 == b2 and b3 == b4 == b2 + 1:
                lab = 'B2'
            elif b1 < b2 and b2 == b3 and b4 == b3 + 1:
                lab = 'B3'
            elif b1 < b2 and b3 == b4 == b2 + 1:
                lab = 'B4'
            else:
                lab = 'OTHER:' + str(tuple(sorted(set(bs))))
            seen[lab] += 1
            if lab not in examples:
                examples[lab] = (x, d, bs)
    return seen, examples

if __name__ == "__main__":
    for r, K in ((3, 7), (4, 6), (5, 5), (2, 9)):
        seen, ex = scan(r, K)
        others = {k: v for k, v in seen.items() if k.startswith('OTHER')}
        print(f"r={r}, all APs with x+3d <= {r**K}: profile {dict(seen)}")
        if others:
            for k in sorted(others):
                print(f"   {k}: example (x,d,blocks)={ex[k]}")
        else:
            print("   pattern-completeness HOLDS (only A,B1,B1',B2,B3,B4)")
        print()
