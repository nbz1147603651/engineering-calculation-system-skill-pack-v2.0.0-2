import { type Plugin, tool } from "@opencode-ai/plugin";
import path from "node:path";
import {
  compactionOrchestrationContext,
  gateSummary,
  ORCHESTRATION_ARTIFACTS,
  ORCHESTRATION_PHASES,
  orchestrationGuidance,
  orchestrationLoadOrder,
  phasePrompt,
  PHASES,
  renderOrchestrationDraft,
  supervisorOnlyDecisions,
  workerOwnershipRules,
} from "./domain.js";
import { resolveSkillRoot, TARGET_SCHEMA_VERSION, toPosixPath } from "./paths.js";
import { runPython } from "./process.js";

function formatSkillRootStatus(rootStatus: ReturnType<typeof resolveSkillRoot>): string {
  const missing =
    rootStatus.missingRequiredPaths.length === 0
      ? "none"
      : rootStatus.missingRequiredPaths.map((item) => `- ${item}`).join("\n");

  return [
    `Skill root: ${rootStatus.root}`,
    `Source: ${rootStatus.source}`,
    `Exists: ${rootStatus.exists ? "yes" : "no"}`,
    `Schema version: ${rootStatus.schemaVersion ?? "unknown"}`,
    `Target schema: ${TARGET_SCHEMA_VERSION}`,
    "Missing required paths:",
    missing,
  ].join("\n");
}

function arrayArg(description: string) {
  return tool.schema.array(tool.schema.string()).default([]).describe(description);
}

