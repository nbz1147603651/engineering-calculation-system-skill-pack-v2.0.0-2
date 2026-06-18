import { tool } from "@opencode-ai/plugin";
import type { Hooks } from "@opencode-ai/plugin";
import path from "node:path";
import {
  gateSummary,
  minimalConfigExample,
} from "./tool-helpers.js";
import {
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
import { fullConfigExample } from "./config/loader.js";
import { formatDoctor } from "./doctor/format.js";
import { runDoctor } from "./doctor/runner.js";
import { getStatus } from "./status.js";
import { resolveSkillRoot, TARGET_SCHEMA_VERSION, toPosixPath } from "./paths.js";
import type { EngineeringCalcConfig } from "./config/schema.js";

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

export function createTools(args: { config: EngineeringCalcConfig }): NonNullable<Hooks["tool"]> {
  return {
    engineering_calc_route: tool({
      description:
        "Return the Engineering Calculation System OpenCode routing prompt, load order, and phase-specific gates.",
      args: {
        phase: tool.schema
          .enum(PHASES)
          .default(args.config.defaultPhase)
          .describe("Workflow phase to route. Use router when unsure."),
        parallel: tool.schema
          .boolean()
          .default(false)
          .describe("Include v2.4.0 multi-agent orchestration load order and ownership rules."),
      },
      async execute(routeArgs, context) {
        const status = resolveSkillRoot({
          directory: context.directory,
          worktree: context.worktree,
          configuredSkillRoot: args.config.skillRoot,
        });
        const skillRoot = status.missingRequiredPaths.length === 0 ? status.root : "<skill root not found>";
        const routerPath =
          status.missingRequiredPaths.length === 0
            ? toPosixPath(path.join(skillRoot, "skills", "00-engineering-calculation-router.skill.md"))
            : "<missing router>";
        const includeOrchestration =
          args.config.orchestration.enabled && (routeArgs.parallel || routeArgs.phase === "orchestration");

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
          phasePrompt(routeArgs.phase),
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

        sections.push("", "## Gates", "", gateSummary(args.config.strictGateMode));
        return sections.join("\n");
      },
    }),

    engineering_calc_orchestration: tool({
      description:
        "Generate read-only v2.4.0 orchestration drafts for parallel work plans, worker result packets, and merge reviews.",
      args: {
        artifact: tool.schema.enum(ORCHESTRATION_ARTIFACTS).default("parallel_work_plan").describe("Draft artifact to render."),
        phase: tool.schema.enum(ORCHESTRATION_PHASES).default("implementation").describe("Lifecycle phase for the orchestration draft."),
        objective: tool.schema.string().optional().describe("Bounded objective for the work item."),
        taskId: tool.schema.string().optional().describe("Task identifier such as TASK-001."),
        role: tool.schema.string().optional().describe("Worker role such as module-worker."),
        readOnlyInputs: arrayArg("Read-only input paths assigned to the worker."),
        ownedPaths: arrayArg("Disjoint paths owned by the worker."),
        expectedArtifacts: arrayArg("Expected artifacts or outputs from the worker."),
        validationCommands: arrayArg("Validation commands the worker or supervisor should run."),
      },
      async execute(orchestrationArgs) {
        return [
          "# Engineering Calculation Orchestration Draft",
          "",
          "This tool is read-only. It returns draft text only and never writes files.",
          "",
          "## Draft",
          "",
          renderOrchestrationDraft(orchestrationArgs),
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
      description: "Run Engineering Calculation System OpenCode plugin doctor checks.",
      args: {
        mode: tool.schema.enum(["default", "verbose", "json"]).default("default").describe("Doctor output mode."),
        validate: tool.schema.boolean().default(true).describe("Run Python validation checks."),
      },
      async execute(doctorArgs, context) {
        const result = await runDoctor({
          target: context.directory,
          overrides: { skillRoot: args.config.skillRoot },
          includeValidation: doctorArgs.validate,
        });
        return formatDoctor(result, doctorArgs.mode);
      },
    }),

    engineering_calc_status: tool({
      description: "Return skill root, schema version, config path, and installed OpenCode asset status.",
      args: {},
      async execute(_statusArgs, context) {
        const status = await getStatus({
          target: context.directory,
          worktree: context.worktree,
          overrides: { skillRoot: args.config.skillRoot },
        });
        return JSON.stringify(status, null, 2);
      },
    }),

    engineering_calc_config_example: tool({
      description: "Return a minimal or full JSONC config example for the plugin.",
      args: {
        full: tool.schema.boolean().default(false).describe("Return the full config example."),
      },
      async execute(exampleArgs) {
        return `\`\`\`jsonc\n${exampleArgs.full ? fullConfigExample() : minimalConfigExample()}\n\`\`\``;
      },
    }),
  };
}
