# Route R9 brief — per-prime digit dynamics and counting lemmas

Read /home/user/erdos/PROBLEM.md first; it is binding. Work ONLY from PROBLEM.md and this
brief. Do not read NOTES.md, ROUTES.md, or other attempts/ directories.

Task: build the rigorous per-prime counting theory for the membership criterion, as reusable
lemmas with complete proofs. With m = n + k, the criterion is
  n in S_k  <=>  for all p:  nu_p(C(2m,m)) >= nu_p(C(2m,2k)) + nu_p((2k)!)
             <=>  for all p:  kappa_p(m) >= W'_p(m) := nu_p((2m)(2m-1)...(2m-2k+1)),
where kappa_p(m) = #carries when doubling m in base p (Kummer).

Lemma targets (state and prove with full rigor, all constants explicit; verify each
numerically first in this directory):
L1. For each prime p and fixed k, the density of m in [M, 2M] with kappa_p(m) >= W'_p(m)
    (asymptotics as M -> infinity; explicit main term and error). Treat p fixed, p growing
    with M, and the boundary p ~ sqrt(M) regimes separately.
L2. Joint version: for any finite set of primes p_1 < ... < p_r <= P0, the density of m
    satisfying the condition at every p_i simultaneously; prove quantitative independence
    (error terms explicit in P0, M). Identify the largest P0 = P0(M) for which the counting
    stays rigorous (residue classes vs interval length).
L3. Automatic regimes: characterize exactly (with proof) the primes/patterns where the
    condition holds for free: (a) p > 2k with no multiple of p in the top window
    (2n, 2n+2k]; (b) multiples at odd positions 2n+2j-1 (prove forced carries from top-heavy
    residues); (c) any others you find.
L4. Failure regimes: characterize exactly the (p, m) patterns that force failure
    (zero-carry patterns; p | n+j with high beta = log p / log m; quantify thresholds).
L5. The "positive proportion of m pass everything at p <= P0, with spikes excluded" lemma:
    for fixed k and any fixed P0, a positive proportion of m in [M, 2M] satisfy the condition
    at every p <= P0 AND have max_{0<=i<2k} nu_p(2m - i) bounded suitably. Full proof
    (Chernoff/Markov-chain bounds on carry counts are fine — prove what you use).
Deliverables in /home/user/erdos/attempts/route-R9/: LEMMAS.md (statements + proofs),
verify_*.py (numerical verification of each lemma's prediction vs data).
Return: structured summary — lemmas proved (list with status), surprises found, files.
