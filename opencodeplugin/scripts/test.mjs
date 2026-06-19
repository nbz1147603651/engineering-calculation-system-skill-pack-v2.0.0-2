#!/usr/bin/env node
import assert from "node:assert/strict";
import fs from "node:fs/promises";
import { existsSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
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

const workspaceRoot = path.resolve(root, "..");
const skillRoot = path.join(
  workspaceRoot,
  "engineering-calculation-system",
  "core",
  "engineering-calculation-system",
);

assert(existsSync(skillRoot), "Expected local v2.4.0 skill root");

{
  const project = await fs.mkdtemp(path.join(os.tmpdir(), "ecs-config-test-"));
  await fs.mkdir(path.join(project, ".opencode"), { recursive: true });
  await fs.writeFile(
    path.join(project, ".opencode", "engineering-calc-system.jsonc"),
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
  assert.equal(resolved.schemaVersion, "2.4.0");
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
  assert(minimalConfigExample().includes("strictGateMode"));
  assert(fullConfigExample().includes("mcpPresets"));
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

console.log("Unit tests passed.");
