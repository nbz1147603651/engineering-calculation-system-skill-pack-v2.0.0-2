#!/usr/bin/env node
import { Command } from "commander";
import { existsSync } from "node:fs";
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { fullConfigExample, loadConfig, minimalConfigExample } from "../config/loader.js";
import { createConfigJsonSchema } from "../config/json-schema.js";
import { formatDoctor } from "../doctor/format.js";
import { runDoctor } from "../doctor/runner.js";
import { installAssets, inspectAssets, uninstallAssets } from "../installer/asset-manager.js";
import {
  MCP_CATALOG,
  MCP_MODES,
  buildMcpConfig,
  mcpForProfile,
  parseMcpMode,
  type McpMode,
} from "../mcp-presets.js";
import { readPluginMeta } from "../plugin-meta.js";
import {
  PROFILE_NAMES,
  type OpenCodeProfile,
  listOpenCodeProfiles,
  parseOpenCodeProfile,
  type OpenCodeProfileName,
} from "../profiles.js";
import { getStatus } from "../status.js";

const packageRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..", "..");

function resolveTarget(value: string | undefined): string {
  return path.resolve(value ?? process.cwd());
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return Boolean(value) && typeof value === "object" && !Array.isArray(value);
}

function mergeDefaults(recommended: unknown, existing: unknown): unknown {
  if (isRecord(recommended) && isRecord(existing)) {
    const merged: Record<string, unknown> = { ...recommended };
    for (const [key, value] of Object.entries(existing)) {
      merged[key] = mergeDefaults(merged[key], value);
    }
    return merged;
  }
  return existing === undefined ? recommended : existing;
}

function pluginEntryForMode(mode: string, packageName: string): string {
  return mode === "npm" ? packageName : "./.opencode/plugins/engineering-calc-system.ts";
}

function parseRegistrationMode(value: string): "local" | "npm" {
  if (value === "local" || value === "npm") return value;
  throw new Error(`Invalid registration mode "${value}". Expected one of: local, npm`);
}

function recommendedOpenCodeConfig(args: {
  pluginEntry: string;
  profile: OpenCodeProfileName;
  mcpMode: McpMode;
}): Record<string, unknown> {
  const config: Record<string, unknown> = {
    $schema: "https://opencode.ai/config.json",
    plugin: [args.pluginEntry],
    permission: {
      edit: {
        "*": "ask",
        "plugins/engineering-calculation-system/*": "deny",
        "engineering-calculation-system/core/*": "deny",
      },
      bash: "ask",
      external_directory: "ask",
      task: "ask",
      skill: {
        "engineering-calc-system": "allow",
      },
    },
  };

  const mcp = buildMcpConfig({ profile: args.profile, mode: args.mcpMode });
  if (mcp) config.mcp = mcp;

  return config;
}

function mergeOpenCodeConfig(existing: Record<string, unknown>, recommended: Record<string, unknown>): Record<string, unknown> {
  const merged = mergeDefaults(recommended, existing) as Record<string, unknown>;
  const existingPlugins = Array.isArray(existing.plugin) ? existing.plugin : [];
  const recommendedPlugins = Array.isArray(recommended.plugin) ? recommended.plugin : [];
  merged.plugin = Array.from(new Set([...existingPlugins, ...recommendedPlugins]));
  return merged;
}

function profileOutput(): Array<OpenCodeProfile & { recommendedMcp: string[] }> {
  return listOpenCodeProfiles().map((profile) => ({
    ...profile,
    recommendedMcp: mcpForProfile(profile.name),
  }));
}

function formatProfiles(): string {
  const profileLines = profileOutput().flatMap((profile) => {
    const recommendedMcp = profile.recommendedMcp;
    return [
      `- ${profile.name}: ${profile.description}`,
      `  recommended MCP: ${recommendedMcp.length > 0 ? recommendedMcp.join(", ") : "none"}`,
    ];
  });

  const catalogLines = Object.entries(MCP_CATALOG).map(
    ([name, entry]) => `- ${name}: ${entry.purpose} Risk: ${entry.risk}`,
  );

  return [
    "OpenCode profile presets",
    "",
    ...profileLines,
    "",
    "MCP catalog",
    "",
    ...catalogLines,
  ].join("\n");
}

