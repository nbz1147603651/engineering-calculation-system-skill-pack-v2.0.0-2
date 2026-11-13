<#
.SYNOPSIS
Install, inspect, or remove this bundle in an installed DeepSeek Harness client.

.DESCRIPTION
The installed Windows client keeps its program files in
`%LOCALAPPDATA%\DSH Custom Client\app` and its Harness home (sessions,
credentials, settings, and plugin profiles) in
`%LOCALAPPDATA%\DSH Custom Client\data`. This script drives the client's own
`dsh.exe`, which forwards `plugin` invocations to pnpm inside the profile
directory and then reconciles `dsh.profile.bundles` against what is installed,
so the bundle becomes a profile layer in the same step.

Both directories are configurable for a client installed elsewhere or for a
source checkout run (`-DataRoot <checkout home>`), and `-Profile` selects the
profile that receives the bundle.

.PARAMETER Install
Add the bundle to the profile (default action).

.PARAMETER Inspect
Print the profile's installed plugins and the composed configuration rows that
mention this bundle, without changing anything.

.PARAMETER Remove
Uninstall the bundle from the profile.

.PARAMETER ClientRoot
Client program directory holding `bin\dsh.exe`.

.PARAMETER DataRoot
Client data directory used as `DSH_HOME`.

.PARAMETER Profile
Profile that receives the bundle. In-box clients use `web`.

.PARAMETER Spec
Dependency spec used by `-Install`. Defaults to `file:<this package>`.

.PARAMETER DryRun
Print the command that would run instead of running it.

.EXAMPLE
powershell -File scripts\install-into-local-client.ps1

.EXAMPLE
powershell -File scripts\install-into-local-client.ps1 -Inspect

.EXAMPLE
powershell -File scripts\install-into-local-client.ps1 -Remove
#>

[CmdletBinding(DefaultParameterSetName = 'Install')]
param(
  [Parameter(ParameterSetName = 'Install')][switch]$Install,
  [Parameter(ParameterSetName = 'Inspect')][switch]$Inspect,
  [Parameter(ParameterSetName = 'Remove')][switch]$Remove,
  [string]$ClientRoot = (Join-Path $env:LOCALAPPDATA 'DSH Custom Client\app'),
  [string]$DataRoot = (Join-Path $env:LOCALAPPDATA 'DSH Custom Client\data'),
  [string]$Profile = 'web',
  [string]$Spec,
  [switch]$DryRun
)

$ErrorActionPreference = 'Stop'

$bundleName = '@engineering-calculation-system/dsh-plugin'
$bundleRowId = 'engineering-calculation-system'
$packageRoot = Split-Path -Parent $PSScriptRoot
$profileDir = Join-Path $DataRoot (Join-Path 'profiles' $Profile)

function Get-ClientLauncher {
  $dshExe = Join-Path $ClientRoot 'bin\dsh.exe'
  $dshEntry = Join-Path $ClientRoot 'runtime\node_modules\@deepseek-ai\dsh\lib\bin.js'
  if (-not (Test-Path -LiteralPath $dshExe)) {
    throw "client launcher not found: $dshExe (pass -ClientRoot pointing at the installed app directory)"
  }
  if (-not (Test-Path -LiteralPath $dshEntry)) {
    throw "client runtime entry not found: $dshEntry"
  }
  if (-not (Test-Path -LiteralPath $DataRoot)) {
    throw "client data directory not found: $DataRoot (pass -DataRoot pointing at the installed data directory)"
  }
  return @{ DshExe = $dshExe; DshEntry = $dshEntry }
}

function Invoke-ClientPluginCommand {
  param(
    [Parameter(Mandatory)][hashtable]$Launcher,
    [Parameter(Mandatory)][string[]]$Arguments
  )

  $display = "DSH_HOME=$DataRoot `"$($Launcher.DshExe)`" `"$($Launcher.DshEntry)`" plugin --profile $Profile $($Arguments -join ' ')"
  Write-Host $display
  if ($DryRun) { return }

  $previousHome = $env:DSH_HOME
  $env:DSH_HOME = $DataRoot
  try {
    & $Launcher.DshExe $Launcher.DshEntry plugin --profile $Profile @Arguments
    if ($LASTEXITCODE -ne 0) {
      throw "dsh plugin exited with code $LASTEXITCODE"
    }
  } finally {
    $env:DSH_HOME = $previousHome
  }
}

function Read-ProfileManifest {
  $manifestPath = Join-Path $profileDir 'package.json'
  if (-not (Test-Path -LiteralPath $manifestPath)) { return $null }
  return Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
}

function Get-ComposedRowIds {
  param([Parameter(Mandatory)][hashtable]$Launcher)

  $previousHome = $env:DSH_HOME
  $env:DSH_HOME = $DataRoot
  try {
    $composed = & $Launcher.DshExe $Launcher.DshEntry '--profile' $Profile '--dump-config' 2>&1
  } finally {
    $env:DSH_HOME = $previousHome
  }
  return @($composed | Where-Object { $_ -match "^# == $([regex]::Escape($bundleName))\b" -or $_ -match "^\s*- id: $bundleRowId\s*$" })
}

function Show-InstallationState {
  param([Parameter(Mandatory)][hashtable]$Launcher)

  $manifest = Read-ProfileManifest
  $dependency = $null
  $isBundleLayer = $false
  if ($null -ne $manifest) {
    $dependency = $manifest.dependencies.PSObject.Properties[$bundleName].Value
    $bundles = @($manifest.dsh.profile.bundles)
    $isBundleLayer = $bundles -contains $bundleName
  }

  Write-Host ''
  Write-Host "profile:      $profileDir"
  Write-Host "dependency:   $(if ($null -eq $dependency) { '<absent>' } else { $dependency })"
  Write-Host "bundle layer: $isBundleLayer"
  Write-Host "composed rows mentioning ${bundleRowId}:"
  $rows = Get-ComposedRowIds -Launcher $Launcher
  if ($rows.Count -eq 0) { Write-Host '  <none>' } else { $rows | ForEach-Object { Write-Host "  $_" } }
}

$launcher = Get-ClientLauncher

if ($Inspect) {
  Invoke-ClientPluginCommand -Launcher $launcher -Arguments @('list')
  Show-InstallationState -Launcher $launcher
  return
}

if ($Remove) {
  Invoke-ClientPluginCommand -Launcher $launcher -Arguments @('remove', $bundleName)
  Show-InstallationState -Launcher $launcher
  Write-Host ''
  Write-Host 'Restart the client to drop the bundle from a running session.'
  return
}

if (-not $Spec) {
  $Spec = 'file:' + ($packageRoot -replace '\\', '/')
}
Invoke-ClientPluginCommand -Launcher $launcher -Arguments @('add', $Spec)
Show-InstallationState -Launcher $launcher
Write-Host ''
Write-Host "The installed profile references the package as a dependency; 'file:' snapshots the"
Write-Host 'package at add time, so re-run this script after editing lib/ or skills/.'
Write-Host 'Restart the client, then load the skill from the skill catalog or the skill tool.'
