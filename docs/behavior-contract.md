# Baseline behavior contract
This is a teaching API, not a persistent order management system.
POST /orders validates product_code (1-40 uppercase letters/digits/hyphens, first character
alphanumeric) and quantity (integer 1-100). Unknown fields are rejected.
HTTP 201 returns a new UUID, submitted fields and a UTC creation timestamp.
No order data is persisted, no audit blob is written, and no GET-order endpoint exists.
The generated receipt is deliberately ephemeral. Do not claim this baseline stores orders.
GET /health returns status=ok and APP_ENVIRONMENT (default local).
Every response has a server-generated X-Correlation-ID. Structured event bodies go to stdout/stderr
via the server logger. Default HTTP access logs are disabled in the supplied launch commands.
No customer names, payment data or real personal data belong in demos.
Public cloud ingress is for a disposable synthetic-data lab, not a production security design.
