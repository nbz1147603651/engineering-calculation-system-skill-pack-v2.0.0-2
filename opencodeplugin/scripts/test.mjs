#!/usr/bin/env node
import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import fs from "node:fs/promises";
import { existsSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const cliPath = path.join(root, "dist", "cli", "index.js");
const {
  loadConfig,
  minimalConfigExample,
  fullConfigExample,
} = await import("../dist/config/loader.js");
const { resolveSkillRoot } = await import("../dist/paths.js");
const { runDoctor } = await import("../dist/doctor/runner.js");
const {
  installAssets,
  inspectAssets,
  uninstallAssets,
  MANAGED_MARKER,
} = await import("../dist/installer/asset-manager.js");
const { DEFAULT_CONFIG } = await import("../dist/config/schema.js");
const { renderOrchestrationDraft } = await import("../dist/domain.js");
const { loadGateState, evaluateEdit, extractFilePath, extractContent } = await import("../dist/gates.js");
const { createHooks } = await import("../dist/create-hooks.js");
const { emptyManifest, writeManifest } = await import("../dist/manifest.js");
const { PROFILE_NAMES, parseOpenCodeProfile } = await import("../dist/profiles.js");
const { MCP_CATALOG, buildMcpConfig, mcpForProfile, parseMcpMode } = await import("../dist/mcp-presets.js");
const fsPromises = await import("node:fs/promises");

function runCli(args, options = {}) {
  return spawnSync(process.execPath, [cliPath, ...args], {
    cwd: root,
    encoding: "utf8",
    ...options,
  });
}

function parseConfigFromCliOutput(stdout) {
  const start = stdout.indexOf("{");
  const end = stdout.lastIndexOf("}");
  assert(start >= 0 && end > start, `Expected JSON object in CLI output:\n${stdout}`);
  return JSON.parse(stdout.slice(start, end + 1));
}

const workspaceRoot = path.resolve(root, "..");
const packageJson = JSON.parse(await fs.readFile(path.join(root, "package.json"), "utf8"));
const targetSchemaVersion = packageJson.skillPack?.schemaVersion;
assert.equal(typeof targetSchemaVersion, "string", "Expected package skillPack.schemaVersion");
const skillRoot = path.join(
  workspaceRoot,
  "engineering-calculation-system",
  "core",
  "engineering-calculation-system",
);

assert(existsSync(skillRoot), `Expected local v${targetSchemaVersion} skill root`);

{
  const project = await fs.mkdtemp(path.join(os.tmpdir(), "ecs-config-test-"));
  await fs.mkdir(path.join(project, ".opencode"), { recursive: true });
  await fs.writeFile(
    path.join(project, ".opencode", "engineering-calc-system.json"),
    `{
      "strictGateMode": false,
      "mcpPresets": { "enabled": true, "allowed": ["unsafe-project-value"] }
    }`,
    "utf8",
  );
  const loaded = loadConfig(project);
  assert.equal(loaded.config.strictGateMode, false);
  assert.equal(loaded.config.mcpPresets.enabled, false, "project mcpPresets must be ignored");
  assert(loaded.messages.some((message) => message.includes("user-only")));
  await fs.rm(project, { recursive: true, force: true });
}

{
  const resolved = resolveSkillRoot({ directory: workspaceRoot, worktree: workspaceRoot });
  assert.equal(resolved.schemaVersion, targetSchemaVersion);
  assert.equal(resolved.missingRequiredPaths.length, 0);
}

{
  const draft = renderOrchestrationDraft({
    artifact: "parallel_work_plan",
    phase: "implementation",
    objective: "bounded module",
    ownedPaths: ["src/pkg/libraries/example/"],
  });
  assert(draft.includes("```yaml"));
  assert(draft.includes("owned_paths"));
}

{
  assert(minimalConfigExample().includes("defaultPhase"));
  assert(fullConfigExample().includes("mcpPresets"));
  assert(fullConfigExample().includes('"runtimeHook": false'));
}

// Profile and MCP catalog tests.
{
  assert.deepEqual(PROFILE_NAMES, [
    "conservative",
    "reference-acquisition",
    "implementation",
    "verification",
    "web-complete",
    "release",
  ]);
  assert.deepEqual(Object.keys(MCP_CATALOG).sort(), ["context7", "gh_grep", "playwright", "sentry"].sort());
  assert.deepEqual(mcpForProfile("conservative"), []);
  assert.deepEqual(mcpForProfile("reference-acquisition"), []);
  assert.deepEqual(mcpForProfile("implementation"), ["context7", "gh_grep"]);
  assert.deepEqual(mcpForProfile("verification"), ["playwright"]);
  assert.deepEqual(mcpForProfile("web-complete"), ["context7", "playwright"]);
  assert.deepEqual(mcpForProfile("release"), []);

  const catalog = buildMcpConfig({ profile: "implementation", mode: "catalog" });
  assert(catalog, "catalog mode should emit all MCP entries");
  assert.deepEqual(Object.keys(catalog).sort(), ["context7", "gh_grep", "playwright", "sentry"].sort());
  assert(Object.values(catalog).every((entry) => entry.enabled === false), "catalog MCP entries must be disabled");

  const implementation = buildMcpConfig({ profile: "implementation", mode: "recommended" });
  assert(implementation, "implementation recommended mode should emit MCP entries");
  assert.deepEqual(Object.keys(implementation).sort(), ["context7", "gh_grep"].sort());
  assert(Object.values(implementation).every((entry) => entry.enabled === true), "recommended MCP entries must be enabled");

  const webComplete = buildMcpConfig({ profile: "web-complete", mode: "recommended" });
  assert(webComplete, "web-complete recommended mode should emit MCP entries");
  assert.deepEqual(Object.keys(webComplete).sort(), ["context7", "playwright"].sort());
  assert.equal(buildMcpConfig({ profile: "conservative", mode: "recommended" }), undefined);
  assert.equal(buildMcpConfig({ profile: "release", mode: "recommended" }), undefined);

  for (const profile of PROFILE_NAMES) {
    assert(!mcpForProfile(profile).includes("sentry"), "sentry must never be profile-recommended");
  }
  assert.throws(() => parseOpenCodeProfile("invalid-profile"), /Invalid profile/);
  assert.throws(() => parseMcpMode("invalid-mode"), /Invalid MCP mode/);
}

// CLI profile/MCP scenarios.
{
  const implementation = runCli(["opencode-json", "--profile", "implementation", "--mcp", "recommended"]);
  assert.equal(implementation.status, 0, implementation.stderr);
  const implementationConfig = parseConfigFromCliOutput(implementation.stdout);
  assert.deepEqual(Object.keys(implementationConfig.mcp).sort(), ["context7", "gh_grep"].sort());
  assert.equal(implementationConfig.mcp.context7.enabled, true);
  assert.equal(implementationConfig.mcp.gh_grep.enabled, true);

  const webComplete = runCli(["opencode-json", "--profile", "web-complete", "--mcp", "recommended"]);
  assert.equal(webComplete.status, 0, webComplete.stderr);
  const webCompleteConfig = parseConfigFromCliOutput(webComplete.stdout);
  assert.deepEqual(Object.keys(webCompleteConfig.mcp).sort(), ["context7", "playwright"].sort());

  const catalog = runCli(["opencode-json", "--mcp", "catalog"]);
  assert.equal(catalog.status, 0, catalog.stderr);
  const catalogConfig = parseConfigFromCliOutput(catalog.stdout);
  assert.deepEqual(Object.keys(catalogConfig.mcp).sort(), ["context7", "gh_grep", "playwright", "sentry"].sort());
  assert(Object.values(catalogConfig.mcp).every((entry) => entry.enabled === false), "catalog CLI entries must be disabled");

  const alias = runCli(["opencode-json", "--include-mcp"]);
  assert.equal(alias.status, 0, alias.stderr);
  const aliasConfig = parseConfigFromCliOutput(alias.stdout);
  assert.deepEqual(aliasConfig.mcp, catalogConfig.mcp, "--include-mcp should match --mcp catalog");

  const profiles = runCli(["profiles"]);
  assert.equal(profiles.status, 0, profiles.stderr);
  assert(profiles.stdout.includes("implementation"));
  assert(profiles.stdout.includes("context7, gh_grep"));

  const profilesJson = runCli(["profiles", "--json"]);
  assert.equal(profilesJson.status, 0, profilesJson.stderr);
  const parsedProfiles = JSON.parse(profilesJson.stdout);
  assert(parsedProfiles.profiles.some((profile) => profile.name === "web-complete"));
  assert(parsedProfiles.mcpCatalog.sentry);

  const invalidProfile = runCli(["opencode-json", "--profile", "invalid-profile"]);
  assert.notEqual(invalidProfile.status, 0);
  assert(invalidProfile.stderr.includes("Invalid profile"));

  const invalidMcp = runCli(["opencode-json", "--mcp", "invalid-mode"]);
  assert.notEqual(invalidMcp.status, 0);
  assert(invalidMcp.stderr.includes("Invalid MCP mode"));
}

// opencode.json merge should preserve user-owned MCP values and only add missing entries.
{
  const project = await fs.mkdtemp(path.join(os.tmpdir(), "ecs-opencode-json-test-"));
  await fs.writeFile(
    path.join(project, "opencode.json"),
    JSON.stringify(
      {
        plugin: ["existing-plugin"],
        mcp: {
          context7: {
            type: "remote",
            url: "https://example.test/custom-context7",
            enabled: false,
          },
          custom_docs: {
            type: "remote",
            url: "https://example.test/custom-docs",
            enabled: true,
          },
        },
      },
      null,
      2,
    ),
    "utf8",
  );
  const write = runCli([
    "opencode-json",
    "--target",
    project,
    "--profile",
    "implementation",
    "--mcp",
    "recommended",
    "--write",
  ]);
  assert.equal(write.status, 0, write.stderr);
  const merged = JSON.parse(await fs.readFile(path.join(project, "opencode.json"), "utf8"));
  assert(merged.plugin.includes("existing-plugin"));
  assert(merged.plugin.includes("./.opencode/plugins/engineering-calc-system.ts"));
  assert.equal(merged.mcp.context7.url, "https://example.test/custom-context7");
  assert.equal(merged.mcp.context7.enabled, false);
  assert.equal(merged.mcp.custom_docs.enabled, true);
  assert.equal(merged.mcp.gh_grep.enabled, true);
  assert(!merged.mcp.sentry, "sentry should not be added in recommended implementation mode");
  await fs.rm(project, { recursive: true, force: true });
}

{
  const project = await fs.mkdtemp(path.join(os.tmpdir(), "ecs-install-test-"));
  const commandDir = path.join(project, ".opencode", "commands");
  await fs.mkdir(commandDir, { recursive: true });
  const userCommand = path.join(commandDir, "engineering-calc-start.md");
  await fs.writeFile(userCommand, "user-owned command\n", "utf8");
  const report = await installAssets({
    target: project,
    skillRoot,
    config: DEFAULT_CONFIG,
    force: true,
  });
  assert(report.installed.some((entry) => entry.includes("engineering-calc-system.ts")));
  assert(report.backups.some((entry) => entry.includes("engineering-calc-start.md")));
  const shim = await fs.readFile(path.join(project, ".opencode", "plugins", "engineering-calc-system.ts"), "utf8");
  assert(shim.includes(MANAGED_MARKER));
  const packageText = await fs.readFile(path.join(project, ".opencode", "package.json"), "utf8");
  assert(packageText.includes("@opencode-ai/plugin"));
  assert(packageText.includes("engineeringCalcOpenCodeManaged"));
  const assets = await inspectAssets(project);
  assert.equal(assets.installed, true);
  const uninstall = await uninstallAssets(project);
  assert(uninstall.removed.length > 0);
  assert(!existsSync(path.join(project, ".opencode", "plugins", "engineering-calc-system.ts")));
  assert(!existsSync(path.join(project, ".opencode", "agents", "engineering-calc-supervisor.md")));
  assert(!existsSync(path.join(project, ".opencode", "package.json")));
  await fs.rm(project, { recursive: true, force: true });
}

{
  const project = await fs.mkdtemp(path.join(os.tmpdir(), "ecs-doctor-test-"));
  const doctor = await runDoctor({
    target: project,
    overrides: { skillRoot },
    includeValidation: false,
  });
  assert.equal(doctor.results.some((entry) => entry.name === "schema-version" && entry.status === "pass"), true);
  assert.equal(doctor.results.some((entry) => entry.name === "optional-capabilities"), true);
  await fs.rm(project, { recursive: true, force: true });
}

// Strict JSON config tests.
{
  const project = await fs.mkdtemp(path.join(os.tmpdir(), "ecs-json-config-test-"));
  await fs.mkdir(path.join(project, ".opencode"), { recursive: true });
  await fs.writeFile(
    path.join(project, ".opencode", "engineering-calc-system.json"),
    JSON.stringify({ gates: { enforcement: "warn", runtimeHook: false } }, null, 2),
    "utf8",
  );
  const loaded = loadConfig(project);
  assert.equal(loaded.config.gates.enforcement, "warn");
  assert.equal(loaded.config.gates.runtimeHook, false);
  assert.equal(loaded.messages.length, 0);
  await fs.writeFile(
    path.join(project, ".opencode", "engineering-calc-system.jsonc"),
    "{\n  // comments are intentionally not supported by plugin config\n  \"defaultPhase\": \"router\"\n}",
    "utf8",
  );
  await fs.rm(path.join(project, ".opencode", "engineering-calc-system.json"), { force: true });
  const deprecated = loadConfig(project);
  assert(deprecated.messages.some((message) => message.includes(".jsonc plugin configs are deprecated")));
  assert(deprecated.messages.length >= 2, "JSONC comments should not be parsed by plugin config");
  await fs.rm(project, { recursive: true, force: true });
}

// Gate enforcer tests.
{
  const project = await fs.mkdtemp(path.join(os.tmpdir(), "ecs-gates-test-"));
  const fakeRoot = {
    root: project,
    source: "directory",
    exists: true,
    schemaVersion: "2.4.1",
    missingRequiredPaths: [],
  };
  const baseConfig = JSON.parse(JSON.stringify(DEFAULT_CONFIG));
  baseConfig.gates = { enabled: true, enforcement: "strict", runtimeHook: false, disable: [] };
  const ctx = { target: project, worktree: project, config: baseConfig, rootStatus: fakeRoot };

  // 1. Cross-platform boundary is always blocked.
  const codexViolation = evaluateEdit(ctx, loadGateState(ctx), "plugins/engineering-calculation-system/skills/foo.md", "x");
  assert(codexViolation.some((v) => v.gate === "cross-platform-boundary" && v.severity === "block"), "Codex plugin path must be blocked");

  // 2. Handoff freeze blocks writes to handoff files.
  const handoffDir = path.join(project, "handoff");
  await fsPromises.mkdir(handoffDir, { recursive: true });
  await fsPromises.writeFile(path.join(handoffDir, "coding_go_no_go.md"), "# Go No Go\n\ndecision: go\n", "utf8");
  const stateAfterFreeze = loadGateState(ctx);
  assert.equal(stateAfterFreeze.handoffFrozen, true, "Handoff should be frozen when decision is go");
  const frozenViolation = evaluateEdit(ctx, stateAfterFreeze, "handoff/implementation_handoff.yaml", "x");
  assert(frozenViolation.some((v) => v.gate === "handoff-freeze"), "Frozen handoff must block edits");

  // 3. owned_paths enforcement when active plan is present.
  const planText = [
    "plan_id: PWP-TEST",
    "status: active",
    "tasks:",
    "  - task_id: TASK-1",
    "    owned_paths:",
    "      - src/pkg/libraries/example/",
  ].join("\n");
  await fsPromises.writeFile(path.join(project, "handoff", "active_plan.yaml"), planText, "utf8");
  const stateWithPlan = loadGateState(ctx);
  assert(stateWithPlan.activePlan, "Active plan should be detected");
  const outOfScope = evaluateEdit(ctx, stateWithPlan, "src/pkg/libraries/other/foo.py", "x");
  assert(outOfScope.some((v) => v.gate === "owned-paths"), "Out-of-scope edit must be blocked");
  const inScope = evaluateEdit(ctx, stateWithPlan, "src/pkg/libraries/example/x.py", "x");
  assert(!inScope.some((v) => v.gate === "owned-paths"), "In-scope edit must not be blocked by owned_paths");

  // 4. Formula-in-presentation heuristic.
  const formulaHit = evaluateEdit(ctx, loadGateState(ctx), "webapp/static/js/main.js", "function compute() { return a ** 2 + b * 3.14; }");
  assert(formulaHit.some((v) => v.gate === "formula-in-presentation"), "Formula content in JS must trigger gate");
  const benignUi = evaluateEdit(ctx, loadGateState(ctx), "webapp/templates/index.html", "<h1>Hello</h1>");
  assert(!benignUi.some((v) => v.gate === "formula-in-presentation"), "Benign UI content must not trigger gate");

  // 5. Enforcement mode off disables everything except cross-platform boundary.
  const offConfig = JSON.parse(JSON.stringify(baseConfig));
  offConfig.gates.enforcement = "off";
  const offCtx = { ...ctx, config: offConfig };
  const offState = loadGateState(offCtx);
  assert.equal(offState.mode, "off", "Enforcement should be off");
  const offResult = evaluateEdit(offCtx, offState, "handoff/implementation_handoff.yaml", "x");
  assert(!offResult.some((v) => v.gate === "handoff-freeze"), "Off mode should not produce handoff-freeze violations");

  // 6. extractFilePath / extractContent.
  assert.equal(extractFilePath("edit", { filePath: "a/b", oldString: "x" }), "a/b");
  assert.equal(extractFilePath("write", { path: "a/b" }), "a/b");
  assert.equal(extractContent("edit", { newString: "hello" }), "hello");
  assert.equal(extractContent("write", { content: "hello" }), "hello");

  // 7. Cross-platform boundary must NOT touch the codex plugin when enforcement is off.
  const offBoundary = evaluateEdit(offCtx, offState, "plugins/engineering-calculation-system/skills/foo.md", "x");
  assert(offBoundary.some((v) => v.gate === "cross-platform-boundary"), "Cross-platform boundary must remain blocked even in off mode");

  // 8. Runtime hook is explicitly opt-in.
  const hooksDefault = createHooks({
    config: baseConfig,
    rootStatus: fakeRoot,
    target: project,
    worktree: project,
  });
  assert.equal(hooksDefault["tool.execute.before"], undefined, "Runtime gate hook should be disabled by default");
  const runtimeConfig = JSON.parse(JSON.stringify(baseConfig));
  runtimeConfig.gates.runtimeHook = true;
  const hooksRuntime = createHooks({
    config: runtimeConfig,
    rootStatus: fakeRoot,
    target: project,
    worktree: project,
  });
  assert.equal(typeof hooksRuntime["tool.execute.before"], "function", "Runtime gate hook should be explicit opt-in");

  await fs.rm(project, { recursive: true, force: true });
}

// Installer: manifest, diff, cross-platform guard, uninstall backup.
{
  const { readManifest, diffManifests, computeSha256 } = await import("../dist/manifest.js");

  // Manifest round-trip.
  const project = await fs.mkdtemp(path.join(os.tmpdir(), "ecs-manifest-test-"));
  const m = emptyManifest("0.3.0", "2.4.1");
  m.files[".opencode/AGENTS.md"] = { relPath: ".opencode/AGENTS.md", sha256: computeSha256("hello"), size: 5 };
  await writeManifest(project, m);
  const back = await readManifest(project);
  assert(back, "Manifest should be readable");
  assert.equal(back.pluginVersion, "0.3.0");
  assert.equal(back.files[".opencode/AGENTS.md"].sha256, computeSha256("hello"));

  // Diff: added / modified / removed.
  const next = emptyManifest("0.3.0", "2.4.1");
  next.files[".opencode/AGENTS.md"] = { relPath: ".opencode/AGENTS.md", sha256: computeSha256("changed"), size: 7 };
  next.files[".opencode/new.md"] = { relPath: ".opencode/new.md", sha256: computeSha256("new"), size: 3 };
  const d = diffManifests(m, next);
  assert(d.added.includes(".opencode/new.md"), "new file should be added");
  assert(d.modified.includes(".opencode/AGENTS.md"), "changed file should be modified");
  assert(d.removed.length === 0, "no removed files in this case");
  await fs.rm(project, { recursive: true, force: true });
}

{
  // Cross-platform guard: install must refuse to write into the codex plugin.
  // We simulate by attempting to install into a tmp project, then creating a
  // codex-style subdir and verifying the installer does NOT touch it.
  const project = await fs.mkdtemp(path.join(os.tmpdir(), "ecs-xp-test-"));
  const codexDir = path.join(project, "plugins", "engineering-calculation-system");
  await fsPromises.mkdir(codexDir, { recursive: true });
  await fsPromises.writeFile(path.join(codexDir, "marker.txt"), "codex-owned", "utf8");

  const report = await installAssets({
    target: project,
    skillRoot,
    config: DEFAULT_CONFIG,
    force: true,
  });
  // The install should succeed and the codex marker must remain untouched.
  const marker = await fs.readFile(path.join(codexDir, "marker.txt"), "utf8");
  assert.equal(marker, "codex-owned", "Codex plugin files must not be modified by the opencode installer");
  // And the install report must not include any codex paths.
  const allInstalled = [...report.installed, ...report.modified, ...report.skipped, ...report.removedLegacy];
  for (const relPath of allInstalled) {
    assert(!relPath.startsWith("plugins/engineering-calculation-system"), `Installer must not touch codex paths, got: ${relPath}`);
  }
  await assert.rejects(
    installAssets({
      target: codexDir,
      skillRoot,
      config: DEFAULT_CONFIG,
      force: true,
    }),
    /cross-platform protected target/,
    "Installer must refuse targets inside the Codex plugin",
  );
  await assert.rejects(
    installAssets({
      target: path.join(workspaceRoot, "engineering-calculation-system", "core"),
      skillRoot,
      config: DEFAULT_CONFIG,
      force: true,
    }),
    /cross-platform protected target/,
    "Installer must refuse targets inside the shared core skill pack",
  );
  // Uninstall and verify backup.
  const uninstallReport = await uninstallAssets(project);
  assert(uninstallReport.manifestRemoved, "Manifest should be removed on uninstall");
  assert(uninstallReport.backupDir, "Backup dir should be created on uninstall");
  assert(uninstallReport.removed.length > 0, "Files should be removed on uninstall");
  await fs.rm(project, { recursive: true, force: true });
}

console.log("Unit tests passed.");
