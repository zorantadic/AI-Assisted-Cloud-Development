[CmdletBinding()]
param([string]$PythonExe = '')
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$ProjectRoot = Split-Path -Parent $PSScriptRoot
Push-Location $ProjectRoot
try {
    if (-not (Test-Path '.venv\Scripts\python.exe')) {
        if ($PythonExe) { & $PythonExe -m venv .venv }
        elseif (Get-Command py -ErrorAction SilentlyContinue) { & py -3.13 -m venv .venv }
        else { throw 'Install Python 3.13, or pass -PythonExe with its full executable path.' }
        if ($LASTEXITCODE -ne 0) { throw 'Virtual environment creation failed.' }
    }
    $Python = Join-Path $ProjectRoot '.venv\Scripts\python.exe'
    & $Python -c "import sys; assert sys.version_info[:2] == (3, 13), 'Python 3.13 required'"
    if ($LASTEXITCODE -ne 0) { throw 'Unexpected Python version.' }
    & $Python -m pip install -r requirements-dev.lock.txt
    if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed.' }
    Write-Host 'Local dependencies installed. Next: .\scripts\02-Test-Local.ps1' -ForegroundColor Green
} finally { Pop-Location }
