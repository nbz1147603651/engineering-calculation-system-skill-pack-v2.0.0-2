$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

. (Join-Path $PSScriptRoot "version-utils.ps1")

$metadata = Get-EcsHomepageVersionMetadata
Assert-EcsHomepageVersionMirror -Metadata $metadata

Push-Location $metadata.ProjectRoot
try {
    $env:ECS_HOMEPAGE_VERSION = $metadata.Version
    & docker compose up -d --build
    if ($LASTEXITCODE -ne 0) {
        throw "docker compose up failed with exit code $LASTEXITCODE"
    }
    Write-Host "Docker deployment started for ecs-homepage:$($metadata.Version)"
}
finally {
    Pop-Location
}