async function main() {
  const program = new Command();
  const meta = readPluginMeta();
  program
    .name("engineering-calc-opencode")
    .description("Engineering Calculation System OpenCode plugin CLI")
    .version(meta.version);

  program
    .command("install")
    .description("Install project-local OpenCode plugin assets")
    .option("--target <project>", "Project root", process.cwd())
    .option("--skill-root <path>", "Skill pack root")
    .option("--force", "Overwrite unmanaged files after backing them up", false)
    .option("--dry-run", "Show what would be installed without writing files", false)
    .action(async (options) => {
      const target = resolveTarget(options.target);
      const loaded = loadConfig(target, { skillRoot: options.skillRoot });
      const report = await installAssets({
        target,
        skillRoot: options.skillRoot,
        config: loaded.config,
        force: Boolean(options.force),
        dryRun: Boolean(options.dryRun),
      });
      console.log(JSON.stringify(report, null, 2));
    });

  program
    .command("update")
    .description("Update project-local managed OpenCode plugin assets")
    .option("--target <project>", "Project root", process.cwd())
    .option("--skill-root <path>", "Skill pack root")
    .option("--dry-run", "Show what would be updated without writing files", false)
    .action(async (options) => {
      const target = resolveTarget(options.target);
      const loaded = loadConfig(target, { skillRoot: options.skillRoot });
      const report = await installAssets({
        target,
        skillRoot: options.skillRoot,
        config: loaded.config,
        force: true,
        dryRun: Boolean(options.dryRun),
      });
      console.log(JSON.stringify(report, null, 2));
    });

  program
    .command("uninstall")
    .description("Remove only managed OpenCode plugin assets")
    .option("--target <project>", "Project root", process.cwd())
    .action(async (options) => {
      console.log(JSON.stringify(await uninstallAssets(resolveTarget(options.target)), null, 2));
    });

  program
    .command("doctor")
    .description("Run plugin and skill-pack diagnostics")
    .option("--target <project>", "Project root", process.cwd())
    .option("--skill-root <path>", "Skill pack root")
    .option("--json", "JSON output", false)
    .option("--verbose", "Verbose output", false)
    .option("--no-validation", "Skip Python validation checks")
    .action(async (options) => {
      const result = await runDoctor({
        target: resolveTarget(options.target),
        overrides: { skillRoot: options.skillRoot },
        includeValidation: Boolean(options.validation),
      });
      console.log(formatDoctor(result, options.json ? "json" : options.verbose ? "verbose" : "default"));
      process.exitCode = result.exitCode;
    });

  program
    .command("status")
    .description("Show resolved config, skill root, and asset status")
    .option("--target <project>", "Project root", process.cwd())
    .option("--skill-root <path>", "Skill pack root")
    .action(async (options) => {
      console.log(JSON.stringify(await getStatus({
        target: resolveTarget(options.target),
        overrides: { skillRoot: options.skillRoot },
      }), null, 2));
    });

  program
    .command("schema")
    .description("Print or write the JSON schema")
    .option("--write", "Write assets/engineering-calc-system.schema.json", false)
    .action(async (options) => {
      const schema = createConfigJsonSchema();
      if (options.write) {
        const outputPath = path.join(packageRoot, "assets", "engineering-calc-system.schema.json");
        await fs.mkdir(path.dirname(outputPath), { recursive: true });
        await fs.writeFile(outputPath, `${JSON.stringify(schema, null, 2)}\n`, "utf8");
        console.log(outputPath);
        return;
      }
      console.log(JSON.stringify(schema, null, 2));
    });

  program
    .command("config-example")
    .description("Print a minimal or full JSON config example")
    .option("--full", "Print full example", false)
    .action((options) => {
      console.log(options.full ? fullConfigExample() : minimalConfigExample());
    });

  program
    .command("assets")
    .description("Inspect managed project asset status")
    .option("--target <project>", "Project root", process.cwd())
    .action(async (options) => {
      console.log(JSON.stringify(await inspectAssets(resolveTarget(options.target)), null, 2));
    });

  program
    .command("profiles")
    .description("List OpenCode profile presets and their recommended MCPs")
    .option("--json", "JSON output", false)
    .action((options) => {
      const output = {
        profiles: profileOutput(),
        mcpCatalog: MCP_CATALOG,
      };
      console.log(options.json ? JSON.stringify(output, null, 2) : formatProfiles());
    });

  program
    .command("opencode-json")
    .description("Print or merge a recommended opencode.json registration and permission snippet")
    .option("--target <project>", "Project root", process.cwd())
    .option("--mode <mode>", "Registration mode: local (project-local shim) or npm (package name)", "local")
    .option("--profile <name>", `Profile preset: ${PROFILE_NAMES.join(", ")}`, "conservative")
    .option("--mcp <mode>", `MCP output mode: ${MCP_MODES.join(", ")}`, "none")
    .option("--write", "Merge the plugin entry into the project's opencode.json", false)
    .option("--package-name <name>", "Override the npm package name", "engineering-calculation-system-opencode-plugin")
    .option("--include-mcp", "Compatibility alias for --mcp catalog", false)
    .action(async (options) => {
      const target = resolveTarget(options.target);
      let mode: "local" | "npm";
      let profile: OpenCodeProfileName;
      let mcpMode: McpMode;
      try {
        mode = parseRegistrationMode(String(options.mode));
        profile = parseOpenCodeProfile(String(options.profile));
        mcpMode = Boolean(options.includeMcp) ? "catalog" : parseMcpMode(String(options.mcp));
      } catch (error) {
        console.error(error instanceof Error ? error.message : String(error));
        process.exitCode = 1;
        return;
      }
      const pluginEntry = pluginEntryForMode(mode, options.packageName);
      const recommended = recommendedOpenCodeConfig({ pluginEntry, profile, mcpMode });

      const configPath = path.join(target, "opencode.json");
      let config: Record<string, unknown> = {};
      let existed = false;
      if (existsSync(configPath)) {
        existed = true;
        try {
          config = JSON.parse(await fs.readFile(configPath, "utf8")) as Record<string, unknown>;
        } catch (error) {
          console.error(
            `Failed to parse existing opencode.json: ${error instanceof Error ? error.message : String(error)}`,
          );
          process.exitCode = 1;
          return;
        }
      }

      const merged = mergeOpenCodeConfig(config, recommended);

      if (options.write) {
        await fs.writeFile(configPath, `${JSON.stringify(merged, null, 2)}\n`, "utf8");
        console.log(
          `${existed ? "Merged into" : "Wrote"} ${configPath} (plugin: ${pluginEntry}, profile: ${profile}, mcp: ${mcpMode})`,
        );
        return;
      }

      console.log(
        `Add or merge the following OpenCode-native config into opencode.json (${mode} mode, profile: ${profile}, mcp: ${mcpMode}):\n\n` +
          JSON.stringify(recommended, null, 2) +
          `\n\nRun with --write to merge into the project's opencode.json.`,
      );
    });

  await program.parseAsync(process.argv);
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : String(error));
  process.exit(1);
});
