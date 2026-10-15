# Rehearsal checkpoints

## Verified baseline for course recording

The completed lab baseline is identified by annotated tag **lab-baseline-v1**, targeting the
verified source commit **62ef8628de19fce2bcced9622787266a51466a81**. The tag identifies the source tested and
deployed on October 15, 2026. The later results receipt commit
`09e03a10cc86e74371fbfd3928abe9a5d33b6893` records the outcome and is not the tag target.

| Baseline evidence | Recorded result |
| --- | --- |
| Tag / source | `lab-baseline-v1` / `62ef8628de19fce2bcced9622787266a51466a81` |
| CI | Pipeline 2, [run 3](https://dev.azure.com/Zoran-DevOps-Lab/5007e9df-c7e7-4945-8f8c-b5dcf4b6bc29/_build/results?buildId=3), succeeded for the tagged source |
| Deployment | Pipeline 3, [run 4](https://dev.azure.com/Zoran-DevOps-Lab/5007e9df-c7e7-4945-8f8c-b5dcf4b6bc29/_build/results?buildId=4), succeeded for the tagged source |
| Image digest | `sha256:51986077f0254fd851cf9e28796c34bb62a5440e6794d1dfc36e7f48f5ea0417` |
| Deployed image | `aiclouddkldarnzw2qiw.azurecr.io/order-api@sha256:51986077f0254fd851cf9e28796c34bb62a5440e6794d1dfc36e7f48f5ea0417` |
| API endpoint | https://aicloud-order-api.calmpond-4d0b6792.centralus.azurecontainerapps.io |
| Verified checks | 29 tests, Ruff, dependency integrity, Bicep compilation, hosted build/push, application validation and what-if passed |
| Runtime evidence | Healthy active revision `aicloud-order-api--wkvvz1z`; private image pulled with the app identity; HTTPS health 200 and synthetic order 201; correlated application logs in aicloud-logs |

These results reuse [preparation-status.md](preparation-status.md); no new runtime verification
or deployment was performed to create this checkpoint. Detailed verification and its limits are
summarized in [verification.md](verification.md). The tag preserves the original source tree;
the results receipt and this checkpoint documentation are later records on main.

## Course checkpoint sequence

The original checkpoint names below remain the rehearsal sequence. They describe course states;
only `lab-baseline-v1` is established here as a Git tag. Create further real commits/tags only
after validating each state.

| Checkpoint | Acceptance / preparation state |
| --- | --- |
| baseline-local | Local API tests pass. Completed lab preparation; included in the verified baseline evidence. |
| baseline-cloud | Baseline deployment and runtime checks pass. Completed lab preparation; represented by `lab-baseline-v1`. |
| audit-scaffold | Reviewed first draft. Course demonstration remains to be prepared and validated. |
| audit-working | Audit request acceptance verified in dev/test. Course demonstration remains to be implemented and validated. |
| defect-fixture | Isolated, reproducible cloud failure with real evidence. Fixture and demonstration remain to be prepared. |
| defect-fixed | Targeted and runtime validation pass. Demonstration remains to be prepared after the defect fixture. |
| candidate-review | Bounded improvement validated; same branch used in Course 2. Demonstration remains to be prepared and validated. |

Completed lab preparation does not establish completed course demonstrations or finished recordings.
No completed audit implementation is hidden in this baseline tree. Audit behavior and Storage data
permissions remain absent by design. Codex instruction-loading demonstrations, review exercises,
production slides and videos still require module-by-module preparation and rehearsal.

Record commit IDs and observed results. Do not use destructive git reset/clean to switch demo states.
Use a clean working tree and ordinary branches/worktrees. The initial deployment guard permits
only app creation; selecting this checkpoint does not authorize or enable a repeat deployment over
the existing app.
