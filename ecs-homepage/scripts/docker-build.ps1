$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

param(
    [string]$ImageName = "ecs-homepage",
    [switch]$NoLatest
)

. (Join-Path $PSScriptRoot "version-utils.ps1")

$metadata = Get-EcsHomepageVersionMetadata
Assert-EcsHomepageVersionMirror -Metadata $metadata

$versionTag = "${ImageName}:$($metadata.Version)"
$dockerArgs = @(
    "build",
    "--build-arg", "ECS_HOMEPAGE_VERSION=$($metadata.Version)",
    "-t", $versionTag
)
if (-not $NoLatest) {
    $dockerArgs += @("-t", "${ImageName}:latest")
}
$dockerArgs += "."

Push-Location $metadata.ProjectRoot
try {
    & docker @dockerArgs
    if ($LASTEXITCODE -ne 0) {
        throw "docker build failed with exit code $LASTEXITCODE"
    }
    Write-Host "Docker image built: $versionTag"
}
finally {
    Pop-Location
}
