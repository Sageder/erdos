# What a resolution of Erdős 196 must look like

Derived from the barrier results of this run. This is the practical distillate: if you are
attacking the problem, these are the constraints your argument has to satisfy, and the
shapes of argument that are provably wasted effort. Every item cites the result that
establishes it (see `attempts/core/CORE.md`).

---

## Part A — requirements on an AFFIRMATIVE proof (every permutation has a monotone 4-AP)

**A1. It must use surjectivity, essentially.** Injections avoid even monotone 3-APs
(n ↦ 2ⁿ, by parity). Any argument that never uses exhaustion of ℕ is wrong. Equivalently,
it must use order type ω: every value at a finite position. (PROBLEM.md; Lemma 1.)

**A2. It cannot be a forced-descent / infinite-chain argument.** Every rule of the form
"these positional facts force t before s" produces an edge descending in position. So chains
are finite, and the ≺-minimum a(1) has no out-edge under ANY such rule — it is always a
sink. This closes the whole family: Theorem 16's digraph, route R17's six-rule extension
G*, and any further enrichment. Improving the sink fraction does not help; one sink per
chain suffices. (Theorem 47, subsuming Theorem 44.)

**A3. It cannot be one-point-anchored forcing.** Every supply statement provable from
{4-AP-freeness, order type ω} pins only ONE previously named value, and the adversary
answers each probe at a fresh scale beyond twice the named span, keeping every finite
forcing tree consistent. Proved twice independently (route R5's Generic Escape; re-derived
by an isolated fresh-eyes route). The named exit is a genuine two-point supply lemma; the
natural candidates (through a given pair, centred at, ending at a given value) are all
FALSE as universal statements.

**A4. It cannot rest on displacement / linear profiles.** Two independent reasons. (i) The
compactness lemma quantifies over ALL profiles φ, so killing every linear one leaves
v log v, v^{1+ε}, … untouched. (ii) The same extinction signature appears in the
KNOWN-NEGATIVE case at length 5 — 5-AP-free permutations under pos(v) ≤ 1.25v die at
N = 13, two solvers agreeing — so the signature does not discriminate the branches.
Additionally no unweighted-ledger argument reaches C ≥ 2 (exact triadic evaluation), and the
forcing step coincides with the ledger's demand step, so those are very likely one tool
rather than two — the auditor downgraded that last point from theorem to remark, so treat it
as strong guidance, not a barrier. (Remarks 17, 27; Theorem 46 as corrected.)

**A5. It cannot rest on shallow/prefix criteria.** The FIN-type statements are dead at all
reachable scales: the minimum achievable position of the first L values stays exactly L for
L ≤ 20, N ≤ 128, and prefix bounds stay satisfiable to N = 355. (Lemmas 7, 7b; measured.)

**A6. Increasing-only arguments cap at C = 3.** The triadic reversed-block permutation has
pos(v) ≤ 3v−1 and NO increasing monotone 4-AP. So any method that never engages the
decreasing orientation cannot pass that constant. (Theorem 14.)

**A7. It must not derive an infinite arithmetic progression from a density hypothesis.**
That is false, and it is an expected error here: Szemerédi and Roth give FINITE progressions
in positive-density sets. An earlier route in this run was caught making exactly this step.

