# Baseline preparation — 2026-10-14

> Current user decision: ACR is the selected registry; GHCR is no longer selected. Build/push runs
> on a Microsoft-hosted Azure DevOps agent, with no local Docker and no ACR Tasks. Container Apps
> pulls from ACR with its user-assigned managed identity. Initial Azure Repos upload and hosted CI
> are now authorized as recorded below; Azure validation/what-if evidence is preserved.
> ACR is not confirmed free. No purchases, Azure resource creation or deployment are authorized.
> Commit/push scope for this step is Azure Repos main only; no GitHub push.
> Confirmed region: `centralus`; resource group: `rg-ai-cloud-dev`. Budget remains unconfirmed.
> Other architecture is unchanged.

## Initial Azure Repos upload and CI execution (2026-10-15 America/Chicago)

Current authorization permits committing the reviewed course files, adding a separate `azure`
remote, pushing `main` only to Azure Repos, and creating/running the CI pipeline from
`pipelines/ci.yml`. GitHub `origin` is preserved and is not a push target in this step.
Azure deployment, provider registration, service connections, purchases and deployment-pipeline
execution remain unauthorized. Earlier no-commit/no-build statements below describe prior stages.

Before editing, the working directory and Git root were both confirmed as
`C:\Projects\AI-Assisted-Cloud-Development`. Azure repository branch discovery returned no refs;
the project had no pipeline definitions. Local Python 3.13.16 checks passed: Ruff, 16 pytest tests
and `pip check`. The existing TestClient/httpx deprecation warning did not fail the tests.

The reviewed CI uses Python 3.13 and `ubuntu-latest`, installs locked development dependencies,
checks dependency integrity, lints, runs behavior tests and publishes JUnit results, compiles
three Bicep templates, and builds a container image without pushing it. It has no Azure login,
Azure deployment, registry push or service-connection requirement. The separate deployment YAML
remains manual and will not be registered or run in this step.

### Verified upload and hosted CI results

| Evidence | Actual result |
| --- | --- |
| Reviewed/tested commit | `9fb72fbff56caa1510f977456a573c0ea7936d47` |
| Git identity | Existing `Cloud Lab <cloud-lab@example.invalid>`; unchanged |
| Upload | `main` pushed only to `azure`; remote ref read-back matched the full tested SHA |
| GitHub origin | `https://github.com/zorantadic/AI-Assisted-Cloud-Development.git`; preserved, not pushed |
| Azure remote | `https://dev.azure.com/Zoran-DevOps-Lab/AI-Assisted-Cloud-Development/_git/AI-Assisted-Cloud-Development` |
| Pipeline | `AI-Assisted-Cloud-Development-CI`, ID **2** |
| Definition binding | Azure repository `dd8b4af5-37d7-494d-9167-a8a197250565`, `pipelines/ci.yml`, main |
| Run | ID **2**, **succeeded**, sourceVersion exactly the reviewed/tested SHA above |
| Run URL | https://dev.azure.com/Zoran-DevOps-Lab/5007e9df-c7e7-4945-8f8c-b5dcf4b6bc29/_build/results?buildId=2 |
| Execution | Microsoft-hosted Azure Pipelines queue, `ubuntu-latest`, Python **3.13.16** |
| Dependency installation/integrity | Locked development install succeeded; `pip check`: no broken requirements |
| Ruff | Passed; all checks passed |
| Pytest | **16 passed, 1 warning**, 0.57 seconds on the hosted agent |
| Published results | JUnit publication succeeded; test run ID 2 completed with **16 total / 16 passed / 0 incomplete** |
| Bicep | foundation.bicep, app.bicep and lab.bicep compiled successfully; no Azure deployment |
| Container | Hosted-agent image build succeeded; tag `order-api:9fb72fbff56caa1510f977456a573c0ea7936d47`; no push |
| Completion | October 15, 2026, **08:59:23 CDT** (13:59:23 UTC) |

