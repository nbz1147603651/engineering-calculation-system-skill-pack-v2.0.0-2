export { minimalConfigExample } from "./config/loader.js";

export function gateSummary(strictGateMode = true): string {
  return [
    `Gate policy: ${strictGateMode ? "strict" : "advisory"}`,
    "Hard gates:",
    "- Do not invent engineering formulas, lookup rules, units, coefficients, branch logic, or pass/fail criteria.",
    "- Do not start production implementation unless implementation_handoff.yaml and coding_go_no_go.md allow it.",
    "- Keep formulas out of UI, report templates, frontend JavaScript, notebooks, batch scripts, and input files.",
    "- Route official calculations through run_book(BookInput) -> BookResult.",
    "- Run scripts/validate_artifacts.py before calling the package or generated project complete.",
  ].join("\n");
}

