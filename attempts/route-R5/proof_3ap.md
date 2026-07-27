# The 3-AP forcing theorem, with anchored and localized refinements

Route R5, deliverable 1. Conventions are those of `/home/user/erdos/PROBLEM.md`:
$\mathbb{N}=\{1,2,3,\dots\}$, a permutation is a bijection $a:\mathbb{N}\to\mathbb{N}$,
$\mathrm{pos}=a^{-1}$, and a monotone $k$-AP is a $k$-term value-AP whose terms appear in
increasing or decreasing value-order along strictly increasing positions.
An **increasing 3-AP** $(u,\,u+e,\,u+2e)$, $e\ge 1$, is one with
$\mathrm{pos}(u)<\mathrm{pos}(u+e)<\mathrm{pos}(u+2e)$.

Everything in this file is proved in full; the machine stress tests of the intermediate
claims are in `stress_3ap.py` (all pass; see the bottom section).

---

## Theorem 1 (basic forcing; strengthens DEGS77(a))

**Every permutation $a$ of $\mathbb{N}$ contains an increasing 3-AP whose first term is
$a(1)$.** In particular every permutation of $\mathbb{N}$ contains a monotone 3-AP.

**Proof.** Let $u=a(1)$, so $\mathrm{pos}(u)=1$. Suppose, for contradiction, that there
is **no** increasing 3-AP with first term $u$. We claim:

> $(\ast)$ for every $v>u$: $\mathrm{pos}(2v-u)<\mathrm{pos}(v)$.

Indeed, let $v>u$ and put $w=2v-u$. Then $u<v<w$ and $(u,v,w)$ is a 3-term value-AP
with common difference $v-u\ge 1$. All three values occur in the sequence (here
surjectivity of $a$ is used: $w$ occurs at the finite position $\mathrm{pos}(w)$), and
$\mathrm{pos}(u)=1<\mathrm{pos}(v)$ automatically since positions are distinct naturals.
If $\mathrm{pos}(w)>\mathrm{pos}(v)$ then $(u,v,w)$ read at positions
$1<\mathrm{pos}(v)<\mathrm{pos}(w)$ is an increasing 3-AP with first term $u$,
contradicting the supposition. Since $w\neq v$, positions differ, so
$\mathrm{pos}(w)<\mathrm{pos}(v)$. This proves $(\ast)$.

Now define the doubling orbit $v_0=u+1$, $v_{t+1}=2v_t-u$, i.e.
$v_t=u+2^t$. Every $v_t>u$, so $(\ast)$ applies at every $t$ and yields
$$\mathrm{pos}(v_0)>\mathrm{pos}(v_1)>\mathrm{pos}(v_2)>\cdots,$$
an infinite strictly decreasing sequence of positive integers. This contradicts the
well-ordering of $\mathbb{N}$ (positions). $\blacksquare$

**Remarks on what was used (audited):**

1. **Surjectivity of $a$** enters exactly once: every orbit value $v_t=u+2^t$ must
   occur somewhere, so $\mathrm{pos}(v_t)$ is defined. This is sharp: the injection
   $n\mapsto 2^n$ has no monotone 3-AP at all (no three powers of two are in AP since
   $2^b-2^a=2^c-2^b$ with $a<b<c$ is impossible mod $2^{b+1}$ after dividing by
   $2^{\min}$; machine check T3). An argument never using occurrence of all values
   would be wrong.
2. **Well-ordering of positions** (order type $\omega$: positions are $\mathbb{N}$)
   enters exactly once: no infinite strictly decreasing position sequence. For
   two-sided position sets (sequences indexed by $\mathbb{Z}$) the proof genuinely
   fails at this point.
3. The proof does **not** force a decreasing 3-AP, and none is forced: the identity
   permutation has no decreasing pair, let alone a decreasing 3-AP. The forcing
   theorem is intrinsically one-sided-increasing.
4. No finite version of the theorem is true: the parity permutation $\sigma_N$ is a
   monotone-3-AP-free permutation of $[1..N]$ for every $N$ (machine check T4), so
   every proof must, as this one does, use the infinite pigeonhole. Note $\sigma_N$
   survives precisely by having the orbit exit the finite universe: on finite models
   the descent $(\ast)$ halts because $2v-u>N$ eventually (machine check T2 confirms
   this is the **only** escape on finite models with no anchored increasing 3-AP).

