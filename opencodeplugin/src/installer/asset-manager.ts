import { existsSync, readFileSync } from "node:fs";
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import type { EngineeringCalcConfig } from "../config/schema.js";
import {
  computeSha256,
  diffManifests,
  emptyManifest,
  readManifest,
  writeManifest,
  type InstallManifest,
} from "../manifest.js";
import { resolveSkillRoot, toPosixPath } from "../paths.js";
import { readPluginMeta } from "../plugin-meta.js";

export const MANAGED_MARKER = "engineering-calc-opencode-managed";
const OPENCODE_PACKAGE_REL_PATH = ".opencode/package.json";
const OPENCODE_PLUGIN_DEPENDENCY = "@opencode-ai/plugin";
const OPENCODE_PACKAGE_MANAGED_KEY = "engineeringCalcOpenCodeManaged";
const OPENCODE_PLUGIN_DEPENDENCY_VERSION = "^1.17.7";

const moduleFile = fileURLToPath(import.meta.url);
const distDir = path.dirname(moduleFile);
const packageRoot = path.resolve(distDir, "..", "..");
const templateRoot = path.join(packageRoot, "templates");

const legacyAssets = [
  ".opencode/agents/engineering-calc-architect.md",
  ".opencode/agents/engineering-calc-builder.md",
];

/**
 * Paths that the OpenCode plugin must never write to, regardless of
 * configuration. These protect the Codex plugin and the shared skill pack.
 */
const CROSS_PLATFORM_PROTECTED_PREFIXES = [
  "plugins/engineering-calculation-system",
  "engineering-calculation-system/core",
];

interface OpenCodePackageManagedMeta {
  opencodePluginDependencyAdded?: boolean;
}

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
  pluginVersion: string;
  skillPackSchemaVersion: string;
  installed: string[];
  modified: string[];
  skipped: string[];
  backups: string[];
  removedLegacy: string[];
  dryRun: boolean;
  diff: { added: string[]; modified: string[]; removed: string[] };
}

export interface UninstallReport {
  target: string;
  removed: string[];
  skipped: string[];
  manifestRemoved: boolean;
  backupDir: string | null;
}

