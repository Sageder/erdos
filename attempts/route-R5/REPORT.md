# REPORT — Route R5 (YES-side Ramsey/pigeonhole bootstrap from forced 3-APs)

## Verdict

**Problem 196 is NOT resolved by this route in this session.** No proof of YES, no
candidate proof. What the route produced, all rigorously proved and machine-audited:

1. A complete self-contained proof of the 3-AP forcing theorem, in a **stronger form
   than DEGS77(a)**: every permutation of $\mathbb{N}$ has an *increasing* 3-AP
   *starting at position 1*; and the **anchored supply theorem**: every position
   anchors an increasing 3-AP with first term the value there, with step divisible by
   any prescribed modulus — plus a quantitative ray-hitting refinement
   (`proof_3ap.md`, stress-tested by `stress_3ap.py`).
2. A suite of 19 structural lemmas for hypothetical 4-AP-free permutations — 14
   finitely-stated blocking/interaction lemmas (incl. orientation duals), 3
   minimality lemmas (M0–M2), and 2 supply-driven theorems (top-anchor gap L9,
   staircase L10) — each proved, and each finitely-stated one verified against **all 12,569,396 monotone-4-AP-free
   permutations of $[1..N]$, $N\le11$** with zero failures
   (`lemmas_4apfree.md`, `verify_lemmas.py`, `verify_minimality.py`).
3. An honest contradiction hunt: a SAT-based forcing-cascade solver over order windows
   with well-ordering extractions (minimal-top-position, minimal-step, minimal-top-
   value), plus a two-player game formalization of the cascade with a **proved
   impossibility result** (Generic Escape, below) explaining *exactly* why every
   forcing tree built from the currently provable supply lemmas stalls.

The exact obstacle is identified and proved, not just observed (§4).

---

## 1. The engine (what is proved as supply)

Quantifier-audited summary of `proof_3ap.md`:

- **Thm 1.** Every permutation of $\mathbb{N}$ has an increasing 3-AP with first term
  $a(1)$. (Three-line doubling-orbit descent; surjectivity and order type $\omega$
  each used exactly once, at certified spots; $n\mapsto2^n$ and parity $\sigma_N$
  machine-certify that neither hypothesis can be dropped.)
- **Thm 2 (anchored supply).** For every position $s$ and modulus $m$ there is
  $e\in m\mathbb{N}$ with $(a(s),a(s)+e,a(s)+2e)$ increasing from position $s$.
- **Thm 2′.** All but an explicitly bounded finite set of doubling rays from each
  anchor contain such a step; hence infinitely many steps per anchor per modulus.
- **Cor 2.1.** Supply localizes into every residue class beyond every position.

The **adversary chooses which** step $e$; supply pins only ONE previously named value
(the anchor, which is the 3-AP's *first* term). Middle-pinned, end-pinned and
two-point-pinned supplies are all FALSE (counterexamples in `proof_3ap.md` §Quantifier
discipline). Decreasing 3-APs are not forced at all (identity permutation).

## 2. The cascade (what is forced around each supplied 3-AP)

In a 4-AP-free permutation, around every increasing 3-AP $(x,x+d,x+2d)$ at positions
$i<j<k$: $P(x+3d)<k$ (L1) and $P(x-d)>i$ if $x>d$ (L2); no shifted/end/doubled
continuations (L4a, L4b, L5, L8); the conditional 2d-cascade (L6, L7); the
$k$-minimal extraction adds M0–M2. Iterating supply + L1/L5 up the tops yields the
**staircase theorem** (L10): from every value, an infinite chain of increasing 3-APs
with step ratios $\ge3$, strictly later tops, and a planted inversion
$P(T_i+f_i)<P(T_i)$ at every rung. This is the furthest the cascade provably goes.

## 3. The contradiction hunt (machine campaign; all quantifiers tracked)

**Solver model** (`solver_minimal.py`, encoding self-validated against literal
enumeration of linear orders, `game_anchor.py` G1): unknown = linear order of a finite
window of values around a hypothetical minimal increasing 3-AP; constraints = exactly
the valid consequences: 4-AP blocking inside the window (universally valid), the base
triple increasing (choice), and the chosen well-ordering extraction (M0 for minimal
top position; minimal step; minimal top value), each valid for the corresponding
extraction. Windows: $d$-grids $x+md$ (valid for every $d$ simultaneously), integer
intervals for concrete $d\in\{1,2,3\}$, and absolute windows $[1..W]$ pinning $(x,d)$
concretely (boundary effects included, no existence side conditions).

**Results.**

- Every configuration is **SAT** — grid windows to $m\le16$, intervals to 21 values,
  absolute windows $W\le13$ over all $(x,d)$ (0 UNSAT out of all cases). No finite
  unsatisfiable subsystem exists at these sizes.
- **Backbone is exactly the blocking lemmas**: the complete set of order relations
  forced by [blocking + $k$-minimality (+ step-/top-value-minimality)] beyond the base
  triple is $\{P(x+3d)<P(x+2d)\}$, plus $\{P(x)<P(x-d)\}$ when negative offsets are
  assumed to exist. Nothing else is pairwise forced, at any tested size.
- **Joint exclusions** beyond the backbone exist and were completely mapped at the
  $(P(x-d),P(x+3d))$ and $(P(x\pm3d))$ granularity (`probe_cases.py`): they are
  precisely the instances of M0 (e.g. M1, M2 in `lemmas_4apfree.md`) — each was then
  re-derived by hand and machine-verified on all finite avoiders $N\le10$.
- **Exactness**: every placement cell that the SAT model allows is *realized* by an
  actual finite avoider's $k$-minimal triple (realization census,
  `verify_minimality.py`). So at this granularity the solver's adversary freedom is
  not an artifact: real avoiders exercise all of it.

