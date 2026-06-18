import type { Hooks, Plugin, PluginModule } from "@opencode-ai/plugin";
import { loadConfig } from "../config/loader.js";
import { createHooks } from "../create-hooks.js";
import { createTools } from "../create-tools.js";
import { runDoctor } from "../doctor/runner.js";
import { resolveSkillRoot } from "../paths.js";

export function createPluginModule(): PluginModule {
  const server: Plugin = async (ctx): Promise<Hooks> => {
    const loaded = loadConfig(ctx.directory);
    const rootStatus = resolveSkillRoot({
      directory: ctx.directory,
      worktree: ctx.worktree,
      configuredSkillRoot: loaded.config.skillRoot,
    });

    await ctx.client.app
      .log({
        body: {
          service: "engineering-calculation-system-opencode-plugin",
          level: rootStatus.missingRequiredPaths.length === 0 ? "info" : "warn",
          message: "Plugin initialized",
          extra: {
            configPath: loaded.path,
            configMessages: loaded.messages,
            skillRoot: rootStatus.root,
            source: rootStatus.source,
            schemaVersion: rootStatus.schemaVersion,
            missingRequiredPaths: rootStatus.missingRequiredPaths,
          },
        },
      })
      .catch(() => undefined);

    if (loaded.config.doctor.validateOnStartup) {
      runDoctor({ target: ctx.directory, includeValidation: true })
        .then((doctor) => {
          void ctx.client.app.log({
            body: {
              service: "engineering-calculation-system-opencode-plugin",
              level: doctor.exitCode === 0 ? "info" : "warn",
              message: "Startup doctor completed",
              extra: { ...doctor.summary },
            },
          });
        })
        .catch(() => undefined);
    }

    return {
      ...createHooks({ config: loaded.config, rootStatus }),
      tool: createTools({ config: loaded.config }),
    };
  };

  return {
    id: "engineering-calculation-system",
    server,
  };
}
