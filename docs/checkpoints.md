# Rehearsal checkpoints
Create real commits/tags only after validating each state. None are pre-created by this package.
- baseline-local: local API tests pass.
- baseline-cloud: baseline deployment and runtime checks pass.
- audit-scaffold: reviewed first draft.
- audit-working: audit request acceptance verified in dev/test.
- defect-fixture: isolated, reproducible cloud failure with real evidence.
- defect-fixed: targeted and runtime validation pass.
- candidate-review: bounded improvement validated; same branch used in Course 2.
Record commit IDs and observed results. Do not use destructive git reset/clean to switch demo states.
Use a clean working tree and ordinary branches/worktrees. No completed audit implementation is hidden
in this baseline tree. Production slides/videos are still prepared module by module.
