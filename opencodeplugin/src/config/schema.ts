import { z } from "zod";
import { PHASES } from "../domain.js";

export const ConfigPhaseSchema = z.enum(PHASES);

export const RoleOverrideSchema = z.object({
  description: z.string().optional(),
  promptAppend: z.string().optional(),
  disabled: z.boolean().optional(),
});

export const EngineeringCalcConfigSchema = z.object({
  $schema: z.string().optional(),
  skillRoot: z.string().optional(),
  strictGateMode: z.boolean().default(true),
  defaultPhase: ConfigPhaseSchema.default("router"),
  doctor: z
    .object({
      validateOnStartup: z.boolean().default(false),
      timeoutMs: z.number().int().positive().default(30_000),
    })
    .default({ validateOnStartup: false, timeoutMs: 30_000 }),
  orchestration: z
    .object({
      enabled: z.boolean().default(true),
      readOnlyDrafts: z.boolean().default(true),
    })
    .default({ enabled: true, readOnlyDrafts: true }),
  agents: z
    .object({
      disabled: z.array(z.string()).default([]),
      roleOverrides: z.record(z.string(), RoleOverrideSchema).default({}),
    })
    .default({ disabled: [], roleOverrides: {} }),
  agentOrder: z.array(z.string().max(128)).max(64).default([]),
  commands: z
    .object({
      disabled: z.array(z.string()).default([]),
    })
    .default({ disabled: [] }),
  mcpPresets: z
    .object({
      enabled: z.boolean().default(false),
      allowed: z.array(z.string()).default([]),
    })
    .default({ enabled: false, allowed: [] }),
});

export type EngineeringCalcConfig = z.infer<typeof EngineeringCalcConfigSchema>;
export type PartialEngineeringCalcConfig = Partial<EngineeringCalcConfig>;

export const DEFAULT_CONFIG = EngineeringCalcConfigSchema.parse({});

export const USER_ONLY_CONFIG_KEYS = new Set(["mcpPresets"]);
