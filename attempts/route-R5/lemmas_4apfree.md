# Structural lemmas for 4-AP-free permutations (forcing-cascade combinatorics)

Route R5, deliverable 2. Standing hypothesis for the whole file: **$a$ is a permutation
of $\mathbb{N}$ with no monotone 4-AP** (both orientations excluded). Notation:
$P(v)=\mathrm{pos}(v)=a^{-1}(v)$. "inc$(x,d)$" means the increasing 3-AP
$P(x)<P(x+d)<P(x+2d)$; "dec$(x,d)$" means $P(x+2d)<P(x+d)<P(x)$.

Machine verification: each finitely-stated lemma below was checked against **all**
monotone-4-AP-free permutations of $[1..N]$ for $N\le 11$ (11,066,766 avoiders at
$N=11$; 12,569,396 in total; enumerator itself cross-validated against a literal
$N!$-filter for $N\le8$ and against the calibration counts for $N\le9$). Firing counts
certify non-vacuity — e.g. L1 fired 24,080,662 times at $N\le11$. Scripts:
`verify_lemmas.py`, `verify_minimality.py`, `enum_avoiders.py`. Zero counterexamples.
This is legitimate evidence because the restriction of any infinite avoider to values
$[1..N]$ (in position order) is a finite avoider, so a finite counterexample to any of
these finitely-stated lemmas would refute the lemma outright.

Throughout, "$v$ exists" abbreviates $v\ge1$; on $\mathbb{N}$ all values $\ge1$ occur
(surjectivity), which is what makes every $P(\cdot)$ below defined — this is where the
infinite setting differs from finite windows, and each lemma's finite test version
carries the corresponding side condition ($x+3d\le N$ etc.).

---

## 1. Blocking lemmas (the elementary forcing steps)

**L1 (up-block).** If inc$(x,d)$ then $P(x+3d)<P(x+2d)$.
*Proof.* Otherwise $P(x)<P(x+d)<P(x+2d)<P(x+3d)$ is an increasing monotone 4-AP.
(Uses surjectivity: $x+3d$ occurs.) $\square$

**L2 (down-block).** If inc$(x,d)$ and $x-d\ge1$ then $P(x-d)>P(x)$.
*Proof.* Otherwise $(x-d,x,x+d,x+2d)$ is an increasing monotone 4-AP. $\square$

**L3a (dual up-block).** If dec$(x,d)$ then $P(x+3d)>P(x+2d)$.
*Proof.* Otherwise $P(x+3d)<P(x+2d)<P(x+d)<P(x)$ makes $(x+3d,x+2d,x+d,x)$ a
decreasing monotone 4-AP. $\square$

**L3b (dual down-block).** If dec$(x,d)$ and $x-d\ge1$ then $P(x-d)<P(x)$.
*Proof.* Otherwise $(x+2d,x+d,x,x-d)$ read along increasing positions is a decreasing
monotone 4-AP. $\square$

Quantifier note: L1–L3 are *universal* — they hold for **every** monotone 3-AP present
in $a$; no choice is involved. They are the complete list of 4-AP constraints touching
a given 3-AP with the same common difference.

## 2. Interaction lemmas (two 3-APs)

**L4a (no shifted abutment).** Not both inc$(x,d)$ and inc$(x+d,d)$.
*Proof.* Together they read $P(x)<P(x+d)<P(x+2d)<P(x+3d)$: an increasing 4-AP.
$\square$

**L4b (no end-to-end abutment).** Not both inc$(x,d)$ and inc$(x+2d,d)$.
*Proof.* inc$(x,d)$ gives $P(x+3d)<P(x+2d)$ by L1; inc$(x+2d,d)$ needs
$P(x+2d)<P(x+3d)$. $\square$

**L5 (no doubled-step continuation).** Not both inc$(x,d)$ and inc$(x+2d,2d)$.
*Proof.* inc$(x,d)$ gives $P(x)<P(x+2d)$; inc$(x+2d,2d)$ gives
$P(x+2d)<P(x+4d)<P(x+6d)$; then $(x,x+2d,x+4d,x+6d)$ is an increasing monotone 4-AP
with difference $2d$. $\square$