The CLI pipeline creation queued the one initial run. Its definition and source commit were
verified before inspecting task logs; no duplicate run or rerun was queued. The repository was
empty before upload; no force push or divergent-history replacement occurred. The existing Git
identity and GitHub remote were retained. The temporary repair script, virtual environment,
credentials/local environment files, generated artifacts and backups are excluded from Git;
only the eleven explicitly reviewed course files were staged for the tested commit. Existing
application behavior and tests were not changed.

Nonblocking warnings: the existing FastAPI/Starlette TestClient httpx deprecation warning, and
a hosted-image notice about an upcoming ubuntu-latest migration. Neither caused a failed task.
No access/capacity blocker occurred; no capacity was purchased and monthly counters were not
re-read. Container-build success is not an image push, deployment or running-container smoke test.

This results receipt changes documentation only and is committed/pushed with `[skip ci]` to
avoid a redundant hosted run. The successful validation belongs to the exact code commit above,
not a claim that the receipt commit was separately tested by CI. No deployment pipeline was
created or run, no service connection/provider registration/Azure resource was created, and
Customer-Portal was not modified. Azure cost approval, foundation creation, registry/image push,
managed-identity pull and deployed-runtime acceptance remain separate outstanding stages.

## Verified Azure DevOps project and workspace correction (2026-10-15 America/Chicago)

The organization `Zoran-DevOps-Lab` already existed. The earlier claim that the course project
already existed was incorrect: its exact lookup returned TF200016 before the authorized creation.
The project was subsequently created successfully and independently read back with its default
Git repository. The earlier project-existence/access blocker below is now resolved.

| Property | Verified value |
| --- | --- |
| Organization | https://dev.azure.com/Zoran-DevOps-Lab |
| Project | AI-Assisted-Cloud-Development |
| Project ID | 5007e9df-c7e7-4945-8f8c-b5dcf4b6bc29 |
| Project URL | https://dev.azure.com/Zoran-DevOps-Lab/AI-Assisted-Cloud-Development |
| Project state | wellFormed |
| Visibility / version control | Private / Git; Git enabled, TFVC disabled |
| Work item process | Basic, verified as the organization's default before creation |
| Process ID | b8a3a935-7e91-48b8-a94c-606d37c3e9f2 |
| Repository | AI-Assisted-Cloud-Development |
| Repository ID | dd8b4af5-37d7-494d-9167-a8a197250565 |
| Repository URL | https://dev.azure.com/Zoran-DevOps-Lab/AI-Assisted-Cloud-Development/_git/AI-Assisted-Cloud-Development |
| Repository state at read-back | Enabled; size 0; defaultBranch null |

These values come from the completed project creation and subsequent project/repository reads,
not a new remote verification during this correction. Customer-Portal was not modified.
Project/repository provisioning does not establish pipeline execution, service-connection setup,
Azure deployment readiness, or runtime success. No commit or push was performed.

The correct course working directory and Git repository root are both
`C:\Projects\AI-Assisted-Cloud-Development`, confirmed before this edit. The previous operation
actually added the course status record to
`C:\Projects\Halo-ADO-Validation-Lab\docs\preparation-status.md`; this was a working-directory
error, not merely a bad report link. Its verified DevOps details are merged into this existing
course file. Only that mistaken Halo addition is removed; unrelated work in both repositories
is preserved. No remote requests or changes are performed by this correction.

The Azure configuration, foundation validation/what-if results, cost limitations and remaining
Azure prerequisites below retain their existing evidence and scope.

## Current target validation and what-if (2026-10-14 America/Chicago)

### Successful checks
- Before Azure operations, `az account show` and subscription discovery confirmed Subscription 1,
  ID `4d992bb0-6909-470c-bbef-896082984f67`, tenant `b7fddbde-dfdf-425e-a785-97d3b91909a0`, Enabled.
  Explicit subscription ID was supplied to Azure target checks, validation and what-if.
