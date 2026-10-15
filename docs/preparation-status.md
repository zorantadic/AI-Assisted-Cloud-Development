# Baseline preparation — 2026-10-14

> Current user decision: ACR is the selected registry; GHCR is no longer selected. Build/push runs
> on a Microsoft-hosted Azure DevOps agent, with no local Docker and no ACR Tasks. Container Apps
> pulls from ACR with its user-assigned managed identity. Initial Azure Repos upload and hosted CI
> succeeded as recorded below; earlier Azure validation/what-if evidence is preserved.
> ACR and Log Analytics are retained. The reviewed seven-resource foundation deployment and
> its five required provider registrations are authorized for the confirmed subscription below.
> The current API step authorizes a dedicated federated deployment identity/service connection,
> scoped role assignments, manual hosted deployment, and reviewed commits/pushes to Azure Repos.
> Local Docker, ACR Tasks, foundation redeployment and changes to other projects remain excluded.
> Earlier restrictions below describe their original stages.
> Confirmed region: `centralus`; resource group: `rg-ai-cloud-dev`. Budget remains unconfirmed.
> Other architecture is unchanged.

## Baseline API deployment (2026-10-15 America/Chicago)

**Result: Succeeded. The baseline API is deployed, the healthy active revision runs the private
ACR image by digest, HTTPS smoke checks pass, and correlated application logs reached aicloud-logs.**

This is the current result. Statements about pending deployment or authorization in the dated
foundation/preparation sections below describe those earlier stages.

Working directory and Git root: `C:\Projects\AI-Assisted-Cloud-Development`. The prior uncommitted
foundation results are preserved. Verified operator/tenant/subscription match the foundation record.

- Service connection: **aicloud-devtest-wif**, ID `bf4283f7-4724-403f-a2fd-c262e6e8cad8`,
  ARM WorkloadIdentityFederation, project-specific (not shared).
- Dedicated deployment identity: **aicloud-devtest-deployer** in rg-ai-cloud-dev, centralus.
  Resource ID: `/subscriptions/4d992bb0-6909-470c-bbef-896082984f67/resourceGroups/rg-ai-cloud-dev/providers/Microsoft.ManagedIdentity/userAssignedIdentities/aicloud-devtest-deployer`.
  Client ID: `01e4cff0-d954-4fe8-8422-971b29de0c6a`.
  Principal ID: `71189a3e-c87d-4ea8-bfe7-978737191f8a`.
- Federated credential: `azure-devops-devtest`; audience `api://AzureADTokenExchange`.
  Actual generated issuer: `https://login.microsoftonline.com/b7fddbde-dfdf-425e-a785-97d3b91909a0/v2.0`.
  Actual generated subject: `/eid1/c/pub/t/3tv9t9_fXkKnhZfTuRkJoA/a/rISbSSETf0KqFyZ8ppdXmA/sc/a54ca4a6-92c6-4754-a67f-0ec8446a8547/bf4283f7-4724-403f-a2fd-c262e6e8cad8`.
  Both values came from Azure DevOps and were used verbatim; no client secret was created.
- Manual deployment pipeline **3**, **AI-Assisted-Cloud-Development-Deploy-Devtest**, is bound to
  this project's Azure repository and `pipelines/deploy-devtest.yml`. Creation skipped the first run.
  Only pipeline 3 is authorized for the connection. The authorization GET lists only pipeline 3;
  `allPipelines` is null (no all-pipeline grant), not an invented explicit false response.
- ACR read-back: `LegacyRegistryPermissions` (registry RBAC); ARM-audience authentication
  `enabled`; admin credentials disabled. Existing app identity's ACR-scoped AcrPull is preserved.

