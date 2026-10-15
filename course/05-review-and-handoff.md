# Course 2 continuity
Use the same candidate change set and original audit request from Course 1.
Open a fresh Reviewer context and explicitly load ai/reviewer.md.
Record baseline/candidate commit IDs. Inspect actual changes and validation evidence.
Baseline CI includes tests, lint, Bicep compilation and image build only.
Before Course 2 recording add and rehearse dependency scanning, secret detection and
representative policy/security checks. Select tools and lock versions; do not imply these
checks currently exist or that any invented finding was observed.
Validate findings independently. Revise/split/reject/escalate as supported by evidence.
Prepare an Azure DevOps PR containing scope, checks, deployment impact, unresolved risks,
reviewer focus areas and required human reviewers. Do not merge or deploy to production.
