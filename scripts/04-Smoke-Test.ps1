[CmdletBinding()]
param(
    [string]$BaseUrl = 'http://127.0.0.1:8000',
    [string]$ExpectedEnvironment = ''
)
$ErrorActionPreference = 'Stop'
$BaseUrl = $BaseUrl.TrimEnd('/')
$Health = Invoke-RestMethod -Uri "$BaseUrl/health" -Method Get
if ($Health.status -ne 'ok') { throw 'Health check failed.' }
if ($ExpectedEnvironment -and $Health.environment -ne $ExpectedEnvironment) {
    throw 'Unexpected runtime environment.'
}
$Body = @{ product_code = 'DEMO-001'; quantity = 2 } | ConvertTo-Json
$Result = Invoke-WebRequest -UseBasicParsing -Uri "$BaseUrl/orders" -Method Post -ContentType 'application/json' -Body $Body
if ($Result.StatusCode -ne 201) { throw 'Expected HTTP 201.' }
$Order = $Result.Content | ConvertFrom-Json
if ($Order.product_code -ne 'DEMO-001' -or $Order.quantity -ne 2) { throw 'Unexpected response.' }
[guid]::Parse($Order.order_id) | Out-Null
if (-not $Result.Headers['X-Correlation-ID']) { throw 'Missing correlation ID.' }
[guid]::Parse([string]$Result.Headers['X-Correlation-ID']) | Out-Null
if ($Result.Headers['Cache-Control'] -ne 'no-store') { throw 'Missing no-store cache policy.' }
if (-not $Order.created_at) { throw 'Missing creation timestamp.' }
$Order | Format-List
Write-Host 'Health and order smoke checks passed.' -ForegroundColor Green
