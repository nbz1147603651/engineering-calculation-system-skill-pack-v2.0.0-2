/**
 * Install manifest for the OpenCode managed assets.
 *
 * The manifest records the version of the plugin that wrote each managed
 * file, so `update` can show a diff and `uninstall` can remove files
 * even when the managed marker has been lost. The manifest is platform
 * personal (OpenCode-only) and stored at `.opencode/.engineering-calc-manifest.json`.
 */

import { createHash } from "node:crypto";
import { existsSync, readFileSync } from "node:fs";
import fs from "node:fs/promises";
import path from "node:path";

export const MANIFEST_REL_PATH = ".opencode/.engineering-calc-manifest.json";
export const MANIFEST_VERSION = 1;

export interface ManifestEntry {
  /** Posix path relative to project root, e.g. ".opencode/AGENTS.md". */
  relPath: string;
  /** SHA-256 hex of the written content. */
  sha256: string;
  /** Size in bytes. */
  size: number;
}

export interface InstallManifest {
  manifestVersion: number;
  pluginVersion: string;
  skillPackSchemaVersion: string;
  installedAt: string;
  /** Map of relPath -> entry. */
  files: Record<string, ManifestEntry>;
}

export function emptyManifest(pluginVersion: string, skillPackSchemaVersion: string): InstallManifest {
  return {
    manifestVersion: MANIFEST_VERSION,
    pluginVersion,
    skillPackSchemaVersion,
    installedAt: new Date().toISOString(),
    files: {},
  };
}

export async function readManifest(target: string): Promise<InstallManifest | null> {
  const full = path.join(target, MANIFEST_REL_PATH);
  if (!existsSync(full)) return null;
  try {
    const raw = JSON.parse(await fs.readFile(full, "utf8")) as InstallManifest;
    if (typeof raw !== "object" || !raw || typeof raw.files !== "object") return null;
    return raw;
  } catch {
    return null;
  }
}

export async function writeManifest(target: string, manifest: InstallManifest): Promise<void> {
  const full = path.join(target, MANIFEST_REL_PATH);
  await fs.mkdir(path.dirname(full), { recursive: true });
  await fs.writeFile(full, `${JSON.stringify(manifest, null, 2)}\n`, "utf8");
}

export function computeSha256(content: string): string {
  return createHash("sha256").update(content, "utf8").digest("hex");
}

export function diffManifests(
  previous: InstallManifest | null,
  current: InstallManifest,
): {
  added: string[];
  modified: string[];
  removed: string[];
} {
  const added: string[] = [];
  const modified: string[] = [];
  const removed: string[] = [];
  const prevFiles = previous?.files ?? {};
  const currFiles = current.files;

  for (const [relPath, entry] of Object.entries(currFiles)) {
    const prev = prevFiles[relPath];
    if (!prev) {
      added.push(relPath);
    } else if (prev.sha256 !== entry.sha256) {
      modified.push(relPath);
    }
  }
  for (const relPath of Object.keys(prevFiles)) {
    if (!currFiles[relPath]) {
      removed.push(relPath);
    }
  }
  return { added, modified, removed };
}
