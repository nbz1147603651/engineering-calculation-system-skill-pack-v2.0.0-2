#!/usr/bin/env node
import { existsSync, readdirSync, readFileSync, statSync } from "node:fs";
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const pluginRoot = path.resolve(scriptDir, "..");
const workspaceRoot = path.resolve(pluginRoot, "..");
const targetSchemaVersion = "2.4.0";

const requiredSkillPaths = [
  "SKILL.md",
  "skills/00-engineering-calculation-router.skill.md",
  "shared/multi-agent-orchestration.md",
  "templates/orchestration/parallel_work_plan.yaml",
  "templates/orchestration/agent_result_packet.yaml",
  "templates/orchestration/merge_review.md",
  "schemas/artifact_contracts.json",
  "scripts/validate_artifacts.py",
];

const legacyTemplatePaths = [
  ".opencode/agents/engineering-calc-architect.md",
  ".opencode/agents/engineering-calc-builder.md",
];

function usage() {
  return `
Usage:
  node scripts/install-project.mjs [--target <project-root>] [--skill-root <skill-root>] [--force]

Examples:
  node scripts/install-project.mjs --target .. --force
  node scripts/install-project.mjs --target .. --skill-root ../engineering-calculation-system-skill-pack-v2.x.x/core/engineering-calculation-system --force
`.trim();
}

function parseArgs(argv) {
  const args = {
    target: process.cwd(),
    skillRoot: undefined,
    force: false,
  };

  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === "--help" || arg === "-h") {
      console.log(usage());
      process.exit(0);
    }
    if (arg === "--force") {
      args.force = true;
      continue;
    }
    if (arg === "--target") {
      args.target = argv[++index];
      continue;
    }
    if (arg === "--skill-root") {
      args.skillRoot = argv[++index];
      continue;
    }
    throw new Error(`Unknown argument: ${arg}\n${usage()}`);
  }

  return {
    target: path.resolve(args.target),
    skillRoot: args.skillRoot ? path.resolve(args.skillRoot) : undefined,
    force: args.force,
  };
}

function toPosix(value) {
  return value.split(path.sep).join("/");
}

function ensureRelativeImport(value) {
  const normalized = toPosix(value);
  if (normalized.startsWith(".")) return normalized;
  return `./${normalized}`;
}

function inspectSkillRoot(root) {
  return requiredSkillPaths.filter((relPath) => !existsSync(path.join(root, relPath)));
}

function schemaVersion(root) {
  const schemaPath = path.join(root, "schemas", "artifact_contracts.json");
  if (!existsSync(schemaPath)) return undefined;
  try {
    const parsed = JSON.parse(readFileSync(schemaPath, "utf8"));
    return typeof parsed.version === "string" ? parsed.version : undefined;
  } catch {
    return undefined;
  }
}

function isDirectory(candidate) {
  try {
    return statSync(candidate).isDirectory();
  } catch {
    return false;
  }
}

function skillPackCandidates(base) {
  if (!isDirectory(base)) return [];
  const candidates = [
    path.resolve(base, "engineering-calculation-system"),
    path.resolve(base, "core", "engineering-calculation-system"),
  ];

  try {
    for (const entry of readdirSync(base, { withFileTypes: true })) {
      if (!entry.isDirectory() || !entry.name.startsWith("engineering-calculation-system-skill-pack-")) {
        continue;
      }
      candidates.push(path.resolve(base, entry.name, "core", "engineering-calculation-system"));
    }
  } catch {
    // Ignore unreadable directories and continue with explicit candidates.
  }

  return candidates;
}

function defaultSkillRoot() {
  const candidates = [
    ...skillPackCandidates(workspaceRoot),
    ...skillPackCandidates(pluginRoot),
    ...skillPackCandidates(path.dirname(workspaceRoot)),
  ];

  const seen = new Set();
  const unique = candidates.filter((candidate) => {
    const key = path.normalize(candidate).toLowerCase();
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });

  const exact = unique.find(
    (candidate) => inspectSkillRoot(candidate).length === 0 && schemaVersion(candidate) === targetSchemaVersion,
  );
  if (exact) return exact;

  return unique.find((candidate) => inspectSkillRoot(candidate).length === 0);
}

