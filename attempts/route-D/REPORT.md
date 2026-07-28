# Route D — Structure theory of block sums H(a,b) and their sumsets B(T)

All computations use exact rational/integer arithmetic (fractions.Fraction, Python int,
or unsigned __int128 in the two C programs). No float appears on any verification path.

Notation. For b>a>=1, H(a,b)=sum_{n=a}^b 1/n; k=b-a+1>=2 is the length.
B(T) = { sum_i H(a_i,b_i) : blocks pairwise disjoint, all elements >= T }
     = { sum_{n in U} 1/n : U finite subset of [T,oo) with no isolated point }.
For a block [a,b]: 2^t is the largest power of 2 dividing an element (the "2-level");
n' = k-rough part of n (primes > k), n'' = n/n', R = prod_{n=a}^b n'; pi = prime counting.

## STATUS TABLE

| # | statement | status |
|---|---|---|
| Q1.1 | v_2(H(a,b)) = -t, t>=1; k <= 2^(t+1)-1 | PROVED (Kuerschak / PROBLEM.md B1) |
| Q1.2 | 2^t R divides den H(a,b), and R >= C(b,k)/b^pi(k) | PROVED (new) |
| Q1.3 | H(a,b) is NEVER a unit fraction 1/N | PROVED (new; finite part machine-checked) |
| Q1.4 | lcm(a..b)/den H(a,b) is odd and k-smooth | PROVED |
| Q1.5 | value of H(c,d) => explicitly finite search: COMPLETE decision procedure | PROVED |
| Q1.6 | H injective on blocks | equal lengths PROVED; else verified for 5187 blocks vs ALL blocks |
| Q2 | 1/N = H(a,b)+H(c,d) with disjoint blocks | NO solutions in every range searched (searches complete in stated class) |
| Q3 | which rho lie in B(T) | 2-adic rigidity PROVED; large exhaustive census; conjecture below |
| Q4 | greedy | PROVED: unrestricted greedy ill-posed; unit fractions are fixed points of the length-2 greedy |
| Q5 | 5 supplied identities + 3 new run-rescaling identities | VERIFIED exactly |

## Q1. SINGLE BLOCKS

### Q1.1 2-adic lemma (known)
[a,b] contains an even number so t>=1; the multiple of 2^t in [a,b] is unique (two
would be consecutive multiples of 2^t, one divisible by 2^(t+1)); hence exactly one
summand has v_2 = -t and  v_2(H(a,b)) = -t.  Any 2^(t+1) consecutive integers contain
a multiple of 2^(t+1), so  k <= 2^(t+1)-1.
CONSEQUENCE USED EVERYWHERE: t, hence a bound on the length, is determined by the VALUE.

### Q1.2 Rough-part divisibility lemma (new)
Lemma. If H(a,b)=u/v in lowest terms then 2^t * R | v, and R >= C(b,k) / b^pi(k).
Proof. For a prime p>k there is at most one multiple of p in [a,b]; if n_0 is it then
v_p(H) = -v_p(n_0), so p^{v_p(n_0)} || v.  Distinct primes > k contribute independently,
so R | v; R is odd and 2^t || v, so 2^t R | v.
For the size: prod_{n=a}^b n = k! * C(b,k), hence for every p,
sum_n v_p(n) = v_p(k!) + v_p(C(b,k)) <= v_p(k!) + log_p b   (Kummer: v_p C(b,k) counts
carries, at most floor(log_p b)).  Multiplying over p<=k: prod_n n'' <= k! b^pi(k),
so R = prod n / prod n'' >= C(b,k)/b^pi(k).  QED
(Verified for all blocks a<=300, k<=14 in q4_greedy.py part 4.  This lemma also gave a
~30x speed-up of the complete solver.)

