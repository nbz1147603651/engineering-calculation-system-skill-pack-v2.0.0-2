#!/usr/bin/env node
import { Command } from "commander";
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { fullConfigExample, loadConfig, minimalConfigExample } from "../config/loader.js";
import { createConfigJsonSchema } from "../config/json-schema.js";
import { formatDoctor } from "../doctor/format.js";
import { runDoctor } from "../doctor/runner.js";
import { installAssets, inspectAssets, uninstallAssets } from "../installer/asset-manager.js";
import { getStatus } from "../status.js";

const packageRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..", "..");

function resolveTarget(value: string | undefined): string {
  return path.resolve(value ?? process.cwd());
}

async function main() {
  const program = new Command();
  program
    .name("engineering-calc-opencode")
    .description("Engineering Calculation System OpenCode plugin CLI")
    .version("0.3.0");

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
    .description("Print a minimal or full JSONC config example")
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

  await program.parseAsync(process.argv);
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : String(error));
  process.exit(1);
});

