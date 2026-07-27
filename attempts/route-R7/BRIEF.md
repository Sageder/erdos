# Route R7 brief — NO-side obstruction hunting

Read /home/user/erdos/PROBLEM.md first; it is binding. Work ONLY from PROBLEM.md and this
brief. Do not read NOTES.md, ROUTES.md, or other attempts/ directories.

Task: attempt to prove the NO branch — that for some fixed k_0 >= 2, S_{k_0} is finite —
or rigorously delimit why such obstructions fail.

Directions to try (expand as needed):
1. Weight/counting arguments: sum the per-prime deficit inequality over primes:
   Sigma_p (p-1)(c_p - b_p) vs global digit identities (e.g. Sigma_p over relevant ranges of
   2s_p(n+k) - s_p(2n) has closed forms/averages). Look for an incompatibility for large k.
2. The window obstruction: every n in S_k (n > 2k^2) needs n+1..n+k all sqrt(2n)-smooth.
   Combined with the digit conditions at mid primes, does some counting argument
   (e.g. valuations forced by k consecutive smooth numbers vs carries available in doubling
   n+k) become contradictory for large fixed k? Make this quantitative.
3. Anti-concentration: the conditions at different primes p in (2k, sqrt(2n)] each exclude
   certain residue/digit patterns; is the total excluded measure provably >= 1 for large k
   uniformly in n (which would prove finiteness)? Compute exactly what total "measure" the
   known-necessary conditions consume as k grows.
4. If (as you may find) every obstruction attempt fails structurally, write a rigorous
   delimitation: exactly which quantitative barrier prevents an eventual-obstruction proof
   (e.g. a construction showing the conditions are simultaneously satisfiable with positive
   measure for every k — this would be major YES-side progress, record it carefully).

Constraints from PROBLEM.md: any claimed obstruction must NOT exclude the verified members
208, 458, 987 in S_2, 3475 in S_3, 8174 in S_4. Test every intermediate claim numerically
(python3 + sympy, exact arithmetic, scripts in this directory).

Deliverable files in /home/user/erdos/attempts/route-R7/:
- OBSTRUCTION.md: the strongest NO-side statement you can prove in full, or the precise
  delimitation of why finiteness proofs are blocked, with proofs.
Return: structured summary — obstruction found (yes/no + statement), what was proved
rigorously, what is heuristic, files written.
