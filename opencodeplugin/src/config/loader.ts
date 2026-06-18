import { existsSync, readFileSync } from "node:fs";
import { homedir } from "node:os";
import path from "node:path";
import { parse as parseJsonc } from "jsonc-parser";
import {
  EngineeringCalcConfigSchema,
  USER_ONLY_CONFIG_KEYS,
  type EngineeringCalcConfig,
  type PartialEngineeringCalcConfig,
} from "./schema.js";
import { mergeConfigLayers } from "./merge.js";

export const CONFIG_BASENAME = "engineering-calc-system";

export interface ConfigLayer {
  path: string;
  scope: "user" | "project";
  config: Partial<EngineeringCalcConfig>;
  messages: string[];
}

export interface LoadedConfig {
  config: EngineeringCalcConfig;
  layers: ConfigLayer[];
  messages: string[];
  path: string | null;
}

function homeDir(): string {
  return process.env.HOME ?? process.env.USERPROFILE ?? homedir();
}

function userConfigDirs(): string[] {
  if (process.platform === "win32") {
    return [path.join(process.env.APPDATA ?? path.join(homeDir(), "AppData", "Roaming"), "opencode")];
  }
  return [path.join(process.env.XDG_CONFIG_HOME ?? path.join(homeDir(), ".config"), "opencode")];
}

function configPathIn(dir: string): string | null {
  for (const extension of [".jsonc", ".json"]) {
    const candidate = path.join(dir, `${CONFIG_BASENAME}${extension}`);
    if (existsSync(candidate)) return candidate;
  }
  return null;
}

function parentDirsNearestFirst(directory: string): string[] {
  const dirs: string[] = [];
  let current = path.resolve(directory);
  const home = path.resolve(homeDir());
  while (true) {
    dirs.push(current);
    if (current === home || current === path.dirname(current)) break;
    current = path.dirname(current);
  }
  return dirs;
}

function stripProjectOnlySensitiveFields(raw: Record<string, unknown>, messages: string[], filePath: string): void {
  for (const key of USER_ONLY_CONFIG_KEYS) {
    if (key in raw) {
      delete raw[key];
      messages.push(`${filePath}: ${key} is user-only and was ignored in project config`);
    }
  }
}

function parseConfigFile(filePath: string, scope: ConfigLayer["scope"]): ConfigLayer {
  const messages: string[] = [];
  try {
    const raw = parseJsonc(readFileSync(filePath, "utf8"));
    if (!raw || typeof raw !== "object" || Array.isArray(raw)) {
      return { path: filePath, scope, config: {}, messages: [`${filePath}: expected object config`] };
    }
    const record = { ...(raw as Record<string, unknown>) };
    if (scope === "project") {
      stripProjectOnlySensitiveFields(record, messages, filePath);
    }
    const parsed = EngineeringCalcConfigSchema.partial().safeParse(record);
    if (!parsed.success) {
      messages.push(...parsed.error.issues.map((issue) => `${filePath}: ${issue.path.join(".") || "<root>"}: ${issue.message}`));
      return { path: filePath, scope, config: record as PartialEngineeringCalcConfig, messages };
    }
    return { path: filePath, scope, config: parsed.data as PartialEngineeringCalcConfig, messages };
  } catch (error) {
    return {
      path: filePath,
      scope,
      config: {},
      messages: [`${filePath}: ${error instanceof Error ? error.message : String(error)}`],
    };
  }
}

export function discoverConfigLayers(directory: string): ConfigLayer[] {
  const userLayers = userConfigDirs()
    .map(configPathIn)
    .filter((value): value is string => Boolean(value))
    .map((filePath) => parseConfigFile(filePath, "user"));

  const projectPaths = parentDirsNearestFirst(directory)
    .map((dir) => configPathIn(path.join(dir, ".opencode")))
    .filter((value): value is string => Boolean(value));

  const projectLayers = [...projectPaths].reverse().map((filePath) => parseConfigFile(filePath, "project"));
  return [...userLayers, ...projectLayers];
}

export function loadConfig(directory: string, overrides: Partial<EngineeringCalcConfig> = {}): LoadedConfig {
  const layers = discoverConfigLayers(directory);
  const config = mergeConfigLayers([...layers.map((layer) => layer.config), overrides]);
  const messages = layers.flatMap((layer) => layer.messages);
  return {
    config,
    layers,
    messages,
    path: layers.at(-1)?.path ?? layers[0]?.path ?? null,
  };
}

export function minimalConfigExample(): string {
  return `{
  "$schema": "./engineering-calc-system.schema.json",
  "strictGateMode": true,
  "defaultPhase": "router"
}`;
}

export function fullConfigExample(): string {
  return `{
  "$schema": "./engineering-calc-system.schema.json",
  "skillRoot": "../engineering-calculation-system/core/engineering-calculation-system",
  "strictGateMode": true,
  "defaultPhase": "router",
  "doctor": {
    "validateOnStartup": false,
    "timeoutMs": 30000
  },
  "orchestration": {
    "enabled": true,
    "readOnlyDrafts": true
  },
  "agents": {
    "disabled": [],
    "roleOverrides": {
      "engineering-calc-module-worker": {
        "description": "Implements one bounded reusable calculation module."
      }
    }
  },
  "agentOrder": [
    "engineering-calc-supervisor",
    "engineering-calc-module-worker",
    "engineering-calc-verification-worker"
  ],
  "commands": {
    "disabled": []
  },
  "mcpPresets": {
    "enabled": false,
    "allowed": []
  }
}`;
}
