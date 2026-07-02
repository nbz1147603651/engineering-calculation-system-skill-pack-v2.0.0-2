$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

. (Join-Path $PSScriptRoot "version-utils.ps1")

$failures = New-Object System.Collections.Generic.List[string]

function Add-Failure {
    param([string]$Message)
    $failures.Add($Message) | Out-Null
}

function Read-ProjectText {
    param(
        [Parameter(Mandatory)][pscustomobject]$Metadata,
        [Parameter(Mandatory)][string]$RelativePath
    )
    $path = Join-Path $Metadata.ProjectRoot $RelativePath
    if (-not (Test-Path -LiteralPath $path)) {
        Add-Failure "Missing file: $RelativePath"
        return ""
    }
    return [System.IO.File]::ReadAllText($path, [System.Text.Encoding]::UTF8)
}

try {
    $metadata = Get-EcsHomepageVersionMetadata
}
catch {
    Write-Error $_.Exception.Message
    exit 1
}

try {
    Assert-EcsHomepageVersionMirror -Metadata $metadata
}
catch {
    Add-Failure $_.Exception.Message
}

$appText = Read-ProjectText -Metadata $metadata -RelativePath "src\App.tsx"
if ($appText -match "v\d+\.\d+\.\d+") {
    Add-Failure "src\App.tsx contains a hardcoded display version. Use APP_VERSION / __APP_VERSION__ instead."
}
if ($appText -notmatch "APP_VERSION") {
    Add-Failure "src\App.tsx does not reference APP_VERSION."
}

$viteText = Read-ProjectText -Metadata $metadata -RelativePath "vite.config.ts"
foreach ($needle in @("release_config.json", "version.json", "__APP_VERSION__")) {
    if (-not $viteText.Contains($needle)) {
        Add-Failure "vite.config.ts is missing '$needle'."
    }
}

$packageScriptText = Read-ProjectText -Metadata $metadata -RelativePath "scripts\package-static.ps1"
foreach ($needle in @("Assert-EcsHomepageVersionMirror", "version.json", "Get-FileHash", ".sha256")) {
    if (-not $packageScriptText.Contains($needle)) {
        Add-Failure "scripts/package-static.ps1 is missing '$needle'."
    }
}

$distVersionPath = Join-Path $metadata.ProjectRoot "dist\version.json"
if (Test-Path -LiteralPath $distVersionPath) {
    try {
        $distVersion = Get-Content -LiteralPath $distVersionPath -Raw -Encoding UTF8 | ConvertFrom-Json
        if ([string]$distVersion.version -ne $metadata.Version) {
            Add-Failure "dist/version.json version '$($distVersion.version)' does not match central version '$($metadata.Version)'."
        }
    }
    catch {
        Add-Failure "dist/version.json is not valid JSON: $($_.Exception.Message)"
    }
}

if ($failures.Count -gt 0) {
    Write-Error ("Version consistency check failed:`n - " + ($failures -join "`n - "))
    exit 1
}

Write-Host "ECS homepage version consistency OK ($($metadata.Version))"
