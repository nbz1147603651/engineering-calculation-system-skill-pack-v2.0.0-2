import { loadConfig } from "../config/loader.js";
import type { PartialEngineeringCalcConfig } from "../config/schema.js";
import { resolveSkillRoot } from "../paths.js";
import { checks } from "./checks.js";
import type { CheckResult, DoctorResult } from "./types.js";

export async function runDoctor(args: {
  target: string;
  overrides?: PartialEngineeringCalcConfig;
  includeValidation?: boolean;
}): Promise<DoctorResult> {
  const started = Date.now();
  const loaded = loadConfig(args.target, args.overrides ?? {});
  const skillRoot = resolveSkillRoot({
    directory: args.target,
    worktree: args.target,
    configuredSkillRoot: loaded.config.skillRoot,
  });

  const selectedChecks = args.includeValidation === false
    ? checks.filter((check) => check.name !== "python-validation" && check.name !== "project-template-validation")
    : checks;

  const results: CheckResult[] = [];
  for (const check of selectedChecks) {
    const checkStarted = Date.now();
    const checkResult = await check.run({
      target: args.target,
      skillRoot,
      config: loaded.config,
      configMessages: loaded.messages,
      configPath: loaded.path,
      timeoutMs: loaded.config.doctor.timeoutMs,
    });
    checkResult.durationMs = Date.now() - checkStarted;
    results.push(checkResult);
  }

  const summary = {
    total: results.length,
    passed: results.filter((item) => item.status === "pass").length,
    warnings: results.filter((item) => item.status === "warn").length,
    failed: results.filter((item) => item.status === "fail").length,
    skipped: results.filter((item) => item.status === "skip").length,
    durationMs: Date.now() - started,
  };

  return {
    target: args.target,
    skillRoot,
    configPath: loaded.path,
    results,
    summary,
    exitCode: summary.failed > 0 ? 1 : 0,
  };
}

