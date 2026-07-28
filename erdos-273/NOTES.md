# NOTES.md — lab notebook, Erdős 273 (newest entries at top)

## 2026-07-28 — how far the pivot elimination can possibly reach (honest limit)

Φ_q(S) ≥ A_q(S) := Σ_{m ∈ S, q ∤ m} 1/m, because moduli coprime to q contribute to EVERY q-adic
fiber for EVERY residue assignment. So the test at q is VACUOUS once A_q > 1.

Measured (`M_pivot`-style computation) for the pivot pool S(M) = {m | M : 2m+1 prime, m ≥ 3}:
  M       pool budget   min_q A_q (always attained at q = 3)
  1080    1.224         0.375
  2520    1.404         0.500
  27720   1.587         0.619
  360360  1.711         0.681
  720720  1.747         0.688
**A_3 stays at roughly HALF the pool budget**, because H is enriched at multiples of 3 (exactly
half of H is divisible by 3, density 1/φ(3) = 1/2 rather than 1/3). So A_3 > 1 needs pool budget
> 2, which route G's beam search says does not happen below M ≈ 10⁹. **The q = 3 fiber test is
therefore still potentially effective for smooth lattices all the way to M ~ 10⁹** — far beyond
where I can compute Φ_3 exactly.

Reconciliation with route D's barrier (P6): D's certificate is S = H ∩ [2, 82899], an INTERVAL,
whose lcm is astronomically large and whose divisor pool is correspondingly rich, so A_3 > 1 there
and the test is genuinely vacuous. The two statements are consistent: the fiber test stays sharp
on *smooth lattices of moderate size* and dies on *lattices with huge lcm*. Since a real covering
system may have a huge lcm, **this can never close the problem** — it is a search tool, not a
proof route. Recorded so nobody mistakes the long run of kills for evidence of NO.

Current elimination state: of the lattices M ≤ 4140 whose pivot pool has budget > 1, **69 killed,
10 undecided**; the undecided ones begin M = 1080, 1260, 1680, 2160, 2520. Exact SAT and
exhaustive DFS on those five are both slow (route B saw the same on 1260/2520/5040): these small
instances are genuinely hard because the UNSAT witness is a counting argument.

## 2026-07-28 — MAIN LINE: the fiber test cracks the PIVOT lattices wholesale

