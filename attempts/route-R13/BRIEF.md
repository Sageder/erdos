# Route R13 brief — anatomy of the consecutive-smooth positive-density proofs

Read /home/user/erdos/PROBLEM.md and /home/user/erdos/attempts/route-R12/LADDER.md
(sections 1, 4.5, 4.6) first. Context: Lemma R‴ (proved, verified) reduces k=2 membership
to: (a) small-prime demands at ℓ ≤ P₀ (class-forceable when small parts bounded), and
(b) the residue condition C_ℓ: ((n+j)/ℓ − 1) mod ℓ ≥ (ℓ−1)/2 at every large prime
ℓ ∥ n+j (j = 1, 2). The missing supply: infinitely many (ideally positive density) n with
n+1, n+2 both having ALL prime factors ≤ n^b (b ≤ 1/2) AND the C_ℓ conditions.
Known (per literature route R11): Hildebrand 1985 (Proc. AMS 95, 517–523, "On a conjecture
of Balog") proves positive lower density of {n : P(n) ∈ (n^a, n^b), P(n+1) ∈ (n^a, n^b)};
Balog–Ruzsa (Cardiff 1995 LMS 237, 55–63, "On an additive property of stable sets")
proves positive density of {n : n and an+c both n^β-smooth}; Heath-Brown 1987
(J. Indian Math. Soc. 52, 39–49, "Consecutive almost-primes") gives a quantitative
machine; Hildebrand 1989 (Mathematika 36, 60–70) has the underlying "stable sets" theory.

Mission: OBTAIN the actual texts of these four papers (WebFetch/WebSearch: AMS Proc. is
open access for old volumes; also search author homepages, archives; degrade gracefully to
detailed secondary accounts if a text is unobtainable — but exhaust options first) and
produce /home/user/erdos/attempts/route-R13/ANATOMY.md answering, per paper:
 1. The exact main statement and the PROOF ARCHITECTURE: constructive family vs
    non-constructive density argument? What are the free parameters (chosen primes,
    CRT classes, intervals, recursion)?
 2. Can the proof tolerate an added congruence n ≡ c₀ (mod Q₀) for a fixed modulus?
    (Where exactly would it enter; what breaks.)
 3. Can it tolerate/produce per-large-prime cofactor conditions of C_ℓ type — i.e. when
    the proof exhibits a large prime factor ℓ of n+j, is the cofactor (n+j)/ℓ free enough
    (equidistributed mod ℓ, or choosable) to impose a positive-proportion residue
    condition? Identify the exact lemma that would need strengthening and its role.
 4. What density/count does the method give, and how do all constants depend on (a, b)?
 5. Frank verdict: for the target
    "positive-density n ≡ c₀ (Q₀) with n+1, n+2 both n^b-smooth-banded and all C_ℓ met"
    — list the NEW lemmas needed, each classified: routine / hard-but-classical / open.
Numerical work is not required, but if you make structural claims about the constructions
(e.g. which n they produce), verify small cases computationally where feasible.
Never search for anything about Erdős problem 727 itself.
Return: structured summary (per-paper architecture + verdict + files).