**L8 (no doubled-step arrival).** If inc$(x,d)$ and $x-4d\ge1$, then not
$P(x-4d)<P(x-2d)<P(x)$.
*Proof.* Otherwise, with $P(x)<P(x+2d)$ from inc$(x,d)$, the values
$(x-4d,x-2d,x,x+2d)$ form an increasing monotone 4-AP with difference $2d$. $\square$

**L7 (2d-ladder step).** If inc$(x,d)$, $x+6d$ exists, and $P(x+4d)>P(x+2d)$, then
$P(x+6d)<P(x+4d)$.
*Proof.* $P(x)<P(x+2d)<P(x+4d)$ makes inc$(x,2d)$; apply L1 at difference $2d$.
$\square$

**L6 (conditional cascade).** If inc$(x,d)$, $x-d\ge1$, and
$P(x-d)<P(x+d)$ and $P(x+3d)>P(x+d)$, then $(x-d,x+d,x+3d)$ is an increasing 3-AP
(difference $2d$), and consequently $P(x+5d)<P(x+3d)$, and $P(x-3d)>P(x-d)$ if
$x-3d\ge1$.
*Proof.* The hypothesis reads $P(x-d)<P(x+d)<P(x+3d)$ directly; then L1, L2 at
difference $2d$. $\square$

Duals L4b′, L5′, L7′, L8′ of L4b, L5, L7, L8 (replace inc by dec and reverse all
position inequalities) hold by the same proofs with orientations reversed; all were
machine-verified separately. **Caution:** the value-reflection symmetry
$v\mapsto N+1-v$ that swaps the two orientations exists only on finite $[1..N]$;
on $\mathbb{N}$ the two orientations are *not* symmetric (Theorem 1 of
`proof_3ap.md` forces increasing 3-APs, never decreasing ones), so the duals are
genuinely separate statements proved separately, and the cascade engine can only be
driven through the increasing side.

## 3. Minimality lemmas (well-ordering extractions)

By Theorem 1 (`proof_3ap.md`), increasing 3-APs exist; the set of their top positions
is a nonempty set of naturals, so by well-ordering there is an increasing 3-AP
$(x,x+d,x+2d)$ with $k:=P(x+2d)$ **minimal**. Fix such a *k-minimal* triple; write
$i=P(x)$, $j=P(x+d)$.

**M0 (exclusion principle).** No increasing 3-AP of $a$ ends at a position $<k$; i.e.
for every value-AP $(p,p+e,p+2e)$ with $P(p+2e)<k$: NOT $P(p)<P(p+e)<P(p+2e)$.
*Proof.* Definition of $k$-minimality (well-ordering of $\mathbb{N}$). $\square$

**M1.** If $x-d\ge1$ then $P(x-d)>j$ or $P(x+3d)<j$.
*Proof.* Suppose $P(x-d)<j$ and $P(x+3d)>j$. By L2, $P(x-d)>i$; by L1,
$P(x+3d)<k$. Then $P(x-d)<j<P(x+3d)$ exhibits the increasing 3-AP
$(x-d,\,x+d,\,x+3d)$ (difference $2d$) ending at $P(x+3d)<k$, contradicting M0.
$\square$

**M2.** If $x-3d\ge1$ then $P(x-3d)>i$ or $P(x+3d)<i$.
*Proof.* Otherwise $P(x-3d)<i<P(x+3d)$, and $P(x+3d)<k$ by L1, so
$(x-3d,\,x,\,x+3d)$ (difference $3d$) is an increasing 3-AP ending before $k$,
contradicting M0. $\square$

M1 and M2 were machine-verified on the $k$-minimal triple of every finite avoider
containing an increasing 3-AP, $N\le10$ (1,441,171 avoiders with a triple; 506,136
M1-firings, 266,521 M2-firings; zero failures). The SAT probe (`probe_cases.py`)
confirms that at window granularity these are **exactly** the joint exclusions: every
placement combination not excluded by L1, L2, M0-instances is realizable by an actual
finite avoider (realization census in `verify_minimality.py` — all 8 admissible
$(P(x-d),P(x+3d))$-cells are populated).

