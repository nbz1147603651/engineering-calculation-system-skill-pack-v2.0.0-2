# Install the bundle into a local DeepSeek Harness client

The bundle becomes a profile layer of the target Harness home. Nothing in the
client program directory changes, and uninstalling removes the layer again.

## Where the client keeps its state

An installed Windows client splits its files in two:

| Directory | Contents |
|---|---|
| `%LOCALAPPDATA%\DSH Custom Client\app` | `bin\dsh.exe`, the bundled Node runtime, the desktop host, and the profile manager scripts |
| `%LOCALAPPDATA%\DSH Custom Client\data` | the Harness home: sessions, credentials, settings, and `profiles\` |

The home is the `DSH_HOME` the client boots with, and the profile that renders
the client UI is `<data>\profiles\web`. Its `package.json` holds both halves of
an installed plugin: a dependency entry and a matching entry in
`dsh.profile.bundles`.

## Install

Preferred: run the packaged script, which resolves both directories, sets
`DSH_HOME` for the child process, and reports the resulting state.

```powershell
powershell -File scripts\install-into-local-client.ps1
```

The equivalent by hand, from any directory:

```powershell
$clientApp = "$env:LOCALAPPDATA\DSH Custom Client\app"
$clientData = "$env:LOCALAPPDATA\DSH Custom Client\data"
$env:DSH_HOME = $clientData
& "$clientApp\bin\dsh.exe" `
  "$clientApp\runtime\node_modules\@deepseek-ai\dsh\lib\bin.js" `
  plugin --profile web add "<this package directory>"
```

The client ships its own Node runtime and `dsh` launcher, but `dsh plugin` is a
pnpm forwarder: it spawns `pnpm` from `PATH` in the profile directory and then
reconciles `dsh.profile.bundles` against what is installed, which is why one
command both installs the dependency and activates the layer. A machine without
pnpm on `PATH` fails this step with `pnpm not found on PATH — install pnpm to
manage profile plugins` and exit code 127, and the profile is left unchanged.

Re-running the install takes a fresh snapshot of the package directory, so it is
also how a later edit to `lib/` or `skills/` reaches the profile.

The client also ships `Manage Web Plugins.cmd` next to `bin\dsh.exe`, which runs
the same invocation with `--profile web` and accepts raw pnpm arguments.

## Verify

```powershell
powershell -File scripts\install-into-local-client.ps1 -Inspect
```

The inspection prints the profile path, the dependency spec, whether the bundle
is an active layer, and the composed configuration rows that mention it. Three
independent signals confirm a healthy installation:

1. `dsh plugin --profile web list` reports `@engineering-calculation-system/dsh-plugin`.
2. `dsh --profile web --dump-config` ends with the bundle's layer and row:

   ```yaml
   # == @engineering-calculation-system/dsh-plugin
   - id: engineering-calculation-system
     name: '@engineering-calculation-system/dsh-plugin'
   ```

3. Inside the client, the skill catalog and the skill tool list
   `engineering-calculation-system`. Loading it returns the pack body and a
   resource base of
   `<installed package>\skills\engineering-calculation-system`, which is the
   directory every relative path in the pack resolves against.

The `skill` registry lives in the host plane and merges deployment-level
providers into every agent preset's catalog, so the bundle needs no preset
changes: the `web` profile disables the host `skill-filesystem` and `tool-skill`
rows because each preset owns its own local discovery and loader, while a
provider registered by this outside bundle still reaches every session.

The client composes the profile at boot. Restart it after installing, removing,
or updating the bundle.

## Refresh after editing the package

`file:` installs snapshot the package directory, so later edits to `lib/` or
`skills/` do not reach the profile by themselves. Re-run the install command to
take a fresh snapshot. To iterate against the working tree instead, install the
same directory with a `link:` spec; the client then reads the package in place
and a restart is enough.

## Uninstall

```powershell
powershell -File scripts\install-into-local-client.ps1 -Remove
```

The script removes the dependency and reports the profile state; the layer list
drops the bundle in the same step. Restart the client afterwards.

## Source checkouts

A `pnpm dsh --profile web` run from a checkout uses `~/.dsh` unless `DSH_HOME`
says otherwise, and that home has its own `profiles\web`. Point the script at it
to install into the source-run terminal or browser client as well:

```powershell
powershell -File scripts\install-into-local-client.ps1 -DataRoot "$env:USERPROFILE\.dsh"
```

Both homes are independent; installing into one leaves the other unchanged.
