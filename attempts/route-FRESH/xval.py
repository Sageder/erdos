import random, sys
sys.path.insert(0, '/home/user/erdos/experiments')
from apcheck import has_monotone_kap_brute, has_monotone_kap_pos, has_monotone_kap_general
from core import has_kap_signs, has_kap_brute, Builder, build_check

rng = random.Random(1961)
# 1) my sign-sequence checker vs apcheck (both implementations), k=3,4,5
for t in range(4000):
    n = rng.randint(4, 10)
    p = list(range(1, n+1)); rng.shuffle(p)
    for k in (3,4,5):
        a = has_kap_signs(p,k); b = has_monotone_kap_pos(p,k)
        c = has_monotone_kap_brute(p,k); d = has_kap_brute(p,k)
        assert a==b==c==d, (p,k,a,b,c,d)
# 2) Builder legality  <=>  no monotone 4-AP  (prefix-by-prefix)
for t in range(3000):
    n = rng.randint(4, 9)
    p = list(range(1, n+1)); rng.shuffle(p)
    ok = build_check(p, n)
    assert ok == (not has_monotone_kap_pos(p,4)), (p, ok)
    # prefixes too: a prefix of a 4-AP-free perm is buildable
    for L in range(n+1):
        assert build_check(p[:L], n) == (not has_monotone_kap_general(p[:L],4)), (p,L)
print("route-FRESH xval OK: sign-checker == apcheck (k=3,4,5); Builder == 4-AP-freeness")