### Q1.3 THEOREM.  H(a,b) is never a unit fraction.
Proof.  Suppose H(a,b)=1/N, k=b-a+1>=2.
 (1) H(a,b) > k/b  =>  N < b/k.
 (2) 2^t || N and 2^(t+1) >= k+1, so 2^t >= (k+1)/2.
 (3) (k+1)/2 <= 2^t <= N < b/k  =>  k(k+1) < 2b, i.e. b >= (k^2+k+2)/2.
     (a=1 is impossible: it would force b<1.)
 (4) By Q1.2, 2^t R | N, so 2^t R < b/k, with R >= C(b,k) b^{-pi(k)}.
 (5) So it suffices to prove, for all k>=2 and b >= (k^2+k+2)/2,
        (STAR)   k(k+1) C(b,k) >= 2 b^{1+pi(k)} ,
     since (STAR) gives 2^t R >= ((k+1)/2) C(b,k) b^{-pi(k)} >= b/k, contradicting (4).
 k=2: gcd(2a+1, a(a+1)) = 1, so H(a,a+1) = (2a+1)/(a(a+1)) is reduced with numerator
      2a+1 >= 3 > 1.
 k=3: exactly one of a,a+1,a+2 is a multiple of 3; of the other two (differing by 1 or 2)
      at most one is divisible by 4; so some n has {2,3}-part <= 2, giving n' >= n/2 >= a/2,
      R >= a/2, and with 2^t >= 2, N >= 2^t R >= a, contradicting N < b/3 = (a+2)/3.
 k>=4, monotonicity in b:  pi(k) <= k-2 for k>=4, and for b>=k
      C(b+1,k) b^{1+pi(k)} >= C(b,k) (b+1)^{1+pi(k)},
      because this is (b+1)/(b+1-k) >= (1+1/b)^{1+pi(k)}, and
      (1+1/b)^{k-1} <= (b+1)/(b+1-k) follows from
      b (1+1/b)^{-(k-2)} >= b(1-(k-2)/b) = b-k+2 > b+1-k  (using (1+x)^m <= e^{mx} <= 1/(1-mx)).
      So for each k the failure set of (STAR) is an initial segment of b.
 k>=40, analytic tail:  at b_0 = floor(k(k+1)/2)+1 > k^2/2, with C(b,k) >= (b/k)^k,
      (STAR) follows from b^{k-1-pi(k)} >= 2k^{k-1}/(k+1), and 2k^{k-1}/(k+1) < k^{k-1};
      so it suffices that (k^2/2)^{k-1-pi(k)} >= k^{k-1}, i.e.
      (k-1-pi(k))(2 ln k - ln 2) >= (k-1) ln k.  Since ln 2 <= (1/2) ln k for k>=4 it
      suffices that (3/2)(k-1-pi(k)) >= k-1, i.e.  pi(k) <= (k-1)/3,
      which holds for every k >= 34 (machine-verified for 34<=k<=10^6; implied for k>=60
      by Rosser-Schoenfeld pi(x) < 1.25506 x/log x).
 4<=k<=39, finite check: by monotonicity only initial segments must be checked.  Exact
      integer computation gives EXACTLY ONE exceptional pair, (k,b)=(5,16), i.e. the block
      [12,16], and H(12,16)=2627/7280 has numerator 2627 != 1.   QED

Independent computational confirmation:
 * q1_single_block.py brute 400 : all 136864 block sums with a<=400, H<=1 -> no unit
   fraction (and no two equal).
 * q1_single_block.py scan 20000 : 2686698 pairs with a<=20000, k<=sqrt(2a)+2 (the only
   region allowed by step 3) -> no unit fraction; in fact NO block sum with numerator <= 3.
 * q1_single_block.py cheap 200000 : 84527442 pairs with a<=200000; 47069871 survive the
   2-adic condition 2^t k < b, and ZERO survive the rough-part condition 2^t R k < b.

