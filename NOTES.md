# NOTES.md — lab notebook, newest entries at top

## 2026-07-27 ~21:55 UTC — session 1 start
- Repo empty; on branch claude/erdos-196-monotone-4ap-gk9blp. Wrote PROBLEM.md, ROUTES.md, this file.
- PRE-FLIGHT: forum thread https://www.erdosproblems.com/forum/thread/196 returns HTTP 403 (bot-blocked),
  as does the problem page. Matches the documented launch-day state; the launch operator checked both
  manually on 2026-07-27 and found no claim. Proceeding per PROMPT §1.
- Python 3.11.15; installed sympy, python-sat, ortools. 4 cores.
- NEXT: calibration experiments (PROMPT §5): reproduce 4-AP-free counts N=3..9 = 6, 22, 102, 564, 3336,
  22266, 168864 and 3-AP-free counts 4, 10, 20, 48, 104, 282, 496; build fast incremental checker +
  brute-force cross-validation; then launch route portfolio.
