[CmdletBinding()]
param()
$ErrorActionPreference = 'Stop'
$ProjectRoot = Split-Path -Parent $PSScriptRoot
if (-not (Get-Command git -ErrorAction SilentlyContinue)) { throw 'Install Git first.' }
Push-Location $ProjectRoot
try {
    & git rev-parse --show-toplevel 2>$null | Out-Null
    if ($LASTEXITCODE -eq 0) { throw 'Already inside a Git repository; no changes made.' }
    & git init -b main
    if ($LASTEXITCODE -ne 0) { throw 'Git initialization failed.' }
    Write-Host 'Repository initialized. Review git status before staging and committing.'
    Write-Host 'No commit, remote, push, or Azure DevOps project was created.'
} finally { Pop-Location }