- `az group exists --name rg-ai-cloud-dev` returned false. There were no group contents to inspect.
- All three templates (`foundation`, `app`, `lab`) compiled; `infra/lab.bicepparam` compiled.
  The existing subscription-scope wrapper was reused, without creating the resource group.
- `az deployment sub validate` succeeded (exit 0, error null); correlation ID
  `16228c85-207f-4456-94e0-39fdc41dda6d`. This is validation success, not a deployment.
- `az deployment sub what-if` succeeded (exit 0): 7 Create, 0 Modify, 0 Delete,
  no diagnostics. Scope is resource group plus foundation, not the separate API deployment.
- Evidence: ignored local `artifacts/lab-validation.txt` and `artifacts/lab-what-if.txt`.
  Parameters: `infra/lab.bicepparam`; planning JSON and deployment defaults match the target.
  Pipeline checks its service connection subscription before registry/build/deployment commands.
- Final JSON/YAML parsing, compiled-parameter consistency, Bash syntax and `git diff --check`
  passed. After validation/what-if, RG existence still returned false and all five provider
  registration states remained NotRegistered.

| Name | Azure resource type | Region | SKU / configuration | What-if |
| --- | --- | --- | --- | --- |
| rg-ai-cloud-dev | Microsoft.Resources/resourceGroups | centralus | none | Create |
| aiclouddkldarnzw2qiw | Microsoft.ContainerRegistry/registries | centralus | Basic; admin disabled | Create |
| aiclouddkldarnzw2qiw | Microsoft.Storage/storageAccounts | centralus | Standard_LRS / StorageV2 | Create |
| aicloud-api-identity | Microsoft.ManagedIdentity/userAssignedIdentities | centralus | none | Create |
| aicloud-logs | Microsoft.OperationalInsights/workspaces | centralus | PerGB2018; 30-day retention | Create |
| aicloud-environment | Microsoft.App/managedEnvironments | centralus | Consumption; no dedicated profile | Create |
| d33eff47-f660-508d-9315-47ec6ebe8183 | Microsoft.Authorization/roleAssignments | not regional; ACR scope | AcrPull for app identity | Create |

No existing resource modification or deletion was proposed. `baseline-foundation` is the nested
ARM deployment module, not an additional service. ACR/Storage names are ARM-evaluated names,
not evidence that either resource has been created.

### Remaining blockers and limits
- API `aicloud-order-api` remains a later planned Create in centralus (Consumption, 0.25 vCPU,
  0.5 GiB, 0–1 replicas). Its Bicep compiled, but cloud validation/what-if of that separate phase
  has not run: it requires foundation resources and a real ACR image digest. No placeholder image
  was built or deployed, and the seven foundation what-if entries do not include the API.
- Provider discovery reported Microsoft.App, Microsoft.ContainerRegistry, Microsoft.Storage,
  Microsoft.ManagedIdentity and Microsoft.OperationalInsights as NotRegistered. No provider
  registration was requested. Successful planning does not establish deployment readiness or quota.
- Resolved on October 15: the course project and its Git repository were created and read back
  as recorded above. The earlier TF200016 was a pre-creation observation, not a current blocker.
  Do not recreate the project. Hosted-capacity confirmation remains separate from pipeline execution.
- ACR is not confirmed free. Cost approval, deployment authorization, service connection and actual
  hosted-agent build, managed-identity pull and runtime checks remain outstanding.

No resources, build or deployment were executed. No commit/push. Earlier observations below are
historical where they differ from the current target and results in this section.

## Observed
- Initial checkout: clean `main`, baseline commit `cd794a4`; only remote is the existing GitHub origin.
- Windows Python 3.13.16: Ruff passed, 16 tests passed, and `pip check` passed.
  TestClient still warns about the future httpx2 migration. This sandbox run also reported a
  pytest cache write warning; neither warning failed the tests.
- Azure CLI 2.90.0, azure-devops extension 1.0.8, Bicep 0.48.1 available.
- Azure authentication and resource-group discovery succeeded in both accessible subscriptions.
  No dedicated project resource group has been identified or selected.
