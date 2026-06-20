import type { Hooks } from "@opencode-ai/plugin";
import { compactionOrchestrationContext } from "./domain.js";
import { createGateEnforcer, type GateHookDeps } from "./gate-enforcer.js";
import { gateSummary } from "./tool-helpers.js";
import type { EngineeringCalcConfig } from "./config/schema.js";
import type { SkillRootInspection } from "./paths.js";

export interface CreateHooksArgs {
  config: EngineeringCalcConfig;
  rootStatus: SkillRootInspection;
  target: string;
  worktree: string;
  log?: GateHookDeps["log"];
}

export function createHooks(args: CreateHooksArgs): Pick<
  Hooks,
  "shell.env" | "experimental.session.compacting"
> & Partial<Pick<Hooks, "tool.execute.before">> {
  const hooks: Pick<Hooks, "shell.env" | "experimental.session.compacting"> &
    Partial<Pick<Hooks, "tool.execute.before">> = {
    "shell.env": async (_input, output) => {
      if (args.rootStatus.missingRequiredPaths.length === 0) {
        output.env.ENGINEERING_CALC_SKILL_ROOT ??= args.rootStatus.root;
      }
    },
    "experimental.session.compacting": async (_input, output) => {
      output.context.push(`
## Engineering Calculation System Context

Preserve the active engineering calculation phase, evidence/coding gate state, source authority decisions, unresolved source gaps, changed artifact files, validation status, and whether official calculations still flow through run_book(BookInput) -> BookResult.

OpenCode gate diagnostics: ${args.config.gates.enforcement}
Experimental runtime gate hook: ${args.config.gates.runtimeHook ? "enabled" : "disabled"}

${compactionOrchestrationContext()}

${gateSummary()}
`);
    },
  };

  if (args.config.gates.runtimeHook) {
    hooks["tool.execute.before"] = createGateEnforcer({
      config: args.config,
      rootStatus: args.rootStatus,
      getTarget: () => args.target,
      getWorktree: () => args.worktree,
      log: args.log,
    });
  }

  return hooks;
}
