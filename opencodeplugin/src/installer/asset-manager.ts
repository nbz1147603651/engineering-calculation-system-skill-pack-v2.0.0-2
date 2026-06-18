import { existsSync } from "node:fs";
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import type { EngineeringCalcConfig } from "../config/schema.js";
import { resolveSkillRoot, toPosixPath } from "../paths.js";

export const MANAGED_MARKER = "engineering-calc-opencode-managed";
const OPENCODE_PACKAGE_REL_PATH = ".opencode/package.json";
const OPENCODE_PLUGIN_DEPENDENCY = "@opencode-ai/plugin";
const OPENCODE_PACKAGE_MANAGED_KEY = "engineeringCalcOpenCodeManaged";

const moduleFile = fileURLToPath(import.meta.url);
const distDir = path.dirname(moduleFile);
const packageRoot = path.resolve(distDir, "..", "..");
const templateRoot = path.join(packageRoot, "templates");

const legacyAssets = [
  ".opencode/agents/engineering-calc-architect.md",
  ".opencode/agents/engineering-calc-builder.md",
];

export interface InstallOptions {
  target: string;
  skillRoot?: string;
  config: EngineeringCalcConfig;
  force?: boolean;
  dryRun?: boolean;
}

export interface InstallReport {
  target: string;
  skillRoot: string;
  installed: string[];
  skipped: string[];
  backups: string[];
  removedLegacy: string[];
  dryRun: boolean;
}

export interface UninstallReport {
  target: string;
  removed: string[];
  skipped: string[];
}

export interface AssetStatus {
  installed: boolean;
  present: string[];
  missing: string[];
  unmanagedPresent: string[];
}

async function walkFiles(root: string): Promise<string[]> {
  const entries = await fs.readdir(root, { withFileTypes: true });
  const files: string[] = [];
  for (const entry of entries) {
    const fullPath = path.join(root, entry.name);
    if (entry.isDirectory()) files.push(...await walkFiles(fullPath));
    if (entry.isFile()) files.push(fullPath);
  }
  return files;
}

function textMarkerFor(relPath: string): string {
  if (relPath.endsWith(".ts") || relPath.endsWith(".js")) return `// ${MANAGED_MARKER}`;
  if (relPath.endsWith(".json")) return "";
  return `<!-- ${MANAGED_MARKER} -->`;
}

function injectMarker(relPath: string, content: string): string {
  const marker = textMarkerFor(relPath);
  if (!marker || content.includes(MANAGED_MARKER)) return content;
  return `${marker}\n${content}`;
}

function hasManagedMarker(relPath: string, content: string): boolean {
  if (toPosixPath(relPath) !== OPENCODE_PACKAGE_REL_PATH) return content.includes(MANAGED_MARKER);
  try {
    const parsed = JSON.parse(content) as Record<string, unknown>;
    return parsed[OPENCODE_PACKAGE_MANAGED_KEY] === true;
  } catch {
    return false;
  }
}

async function readTextIfExists(filePath: string): Promise<string | null> {
  if (!existsSync(filePath)) return null;
  return await fs.readFile(filePath, "utf8");
}

async function backupExisting(filePath: string): Promise<string> {
  const backupPath = `${filePath}.bak-${new Date().toISOString().replace(/[:.]/g, "-")}`;
  await fs.copyFile(filePath, backupPath);
  return backupPath;
}

function shouldSkipTemplate(relPath: string, config: EngineeringCalcConfig): boolean {
  const slashPath = toPosixPath(relPath);
  if (slashPath.includes("/agents/")) {
    const name = path.basename(slashPath, ".md");
    if (config.agents.disabled.includes(name)) return true;
    if (config.agents.roleOverrides[name]?.disabled) return true;
  }
  if (slashPath.includes("/commands/")) {
    const name = path.basename(slashPath, ".md");
    if (config.commands.disabled.includes(name)) return true;
  }
  return false;
}

function applyRoleOverrides(relPath: string, content: string, config: EngineeringCalcConfig): string {
  if (!toPosixPath(relPath).includes("/agents/")) return content;
  const name = path.basename(relPath, ".md");
  const override = config.agents.roleOverrides[name];
  if (!override) return content;
  let next = content;
  if (override.description) {
    next = next.replace(/^description:.*$/m, `description: ${override.description}`);
  }
  if (override.promptAppend) {
    next = `${next.trimEnd()}\n\n## Project Role Override\n\n${override.promptAppend}\n`;
  }
  return next;
}