export const EngineeringCalculationSystemPlugin: Plugin = async (ctx) => {
  const rootStatus = resolveSkillRoot({
    directory: ctx.directory,
    worktree: ctx.worktree,
  });

  await ctx.client.app
    .log({
      body: {
        service: "engineering-calculation-system-opencode-plugin",
        level: rootStatus.missingRequiredPaths.length === 0 ? "info" : "warn",
        message: "Plugin initialized",
        extra: {
          skillRoot: rootStatus.root,
          source: rootStatus.source,
          missingRequiredPaths: rootStatus.missingRequiredPaths,
        },
      },
    })
    .catch(() => undefined);

  return {
    "shell.env": async (_input, output) => {
      if (rootStatus.missingRequiredPaths.length === 0) {
        output.env.ENGINEERING_CALC_SKILL_ROOT ??= rootStatus.root;
      }
    },

    "experimental.session.compacting": async (_input, output) => {
      output.context.push(`
## Engineering Calculation System Context

Preserve the active engineering calculation phase, evidence/coding gate state, source authority decisions, unresolved source gaps, changed artifact files, validation status, and whether official calculations still flow through run_book(BookInput) -> BookResult.

${compactionOrchestrationContext()}

${gateSummary()}
`);
    },

    tool: {
      engineering_calc_route: tool({
        description:
          "Return the Engineering Calculation System OpenCode routing prompt, load order, and phase-specific gates.",
        args: {
          phase: tool.schema
            .enum(PHASES)
            .default("router")
            .describe("Workflow phase to route. Use router when unsure."),
          parallel: tool.schema
            .boolean()
            .default(false)
            .describe("Include v2.4.0 multi-agent orchestration load order and ownership rules."),
        },
        async execute(args, context) {
          const status = resolveSkillRoot({
            directory: context.directory,
            worktree: context.worktree,
          });
          const skillRoot = status.missingRequiredPaths.length === 0 ? status.root : "<skill root not found>";
          const routerPath =
            status.missingRequiredPaths.length === 0
              ? toPosixPath(path.join(skillRoot, "skills", "00-engineering-calculation-router.skill.md"))
              : "<missing router>";
          const includeOrchestration = args.parallel || args.phase === "orchestration";

          const sections = [
            "# Engineering Calculation Route",
            "",
            formatSkillRootStatus(status),
            "",
            "## Load order",
            "",
            `1. ${toPosixPath(path.join(skillRoot, "SKILL.md"))}`,
            `2. ${routerPath}`,
            "3. The one parent orchestrator selected by the router.",
            "4. Only the child skill files needed for the current task.",
            ...(includeOrchestration
              ? ["5. For explicit multi-agent or parallel work, load the orchestration contract and templates."]
              : []),
            "",
            "## Phase guidance",
            "",
            phasePrompt(args.phase),
          ];

          if (includeOrchestration) {
            sections.push(
              "",
              "## Orchestration",
              "",
              orchestrationLoadOrder(toPosixPath(skillRoot)),
              "",
              orchestrationGuidance(),
            );
          }

          sections.push("", "## Gates", "", gateSummary());
          return sections.join("\n");
        },
      }),

      engineering_calc_orchestration: tool({
        description:
          "Generate read-only v2.4.0 orchestration drafts for parallel work plans, worker result packets, and merge reviews.",
        args: {
          artifact: tool.schema
            .enum(ORCHESTRATION_ARTIFACTS)
            .default("parallel_work_plan")
            .describe("Draft artifact to render."),
          phase: tool.schema
            .enum(ORCHESTRATION_PHASES)
            .default("implementation")
            .describe("Lifecycle phase for the orchestration draft."),
          objective: tool.schema.string().optional().describe("Bounded objective for the work item."),
          taskId: tool.schema.string().optional().describe("Task identifier such as TASK-001."),
          role: tool.schema.string().optional().describe("Worker role such as module-worker."),
          readOnlyInputs: arrayArg("Read-only input paths assigned to the worker."),
          ownedPaths: arrayArg("Disjoint paths owned by the worker."),
          expectedArtifacts: arrayArg("Expected artifacts or outputs from the worker."),
          validationCommands: arrayArg("Validation commands the worker or supervisor should run."),
        },
        async execute(args) {
          return [
            "# Engineering Calculation Orchestration Draft",
            "",
            "This tool is read-only. It returns draft text only and never writes files.",
            "",
            "## Draft",
            "",
            renderOrchestrationDraft(args),
            "",
            "## Safety Notes",
            "",
            supervisorOnlyDecisions(),
            "",
            workerOwnershipRules(),
            "",
            "Write the draft intentionally through normal OpenCode file-edit permissions only after review.",
          ].join("\n");
        },
      }),

      engineering_calc_doctor: tool({
        description:
          "Inspect the Engineering Calculation System skill pack installation and optionally run artifact validation.",
        args: {
          profile: tool.schema
            .enum(["core", "adapters-light", "qoder-addon", "singlefile"])
            .default("core")
            .describe("Validation profile to pass to scripts/validate_artifacts.py."),
          validate: tool.schema
            .boolean()
            .default(true)
            .describe("Run validate_artifacts.py when the skill root is complete."),
        },
        async execute(args, context) {
          const status = resolveSkillRoot({
            directory: context.directory,
            worktree: context.worktree,
          });
          const sections = ["# Engineering Calculation Doctor", "", formatSkillRootStatus(status)];

          if (status.missingRequiredPaths.length > 0) {
            sections.push(
              "",
              "Validation skipped because the skill root is incomplete.",
              "Set ENGINEERING_CALC_SKILL_ROOT or run scripts/install-project.mjs with --skill-root.",
            );
            return sections.join("\n");
          }

          if (!args.validate) {
            sections.push("", "Validation skipped by request.");
            return sections.join("\n");
          }

          const result = await runPython(
            ["scripts/validate_artifacts.py", "--package-root", ".", "--profile", args.profile],
            { cwd: status.root },
          );

          sections.push(
            "",
            "## Validation",
            "",
            `Command: ${result.command} ${result.args.join(" ")}`,
            `Exit code: ${result.exitCode}`,
          );
          if (result.stdout.trim()) {
            sections.push("", "stdout:", "```text", result.stdout.trim(), "```");
          }
          if (result.stderr.trim()) {
            sections.push("", "stderr:", "```text", result.stderr.trim(), "```");
          }

          return sections.join("\n");
        },
      }),
    },
  };
};

export default EngineeringCalculationSystemPlugin;
