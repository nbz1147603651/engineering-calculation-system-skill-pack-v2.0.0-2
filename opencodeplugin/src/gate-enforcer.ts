/**
 * Optional experimental wiring for gate diagnostics into OpenCode's
 * `tool.execute.before` hook.
 *
 * This hook is disabled by default. Prefer OpenCode permissions, the core skill
 * workflow, and doctor/status diagnostics for normal project guardrails.
 */

import type { Hooks } from "@opencode-ai/plugin";
import {
  EditToolNames,
  evaluateEdit,
  extractContent,
  extractFilePath,
  loadGateState,
  type GateContext,
  type GateViolation,
} from "./gates.js";
import type { EngineeringCalcConfig } from "./config/schema.js";
import type { SkillRootInspection } from "./paths.js";

export interface GateHookDeps {
  config: EngineeringCalcConfig;
  rootStatus: SkillRootInspection;
  getTarget: () => string;
  getWorktree: () => string;
  log?: (level: "info" | "warn" | "error", message: string, extra?: Record<string, unknown>) => void;
}

function violationToLog(violation: GateViolation): string {
  const tag = violation.severity === "block" ? "[BLOCK]" : "[WARN]";
  return `${tag} gate=${violation.gate} ${violation.message}`;
}

function buildGateContext(deps: GateHookDeps): GateContext {
  return {
    target: deps.getTarget(),
    worktree: deps.getWorktree(),
    config: deps.config,
    rootStatus: deps.rootStatus,
  };
}

export function createGateEnforcer(deps: GateHookDeps): NonNullable<Hooks["tool.execute.before"]> {
  return async (input, output) => {
    if (!EditToolNames.has(input.tool)) return;

    const ctx = buildGateContext(deps);
    const state = loadGateState(ctx);

    const filePath = extractFilePath(input.tool, output.args);
    if (!filePath) return;

    const relPath = filePath.split(path_sep()).join("/");
    const content = extractContent(input.tool, output.args);
    const violations = evaluateEdit(ctx, state, relPath, content);

    if (violations.length === 0) return;

    for (const violation of violations) {
      deps.log?.(
        violation.severity === "block" ? "warn" : "info",
        violationToLog(violation),
        { gate: violation.gate, filePath: violation.filePath },
      );
    }

    const blocks = violations.filter((v) => v.severity === "block");
    if (blocks.length > 0) {
      const messages = blocks.map((v) => `- ${v.message}`).join("\n");
      throw new Error(
        `Engineering gate violation(s):\n${messages}\n` +
          `Set gates.runtimeHook to false or gates.enforcement to "warn" in engineering-calc-system.json to relax, ` +
          `or fix the violation.`,
      );
    }
  };
}

function path_sep(): string {
  return "/";
}
