# Package verification

## Verified lab baseline (October 15, 2026)

Annotated tag **lab-baseline-v1** identifies source commit
`62ef8628de19fce2bcced9622787266a51466a81`. It does not target the later documentation receipt
`09e03a10cc86e74371fbfd3928abe9a5d33b6893`.

This checkpoint reuses the completed evidence in [preparation-status.md](preparation-status.md).
No application change, new test execution or deployment was performed to prepare these records.
Git publication of the documentation and tag is separate from runtime
verification. The [course checkpoint sequence](checkpoints.md) preserves the later demonstrations.

| Evidence | Verified result |
| --- | --- |
| Baseline tag / source | `lab-baseline-v1` / `62ef8628de19fce2bcced9622787266a51466a81` |
| CI | Pipeline 2, [run 3](https://dev.azure.com/Zoran-DevOps-Lab/5007e9df-c7e7-4945-8f8c-b5dcf4b6bc29/_build/results?buildId=3), succeeded for exactly that source |
| Deployment | Pipeline 3, [run 4](https://dev.azure.com/Zoran-DevOps-Lab/5007e9df-c7e7-4945-8f8c-b5dcf4b6bc29/_build/results?buildId=4), succeeded for exactly that source |
| Execution | Microsoft-hosted Ubuntu, Python 3.13.16; no local Docker or ACR Tasks |
| Checks | Locked dependencies and pip check, Ruff, 29 tests, JUnit publication, three Bicep compilations and hosted container build passed |
| Deployment gates | Exact-source CI success, repeated checks, federation authentication, ACR checks, hosted push, provider validation and what-if passed |
| Application what-if | 1 Create (aicloud-order-api), 0 Modify, 0 Delete; existing-resource Ignore entries only; no unexpected changes or diagnostics |
| Deployment result | ARM deployment `api-4` succeeded; foundation was not redeployed |
| Image digest | `sha256:51986077f0254fd851cf9e28796c34bb62a5440e6794d1dfc36e7f48f5ea0417` |
| Deployed image | `aiclouddkldarnzw2qiw.azurecr.io/order-api@sha256:51986077f0254fd851cf9e28796c34bb62a5440e6794d1dfc36e7f48f5ea0417` |
| API endpoint | https://aicloud-order-api.calmpond-4d0b6792.centralus.azurecontainerapps.io |
| Active revision | `aicloud-order-api--wkvvz1z`, Healthy, Provisioned, active; 100% traffic |
| Runtime settings | Existing Consumption environment; 0.25 vCPU, 0.5 GiB, minimum 0 / maximum 1 replica; HTTPS external ingress |
| Image authentication | App identity aicloud-api-identity with ACR-scoped AcrPull; separate federated deployment identity; registry admin and anonymous pull disabled |
| Smoke checks | Existing PowerShell smoke script passed on the hosted agent; independent HTTPS health 200 and synthetic order 201 matched the baseline contract |
| Logging | Correlated order_created and http_request_completed (201) events reached aicloud-logs from the active revision |

The independent synthetic order was `57596616-00e8-44dd-bcee-e927835acf8f`, with correlation ID
`6a56185e-595e-4c14-978a-da948f66eff9`. Both events were found in
`ContainerAppConsoleLogs_CL` at `2026-10-15T15:18:09.0003456Z`, after initial ingestion delay.
The response also verified the expected product/quantity, UUID identifiers, creation timestamp and
Cache-Control `no-store`. Detailed scopes, resource IDs and ignored evidence locations remain in
preparation-status.md.

The configured managed-identity pull path is supported by the healthy running private-image
revision, identity-only registry configuration, disabled admin/anonymous access and successful
HTTPS requests. No separate token-exchange trace or specific system-log pull event is claimed.
The existing TestClient/httpx deprecation warning did not fail the tests. Idle scale-to-zero timing
and budget enforcement were not verified.

## Course demonstrations still to be prepared

The baseline lab preparation is complete. Audit implementation and acceptance, reproducible defect
fixtures, defect fixes, bounded improvement/review checkpoints, Codex instruction-loading
demonstrations and finished module recordings remain to be prepared and validated. No audit
feature or Storage data permission was added. The initial app-creation guard requires a separately
reviewed allowance before future application updates; this tag does not perform a deployment.

## Historical package-only verification (October 14, 2026)

Verified on 2026-10-14 in Linux with Python 3.12 and PowerShell 7.4.6:
- 16 API tests passed; Ruff passed.
- Both Bicep templates compiled successfully.
- All 6 PowerShell scripts parsed.
- Initializer created a fresh directory and refused an existing destination.
- PowerShell smoke test passed against a running API (health and order creation).

Not executed during that original package check: Windows dependency setup, Docker build, Azure deployment, Azure DevOps pipeline,
Codex instruction loading, audit scenarios or review checkpoints.
One upstream TestClient warning reports future migration from httpx to httpx2; tests pass.
At that stage, cloud definitions were drafts pending target-subscription validation. The subsequent
verified baseline above supersedes that deployment status.

Preparation-time pip-audit of the locked development dependency set reported no known vulnerabilities.
This is not a guarantee and does not implement a pipeline security gate.
