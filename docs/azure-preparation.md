# Azure preparation (later phase; not performed by the initializer)
The selected organization name is ai-cloud-development-lab; creation and availability are unverified.
The project name AI-Assisted-Cloud-Development is proposed; no project or remote has been created.
Before deployment confirm tenant, subscription, region, resource group, permissions, budget,
playground suitability and exact resource names. Copy config/azure.example.json to an ignored
azure.local.json only when actual values are known. The JSON is a planning record, not a deployment input.

Sequence:
1. Sign in with az login, verify the tenant and explicitly select the agreed subscription.
2. Review/compile foundation.bicep and app.bicep; run a deployment what-if for the agreed resource group.
3. Deploy foundation.bicep. It creates ACR, Storage, managed identity, log workspace and Container Apps
   environment. The identity gets AcrPull only. Storage data permission and audit container are absent.
4. Build/push the baseline image; only then deploy app.bicep with actual foundation outputs.
   The separate files avoid attempting to pull an image from an empty registry.
5. Verify health, order contract, logs and identity. No audit behavior is expected yet.
6. Create an Azure DevOps federated service connection with reviewed permissions, then bind the manual
   dev/test pipeline parameters to actual values. Foundation deployment needs role-assignment permission;
   do not blindly grant Owner to the pipeline. ACR build availability/permissions must be checked.
7. Run CI for the exact commit, then manually run deployment for that commit; current YAML does not
   automatically enforce this relationship. Add the selected environment checks before recording if needed.

Managed identity image pull reference:
https://learn.microsoft.com/en-us/azure/container-apps/managed-identity-image-pull

Bicep and pipeline files are implementation drafts until compiled and validated against the actual
subscription and Azure DevOps project. No production deployment is included.
Container Apps can scale to zero; ACR, logs and Storage can still incur cost. Estimate with the chosen
region/SKUs before deployment. Use a dedicated resource group and document exact resource IDs for cleanup.
After use, review that group's contents, delete only the agreed disposable group and verify deletion.
No automatic deletion command is included because the target subscription/group is not yet known.