**Why no finite subsystem can be UNSAT without an extraction:** the parity permutation
$\sigma_N$ has no monotone 3-AP at all, hence satisfies every consequence of
4-AP-freeness alone; only constraints that *assert the presence* of an increasing 3-AP
(supply/extraction) can ever create tension. This is why the campaign centred on
minimality extractions, which are exactly the finite traces of "increasing 3-APs
exist + positions are well-ordered".

## 4. The game, and the exact obstacle (proved)

**Anchored-supply game.** Position: a finite set $X$ of named values with a constraint
store $C$ (order facts and blocked 4-APs accumulated so far), consistent in the sense
that some linear order of $X$ satisfies $C$ and has no monotone 4-AP among value-APs
inside $X$. Prover move: name an anchor $u\in X$ and modulus $m$. Adversary reply: a
step $e\in m\mathbb{N}$; the store gains $P(u)<P(u+e)<P(u+2e)$ (supply), $P(u+3e)<
P(u+2e)$ (L1) and, when $u-e\ge1$ is guaranteed, $P(u-e)>P(u)$ (L2), with
$u\pm e,u+2e,u+3e$ added to $X$. Prover wins if the store becomes inconsistent. A YES
proof by forcing tree of this kind = a Prover strategy winning against **every**
adversary in finitely many rounds.

**Proposition (Generic Escape).** *The Adversary always survives: from any consistent
position, for any Prover move $(u,m)$, every step $e=gm>2\cdot(\max X-\min X)$ gives a
consistent successor position. Hence Prover has no winning strategy at any finite
depth, even if the store also carries the $k$-minimality constraints M0.*

*Proof.* Let $D=\max X-\min X$ and $e>2D$. (i) *AP disjointness*: a 3-term value-AP
with two terms in $X$ and one new term is impossible — the new terms
$n_1=u+e,n_2=u+2e,n_3=u+3e$ all exceed $\max X+D$, so a new term completing an AP over
two old terms $a<b$ would equal $2b-a\le\max X+D$; and an AP with one old term $a$ and
two new terms forces $a=n_i-e$ or $a=n_i-2e$, giving $a=u$ (the supplied AP
$(u,n_1,n_2)$) or $a<\min X$. Consequently the only value-APs inside $X\cup\{n_1,n_2,
n_3\}$ (and $n_0=u-e<\min X$ if it exists) meeting both old and new values are
$(u,n_1,n_2)$, $(n_0,u,n_1)$, $(n_0,n_1,n_3)$, and the 4-APs $(n_0,u,n_1,n_2)$,
$(u,n_1,n_2,n_3)$. (ii) *Extension*: take a model of the current store and append, at
the far position end, $n_0$, then $n_1$, then $n_3$, then $n_2$. All supply/blocking
facts of the reply hold by construction; each of the finitely many new mixed APs is
checked non-monotone: $(n_0,u,n_1,n_2)$ fails increasing at $P(n_0)>P(u)$ and
decreasing at $P(n_1)>P(u)$; $(u,n_1,n_2,n_3)$ fails increasing at $P(n_3)<P(n_2)$
and decreasing at $P(n_1)>P(u)$; old APs are untouched. (iii) *M0-compatibility*: all
new increasing triples end at appended positions, after every old position, in
particular not before $k$. $\blacksquare$

