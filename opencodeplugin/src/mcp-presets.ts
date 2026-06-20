import type { OpenCodeProfileName } from "./profiles.js";

export const MCP_NAMES = ["context7", "gh_grep", "playwright", "sentry"] as const;
export type McpName = (typeof MCP_NAMES)[number];

export const MCP_MODES = ["none", "catalog", "recommended"] as const;
export type McpMode = (typeof MCP_MODES)[number];

export interface McpCatalogEntry {
  name: McpName;
  purpose: string;
  risk: string;
  config: Record<string, unknown>;
}

export const MCP_CATALOG = {
  context7: {
    name: "context7",
    purpose: "Current library and API documentation lookup for implementation work.",
    risk: "Documentation accelerator only; not an authority for engineering formulas, standards, or source contracts.",
    config: {
      type: "remote",
      url: "https://mcp.context7.com/mcp",
    },
  },
  gh_grep: {
    name: "gh_grep",
    purpose: "Public GitHub code-pattern search for implementation references.",
    risk: "Do not copy unreviewed code and do not treat examples as engineering formula evidence.",
    config: {
      type: "remote",
      url: "https://mcp.grep.app",
    },
  },
  playwright: {
    name: "playwright",
    purpose: "Local Web UI smoke tests, report previews, and interaction verification.",
    risk: "Local browser automation; enable only for verification-oriented profiles.",
    config: {
      type: "local",
      command: ["npx", "@playwright/mcp@latest"],
    },
  },
  sentry: {
    name: "sentry",
    purpose: "Deployed-system error diagnostics and release/ops checks.",
    risk: "OAuth and project data access; catalog example only and never auto-enabled by a profile.",
    config: {
      type: "remote",
      url: "https://mcp.sentry.dev/mcp",
      oauth: {},
    },
  },
} satisfies Record<McpName, McpCatalogEntry>;

export const PROFILE_RECOMMENDED_MCP = {
  conservative: [],
  "reference-acquisition": [],
  implementation: ["context7", "gh_grep"],
  verification: ["playwright"],
  "web-complete": ["context7", "playwright"],
  release: [],
} satisfies Record<OpenCodeProfileName, readonly McpName[]>;

export function parseMcpMode(value: string): McpMode {
  if (MCP_MODES.includes(value as McpMode)) return value as McpMode;
  throw new Error(`Invalid MCP mode "${value}". Expected one of: ${MCP_MODES.join(", ")}`);
}

export function mcpForProfile(profile: OpenCodeProfileName): McpName[] {
  return [...PROFILE_RECOMMENDED_MCP[profile]];
}

function cloneJsonRecord(value: Record<string, unknown>): Record<string, unknown> {
  return JSON.parse(JSON.stringify(value)) as Record<string, unknown>;
}

function serverConfig(name: McpName, enabled: boolean): Record<string, unknown> {
  return {
    ...cloneJsonRecord(MCP_CATALOG[name].config),
    enabled,
  };
}

export function buildMcpConfig(args: {
  profile: OpenCodeProfileName;
  mode: McpMode;
}): Record<string, unknown> | undefined {
  if (args.mode === "none") return undefined;

  const names = args.mode === "catalog" ? [...MCP_NAMES] : mcpForProfile(args.profile);
  if (names.length === 0) return undefined;

  const enabled = args.mode === "recommended";
  return Object.fromEntries(names.map((name) => [name, serverConfig(name, enabled)]));
}