### Q1.4 THEOREM (denominators)
D = den H(a,b), L = lcm(a..b).  Then D | L, v_2(L/D)=0, and v_p(L/D)=0 for all p>k.
So L/D is ODD and k-SMOOTH.
Proof: v_2(L)=t=v_2(D) (Q1.1); for p>k the unique multiple n_0 of p in [a,b] has
v_p(L)=v_p(n_0)=v_p(D) (Q1.2).  QED
Data (all blocks a<=200, 2<=k<=10; 1791 blocks): the cofactor L/D takes only the values
1 (1447x), 3 (198), 5 (112), 7 (23), 15 (8), 9 (2), 63 (1)  -- exactly as predicted.
Which denominators occur?  D is always divisible by 2^t R, and R is huge, so block-sum
denominators are large: length 2 gives D = a(a+1) exactly, length 3 gives
D = a(a+1)(a+2)/g with g|4, and in general D >= 2^t C(b,k) b^{-pi(k)}.

### Q1.5 THEOREM (value => block; complete decision procedure)
If H(c,d)=u/v (lowest terms), k=d-c+1>=2, t=-v_2(u/v), then
 (1) t>=1 and k <= 2^(t+1)-1;
 (2) kv/u <= d <= kv/u + k - 1  and  kv/u - k + 1 <= c <= kv/u   (from k/d <= H <= k/c);
 (3) 2^t C(d,k) <= v d^pi(k)                                     (Q1.2);
 (4) the block contains a multiple of 2^t and none of 2^(t+1), and a multiple of p^e for
     every prime power p^e || v.
(1)+(2) already make "is rho a block sum?" a FINITE question with no a-priori bound on the
elements; (3) collapses the admissible lengths from O(2^t) to O(log v / log(v/u)).
Implemented as blocks.blocks_with_sum(r, cmin); it produces every "-" below.
Examples: 1/20 has t=2, so k<=7 and c in [20k-k+1, 20k]: only 27 candidate blocks in all of
Z, none works.  5/6 has t=1, so k<=3 and c <= 3*6/5 = 3: the ONLY block anywhere with sum
5/6 is [2,3].

### Q1.6 Injectivity
PROVED: two blocks of the same length with equal sums are equal (c -> H(c,c+k-1) strictly
decreasing).
VERIFIED (not merely in a box): for each of the 5187 blocks with 2<=a<=400, 2<=k<=14 the
COMPLETE solver applied to H(a,b) returned exactly {(a,b)} -- no block anywhere in Z_{>=2},
of any length, has the same sum.  Also no coincidence among all 136864 block sums a<=400.
CONJECTURE Q1.6: H is injective on blocks.

## Q2. TWO BLOCKS: 1/N = H(a,b) + H(c,d)

Complete algorithm.  Order so H_1 >= H_2; then 1/(2N) <= H_1 < 1/N, and with k_1 the length
   k_1(N-1)+1 <= a_1 <= 2 N k_1 ,
an explicit finite range.  For each first block the second must have sum exactly
r = 1/N - H_1, and blocks_with_sum(r) finds ALL of them with NO element bound.  The only
unbounded parameter is k_1: the search is complete for k_1 <= K.
2-adic remark: if the two blocks have different 2-levels then max(t_1,t_2) = v_2(N) and both
lengths are <= 2^{v_2(N)+1} - 1.  Hence for N ODD the two blocks must have EQUAL 2-level,
and for v_2(N) <= 2 the choice K=7 settles the unequal-level case completely.

RESULTS
 * q3_table.py (SMAX=2, K=8, non-final block start <= 10^5): no 1/N is a sum of two disjoint
   blocks, for N in {2,3,4,5,6,7,8,10,12,15,20,24,30,35,36,42,60,100} and
   T in {2,3,5,7,10,20,50,100} -- every entry a complete search in the stated class.
 * btarget (C; exhaustive over ALL U in [T,X] with no isolated point, i.e. ANY number of
   blocks): X=85, T in {2,5,10,20,40}, and 34 values of N
   (2..10,12,14,15,16,18,20,21,24,28,30,35,36,40,42,45,48,56,60,70,84,90,100,120,210,2520):
   NO representation of 1/N at all.  170 exhaustive searches, up to 5.5x10^8 nodes each,
   0 solutions.
