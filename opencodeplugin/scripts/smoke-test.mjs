#!/usr/bin/env node
import { existsSync, readdirSync, readFileSync, statSync } from "node:fs";
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const pluginRoot = path.resolve(scriptDir, "..");
const workspaceRoot = path.resolve(pluginRoot, "..");
const pluginPackageJson = JSON.parse(readFileSync(path.join(pluginRoot, "package.json"), "utf8"));
const targetSchemaVersion = pluginPackageJson.skillPack?.schemaVersion;
if (typeof targetSchemaVersion !== "string" || targetSchemaVersion.length === 0) {
  throw new Error("Plugin package is missing skillPack.schemaVersion");
}

const requiredFiles = [
  "package.json",
  "tsconfig.json",
  "assets/engineering-calc-system.schema.json",
  "src/index.ts",
  "src/plugin/create-plugin-module.ts",
  "src/create-tools.ts",
  "src/create-hooks.ts",
  "src/config/loader.ts",
  "src/doctor/runner.ts",
  "src/installer/asset-manager.ts",
  "src/cli/index.ts",
  "src/paths.ts",
  "templates/.opencode/AGENTS.md",
  "templates/.opencode/skills/engineering-calc-system/SKILL.md",
  "templates/.opencode/commands/engineering-calc-start.md",
  "templates/.opencode/commands/engineering-calc-status.md",
  "templates/.opencode/commands/engineering-calc-config.md",
  "templates/.opencode/commands/engineering-calc-validate.md",
  "templates/.opencode/commands/engineering-calc-doctor.md",
  "templates/.opencode/commands/engineering-calc-orchestrate.md",
  "templates/.opencode/commands/engineering-calc-worker-packet.md",
  "templates/.opencode/commands/engineering-calc-merge-review.md",
  "templates/.opencode/commands/engineering-calc-handoff.md",
  "templates/.opencode/commands/engineering-calc-release.md",
  "templates/.opencode/agents/engineering-calc-supervisor.md",
  "templates/.opencode/agents/engineering-calc-reference-acquirer.md",
  "templates/.opencode/agents/engineering-calc-source-intake.md",
  "templates/.opencode/agents/engineering-calc-logic-extractor.md",
  "templates/.opencode/agents/engineering-calc-module-worker.md",
  "templates/.opencode/agents/engineering-calc-interface-worker.md",
  "templates/.opencode/agents/engineering-calc-verification-worker.md",
  "scripts/install-project.mjs",
  "docs/optimization-assessment.md",
];

const requiredSkillFiles = [
  "SKILL.md",
  "skills/00-engineering-calculation-router.skill.md",
  "shared/lifecycle.md",
  "shared/quality-gates.md",
  "shared/delivery-contract.md",
  "shared/lifecycle-matrix.md",
  "shared/multi-agent-orchestration.md",
  "templates/orchestration/parallel_work_plan.yaml",
  "templates/orchestration/agent_result_packet.yaml",
  "templates/orchestration/merge_review.md",
  "schemas/artifact_contracts.json",
  "scripts/validate_artifacts.py",
];

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function isDirectory(candidate) {
  try {
    return statSync(candidate).isDirectory();
  } catch {
    return false;
  }
}

function candidateSkillRoots(base) {
  if (!isDirectory(base)) return [];
  const candidates = [
    path.join(base, "engineering-calculation-system"),
    path.join(base, "engineering-calculation-system", "core", "engineering-calculation-system"),
    path.join(base, "core", "engineering-calculation-system"),
  ];
  for (const entry of readdirSync(base, { withFileTypes: true })) {
    const isCanonicalPackage = entry.name === "engineering-calculation-system";
    const isVersionedSkillPack = entry.name.startsWith("engineering-calculation-system-skill-pack-");
    if (entry.isDirectory() && (isCanonicalPackage || isVersionedSkillPack)) {
      candidates.push(path.join(base, entry.name, "core", "engineering-calculation-system"));
    }
  }
  return candidates;
}

function schemaVersion(root) {
  const schemaPath = path.join(root, "schemas", "artifact_contracts.json");
  if (!existsSync(schemaPath)) return undefined;
  const parsed = JSON.parse(readFileSync(schemaPath, "utf8"));
  return parsed.version;
}

function findSkillRoot() {
  const candidates = [
    ...candidateSkillRoots(workspaceRoot),
    ...candidateSkillRoots(pluginRoot),
    ...candidateSkillRoots(path.dirname(workspaceRoot)),
  ];
  return candidates.find(
    (candidate) =>
      requiredSkillFiles.every((relPath) => existsSync(path.join(candidate, relPath))) &&
      schemaVersion(candidate) === targetSchemaVersion,
  );
}