| Deployment identity role | Actual assignment scope | Role / assignment ID |
| --- | --- | --- |
| AI Cloud Devtest App Deployer (custom) | `/subscriptions/4d992bb0-6909-470c-bbef-896082984f67/resourceGroups/rg-ai-cloud-dev` | Role `6fb939c8-f691-4aa2-a3b0-32c92d25e594`; assignment `0f4b5afb-38e2-43d7-9e63-60c4779fbb4e` |
| AcrPush | The same RG's `Microsoft.ContainerRegistry/registries/aiclouddkldarnzw2qiw` only | Role `8311e382-0749-4cb8-b61a-304f252e45ec`; assignment `a58d1b3b-3d90-4056-a94e-7fe134f4654e` |
| Managed Identity Operator | The same RG's `Microsoft.ManagedIdentity/userAssignedIdentities/aicloud-api-identity` only | Role `f1a07417-d97a-45cb-824c-7a7467783830`; assignment `308e0bd9-425d-4b3f-b86d-925cde398744` |

The custom role is recorded in `config/deployment-role.json`; its assignable scope is only this RG.
It permits app read/write, environment read/join, foundation identity/registry reads, and ARM
deployment validation/what-if/execution reads/writes. It grants no foundation resource writes,
deletes, role management or subscription-wide permissions. Managed Identity Operator is confined
to the runtime identity, so its built-in auxiliary permissions do not apply across the RG.
The deployment identity is separate from the runtime identity and has no Storage data role.

The manual pipeline requires a successful CI pipeline 2 run for its exact main-branch source SHA.
It repeats dependency integrity, lint and behavior tests, checks registry authentication, builds
and pushes on Microsoft-hosted Ubuntu, resolves the actual ACR digest, validates the unchanged
application Bicep and inspects full what-if before execution. The initial-deployment guard permits
exactly one app Create with the reviewed identity/environment, HTTPS, digest, CPU/memory and scale;
it fails on modifications, deletions, additional creates, diagnostics or unexpected resource IDs.
It intentionally does not authorize subsequent app updates. Application code and the audit exercise
are unchanged. The successful runs and runtime evidence are recorded below.