**A8. It must survive the vacuity test.** Ask explicitly of every claimed equivalence
whether it is P ⟺ P, and of every claimed optimum whether a trivial construction attains it.
THREE separate results in this run failed this — including one of my own. (Remark 31;
Correction to Theorem 16(c); route R17's audited biconditional.)

**What is available to build on.** The record set of a counterexample is 3-AP-free, and so
is the record set of EVERY affine sub-copy and tail — an infinite coupled family of
Roth-critical sets inside one order (Lemmas 13, 24). Records sit early (position ≤ value,
and each record at position ≤ previous record's value + 1, Lemma 43) while grounded values
sit late. Along every progression at every scale the descent word avoids 000 and 111
(Lemma 11). The known obstacle to using the record family: any single record set may be
arbitrarily sparse, so there is no density lower bound to play against Roth — a
contradiction must come from the COUPLING between different progressions.

---

## Part B — requirements on a NEGATIVE proof (an explicit counterexample)

**B1. Three separate obligations, all needed.** No monotone 4-AP in either orientation;
bijectivity; and order type ω — every value at a finite position, every position filled.
Constructions that satisfy the first two but have some element with infinitely many
predecessors (odds-then-evens and every block limit) resolve nothing. (PROBLEM.md; Lemma 1.)

**B2. It cannot be a digit comparator.** Comparing values at their first differing base-b
digit kills every monotone 4-AP but forces infinite predecessor classes; the reverse
priority gives order type ω but is a contiguous block layout, already dead. Truncation
escapes neither, since an AP with terms below v has critical level at most log_b v.
(Remark 20.)

**B3. It cannot use a congruence-determined delay.** If any level set of the delay is a
union of residue classes, the delay is constant on a full progression, that progression is
tame, and the architecture has linear displacement there. This retires ρ(v_p(v)) for every
prime, shifted variants, every function of v mod m, and every Boolean combination.
(Propositions 29, 30.)

**B4. It cannot be an in-order geometric block layout at ratio 3 or 4, nor a bounded-lag
interleaving. SCOPE (Proposition 49): this constrains only permutations WITH an infinite
cut sequence, and avoiders are overwhelmingly indecomposable — 78.9% of the avoiders of
[1..9] have no proper cut point, the standard parity construction has essentially none, and
solver-found avoiders at N = 200–400 have none. So B4 is a real theorem about a THIN
subfamily and is much weaker evidence against the negative branch than its provenance
suggests.** Established by SAT over construction stages plus König, so the finite UNSAT
results are impossibility theorems quantified over ALL within-block gadgets. Minimal
infeasible cut-set {8, 26, 80}; the lag-2 interleaving dies at stage 7. (Route R1; route
R18 re-derived the ratio-3 and ratio-4 deaths faster via block localization.)

**B5. It cannot reuse the length-5 mechanism.** That construction's contradiction is a
TWO-PAIR parity argument, and at any ratio ≥ 3 a 4-AP's last three terms split as
pair + singleton — four terms never supply two pairs. Nor can the block parity be replaced
by an arithmetic sign: such rules are not transitive (exhaustive classification — only 16 of
256 candidates transitive, none genuinely value-dependent), so the sign must be constant on
a convex partition, i.e. carried by blocks. (Remarks 23, 25; Theorem 21.)

**B6. It must have superlinear displacement.** Certified extinction of pos(v) ≤ Cv at
C = 1.25, 1.5, 1.75, 2 (thresholds N* = 4, 15, 31, 74). Verification standard differs by
entry: C = 1.5 and 1.75 agree between exhaustive extension-tree enumeration and SAT;
C = 2's threshold was located by route R18 and independently re-verified here (SAT at
N = 70, 72 and UNSAT at N = 74, cadical and glucose agreeing on an eager encoding). Also the profile ⌈0.5·v·log₂ 2v⌉ dies at N = 130, so "Θ(v log v)" is not a
target either. (Theorem 12; Remarks 17, 28.)

**B7. It must come with a PROOF, not a verification.** From the certified extinction law
N*(C) ≈ 4·exp(3.89(C−1.25)), a design whose progression-restriction has displacement
constant C cannot die before N ≈ 3.6·10³ at C = 3, 9·10⁶ at C = 5, 4·10⁸ at C = 6. Checking a
candidate to 10⁴–10⁵ therefore certifies NOTHING in the regime where the surviving
candidates live. (Remark 27.)

**B8. Satisfying the coarse class condition is not enough.** "No strictly monotone class
sequence along any 4-AP" is necessary but far from sufficient: values sharing a class are
ordered freely and those orders must themselves avoid monotone 4-APs. Aperiodic delays
meeting the coarse condition were found and are UNSAT over ALL within-class orders at
N = 150, 260, 340. Any construction must clear the realizability layer too. (Proposition 41.)

**Where the negative branch is still alive.** Accelerating non-geometric cut sequences
(feasible at depth 5, e.g. [1, 2, 4, 10, 90]) — but they sit inside the B7 blind spot, so
only an explicit rule with a proof can settle them. And unbounded-delay class architectures,
for the same reason.

---

## Part C — the single most useful methodological rule

Every substantive error in this run — SEVEN of them, all recorded, the last found by an
adversarial auditor in a table I had copied into the core file — had one root cause:
**reading finite or partial evidence as though it settled an asymptotic statement.** Before
believing any claim here, ask: does this finite computation actually bound the infinite
object, or only the family it happens to quantify over? The certified extinction law (B7)
makes that question quantitative, and it is usually the answer.

A second rule, learned the same way: **a single UNSAT witnesses extinction at that size,
never minimality.** Minimality requires the SAT point immediately below. I published a table
headed "minimal N" whose last entry was merely the first size I happened to test — the true
value was 74, not 90. Report the bracketing SAT/UNSAT pair, not one endpoint.