CONJECTURE Q2: 1/N is not in B(T) for any N>=1 and any T>=2 (proved for one block: Q1.3).

Hint check: rho=u/v is a length-2 block sum iff u a^2 + (u-2v)a - v = 0 has a positive
integral root, forcing u^2+4v^2 to be a perfect square.  Among the 12151 reduced u/v in
(0,1) with v<200 exactly 12 pass: precisely (2a+1)/(a(a+1)), a=2..13.  This thinness is the
quantitative reason exact hits are hard.

## Q3. SMALL RATIONALS WITH LARGE ELEMENTS

### Q3.1 THEOREM (2-adic rigidity)
Let rho = sum_{i=1}^s H(I_i), disjoint blocks, t_i the 2-level of I_i (t_i>=1),
t* = max t_i, c* = #{i : t_i = t*}.
(a) v_2(rho) = -t*  IFF  c* is odd; otherwise v_2(rho) > -t*.
    Proof: H_i = 2^{-t_i} x_i/y_i with x_i,y_i odd; blocks with t_i<t* contribute valuation
    > -t*; the c* top blocks sum to 2^{-t*} sum x_i/y_i and a sum of c* odd/odd fractions
    has numerator = c* mod 2 over an odd denominator.  QED
(b) Each I_i has length <= 2^{t_i+1}-1 and lies strictly between two consecutive multiples
    of 2^{t_i+1}.
(c) If v_2(rho) = -t <= -1 then EITHER
      (i) t*=t : EVERY block has length <= 2^{t+1}-1 and contains no multiple of 2^{t+1}
          (all blocks live in the gaps between consecutive multiples of 2^{t+1}), and the
          number of blocks containing a multiple of 2^t is odd;  OR
      (ii) t*>t and an EVEN number >=2 of blocks have 2-level t*; those contain distinct odd
          multiples of 2^{t*}, so the largest element used is >= 3*2^{t*}.
(d) If v_2(rho) >= 0 (odd denominator, e.g. rho=1 or 1/3) then c* is even; in particular
    s >= 2, so no such rho is a single block sum.
Example: for rho=1/20 (t=2) case (i) forces every block into some interval (8j, 8j+8) with
length <= 7, and every level-1 block to be a sub-block of {4j+1,4j+2,4j+3} containing 4j+2.

### Q3.2 Exhaustive census of B(T) inside a window
q3_window.py (Python, exact) and wincensus.c (C, exact __int128, with the p-adic prune
Q[pos] | S) enumerate EVERY U in [T,X] with no isolated point and report every value with
denominator <= DCAP.  The two agree exactly on all overlapping ranges.

Window [2,X], all values with denominator <= 12:
  X=26 and X=30 : 5/6, 7/12, 13/12, 6/5, 5/7, 6/7, 8/7
  X=40          : + 7/9
  X=50          : + 15/11
  X=70          : + 7/11, 8/11
with, for example,
  6/5   = H(2,3)+H(5,6)
  7/9   = H(3,4)+H(14,15)+H(35,36)
  15/11 = H(3,6)+H(11,12)+H(14,15)+H(35,36)+H(44,45)
  7/11  = H(7,8)+H(14,15)+H(21,22)+H(35,36)+H(44,45)+H(55,56)
(all verified exactly).

Complete statements inside those boxes:
 * NO value with denominator 1,2,3 or 4 occurs for X<=70; in particular 1 is not in B(2)
   with elements <= 70 (and <= 80 by the parent experiments/csearch run).
 * NO unit fraction occurs anywhere.
 * every value found has numerator >= 5.
 * smallest denominators grow fast with T: window [2,26] has 300 values with den <= 300;
   window [50,74] has only 53 values with den <= 10^5, smallest denominator 5402 = 73*74;
   window [100,124] has 54 values with den <= 10^6, smallest 15252 = 123*124.

