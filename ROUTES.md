# ROUTES.md — route registry (Erdős 289)

Format: id | mathematical family | status | outcome / lemma targets.
Last updated 2026-07-28. See NOTES.md for the running log and PROBLEM.md for conventions.

## Established (proved, independently verified)

- **BASE | exhaustive certificate search** | COMPLETE |
  `experiments/csearch.c`, `csearch2.c`, `csearch3.c` (exact integer arithmetic over
  L = lcm(pruned universe); endgame table; p-adic pooled prune). Results:
  **no legal U with max(U) ≤ 84**; the minimum is exactly **85**, with exactly 4 solutions.
  315 solutions verified with max(U) ≤ 130. ⇒ **P(k) TRUE for k = 7,…,18**, all
  certificates re-verified by an independent script (`experiments/verify.py`).
- **C | p-adic obstruction hunt (NO branch)** | CLOSED BY REFUTATION |
  `attempts/route-C/`. RULE A (strengthening of the two-attainer rule): if
  Σ1/n = q, e = max ν_p(n) > −ν_p(q), then Σ m_n^{-1} ≡ 0 (mod p) over the top-level
  attainers. RULE B: legality. The A+B fixpoint of [2,N] is EMPTY for all N ≤ 76 —
  a millisecond proof replacing a 9·10⁹-node DFS. Every candidate obstruction O1–O9 is
  refuted; only O10 survives (max(U) and max(U)−1 are never prime), which constrains
  the top element, not existence. Honest local-global heuristic with EXACTLY computed
  local densities predicts #solutions ≈ e^{cN} → ∞. **The NO branch is dead.**

## Blocked routes (with diagnosis)

- **A′ | atom split 1/a+1/(a+1) = 1/c+1/(c+1)+1/d+1/(d+1)** | BLOCKED: no solutions |
  exhaustive for a ≤ 400, c ≥ a+2, d ≥ c+2 (`experiments/atom_split.py`). Kills the
  simplest "+1 block" move.
- **A″ | equal-sum blocks H(a,b) = H(c,d)** | BLOCKED: block sums are injective |
  no collision for any two blocks with elements ≤ 3000 (`experiments/collide.c`,
  2.84·10⁶ blocks, two independent 62-bit fingerprints). Kills "replace a block by a
  longer block of the same sum", which would have raised capacity at fixed run count.
- **A‴ | unit fraction as a single block, 1/n = H(c,d)** | BLOCKED: none |
  no solution for n ≤ 60 with c ≤ 2·10⁵ (`experiments/two_to_block.c`).
- **DBL | capacity-doubling by atom recolouring** | BLOCKED: BALANCE unsolvable |
  For a set V, D_σ(V) = ∪ atoms ({2n,2n+1} or {2n−1,2n}) is automatically legal with
  cap = |V| and run count = #runs(V) + #proper prefixes; admissible colourings are exactly
  PREFIX colourings of each run of V. Σ is preserved iff
  Σ_j (1/(2u_j−1) − 1/(2c_j+1)) = Σ_{n∈V} 1/(2n(2n+1))   (BALANCE),
  using 2/(4n²−1) = 1/(2n−1) − 1/(2n+1) (telescoping). Exhaustive over all admissible
  colourings of the known solutions: no solution (`experiments/doubling.py`). Diagnosis:
  only ∏(L_i+1) ≈ 3^r colourings against a target with an lcm-sized denominator — far
  too little entropy. Reopen only with a richer per-index gadget menu.
- **TOP | long top run** | BLOCKED BY A PROOF | the top run [c,N] of any solution must
  satisfy c > N/2 and be prime-free (a prime p in it needs a second multiple ≥ 2p > N).
  Hence its length is at most the maximal prime gap below N: capacity cannot be obtained
  from one long run at the top. Corollary: 2-run solutions are impossible, so P(2) is
  almost certainly false; consistent with P(k) first holding at k = 7.

## Active

- **E | the CRUX: scaling of representability** | ACTIVE (subagent running) |
  > (CRUX) for which ρ > 0 and T is ρ the sum of a legal block system with all elements ≥ T?
  Every mechanism examined reduces to this. Known: 1/2 and 1/3 ARE legal block sums
  (certificates verified); 1/4, 1/6 are not inside [2,120]. What is needed is
  representability *arbitrarily far out*, which would make every gadget iterable.
- **A | algebraic identities / pending-fraction calculus** | ACTIVE (subagent).
- **B | alternative search technology (MITM/CP-SAT/PB)** | ACTIVE (subagent).
- **D | structure theory of block sums and their sumsets** | ACTIVE (subagent).

## Swap gadgets (data, verified)

Rationals with legal representations of DIFFERENT block counts exist, e.g.
397/1820 = {13,14}{39,40}{104,105} (3 blocks) = {17,18}{34,35}{84,85}{90,91} (4 blocks);
117 such pairs extracted from the 152-solution corpus. A "+1 block" move therefore exists
in principle; what is missing is a version whose *output* can be placed arbitrarily far
out, so that it can be iterated. That is exactly the CRUX.

## Status

The NO branch is closed. The YES branch is reduced to a single analytic statement (CRUX),
which is the block analogue of Egyptian-fraction representability with denominators in a
short interval. No external theorem can be used here: the session's egress policy blocks
arXiv/EuDML, so nothing can be quoted with hypotheses verified.