function renderTemplate(content: string, replacements: Record<string, string>): string {
  let rendered = content;
  for (const [key, value] of Object.entries(replacements)) {
    rendered = rendered.replaceAll(`{{${key}}}`, value);
  }
  return rendered;
}

async function managedAssetPaths(): Promise<string[]> {
  const files = await walkFiles(templateRoot);
  return files.map((filePath) => toPosixPath(path.relative(templateRoot, filePath)));
}

async function writeManagedFile(args: {
  destination: string;
  relPath: string;
  content: string;
  force?: boolean;
  dryRun?: boolean;
  report: InstallReport;
}): Promise<void> {
  const existing = await readTextIfExists(args.destination);
  if (existing && !existing.includes(MANAGED_MARKER) && !args.force) {
    args.report.skipped.push(toPosixPath(args.relPath));
    return;
  }
  if (existing && !existing.includes(MANAGED_MARKER) && args.force && !args.dryRun) {
    args.report.backups.push(await backupExisting(args.destination));
  }
  args.report.installed.push(toPosixPath(args.relPath));
  if (args.dryRun) return;
  await fs.mkdir(path.dirname(args.destination), { recursive: true });
  await fs.writeFile(args.destination, injectMarker(args.relPath, args.content), "utf8");
}

async function writePluginShim(args: InstallOptions & { skillRoot: string; report: InstallReport }): Promise<void> {
  const pluginDir = path.join(args.target, ".opencode", "plugins");
  const destination = path.join(pluginDir, "engineering-calc-system.ts");
  const distEntry = path.join(packageRoot, "dist", "index.js");
  const srcEntry = path.join(packageRoot, "src", "index.ts");
  const entry = existsSync(distEntry) ? distEntry : srcEntry;
  let importPath = toPosixPath(path.relative(pluginDir, entry));
  if (!importPath.startsWith(".")) importPath = `./${importPath}`;
  const content = [
    `// ${MANAGED_MARKER}`,
    `export { default } from "${importPath}";`,
    "",
  ].join("\n");
  await writeManagedFile({
    destination,
    relPath: ".opencode/plugins/engineering-calc-system.ts",
    content,
    force: args.force,
    dryRun: args.dryRun,
    report: args.report,
  });
}

async function mergeOpenCodePackage(args: InstallOptions & { report: InstallReport }): Promise<void> {
  const relPath = OPENCODE_PACKAGE_REL_PATH;
  const destination = path.join(args.target, relPath);
  let packageJson: Record<string, unknown> = {};
  const existing = await readTextIfExists(destination);
  if (existing) packageJson = JSON.parse(existing);
  packageJson.dependencies = {
    ...((packageJson.dependencies as Record<string, string> | undefined) ?? {}),
    [OPENCODE_PLUGIN_DEPENDENCY]: "^1.17.7",
  };
  packageJson[OPENCODE_PACKAGE_MANAGED_KEY] = true;
  args.report.installed.push(relPath);
  if (args.dryRun) return;
  await fs.mkdir(path.dirname(destination), { recursive: true });
  await fs.writeFile(destination, `${JSON.stringify(packageJson, null, 2)}\n`, "utf8");
}

async function uninstallOpenCodePackage(root: string, report: UninstallReport): Promise<void> {
  const fullPath = path.join(root, OPENCODE_PACKAGE_REL_PATH);
  const content = await readTextIfExists(fullPath);
  if (!content) return;
  if (!hasManagedMarker(OPENCODE_PACKAGE_REL_PATH, content)) {
    report.skipped.push(OPENCODE_PACKAGE_REL_PATH);
    return;
  }

  let packageJson: Record<string, unknown>;
  try {
    packageJson = JSON.parse(content) as Record<string, unknown>;
  } catch {
    report.skipped.push(OPENCODE_PACKAGE_REL_PATH);
    return;
  }

  const dependencies = packageJson.dependencies as Record<string, unknown> | undefined;
  if (dependencies) {
    delete dependencies[OPENCODE_PLUGIN_DEPENDENCY];
    if (Object.keys(dependencies).length === 0) delete packageJson.dependencies;
  }
  delete packageJson[OPENCODE_PACKAGE_MANAGED_KEY];

  if (Object.keys(packageJson).length === 0) {
    await fs.rm(fullPath, { force: true });
  } else {
    await fs.writeFile(fullPath, `${JSON.stringify(packageJson, null, 2)}\n`, "utf8");
  }
  report.removed.push(OPENCODE_PACKAGE_REL_PATH);
}

