# PROBLEM.md — Erdős Problem 196 (immutable statement of record)

Written once at session start, 2026-07-27. Never edit.

## Statement

**Must every permutation of $\mathbb{N}$ contain a monotone 4-term arithmetic progression
$x_1 < x_2 < x_3 < x_4$?** (erdosproblems.com/196; site statement governs.)

## Conventions (binding)

- $\mathbb{N} = \{1, 2, 3, \dots\}$ (starts at 1). All values and positions are in $\mathbb{N}$.
- A **permutation of $\mathbb{N}$** is a bijection $a : \mathbb{N} \to \mathbb{N}$, viewed as the
  sequence $a(1), a(2), a(3), \dots$. Injectivity AND surjectivity are both part of the definition:
  every natural number occurs exactly once, at a finite position.
- A **monotone 4-term AP** (monotone 4-AP) in $a$ is a choice of positions $i_1 < i_2 < i_3 < i_4$
  and integers $x \ge 1$, $d \ge 1$ such that
  $(a(i_1), a(i_2), a(i_3), a(i_4)) = (x, x+d, x+2d, x+3d)$   [increasing orientation]
  or
  $(a(i_1), a(i_2), a(i_3), a(i_4)) = (x+3d, x+2d, x+d, x)$   [decreasing orientation].
- The AP lives in the **values** (common difference $d \ge 1$ in values); the **positions** are only
  required to be strictly increasing — no pattern required on positions.
- Both orientations count as monotone. $d = 0$ is excluded (impossible for injective $a$ anyway).

## The two branches (exactly one must be fully proved)

**YES**: For every bijection $a : \mathbb{N} \to \mathbb{N}$ there exist positions
$i_1 < i_2 < i_3 < i_4$ and $d \ge 1$ with
$a(i_2) - a(i_1) = a(i_3) - a(i_2) = a(i_4) - a(i_3) = \pm d$ (one common sign).

**NO**: There exists a bijection $a : \mathbb{N} \to \mathbb{N}$ such that for ALL
$i_1 < i_2 < i_3 < i_4$ the quadruple $(a(i_1), \dots, a(i_4))$ is not an AP in either orientation.
A NO proof must separately establish: (i) no monotone 4-AP (exhaustive case analysis over all
$(x, d)$, both orientations); (ii) injectivity and surjectivity; (iii) order type $\omega$ —
every value at a finite position, every position filled.

## Order reformulation (with the order-type lemma, to be proved before use)

Bijections $\mathbb{N} \to \mathbb{N}$ correspond exactly to linear orders $\prec$ on $\mathbb{N}$
with all predecessor sets finite, via $v \prec w \iff a^{-1}(v) < a^{-1}(w)$.
YES $\iff$ for every such $\prec$ there are $x, d \ge 1$ with
$x \prec x+d \prec x+2d \prec x+3d$ or $x+3d \prec x+2d \prec x+d \prec x$.

## Lean cross-check

google-deepmind/formal-conjectures `ErdosProblems/196.lean`:
`erdos_196 : answer(sorry) ↔ ∀ (f : ℕ ≃ ℕ), HasMonotoneAP f 4`.
Lean's ℕ contains 0; equivalent to the site version by conjugating with the shift $n \mapsto n+1$.
Site statement (ℕ starting at 1) governs here.

## Known background assumable with attribution

- **[DEGS77]** (Davis–Entringer–Graham–Simmons 1977): (a) every permutation of ℕ contains a
  monotone 3-term AP; (b) there exists a permutation of ℕ with no monotone 5-term AP.
  Only these two statements are certified; construction internals must be re-derived if needed.
- **Finite avoidance at every length**: for every $N$ the parity recursion $\sigma_N$ gives a
  permutation of $[1..N]$ with no monotone 3-AP (hence no 4-AP). So finite exhaustion can never
  prove YES; any YES proof must genuinely use infinitude.
- **Restriction principle**: values $\{1..M\}$ of a permutation of ℕ, in position order, form a
  permutation of $[1..M]$, and its monotone 4-APs are monotone 4-APs of $a$.
- Toolbox: Szemerédi (4-AP case), van der Waerden, Ramsey, Erdős–Szekeres, König, Behrend,
  digit constructions, compactness — all with hypotheses verified and uniformity tracked.

## Do not drift

Problems 194, 195 ($\mathbb{Z}$-analogue), 197 are DIFFERENT problems. One-sidedness of ℕ is
essential. Monotone = values monotone along increasing positions. APs in values, not positions.
