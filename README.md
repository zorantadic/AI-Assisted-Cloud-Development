# AI-Assisted Cloud Development
A small Python/FastAPI Order API used across two AI-assisted cloud development courses.

## Current state
Local baseline source, meaningful tests, PowerShell helpers and draft cloud definitions.
No audit feature, Azure resources, remote repository or demo checkpoint is created automatically.
See docs/behavior-contract.md for exact API semantics and course/ for separate exercise plans.

## Windows quick start
Prerequisites: Python 3.13 (with the Windows py launcher), PowerShell 5.1 or 7.
Git is needed only for source control; Docker/Azure CLI are not needed for the local API.
Run from this project root:

```powershell
.\scripts\01-Setup-Local.ps1
.\scripts\02-Test-Local.ps1
.\scripts\03-Start-Local.ps1
```
Open http://127.0.0.1:8000/docs. In a second terminal run:

```powershell
.\scripts\04-Smoke-Test.ps1
```
Stop the API with Ctrl+C. No virtual-environment activation is required.
APP_ENVIRONMENT is runtime configuration; set `$env:APP_ENVIRONMENT = 'local'` if desired.
The .env.example file is documentation and is not loaded automatically.

## Files
- app/: baseline API
- tests/: behavioral checks
- scripts/: setup, test, run, smoke check and optional Git initialization
- infra/: foundation and app Bicep drafts
- pipelines/: baseline CI and manual dev/test deployment drafts
- config/: environment planning example (no credentials)
- ai/: explicitly loaded Builder/Reviewer role text
- course/: bounded tasks and rehearsal plans, separate from application code
- docs/: behavior, cloud preparation and checkpoints
- requests/: sample HTTP calls
- artifacts/: generated local evidence, ignored by Git

requirements*.txt declare direct dependency versions; requirements*.lock.txt lock the resolved
runtime/dev dependency sets. Revalidate and regenerate locks when adding the audit SDK.
Dependencies are checked during preparation; this does not replace Course 2 security evidence.
Do not paste credentials or production/customer data into the repository or AI prompts.
Learner repository publication will follow the agreed Pluralsight-managed handoff process.

Testing reference: https://fastapi.tiangolo.com/tutorial/testing/