async function walkFiles(root) {
  const entries = await fs.readdir(root, { withFileTypes: true });
  const files = [];
  for (const entry of entries) {
    const fullPath = path.join(root, entry.name);
    if (entry.isDirectory()) {
      files.push(...(await walkFiles(fullPath)));
    } else if (entry.isFile()) {
      files.push(fullPath);
    }
  }
  return files;
}

async function writeFileOnce(filePath, content, force) {
  if (existsSync(filePath) && !force) {
    throw new Error(`Refusing to overwrite existing file without --force: ${filePath}`);
  }
  await fs.mkdir(path.dirname(filePath), { recursive: true });
  await fs.writeFile(filePath, content, "utf8");
}

async function copyTemplates({ target, skillRoot, force }) {
  const templateRoot = path.join(pluginRoot, "templates");
  const files = await walkFiles(templateRoot);

  const skillWrapperDir = path.join(target, ".opencode", "skills", "engineering-calc-system");
  const commandDir = path.join(target, ".opencode", "commands");
  const skillRootRelative = toPosix(path.relative(skillWrapperDir, skillRoot)) || ".";
  const skillRootRelativeFromCommand = toPosix(path.relative(commandDir, skillRoot)) || ".";

  for (const source of files) {
    const relPath = path.relative(templateRoot, source);
    const destination = path.join(target, relPath);
    const raw = await fs.readFile(source, "utf8");
    const rendered = raw
      .replaceAll("{{SKILL_ROOT_RELATIVE}}", skillRootRelative)
      .replaceAll("{{SKILL_ROOT_RELATIVE_FROM_COMMAND}}", skillRootRelativeFromCommand);

    await writeFileOnce(destination, rendered, force);
  }
}

async function writePluginShim({ target, force }) {
  const pluginDir = path.join(target, ".opencode", "plugins");
  const pluginShimPath = path.join(pluginDir, "engineering-calc-system.ts");
  const sourceEntry = path.join(pluginRoot, "src", "index.ts");
  const importPath = ensureRelativeImport(path.relative(pluginDir, sourceEntry));
  const content = [
    `export { EngineeringCalculationSystemPlugin, EngineeringCalculationSystemPlugin as default } from "${importPath}";`,
    "",
  ].join("\n");

  await writeFileOnce(pluginShimPath, content, force);
}

async function mergeOpenCodePackage({ target }) {
  const packagePath = path.join(target, ".opencode", "package.json");
  let packageJson = {};

  if (existsSync(packagePath)) {
    packageJson = JSON.parse(await fs.readFile(packagePath, "utf8"));
  }

  packageJson.dependencies = {
    ...(packageJson.dependencies ?? {}),
    "@opencode-ai/plugin": "^1.17.7",
  };

  await fs.mkdir(path.dirname(packagePath), { recursive: true });
  await fs.writeFile(packagePath, `${JSON.stringify(packageJson, null, 2)}\n`, "utf8");
}

async function removeLegacyTemplates({ target, force }) {
  if (!force) return;
  for (const relPath of legacyTemplatePaths) {
    const fullPath = path.join(target, relPath);
    if (existsSync(fullPath)) {
      await fs.rm(fullPath, { force: true });
    }
  }
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const skillRoot = args.skillRoot ?? defaultSkillRoot();

  if (!skillRoot) {
    throw new Error("Could not infer the skill root. Pass --skill-root explicitly.");
  }

  const missing = inspectSkillRoot(skillRoot);
  if (missing.length > 0) {
    throw new Error(`Skill root is incomplete: ${skillRoot}\nMissing:\n- ${missing.join("\n- ")}`);
  }
  const version = schemaVersion(skillRoot);
  if (version !== targetSchemaVersion) {
    throw new Error(
      `Skill root schema version must be ${targetSchemaVersion}, got ${version ?? "unknown"}: ${skillRoot}`,
    );
  }

  await removeLegacyTemplates({ target: args.target, force: args.force });
  await copyTemplates({ target: args.target, skillRoot, force: args.force });
  await writePluginShim({ target: args.target, force: args.force });
  await mergeOpenCodePackage({ target: args.target });

  console.log("OpenCode Engineering Calculation System plugin files installed.");
  console.log(`Target: ${args.target}`);
  console.log(`Skill root: ${skillRoot}`);
  console.log(`Skill schema: ${version}`);
  console.log("Run OpenCode from the target project root so it can discover .opencode/.");
}

main().catch((error) => {
  console.error(error.message);
  process.exit(1);
});