- Historical: authenticated project discovery at the previously supplied organization
  `ai-cloud-development-lab` returned HTTP 404. That organization is no longer the course target.
- Historical pre-creation discovery (October 14): https://dev.azure.com/Zoran-DevOps-Lab.
  Agent-executed authenticated
  `az devops project list --organization https://dev.azure.com/Zoran-DevOps-Lab` succeeded
  (exit code 0), listing `Customer-Portal`, ID `4d3169ec-5eb3-4017-8d12-a69e940f9368`,
  state `wellFormed`. The proposed `AI-Assisted-Cloud-Development` project was not listed.
  This verifies project-list access, not project-creation permission or pipeline execution.
- User-confirmed portal evidence for Zoran-DevOps-Lab: Parallel jobs > Private projects >
  Microsoft-hosted > Free tier; one parallel job, 1,800 minutes/month, 0 used
  (1,800 remaining at the user's check). The user clarified that the previous screenshot
  did not belong to ai-cloud-development-lab. The agent has not independently checked
  the capacity/usage counters or run a pipeline.
- All three Bicep templates compile. PowerShell scripts parse; the revised smoke script passed
  on Windows PowerShell against a local server with `APP_ENVIRONMENT=devtest`.
  Observed health success, order HTTP 201, correlation IDs, and structured application logs.

## Local changes awaiting cloud verification
- `infra/lab.bicep` includes the resource group and foundation in subscription-level planning.
- Manual deployment tests its own commit, authenticates with `az acr login`, builds and pushes
  with Docker on the Microsoft-hosted Ubuntu agent, resolves the ACR digest, and deploys by digest.
  Health/order smoke checks remain in the pipeline. CI also builds only on a Microsoft-hosted agent.
- The planning JSON identifies ACR, hosted-agent builds and user-assigned identity image pulls.
  Target names are now resolved from the foundation plan; service connection remains a placeholder.
  The JSON is not a deployment input.
- Existing Bicep already defines ACR Basic with admin disabled, registry-scoped AcrPull for the
  runtime identity, and Container Apps registry authentication using that identity; it was preserved.
  Verify registry-scoped AcrPush for the federated pipeline identity before any future build/push.
  No registry username/password or GHCR credential is added to runtime configuration.
- No application behavior or dependency changes; no audit feature or demonstration defect added.
- No local Docker, cloud deployment, remote image build, or Azure DevOps run performed.
  YAML has not yet been validated by Azure DevOps. Linux PowerShell smoke execution remains untested.

## Local checks after the ACR decision
- Planning JSON parsed successfully; organization URL, ACR selection, hosted-agent settings,
  identity image-pull setting and unconfirmed region/resource-group placeholders were checked.
- Both pipeline YAML files parsed with the installed Azure CLI Python's PyYAML; all four Bash
  blocks passed Git Bash `bash -n` syntax checks without executing their commands.
- Both pipelines select `ubuntu-latest`. Deployment contains ACR login, agent-side Docker build/push,
  registry digest lookup and digest-pinned deployment; neither pipeline invokes ACR Tasks or GHCR.
- Existing foundation/app Bicep was inspected for disabled registry admin, AcrPull scope and
  managed-identity registry authentication. No Bicep, application or dependency changes in this step.
- Git whitespace validation passed. These are local syntax/consistency checks, not Azure DevOps
  YAML schema validation or a successful hosted build. Federated connection, registry push, actual
  managed-identity pull, runtime responses and deployment remain unverified. No cloud commands,
  Docker builds, deployments, commits or pushes were executed in this preparation step.

## Required next decisions and evidence
1. Subscription 1, centralus and rg-ai-cloud-dev are confirmed. Budget remains unapproved.
2. Foundation validation/what-if succeeded as recorded above; resolve deployment prerequisites
   and obtain resource-creation approval before any deployment.
3. The Private/Git/Basic course project and repository are verified, main is uploaded to Azure
   Repos, and CI pipeline 2/run 2 passed for the recorded code commit. GitHub origin is preserved;
   a separate azure remote is configured. No GitHub push, import or branch-policy change occurred.
   Federated service-connection configuration and deployment execution remain outstanding and
   require separate authorization. The deployment YAML was uploaded but not registered or run.
4. Scope deployment permissions to the dedicated lab; keep foundation role-assignment permission
   separate from routine application deployment. Runtime identity receives registry AcrPull only.
   Confirm the actual federated principal and required build/deployment roles before assignment.
5. Deploy only after approval; record image digest, resource names, URL, runtime logs, successful
   pipeline/run IDs, estimated ongoing cost, and target-specific cleanup instructions from evidence.

The lab is not yet deployed or ready for recording. No billable resources were created.
Cleanup target is rg-ai-cloud-dev in the confirmed subscription; deletion is not authorized. Once deployed, inventory
and confirm the dedicated group's contents before deleting that exact group and verifying removal.

## Earlier ACR cost proposal (superseded; not approved)

Central US (`centralus`) is listed for the selected subscription and by the Container Apps provider.
The proposed group `rg-aicloud-devtest-cus` does not exist. Central US is a practical central-US
location for the lab; all regional resources would be colocated. Deployment capacity is not yet
validated. Microsoft.App is currently NotRegistered; no registration was performed.

Retail rates retrieved from https://prices.azure.com/api/retail/prices on 2026-10-14:
- ACR Basic: $0.1666/day, approximately $5.00 per 30-day month, including when idle.
- ACR Tasks: $0.0001/vCPU-second after applicable free usage. Twenty five-minute builds
  at two vCPUs cost at most $1.20 before any free allowance.
- Container Apps: $0.000024/vCPU-second and $0.000003/GiB-second active usage.
  At 0.25 vCPU / 0.5 GiB, 40 running hours cost $1.08 before free allowances;
  requests cost $0.40/million before the free allowance. Zero replicas incur no compute charge.
- Log Analytics Analytics Logs ingestion: $2.76/GB after applicable free usage.
  Allow $0–$5.52 for up to 2 GB/month; 30-day retention stays within included retention.
  System logs can still incur ingestion cost when the API is inactive.
- Hot LRS blob storage: $0.0184/GB-month plus operations. The baseline writes no blobs;
  allow $0–$0.10 for negligible storage/operations. Stored data remains billable when idle.
- Resource group and managed identity: no separate charge. Consumption environment has no
  dedicated compute allocation; no private endpoint or planned-maintenance feature is proposed.

Expected light-use total: approximately $5–$15/month before tax. Suggested budget: $20/month,
pending user agreement. Assumes <=40 running hours, <=100,000 requests, <=2 GB logs,
20 small remote builds, images within Basic included storage, negligible network transfer,
and no paid Azure DevOps capacity. Free grants are shared and have not been verified as unused.
This estimate is not a spending cap; sustained traffic, logs, builds and retained images add cost.

At the time of this superseded estimate, free Microsoft-hosted capacity was unverified. A paid
Microsoft-hosted parallel job is listed at $40/month, making the estimate $45–$55/month.
Do not purchase capacity without approval. A budget alert does not stop resources automatically.

Sources: [Container Apps billing](https://learn.microsoft.com/en-us/azure/container-apps/billing),
[registry pricing](https://azure.microsoft.com/en-us/pricing/details/container-registry/),
[DevOps pricing](https://azure.microsoft.com/en-us/pricing/details/devops/azure-devops-services/),
[hosted job entitlement](https://learn.microsoft.com/en-us/azure/devops/pipelines/licensing/concurrent-jobs?view=azure-devops).
Public API pricing responses are saved locally under ignored `artifacts/centralus-*-prices.json`.

## Earlier free-services proposal (superseded; not selected)

The following records the earlier proposal, not the current implementation or an approved change.
The current decision above restores ACR and managed-identity pulls. Other infrastructure has not
been changed; in particular the existing Log Analytics definition remains intact.

- Keep Azure Repos, Azure Pipelines and Azure DevOps PR review in Zoran-DevOps-Lab. Use a free
  Microsoft-hosted Ubuntu agent for test/build/push/deployment. The user has confirmed its grant
  and unused monthly allowance; actual pipeline execution remains unverified.
  No ACR, ACR Tasks, paid agents, purchases or local Docker.
- Publish a public image at proposed `ghcr.io/zorantadic/aicloud-order-api`, pinned by digest.
  Public package storage/transfer are free under GitHub's published policy. The connected GitHub
  account owns the existing public repository and has admin permission. GHCR publishing credentials
  and successful push have not been verified. Azure Pipelines needs a classic PAT with write:packages
  stored as a protected secret, never in source/chat; first-published package visibility must be checked.
- Keep a Consumption Container Apps environment and API (0.25 vCPU, 0.5 GiB, 0–1 replicas),
  an empty Standard LRS Storage account and a user-assigned managed identity.
  Public GHCR pull is anonymous: this changes the original managed-identity image-pull requirement.
  Identity remains attached, with no baseline Storage data role; future audit work can add it.
- Prefer live console/system log streaming with no persisted log destination; capture runtime
  evidence locally. This avoids Log Analytics ingestion charges but removes historical KQL queries.
  Retaining Log Analytics instead requires verifying the shared free ingestion allowance.

Actual checks in Subscription 1:
- Subscription policy reports PayAsYouGo_2014-09-01 with spendingLimit Off.
- Current inventory lists no Container Apps, managed environments, Storage accounts or Log Analytics
  workspaces. An October 1–14 Consumption usage-details query returned zero records and no next page.
  These observations do not prove unused grants: deleted resources and delayed/unreported usage matter.
- Container Apps grants are 180,000 vCPU-seconds, 360,000 GiB-seconds and two million requests
  per subscription/month. At the proposed replica size, the compute grant corresponds to 200 running
  replica-hours if otherwise unused. Actual remaining grant and regional deployment quota are unverified.
- Storage's time-limited free-account benefit is not established by pay-as-you-go metadata.
  Its eligibility, expiry and remaining storage/operation allowances require the subscription's
  free-services table. No general always-free Blob allowance is assumed.
- Azure DevOps: authenticated project-list access to Zoran-DevOps-Lab succeeded as recorded above.
  Free hosted capacity and 0/1,800 used minutes are user-confirmed; the agent did not independently
  read those counters. Published free allowance: one concurrent job, 60 minutes/run, 1,800 minutes/month.
- Public GHCR has no paid storage/bandwidth allowance balance to exhaust under current policy;
  publishing/rate limits still apply. No package was created or changed.

Current cost limitation: ACR is not confirmed free; actual remaining Azure grants are unresolved.
Azure DevOps free capacity is
user-confirmed, but pipeline execution is untested. No paid fallback is authorized.
If Storage free eligibility is absent, nonzero stored data/operations are chargeable even at tiny
volumes. An unused empty account can have no usage charges, but that is not a free-tier entitlement.
Container Apps overage remains chargeable on this subscription. Resource creation remains blocked.

For the next read-only Azure check: Azure portal > Subscriptions > Subscription 1 > free-service
usage (benefit expiry and Usage/Limit). Missing free-service table does not establish a Storage benefit.
The Azure DevOps Parallel jobs check was completed by the user in Zoran-DevOps-Lab as recorded above.

References: [GHCR billing](https://docs.github.com/en/billing/concepts/product-billing/github-packages),
[GHCR authentication](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry),
[free-service usage](https://learn.microsoft.com/en-us/azure/cost-management-billing/manage/check-free-service-usage),
[log destinations](https://learn.microsoft.com/en-us/azure/container-apps/log-options).
