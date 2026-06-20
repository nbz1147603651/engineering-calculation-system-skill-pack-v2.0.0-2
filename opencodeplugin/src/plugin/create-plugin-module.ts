import type { Hooks, Plugin, PluginModule } from "@opencode-ai/plugin";
import { loadConfig } from "../config/loader.js";
import { createHooks } from "../create-hooks.js";
import { createTools } from "../create-tools.js";
import { runDoctor } from "../doctor/runner.js";
import { loadGateState } from "../gates.js";
import { resolveSkillRoot } from "../paths.js";

export function createPluginModule(): PluginModule {
  const server: Plugin = async (ctx): Promise<Hooks> => {
    const loaded = loadConfig(ctx.directory);
    const rootStatus = resolveSkillRoot({
      directory: ctx.directory,
      worktree: ctx.worktree,
      configuredSkillRoot: loaded.config.skillRoot,
    });

    const log = (level: "info" | "warn" | "error", message: string, extra?: Record<string, unknown>) => {
      void ctx.client.app
        .log({
          body: {
            service: "engineering-calculation-system-opencode-plugin",
            level,
            message,
            extra,
          },
        })
        .catch(() => undefined);
    };

    await log(
      rootStatus.missingRequiredPaths.length === 0 ? "info" : "warn",
      "Plugin initialized",
      {
        configPath: loaded.path,
        configMessages: loaded.messages,
        skillRoot: rootStatus.root,
        source: rootStatus.source,
        schemaVersion: rootStatus.schemaVersion,
        missingRequiredPaths: rootStatus.missingRequiredPaths,
        gateDiagnostics: loaded.config.gates.enforcement,
        runtimeGateHook: loaded.config.gates.runtimeHook,
      },
    );

    if (loaded.config.doctor.validateOnStartup) {
      runDoctor({
        target: ctx.directory,
        overrides: { skillRoot: loaded.config.skillRoot },
        includeValidation: true,
      })
        .then((doctor) => {
          log(
            doctor.exitCode === 0 ? "info" : "warn",
            "Startup doctor completed",
            { ...doctor.summary },
          );
        })
        .catch(() => undefined);
    }

    return {
      ...createHooks({
        config: loaded.config,
        rootStatus,
        target: ctx.directory,
        worktree: ctx.worktree,
        log,
      }),
      tool: createTools({
        config: loaded.config,
        rootStatus: loadGateState({
          target: ctx.directory,
          worktree: ctx.worktree,
          config: loaded.config,
          rootStatus,
        }),
      }),
    };
  };

  return {
    id: "engineering-calculation-system",
    server,
  };
}