(Machine sanity check: 200 random 6-round generic games stay SAT — `game_anchor.py`
G4. Local sharpness of the small-$g$ exclusions: at the top of a 3-AP in its own
modulus, $g\in\{1,2\}$ are UNSAT and $g=3$ is SAT — G2, matching L9.)

**The exact combinatorial obstacle, stated precisely.** Every supply statement this
route can prove (Thm 1, Thm 2, Thm 2′, Cor 2.1, L9, L10) pins only **one previously
named value per application** — the anchor, always as *first* term — while the
adversary retains the choice of step. The Generic Escape Proposition proves that
one-point-pinned supply + all blocking/minimality constraints can never produce a
finite inconsistency: the adversary answers every probe at a fresh scale
$>2\times$ the named span, and the new gadget interacts with the past only through
the anchor. The cascade therefore *provably* cannot close by itself. To break the
barrier one needs either
(a) a **two-point supply lemma** — some provable statement forcing a monotone
configuration through *two* adversary-independent named values (the natural
candidates — through a given pair, centred/ending at a given value — are all false as
universal statements); or
(b) a **globally quantitative argument** that plays infinitely many supplies at once
against order type $\omega$ / surjectivity (the staircase's infinitely many planted
inversions and the escape gadgets' unbounded scale growth both consume "room" in the
permutation; nothing proved here yet turns that into a contradiction — this is where
R5 hands off to R6-style density/exhaustion pressure).

## 5. Files

| file | content |
|---|---|
| `proof_3ap.md` | Deliverable 1: Theorems 1, 2, 2′, Cor 2.1, usage audit |
| `stress_3ap.py` | T1–T5 machine stress tests of the proof (all PASS) |
| `lemmas_4apfree.md` | Deliverable 2: L1–L10, M0–M2 with proofs + verification table |
| `enum_avoiders.py` | exact avoider enumerator (cross-validated two ways) |
| `verify_lemmas.py` | lemma verification on all avoiders $N\le11$ (0 fails) |
| `verify_minimality.py` | M1/M2 verification + realization census (0 fails, census exact) |
| `solver_minimal.py` | order-window SAT solver, extraction constraint menu, backbones |
| `probe_cases.py` | joint-placement probes (found M1/M2 exclusions; nothing further) |
| `game_anchor.py` | game experiments G1–G4 (encoding self-test, gap sharpness, generic escape demo) |
| `verify_lemmas_N11.log`, `bigger_windows.log` | long-run logs |

## 6. Next steps (ranked)

1. **Hunt a two-point supply.** The most promising shape: for a *pair* $(u,w)$ with
   $u<w$, $P(u)<P(w)$, both far from the origin, does 4-AP-freeness + supply force an
   increasing 3-AP whose first two terms are *both* in a small window around
   $\{u,w\}$? SAT experiments on two-anchor windows could map candidate statements
   before attempting proofs.
2. **Quantify the staircase against surjectivity (merge with R6/R4).** Each rung
   plants an inversion $P(T_i+f_i)<P(T_i)$ with $f_{i+1}\ge3f_i$ and $T_i\le u+3f_i$:
   staircases from *every* value produce a positive-density-like family of inversions
   at all scales. Try to contradict displacement bounds ($\pi(v)\le Cv$) or derive
   that some value is preceded by infinitely many others (violating order type
   $\omega$).
3. **Strengthen Thm 2′** toward density of good steps (currently: all but finitely
   many rays per anchor). If the good-step set had positive density in every
   $m\mathbb{N}$, counting arguments across anchors might pin two points.
4. **Exclude adversary answer-patterns at scale ratios $\le2$** systematically (the
   solver shows ratio-3 gadgets are consistent; a full classification of consistent
   two-round answer books might reveal a provable global invariant — e.g. "step
   ratios along staircases are eventually forced to be exactly 3-adic", which would be
   a strong structure theorem for any counterexample).
