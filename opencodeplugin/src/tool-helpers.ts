export { minimalConfigExample } from "./config/loader.js";

export function gateSummary(): string {
  return [
    "Gate policy: OpenCode-native permissions plus advisory engineering diagnostics",
    "Behavior discipline:",
    "- Read shared/execution-discipline.md for route card, gate card, artifact contract, and validation evidence.",
    "- Read shared/completion-evidence.md before source-backed, production, verified, web-complete, deployable, or bug-fixed claims.",
    "- Read shared/systematic-debugging.md before bug fixes and repair the lowest correct layer.",
    "Core workflow rules:",
    "- Do not invent engineering formulas, lookup rules, units, coefficients, branch logic, or pass/fail criteria.",
    "- Do not start production implementation unless implementation_handoff.yaml and coding_go_no_go.md allow it.",
    "- Keep formulas out of UI, report templates, frontend JavaScript, notebooks, batch scripts, and input files.",
    "- Route official calculations through run_book(BookInput) -> BookResult.",
    "- Run scripts/validate_artifacts.py before calling the package or generated project complete.",
    "Runtime tool blocking is experimental and disabled unless gates.runtimeHook is true.",
  ].join("\n");
}
