route R22 (angle B) -- file map

arch.py        library: exact block index, two independent condition-(ii) checkers,
               delay families, fibre sizes, Lemma B1 budget identity.
validate.py    cross-validation of the two (ii)-checkers against each other and against
               route R20's positive/negative controls; plus the link
               "(ii) violated => monotone 4-AP for EVERY within-class order", tested with
               the trusted experiments/apcheck.py.        -> ALL OK
headdelay.py   the head-delay architecture; (ii) over all 4-APs to M; AP diagnostics.
sweep.py       parameter sweep (b, s_m, K_m) + sharpness probes.  `main` / `sharp` /
               `kmono` / `big` modes.
budget.py      Lemma B1 + Corollary B2 with the SHARPNESS example (fat-head family).
reslimit.py    the resolution limit: at range b^{J+1} the failure of tameness is visible
               only for AP steps q <= J+1.  (Why no finite search could have refuted
               R21-C.)
d1check.py     Theorem R22-2 diagnostics + Lemma R22-0 (t>=0 forces a block layout).
window.py      exact eager encoding of a class architecture over an arbitrary value set.
eager.py       eager encoding over [1..N] + 3 solvers; reproduces route R20's certified
               CLS(3,a) verdicts (SAT 160 / UNSAT 250).
satprobe.py    route R20's CEGAR class solver applied to head-delay architectures.
tailprobe.py   the same over value-windows [V0..W] (CORE Lemma 24 tails).
scan_heads.py  first-UNSAT board size over a grid of (b, s, K).
mus.py         single-deletion-minimal UNSAT value set.
lowprofile.py  NEXT-STEP probe: extinction for the LOWER profile pos(v) >= gamma v.
