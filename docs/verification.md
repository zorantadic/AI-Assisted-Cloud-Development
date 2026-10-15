# Package verification

Verified on 2026-10-14 in Linux with Python 3.12 and PowerShell 7.4.6:
- 16 API tests passed; Ruff passed.
- Both Bicep templates compiled successfully.
- All 6 PowerShell scripts parsed.
- Initializer created a fresh directory and refused an existing destination.
- PowerShell smoke test passed against a running API (health and order creation).

Not executed: Windows dependency setup, Docker build, Azure deployment, Azure DevOps pipeline,
Codex instruction loading, audit scenarios or review checkpoints.
One upstream TestClient warning reports future migration from httpx to httpx2; tests pass.
Cloud definitions remain drafts until validated in the selected subscription.

Preparation-time pip-audit of the locked development dependency set reported no known vulnerabilities.
This is not a guarantee and does not implement a pipeline security gate.
