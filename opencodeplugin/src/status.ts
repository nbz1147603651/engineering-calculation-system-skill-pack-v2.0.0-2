import { loadConfig } from "./config/loader.js";
import type { PartialEngineeringCalcConfig } from "./config/schema.js";
import { loadGateState } from "./gates.js";
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
  const gateState = loadGateState({
    target: args.target,
    worktree: args.worktree ?? args.target,
    config: loaded.config,
    rootStatus: skillRoot,
  });
  return {
    target: args.target,
    configPath: loaded.path,
    configMessages: loaded.messages,
    skillRoot,
    assets,
    gates: {
      advisoryMode: gateState.mode,
      runtimeHook: loaded.config.gates.runtimeHook,
      diagnostics: gateState.enabledGates,
      handoffStatus: gateState.handoffStatus,
      handoffFrozen: gateState.handoffFrozen,
      activePlan: gateState.activePlan
        ? { planId: gateState.activePlan.planId, status: gateState.activePlan.status }
        : null,
    },
    preferredAgentOrder: loaded.config.agentOrder,
  };
}
