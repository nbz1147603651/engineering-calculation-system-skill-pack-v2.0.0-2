export const PROFILE_NAMES = [
  "conservative",
  "reference-acquisition",
  "implementation",
  "verification",
  "web-complete",
  "release",
] as const;

export type OpenCodeProfileName = (typeof PROFILE_NAMES)[number];

export interface OpenCodeProfile {
  name: OpenCodeProfileName;
  label: string;
  description: string;
}

const PROFILE_DETAILS = {
  conservative: {
    label: "Conservative",
    description: "Minimal OpenCode registration with no optional MCP surface.",
  },
  "reference-acquisition": {
    label: "Reference acquisition",
    description: "Evidence-first source intake; MCPs stay disabled so source authority remains explicit.",
  },
  implementation: {
    label: "Implementation",
    description: "Software implementation support for current library docs and public code-pattern search.",
  },
  verification: {
    label: "Verification",
    description: "Validation and local UI/report smoke checks.",
  },
  "web-complete": {
    label: "Web complete",
    description: "End-to-end web implementation and browser verification support.",
  },
  release: {
    label: "Release",
    description: "Release review posture with secret-bearing services kept opt-in only.",
  },
} satisfies Record<OpenCodeProfileName, Omit<OpenCodeProfile, "name">>;

export function isOpenCodeProfileName(value: string): value is OpenCodeProfileName {
  return PROFILE_NAMES.includes(value as OpenCodeProfileName);
}

export function parseOpenCodeProfile(value: string): OpenCodeProfileName {
  if (isOpenCodeProfileName(value)) return value;
  throw new Error(`Invalid profile "${value}". Expected one of: ${PROFILE_NAMES.join(", ")}`);
}

export function listOpenCodeProfiles(): OpenCodeProfile[] {
  return PROFILE_NAMES.map((name) => ({
    name,
    ...PROFILE_DETAILS[name],
  }));
}
