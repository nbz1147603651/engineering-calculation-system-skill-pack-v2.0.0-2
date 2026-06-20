/**
 * Engineering gate diagnostics module.
 *
 * This module implements the most deterministic "non-negotiable gates" as
 * advisory diagnostics. The optional `tool.execute.before` hook can use the
 * same checks when explicitly enabled, but runtime blocking is no longer the
 * default OpenCode posture. The core skill pack remains the source of truth for
 * engineering workflow rules.
 *
 * Platform-specific: this is OpenCode-only. The Codex plugin and the core
 * skill pack must not be affected.
 */

import { existsSync, readFileSync } from "node:fs";
import path from "node:path";
import type { EngineeringCalcConfig } from "./config/schema.js";
import type { SkillRootInspection } from "./paths.js";

export type GateEnforcementMode = "off" | "warn" | "strict";

export interface GateViolation {
  gate: GateName;
  severity: "block" | "warn";
  message: string;
  filePath?: string;
}

export type GateName =
  | "handoff-freeze"
  | "owned-paths"
  | "formula-in-presentation"
  | "protected-registries"
  | "cross-platform-boundary";

export interface GateContext {
  target: string;
  worktree: string;
  config: EngineeringCalcConfig;
  rootStatus: SkillRootInspection;
}

export interface GateState {
  handoffFrozen: boolean;
  handoffStatus: "frozen" | "active" | "missing" | "unknown";
  activePlan: ParallelWorkPlanSummary | null;
  mode: GateEnforcementMode;
  enabledGates: GateName[];
}

/**
 * Subset of the parallel_work_plan schema that the gate enforcer needs.
 */
export interface ParallelWorkPlanSummary {
  planId: string;
  status: string;
  tasks: Array<{
    taskId: string;
    ownedPaths: string[];
  }>;
}

const HandoffFileNames = new Set([
  "implementation_handoff.yaml",
  "coding_go_no_go.md",
]);

const ProtectedRegistryPatterns = [
  /(^|\/)references\/source_registry\.yaml$/,
  /(^|\/)references\/formula_registry\.yaml$/,
  /(^|\/)references\/lookup_registry\.yaml$/,
  /(^|\/)references\/branch_registry\.yaml$/,
  /(^|\/)references\/module_registry\.yaml$/,
];

const PresentationLayerPatterns = [
  /(^|\/)webapp\/static\/js\//,
  /(^|\/)webapp\/templates\//,
  /(^|\/)webapp\/static\/css\//,
  /(^|\/)notebooks\//,
  /(^|\/)batch_scripts\//,
  /(^|\/)templates\/implementation\/ui_design_system\.md$/,
];

const InputFileExtensions = [".csv", ".xlsx", ".xls"];

/**
 * Heuristic patterns that suggest formula content in non-formula files.
 * Used only for the `formula-in-presentation` gate.
 */
const FormulaContentPatterns: RegExp[] = [
  /\bdef\s+\w+\s*\([^)]*\)\s*:/,           // Python def
  /=\s*[A-Za-z_][A-Za-z0-9_]*\s*\(/,       // function call assignment
  /\b[0-9]+(?:\.[0-9]+)?\s*[\*\/]\s*[0-9]+(?:\.[0-9]+)?/,  // arithmetic
  /\*\*\s*[0-9]/,                          // exponent
  /\b(?:coefficient|lookup|formula|gamma|sigma|lambda)\s*[:=]/i,
];

const CrossPlatformProtectedRoots = [
  "plugins/engineering-calculation-system",
  "engineering-calculation-system/core",
];

function readIfExists(filePath: string): string | null {
  if (!existsSync(filePath)) return null;
  try {
    return readFileSync(filePath, "utf8");
  } catch {
    return null;
  }
}

function resolveHandoffDir(target: string): string | null {
  const candidates = [
    path.join(target, "handoff"),
    path.join(target, "..", "handoff"),
    path.join(target, "..", "..", "handoff"),
  ];
  for (const candidate of candidates) {
    if (existsSync(candidate)) return candidate;
  }
  return null;
}

function resolveHandoffDirFromSkillRoot(skillRoot: string): string | null {
  return resolveHandoffDir(skillRoot);
}

function isHandoffFrozen(handoffDir: string): boolean {
  const goNoGo = readIfExists(path.join(handoffDir, "coding_go_no_go.md"));
  if (!goNoGo) return false;
  // Match a top-level decision: `decision: go` or `status: frozen` (case-insensitive).
  const decisionMatch = /(?:^|\n)\s*(?:decision|status)\s*:\s*([A-Za-z_-]+)/i.exec(goNoGo);
  if (!decisionMatch) return false;
  const decision = decisionMatch[1].toLowerCase();
  return decision === "go" || decision === "frozen" || decision === "approved";
}

