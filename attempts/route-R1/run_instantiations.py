"""run_instantiations.py — Route R1 instantiation sweep.

Claim tested: for each instantiation (block partition + gadget schedule + interleaving)
whether the induced permutation prefix restricted to values [1..M] is monotone-4-AP-free.
Verdicts + exact minimal killing APs printed; classification into cases
A / B1 / B1' / B2 / B3 / B4 / other refers to blocks-in-increasing-position-order geometry.
"""

from framework import *

def run(name, blocks, gadget_for_block, M, order=None, max_report=12):
    seq = build_sequence(blocks, gadget_for_block, order)
    perm = restrict_to_M(seq, M)
    viol, total = monotone_4ap_violations(perm, max_report=max_report)
    print(f"== {name}  (M={M}, blocks={len(blocks)})")
    if total == 0:
        print("   SURVIVES: no monotone 4-AP among values 1..%d" % M)
    else:
        print(f"   DIES: {total} monotone 4-APs among values 1..{M}. Minimal witnesses:")
        from collections import Counter
        cc = Counter()
        for (x, d, o) in viol:
            bs, lab = classify_ap(blocks, x, d)
            cc[lab] += 1
            print(f"     {o} AP {x},{x+d},{x+2*d},{x+3*d}  (d={d})  blocks={bs}  case={lab}")
        # classify a bigger sample for the mechanism profile
        big, _ = monotone_4ap_violations(perm, max_report=4000)
        prof = Counter(classify_ap(blocks, x, d)[1] + o for (x, d, o) in big)
        print(f"   case profile of first {len(big)} violations: {dict(prof)}")
    print()
    return total

def sig(j):
    return gadget_sigma

if __name__ == "__main__":
    M = 10000

    # I1: equal-size blocks (16), sigma everywhere, blocks in order
    run("I1 equal-16 / sigma / in-order", blocks_equal(16, (M // 16) + 1), sig, M)

    # I2: geometric r=2, sigma, in order
    run("I2 geometric x2 / sigma / in-order", blocks_geometric(2, 14), sig, M)

    # I3: geometric r=4, sigma, in order
    run("I3 geometric x4 / sigma / in-order", blocks_geometric(4, 8), sig, M)

    # I3b: geometric r=3, sigma, in order
    run("I3b geometric x3 / sigma / in-order", blocks_geometric(3, 9), sig, M)

    # I4: geometric r=4, alternate sigma / value-reflected sigma
    run("I4 geometric x4 / alternate sigma,reflect / in-order", blocks_geometric(4, 8),
        lambda j: gadget_sigma if j % 2 == 0 else gadget_sigma_reflect, M)

    # I5: geometric r=4, alternate sigma / position-reversed sigma
    run("I5 geometric x4 / alternate sigma,revpos / in-order", blocks_geometric(4, 8),
        lambda j: gadget_sigma if j % 2 == 0 else gadget_sigma_revpos, M)

    # I6: geometric r=4, all blocks value-reflected sigma
    run("I6 geometric x4 / all reflect / in-order", blocks_geometric(4, 8),
        lambda j: gadget_sigma_reflect, M)

    # I7: factorial blocks, sigma (cover 1..7! - 1 = 5039)
    run("I7 factorial / sigma / in-order", blocks_factorial(6), sig, 5039)

    # I8: geometric r=4, sigma, adjacent-block-swap interleaving (B2 B1 B4 B3 ...)
    nb = 8
    swap = [j + 1 if j % 2 == 0 else j - 1 for j in range(nb)]
    run("I8 geometric x4 / sigma / adjacent-swap interleave", blocks_geometric(4, nb), sig,
        M, order=swap)

    # I9: geometric r=4, top-half-first coarse inversion with sigma halves
    run("I9 geometric x4 / tophalf-sigma / in-order", blocks_geometric(4, 8),
        lambda j: gadget_tophalf_sigma, M)

    # I10: geometric r=4, full recursive top-half-first (identity leaves)
    run("I10 geometric x4 / tophalf-recursive / in-order", blocks_geometric(4, 8),
        lambda j: gadget_tophalf_first, M)
