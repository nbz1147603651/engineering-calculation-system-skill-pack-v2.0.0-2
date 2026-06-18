import { DEFAULT_CONFIG, EngineeringCalcConfigSchema, type EngineeringCalcConfig } from "./schema.js";

function mergeRecord(base: Record<string, unknown>, override: Record<string, unknown>): Record<string, unknown> {
  const next: Record<string, unknown> = { ...base };
  for (const [key, value] of Object.entries(override)) {
    if (
      value &&
      typeof value === "object" &&
      !Array.isArray(value) &&
      base[key] &&
      typeof base[key] === "object" &&
      !Array.isArray(base[key])
    ) {
      next[key] = mergeRecord(base[key] as Record<string, unknown>, value as Record<string, unknown>);
      continue;
    }
    next[key] = value;
  }
  return next;
}

export function mergeConfigLayers(layers: Array<Partial<EngineeringCalcConfig>>): EngineeringCalcConfig {
  let merged = DEFAULT_CONFIG as unknown as Record<string, unknown>;
  for (const layer of layers) {
    merged = mergeRecord(merged, layer as Record<string, unknown>);
  }
  return EngineeringCalcConfigSchema.parse(merged);
}