---

## Theorem 2 (anchored supply: every position anchors, in every modulus)

**Let $a$ be a permutation of $\mathbb{N}$, $s\in\mathbb{N}$ any position, $u=a(s)$, and
$m\ge 1$ any modulus. Then there exists $e\ge 1$ with $m\mid e$ such that**
$$s<\mathrm{pos}(u+e)<\mathrm{pos}(u+2e),$$
**i.e. $(u,\,u+e,\,u+2e)$ is an increasing 3-AP starting exactly at position $s$, with
step divisible by $m$.**

**Proof.** Suppose not:

> $(\ast\ast)$ for every $v\equiv u \pmod m$ with $v>u$ and $\mathrm{pos}(v)>s$:
> $\mathrm{pos}(2v-u)<\mathrm{pos}(v)$.

(As in Theorem 1: $2v-u\equiv u \pmod m$ and $2v-u>v$, so if
$\mathrm{pos}(2v-u)>\mathrm{pos}(v)$ then $e=v-u$ works, contradiction; distinct values
have distinct positions.)

Let
$$V=\{v\in\mathbb{N}: v\equiv u\ (\mathrm{mod}\ m),\ v>u,\ \mathrm{pos}(v)>s\},\qquad
E=\{a(1),\dots,a(s-1)\}$$
($E$ = values at positions $<s$; $|E|=s-1$). The residue class of $u$ above $u$ is
infinite (unboundedness of $\mathbb{N}$), and only finitely many of its members can sit
at positions $\le s$; hence **$V$ is infinite**.

Fix $v\in V$ and define the doubling orbit $v_0=v$, $v_{t+1}=2v_t-u$, so
$v_t=u+2^t(v-u)$. Each $v_t$ is $\equiv u\pmod m$ and $>u$ (so $v_t\ne u$, hence
$\mathrm{pos}(v_t)\ne s$). By induction: as long as $\mathrm{pos}(v_t)>s$, we have
$v_t\in V$, and $(\ast\ast)$ gives $\mathrm{pos}(v_{t+1})<\mathrm{pos}(v_t)$. An
infinite strict descent of positions is impossible, so there is a least $t^*=t^*(v)$
with $\mathrm{pos}(v_{t^*})<s$, i.e. $v_{t^*}\in E$; note $v_{t^*}>u$.

**Counting.** The map $v\mapsto (v_{t^*(v)},\,t^*(v))\in E\times\mathbb{Z}_{\ge0}$ is
injective, because $v=u+(g-u)/2^{t}$ is determined by the pair $(g,t)$. Moreover for a
fixed $g\in E$ with $g>u$, the exponent $t$ must satisfy $2^{t}\mid(g-u)$ (and
$2^t\le g-u$, since $v-u\ge m\ge 1$), so at most $\nu_2(g-u)+1$ values of $t$ are
possible, where $\nu_2$ is the 2-adic valuation. Hence
$$|V|\;\le\;\sum_{g\in E,\ g>u}\bigl(\nu_2(g-u)+1\bigr)\;<\;\infty,$$
contradicting that $V$ is infinite. $\blacksquare$

**Usage audit for Theorem 2.** Surjectivity: positions of all orbit values are
defined. Order type $\omega$: (i) $E$ is finite; (ii) no infinite position descent;
(iii) only finitely many class members sit at positions $\le s$ (these are three
distinct uses of "every position set bounded above is finite"). Unboundedness of
$\mathbb{N}$: the residue class above $u$ is infinite. Note that Theorems 1 and 2, as
proved, also hold verbatim for bijections $\mathbb{N}\to\mathbb{Z}$ (values in
$\mathbb{Z}$, positions of order type $\omega$); one-sidedness of the **value** set is
never used by the supply engine — only one-sidedness of the **position** set is
essential.

### Corollary 2.1 (tail-affine supply)

For every $\alpha\ge1$, $\beta\ge0$ and every position threshold $T$: the permutation
contains an increasing 3-AP, all of whose terms lie in $\{\beta+\alpha k:k\ge1\}$, with
step divisible by $\alpha$, and all of whose positions exceed $T$.

