# NOTES.md — lab notebook (newest entries at top)

## 2026-07-27 ~21:50 UTC — Session 1 start: pre-flight PASSED, setup

- Pre-flight per PROMPT §1: erdosproblems.com forum threads 403 bot-blocked (expected; operator
  manual browser check was the mandatory launch gate and this run was launched after it).
  My own checks: AI-contributions wiki (data through 2026-06-30) — NO mention of 727;
  teorth/erdosproblems problems.yaml fetched fresh from main — 727 status "open"
  (728 "proved", consistent with known Aristotle result; no news). No claim encountered
  anywhere. RUN PROCEEDS.
- Repo was empty (no commits). Wrote PROBLEM.md, ROUTES.md, this file, AUDITS.md stub.
- Observation recorded during setup (to verify computationally): the full per-prime condition
  compresses to the clean equivalent
      n ∈ S_k  ⟺  (2m)(2m-1)···(2m-2k+1) | C(2m, m),  m = n+k,
  because 2k - s_p(2k) = (p-1)·ν_p((2k)!) turns the deficit inequality into
  ν_p(C(2m,m)) ≥ ν_p(C(2m,2k)) + ν_p((2k)!) for every p. Balakran = k=1 case
  ((2m)(2m-1) | C(2m,m) i.o.). MUST be verified numerically before use.
- Balakran m-values (m = n+1): 6, 15, 28, 45, 66, 91, 153 are hexagonal j(2j-1), but 42, 77,
  110, 120-missing, 126, 140, 156, 170 break the pattern — dissect in R3.
- Next: calibration gate (reproduce §4 table), verify all §2 identities, then launch routes.
