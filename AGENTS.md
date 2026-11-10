**# AI-Assisted Cloud Development: project guidance**

**## Verify the baseline**
\- Start with README.md and docs/behavior-contract.md; inspect relevant code and tests before asserting behavior.
\- The current FastAPI Order API exposes GET /health and POST /orders. This baseline does not persist orders or write audit blobs.
\- Keep CI build/test evidence separate from runtime configuration, Azure deployment, and observed service behavior.

**## Builder responsibility**
\- For an authorized implementation request, explicitly read ai/builder.md and the selected request under course/.
\- State the permitted files, assumptions, acceptance criteria, and validation plan before edits.
\- Do not expand scope, dependencies, resources, or identity permissions without human approval.

**## Safety and validation**
\- Do not include secrets, customer data, or personal data in files, prompts, or logs.
\- Do not push, commit, deploy, or modify cloud resources or IAM without explicit authorization.
\- After approved edits, inspect the diff, run relevant tests, and distinguish executed checks from unverified assumptions.