async function removeLegacyAssets(args: InstallOptions & { report: InstallReport }): Promise<void> {
  if (!args.force) return;
  for (const relPath of legacyAssets) {
    const fullPath = path.join(args.target, relPath);
    if (!existsSync(fullPath)) continue;
    args.report.removedLegacy.push(relPath);
    if (!args.dryRun) await fs.rm(fullPath, { force: true });
  }
}

export async function installAssets(options: InstallOptions): Promise<InstallReport> {
  const target = path.resolve(options.target);
  const resolved = resolveSkillRoot({
    directory: target,
    worktree: target,
    configuredSkillRoot: options.skillRoot ?? options.config.skillRoot,
  });
  if (resolved.missingRequiredPaths.length > 0) {
    throw new Error(`Skill root is incomplete: ${resolved.root}\nMissing:\n- ${resolved.missingRequiredPaths.join("\n- ")}`);
  }

  const report: InstallReport = {
    target,
    skillRoot: resolved.root,
    installed: [],
    skipped: [],
    backups: [],
    removedLegacy: [],
    dryRun: Boolean(options.dryRun),
  };

  await removeLegacyAssets({ ...options, target, report });

  const skillWrapperDir = path.join(target, ".opencode", "skills", "engineering-calc-system");
  const commandDir = path.join(target, ".opencode", "commands");
  const replacements = {
    SKILL_ROOT_RELATIVE: toPosixPath(path.relative(skillWrapperDir, resolved.root)) || ".",
    SKILL_ROOT_RELATIVE_FROM_COMMAND: toPosixPath(path.relative(commandDir, resolved.root)) || ".",
  };

  for (const source of await walkFiles(templateRoot)) {
    const relPath = toPosixPath(path.relative(templateRoot, source));
    if (shouldSkipTemplate(relPath, options.config)) continue;
    const raw = await fs.readFile(source, "utf8");
    const rendered = applyRoleOverrides(relPath, renderTemplate(raw, replacements), options.config);
    await writeManagedFile({
      destination: path.join(target, relPath),
      relPath,
      content: rendered,
      force: options.force,
      dryRun: options.dryRun,
      report,
    });
  }

  await writePluginShim({ ...options, target, skillRoot: resolved.root, report });
  await mergeOpenCodePackage({ ...options, target, report });
  return report;
}

export async function uninstallAssets(target: string): Promise<UninstallReport> {
  const root = path.resolve(target);
  const report: UninstallReport = { target: root, removed: [], skipped: [] };
  const relPaths = [
    ...await managedAssetPaths(),
    ".opencode/plugins/engineering-calc-system.ts",
    OPENCODE_PACKAGE_REL_PATH,
  ];
  for (const relPath of relPaths) {
    if (relPath === OPENCODE_PACKAGE_REL_PATH) {
      await uninstallOpenCodePackage(root, report);
      continue;
    }
    const fullPath = path.join(root, relPath);
    const content = await readTextIfExists(fullPath);
    if (!content) continue;
    if (!hasManagedMarker(relPath, content)) {
      report.skipped.push(relPath);
      continue;
    }
    await fs.rm(fullPath, { force: true });
    report.removed.push(relPath);
  }
  return report;
}

export async function inspectAssets(target: string): Promise<AssetStatus> {
  const root = path.resolve(target);
  const relPaths = [
    ...await managedAssetPaths(),
    ".opencode/plugins/engineering-calc-system.ts",
    OPENCODE_PACKAGE_REL_PATH,
  ];
  const present: string[] = [];
  const missing: string[] = [];
  const unmanagedPresent: string[] = [];
  for (const relPath of relPaths) {
    const fullPath = path.join(root, relPath);
    const content = await readTextIfExists(fullPath);
    if (!content) {
      missing.push(relPath);
      continue;
    }
    present.push(relPath);
    if (!hasManagedMarker(relPath, content)) unmanagedPresent.push(relPath);
  }
  return {
    installed: missing.length === 0 && unmanagedPresent.length === 0,
    present,
    missing,
    unmanagedPresent,
  };
}
