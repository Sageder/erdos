# CLAUDE.md — Erdős research-loop harness

This repository runs long autonomous proof-search sessions on open Erdős problems.
Each problem lives in its own folder `erdos-NNN/` containing `PROMPT.md`. The prompt
is the binding task specification; this file sets the standing discipline for every
session in this repo.

## Prime directives

1. The ONLY acceptable final outputs are: a complete proof, a complete disproof, or
   an explicit ABORT because the problem was found to be already claimed (pre-flight)
   or the operator stopped the run. Partial progress is recorded in files, never
   presented as a result.
2. Never assume the answer's sign in advance. Maintain routes toward BOTH branches
   until one is rigorously ruled out.
3. Everything of value lives on disk, not in the context window. Assume the session
   can be killed at any moment; `NOTES.md` must always allow a cold resume.

## File protocol (per problem folder)

- `PROMPT.md` — the task. Read fully at session start. Immutable.
- `PROBLEM.md` — exact statement + conventions, written once at first session start.
- `NOTES.md` — timestamped lab notebook. Every work cycle appends: what was tried,
  what broke, the diagnosis, what changes next. Newest entries at top.
- `ROUTES.md` — route registry: id, mathematical family, status
  (`active` / `blocked: <reason>` / `merged`), current lemma targets.
- `AUDITS.md` — adversarial audit reports, one per candidate argument, verdict first.
- `experiments/` — Python/SAT computations. Every script: deterministic, seeded,
  exact arithmetic (fractions/sympy/gmpy2) for anything feeding a proof; a header
  comment stating claim tested and conclusion. Never trust floats near a boundary.
- `attempts/route-NNN/` — proof drafts and dead ends, kept for autopsy.
- `DRAFT.tex` — only once an argument has survived audit. Professional standard.
- `VERDICT.md` — final: statement, answer, method summary, audit trail, next steps.

## Session loop

On session start: read `PROMPT.md`, `NOTES.md` (top 100 lines), `ROUTES.md`; then
continue the loop:

```
pick route (or open new one) → develop next lemma / construction
→ counterexample-search the lemma computationally BEFORE proving it
→ if lemma survives search: prove it; if proof found: extend route
→ when a route claims a full argument: STOP building, run adversarial audit
→ audit fail: diagnose in NOTES.md, repair or block route, loop
→ audit pass: second independent audit (fresh subagent if available)
→ two passes: write DRAFT.tex, then attack the draft once more, then VERDICT.md
```

Audit discipline: audits are performed adversarially — the auditor's goal is to
BREAK the argument (quantifier order, hidden uniformity, boundary/edge cases,
circularity, misapplied theorems, gaps papered over with "clearly"). Use the
problem-specific audit checklist in `PROMPT.md` §7 every time. Three failed repairs
of the same gap → route blocked, move on.

Subagents: when the Task tool is available, use it for (a) independent route
exploration WITHOUT telling the agent the favored approach, (b) fresh-context
audits fed only PROBLEM.md + the draft. If unavailable, enforce independence by
separate files and separate passes.

## Computation rules

- Compute early, compute often: small cases, exhaustive windows, SAT/ILP searches,
  asymptotic sanity checks. Data guides; certificates prove.
- A finite certificate counts as proof ONLY together with (i) a rigorous reduction
  of the problem (or a lemma) to that finite check and (ii) an independent verifier
  script in `experiments/verify_*.py` that re-checks it from scratch.
- Long searches: checkpoint to disk, print progress, make resumable.

## Web policy

Background only: standard theorems, named results, cited papers explicitly allowed
by `PROMPT.md`. NEVER search for solutions/claims for the problem itself (the
pre-flight check in PROMPT.md §1 is the single exception). Never import a "proof"
from the internet.

## Honesty bar

No sycophancy toward your own work. "Suspiciously short/elementary" triggers extra
audit, not celebration (it usually means a misread statement — recheck §1 conventions
against the argument). If the run ends without resolution, `VERDICT.md` says exactly
that, with the strongest rigorously proved statements and the precise open gap —
never dress a partial result as a solution.
