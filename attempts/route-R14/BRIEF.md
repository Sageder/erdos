# Route R14 brief — L4a and the road to L4 (the re-scoped k=2 wall)

Read `/home/user/erdos/PROBLEM.md` first (binding). Then read, as established context (all
proved and audited in this project — do not re-derive unless you doubt them):
- `/home/user/erdos/MIRROR.md` §§1–4 (digit trichotomy; the exact per-prime condition);
- `/home/user/erdos/attempts/route-R12/LADDER.md` §4.5 (Lemma R‴, and remark (iii): the
  congruence C_ℓ is SUFFICIENT ONLY — higher-digit carries count too);
- `/home/user/erdos/attempts/route-R13/ANATOMY.md` (findings L0–L6; this brief continues it).

## Established framing

For `k = 2`, `n` large, `P₀ = 4`: `n ∈ S_2` iff the small-prime demands hold at `ℓ ≤ P₀` and,
at every prime `ℓ > P₀` with `ℓ^J ∥ (n+j)` (`j ∈ {1,2}`), `κ_ℓ(n) ≥ 2J`, where `κ_ℓ` counts
carries in `n + n` base `ℓ`. For `ℓ ∥ n+j` this is: writing `n = ℓ(W−1) + (ℓ−j)` with
`W = (n+j)/ℓ`, digit 0 always carries, so the condition is that doubling `W−1` base `ℓ` with
carry-in 1 produces at least one carry — failure means `W−1` is "digit-poor" base `ℓ`
(all digits `< ℓ/2`, with the position-0 digit `< (ℓ−1)/2`), an event of density `≈ 2^{−D}`,
`D ≈ log n / log ℓ`.

Supply (theorem, verified from the source): for every `b > 0` there is positive lower density
of `n` with `n+1, n+2` both `n^b`-smooth (Hildebrand 1985 / Balog's conjecture applied to the
stable set `{P(m) ≤ m^b}`). Congruence-restricted version (L1) is assessed as
hard-but-classical and essentially available from Tao–Teräväinen arXiv:2512.01739 Thm 3.1 and
the proof of its Thm 1.8 (the AP restriction `1_{n≡c₀ (mod Q₀)}` is already in the statement).

## Targets, in priority order

**T1 (L4a — the concrete first target).** Prove: there is `b > 0` and `δ > 0` such that, for
`x` large, at least `δ · #{smooth pairs ≤ x}` of the `n ≤ x` with `n+1, n+2` both `n^b`-smooth
satisfy the exact carry condition at the **largest prime factor of `n+1`**. Equivalently, bound
from above the count of smooth pairs whose largest-prime cofactor is digit-poor. Natural inputs:
equidistribution of smooth numbers in arithmetic progressions to modulus `ℓ ≤ x^b` (Fouvry–
Tenenbaum; Harman; Drappeau; Soundararajan; Granville's survey), noting `ℓ² ≤ x^{2b} ≪ x^{1/2}`
so the moduli are well inside Bombieri–Vinogradov range on average. The genuine difficulties to
confront, not paper over: (i) the modulus is a *function of n*; (ii) the digit-poor condition is
a union of `≈ ℓ^{D}2^{−D}` residue classes mod `ℓ^{D}`, not a single class — so what is needed
is equidistribution of smooth numbers in *unions of classes to a large power of `ℓ`*, or an
equivalent Fourier/large-sieve treatment; (iii) the second neighbour `n+2` must remain smooth,
which couples the two conditions.

**T2 (toward L4).** With T1 in hand (or conditionally on it), determine exactly what is needed
to run the same bound at *every* large prime factor simultaneously and conclude by a first
moment inside the smooth set. Quantify: for which `b` is
`E[#failures | n+1, n+2 both n^b-smooth] < 1`? Measure this directly (it is cheap) and compare
with the union bound your T1 method would give. If the measured expectation is `< 1` for some
explicit `b`, state precisely the equidistribution statement whose truth would complete a proof
that `S_2` is infinite, with all quantifiers and uniformities explicit.

**T3 (honest boundary).** Say plainly which of T1/T2 you actually proved, which are conditional,
and what the first genuinely open input is. A conditional theorem is fine and valuable **provided
it is labelled conditional**; per PROBLEM.md a reduction to an unproved statement of comparable
strength does NOT count as resolving anything, so do not present one as a resolution.

## Discipline

- Numerically falsify before proving. python3 + sympy, exact integer arithmetic; scripts and
  outputs in `/home/user/erdos/attempts/route-R14/`.
- Every constant explicit; every "sufficiently large" quantified; track uniformity in `b`, `ℓ`, `x`.
- Web search is allowed ONLY for standard named theorems (smooth numbers in progressions, large
  sieve, BV-type results, Tao–Teräväinen/Teräväinen correlation theorems). NEVER search for
  Erdős problem 727 or its solvability.
- Deliverable: `/home/user/erdos/attempts/route-R14/L4A.md` — statements, proofs, explicit
  conditional dependencies, and the measured tables backing every heuristic.

Return: a structured summary — what is proved unconditionally, what is conditional and on what,
the measured `E[#failures]` table by `b`, and the precise first open input.
