# Route A — SAT / exact-cover certificate search. Final report.
(Transcribed by the session; scripts: `experiments/A_*`; certificates in `certs/`.)

## Headline
No certificate was found, but the SAT work distilled into an elementary fully-proved obstruction
(Theorem A3) that kills 63 of the 90 possible lcm values ≤ 10⁶ with no search at all.

## PROVED (audited independently by the session — see AUDITS.md audit 5)
- **Lemma A1 (parity split).** Fifth independent derivation; agrees with Lemma M3. Adds the
  bookkeeping: each half's excess X_c := Σ_{M_c} 1/m − 1 satisfies X_0 + X_1 ≤ 2·B_E(L) − 2.
- **★ Lemma A2 (forced overlap) — the workhorse.** For a covering family with modulus set M and
  any T ⊆ M with PAIRWISE COPRIME elements,
      X := Σ_{m∈M} 1/m − 1  ≥  f(T) := Σ_{m∈T} 1/m − 1 + Π_{m∈T}(1 − 1/m).
  *Proof.* g(S) = Σ_{m∈S} 1/m − dens(∪ classes of S) is non-decreasing in S (adding a class of
  modulus m′ raises the sum by 1/m′ and the density by at most 1/m′); g(M) = X since the union is
  ℤ; and for pairwise coprime T the classes are independent by CRT, so dens(∪_T) = 1 − Π(1−1/m)
  EXACTLY, whatever the residues. Hence X = g(M) ≥ g(T) = f(T). ∎
  Values: f({2,3}) = 1/6, f({2,5}) = 1/10, f({3,5}) = 1/15.
- **★ Theorem A3.** If 60 | L and 1 < B_E(L) ≤ 31/30, then no covering system with distinct moduli
  in E has lcm dividing L.
  *Proof.* 60 | L ⟹ 4, 6, 10 | L and all lie in E. B_E(L) − 1 ≤ 1/30 < 1/10, so each of 4, 6, 10
  is FORCED (deleting it leaves reciprocal sum < 1). Their halves 2, 3, 5 are pairwise coprime.
  By A1, X_0 + X_1 ≤ 2B_E(L) − 2 ≤ 1/15 with both X_c > 0 strictly (DMNR), so each X_c < 1/15.
  By A2, two of {2,3,5} in the same half would force X_c ≥ f(pair) ≥ 1/15 — contradiction. So the
  three must lie in three different halves; there are only two. ∎

## VERIFIED
- Sieve over EVERY L (not only smooth ones): **90 values L ≤ 10⁶ have B_E(L) > 1; all are
  divisible by 60; the smallest is 55440.** A3 kills 63, leaving 27 survivors:
  55440, 110880, 166320, 221760, 262080, 277200, 327600, 332640, 388080, 393120, 443520, 498960,
  524160, 554400, 589680, 609840, 655200, 665280, 720720, 776160, 786240, 831600, 887040, 917280,
  942480, 982800, 997920.
  (Reproduced exactly by the session's independent re-implementation.)
- **Half of the problem is easy** — 11 classes with distinct E-moduli covering all even integers:
  (4,0),(6,4),(10,0),(12,6),(18,14),(30,8),(36,2),(40,14),(60,2),(72,26),(180,26).
- Smallest L admitting an H-world covering: **180**. Smallest for the relaxed ("cover ℤ/L except
  one class") version: 18, via (2,1),(3,1),(6,2),(9,3),(18,6).
- **The relaxed problem is not measurably easier**: the smallest L with B_E(L) > (L−1)/L is again
  55440, and A3 applies there too.
- Encoder soundness: 24/24 agreement with an independent exhaustive DFS, 0 disagreements.

## FAILED, and why
- **No E-world instance was ever SAT.** None of the six L in the brief was decided.
- **The SAT ceiling is far lower than expected and it is the SOLVER, not memory.** CaDiCaL got no
  verdict on the smallest possible instance (L = 55440, only 3.7M literals) in > 30 min wall.
  Reason: the UNSAT witness is a *counting* argument, which resolution reproduces only with
  exponential effort. Measured monolithic ceiling ≈ 10⁴–10⁵ residues for UNSAT, not 10⁷.
- The CEGAR-over-parity-splits driver never converged (untested code).
- Dead end recorded: for every L tested, D_E(L) CAN be split into two parts each of reciprocal sum
  > 1/2, so the subset-sum condition adds nothing beyond B_E(L) > 1.

## Route A's recommendation
Push Lemma A2 further rather than enlarging SAT instances: larger pairwise-coprime sets give much
bigger f (e.g. f({2,9,11}) ≈ 0.1061), and the CONDITIONAL form "if T ⊆ M_c then Σ_{M_c} 1/m ≥
1 + f(T)" is strictly stronger than what A3 uses.