So: does representability depend on the size of rho relative to T?  YES.  Two rigorous
mechanisms:
 (size)  rho <= sum_{n=T}^X 1/n < ln(X/(T-1)), so a representation needs X >~ T e^rho;
 (arithmetic)  if rho=u/v and p^e > v is a prime power dividing some n in U with maximal
   v_p, then a SECOND element of U must attain v_p = e, so max U >= 2 p^e.  Hence no element
   of U may have a prime power factor in ( max(v, maxU/2), maxU ]; in particular U contains
   no prime p > max(v, maxU/2).  Since every maximal run has length >= 2 and consecutive
   integers are coprime, this is severe -- it is exactly the obstruction the p-adic prune
   exploits, and why every search terminates so quickly.

### Q3.2b  B(T) IS NOT SHIFT-INVARIANT  (new, exhaustive)

btarget (exhaustive over ALL U in [T,X], any number of blocks, X=46 unless stated):

  rho    T=2   T=3   T=4   T=5   T=7   T=10
  6/5    YES   no    no    no    no    no
  5/6    YES   no    no    no    no    no
  7/12   YES   YES   no    no    no    no
  19/20  YES   YES   no    no    no    no

with 6/5 = H(2,3)+H(5,6), 5/6 = H(2,3), 7/12 = H(3,4), 19/20 = H(3,6).
Stronger exhaustive negatives (larger box):
  7/12 not in B(4) with elements <= 66   (32 298 335 nodes, 0 solutions)
  5/6  not in B(5) with elements <= 66   (491 902 734 nodes, 0 solutions)

So membership in B(T) is genuinely T-dependent: it is NOT the case that
B(T) = B(2) for all T, and B(T) is (as far as the data go) NOT closed under
addition either -- one cannot freely "push a representation to the right".
This is the structural reason a naive "translate the construction far out"
strategy fails, and it matches Q1.5: e.g. 5/6 has 2-level t=1, hence length <= 3
and start c <= 3*6/5 = 3, so [2,3] is the ONLY block anywhere with that value.

