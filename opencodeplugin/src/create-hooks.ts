import type { Hooks } from "@opencode-ai/plugin";
import { compactionOrchestrationContext } from "./domain.js";
import { gateSummary } from "./tool-helpers.js";
import type { EngineeringCalcConfig } from "./config/schema.js";
import type { SkillRootInspection } from "./paths.js";

export function createHooks(args: {
  config: EngineeringCalcConfig;
  rootStatus: SkillRootInspection;
}): Pick<Hooks, "shell.env" | "experimental.session.compacting"> {
  return {
    "shell.env": async (_input, output) => {
      if (args.rootStatus.missingRequiredPaths.length === 0) {
        output.env.ENGINEERING_CALC_SKILL_ROOT ??= args.rootStatus.root;
      }
    },
    "experimental.session.compacting": async (_input, output) => {
      output.context.push(`
## Engineering Calculation System Context

Preserve the active engineering calculation phase, evidence/coding gate state, source authority decisions, unresolved source gaps, changed artifact files, validation status, and whether official calculations still flow through run_book(BookInput) -> BookResult.

Strict gate mode: ${args.config.strictGateMode ? "enabled" : "disabled"}

${compactionOrchestrationContext()}

${gateSummary(args.config.strictGateMode)}
`);
    },
  };
}
