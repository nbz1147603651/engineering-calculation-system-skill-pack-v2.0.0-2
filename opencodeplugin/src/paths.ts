import { existsSync, readdirSync, readFileSync, statSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

export type SkillRootSource =
  | "env"
  | "worktree"
  | "directory"
  | "plugin-adjacent"
  | "plugin-assets"
  | "missing";

export interface OpenCodePathContext {
  directory?: string;
  worktree?: string;
  configuredSkillRoot?: string;
}

export interface SkillRootInspection {
  root: string;
  source: SkillRootSource;
  exists: boolean;
  schemaVersion: string | undefined;
  missingRequiredPaths: string[];
}

export const TARGET_SCHEMA_VERSION = "2.4.0";

export const REQUIRED_SKILL_PATHS = [
  "SKILL.md",
  "skills/00-engineering-calculation-router.skill.md",
  "shared/quality-gates.md",
  "shared/multi-agent-orchestration.md",
  "templates/orchestration/parallel_work_plan.yaml",
  "templates/orchestration/agent_result_packet.yaml",
  "templates/orchestration/merge_review.md",
  "schemas/artifact_contracts.json",
  "scripts/validate_artifacts.py",
] as const;

const moduleFile = fileURLToPath(import.meta.url);
const pluginDistDir = path.dirname(moduleFile);
const pluginRoot = path.resolve(pluginDistDir, "..");

function normalizeCandidate(candidate: string | undefined): string | undefined {
  if (!candidate) return undefined;
  return path.resolve(candidate);
}

function isDirectory(candidate: string): boolean {
  try {
    return statSync(candidate).isDirectory();
  } catch {
    return false;
  }
}

function schemaVersion(root: string): string | undefined {
  const schemaPath = path.join(root, "schemas", "artifact_contracts.json");
  if (!existsSync(schemaPath)) return undefined;
  try {
    const parsed = JSON.parse(readFileSync(schemaPath, "utf8")) as { version?: unknown };
    return typeof parsed.version === "string" ? parsed.version : undefined;
  } catch {
    return undefined;
  }
}

function addCandidate(
  roots: Array<{ root: string; source: SkillRootSource }>,
  root: string,
  source: SkillRootSource,
): void {
  roots.push({ root: path.resolve(root), source });
}

function addSkillPackCandidates(
  roots: Array<{ root: string; source: SkillRootSource }>,
  base: string | undefined,
  source: SkillRootSource,
): void {
  if (!base || !isDirectory(base)) return;

  try {
    const entries = readdirSync(base, { withFileTypes: true });
    for (const entry of entries) {
      const isCanonicalPackage = entry.name === "engineering-calculation-system";
      const isVersionedSkillPack = entry.name.startsWith("engineering-calculation-system-skill-pack-");
      if (!entry.isDirectory() || (!isCanonicalPackage && !isVersionedSkillPack)) {
        continue;
      }
      addCandidate(
        roots,
        path.join(base, entry.name, "core", "engineering-calculation-system"),
        source,
      );
    }
  } catch {
    // Ignore unreadable roots; the doctor tool will report the final candidates.
  }
}

function candidateRoots(ctx: OpenCodePathContext): Array<{ root: string; source: SkillRootSource }> {
  const roots: Array<{ root: string; source: SkillRootSource }> = [];

  const configuredRoot = normalizeCandidate(ctx.configuredSkillRoot);
  if (configuredRoot) addCandidate(roots, configuredRoot, "env");

  const envRoot = normalizeCandidate(process.env.ENGINEERING_CALC_SKILL_ROOT);
  if (envRoot) addCandidate(roots, envRoot, "env");

  for (const base of [ctx.worktree, ctx.directory].filter(Boolean) as string[]) {
    const source: SkillRootSource = base === ctx.worktree ? "worktree" : "directory";
    addCandidate(roots, base, source);
    addCandidate(roots, path.join(base, "engineering-calculation-system"), source);
    addCandidate(roots, path.join(base, "core", "engineering-calculation-system"), source);
    addSkillPackCandidates(roots, base, source);
    addSkillPackCandidates(roots, path.dirname(base), source);
  }

  addCandidate(roots, path.join(pluginRoot, "..", "core", "engineering-calculation-system"), "plugin-adjacent");
  addSkillPackCandidates(roots, path.resolve(pluginRoot, ".."), "plugin-adjacent");
  addCandidate(roots, path.join(pluginRoot, "assets", "engineering-calculation-system"), "plugin-assets");

  const seen = new Set<string>();
  return roots.filter((candidate) => {
    const key = path.normalize(candidate.root).toLowerCase();
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}

export function inspectSkillRoot(root: string, source: SkillRootSource): SkillRootInspection {
  const missingRequiredPaths = REQUIRED_SKILL_PATHS.filter((relPath) => {
    return !existsSync(path.join(root, relPath));
  });

  return {
    root,
    source,
    exists: existsSync(root),
    schemaVersion: schemaVersion(root),
    missingRequiredPaths,
  };
}

export function resolveSkillRoot(ctx: OpenCodePathContext): SkillRootInspection {
  const inspections = candidateRoots(ctx).map((candidate) => inspectSkillRoot(candidate.root, candidate.source));
  const exactMatch = inspections.find(
    (inspection) =>
      inspection.schemaVersion === TARGET_SCHEMA_VERSION && inspection.missingRequiredPaths.length === 0,
  );
  if (exactMatch) return exactMatch;

  const complete = inspections.find((inspection) => inspection.missingRequiredPaths.length === 0);
  if (complete) return complete;

  const fallback = candidateRoots(ctx)[0]?.root ?? process.cwd();
  return inspectSkillRoot(fallback, "missing");
}

export function toPosixPath(value: string): string {
  return value.split(path.sep).join("/");
}