## 4. Supply-driven lemmas (infinite statements; finite shadows verified)

These use Theorem 2 (anchored supply) of `proof_3ap.md`, hence are statements about
infinite avoiders; their finite shadows are L4b and L5, verified above.

**L9 (top-anchor gap).** Let $(x,x+d,x+2d)$ be any increasing 3-AP of $a$. Apply
Theorem 2 at the anchor $u=x+2d$ (position $k$) with modulus $d$: it returns some step
$e=gd$, $g\ge1$, with inc$(x+2d,\,gd)$ starting at position $k$. Then necessarily
$g\ge3$.
*Proof.* $g=1$ would need $P(x+3d)>k$, contradicting L1. $g=2$ would give
inc$(x+2d,2d)$, contradicting L5. $\square$
*(Machine: `game_anchor.py` G2 — $g=1,2$ UNSAT, $g=3$ SAT, so the bound is sharp at
this window size.)*

**L10 (staircase theorem).** For every value $u$ there is an infinite sequence of
increasing 3-APs of $a$,
$$\#i:\ (T_{i-1},\ T_{i-1}+f_i,\ T_{i-1}+2f_i),\qquad T_i:=T_{i-1}+2f_i,\ T_0:=u,$$
with: $f_1\ge1$; $f_i\mid f_{i+1}$ and $f_{i+1}\ge3f_i$ for all $i\ge1$ (hence
$f_i\ge3^{i-1}$); positions $P(T_0)<P(T_1)<P(T_2)<\cdots$; and for every $i\ge1$ the
planted inversion $P(T_i+f_i)<P(T_i)$.
Moreover $u+2f_i\le T_i\le u+3f_i$, so the staircase climbs at the scale of its own
top step.
*Proof.* Theorem 2 at anchor $u$, modulus 1, gives $\#1$ with some step $f_1\ge1$.
Given $\#i$ with top $T_i$ and step $f_i$: Theorem 2 at anchor $T_i$ (its true
position) with modulus $f_i$ gives a step $f_{i+1}=g f_i$, $g\ge 1$, and an increasing
3-AP $\#(i+1)$ starting at $P(T_i)$. By L9 applied to $\#i$ (whose top is $T_i$ and
step is $f_i$), $g\ge3$. Positions: the start of $\#(i+1)$ is $P(T_i)$ and its top is
$P(T_{i+1})>P(T_i)$. The inversion is L1 applied to $\#i$:
$P(T_{i-1}+3f_i)=P(T_i+f_i)<P(T_i)$. Finally
$T_i=u+2\sum_{j\le i}f_j$ and $\sum_{j\le i}f_j\le f_i\sum_{r\ge0}3^{-r}=\tfrac32f_i$.
$\square$

Interpretation: a 4-AP-free permutation must contain, from **every** value, an
infinite geometrically-accelerating "staircase" of increasing 3-APs, each rung placing
one value ($T_i+f_i$) *behind* its own top — infinitely many specific inversions at
prescribed value-gaps. This is the deepest unconditional cascade this route reached.

## 5. Verification summary

| lemma | status | machine evidence |
|---|---|---|
| L1,L2,L3a,L3b | proved | all avoiders $N\le11$, 24.1M firings each, 0 fails |
| L4a,L4b + dual | proved | $N\le11$, 16.5–24.1M firings, 0 fails |
| L5,L8 + duals | proved | $N\le11$, 8.0M firings each, 0 fails |
| L6 | proved | $N\le11$, 963K firings, 0 fails |
| L7 + dual | proved | $N\le11$, 1.59M firings, 0 fails |
| M0–M2 | proved (uses Thm 1 + well-ordering) | $k$-minimal triple of every avoider, $N\le10$, 0 fails; SAT-window exactness |
| L9 | proved (uses Thm 2) | finite shadows = L4b, L5; SAT check G2 sharp |
| L10 | proved (uses Thm 2 + L9) | rung shadows = L1/L4b/L5 all verified |
