# Project overview

Inspected 2026-10-31.

- **Purpose:** `app/main.py` implements a teaching FastAPI Order API: health checks, validated order receipts, correlation IDs and structured logs; no persistence or audit storage.
- **Local/remote:** Initially clean local `main` and Azure `main` both point to `db96cb400884742ca191210f9d28586e06848d08`; all 43 tracked file hashes match. This report is the only new file.
- **Tests:** `tests/test_orders.py` covers health, validation, receipt fields and identifiers; `tests/test_deployment_checks.py` covers deployment guards and configuration drift. Both reviewed runs published 29/29 passing tests.
- **Infrastructure:** `infra/lab.bicep`/`lab.bicepparam` target `rg-ai-cloud-dev`, Central US. `foundation.bicep` defines ACR Basic, storage, identity/AcrPull, logs and Container Apps environment. `app.bicep` configures HTTPS, digest-pinned images, managed identity, 0.25 CPU/0.5Gi and 0–1 replicas.
- **Pipelines/evidence:** `pipelines/ci.yml` tests, lints, compiles Bicep and builds Docker. Manual `pipelines/deploy-devtest.yml` gates CI, pushes/deploys and smoke-checks. Latest [CI #3](https://dev.azure.com/Zoran-DevOps-Lab/AI-Assisted-Cloud-Development/_build/results?buildId=3) and [dev/test #4](https://dev.azure.com/Zoran-DevOps-Lab/AI-Assisted-Cloud-Development/_build/results?buildId=4) succeeded October 15 at `62ef8628de19fce2bcced9622787266a51466a81`.
- **Difference/limits:** Only `docs/checkpoints.md`, `docs/preparation-status.md`, and `docs/verification.md` changed afterward. Executable files match the evidenced commit; current HEAD has no exact-commit run. Coverage percentage and current runtime health/drift remain unverified. No tests, builds or deployments were executed during inspection.
