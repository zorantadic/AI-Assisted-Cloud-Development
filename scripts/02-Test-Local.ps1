[CmdletBinding()]
param()
$ErrorActionPreference = 'Stop'
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $ProjectRoot '.venv\Scripts\python.exe'
if (-not (Test-Path $Python)) { throw 'Run scripts\01-Setup-Local.ps1 first.' }
Push-Location $ProjectRoot
try {
    New-Item -ItemType Directory -Path artifacts -Force | Out-Null
    & $Python -m ruff check app tests
    if ($LASTEXITCODE -ne 0) { throw 'Lint failed.' }
    & $Python -m pytest -q --junitxml=artifacts/local-tests.junit.xml
    if ($LASTEXITCODE -ne 0) { throw 'Tests failed.' }
} finally { Pop-Location }