**Proof.** The class $A=\{\beta+\alpha k\}$ is infinite and only finitely many of its
members sit at positions $\le T$; pick $u\in A$ with $s:=\mathrm{pos}(u)>T$ and apply
Theorem 2 with anchor $s$ and modulus $\alpha$. All three terms are $\equiv u\pmod
\alpha$ and $\ge u>\beta$, hence lie in $A$; all three positions are $\ge s>T$.
$\blacksquare$

(This is the "affine copy" localization promised by the restriction principle, obtained
here directly, without re-proving the theorem inside the copy.)

### Theorem 2′ (ray-hitting refinement, quantitative supply)

Fix $s,u=a(s),m$ as in Theorem 2 and let $V,E$ be as in the proof. Call $v\in V$
**bad** if its entire doubling orbit descends into $E$ (formally: positions strictly
decrease along the orbit until some $v_{t}\in E$). Then:

1. the number of bad $v$ is at most $C(s,u):=\sum_{g\in E,\ g>u}(\nu_2(g-u)+1)$;
2. every $v\in V$ that is not bad admits $t\ge0$ with
   $s<\mathrm{pos}(v_t)<\mathrm{pos}(v_{t+1})$, i.e. the increasing 3-AP
   $\bigl(u,\ u+2^t(v-u),\ u+2^{t+1}(v-u)\bigr)$ starting at position $s$;
3. consequently $u$ is the first term of **infinitely many** increasing 3-APs with
   pairwise distinct steps, all divisible by $m$.

**Proof.** (1) is the counting step of Theorem 2 applied to the bad set. (2): if $v$
is not bad, the descent must halt before reaching $E$; halting at step $t$ means
$\mathrm{pos}(v_{t+1})>\mathrm{pos}(v_t)$ while $\mathrm{pos}(v_t)>s$, and
$(\ast\ast)$-style reading gives the displayed 3-AP (its step is
$2^t(v-u)\in m\mathbb{N}$). (3): the doubling rays $\{u+2^t(v-u):t\ge0\}$ and
$\{u+2^t(v'-u):t\ge0\}$ are disjoint whenever $(v-u)$ and $(v'-u)$ have distinct odd
parts; taking $v=u+mq$ for odd $q=1,3,5,\dots$ gives infinitely many pairwise disjoint
rays, at most finitely many of which are bad by (1); each good ray contributes a 3-AP
whose step lies on that ray. $\blacksquare$

---

## What the engine gives and does not give (quantifier discipline)

- **Given:** for every anchor value $u$ (at its true position) and every modulus $m$,
  *there exists* a step $e\in m\mathbb{N}$ with $(u,u+e,u+2e)$ increasing; and
  infinitely many such $e$ (Thm 2′.3); and copies localized to any residue class
  beyond any position (Cor 2.1).
- **Not given:** any control over *which* $e$; the adversary (the permutation) chooses.
  In particular a "two-point" supply — an increasing 3-AP through a *prescribed pair*
  $(u,v)$ — is FALSE in general (nothing prevents $\mathrm{pos}(2v-u)<\mathrm{pos}(v)$
  for any single fixed pair).
- **Not given:** decreasing 3-APs (identity permutation), nor any 3-AP *ending* or
  *centred* at a prescribed value ($u=a(1)$ can end/centre no increasing 3-AP).

## Machine stress tests (`stress_3ap.py`, all PASS)

- **T1**: the contrapositive step $(\ast)$/$(\ast\ast)$ is checked literally
  (equivalence of "no anchored increasing 3-AP" with the descent constraint) on all
  permutations of $[1..7]$, all anchors, and a deterministic sample at $N=8$.
- **T2**: on every finite permutation with no anchored increasing 3-AP: positions
  strictly descend along doubling orbits inside the universe; orbits terminate only by
  escaping into the head $E$ or leaving the finite value universe; the injectivity and
  the capacity bound $\sum(\nu_2+1)$ hold numerically (48108 instances).
- **T3**: $n\mapsto2^n$ has no monotone 3- or 4-AP (surjectivity is necessary).
- **T4**: parity $\sigma_N$ is monotone-3-AP-free for $N\in\{64,128,256,512\}$ (no
  finite fragment of the theorem is unsatisfiable; infinitude is necessary).
