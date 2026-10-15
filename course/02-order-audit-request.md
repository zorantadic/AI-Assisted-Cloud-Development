# Work request: successful-order audit
Status: implementation task for Course 1; not implemented in baseline.

Add one private Azure Blob JSON audit record for each successful order creation.
Include order_id, product_code, quantity, created_at (UTC) and correlation_id.
Use the application's managed identity at runtime; no connection strings or storage keys.
Introduce explicit runtime settings for the blob service URL and audit container name.
Create the container and narrowly scoped Blob data permission through app-level Bicep.
Preserve input validation, response fields and HTTP 201 for successful requests.

Proposed failure contract: if audit storage fails, do not return success. Return a sanitized
HTTP 503, log the correlation ID and safe diagnostic fields, and avoid exposing credentials.
Confirm this contract before implementation. No exactly-once or durable-order claim is made;
retries can create another identifier. Durable order persistence and idempotency are out of scope.

Allowed areas: app, tests, dependency manifests/locks, runtime configuration and app-level Bicep.
Do not add databases, user accounts, payments, new cloud services or production deployment.
Review the scaffold before treating it as complete. Update lock files when dependencies change.

Acceptance: successful 201 has matching real blob evidence; invalid inputs create no audit;
Storage failures follow the confirmed contract; tests cover success and failure without live Azure;
actual dev/test identity, configuration, deployment and logs validate the cloud behavior.
