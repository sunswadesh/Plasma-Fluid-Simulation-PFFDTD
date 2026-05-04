# Documentation Remediation Checklist

Purpose: concrete, prioritized fixes to align docs with actual repository state and reduce onboarding friction.

Last updated: 2026-05-04

## Priority 0 (Critical entrypoint accuracy)

- [x] Replace minimal root README with real quick-start and project description.
  - Implemented in: `README.md`
- [x] Fix docs index links and stale "to create" statements.
  - Implemented in: `docs/INDEX.md`
- [x] Update setup summary from planning narrative to current-state snapshot.
  - Implemented in: `docs/SETUP_SUMMARY.md`

## Priority 1 (Consistency and trust)

- [x] Mark historical completion report as historical to avoid confusion.
  - Implemented in: `docs/COMPLETION_REPORT.md`
- [x] Refresh `docs/DEVELOPERS.md` sections that imply missing build systems or outdated folder assumptions.
  - Exact areas: prerequisites/build guidance and directory layout sections.
- [x] Reconcile planned-vs-current structure language in `docs/README_STRUCTURE.md`.
  - Exact areas: "future" tree versus currently implemented tree.

## Priority 2 (Coverage improvements)

- [x] Add a focused troubleshooting section in `README.md`.
  - Include: compiler not found, OpenMP missing, bad input file format, missing Python deps.
- [x] Add a short branch model section in `README.md` or `docs/DEVELOPERS.md`.
  - Include current branches and intended roles.
- [x] Add doc ownership/update policy.
  - Suggested location: `docs/CONTRIBUTING.md`.

## Priority 3 (Nice-to-have)

- [x] Add a one-page simulation walkthrough using `dipole.str`.
  - Suggested location: `docs/INPUT_FORMAT.md` or a new `docs/QUICK_TUTORIAL.md`.
- [x] Add generated screenshots/plots references from `visualization/` output.
- [x] Add docs linting/link-check workflow in CI.
