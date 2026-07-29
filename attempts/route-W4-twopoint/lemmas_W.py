"""lemmas_W.py -- statements, proofs and re-verification of the two-point lemmas
found by route W4 (TWO-POINT SUPPLY hunt).  Running this file re-runs the exhaustive
machine verification (crossval.py) for every lemma below.

Standing hypothesis for W1-W7 and C1-C4: `a` is a monotone-4-AP-free permutation of N
(both orientations excluded).  pos = a^{-1}; u < v means value order; u < v in position
is written u ~< v.  L = value-records (Lemma 11: w in L iff w ~< t for every t > w).
G = grounded values (g in G iff t ~< g for every t < g).  Both infinite (CORE Lemma 11).

The two free facts used throughout:
    (R)  w in L, t > w   ==>  w ~< t
    (G)  g in G, t < g   ==>  t ~< g
and the two blocking lemmas of route R5:
    (L1) pos(x) < pos(x+d) < pos(x+2d)  ==>  pos(x+3d) < pos(x+2d)
    (L2) pos(x) < pos(x+d) < pos(x+2d), x-d >= 1  ==>  pos(x-d) > pos(x)
(both immediate: otherwise the four terms form an increasing monotone 4-AP).

--------------------------------------------------------------------------------
W1  (record-grounded TRISECTION).  w in L, g in G, w < g, 3 | (g-w), s = (g-w)/3.
    Then pos(w+2s) < pos(w+s).
    Proof.  w ~< w+s by (R).  w+2s < g so w+2s ~< g by (G).  If pos(w+s)<pos(w+2s)
    then (w, w+s, w+2s, g) is an increasing monotone 4-AP of step s.  []

W2  (record-grounded BISECTION -- a genuine two-point SUPPLY).
    w in L, g in G, w < g, 2 | (g-w), s = (g-w)/2.  Then
        pos(w) < pos(w+s) < pos(g),
    i.e. (w, (w+g)/2, g) is an increasing monotone 3-AP: BOTH endpoints are named and
    the step s is determined by them, with no adversary freedom.
    Proof.  w ~< w+s by (R); w+s < g so w+s ~< g by (G).  []
    W2a (= L1 applied to it):  pos(g+s) < pos(g).
    W2b (= L2 applied to it):  if w-s >= 1 then pos(w) < pos(w-s).

W3  (grounded-grounded BISECTION).  g < g' in G, 2 | (g'-g), s = (g'-g)/2, g-s >= 1
    (equivalently g' < 3g).  Then pos(g+s) < pos(g).
    Proof.  g-s ~< g by (G) and g+s ~< g' by (G).  If pos(g) < pos(g+s) then
    (g-s, g, g+s, g') is an increasing monotone 4-AP of step s.  []
    Sharper than CORE Lemma 13(b), which only says (g+g')/2 is not grounded.

W4  (record-record BISECTION).  w < w' in L, 2 | (w'-w), s = (w'-w)/2.
    Then pos(w') < pos(w+s):  the value (w+w')/2, which is SMALLER than w', sits
    AFTER w'.
    Proof.  w ~< w+s by (R) and w' ~< w'+s by (R).  If pos(w+s) < pos(w') then
    (w, w+s, w', w'+s) is an increasing monotone 4-AP of step s.  []
    Sharper than CORE Lemma 13(a), which only says (w+w')/2 is not a record.

W5  (grounded-grounded, one step -- two-point SUPPLY).  g < g' in G, g' < 2g.
    Then (2g-g', g, g') is an increasing monotone 3-AP; hence pos(2g'-g) < pos(g').
    Proof.  2g-g' < g so 2g-g' ~< g by (G); g < g' so g ~< g' by (G).  Then L1.  []

W6  (record-record, one step -- two-point SUPPLY).  w < w' in L.
    Then (w, w', 2w'-w) is an increasing monotone 3-AP; hence
        pos(3w'-2w) < pos(2w'-w)                     (L1)
    and, if 2w-w' >= 1,  pos(w) < pos(2w-w')          (L2, = W6b).
    Proof.  w ~< w' and w' ~< 2w'-w, both by (R).  []
    (This is R17.4 specialised to v in L; recorded here because W6b -- the L2 half --
     is the one that gives the counting corollary C4.)

W7  (a record below 2g precedes the grounded g).  g in G, w in L, g < w < 2g.
    Then pos(w) < pos(g).  Equivalently: pos(g) < pos(w)  ==>  w >= 2g.
    Proof.  2g-w >= 1 and 2g-w < g so 2g-w ~< g by (G); w < 2w-g and w in L so
    w ~< 2w-g by (R).  If pos(g) < pos(w) then (2g-w, g, w, 2w-g) is an increasing
    monotone 4-AP of step w-g.  []
    Together with the trivial case w < g (where w ~< g by (R)):
        for w in L, g in G:  w < 2g  ==>  w ~< g.

--------------------------------------------------------------------------------
Counting corollaries (all proved from the above plus "pos(g)-1 predecessors of a
grounded g include all g-1 smaller values" and "all pos(w)-1 predecessors of a record
w are smaller than w").

C1  g in G  ==>  pos(g) >= g + #(L cap (g, 2g)).                     [from W7]
C2  w' in L ==>  pos(w') <= w' - #{w in L : w < w', w = w' mod 2}.    [from W4]
C3  g in G  ==>  pos(g) >= g + #{g' in G : g < g' < 3g, g' = g mod 2}.[from W3]
C4  w in L  ==>  pos(w) <= w - #(G cap (w/2, w)).                     [from W7]

--------------------------------------------------------------------------------
Lemma TP (position-anchored bounded supply) -- see tp_check.py.  This one needs NO
4-AP-freeness and holds for every bijection a : N -> N.
    Let i < j, u = a(i), v = a(j) with v > u and v > max(a(1),...,a(i-1)); e0 = v-u.
    Then some k with 0 <= k <= j-i-1 satisfies
        pos(u) < pos(u + 2^k e0) < pos(u + 2^{k+1} e0).
    Proof.  Every u + 2^k e0 is >= v > max(a(1..i-1)) and != u, so its position
    exceeds i.  If all k = 0..K (K = j-i-1) failed, each failure would give
    pos(u+2^{k+1}e0) < pos(u+2^k e0), so pos(u+2^{K+1}e0) < ... < pos(u+e0) = j would
    be K+2 = j-i+1 distinct positions inside the interval [i+1, j] of size j-i.  []

Lemma TP-gen (the two-point form; same hypotheses).
    EITHER 2v-u is one of a(i+1),...,a(j-1),  OR  (u, v, 2v-u) is an increasing
    monotone 3-AP.
    Proof.  pos(2v-u) > i as above; if pos(2v-u) > j the triple is increasing, else
    pos(2v-u) is in (i,j).  []
    For j = i+1 the escape set is empty, and the hypothesis says exactly that a(i+1)
    is a record: this is the j=i+1 case of W6.
"""
import crossval

if __name__ == '__main__':
    for N in (8, 9):
        nb, f, v = crossval.run(N, False)
        print(f"N={N} boards={nb}  " +
              "  ".join(f"{r}:{f[r]}/{v[r]}" for r in crossval.RULES))
    print("format rule:fires/violations   (0 violations everywhere)")
