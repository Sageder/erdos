# Route R3 brief — Balakran dissection and upgrade

Read /home/user/erdos/PROBLEM.md first; it is binding. Work ONLY from PROBLEM.md and this
brief. Do not read NOTES.md, ROUTES.md, or other attempts/ directories.

Task: dissect the k=1 case to locate exactly what breaks at k=2.

1. Balakran's theorem: infinitely many n with ((n+1)!)^2 | (2n)!. Reconstruct an explicit
   construction proving it (you may re-derive it yourself from scratch; that is encouraged).
   Hint from data: the first solutions n+1 = m are 6, 15, 28, 45, 66, 91, 153 — many are
   hexagonal numbers j(2j-1) — but 42, 77, 110, 126, 140, 156, 170 are not; 120 is hexagonal
   but absent. Find a clean infinite family INSIDE S_1 with a complete valuation proof
   (every prime p, using the per-prime criterion of PROBLEM.md).
2. Then attempt the SAME construction for k=2 and document precisely which per-prime
   conditions break, and why. Classify: which primes fail (size ranges, digit patterns), and
   whether any modification (congruence conditions, different parametrization) repairs them.
3. Deliverable files in /home/user/erdos/attempts/route-R3/:
   - FAMILY.md: the k=1 family + full proof; every claimed member verified numerically
     (write experiments as needed in this directory, using python3 with sympy).
   - BREAKAGE.md: the exact k=2 failure analysis.
4. Numerically verify every intermediate claim before investing proof effort. Use exact
   integer arithmetic. The membership criterion (digit form) is in PROBLEM.md; reimplement it
   yourself (do not import from experiments/) and sanity-check against the PROBLEM.md tables.

Return (as your final message): a structured summary — family found (yes/no + definition),
proof status (complete/gaps: list), k=2 breakage mechanism (precise), most promising repair
idea, files written.
