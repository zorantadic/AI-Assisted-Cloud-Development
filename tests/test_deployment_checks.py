"""Exercise the fail-closed boundary before a remote deployment."""
import copy
import runpy
from pathlib import Path

import pytest

checks = runpy.run_path(str(Path(__file__).parents[1] / "scripts" / "deployment_checks.py"))
IMAGE = checks["SERVER"] + "/order-api@sha256:" + "a" * 64


def candidate():
    return {
        "id": checks["APP"], "location": "centralus",
        "identity": {"type": "UserAssigned", "userAssignedIdentities": {checks["IDENTITY"]: {}}},
        "properties": {
            "managedEnvironmentId": checks["ENVIRONMENT"],
            "configuration": {
                "activeRevisionsMode": "Single",
                "ingress": {"external": True, "allowInsecure": False, "targetPort": 8000},
                "registries": [{"server": checks["SERVER"], "identity": checks["IDENTITY"]}],
            },
            "template": {
                "scale": {"minReplicas": 0, "maxReplicas": 1},
                "containers": [{"name": "order-api", "image": IMAGE,
                                "resources": {"cpu": 0.25, "memory": "0.5Gi"},
                                "env": [{"name": "APP_ENVIRONMENT", "value": "devtest"}]}],
            },
        },
    }


def plan():
    return {"status": "Succeeded", "changes": [
        {"changeType": "Create", "resourceId": checks["APP"], "after": candidate()}]}


def test_expected_initial_app_is_allowed():
    checks["check_plan"](plan(), IMAGE)


@pytest.mark.parametrize("kind", ["Modify", "Delete", "Deploy", "Unsupported", "NoChange"])
def test_unexpected_app_change_stops_deployment(kind):
    value = plan()
    value["changes"][0]["changeType"] = kind
    with pytest.raises(ValueError):
        checks["check_plan"](value, IMAGE)


def test_additional_resource_creation_stops_deployment():
    value = plan()
    extra = copy.deepcopy(value["changes"][0])
    extra["resourceId"] = checks["ENVIRONMENT"]
    value["changes"].append(extra)
    with pytest.raises(ValueError):
        checks["check_plan"](value, IMAGE)


def test_diagnostics_stop_deployment():
    value = plan()
    value["diagnostics"] = [{"message": "Unable to evaluate"}]
    with pytest.raises(ValueError):
        checks["check_plan"](value, IMAGE)


@pytest.mark.parametrize("mutation", ["image", "scale", "identity", "https", "cpu"])
def test_configuration_drift_stops_deployment(mutation):
    value = plan()
    app = value["changes"][0]["after"]
    props = app["properties"]
    if mutation == "image":
        props["template"]["containers"][0]["image"] = "untrusted:latest"
    elif mutation == "scale":
        props["template"]["scale"]["maxReplicas"] = 2
    elif mutation == "identity":
        app["identity"]["userAssignedIdentities"] = {"unapproved": {}}
    elif mutation == "https":
        props["configuration"]["ingress"]["allowInsecure"] = True
    else:
        props["template"]["containers"][0]["resources"]["cpu"] = 0.5
    with pytest.raises(ValueError):
        checks["check_plan"](value, IMAGE)
