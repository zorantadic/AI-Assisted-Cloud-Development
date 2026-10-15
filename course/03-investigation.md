# Prepared cloud defect
Status: rehearsal plan, not an existing defect or captured evidence.
After the audit checkpoint works, use a separate controlled dev/test fixture to omit
its Blob data-plane role assignment. Do not remove the ACR pull permission.
Capture the actual failed request, sanitized SDK error, correlation ID, identity and role scope.
Ask the Builder for hypotheses based on this evidence. Verify the cause before applying a fix.
After restoring the required narrow role assignment, allow for RBAC propagation and recheck.
If the observed failure differs, investigate the actual evidence; do not script a false explanation.
Never attribute this deliberately prepared fixture to an accidental AI mistake.