function getHandoffStatus(target: string, skillRoot: string): {
  status: GateState["handoffStatus"];
  frozen: boolean;
} {
  const dir = resolveHandoffDir(target) ?? resolveHandoffDirFromSkillRoot(skillRoot);
  if (!dir) return { status: "missing", frozen: false };
  const hasHandoff = existsSync(path.join(dir, "implementation_handoff.yaml"));
  const hasGoNoGo = existsSync(path.join(dir, "coding_go_no_go.md"));
  if (!hasHandoff && !hasGoNoGo) return { status: "missing", frozen: false };
  const frozen = isHandoffFrozen(dir);
  return { status: frozen ? "frozen" : "active", frozen };
}

function findActivePlan(target: string): ParallelWorkPlanSummary | null {
  const candidates = [
    path.join(target, "handoff", "active_plan.yaml"),
    path.join(target, ".opencode", "active_plan.yaml"),
    path.join(target, "parallel_work_plan.yaml"),
  ];
  for (const candidate of candidates) {
    const text = readIfExists(candidate);
    if (!text) continue;
    try {
      return parsePlanSummary(text);
    } catch {
      continue;
    }
  }
  return null;
}

function parsePlanSummary(text: string): ParallelWorkPlanSummary {
  // Lightweight key/value extraction to avoid a YAML dependency at runtime.
  const lines = text.split(/\r?\n/);
  const tasks: ParallelWorkPlanSummary["tasks"] = [];
  let planId = "PWP-000";
  let status = "draft";
  let currentTask: ParallelWorkPlanSummary["tasks"][number] | null = null;

  for (const line of lines) {
    const planMatch = /^\s*plan_id\s*:\s*(\S+)/.exec(line);
    if (planMatch) {
      planId = planMatch[1];
      continue;
    }
    const statusMatch = /^\s*status\s*:\s*(\S+)/.exec(line);
    if (statusMatch) {
      status = statusMatch[1];
      continue;
    }
    const taskMatch = /^\s*-\s*task_id\s*:\s*(\S+)/.exec(line);
    if (taskMatch) {
      if (currentTask) tasks.push(currentTask);
      currentTask = { taskId: taskMatch[1], ownedPaths: [] };
      continue;
    }
    const ownedMatch = /^\s*-\s*(.+)/.exec(line);
    if (ownedMatch && currentTask && /owned_paths/.test(prevLineKey(lines, lines.indexOf(line)))) {
      currentTask.ownedPaths.push(ownedMatch[1].trim());
    }
  }
  if (currentTask) tasks.push(currentTask);

  return { planId, status, tasks };
}

function prevLineKey(lines: string[], idx: number): string {
  for (let j = idx - 1; j >= 0; j--) {
    if (lines[j].trim() !== "") return lines[j];
  }
  return "";
}

