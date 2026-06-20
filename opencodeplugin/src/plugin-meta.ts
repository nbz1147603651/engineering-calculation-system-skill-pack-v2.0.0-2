/**
 * Read the plugin's own package.json metadata.
 *
 * Platform-personal (used only by the OpenCode plugin). Provides a single
 * source of truth for the CLI version string and the target skill pack
 * schema version, so the CLI does not drift from package.json.
 */

import { existsSync, readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";

const moduleFile = fileURLToPath(import.meta.url);
const distDir = path.dirname(moduleFile);

function findPackageJson(): string | null {
  let dir = distDir;
  for (let i = 0; i < 6; i++) {
    const candidate = path.join(dir, "package.json");
    if (existsSync(candidate)) return candidate;
    const parent = path.dirname(dir);
    if (parent === dir) return null;
    dir = parent;
  }
  return null;
}

const packageJsonPath = findPackageJson();

let cached: { version: string; schemaVersion: string } | null = null;

export function readPluginMeta(): { version: string; schemaVersion: string } {
  if (cached) return cached;
  if (!packageJsonPath) {
    cached = { version: "unknown", schemaVersion: "unknown" };
    return cached;
  }
  try {
    const parsed = JSON.parse(readFileSync(packageJsonPath, "utf8")) as {
      version?: string;
      skillPack?: { schemaVersion?: string };
    };
    cached = {
      version: typeof parsed.version === "string" ? parsed.version : "unknown",
      schemaVersion:
        typeof parsed.skillPack?.schemaVersion === "string" ? parsed.skillPack.schemaVersion : "unknown",
    };
    return cached;
  } catch {
    cached = { version: "unknown", schemaVersion: "unknown" };
    return cached;
  }
}