The pivot (Observation M4 / route G's Corollary 3) is: **is there a covering of ℤ with distinct
moduli from H ∖ {2}?** A negative answer proves 273 is NO.

`experiments/M_pivot.py` applies the SAME q-adic fiber machinery but at threshold **1** (a single
covering, not two): for every prime q | M, Φ_q(S) ≥ 1 is necessary, S = {m | M : 2m+1 prime,
m ≥ 3}. Exact branch-and-bound. Result on every lattice M ≤ 1200 whose pool has budget > 1
(21 of them): **20 KILLED**, only M = 1080 survives.
  180 (Φ₃), 240 (Φ₂), 270 (Φ₂), 360 (Φ₃), 420 (Φ₂), 450 (Φ₂), 480 (Φ₂), 540 (Φ₃), 600 (Φ₂),
  630 (Φ₃), 660 (Φ₂), 720 (Φ₃), 810 (Φ₂), 840 (Φ₅), 900 (Φ₃), 960 (Φ₂), 990 (Φ₃), 1008 (Φ₂),
  1170 (Φ₃), 1200 (Φ₂).
This reproduces route G's SAT-UNSAT results for M ≤ 720 **instantly and by a rigorous test rather
than by search**, and extends them to 1200. Scan to M = 30000 launched.

Why this matters methodologically: route A measured that CaDiCaL cannot even decide L = 55440
(3.7M literals) in 30 minutes, because the UNSAT witness is a counting argument that resolution
reproduces only exponentially. The fiber test IS that counting argument, made exact — so it
decides in milliseconds what SAT cannot decide at all. All flat-SAT effort in this project should
be replaced by fiber elimination plus targeted SAT only on survivors.

CAVEAT (scope, §7 item 5): these eliminate individual lattices. H ∖ {2} is infinite, so no finite
list of eliminations can prove the pivot negatively. They are search lemmas, not a proof — exactly
the truncation trap PROMPT §3 warns about, and it is recorded as such.

## 2026-07-28 — WAVE 1 COMPLETE (routes A, B, D, E, F, G in; C, H still running)

Findings transcribed into `attempts/route-*/FINDINGS.md` (the subagent harness blocked them from
writing report .md files themselves). Audits 4 and 5 in AUDITS.md. Headline items:

**Five independent re-derivations of the parity split** (Lemma M3 = D1 = G's Lemma 2 = A's Lemma
A1 = F's parity reduction). This is now solid.

**NEW PROVED TOOLS (both audited by me independently):**
- **Route A, Lemma A2 (forced overlap).** For a covering with modulus set M and any pairwise
  coprime T ⊆ M: Σ_{m∈M} 1/m − 1 ≥ Σ_{m∈T} 1/m − 1 + Π_{m∈T}(1 − 1/m) =: f(T). Residue-free,
  because coprimality makes the classes independent by CRT.
- **Route A, Theorem A3.** If 60 | L and 1 < B_E(L) ≤ 31/30 then no E-covering has lcm dividing L.
  (4, 6, 10 forced; halves 2, 3, 5 pairwise coprime; f({3,5}) = 1/15 ≥ 2B_E−2 forbids sharing a
  half; three objects, two halves.) Kills **63 of the 90** candidate lcm values ≤ 10⁶.
- **Route D, fiber condition Φ_q ≥ 2** (exact max-min q-adic fiber budget). Kills L = 55440 (q=5),
  65520, 75600, 32760, 50400, 27720·2 — including the minimal budget-feasible lattice.
- **Route F, RIGIDITY THEOREM.** The only exact partition of ℤ minus one class by distinct moduli
  > 1 is the dyadic staircase {2,4,…,2^m}. Since E ∩ {2^k} = {4,16,256,65536} (Fermat primes minus
  1) contains no two consecutive powers of 2 and 2 ∉ E, **the only known mechanism driving the
  reciprocal cost to 1 is structurally unavailable in E**, and in H only trivially available.

**ROUTE D'S DECISIVE NEGATIVE META-RESULT (P6).** For every FIXED finite set Q of primes,
Σ_{m ∈ H, gcd(m,∏Q)=1} 1/m = ∞, and such moduli contribute to every Q-cell for every residue
assignment. Explicit certificate: **S = H ∩ [2, 82899] satisfies every single-prime fiber
condition with threshold 2, at every level, for every residue assignment.** So NO obstruction
local at a fixed finite set of primes can ever prove NO. PROMPT §5's q-adic-fiber idea is dead as
a route to NO (it survives only as a per-lattice elimination tool, which is how we now use it).

**THE QUANTITATIVE PICTURE (consistent across routes B, F, G):**
- Cheapest H-covering found anywhere: **65/48 ≈ 1.3542** (route F, L = 288), re-verified by me;
  its E-image {4,6,12,16,18,36,72,96,192,576} covers every even integer at cost 65/96.
  μ_H shows NO downward trend (65/48 at L = 288, 576, 864, 1152, 1728) — the opposite of the
  unrestricted world where the infimum is 1.
- Two disjoint H-coverings need B_H > 2·(cheapest). At 2·1.3542 = 2.708 that first happens around
  **lcm ≈ 3.5·10¹⁵**; at route B's constructible 2·1.4335 = 2.867, around **lcm ≈ 2·10²²**.
- Every flat search is capped at lcm ≲ 10⁷–10⁸ (memory) and, for UNSAT, at ~10⁴–10⁵ residues
  (route A measured CaDiCaL failing on L = 55440, only 3.7M literals, in > 30 min).
  **That is a gap of 8–15 orders of magnitude, and it is where every route broke.**

**THE CRUX, now sharply identified and consistent with my Observation M4:**
> Is there a covering system of ℤ with distinct moduli all of the form (p−1)/2, p ≥ 7 prime
> (equivalently: an H-covering avoiding the modulus 2)?
Route G proved **UNSAT for every lattice M ≤ 600 with budget > 1, plus 720** (SAT, cross-checked
by an independent branch-and-bound), with exact near-misses: min uncovered 25/180, 34/360, 60/720.
The obstruction concentrates on **4, 10, 12 ∉ H** — exactly the moduli every cheap least-modulus-3
covering wants. Route B and route G both failed to decide the first genuinely relevant lattice
(M = 27720, budget 1.5873): SAT ran > 20 min without a verdict.

**Corrections logged:** (i) my hand-written H list in the wave-1 briefs OMITTED 54 (109 is prime);
PROBLEM.md's list stops at 44 and is correct, and every agent recomputed H itself, so nothing
downstream was affected. (ii) PROMPT.md §4 names "Sawhney"; the correct author is Sahasrabudhe.

## 2026-07-28 — Observation M4: a pivot that could decide the problem outright

Immediate from Lemma M3 plus the disjointness of M_0 and M_1, since 2 and 3 each occur ONCE in H:
  * at most one of M_0, M_1 contains 2, so **at least one of them avoids 2**;
  * at most one contains 3, so **at least one avoids 3**.
Hence:

  **273 has answer YES  ⟹  there is a covering system of ℤ with distinct moduli from H \ {2},
    AND there is one with distinct moduli from H \ {3}.**

Contrapositive, which is the valuable direction:

  **If NO covering system exists with distinct moduli from H \ {2}, the answer to 273 is NO.**

This is a genuine reduction of the NO branch to a single cleaner statement, and it is the pivot
PROMPT §5 flags. Two honest caveats:
 (a) It is still a UNIVERSAL statement over all finite subsets of the infinite set H \ {2}, so no
     finite search can establish it — exactly the same quantifier difficulty as the original.
     Its value is that H \ {2} is a *less* structured target than "two disjoint systems", and that
     a POSITIVE answer (an explicit covering avoiding 2) is a finite certificate that removes this
     obstruction and focuses everything on disjointness.
 (b) It is only a necessary condition for YES: exhibiting one covering avoiding 2 and one avoiding
     3 does NOT give a disjoint pair.
Budget check (so the pivot is not vacuous): Σ 1/m over m ∈ H \ {2}, m ≤ Y equals 1.943 (Y = 100)
and 2.631 (Y = 10^3), so the pivot is not budget-obstructed; the difficulty is structural (least
modulus 3).
Route C was tasked with exactly this and is running it (its `experiments/C_out/f2_*.txt` show
H-divisor pools with 2 forbidden: budget 1.404 at L' = 2520, 1.587 at 27720, 1.711 at 360360,
1.747 at 720720 — all comfortably above 1).

ALSO recorded, from Lemma M3 + the joint requirement: two disjoint H-systems need H-divisor budget
> 2 on the common lattice, i.e. f(2L') > 1, i.e. 2L' ≥ 55440. So **L' ≥ 27720 in the halved world**
— the smallest lattice that could possibly host BOTH halves is exactly the L = 55440 instance.

## 2026-07-28 — Lemma M3 (parity split) PROVED and verified both directions

`attempts/route-M-main/PARITY_SPLIT.md`, verified by `experiments/M_parity_split.py`.
Statement: a covering system with all moduli in E exists ⟺ there are two DISJOINT finite sets
M_0, M_1 ⊆ H = {m ≥ 2 : 2m+1 prime}, each supporting a distinct-moduli covering of ℤ.
Both directions written out in full; negative integers explicitly handled (classes are two-sided,
and the argument quantifies over all y ∈ ℤ); disjointness of M_0, M_1 derived from distinctness of
the E-moduli; the E-unit/H-unit budget bookkeeping spelled out (NO doubling of the E-budget).
Computationally confirmed: the lift of the verified H-covering covers EXACTLY one parity class
(both j = 0 and j = 1 checked by full mod-360 sweeps), and on 119 random E-systems
"original covers the parity-j integers" ⟺ "the halved subsystem covers ℤ" in every case.

**Concrete artifact.** Lifting route A's verified H-covering gives 11 congruences whose moduli
{4, 6, 10, 12, 18, 30, 36, 40, 60, 72, 180} all lie in E and which cover EXACTLY the even integers
(cost 7/9). These are precisely the divisors of 360 lying in E — Selfridge's pool with the modulus
2 deleted. So one half of the problem is solved explicitly and the entire remaining difficulty is:
**cover the odd integers using E-moduli DISJOINT from those 11.**
In H-units: find a covering of ℤ with distinct moduli from H \ {2,3,5,6,9,15,18,20,30,36,90},
whose least available modulus is 8. Budget of the leftover pool: 1.575 (m ≤ 10^3), 2.10 (m ≤ 10^4).
So it is not budget-obstructed, but it demands a covering of least modulus ≥ 8 from a thin set —
and the first half should really be chosen jointly with the second rather than greedily.

**Trap recorded (route E, item 6).** Any construction that forces one of M_0, M_1 to consist of
ODD moduli only is a dead end: that is the Erdős–Selfridge odd covering problem, still open.

## 2026-07-28 — search data: how far are the lattices from admitting a covering?

`experiments/M_local2.c` (greedy + full coordinate-descent sweeps; assigns a residue to EVERY
admissible divisor of L, which is WLOG optimal since coverage is monotone and distinctness allows
one residue per modulus). Best uncovered fraction found:
  L = 55440   f = 1.0437   ->  14.49 % uncovered
  L = 720720  f = 1.1057   ->  12.31 % uncovered
  L = 8648640 f = 1.1575   ->   9.22 % uncovered
Trend: roughly 3 % of coverage gained per 0.05 of f. Naive extrapolation would put closure near
f ≈ 1.3 (lcm ~ 3·10^12). THIS IS NOT EVIDENCE OF ANYTHING — local search on covering systems is
notoriously bad because coverings are brittle interlocking objects, and Lemma M2's cheap systems
would never be found by local search either. Recorded only as a difficulty gauge.

q-adic fiber balance (necessary condition: min over q-adic paths of the fiber budget must be ≥ 1;
its Haar average is exactly f). A greedy balancing heuristic gives LOWER bounds on the achievable
minimum: at L = 8648640, q = 3,5,7,11,13 all reach ≥ 1 comfortably, and q = 2 reaches only 0.903.
The q = 2 tree is the binding one — as expected, since every element of E is even so the level-0
term vanishes identically. NOTE: a greedy lower bound below 1 proves NOTHING (the optimum may be
higher); to convert this into a rigorous impossibility one needs an UPPER bound on the max-min,
which is a genuinely hard combinatorial optimisation. Also noted: the moduli 4, 16, 256, 65536
(the Fermat primes) have 2-adic weight exactly 1, i.e. each alone satisfies every fiber below its
node — so the q = 2 condition is much less binding than the greedy number suggests.

Exact SAT at L = 55440 (43 moduli, 212640 vars, 480634 clauses) did NOT terminate within 1500 s
under heavy CPU contention; relaunched with a 5400 s budget (`sat55440.log`). Its verdict either
way is a rigorous statement about that lattice only.

## 2026-07-28 — ROUTE E (literature) returned. Two items change the picture.

Full report: `attempts/route-E-literature/LITERATURE.md`. CAVEAT recorded by the agent and
retained here: outbound HTTPS to arxiv/journals was blocked in the sandbox, so NO primary PDF was
opened; everything is reconstructed from search-engine summaries and is tagged [V2]/[V1]/[U] in
that file. Treat all of it as UNCONFIRMED until a primary source is read. Do not let any of it
become load-bearing in a final write-up without re-verification.

0. **I RE-VERIFIED items 1 and 2 MYSELF by web search (2026-07-28).** Confirmed:
   (a) "On the Erdős covering problem: the density of the uncovered set", Balister, Bollobás,
       Morris, **Sahasrabudhe**, Tiba, *Inventiones mathematicae* **228** (2022), no. 1, 377–414
       (Springer link confirms title, authors, volume, pages). "Sawhney" in PROMPT.md §4/§7 is
       an error.
   (b) arXiv:2407.15280, **Michael Filaseta and Alexandros Kalogirou**, "Covering systems with the
       sum of the reciprocals of the moduli close to 1" (submitted 21 July 2024): addresses
       Davenport's 1952 problem of finding a condition on the minimum modulus of a finite distinct
       covering system forcing Σ1/n_i to be bounded away from 1, and **proves the 1973
       Erdős–Selfridge conjecture that minimum modulus > 4 suffices**.
   Direct HTTPS to arxiv/journals is blocked by this sandbox's egress gateway (403 on CONNECT) and
   WebFetch also 403s, so I could NOT read the primary PDFs; the above is confirmed at
   title/abstract/bibliographic level via search only. Whether Filaseta–Kalogirou's constant is
   explicit remains UNVERIFIED — do not make it load-bearing.

1. **ATTRIBUTION CORRECTION to PROMPT.md §4.** The covering-systems author is Julian
   **SAHASRABUDHE**, not "Sawhney": Balister–Bollobás–Morris–**Sahasrabudhe**–Tiba. (Mehtaab
   Sawhney is a different mathematician.) PROMPT.md §4 and §7.10 name "Sawhney"; that is an error
   in the prompt's background, not in the mathematics. Every citation in this project must use
   Sahasrabudhe.

2. **Filaseta–Kalogirou (arXiv:2407.15280, 2024) — kills the budget route for good.** Reported
   statement: distinct-moduli covering systems with least modulus m_0 ∈ {2,3,4} exist with
   Σ 1/n_i < 1 + ε for EVERY ε > 0; a positive lower bound on the excess is only available once
   m_0 > 4. **Since 4 ∈ E, any E-system using the modulus 4 lies exactly in the regime where no
   excess bound is known.** This independently corroborates our Lemma M2 (which we proved and
   verified ourselves for m_0 = 2) and extends it to m_0 = 3, 4.
   ⟹ Reciprocal-sum/budget counting can NEVER decide problem 273, in either direction.

3. **BBMST second main theorem (Schinzel's conjecture, Invent. Math. 228 (2022)):** every covering
   system with distinct moduli has n_i | n_j for some i ≠ j. Applies verbatim to E; satisfiable in
   E (4 | 12), so not fatal, but it is a genuine and cheap search filter: the modulus set may not
   be a divisibility antichain.

4. **Dalton–Trifonov (J. Integer Seq. 25 (2022) 22.9.1):** least modulus 4 ⟹ largest modulus ≥ 60
   and lcm ≥ 360 (best possible). Applies to any E-system containing 4.

5. **Most famous tools are VACUOUS on E**, as the agent checked item by item: Hough (least modulus
   ≤ 10^16) and BBMST (≤ 616000) are about LARGE least modulus — E has least element 4;
   Hough–Nielsen ("some modulus divisible by 2 or 3") is automatic since every element of E is
   even; the squarefree/odd-moduli results do not apply since E is not squarefree.
   DMNR confirmed exactly as used here ("in an exact cover by k ≥ 2 classes the largest modulus
   occurs at least twice"), with the Znám/Newman refinement to "at least p times", p the least
   prime factor of the largest modulus.

6. **Item 9 settled computationally** (`experiments/E_selfridge360.py`, exhaustive + exact): the
   divisors d > 1 of 360 with d+1 prime are {2,4,6,10,12,18,30,36,40,60,72,180}, Σ1/d = 23/18, and
   a covering system using all twelve EXISTS (explicit witness, re-verified residue by residue).
   Deleting the modulus 2 leaves budget 7/9 < 1, so no cover survives: Selfridge's construction
   rests entirely on 0 (mod 2) — precisely what 273 forbids.

DIAGNOSIS. The NO branch loses its most natural tool: no density/reciprocal-sum obstruction can
work, and every published minimum-modulus theorem is vacuous on E because 4 ∈ E. The NO branch
would need a genuinely new mechanism keyed to the arithmetic of shifted primes. The YES branch is
correspondingly unobstructed by anything known — it is a search problem.

## 2026-07-28 — Lemma M2 (proved + verified): the reciprocal-cost infimum is exactly 1

`attempts/route-M-main/COST_INFIMUM.md`, verified by `experiments/M_cost_infimum.py`.
The DOUBLING MAP  D(C) = {0 mod 2} ∪ {(2a_i+1) mod 2n_i}  sends a distinct-moduli covering system
to a distinct-moduli covering system with cost(D(C)) = 1/2 + cost(C)/2. Iterating from the
classical C_0 (cost 4/3) gives systems C_k of cost exactly 1 + (1/3)2^{-k}; all verified by full
mod-lcm sweeps (C_0..C_8, lcm 12..3072, 5..13 classes). With the density lower bound and DMNR this
gives inf = 1, not attained.

CONSEQUENCE FOR 273 (important, changes the search): the natural heuristic "a covering needs
cost ≈ 4/3, so f(L) ≥ 4/3, so lcm ≳ 10^15" is FALSE. Cost can be 1 + ε, so lattices with f(L)
only slightly above 1 are not excluded a priori. Conversely no reciprocal-budget argument can
ever decide the problem — matching PROMPT §3's warning that Σ_{p≥5} 1/(p−1) diverges.
CAVEAT recorded: the doubling map needs 2 and 2n_i admissible; in the E-world "n+1 prime" and
"2n+1 prime" are unrelated, so D does NOT act on E-systems. Lemma M2 is about the unrestricted
problem only and gives no construction inside E.

## 2026-07-28 — main-line computations

- `experiments/M_lattice_scan.py` (exhaustive sieve, L ≤ 10^7): f(L) := Σ_{n|L, n∈E} 1/n.
  * **Minimal L with f(L) > 1 is L = 55440 = 2^4·3^2·5·7·11, f = 6429/6160 ≈ 1.043669** (43 moduli).
    Since every modulus of a qualifying system divides the lcm and Σ1/n_i > 1, this is a rigorous
    lower bound: **the lcm of any covering system with all moduli in E is ≥ 55440**, and must be a
    multiple of one of the 223 divisibility-minimal lattices found below 10^7.
  * Best lattice ≤ 10^7: L = 8648640 = 2^6·3^3·5·7·11·13 with f = 1.157547.
  * 1024 values of L ≤ 10^7 have f(L) > 1.
- **55441 is prime, so 55440 ∈ E itself.** Hence if ℤ/55440 minus the single class 0 can be
  covered by the other admissible divisors, adjoining 0 mod 55440 completes a covering system.
- Recursion pools Q(k) := {e ≥ 2 : ke+1 prime} (the set that must cover ℤ after rescaling a class
  0 mod d, with k = d in the E-world / k = 2d in the H-world). Budgets on [2,400]:
  Q(1) 1.8316, Q(2) 2.8773, Q(4) 2.1141, Q(6) 3.2580, Q(12) 2.4246 — the pools are far richer than
  E itself (the d/φ(d) enrichment), so the difficulty is concentrated at the TOP level.
- Local search (`experiments/M_local.c`, greedy + coordinate descent) at L = 55440 stalls at
  ~7800/55440 ≈ 14% uncovered against an overlap budget of only 2421 residues — strong evidence
  (not proof) that L = 55440 is infeasible. Exact SAT runs on 55440 did not finish within the
  time allotted under heavy CPU contention; rerun needed.
- `experiments/verify_certificate.py` written and tested: independent verifier checking
  admissibility (deterministic trial division, cross-checked against sympy), distinctness, and
  coverage by BOTH a full mod-L sweep and an exact class-elimination argument. Correctly rejects
  a non-covering and a system using moduli 2,3; agrees with itself on the classical covering.

## 2026-07-28 — session start: setup, verified numerics, wave-1 launch

**State for a cold resume.** Problem statement in `PROBLEM.md` (immutable). Route registry in
`ROUTES.md`. Nothing is proved yet beyond the necessary conditions below.

**Verified from scratch (`experiments/e_basics.py`, exact `Fraction` + `sympy.isprime`):**
- E ∩ [4,102] matches the PROMPT list; the claimed non-members 8,14,20,24,26,32,34,38,44,48,50,
  54,56,62,64,68,74,76,80,84,86,90,92,94,98 all verified (n+1 composite).
- 17 smallest elements of E are 4,6,10,12,16,18,22,28,30,36,40,42,46,52,58,60,66 with reciprocal
  sum **160107799/160240080 ≈ 0.99917 < 1**; adding 70 gives ≈ 1.01346 > 1. lcm of the 18 smallest
  = 480720240 = 2⁴·3²·5·7·11·13·23·29. ⟹ any qualifying system has k ≥ 18 and a modulus ≥ 70.
- H ∩ [2,44] matches the PROMPT list; the claimed omissions 4,7,10,12,13,16,17,19,22,24,25,27,28
  verified.
- **B_E(X) = Σ_{n∈E, n≤X} 1/n**: 1.08415 (10²), 1.47111 (10³), 1.75621 (10⁴), 1.97843 (10⁵),
  2.16048 (10⁶), 2.31461 (10⁷). Asymptotically ≈ ln ln X − 0.4654. This slow growth is the
  central quantitative difficulty of the problem.
- **B_H(Y) = 2·B_E(2Y)**: 2.44288 (10²), 3.13109 (10³), 3.65617 (10⁴), 4.07354 (10⁵), 4.41890 (10⁶).

**Enrichment (measured, `e_basics.py`).** The share of the E-budget carried by multiples of d is
≈ 1/φ(d), NOT 1/d: measured share/1/φ(d)/(1/d) = 0.4625/0.5/0.333 (d=3), 0.5046/0.5/0.25 (d=4),
0.2151/0.25/0.2 (d=5), 0.4625/0.5/0.1667 (d=6), 0.0857/0.125/0.0333 (d=30). Reason: n ∈ E with
d | n ⟺ p ≡ 1 (mod d), density 1/φ(d) among primes. So E is substantially *richer* in
highly-divisible moduli than a random even set — a real advantage for any construction.

**Divisor-lattice budgets (`experiments/lchoice.py`, exact divisor enumeration).**
Σ 1/n over n ∈ E dividing L: 1.1057 (L=720720), 1.1294 (2162160), 1.1472 (4324320),
1.1168 (5045040), 1.1579 (10810800), 1.1759 (21621600), 1.2109 (9.08·10⁸), 1.2624 (3.09·10¹⁰),
1.3014 (2.93·10¹²), 1.3692 (4.45·10¹⁵), 1.4345 (1.04·10²⁰), 1.5096 (2.85·10²⁷).
For calibration the classical covering {0(2),0(3),1(4),5(6),7(12)} costs 4/3 ≈ 1.333.
⟹ if a qualifying system needs cost ≈ 4/3 it needs lcm ≳ 10¹⁵. Whether it needs that much is
exactly the question route F is measuring.

**Structural reductions recorded (to be re-proved and audited before any load-bearing use):**
1. *Parity split.* All of E is even, so classes split by residue parity; substituting
   x = 2y + (a mod 2) shows: an E-covering exists ⟺ there are two DISJOINT finite
   M_0, M_1 ⊆ H = {m : 2m+1 prime}, each supporting a distinct-moduli covering of ℤ.
   NOTE for auditing: in H-units each M_j needs Σ 1/m > 1, i.e. Σ_{n∈S_j} 1/n > 1/2 in E-units;
   summing the two gives the ordinary Σ 1/n > 1 — there is NO doubling of the E-budget
   requirement. (I made exactly this slip once during setup; it is corrected here.)
2. *Necessary lcm condition.* Every modulus divides L = lcm, so f(L) := Σ_{n|L, n∈E} 1/n > 1 is
   necessary. Computing the minimal such L bounds the lcm of ANY qualifying system from below.
   Running: `experiments/M_min_lcm.py`.
3. *q-adic fiber condition.* For prime q and q-adic path r, F(r) = Σ_{n : a_n ≡ r mod q^{ν_q(n)}}
   q^{ν_q(n)}/n must be ≥ 1 for EVERY path, while the Haar average of F is exactly Σ 1/n.
   So Σ 1/n > 1 is only the average condition; the covering condition is the min. At q = 2 this
   degenerates to precisely the parity split (every element of E is even).

**Wave-1 routes launched** (8 independent subagents, none told a favoured answer): A SAT search,
B recursive divisor-tree, C halved world H, D obstruction/NO, E literature, F minimum reciprocal
cost, G Selfridge surgery, H minimal-family refutation. Details in `ROUTES.md`.

**Diagnosis line.** Nothing has failed yet; the identified crux is quantitative: the available
reciprocal budget inside any single divisor lattice is barely above 1, so the YES branch needs an
unusually *cheap* covering, and the NO branch needs an obstruction that survives the divergence of
Σ_{p≥5} 1/(p−1). Next: minimal-lcm lemma, then triage wave-1 results.

**Tooling note.** `experiments/cover_dfs.c` (exhaustive "cover the smallest uncovered residue" DFS
with reciprocal-budget pruning) is written but was killed at 300 s on L=720720 with output still
buffered — needs `setbuf(stdout, NULL)` and much stronger pruning before it is useful. Do not
trust it until re-tested.