export interface AssetStatus {
  installed: boolean;
  present: string[];
  missing: string[];
  unmanagedPresent: string[];
  manifest: { pluginVersion: string; installedAt: string } | null;
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
    return parsed[OPENCODE_PACKAGE_MANAGED_KEY] === true ||
      (typeof parsed[OPENCODE_PACKAGE_MANAGED_KEY] === "object" && parsed[OPENCODE_PACKAGE_MANAGED_KEY] !== null);
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

function isCrossPlatformProtected(relPath: string): boolean {
  const normalized = toPosixPath(relPath).replace(/^\.\//, "");
  return CROSS_PLATFORM_PROTECTED_PREFIXES.some(
    (prefix) => normalized === prefix || normalized.startsWith(`${prefix}/`),
  );
}

function isProtectedTarget(target: string): boolean {
  const normalized = toPosixPath(path.resolve(target));
  return CROSS_PLATFORM_PROTECTED_PREFIXES.some((prefix) => {
    const boundary = `/${prefix}`;
    return normalized.endsWith(boundary) || normalized.includes(`${boundary}/`);
  });
}

function assertTargetAllowed(target: string): void {
  if (!isProtectedTarget(target)) return;
  throw new Error(
    `Refusing to manage OpenCode assets inside cross-platform protected target '${target}'. ` +
      `Install the OpenCode adapter at a project root, not inside the Codex plugin or shared core skill pack.`,
  );
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

interface WriteManagedArgs {
  destination: string;
  relPath: string;
  content: string;
  force?: boolean;
  dryRun?: boolean;
  report: InstallReport;
  manifest: InstallManifest;
}

async function writeManagedFile(args: WriteManagedArgs): Promise<void> {
  const { destination, relPath, content, report, manifest } = args;
  if (isCrossPlatformProtected(relPath)) {
    throw new Error(
      `Refusing to write cross-platform protected path '${relPath}'. ` +
        `The OpenCode plugin installer must not modify the Codex plugin or shared skill pack.`,
    );
  }
  const existing = await readTextIfExists(args.destination);
  if (existing && !existing.includes(MANAGED_MARKER) && !args.force) {
    args.report.skipped.push(toPosixPath(args.relPath));
    return;
  }
  if (existing && !existing.includes(MANAGED_MARKER) && args.force && !args.dryRun) {
    args.report.backups.push(await backupExisting(args.destination));
  }
  const finalContent = injectMarker(relPath, content);
  const sha = computeSha256(finalContent);
  const size = Buffer.byteLength(finalContent, "utf8");
  const wasPresent = Boolean(existing);
  args.report.installed.push(toPosixPath(args.relPath));
  if (wasPresent) args.report.modified.push(toPosixPath(args.relPath));
  if (!args.dryRun) {
    await fs.mkdir(path.dirname(args.destination), { recursive: true });
    await fs.writeFile(args.destination, finalContent, "utf8");
  }
  manifest.files[toPosixPath(args.relPath)] = { relPath: toPosixPath(args.relPath), sha256: sha, size };
}

async function writePluginShim(args: InstallOptions & { skillRoot: string; report: InstallReport; manifest: InstallManifest }): Promise<void> {
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
    manifest: args.manifest,
  });
}

async function mergeOpenCodePackage(
  args: InstallOptions & { report: InstallReport; manifest: InstallManifest },
): Promise<void> {
  const relPath = OPENCODE_PACKAGE_REL_PATH;
  const destination = path.join(args.target, relPath);
  let packageJson: Record<string, unknown> = {};
  const existing = await readTextIfExists(destination);
  if (existing) packageJson = JSON.parse(existing);
  const existingDependencies = (packageJson.dependencies as Record<string, string> | undefined) ?? {};
  const hadDependency = Object.prototype.hasOwnProperty.call(existingDependencies, OPENCODE_PLUGIN_DEPENDENCY);
  packageJson.dependencies = {
    ...existingDependencies,
    [OPENCODE_PLUGIN_DEPENDENCY]: existingDependencies[OPENCODE_PLUGIN_DEPENDENCY] ?? OPENCODE_PLUGIN_DEPENDENCY_VERSION,
  };
  const existingManaged = packageJson[OPENCODE_PACKAGE_MANAGED_KEY];
  const previousAdded =
    (typeof existingManaged === "object" &&
      existingManaged !== null &&
      (existingManaged as OpenCodePackageManagedMeta).opencodePluginDependencyAdded === true);
  packageJson[OPENCODE_PACKAGE_MANAGED_KEY] = {
    opencodePluginDependencyAdded: previousAdded || !hadDependency,
  } satisfies OpenCodePackageManagedMeta;
  const serializedPackageJson = `${JSON.stringify(packageJson, null, 2)}\n`;
  args.report.installed.push(relPath);
  if (!args.dryRun) {
    await fs.mkdir(path.dirname(destination), { recursive: true });
    await fs.writeFile(destination, serializedPackageJson, "utf8");
  }
  args.manifest.files[relPath] = {
    relPath,
    sha256: computeSha256(serializedPackageJson),
    size: Buffer.byteLength(serializedPackageJson, "utf8"),
  };
}

async function uninstallOpenCodePackage(
  root: string,
  report: UninstallReport,
  manifest: InstallManifest | null,
): Promise<void> {
  const fullPath = path.join(root, OPENCODE_PACKAGE_REL_PATH);
  const content = await readTextIfExists(fullPath);
  if (!content) return;
  const inManifest = manifest?.files[OPENCODE_PACKAGE_REL_PATH];
  if (!hasManagedMarker(OPENCODE_PACKAGE_REL_PATH, content) && !inManifest) {
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
  const managed = packageJson[OPENCODE_PACKAGE_MANAGED_KEY];
  const shouldRemoveDependency =
    typeof managed === "object" &&
    managed !== null &&
    (managed as OpenCodePackageManagedMeta).opencodePluginDependencyAdded === true;
  if (dependencies && shouldRemoveDependency) {
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

function readPackageMeta(): { version: string; schemaVersion: string } {
  return readPluginMeta();
}

export async function installAssets(options: InstallOptions): Promise<InstallReport> {
  const target = path.resolve(options.target);
  assertTargetAllowed(target);
  const resolved = resolveSkillRoot({
    directory: target,
    worktree: target,
    configuredSkillRoot: options.skillRoot ?? options.config.skillRoot,
  });
  if (resolved.missingRequiredPaths.length > 0) {
    throw new Error(`Skill root is incomplete: ${resolved.root}\nMissing:\n- ${resolved.missingRequiredPaths.join("\n- ")}`);
  }

  const meta = readPackageMeta();
  const previous = await readManifest(target);
  const manifest = emptyManifest(meta.version, meta.schemaVersion);

  const report: InstallReport = {
    target,
    skillRoot: resolved.root,
    pluginVersion: meta.version,
    skillPackSchemaVersion: meta.schemaVersion,
    installed: [],
    modified: [],
    skipped: [],
    backups: [],
    removedLegacy: [],
    dryRun: Boolean(options.dryRun),
    diff: { added: [], modified: [], removed: [] },
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
    if (isCrossPlatformProtected(relPath)) {
      // Templates should never include cross-platform paths, but defend in depth.
      throw new Error(`Template path is cross-platform protected: ${relPath}`);
    }
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
      manifest,
    });
  }

  await writePluginShim({ ...options, target, skillRoot: resolved.root, report, manifest });
  await mergeOpenCodePackage({ ...options, target, report, manifest });

  // Compute the diff AFTER all writes so it reflects the actual change set
  // compared to the previously installed manifest.
  const finalManifest: InstallManifest = { ...manifest, installedAt: new Date().toISOString() };
  report.diff = diffManifests(previous, finalManifest);

  if (!options.dryRun) {
    await writeManifest(target, finalManifest);
  }

  return report;
}

export async function uninstallAssets(target: string): Promise<UninstallReport> {
  const root = path.resolve(target);
  assertTargetAllowed(root);
  const report: UninstallReport = {
    target: root,
    removed: [],
    skipped: [],
    manifestRemoved: false,
    backupDir: null,
  };
  const manifest = await readManifest(root);
  const backupDir = path.join(root, ".opencode", ".engineering-calc-backup");
  if (manifest) {
    await fs.mkdir(backupDir, { recursive: true });
    report.backupDir = toPosixPath(path.relative(root, backupDir));
  }

  const relPaths = new Set<string>([
    ...await managedAssetPaths(),
    ".opencode/plugins/engineering-calc-system.ts",
    OPENCODE_PACKAGE_REL_PATH,
  ]);
  if (manifest) {
    for (const relPath of Object.keys(manifest.files)) relPaths.add(relPath);
  }

  for (const relPath of relPaths) {
    if (relPath === OPENCODE_PACKAGE_REL_PATH) {
      await uninstallOpenCodePackage(root, report, manifest);
      continue;
    }
    const fullPath = path.join(root, relPath);
    const content = await readTextIfExists(fullPath);
    if (!content) continue;
    const inManifest = manifest?.files[relPath];
    if (!hasManagedMarker(relPath, content) && !inManifest) {
      report.skipped.push(relPath);
      continue;
    }
    if (manifest && !existsSync(backupDir)) {
      await fs.mkdir(backupDir, { recursive: true });
    }
    if (manifest) {
      const backupPath = path.join(backupDir, relPath.replace(/\//g, "__"));
      await fs.copyFile(fullPath, backupPath).catch(() => undefined);
    }
    await fs.rm(fullPath, { force: true });
    report.removed.push(relPath);
  }

  if (manifest) {
    const manifestPath = path.join(root, ".opencode", ".engineering-calc-manifest.json");
    if (existsSync(manifestPath)) {
      await fs.rm(manifestPath, { force: true });
      report.manifestRemoved = true;
    }
  }

  return report;
}

export async function inspectAssets(target: string): Promise<AssetStatus> {
  const root = path.resolve(target);
  const relPaths = new Set<string>([
    ...await managedAssetPaths(),
    ".opencode/plugins/engineering-calc-system.ts",
    OPENCODE_PACKAGE_REL_PATH,
  ]);
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
  const manifest = await readManifest(root);
  return {
    installed: missing.length === 0 && unmanagedPresent.length === 0,
    present,
    missing,
    unmanagedPresent,
    manifest: manifest
      ? { pluginVersion: manifest.pluginVersion, installedAt: manifest.installedAt }
      : null,
  };
}
