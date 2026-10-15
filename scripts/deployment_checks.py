"""Fail-closed checks for the initial course API deployment; no Azure writes."""
import json
import os
import re
import sys
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

SUBSCRIPTION = "4d992bb0-6909-470c-bbef-896082984f67"
GROUP = f"/subscriptions/{SUBSCRIPTION}/resourceGroups/rg-ai-cloud-dev"
APP = f"{GROUP}/providers/Microsoft.App/containerApps/aicloud-order-api"
IDENTITY = f"{GROUP}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/aicloud-api-identity"
ENVIRONMENT = f"{GROUP}/providers/Microsoft.App/managedEnvironments/aicloud-environment"
SERVER = "aiclouddkldarnzw2qiw.azurecr.io"
EXISTING = {
    IDENTITY, ENVIRONMENT,
    f"{GROUP}/providers/Microsoft.ContainerRegistry/registries/aiclouddkldarnzw2qiw",
    f"{GROUP}/providers/Microsoft.Storage/storageAccounts/aiclouddkldarnzw2qiw",
    f"{GROUP}/providers/Microsoft.OperationalInsights/workspaces/aicloud-logs",
    f"{GROUP}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/aicloud-devtest-deployer",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check_app(app, image, deployed=False):
    require(re.fullmatch(re.escape(SERVER) + r"/order-api@sha256:[a-f0-9]{64}", image),
            "Expected image must use this ACR and an immutable digest")
    require(app["id"].lower() == APP.lower(), "Unexpected application ID")
    require(app["location"].replace(" ", "").lower() == "centralus", "Unexpected region")
    identity = app["identity"]
    require(identity["type"] == "UserAssigned", "Unexpected identity type")
    require({x.lower() for x in identity["userAssignedIdentities"]} == {IDENTITY.lower()},
            "Unexpected application identity")
    props = app["properties"]
    require(props["managedEnvironmentId"].lower() == ENVIRONMENT.lower(), "Unexpected environment")
    config = props["configuration"]
    require(config["activeRevisionsMode"] == "Single", "Expected single revision mode")
    ingress = config["ingress"]
    require(ingress["external"] and not ingress["allowInsecure"]
            and ingress["targetPort"] == 8000, "Unexpected ingress")
    registries = config["registries"]
    require(len(registries) == 1 and registries[0]["server"] == SERVER
            and registries[0]["identity"].lower() == IDENTITY.lower()
            and not registries[0].get("username") and not registries[0].get("passwordSecretRef"),
            "Expected managed-identity registry authentication")
    require(not config.get("secrets"), "Unexpected application secrets")
    template = props["template"]
    require(template["scale"]["minReplicas"] == 0 and template["scale"]["maxReplicas"] == 1,
            "Unexpected scaling")
    if props.get("workloadProfileName"):
        require(props["workloadProfileName"] == "Consumption", "Unexpected workload profile")
    containers = template["containers"]
    require(len(containers) == 1, "Unexpected container count")
    container = containers[0]
    require(container["name"] == "order-api" and container["image"] == image, "Image mismatch")
    require(container["resources"]["cpu"] == 0.25
            and container["resources"]["memory"] == "0.5Gi", "Unexpected CPU or memory")
    require(container["env"] == [{"name": "APP_ENVIRONMENT", "value": "devtest"}],
            "Unexpected application configuration")
    if deployed:
        require(props["provisioningState"] == "Succeeded", "Application provisioning incomplete")
        require(props["latestRevisionName"] == props["latestReadyRevisionName"],
                "Latest revision is not ready")
        require(ingress.get("fqdn"), "Missing HTTPS hostname")


def check_plan(plan, image):
    require(plan.get("status") == "Succeeded" and not plan.get("error"), "What-if did not succeed")
    require(not plan.get("diagnostics"), "What-if contains unresolved diagnostics")
    creates = []
    for change in plan.get("changes", []):
        kind = change["changeType"]
        if kind == "Create":
            require(change["resourceId"].lower() == APP.lower(), "Unexpected resource creation")
            creates.append(change)
        else:
            require(kind in {"NoChange", "Ignore"}
                    and change["resourceId"].lower() in {x.lower() for x in EXISTING},
                    f"Unexpected change: {kind} {change['resourceId']}")
    require(len(creates) == 1, "Expected exactly one application creation")
    check_app(creates[0]["after"], image)


def check_registry(registry):
    require(registry["id"].lower() ==
            f"{GROUP}/providers/Microsoft.ContainerRegistry/registries/aiclouddkldarnzw2qiw".lower(),
            "Unexpected registry")
    require(registry["adminUserEnabled"] is False, "ACR admin must remain disabled")
    require(registry["roleAssignmentMode"] == "LegacyRegistryPermissions", "Unexpected ACR RBAC mode")
    require(registry["policies"]["azureAdAuthenticationAsArmPolicy"]["status"] == "enabled",
            "ACR must accept ARM-audience tokens")


def check_ci():
    require(os.environ["SYSTEM_TEAMPROJECTID"] == "5007e9df-c7e7-4945-8f8c-b5dcf4b6bc29",
            "Unexpected project")
    require(os.environ["BUILD_REPOSITORY_ID"] == "dd8b4af5-37d7-494d-9167-a8a197250565",
            "Unexpected repository")
    require(os.environ["BUILD_SOURCEBRANCH"] == "refs/heads/main", "Deploy main only")
    query = urlencode({"definitions": 2, "statusFilter": "completed",
                       "resultFilter": "succeeded", "branchName": "refs/heads/main",
                       "queryOrder": "finishTimeDescending", "$top": 100, "api-version": "7.1"})
    url = ("https://dev.azure.com/Zoran-DevOps-Lab/"
           "5007e9df-c7e7-4945-8f8c-b5dcf4b6bc29/_apis/build/builds?" + query)
    request = Request(url, headers={"Authorization": "Bearer " + os.environ["SYSTEM_ACCESSTOKEN"]})
    with urlopen(request, timeout=60) as response:
        runs = json.load(response)["value"]
    matches = [run for run in runs if run["sourceVersion"] == os.environ["BUILD_SOURCEVERSION"]
               and run["repository"]["id"] == os.environ["BUILD_REPOSITORY_ID"]]
    require(matches, "No successful CI pipeline 2 run for this exact source SHA")
    Path("artifacts/deployment").mkdir(parents=True, exist_ok=True)
    evidence = {"id": matches[0]["id"], "sourceVersion": matches[0]["sourceVersion"],
                "result": matches[0]["result"], "url": matches[0]["_links"]["web"]["href"]}
    Path("artifacts/deployment/ci.json").write_text(json.dumps(evidence, indent=2))
    print(f"CI run {matches[0]['id']} succeeded for this exact commit")


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "ci":
        check_ci()
    else:
        data = json.loads(Path(sys.argv[2]).read_text())
        if mode == "registry":
            check_registry(data)
        elif mode == "plan":
            check_plan(data, os.environ["EXPECTED_IMAGE"])
        elif mode == "app":
            check_app(data, os.environ["EXPECTED_IMAGE"], deployed=True)
        else:
            raise ValueError("Unknown check")
        print(f"{mode} checks passed")
