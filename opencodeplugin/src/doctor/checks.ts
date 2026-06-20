import { existsSync } from "node:fs";
import path from "node:path";
import { runPython } from "../process.js";
import { REQUIRED_SKILL_PATHS, TARGET_SCHEMA_VERSION } from "../paths.js";
import type { CheckResult, DoctorContext } from "./types.js";

export type CheckDefinition = {
  name: string;
  run(ctx: DoctorContext): Promise<CheckResult> | CheckResult;
};

function result(name: string, status: CheckResult["status"], message: string, details?: string[]): CheckResult {
  return { name, status, message, details };
}

export const checks: CheckDefinition[] = [
  {
    name: "skill-root",
    run(ctx) {
      if (!ctx.skillRoot.exists) return result("skill-root", "fail", "Skill root does not exist", [ctx.skillRoot.root]);
      return result("skill-root", "pass", "Skill root exists", [ctx.skillRoot.root]);
    },
  },
  {
    name: "schema-version",
    run(ctx) {
      if (ctx.skillRoot.schemaVersion !== TARGET_SCHEMA_VERSION) {
        return result(
          "schema-version",
          "fail",
          `Expected ${TARGET_SCHEMA_VERSION}, got ${ctx.skillRoot.schemaVersion ?? "unknown"}`,
        );
      }
      return result("schema-version", "pass", `Schema version is ${TARGET_SCHEMA_VERSION}`);
    },
  },
  {
    name: "required-files",
    run(ctx) {
      if (ctx.skillRoot.missingRequiredPaths.length > 0) {
        return result("required-files", "fail", "Required skill files are missing", ctx.skillRoot.missingRequiredPaths);
      }
      return result("required-files", "pass", `${REQUIRED_SKILL_PATHS.length} required files found`);
    },
  },
  {
    name: "orchestration-templates",
    run(ctx) {
      const required = [
        "shared/multi-agent-orchestration.md",
        "templates/orchestration/parallel_work_plan.yaml",
        "templates/orchestration/agent_result_packet.yaml",
        "templates/orchestration/merge_review.md",
      ];
      const missing = required.filter((relPath) => !existsSync(path.join(ctx.skillRoot.root, relPath)));
      if (missing.length > 0) return result("orchestration-templates", "fail", "Orchestration files missing", missing);
      return result("orchestration-templates", "pass", `v${TARGET_SCHEMA_VERSION} orchestration files found`);
    },
  },
  {
    name: "opencode-assets",
    run(ctx) {
      const required = [
        ".opencode/plugins/engineering-calc-system.ts",
        ".opencode/skills/engineering-calc-system/SKILL.md",
        ".opencode/commands/engineering-calc-start.md",
        ".opencode/agents/engineering-calc-supervisor.md",
      ];
      const missing = required.filter((relPath) => !existsSync(path.join(ctx.target, relPath)));
      if (missing.length > 0) return result("opencode-assets", "warn", "Project OpenCode assets are not fully installed", missing);
      return result("opencode-assets", "pass", "Project OpenCode assets are installed");
    },
  },
  {
    name: "config",
    run(ctx) {
      if (ctx.configMessages.length > 0) return result("config", "warn", "Config loaded with warnings", ctx.configMessages);
      return result("config", "pass", ctx.configPath ? "Config loaded" : "Using default config");
    },
  },
  {
    name: "mcp-policy",
    run(ctx) {
      if (ctx.config.mcpPresets.enabled && ctx.config.mcpPresets.allowed.length === 0) {
        return result("mcp-policy", "warn", "MCP presets enabled but no allowed presets are listed");
      }
      return result("mcp-policy", "pass", "MCP presets are conservative");
    },
  },
  {
    name: "optional-capabilities",
    async run(ctx) {
      if (ctx.skillRoot.missingRequiredPaths.length > 0) return result("optional-capabilities", "skip", "Skill root incomplete");
      const projectRoot = path.join(ctx.skillRoot.root, "project_template", "engineering_calc_project");
      if (!existsSync(projectRoot)) return result("optional-capabilities", "skip", "Project template not present");

      const script = [
        "import json, sys",
        `sys.path.insert(0, ${JSON.stringify(path.join(projectRoot, "src"))})`,
        "from pkg.core.capabilities import detect_capabilities",
        "caps = detect_capabilities()['capabilities']",
        "print(json.dumps({'marimo_review': caps['marimo_review']['status'], 'latex': caps['latex']['status'], 'docker': caps['docker']['status']}))",
      ].join("; ");
      const report = await runPython(["-c", script], { cwd: projectRoot, timeoutMs: ctx.timeoutMs });
      if (report.exitCode !== 0) {
        return result("optional-capabilities", "warn", "Optional capability detection could not run", [
          report.stdout.trim(),
          report.stderr.trim(),
        ].filter(Boolean));
      }

      try {
        const caps = JSON.parse(report.stdout.trim()) as Record<string, string>;
        const details = [
          `marimo_review: ${caps.marimo_review}`,
          `latex: ${caps.latex}`,
          `docker: ${caps.docker}`,
        ];
        if (caps.marimo_review === "configured") {
          return result("optional-capabilities", "pass", "Optional capabilities detected", details);
        }
        return result("optional-capabilities", "warn", "Marimo review is optional and not fully configured", [
          ...details,
          "Install with: python -m pip install marimo",
          "Set ADMIN_REVIEW_TOKEN before running the review admin.",
        ]);
      } catch {
        return result("optional-capabilities", "warn", "Optional capability report was not valid JSON", [report.stdout.trim()]);
      }
    },
  },
  {
    name: "python-validation",
    async run(ctx) {
      if (ctx.skillRoot.missingRequiredPaths.length > 0) return result("python-validation", "skip", "Skill root incomplete");
      const validation = await runPython(
        ["scripts/validate_artifacts.py", "--package-root", ".", "--profile", "core"],
        { cwd: ctx.skillRoot.root, timeoutMs: ctx.timeoutMs },
      );
      if (validation.exitCode === 0) return result("python-validation", "pass", "Core artifact validation passed");
      return result("python-validation", "fail", `Validation failed with exit code ${validation.exitCode}`, [
        validation.stdout.trim(),
        validation.stderr.trim(),
      ].filter(Boolean));
    },
  },
  {
    name: "project-template-validation",
    async run(ctx) {
      if (ctx.skillRoot.missingRequiredPaths.length > 0) return result("project-template-validation", "skip", "Skill root incomplete");
      const projectRoot = path.join(ctx.skillRoot.root, "project_template", "engineering_calc_project");
      if (!existsSync(projectRoot)) return result("project-template-validation", "skip", "Project template not present");
      const validation = await runPython(
        ["scripts/validate_artifacts.py", "--package-root", ".", "--profile", "core", "--project", projectRoot],
        { cwd: ctx.skillRoot.root, timeoutMs: ctx.timeoutMs },
      );
      if (validation.exitCode === 0) return result("project-template-validation", "pass", "Project template validation passed");
      return result("project-template-validation", "fail", `Project template validation failed with exit code ${validation.exitCode}`, [
        validation.stdout.trim(),
        validation.stderr.trim(),
      ].filter(Boolean));
    },
  },
];