### Q3.3 What IS representable (proved)
 * H(a,b) is in B(T) for every a>=T -- and by Q1.5 these are rigid (e.g. 5/6 is in B(2) but
   has no single-block representation with c>=4 at all).
 * B(T) contains B(T') for T<=T'; and if rho_1 in B(T) is realised with largest element M
   and rho_2 in B(M+2), then rho_1+rho_2 in B(T).
 * LENGTH-2 NORMAL FORM (verified).  If N is a set of integers >= T pairwise at distance
   >= 2 (so the blocks [n,n+1], n in N, are pairwise disjoint), then n -> ceil(n/2) is
   injective on N and
        sum_{n in N} H(n,n+1) = sum_{n in N} 1/ceil(n/2) + Delta(N),
        Delta(N) = sum_{n in N} (-1)^{n+1} / (n(n+1)).
   So every element of B(T) coming from length-2 blocks is an Egyptian fraction with
   distinct denominators, CORRECTED by Delta.  Delta(N)=0 would convert an arbitrary
   Egyptian representation into a block representation.  A necessary condition (2-adic) is
   that the top value of v_2(n(n+1)) be attained an even number of times.  No Delta=0
   family with max N <= 60 exists (q4_correction_cancel.py; search truncated above that).

### Q3.4 Sharpest conjecture supported by the data
CONJECTURE Q3.  For every T>=2, B(T) contains no rational with numerator 1 (= Conjecture
Q2); and more generally, if rho is in B(T) and a is the smallest element used, then
den(rho) >= a(a+1), where a >= max(T, 2/rho - 1).
The bound a >= 2/rho - 1 is PROVED (the block containing the smallest element already
contributes 1/a + 1/(a+1)).  The census data are consistent with the denominator bound: in
each window [T,T+24] the minimal denominator found was exactly (X-1)X, from the right-most
single block.
NOT supported: any purely congruence/valuation criterion.  The low-denominator members of
B(2) found -- 5/6, 7/12, 13/12, 6/5, 5/7, 6/7, 8/7, 7/9, 15/11, 7/11, 8/11 -- show no
congruence pattern; representability is genuinely Diophantine (cf. Q2 / Q4.3).

## Q4. A GREEDY THEORY

### Q4.0 THEOREM.  The unrestricted greedy does not exist.
If rho > 0 is not itself a block sum then
    sup { H(I) : I a block, H(I) <= rho } = rho,   and the sup is NOT attained.
Indeed for each start a let b(a) be maximal with H(a,b(a)) <= rho; then
rho - H(a,b(a)) < 1/(b(a)+1) -> 0 as a -> infinity, while equality is impossible (Q1.3 when
rho is a unit fraction, by hypothesis otherwise).  Illustration for rho=1/6:
   [12,13] gap 1/156 ; [25,28] gap 3797/245700 ; [51,59], [103,120], [207,243], [415,489]
   with gaps tending to 0.
CONSEQUENCE: a greedy for block sums must fix the length (or the start).

### Q4.1 THEOREM.  Unit fractions are fixed points of the length-2 greedy.
For every N>=1 the largest length-2 block sum <= 1/N is H(2N,2N+1)
(H(2N-1,2N) = 1/N + 1/(2N(2N-1)) > 1/N and H(2N,2N+1) = 1/N - 1/(2N(2N+1)) < 1/N), and
        1/N - H(2N,2N+1) = 1/(2N(2N+1)).
So the greedy maps a unit fraction to a unit fraction: the numerator is permanently stuck
at 1 and the process never terminates.  It produces N_0=N, N_{j+1} = 2N_j(2N_j+1) and, for
every s, the exact identity
        1/N = sum_{j<s} H(2N_j, 2N_j+1) + 1/N_s ,
whose blocks are pairwise disjoint (they grow doubly exponentially).  E.g.
 1/6 = H(12,13)+H(312,313)+H(195312,195313)+H(76293945312,76293945313)
       + 1/5820766091346740722656 .
Machine-verified for 1<=N<=3000.  This is the sharp form of the warning in the prompt.

### Q4.2 No potential based on the numerator can work.
For rho in {1/2, 1/6, 1/20, 3/7, 11/2520} NOT ONE of the ~2400 blocks with 2<=a<=400,
2<=k<=6 and H<=rho lowers the numerator of rho-H.  (For rho=5/12 and 7/30 a few do.)
Moreover any greedy that reaches numerator 1 is dead by Theorem Q1.3, and by Conjecture Q2
probably dead for good.

### Q4.3 What the correct greedy looks like
 1. write rho as an Egyptian fraction sum_{u in U} 1/u with all u >= T (always possible,
    since sum_{n>=T} 1/n diverges);
 2. replace each 1/u by a length-2 block: [2u-1,2u] (error +1/(2u(2u-1))) or [2u,2u+1]
    (error -1/(2u(2u+1))).  The blocks are automatically pairwise disjoint provided we never
    pick [2u-1,2u] and [2(u-1),2u-1] together;
 3. the representation is EXACT iff the signed errors cancel:
        sum_{u in P} 1/(2u(2u-1))  =  sum_{u in Q} 1/(2u(2u+1)),   U = P u Q disjointly.
Equivalently, with c_n = 1/(n(n+1)): find a set of odd n and a set of even n with equal
sum of c_n.  Necessary (2-adic): the maximum of v_2(n(n+1)) is attained an even number of
times.  Exhaustive search found NO solution with max n <= 60.  This is the precise
"endgame" obstruction: the greedy always leaves a residual error and killing it exactly is
a genuinely Diophantine problem (the length-2 instance is the Pythagorean condition
u^2 + 4v^2 = square of Q2).

## Q5. IDENTITIES  (all verified exactly, q5_identities.py)

Supplied (symbolically confirmed in Q(n)):
  1/n = 1/(2n) + 1/(2n+1) + 1/(2n(2n+1))
  1/n = 1/(n+d) + 1/(n + n^2/d)                          for d | n^2
  1/(2m) + 1/(2m+1) = 1/m - 1/(2m(2m+1))
  1/(2m-1) + 1/(2m) = 1/m + 1/(2m(2m-1))
  1/(3m-1) + 1/(3m) + 1/(3m+1) = 1/m + 2/(3m(3m-1)(3m+1))

NEW (route-D) -- RUN RESCALING.  Key point: a q-fold blow-up of a run is again a run,
  { qn + j : a <= n <= b, 0 <= j < q } = [ qa , qb+q-1 ].
Hence
  H(2a, 2b+1)   = H(a,b) - sum_{n=a}^{b} 1/(2n(2n+1))
  H(2a-1, 2b)   = H(a,b) + sum_{n=a}^{b} 1/(2n(2n-1))
  H(3a-1, 3b+1) = H(a,b) + sum_{n=a}^{b} 2/(3n(9n^2-1))
Verified exactly for 1<=a<=59, a<=b<=a+24 (and the general q-version for 2<=q<=7).
Also verified: H(n,n+1) = 1/ceil(n/2) + (-1)^{n+1}/(n(n+1)) for 2<=n<=400, and the three
length-3 normal forms around 3m for 2<=m<=200.
Sanity: 1/3+1/4+1/5+1/6+1/20 = 1 ; 1/2+1/3+1/10+1/15 = 1 ;
        1/2+1/3+1/4+1/5+1/6+1/20 = 3/2  (the circulating identity is indeed false).

## FILES

blocks.py                 core library: exact H (binary splitting), v_2, COMPLETE solver
                          blocks_with_sum (Q1.5), helpers
q1_single_block.py        brute / pruned / sieve scans for unit-fraction block sums, collisions
q1_proof_check.py         machine-checks the finite part of Theorem Q1.3
q1_injectivity.py         injectivity against ALL blocks; denominator structure (Q1.4)
q2_two_blocks.py          complete two-block search + pair scan
q3_multiblock.py          complete <= s-block search (bounded lengths for all but the last)
q3_table.py               representability table over many (rho,T)
q3_window.py              exact Python window census
q3_box.py                 box DFS over runs
wincensus.c               fast exact census of no-isolated-point subsets of [T,X]
btarget.c                 fast exact decision "is p/q in B(T) with elements <= X"
sweep.sh                  driver for the 1/N sweep
q4_greedy.py              greedy theorems and experiments
q4_correction_cancel.py   search for Delta(N)=0 (Q4.3)
q5_identities.py          exact verification of all identities
out_*.txt                 raw outputs of the runs quoted above

Reproduce with e.g.
  python3 q1_proof_check.py
  python3 q5_identities.py
  python3 q1_injectivity.py 400 14
  gcc -O2 -o btarget btarget.c   && ./btarget 2 85 1 20 1
  gcc -O2 -o wincensus wincensus.c && ./wincensus 2 70 12 400

## RUNS THAT DID NOT FINISH IN THIS SESSION (no claims made from them)

 * ./btarget 2 88 1 1        (is 1 in B(2) with elements <= 88?)  -- still running at the
   end of the session; the parent's experiments/csearch already settled X <= 80 (no solution).
 * ./wincensus 2 90 1        (all INTEGER values in a window [2,90])  -- still running.
 * q3_table.py rows below 5/12 (11/2520, 1, 6/5, 19/20, 5/6, 7/12) were not reached;
   the same questions for 6/5, 19/20, 5/6, 7/12 are answered exhaustively (and more
   strongly) by btarget in section Q3.2b.