function normalizePath(value: string): string {
  return value.split(path.sep).join("/").replace(/^\.\//, "");
}

function matchesAnyPattern(value: string, patterns: RegExp[]): boolean {
  const normalized = normalizePath(value);
  return patterns.some((pattern) => pattern.test(normalized));
}

function isPresentationLayerPath(relPath: string): boolean {
  return matchesAnyPattern(relPath, PresentationLayerPatterns);
}

function isInputFilePath(relPath: string): boolean {
  const lower = relPath.toLowerCase();
  return InputFileExtensions.some((ext) => lower.endsWith(ext));
}

function isHandoffFile(relPath: string): boolean {
  return Array.from(HandoffFileNames).some(
    (name) => relPath === name || relPath.endsWith(`/${name}`),
  );
}

function isProtectedRegistry(relPath: string): boolean {
  return matchesAnyPattern(relPath, ProtectedRegistryPatterns);
}

function isCrossPlatformBoundary(relPath: string): boolean {
  const normalized = normalizePath(relPath);
  return CrossPlatformProtectedRoots.some(
    (root) => normalized === root || normalized.startsWith(`${root}/`),
  );
}

function isWithinAny(relPath: string, ownedPaths: string[]): boolean {
  const normalized = normalizePath(relPath);
  return ownedPaths.some((owned) => {
    const owner = normalizePath(owned).replace(/\/+$/, "");
    if (!owner) return false;
    return normalized === owner || normalized.startsWith(`${owner}/`);
  });
}

function looksLikeFormulaContent(content: string): boolean {
  return FormulaContentPatterns.some((pattern) => pattern.test(content));
}

export function loadGateState(ctx: GateContext): GateState {
  const handoff = getHandoffStatus(ctx.target, ctx.rootStatus.root);
  const activePlan = findActivePlan(ctx.target);
  const mode = resolveEnforcementMode(ctx.config);
  const enabledGates = enabledGateNames(ctx.config);

  return {
    handoffFrozen: handoff.frozen,
    handoffStatus: handoff.status,
    activePlan,
    mode,
    enabledGates,
  };
}

function resolveEnforcementMode(config: EngineeringCalcConfig): GateEnforcementMode {
  const gate = config.gates;
  return gate?.enforcement ?? "warn";
}

function enabledGateNames(config: EngineeringCalcConfig): GateName[] {
  const defaults: GateName[] = [
    "handoff-freeze",
    "owned-paths",
    "formula-in-presentation",
    "protected-registries",
    "cross-platform-boundary",
  ];
  const gate = config.gates;
  if (!gate) return defaults;
  if (gate.enabled === false) return [];
  if (!gate.disable || gate.disable.length === 0) return defaults;
  return defaults.filter((name) => !gate.disable!.includes(name));
}

export interface ToolExecutionInput {
  tool: string;
  args: unknown;
}

export interface ToolExecutionOutput {
  args: unknown;
  title?: string;
  output?: string;
  metadata?: unknown;
}

export function evaluateEdit(
  ctx: GateContext,
  state: GateState,
  relPath: string,
  content: string | undefined,
): GateViolation[] {
  const violations: GateViolation[] = [];

  // 1. Cross-platform boundary — always strict regardless of mode. This is
  // a safety invariant to protect the Codex plugin and shared skill pack
  // from accidental writes by the OpenCode plugin.
  if (isCrossPlatformBoundary(relPath)) {
    violations.push({
      gate: "cross-platform-boundary",
      severity: "block",
      message: `Refusing to write to cross-platform boundary path '${relPath}'. The OpenCode plugin must not modify the Codex plugin or the shared skill pack.`,
      filePath: relPath,
    });
    return violations;
  }

  if (state.mode === "off") return violations;

  // 2. Handoff freeze — block writes to handoff files when frozen.
  if (
    state.enabledGates.includes("handoff-freeze") &&
    state.handoffFrozen &&
    isHandoffFile(relPath)
  ) {
    violations.push({
      gate: "handoff-freeze",
      severity: state.mode === "strict" ? "block" : "warn",
      message: `Handoff is frozen; refusing to write '${relPath}'. Update coding_go_no_go.md decision first.`,
      filePath: relPath,
    });
  }

  // 3. Protected registries — supervisor-only.
  if (state.enabledGates.includes("protected-registries") && isProtectedRegistry(relPath)) {
    violations.push({
      gate: "protected-registries",
      severity: state.mode === "strict" ? "block" : "warn",
      message: `'${relPath}' is a supervisor-only registry. Delegate via a plan, not a direct edit.`,
      filePath: relPath,
    });
  }

  // 4. owned_paths enforcement — when an active plan is present.
  if (state.enabledGates.includes("owned-paths") && state.activePlan) {
    const allOwned = state.activePlan.tasks.flatMap((task) => task.ownedPaths);
    if (allOwned.length > 0 && !isWithinAny(relPath, allOwned)) {
      violations.push({
        gate: "owned-paths",
        severity: state.mode === "strict" ? "block" : "warn",
        message: `Active plan ${state.activePlan.planId} restricts edits to declared owned_paths. '${relPath}' is not owned by any task.`,
        filePath: relPath,
      });
    }
  }

  // 5. Formula-in-presentation heuristic.
  if (
    state.enabledGates.includes("formula-in-presentation") &&
    content !== undefined &&
    (isPresentationLayerPath(relPath) || isInputFilePath(relPath)) &&
    looksLikeFormulaContent(content)
  ) {
    violations.push({
      gate: "formula-in-presentation",
      severity: state.mode === "strict" ? "block" : "warn",
      message: `'${relPath}' looks like a presentation or input layer but the new content appears to contain formula logic. Move it to a reusable calculation module.`,
      filePath: relPath,
    });
  }

  return violations;
}

/**
 * Extract the file path argument from a tool call. Defensive against
 * multiple tool arg shapes.
 */
export function extractFilePath(tool: string, args: unknown): string | null {
  if (!args || typeof args !== "object") return null;
  const record = args as Record<string, unknown>;
  const candidates = ["filePath", "path", "filepath", "file", "target"];
  for (const key of candidates) {
    if (typeof record[key] === "string") return record[key] as string;
  }
  return null;
}

/**
 * Extract the content argument from a tool call.
 */
export function extractContent(tool: string, args: unknown): string | undefined {
  if (!args || typeof args !== "object") return undefined;
  const record = args as Record<string, unknown>;
  const candidates = ["content", "newString", "text", "data"];
  for (const key of candidates) {
    if (typeof record[key] === "string") return record[key] as string;
  }
  return undefined;
}

export const EditToolNames = new Set([
  "edit",
  "write",
  "create",
  "patch",
  "applyEdit",
  "edit_file",
  "write_file",
  "create_file",
  "multi_edit",
]);
