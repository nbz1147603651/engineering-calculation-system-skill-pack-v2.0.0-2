import { loadConfig } from "./config/loader.js";
import type { PartialEngineeringCalcConfig } from "./config/schema.js";
import { inspectAssets } from "./installer/asset-manager.js";
import { resolveSkillRoot } from "./paths.js";

export async function getStatus(args: {
  target: string;
  worktree?: string;
  overrides?: PartialEngineeringCalcConfig;
}) {
  const loaded = loadConfig(args.target, args.overrides ?? {});
  const skillRoot = resolveSkillRoot({
    directory: args.target,
    worktree: args.worktree ?? args.target,
    configuredSkillRoot: loaded.config.skillRoot,
  });
  const assets = await inspectAssets(args.target);
  return {
    target: args.target,
    configPath: loaded.path,
    configMessages: loaded.messages,
    skillRoot,
    assets,
  };
}

