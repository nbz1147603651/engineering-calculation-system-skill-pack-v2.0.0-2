import type { EngineeringCalcConfig } from "../config/schema.js";
import type { SkillRootInspection } from "../paths.js";

export type CheckStatus = "pass" | "warn" | "fail" | "skip";

export interface CheckResult {
  name: string;
  status: CheckStatus;
  message: string;
  details?: string[];
  durationMs?: number;
}

export interface DoctorSummary {
  total: number;
  passed: number;
  warnings: number;
  failed: number;
  skipped: number;
  durationMs: number;
}

export interface DoctorContext {
  target: string;
  skillRoot: SkillRootInspection;
  config: EngineeringCalcConfig;
  configMessages: string[];
  configPath: string | null;
  timeoutMs: number;
}

export interface DoctorResult {
  target: string;
  skillRoot: SkillRootInspection;
  configPath: string | null;
  results: CheckResult[];
  summary: DoctorSummary;
  exitCode: number;
}