Implementation references: [Microsoft federation automation](https://learn.microsoft.com/en-us/azure/devops/pipelines/release/automate-service-connections?view=azure-devops),
[managed-identity image pull](https://learn.microsoft.com/en-us/azure/container-apps/managed-identity-image-pull).
The federation sequence follows the documented identity -> connection -> actual issuer/subject
-> federated credential order. The documentation's broad sample role grant was replaced by the
bounded roles above.

### Exact source, hosted execution and runtime verification

| Evidence | Verified result |
| --- | --- |
| Deployment source SHA | `62ef8628de19fce2bcced9622787266a51466a81` |
| Source upload | Reviewed commit pushed only to Azure Repos main after ancestry verification; GitHub origin preserved |
| CI | Pipeline **2**, [run **3**](https://dev.azure.com/Zoran-DevOps-Lab/5007e9df-c7e7-4945-8f8c-b5dcf4b6bc29/_build/results?buildId=3), **succeeded** for exactly that SHA |
| CI checks | Python 3.13.16 on Microsoft-hosted Ubuntu; locked dependency install, pip check, Ruff, **29 tests**, JUnit publication, three Bicep compilations and image build passed |
| Deployment | Pipeline **3**, [run **4**](https://dev.azure.com/Zoran-DevOps-Lab/5007e9df-c7e7-4945-8f8c-b5dcf4b6bc29/_build/results?buildId=4), **succeeded** for exactly that SHA; manual trigger |
| Deployment gates | Exact-commit CI check, repeated dependency/lint/29-test checks, workload federation login, registry authentication checks, hosted Docker build/push, validation, what-if, app read-back and existing PowerShell smoke script all passed |
| ACR tag | `order-api:62ef8628de19fce2bcced9622787266a51466a81-4` |
| Actual ACR/deployed digest | `sha256:51986077f0254fd851cf9e28796c34bb62a5440e6794d1dfc36e7f48f5ea0417` |
| Deployed image | `aiclouddkldarnzw2qiw.azurecr.io/order-api@sha256:51986077f0254fd851cf9e28796c34bb62a5440e6794d1dfc36e7f48f5ea0417` |
| Provider validation | Succeeded, error null; correlation `e93e7868-9666-4950-a916-5ee7669d93a5` |
| Full what-if | **1 Create: aicloud-order-api; 0 Modify; 0 Delete**. Four Ignore entries were the existing environment, ACR and two identities; no unexpected IDs or diagnostics |
| ARM deployment ID | `/subscriptions/4d992bb0-6909-470c-bbef-896082984f67/resourceGroups/rg-ai-cloud-dev/providers/Microsoft.Resources/deployments/api-4` |
| ARM result | Succeeded; correlation `995db8b3-2760-4f7a-9c1e-ae1454cc000b`; duration 19.64 seconds; terminal timestamp 2026-10-15 15:16:00 UTC |
| App resource ID | `/subscriptions/4d992bb0-6909-470c-bbef-896082984f67/resourceGroups/rg-ai-cloud-dev/providers/Microsoft.App/containerApps/aicloud-order-api` |
| Active revision | `aicloud-order-api--wkvvz1z`; active=true, Healthy, Provisioned; latest revision equals latest ready revision; 100% traffic |
| API URL | https://aicloud-order-api.calmpond-4d0b6792.centralus.azurecontainerapps.io |
| Actual app settings | centralus, existing aicloud-environment, 0.25 vCPU, 0.5 GiB, min 0 / max 1 replica, Single revision, HTTPS external ingress on target port 8000, APP_ENVIRONMENT=devtest |
| Runtime image identity | aicloud-api-identity, principal `7662094f-69d6-450a-80cd-fd8030ec80ca`; only its existing ACR-scoped AcrPull assignment |
| Run completion | CI 15:13:38 UTC / 10:13:38 CDT; deployment 15:16:26 UTC / 10:16:26 CDT on October 15 |

The actual registry digest was independently read back and exactly matches the active revision.
The registry's admin and anonymous pulls are both disabled. The app's registry configuration
selects only aicloud-api-identity, with empty username/passwordSecretRef and no application secrets.
Together with the healthy running private-image revision and successful HTTPS requests, this
verifies the configured managed-identity pull path in operation. No separate token-exchange trace
is claimed. A bounded system-log query returned zero rows at the time of collection; it is not
used as proof of a particular pull event.

The Consumption environment is unchanged; the app has the planned resource limits. One replica
was running at read-back (`RunningAtMaxScale` with maximum 1). This does not prove idle scale-to-zero
timing. The foundation deployment still has its original timestamp and correlation ID; it was not
redeployed. Final RG inventory contains the original five service resources plus the authorized
deployment identity and Container App, with no additional service resources.

The existing `scripts/04-Smoke-Test.ps1` passed on the hosted Ubuntu agent using synthetic
DEMO-001 / quantity 2. An independent HTTPS check at 15:18 UTC returned health HTTP **200**,
status **ok**, environment **devtest**, and order HTTP **201** with the expected product/quantity,
UUID order ID, creation timestamp, UUID X-Correlation-ID and Cache-Control **no-store**.
Synthetic order: `57596616-00e8-44dd-bcee-e927835acf8f`.
Correlation ID: `6a56185e-595e-4c14-978a-da948f66eff9`.

Log Analytics link was read back as destination `log-analytics`, workspace customer ID
`20d3b0d1-db90-4db1-9882-606abba560a3` (aicloud-logs). An initial query had no rows; a later
query after ingestion found **both** `order_created` and `http_request_completed` with HTTP 201,
the exact correlation ID above, and revision `aicloud-order-api--wkvvz1z`, timestamp
**2026-10-15T15:18:09.0003456Z**. The order_created event also matches the returned order ID.
This verifies application-log ingestion, beyond the previously verified configuration link.
Query: `ContainerAppConsoleLogs_CL`, filtered to this app and the synthetic correlation/order
events within one hour. No new logging feature or audit implementation was added.

Sanitized local evidence remains ignored under `artifacts/api-deployment-20261015/`:
connection/federation metadata, pipeline authorization, CI/deployment task results and run IDs,
downloaded hosted `deployment-evidence` (validation, full what-if, image, app and deployment),
independent app/revision read-back, smoke responses, console/system query results and the
verification summary. No credentials, tokens or registry/workspace keys are stored.
The initial connection setup required two configuration corrections before success: remove a local
UTF-8 BOM rejected by the CLI, then remove unsupported resourceGroup connection metadata.
RBAC scopes stayed narrow. CI and deployment each succeeded on their first actual run; no retry,
duplicate run, permission expansion or test weakening was needed.

**Remaining blockers: none for this baseline deployment.** The audit course feature and Storage
data permissions remain absent by design. Budget enforcement and idle scaling timing are not
claimed as verified. Future application updates need a separately reviewed what-if allowance:
the current guard intentionally permits only the initial app creation. No local Docker, ACR Tasks,
capacity purchase, foundation redeployment or other-project change occurred.

The final documentation receipt is committed/pushed to Azure Repos with `[skip ci]`. That receipt
does not change the tested/deployed source SHA above and does not trigger another CI or deployment
run. GitHub origin is preserved and was not pushed.

## Foundation deployment execution (2026-10-15 America/Chicago)

**Result: Succeeded. All seven reviewed foundation objects were created and verified.**

The user authorized the reviewed foundation deployment while retaining ACR and Log Analytics:
subscription `4d992bb0-6909-470c-bbef-896082984f67`, resource group `rg-ai-cloud-dev`, region
`centralus`. Working directory and Git root were confirmed as
`C:\Projects\AI-Assisted-Cloud-Development`; the initial working tree was clean. The signed-in
operator was `zoran@zoranitprofessional.onmicrosoft.com`, tenant
`b7fddbde-dfdf-425e-a785-97d3b91909a0`, in the confirmed Enabled subscription. Provider/resource/deployment CLI commands used that
explicit subscription; direct ARM reads used its resource IDs. No DevOps project or pipeline was recreated.

### Registration, refreshed gates and deployment

- Registered exactly Microsoft.App, Microsoft.ContainerRegistry, Microsoft.Storage,
  Microsoft.ManagedIdentity and Microsoft.OperationalInsights. Each was NotRegistered before
  this step and was read back Registered before validation. No other provider registration was
  requested. The resource group was absent and both reviewed global resource names were available.
- Refreshed full provider/RBAC validation succeeded (error null), correlation
  `28d58a20-bf0e-43e3-8371-8d31d1436b12`.
- Refreshed full-payload what-if: **7 Create, 0 Modify, 0 Delete**, no diagnostics. Exact IDs,
  names, centralus placement, SKUs, security settings, retention, log link and role scope matched
  the seven reviewed creations. No change types were hidden or excluded.
- Used the unchanged `infra/lab.bicepparam` -> `infra/lab.bicep` -> `infra/foundation.bicep`
  entry point/module. Source hashes were checked before submission and after provisioning;
  no template, parameter or architecture substitution was made.
- Subscription deployment: **foundation-20261015**, **Succeeded**, error null.
- Deployment ID: `/subscriptions/4d992bb0-6909-470c-bbef-896082984f67/providers/Microsoft.Resources/deployments/foundation-20261015`.
- Nested deployment: **baseline-foundation**, **Succeeded**, error null.
- Nested deployment ID: `/subscriptions/4d992bb0-6909-470c-bbef-896082984f67/resourceGroups/rg-ai-cloud-dev/providers/Microsoft.Resources/deployments/baseline-foundation`.
- Correlation ID: `01c3d703-4457-4ba1-9c38-130f29646520`.
- ARM terminal-state timestamp: **2026-10-15 09:31:01 CDT** (14:31:01 UTC).
- Duration: **16 minutes 12.8 seconds**. The environment temporarily reported Waiting; it later
  reached Succeeded. No deployment retry, cleanup or permission workaround was performed.

### Actual resource IDs and configurations

| Object | Actual resource ID | Verified result/configuration |
| --- | --- | --- |
| Resource group | `/subscriptions/4d992bb0-6909-470c-bbef-896082984f67/resourceGroups/rg-ai-cloud-dev` | Succeeded; centralus; course/devtest tags |
| ACR | `/subscriptions/4d992bb0-6909-470c-bbef-896082984f67/resourceGroups/rg-ai-cloud-dev/providers/Microsoft.ContainerRegistry/registries/aiclouddkldarnzw2qiw` | Succeeded; Basic; admin disabled; aiclouddkldarnzw2qiw.azurecr.io |
| Storage | `/subscriptions/4d992bb0-6909-470c-bbef-896082984f67/resourceGroups/rg-ai-cloud-dev/providers/Microsoft.Storage/storageAccounts/aiclouddkldarnzw2qiw` | Succeeded; StorageV2 / Standard_LRS; TLS1_2; HTTPS only; public blob and shared-key access disabled |
| User-assigned identity | `/subscriptions/4d992bb0-6909-470c-bbef-896082984f67/resourcegroups/rg-ai-cloud-dev/providers/Microsoft.ManagedIdentity/userAssignedIdentities/aicloud-api-identity` | GET verified; creation operation Succeeded; principal 7662094f-69d6-450a-80cd-fd8030ec80ca |
| Log Analytics | `/subscriptions/4d992bb0-6909-470c-bbef-896082984f67/resourceGroups/rg-ai-cloud-dev/providers/Microsoft.OperationalInsights/workspaces/aicloud-logs` | Succeeded; PerGB2018; retention 30 days; customer ID 20d3b0d1-db90-4db1-9882-606abba560a3 |
| Container Apps environment | `/subscriptions/4d992bb0-6909-470c-bbef-896082984f67/resourceGroups/rg-ai-cloud-dev/providers/Microsoft.App/managedEnvironments/aicloud-environment` | Succeeded; centralus (API display: Central US); one Consumption workload profile, no dedicated profile |
| AcrPull assignment | `/subscriptions/4d992bb0-6909-470c-bbef-896082984f67/resourcegroups/rg-ai-cloud-dev/providers/Microsoft.ContainerRegistry/registries/aiclouddkldarnzw2qiw/providers/Microsoft.Authorization/roleAssignments/d33eff47-f660-508d-9315-47ec6ebe8183` | GET verified; creation operation Succeeded; role 7f951dda-4ed3-4680-a7ca-43fe172d538d; exact ACR scope |

Identity client ID: `f83d87a1-d67e-46b0-b924-0d45e6d69522`. The AcrPull assignment's
`principalId` exactly equals the app identity principal, its scope exactly equals this ACR ID,
and its role definition is AcrPull. No Contributor/Owner or broader-scope role was granted.
Identity and role GET responses do not expose a provisioningState here; their recorded **Succeeded**
status comes from the deployment operations, not an invented GET property.

The environment's `appLogsConfiguration.destination` is **log-analytics** and its customer ID
**20d3b0d1-db90-4db1-9882-606abba560a3** matches the actual aicloud-logs workspace. Final
GET reports one **Consumption** workload profile, no dedicated profiles, no additional infrastructure
resource group and no deployment error. This verifies the configuration link; application log
ingestion and managed-identity image pulling are not claimed as runtime-tested.

Final target-group inventory contains exactly the five reviewed service resources (ACR, Storage,
identity, workspace, environment), plus the separately verified resource group and registry-scoped
role assignment: **seven foundation objects**. The nested ARM deployment is metadata, not an eighth
service. No Container App/API or unexpected target-group service resource was present.

Sanitized, ignored local evidence: `artifacts/foundation-deployment-20261015/` contains
`provider-registration.json`, `preflight.json`, `deployment-activity.json` and `readback.json`.
These record source hashes, matched what-if, IDs, configurations, relationships and successful
operations. Keys, tokens and raw secret-bearing responses are not saved.

### Remaining stages and boundaries

There is no remaining provisioning blocker for this foundation at final read-back. The API is
**not deployed**. A future application stage still needs separately authorized scoped deployment
credentials/service connection, an actual ACR image push and immutable digest, application
validation/deployment and runtime checks for health/orders, managed-identity image pull and logs.
The earlier passing CI image build did not push an image and does not prove these runtime paths.
No budget/spend-limit enforcement is claimed.

No local Docker, API deployment, service connection creation, deployment-pipeline execution,
resource deletion, commit or push occurred in this step. Existing CI and DevOps configuration
were left unchanged. Only this tracked status document is modified; generated deployment evidence
remains ignored. Earlier resource-absence/NotRegistered/no-deployment statements below describe
historical checks and do not override this completed foundation result.

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

## Historical target validation and what-if (2026-10-14 America/Chicago)

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

## Historical next decisions and evidence (before foundation/API execution)
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
