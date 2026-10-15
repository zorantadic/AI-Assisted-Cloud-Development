# Azure preparation (later phase; not performed by the initializer)
The selected organization is Zoran-DevOps-Lab: https://dev.azure.com/Zoran-DevOps-Lab.
The Private/Git/Basic project AI-Assisted-Cloud-Development now exists, with its default Git
repository, in this organization. Project ID: 5007e9df-c7e7-4945-8f8c-b5dcf4b6bc29.
Initial repository upload and CI execution are authorized; deployment remains unauthorized.
The user verified the private-project Microsoft-hosted Free tier in this organization:
one parallel job, 1,800 minutes/month, 0 used. This capacity is user-reported, not CLI-verified.
See docs/preparation-status.md for evidence and the current proposal.
Confirmed target: Subscription 1 (`4d992bb0-6909-470c-bbef-896082984f67`), `centralus`,
resource group `rg-ai-cloud-dev`. Before deployment confirm permissions, budget,
playground suitability and resource creation approval. Copy config/azure.example.json to an ignored
azure.local.json only when actual values are known. The JSON is a planning record, not a deployment input.

Sequence:
1. Sign in with az login, verify the tenant and explicitly select the agreed subscription.
2. Review/compile lab.bicep, foundation.bicep and app.bicep. Use subscription-level validation and
   what-if with lab.bicep to include the proposed dedicated resource group before creating it.
3. Deploy foundation.bicep. It creates ACR, Storage, managed identity, log workspace and Container Apps
   environment. The identity gets AcrPull only. Storage data permission and audit container are absent.
4. Build/push the baseline image to ACR on the Microsoft-hosted Azure DevOps Ubuntu agent
   using Docker; no local Docker or ACR Tasks. Only then deploy app.bicep with foundation outputs.
   The separate files avoid attempting to pull an image from an empty registry.
5. Verify health, order contract, logs and identity. No audit behavior is expected yet.
6. Create an Azure DevOps federated service connection with reviewed permissions, then bind the manual
   dev/test pipeline parameters to actual values. Foundation deployment needs role-assignment permission;
   do not blindly grant Owner to the pipeline. Verify registry-scoped AcrPush for the build/deploy
   service connection with this RBAC registry; runtime managed identity keeps only AcrPull.
7. Run CI for the exact commit, then manually run deployment for that commit. Deployment repeats lint
   and behavior tests before the hosted-agent build/push, pins the image digest, and checks health/orders.
   Azure DevOps pipeline execution and environment checks still require live verification.

Managed identity image pull reference:
https://learn.microsoft.com/en-us/azure/container-apps/managed-identity-image-pull

Bicep and pipeline files are implementation drafts until compiled and validated against the actual
subscription and Azure DevOps project. No production deployment is included.
Container Apps can scale to zero; ACR, logs and Storage can still incur cost. Estimate with the chosen
region/SKUs before deployment. Use a dedicated resource group and document exact resource IDs for cleanup.
ACR is selected but is not confirmed free. This decision authorizes local preparation only;
region and resource-group name are confirmed, but no purchases or deployment are authorized.
After use, review that group's contents, delete only the agreed disposable group and verify deletion.
No deletion is authorized. See preparation-status.md for actual validation/what-if results.
