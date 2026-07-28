"""mod2_signs.py — Modification idea 2 (REFUTED, with certificate).

Family: keep the blocks B_m = [4^m, 4^{m+1}) in increasing order, but order
each block by LSB-first lexicographic comparison with an arbitrary sign table
sigma[m][l] in {0,1} (at recursion level l, put bit-value sigma[m][l] first).
Construction A is the member sigma[m][l] = m mod 2.

Pair criterion (proved in REPORT.md): for u, u+d in B_m with l = v2(d),
u precedes u+d  <=>  bit_l(u) = sigma[m][l].

REFUTATION: the two 4-APs
    1,  6, 11, 16   (x=1, d=5): needs only "6 before 11 in pi_1";
                     6 even -> realized iff sigma[1][0] = 0.
    2,  7, 12, 17   (x=2, d=5): needs only "7 before 12 in pi_1";
                     7 odd  -> realized iff sigma[1][0] = 1.
Heads (1 resp. 2) lie in B_0, tails (16 resp. 17) in B_2 — their positions are
automatic.  So EVERY sign table realizes one of the two: the whole 2^infinity
family contains a monotone 4-AP.  Machine check below on both settings of
sigma[1][0] (all other signs alternating as in Construction A).
"""

import sys

sys.path.insert(0, "/home/user/erdos/attempts/route-R2")
from checkers import enumerate_monotone_kaps, find_monotone_kap
from construction import block


def block_order_sigma(m, sigma_row):
    """Order B_m by LSB-lex with per-level signs sigma_row (list of bits)."""
    width = 2 * (m + 1)

    def key(v):
        return tuple(((v >> i) & 1) ^ sigma_row[i] for i in range(width))
    return sorted(block(m), key=key)


def build_variant(num_blocks, sigma):
    out = []
    for m in range(num_blocks):
        out.extend(block_order_sigma(m, sigma(m)))
    return out


if __name__ == "__main__":
    outlines = []

    def log(s):
        print(s)
        outlines.append(s)

    # sanity: sigma[m][l] = m mod 2 reproduces Construction A
    from construction import prefix
    sigA = lambda m: [m % 2] * (2 * (m + 1))
    assert build_variant(6, sigA) == prefix(6)
    log("sanity OK: sigma=m mod 2 reproduces Construction A")

    for s10 in (0, 1):
        def sig(m, s10=s10):
            row = [m % 2] * (2 * (m + 1))
            if m == 1:
                row[0] = s10
            return row
        p = build_variant(6, sig)
        n = len(p)
        assert sorted(p) == list(range(1, n + 1))
        aps = set(enumerate_monotone_kaps(p, 4))
        pred = (1, 5, "inc") if s10 == 0 else (2, 5, "inc")
        log("sigma[1][0]=%d: predicted 4-AP %s present: %s "
            "(certificate pair realized)" % (s10, pred, pred in aps))
        assert pred in aps
        w5 = find_monotone_kap(p, 5)
        log("   (5-AP status of this variant on N=%d: %s)"
            % (n, "none" if w5 is None else repr(w5)))

    log("")
    log("CONCLUSION: every sign table sigma realizes 1,6,11,16 or 2,7,12,17;")
    log("the entire LSB-lex-with-signs family fails at length 4. REFUTED.")

    with open("/home/user/erdos/attempts/route-R2/mod2_output.txt", "w") as f:
        f.write("\n".join(outlines) + "\n")