async function main() {
  for (const relPath of requiredFiles) {
    assert(existsSync(path.join(pluginRoot, relPath)), `Missing plugin file: ${relPath}`);
  }
  assert(!existsSync(path.join(pluginRoot, "templates/.opencode/agents/engineering-calc-architect.md")), "Legacy architect agent template is still present");
  assert(!existsSync(path.join(pluginRoot, "templates/.opencode/agents/engineering-calc-builder.md")), "Legacy builder agent template is still present");

  const packageJson = pluginPackageJson;
  assert(packageJson.version === "0.3.0", "Plugin package version should be 0.3.0");
  assert(packageJson.skillPack?.schemaVersion === targetSchemaVersion, `Plugin package should declare skill pack schema ${targetSchemaVersion}`);
  assert(packageJson.bin?.["engineering-calc-opencode"], "Missing CLI bin");
  assert(packageJson.dependencies?.zod, "Missing zod dependency");
  assert(packageJson.dependencies?.["jsonc-parser"], "Missing jsonc-parser dependency");
  assert(packageJson.dependencies?.commander, "Missing commander dependency");
  assert(packageJson.dependencies?.["@opencode-ai/plugin"], "Missing @opencode-ai/plugin dependency");
  assert(packageJson.scripts?.build, "Missing build script");

  const skillTemplate = await fs.readFile(
    path.join(pluginRoot, "templates/.opencode/skills/engineering-calc-system/SKILL.md"),
    "utf8",
  );
  assert(skillTemplate.startsWith("---\nname: engineering-calc-system"), "Skill template frontmatter is invalid");
  assert(skillTemplate.includes("{{SKILL_ROOT_RELATIVE}}/SKILL.md"), "Skill template placeholder is missing");
  assert(skillTemplate.includes("multi-agent-orchestration.md"), "Skill template missing orchestration contract");
  assert(skillTemplate.includes("templates/orchestration/"), "Skill template missing orchestration templates");
  assert(skillTemplate.includes("strict JSON object arguments"), "Skill template missing strict JSON tool-call guidance");

  const commandDir = path.join(pluginRoot, "templates/.opencode/commands");
  const commandTemplates = await Promise.all(
    readdirSync(commandDir)
      .filter((entry) => entry.endsWith(".md"))
      .map(async (entry) => [entry, await fs.readFile(path.join(commandDir, entry), "utf8")]),
  );
  const shorthandPattern = /\b(?:phase|artifact|parallel|full|mode|validate|profile)=/;
  const shorthandMatch = commandTemplates.find(([, text]) => shorthandPattern.test(text));
  assert(!shorthandMatch, `Command template uses non-JSON tool argument shorthand: ${shorthandMatch?.[0]}`);
  assert(
    commandTemplates.some(([, text]) => text.includes("strict JSON object arguments")),
    "Command templates should include strict JSON tool-call guidance",
  );

  const indexSource = await fs.readFile(path.join(pluginRoot, "src/index.ts"), "utf8");
  assert(indexSource.includes("createPluginModule"), "Index should export the plugin module factory");
  const toolSource = await fs.readFile(path.join(pluginRoot, "src/create-tools.ts"), "utf8");
  assert(toolSource.includes("engineering_calc_route"), "Route tool is missing");
  assert(toolSource.includes("engineering_calc_doctor"), "Doctor tool is missing");
  assert(toolSource.includes("engineering_calc_orchestration"), "Orchestration tool is missing");
  assert(toolSource.includes("engineering_calc_status"), "Status tool is missing");
  assert(toolSource.includes("engineering_calc_config_example"), "Config example tool is missing");
  assert(toolSource.includes("STRICT_JSON_ARGUMENTS_NOTE"), "Tool descriptions should include strict JSON compatibility notes");
  assert(toolSource.includes("key=value"), "Tool descriptions should warn against key=value shorthand");

  const domainSource = await fs.readFile(path.join(pluginRoot, "src/domain.ts"), "utf8");
  assert(domainSource.includes("\"orchestration\""), "Orchestration phase is missing");
  assert(domainSource.includes("parallel_work_plan"), "Parallel work plan artifact is missing");
  assert(domainSource.includes("agent_result_packet"), "Agent result packet artifact is missing");
  assert(domainSource.includes("merge_review"), "Merge review artifact is missing");

  const skillRoot = findSkillRoot();
  assert(skillRoot, `Could not find a ${targetSchemaVersion} skill root`);
  for (const relPath of requiredSkillFiles) {
    assert(existsSync(path.join(skillRoot, relPath)), `Missing source skill file: ${relPath}`);
  }
  assert(schemaVersion(skillRoot) === targetSchemaVersion, `Source skill schema is not ${targetSchemaVersion}`);

  console.log("Smoke test passed.");
}

main().catch((error) => {
  console.error(error.message);
  process.exit(1);
});
