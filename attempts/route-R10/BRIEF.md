# Route R10 brief — the headline route: smooth-window constructions with digit control
# (Balog–Wooley injection), targeting ALL fixed k >= 2

Read /home/user/erdos/PROBLEM.md first; it is binding.

## Verified facts you may use (machine-checked in this project; re-derive before relying)

With m = n + k the membership criterion is: n in S_k iff for every prime p,
kappa_p(m) >= nu_p((2m)(2m-1)...(2m-2k+1)), where kappa_p(m) = #carries doubling m base p.
Proposition N (verified numerically, proof elementary): for n > 2k^2 this reduces to
 (a) p <= 2k: kappa_p(m) >= nu_p(window product);
 (b) p > 2k, p^J || n+j (1 <= j <= k): kappa_p(floor(m/p^J)) >= J.
   [Odd top-window elements 2m - odd force their own carries automatically ("Lemma O"):
    m == (p^J + i)/2 mod p^J has digits (p+i)/2, (p-1)/2, ..., (p-1)/2 — all >= ceil(p/2).]
Consequence: any n in S_k (n > 2k^2) has n+1..n+k all sqrt(2n)-smooth, and a YES proof for
fixed k must produce infinitely many sqrt(2n)-smooth k-windows PLUS the carry conditions (b)
at every prime dividing a window element, plus (a) at small primes.

## Background you may use (methods; copies in /home/user/erdos/references/)

- balog-wooley.txt: Balog–Wooley 1998 "On strings of consecutive integers with no large
  prime factors": for fixed u > 1, infinitely many n such that n+1,...,n+t(n) are all
  n^{1/u}-smooth with t(n) = floor(log_4 n / log 3u) -> infinity. Their construction
  (Lemma 2.2): CRT + cyclotomic factorization: the string elements are x - i =
  i(z_i^{d_i} - 1), with x an explicit product determined by an equitable partition of the
  primes <= y into classes. The set of such x is exceedingly thin but the construction has
  combinatorial freedom (choice of partition, choice of d-structure, and the freedom to add
  more binomial forms to the system).
- aristotle728.txt: the Erdős-728 writeup (methods licensed; NO conclusion about 727 may be
  imported): carry-rich counting machinery for small primes.

## Mission

Find a construction scheme that, for EVERY fixed k >= 2, produces infinitely many n whose
window n+1..n+k is smooth AND whose Prop-N carry conditions can be forced or counted. Ideas
to explore (non-exhaustive — invent your own):
 1. BW injection: analyze exactly which primes divide the BW window elements
    i(z_i^{d_i} - 1) (order conditions ord_p(z_i) | d_i), and what m = x - 1 looks like
    base p for such p. Can the partition/d/extra-form freedom force top-heavy digits of
    m at those primes (e.g. make m + 1 = z_1^{d_1} divisible by high powers of the
    dangerous primes — note p^J | m+1 forces J carries since the low digits of m are all
    p-1)? Quantify how much of the needed condition set can be forced structurally.
 2. The m+1 trick in general: primes with p^J | m+1 contribute J automatic carries. Design
    windows where every even-position prime factor ALSO divides m + 1 to sufficient order??
    (impossible for p | n+j directly since gcd(n+j, m+1) | k+1-j+... — compute exactly
    what IS possible: gcd(n+j, n+k+1) divides k+1-j; so only small primes — document the
    obstruction precisely and look for the next-best structural carry source: which
    RESIDUES of m mod p^{J+t} force J carries from positions >= J? Characterize the full
    forcing set F(p, J, t) = {r mod p^{J+t} : every m == r has >= J carries in positions
    [J, J+t)} and its density; then ask which constructions can hit F for all relevant p.)
 3. Two-parameter or recursive supplies for k = 3, 4 with positive-density averaging over
    at least one parameter (needed so that first-moment/union-bound counting can beat the
    probabilistic conditions at uncontrolled primes). E.g.: windows around m = x^2 with
    x^2 - 2 = 2y^2 (Pell) give k = 3 supply but zero averaging freedom; can a Pell FAMILY
    (varying d: x^2 - d y^2 = c with d, c smooth-bounded) restore a free parameter while
    keeping the window smooth? Investigate rigorously which of these families are infinite
    (classical Pell theory) and what the carry conditions look like along them.
 4. Any other mechanism for "smooth window + forced carries" you can devise. Wild ideas
    welcome as long as every infinitude claim is backed by a theorem (Pell, BW, or proved
    by you) — reductions to UNPROVED smooth-window conjectures are explicitly worthless
    (PROBLEM.md insufficiency list).

Discipline: numerically test every structural claim (python3+sympy; write scripts in
/home/user/erdos/attempts/route-R10/). Deliverables: HEADLINE.md (analysis + strongest
scheme + what remains), scripts, and if a scheme reaches proof-plausible state, a full
lemma-by-lemma skeleton with each lemma's status (proved / provable-classical / open).
Return: structured summary.
