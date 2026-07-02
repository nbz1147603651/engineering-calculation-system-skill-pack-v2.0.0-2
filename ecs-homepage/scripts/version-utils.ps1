$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

function Get-EcsHomepageProjectRoot {
    return (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
}

function Get-EcsHomepageVersionMetadata {
    $projectRoot = Get-EcsHomepageProjectRoot
    $repoRoot = (Resolve-Path (Join-Path $projectRoot "..")).Path
    $releaseConfigPath = Join-Path $repoRoot "engineering-calculation-system\tools\release_config.json"
    $packageJsonPath = Join-Path $projectRoot "package.json"
    $packageLockPath = Join-Path $projectRoot "package-lock.json"

    if (-not (Test-Path -LiteralPath $releaseConfigPath)) {
        throw "Missing central version file: $releaseConfigPath"
    }
    if (-not (Test-Path -LiteralPath $packageJsonPath)) {
        throw "Missing package.json: $packageJsonPath"
    }

    $releaseConfig = Get-Content -LiteralPath $releaseConfigPath -Raw -Encoding UTF8 | ConvertFrom-Json
    $version = [string]$releaseConfig.version
    if ($version -notmatch "^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$") {
        throw "release_config.json version is not valid semver: $version"
    }

    return [pscustomobject]@{
        Version = $version
        CreatedAt = [string]$releaseConfig.created_at
        ProjectRoot = $projectRoot
        RepoRoot = $repoRoot
        ReleaseConfigPath = $releaseConfigPath
        PackageJsonPath = $packageJsonPath
        PackageLockPath = $packageLockPath
    }
}

function Assert-EcsHomepageVersionMirror {
    param(
        [Parameter(Mandatory)]
        [pscustomobject]$Metadata
    )

    $failures = New-Object System.Collections.Generic.List[string]
    $packageJson = Get-Content -LiteralPath $Metadata.PackageJsonPath -Raw -Encoding UTF8 | ConvertFrom-Json
    if ([string]$packageJson.version -ne $Metadata.Version) {
        $failures.Add("package.json version '$($packageJson.version)' does not match central version '$($Metadata.Version)'") | Out-Null
    }

    if (Test-Path -LiteralPath $Metadata.PackageLockPath) {
        $packageLockText = [System.IO.File]::ReadAllText($Metadata.PackageLockPath, [System.Text.Encoding]::UTF8)
        $rootVersionMatch = [regex]::Match($packageLockText, '(?m)^\s*"version"\s*:\s*"([^"]+)"')
        if (-not $rootVersionMatch.Success) {
            $failures.Add("package-lock.json root version was not found") | Out-Null
        }
        elseif ($rootVersionMatch.Groups[1].Value -ne $Metadata.Version) {
            $failures.Add("package-lock.json root version '$($rootVersionMatch.Groups[1].Value)' does not match central version '$($Metadata.Version)'") | Out-Null
        }

        $rootPackageMatch = [regex]::Match(
            $packageLockText,
            '"packages"\s*:\s*\{\s*""\s*:\s*\{.*?"version"\s*:\s*"([^"]+)"',
            [System.Text.RegularExpressions.RegexOptions]::Singleline
        )
        if (-not $rootPackageMatch.Success) {
            $failures.Add("package-lock.json packages[''] version was not found") | Out-Null
        }
        elseif ($rootPackageMatch.Groups[1].Value -ne $Metadata.Version) {
            $failures.Add("package-lock.json packages[''] version '$($rootPackageMatch.Groups[1].Value)' does not match central version '$($Metadata.Version)'") | Out-Null
        }
    }

    if ($failures.Count -gt 0) {
        throw "Version mirror check failed:`n - $($failures -join "`n - ")"
    }
}

function Get-EcsHomepageSafeVersion {
    param([Parameter(Mandatory)][string]$Version)
    return $Version -replace "[^A-Za-z0-9._-]", "-"
}
