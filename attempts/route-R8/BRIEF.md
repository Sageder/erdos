# Route R8 brief — toolbox literature verification (exact statements + ranges)

Read /home/user/erdos/PROBLEM.md first. This route verifies the exact citable forms of
classical tools needed by counting arguments elsewhere in the project. Web search IS allowed
for this route, but ONLY for the standard named results below — never search for anything
about Erdős problem 727 itself, its solvability, or factorial-divisibility problems 727-729.

For each item: find the precise theorem (statement with ALL hypotheses, uniformity ranges,
where published), quote it exactly, give the citation, and assess whether the stated target
form follows. If a target form does NOT follow from literature, say so plainly and give the
strongest available substitute. Write everything to
/home/user/erdos/attempts/route-R8/TOOLBOX.md.

 T1. Smooth numbers in a FIXED arithmetic progression: for fixed u > 1 and fixed modulus q,
     gcd-conditions as needed: #{x < n <= 2x : P(n) <= n^{1/u}, n ≡ a (mod q)} =
     (rho(u)/q + o(1)) x. Need: fixed q version only. (Likely: Tenenbaum's book, or
     Granville's survey "Smooth numbers: computational number theory and beyond".)
 T2. Equidistribution of {N/p mod 1} and of ({N/p}, {N/p^2}, ...) as p runs over primes in
     [P, 2P], N fixed of size P^{c}, 1 < c < 4: discrepancy bounds with power savings
     (Vinogradov-era; also fine if only crude bounds with any o(1) discrepancy exist).
 T3. Weyl-sum equidistribution for quartic monomials: for the polynomial v -> v^4, moduli
     Q = p^t (p prime), v ranging over an interval of length V with Q <= V^{4-delta}:
     bounds of the form |sum_{v ~ V} e(a v^4 / Q)| << V^{1-c(delta)} for (a, Q) with
     controlled gcd; OR equivalent equidistribution of v^4 mod p^t in unions of digit
     cylinders. (Weyl's inequality + standard complete-sum estimates mod p^t; Hua.)
 T4. Complete exponential sums mod p^L: Hua-type bound |sum_{z mod p^L} e(a z^4 / p^L)|
     <= C p^{L(3/4)} (or similar) for p odd, p not dividing a; exact form and constant.
 T5. Selberg/Brun-Titchmarsh upper bound for prime values of (z^2+1)/a: for fixed a with
     a | z^2+1 solvable, an upper bound of expected order, UNIFORM in a up to x^{1-delta},
     for #{z <= x : z^2 ≡ -1 (mod a), (z^2+1)/a prime}: constant tracked explicitly
     (dimension-1 sieve; any explicit constant C_sieve, e.g. 4+o(1), is fine — report it).
 T6. Average of rho_2(a) = #{roots of t^2 ≡ -1 mod a} : Sigma_{a <= x} rho_2(a) ~ c x with
     explicit c, and the partial-sum version Sigma_{A < a <= 2A} rho_2(a)/a.
 T7. The largest-prime-factor distribution (Dickman): P(P(n) > n^beta) -> log(1/beta)
     integral form; also E[#prime factors of n in (n^b1, n^b2)] -> log(b2/b1); and the
     analogue for the prime factors of shifted/quadratic values needed only as UPPER bounds
     via T5/T6-style counting (say what is unconditional).
 T8. Carry/digit Markov chain for doubling in base p (transition matrix ((1/2+1/2p,
     1/2-1/2p),(1/2-1/2p,1/2+1/2p)) on uniform digits): confirm standard large-deviation
     bounds (this may simply be re-proved; note if any published reference exists, e.g. in
     the Erdős-728 writeup arXiv 2601.07421 appendix — a copy is at
     /home/user/erdos/references/aristotle728.txt; methods from it may be used freely).
Return: structured summary — per item: status (citable-as-needed / weaker-than-needed +
substitute / must-prove-inline), citation, exact quoted statement (abbreviated ok), file.
