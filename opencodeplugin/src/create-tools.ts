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

const STRICT_JSON_ARGUMENTS_NOTE =
  "Tool-call compatibility: arguments must be one strict JSON object with double-quoted keys and strings. Use {} for defaults; omit optional fields instead of undefined. Do not use key=value, single quotes, comments, trailing commas, or Markdown.";

function toolDescription(summary: string, exampleArgs: string): string {
  return `${summary} ${STRICT_JSON_ARGUMENTS_NOTE} Example arguments: ${exampleArgs}.`;
}

function argDescription(description: string, jsonShape: string): string {
  return `${description} JSON shape: ${jsonShape}.`;
}

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
  return tool.schema.array(tool.schema.string()).default([]).describe(argDescription(description, "[\"path/or/command\"] or []"));
}

export function createTools(args: { config: EngineeringCalcConfig }): NonNullable<Hooks["tool"]> {
  return {
    engineering_calc_route: tool({
      description: toolDescription(
        "Return the Engineering Calculation System OpenCode routing prompt, load order, and phase-specific gates.",
        "{\"phase\":\"router\",\"parallel\":false}",
      ),
      args: {
        phase: tool.schema
          .enum(PHASES)
          .default(args.config.defaultPhase)
          .describe(argDescription("Workflow phase to route. Use router when unsure.", "\"router\"")),
        parallel: tool.schema
          .boolean()
          .default(false)
          .describe(argDescription(`Include v${TARGET_SCHEMA_VERSION} multi-agent orchestration load order and ownership rules.`, "true or false")),
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
      description: toolDescription(
        `Generate read-only v${TARGET_SCHEMA_VERSION} orchestration drafts for parallel work plans, worker result packets, and merge reviews.`,
        "{\"artifact\":\"parallel_work_plan\",\"phase\":\"implementation\",\"ownedPaths\":[\"src/pkg/libraries/example/\"]}",
      ),
      args: {
        artifact: tool.schema
          .enum(ORCHESTRATION_ARTIFACTS)
          .default("parallel_work_plan")
          .describe(argDescription("Draft artifact to render.", "\"parallel_work_plan\"")),
        phase: tool.schema
          .enum(ORCHESTRATION_PHASES)
          .default("implementation")
          .describe(argDescription("Lifecycle phase for the orchestration draft.", "\"implementation\"")),
        objective: tool.schema.string().optional().describe(argDescription("Bounded objective for the work item.", "\"bounded module\"")),
        taskId: tool.schema.string().optional().describe(argDescription("Task identifier such as TASK-001.", "\"TASK-001\"")),
        role: tool.schema.string().optional().describe(argDescription("Worker role such as module-worker.", "\"module-worker\"")),
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
      description: toolDescription(
        "Run Engineering Calculation System OpenCode plugin doctor checks.",
        "{\"mode\":\"verbose\",\"validate\":true}",
      ),
      args: {
        mode: tool.schema
          .enum(["default", "verbose", "json"])
          .default("default")
          .describe(argDescription("Doctor output mode.", "\"default\", \"verbose\", or \"json\"")),
        validate: tool.schema.boolean().default(true).describe(argDescription("Run Python validation checks.", "true or false")),
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
      description: toolDescription(
        "Return skill root, schema version, config path, and installed OpenCode asset status.",
        "{}",
      ),
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
      description: toolDescription(
        "Return a minimal or full JSONC config example for the plugin.",
        "{\"full\":false}",
      ),
      args: {
        full: tool.schema.boolean().default(false).describe(argDescription("Return the full config example.", "true or false")),
      },
      async execute(exampleArgs) {
        return `\`\`\`jsonc\n${exampleArgs.full ? fullConfigExample() : minimalConfigExample()}\n\`\`\``;
      },
    }),
  };
}
