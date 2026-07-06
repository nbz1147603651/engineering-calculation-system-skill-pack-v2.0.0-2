param(
    [string]$Version = "",
    [switch]$SkipBuild
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

. (Join-Path $PSScriptRoot "version-utils.ps1")

$metadata = Get-EcsHomepageVersionMetadata
Assert-EcsHomepageVersionMirror -Metadata $metadata

if ([string]::IsNullOrWhiteSpace($Version)) {
    $Version = $metadata.Version
}
elseif ($Version -ne $metadata.Version) {
    throw "Static package version '$Version' must match central version '$($metadata.Version)' from release_config.json."
}

$root = $metadata.ProjectRoot
$safeVersion = $Version -replace "[^A-Za-z0-9._-]", "-"
$releaseDir = Join-Path $root "release"
$packageName = "ecs-homepage-$safeVersion-linux-web"
$stagingRoot = Join-Path $releaseDir "staging"
$packageRoot = Join-Path $stagingRoot $packageName
$zipPath = Join-Path $releaseDir "$packageName.zip"
$hashPath = "$zipPath.sha256"
$repoRoot = Split-Path -Parent $root
$guiInstallerName = "engineering-calc-system-installer-v$Version.exe"
$uiClientRoot = Join-Path $repoRoot "engineering-calculation-system\dist\ui-client"
$guiInstallerSource = Join-Path $uiClientRoot $guiInstallerName
$guiChecksumsSource = Join-Path $uiClientRoot "CHECKSUMS.txt"

function Assert-ChildPath {
    param(
        [Parameter(Mandatory)][string]$Path,
        [Parameter(Mandatory)][string]$Parent
    )

    $resolvedPath = [System.IO.Path]::GetFullPath($Path)
    $resolvedParent = [System.IO.Path]::GetFullPath($Parent)
    if (-not $resolvedPath.StartsWith($resolvedParent, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Refusing to operate outside release directory: $resolvedPath"
    }
}

function Copy-DirectoryContents {
    param(
        [Parameter(Mandatory)][string]$Source,
        [Parameter(Mandatory)][string]$Destination
    )

    if (-not (Test-Path -LiteralPath $Source)) {
        throw "Missing source directory: $Source"
    }
    New-Item -ItemType Directory -Force -Path $Destination | Out-Null
    Get-ChildItem -LiteralPath $Source -Force | ForEach-Object {
        Copy-Item -LiteralPath $_.FullName -Destination $Destination -Recurse -Force
    }
}

function Copy-GuiInstallerDownload {
    param(
        [Parameter(Mandatory)][string]$DestinationRoot
    )

    $downloadsRoot = Join-Path $DestinationRoot "downloads"
    New-Item -ItemType Directory -Force -Path $downloadsRoot | Out-Null
    Copy-Item -LiteralPath $guiInstallerSource -Destination (Join-Path $downloadsRoot $guiInstallerName) -Force
    if (Test-Path -LiteralPath $guiChecksumsSource) {
        Copy-Item -LiteralPath $guiChecksumsSource -Destination (Join-Path $downloadsRoot "CHECKSUMS.txt") -Force
    }
}

function New-LinuxFriendlyZip {
    param(
        [Parameter(Mandatory)][string]$SourceDirectory,
        [Parameter(Mandatory)][string]$DestinationZip,
        [Parameter(Mandatory)][string]$EntryRootName
    )

    Add-Type -AssemblyName System.IO.Compression
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    if (Test-Path -LiteralPath $DestinationZip) {
        Remove-Item -LiteralPath $DestinationZip -Force
    }

    $sourceFullPath = [System.IO.Path]::GetFullPath($SourceDirectory)
    $zip = [System.IO.Compression.ZipFile]::Open($DestinationZip, [System.IO.Compression.ZipArchiveMode]::Create)
    try {
        Get-ChildItem -LiteralPath $SourceDirectory -Recurse -File -Force | ForEach-Object {
            $fileFullPath = [System.IO.Path]::GetFullPath($_.FullName)
            $relativePath = $fileFullPath.Substring($sourceFullPath.Length).TrimStart([System.IO.Path]::DirectorySeparatorChar, [System.IO.Path]::AltDirectorySeparatorChar)
            $entryName = (($EntryRootName.TrimEnd("/") + "/" + $relativePath) -replace "\\", "/")
            [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile(
                $zip,
                $_.FullName,
                $entryName,
                [System.IO.Compression.CompressionLevel]::Optimal
            ) | Out-Null
        }
    }
    finally {
        $zip.Dispose()
    }
}

Push-Location $root
try {
    if (-not $SkipBuild) {
        npm run build
    }

    & (Join-Path $PSScriptRoot "check-version.ps1")

    $indexPath = Join-Path $root "dist\index.html"
    if (-not (Test-Path -LiteralPath $indexPath)) {
        throw "dist/index.html was not found. Run npm run build first."
    }
    $versionManifestPath = Join-Path $root "dist\version.json"
    if (-not (Test-Path -LiteralPath $versionManifestPath)) {
        throw "dist/version.json was not found. The Vite version manifest plugin did not run."
    }
    $versionManifest = Get-Content -LiteralPath $versionManifestPath -Raw -Encoding UTF8 | ConvertFrom-Json
    if ([string]$versionManifest.version -ne $Version) {
        throw "dist/version.json version '$($versionManifest.version)' does not match package version '$Version'."
    }
    if (-not (Test-Path -LiteralPath $guiInstallerSource)) {
        throw "GUI installer download is missing: $guiInstallerSource. Build it first with `python engineering-calculation-system/tools/build_release.py --profile ui-client`."
    }

    New-Item -ItemType Directory -Force -Path $releaseDir | Out-Null
    Assert-ChildPath -Path $stagingRoot -Parent $releaseDir
    if (Test-Path -LiteralPath $stagingRoot) {
        Remove-Item -LiteralPath $stagingRoot -Recurse -Force
    }
    New-Item -ItemType Directory -Force -Path $packageRoot | Out-Null

    if (Test-Path -LiteralPath $zipPath) {
        Remove-Item -LiteralPath $zipPath -Force
    }
    if (Test-Path -LiteralPath $hashPath) {
        Remove-Item -LiteralPath $hashPath -Force
    }

    $siteRoot = Join-Path $packageRoot "site"
    Copy-DirectoryContents -Source (Join-Path $root "dist") -Destination $siteRoot
    Copy-DirectoryContents -Source (Join-Path $root "dist") -Destination (Join-Path $siteRoot "home")
    Copy-GuiInstallerDownload -DestinationRoot $siteRoot
    Copy-Item -LiteralPath (Join-Path $root "deploy") -Destination $packageRoot -Recurse -Force

    $manifest = [ordered]@{
        name = "ecs-homepage"
        version = $Version
        packageType = "linux-static-nginx"
        packageRoot = $packageName
        siteRoot = "site"
        installScript = "deploy/linux/deploy.sh"
        nginxTemplate = "deploy/nginx/ecs-homepage-linux.conf.template"
        versionManifest = "site/version.json"
        guiInstaller = "site/downloads/$guiInstallerName"
        downloadPaths = @("/downloads/$guiInstallerName")
        defaultInstallRoot = "/opt/ecs-homepage"
        defaultNginxConf = "/etc/nginx/conf.d/ecs-homepage.conf"
        healthChecks = @("/", "/home/", "/healthz", "/version.json")
        automation = [ordered]@{
            verifyChecksum = "sha256sum -c $(Split-Path $hashPath -Leaf)"
            deployCommand = "sudo bash deploy/linux/deploy.sh"
            deployWithDomain = "sudo ECS_HOMEPAGE_SERVER_NAME=example.com bash deploy/linux/deploy.sh"
            skipNginx = "sudo ECS_HOMEPAGE_SKIP_NGINX=1 bash deploy/linux/deploy.sh"
        }
    }
    $manifestJson = $manifest | ConvertTo-Json -Depth 8
    [System.IO.File]::WriteAllText(
        (Join-Path $packageRoot "deployment-manifest.json"),
        $manifestJson + [Environment]::NewLine,
        [System.Text.UTF8Encoding]::new($false)
    )
    [System.IO.File]::WriteAllText(
        (Join-Path $packageRoot "VERSION"),
        $Version + [Environment]::NewLine,
        [System.Text.UTF8Encoding]::new($false)
    )

    $readme = @'
# ECS Homepage Linux Web Package

Version: {{VERSION}}

This package is ready for a Linux cloud server running Nginx. It contains the
built static homepage, a `/home/` compatibility copy, an Nginx template, and a
non-interactive deployment script for human operators or cloud agents.

## Contents

- `site/` - static web root for `/`.
- `site/home/` - compatibility copy for `/home/`.
- `site/version.json` - release identity served by the website.
- `site/downloads/{{GUI_INSTALLER_NAME}}` - GUI installer served from `/downloads/`.
- `deploy/linux/deploy.sh` - idempotent Linux deployment script.
- `deploy/nginx/ecs-homepage-linux.conf.template` - Nginx server block template.
- `deploy/AGENT_DEPLOYMENT.md` - automation-oriented deployment runbook.
- `deployment-manifest.json` - machine-readable deployment metadata.

## Fast Path

```bash
sha256sum -c ecs-homepage-{{VERSION}}-linux-web.zip.sha256
unzip ecs-homepage-{{VERSION}}-linux-web.zip
cd ecs-homepage-{{VERSION}}-linux-web
sudo bash deploy/linux/deploy.sh
```

For a real domain:

```bash
sudo ECS_HOMEPAGE_SERVER_NAME=example.com bash deploy/linux/deploy.sh
```

## Expected Checks

```bash
curl -fsSI http://127.0.0.1/
curl -fsSI http://127.0.0.1/home/
curl -fsSI http://127.0.0.1/downloads/{{GUI_INSTALLER_NAME}}
curl -fsS http://127.0.0.1/healthz
curl -fsS http://127.0.0.1/version.json
```

Read `deploy/AGENT_DEPLOYMENT.md` before making non-default choices such as a
custom install root, custom Nginx config path, or containerized deployment.
'@
    $readme = $readme.Replace("{{VERSION}}", $Version)
    $readme = $readme.Replace("{{GUI_INSTALLER_NAME}}", $guiInstallerName)
    [System.IO.File]::WriteAllText(
        (Join-Path $packageRoot "README.md"),
        $readme + [Environment]::NewLine,
        [System.Text.UTF8Encoding]::new($false)
    )

    New-LinuxFriendlyZip -SourceDirectory $packageRoot -DestinationZip $zipPath -EntryRootName $packageName
    $hash = Get-FileHash -LiteralPath $zipPath -Algorithm SHA256
    $hashLine = "$($hash.Hash.ToLowerInvariant())  $(Split-Path $zipPath -Leaf)"
    [System.IO.File]::WriteAllText($hashPath, $hashLine + [Environment]::NewLine, [System.Text.UTF8Encoding]::new($false))

    Remove-Item -LiteralPath $stagingRoot -Recurse -Force

    Write-Host "Linux web package: $zipPath"
    Write-Host "SHA256: $hashPath"
}
finally {
    Pop-Location
}
