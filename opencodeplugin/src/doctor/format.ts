import type { DoctorResult } from "./types.js";

function statusIcon(status: string): string {
  switch (status) {
    case "pass":
      return "PASS";
    case "warn":
      return "WARN";
    case "skip":
      return "SKIP";
    default:
      return "FAIL";
  }
}

export function formatDoctor(result: DoctorResult, mode: "default" | "verbose" | "json" = "default"): string {
  if (mode === "json") return JSON.stringify(result, null, 2);

  const lines = [
    "# Engineering Calc OpenCode Doctor",
    "",
    `Target: ${result.target}`,
    `Config: ${result.configPath ?? "none"}`,
    `Skill root: ${result.skillRoot.root}`,
    `Schema: ${result.skillRoot.schemaVersion ?? "unknown"}`,
    "",
    "## Checks",
  ];

  for (const check of result.results) {
    lines.push(`- ${statusIcon(check.status)} ${check.name}: ${check.message}`);
    if (mode === "verbose" && check.details?.length) {
      for (const detail of check.details) lines.push(`  - ${detail}`);
    }
  }

  lines.push(
    "",
    "## Summary",
    "",
    `${result.summary.passed} passed, ${result.summary.warnings} warnings, ${result.summary.failed} failed, ${result.summary.skipped} skipped in ${result.summary.durationMs}ms`,
  );
  return lines.join("\n");
}

