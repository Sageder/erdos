# ROUTES.md — route registry (Erdős 273)

Format: id | mathematical family | status | targets / outcome.
Last updated 2026-07-28. See NOTES.md (newest first) and AUDITS.md.

## Main line (run by the session itself)

- **M | necessary conditions, reductions, infrastructure** | ACTIVE, four results |
  * **Lemma M1 (audited, passes):** every covering system with all moduli in E has
    lcm ≥ **55440** = 2⁴·3²·5·7·11, since f(L) := Σ_{n|L, n∈E} 1/n must exceed 1 and 55440 is the
    least L with f(L) > 1 (exhaustive sieve over ALL L ≤ 3·10⁶, re-derived to 10⁷; f = 6429/6160).
    Also: 223 divisibility-minimal such lattices below 10⁷; best lattice ≤ 10⁷ is
    L = 8648640 with f = 1.157547.
  * **Lemma M2 (audited, passes):** inf Σ1/n over distinct-moduli covering systems = 1, not
    attained; explicit systems of cost 1 + (1/3)2^{−k} via the doubling map, verified by full
    sweeps. ⟹ reciprocal-budget counting cannot decide 273 in either direction.
    (Independently corroborated by Filaseta–Kalogirou arXiv:2407.15280.)
  * **Lemma M3 (proved + verified both directions):** E-covering ⟺ two DISJOINT M_0, M_1 ⊆ H,
    each supporting a distinct-moduli covering of ℤ. `attempts/route-M-main/PARITY_SPLIT.md`.
  * **Observation M4:** at most one of M_0, M_1 contains 2 and at most one contains 3, so YES
    requires a covering from H\{2} AND one from H\{3}. Contrapositive: **no covering from H\{2}
    ⟹ 273 is NO.**
  * Infrastructure: `experiments/verify_certificate.py` (independent verifier: admissibility by
    deterministic trial division, distinctness, coverage by both a full mod-L sweep and exact
    class-elimination), `M_sat.py`/`M_sat2.py` (exact SAT over divisor lattices and over the
    recursion pools Q(k) = {e : ke+1 prime}), `M_local2.c` (fast local search),
    `M_lattice_scan.py`, `M_cost_infimum.py`, `M_parity_split.py`.

## Wave 1 (8 independent subagents, none told a favoured answer)

- **A | SAT / exact-cover certificate search over structured L** | running; first result in |
  produced a **verified H-world covering**: moduli {2,3,5,6,9,15,18,20,30,36,90} (all dividing
  180), cost 14/9 — independently re-verified by me. Lifting it (Lemma M3) gives 11 congruences
  with moduli {4,6,10,12,18,30,36,40,60,72,180} ⊆ E covering EXACTLY the even integers.
- **B | recursive / hierarchical divisor-tree construction** | running.
- **C | parity split, halved world H** | running; is attacking the M4 pivot (coverings with the
  modulus 2 forbidden) at L' = 2520, 27720, 360360, 720720.
- **D | local obstruction / NO branch** | running.
- **E | literature + toolbox** | **COMPLETE**, `attempts/route-E-literature/LITERATURE.md`.
  Key outputs: attribution fix (Sahasrabudhe, not Sawhney); Filaseta–Kalogirou kills the budget
  route; BBMST/Schinzel (some n_i | n_j) applies to E as a cheap filter; Hough, Hough–Nielsen,
  BBMST-616000, Cummings–Filaseta–Trifonov are all **vacuous on E** because 4 ∈ E and every
  element of E is even; **no refereed work exists on covering systems with moduli restricted to
  shifted primes**; Z.-W. Sun's "covering numbers" is the closest framework.
  CAVEAT: sandbox egress blocked all primary PDFs; everything is search-level only.
- **F | minimum reciprocal cost** | running.
- **G | Selfridge template surgery** | running.
- **H | budget combinatorics, exhaustive refutation of small families** | running.

## Wave 2 (launched after wave-1 triage)

- **P2 | pivot certificate hunt** | running | decide the surviving pivot lattices
  (M = 1080, 1260, 1680, 2160, 2520 and beyond) exactly; extend the fiber elimination; quantify
  the frontier where Φ_q ≥ 1 becomes vacuous.
- **AUD | fresh adversarial audit** | running | given only the problem statement and the draft,
  instructed to BREAK the parity split, the infimum theorem, Lemma A2, Theorem A3, the fiber test,
  the rigidity theorem, the fixed-Q barrier, and to hunt for overclaims.
- **M (main line) | pivot elimination** | ACTIVE, strong result |
  `experiments/M_pivot.py`: the q-adic fiber test at threshold 1 kills the pivot on 58 of the 63
  lattices M ≤ 3168 whose pool has budget > 1; survivors so far M = 1080, 1260, 1680, 2160, 2520.
  This reproduces route G's SAT-UNSAT results for M ≤ 720 instantly and extends them, replacing
  search by a rigorous counting test — the same counting argument SAT could not reproduce.

## Blocked / forbidden directions (recorded so they are not reopened)

- **Reciprocal-budget obstructions for the NO branch** — BLOCKED by Lemma M2 + Filaseta–Kalogirou:
  cost can be 1 + ε and Σ_{p≥5} 1/(p−1) diverges.
- **Minimum-modulus theorems (Hough, BBMST) as obstructions** — BLOCKED: vacuous because 4 ∈ E.
- **Any construction forcing one of M_0, M_1 to have all moduli odd** — FORBIDDEN: that is the
  open Erdős–Selfridge odd covering problem.
- **Flat SAT/local search beyond L ≈ 10⁷** — BLOCKED by instance size; needs the hierarchical route.

## Status of the problem

**Unresolved.** Proved so far: M1, M2, M3, M4 and the verified H-covering / even-integer artifact.
The entire remaining difficulty is the disjointness requirement of Lemma M3.
