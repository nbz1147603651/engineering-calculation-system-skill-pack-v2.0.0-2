$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

. (Join-Path $PSScriptRoot "version-utils.ps1")

$metadata = Get-EcsHomepageVersionMetadata

Push-Location $metadata.ProjectRoot
try {
    npm version $metadata.Version --no-git-tag-version --allow-same-version
    Assert-EcsHomepageVersionMirror -Metadata $metadata
    Write-Host "ECS homepage npm version mirror synced to $($metadata.Version)"
}
finally {
    Pop-Location
}
