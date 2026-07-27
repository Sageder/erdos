# Route R2 brief — small-prime carry machinery for fixed k (Lemma SP)

Read /home/user/erdos/PROBLEM.md first; it is binding. Work ONLY from PROBLEM.md, this brief,
and the one licensed background paper described below. Do not read NOTES.md, ROUTES.md, or
other attempts/ directories.

Licensed background (methods only; import techniques, never any conclusion about problem
727): arXiv 2601.07421 (writeup of the Erdős-728 resolution). A local text copy is at
/tmp/claude-0/-home-user-erdos/49f04ef0-a63d-55e0-b5d7-ad8e910eb3fe/scratchpad/aristotle728.txt
Its Lemmas 6-15 develop: forced carries from large digits, Chernoff bounds for digit/carry
counts, residue-class counting in [M, 2M], spike exclusion. Port this machinery to 727.

Task: state and prove, with full rigor and explicit constants, the following building-block
lemma for fixed k (call it Lemma SP), in the strongest true form you can:

  Lemma SP (target shape). Fix k >= 2. There is a function P(M) -> infinity (as large as the
  method allows, e.g. exp(c sqrt(log M)) or a power of log M) and a constant delta_k > 0 such
  that for all large M, at least delta_k * M integers m in [M, 2M] satisfy BOTH:
   (i) for EVERY prime p <= P(M):  kappa_p(m) >= nu_p((2m)(2m-1)...(2m-2k+1))  [the 727
       criterion at p, see PROBLEM.md product form], and
   (ii) no spike: max_{0 <= i < 2k} nu_p(2m - i) <= (bound you choose) for every p <= P(M).
  Moreover quantify delta_k and, if possible, make delta_k -> 1 (density 1) when (i) is only
  required for p <= P0 fixed. Also prove the variant where m is additionally restricted to
  any fixed residue class a mod q0 with q0 <= M^{1/10} coprime conditions as needed (this
  matters for later combination with other constraints — make the lemma as
  intersection-friendly as you can: state it as "all but o(M) [or (1-delta)M] of m in ANY
  arithmetic progression of modulus <= Q(M) in [M, 2M]" if you can prove that).

Notes: (a) the criterion at p includes the contribution nu_p((2k)!) — the demand at p <= 2k
is kappa_p >= roughly 2k/(p-1) + spikes, NOT just the spike part; design the digit conditions
accordingly (depth L_p large enough to force that many carries). (b) p = 2: kappa_2(m) =
s_2(m) (prove it). (c) Verify numerically (scripts in this directory) the exact criterion
and your digit-condition implications before proving; then verify the final lemma's
prediction on data (e.g. k=3, P0=13: measure the density and compare with your delta_k).

Deliverables in /home/user/erdos/attempts/route-R2/: LEMMA_SP.md (statement + full proof +
explicit constants), verify_sp.py (numerics).
Return: structured summary — strongest lemma form proved, P(M) reached, density achieved,
AP-restricted version status, files written.
