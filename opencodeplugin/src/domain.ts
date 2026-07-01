export const PHASES = [
  "router",
  "reference-acquisition",
  "logic-blueprint",
  "implementation-handoff",
  "implementation",
  "interfaces",
  "verification",
  "release",
  "orchestration",
] as const;

export type EngineeringCalcPhase = (typeof PHASES)[number];

export const ORCHESTRATION_PHASES = [
  "acquisition",
  "analysis",
  "implementation",
  "verification",
  "release",
] as const;

export type OrchestrationPhase = (typeof ORCHESTRATION_PHASES)[number];

export const ORCHESTRATION_ARTIFACTS = [
  "parallel_work_plan",
  "task_brief",
  "agent_result_packet",
  "task_review",
  "merge_review",
  "progress_ledger",
] as const;

export type OrchestrationArtifact = (typeof ORCHESTRATION_ARTIFACTS)[number];

export function phasePrompt(phase: EngineeringCalcPhase): string {
  switch (phase) {
    case "reference-acquisition":
      return [
        "Use the reference acquisition parent skill.",
        "Load parent/engineering-calculation-reference-acquisition.skill.md, then the child skills selected by the router.",
        "Record meaningful searches, accepted/rejected sources, access limits, and local persistence decisions.",
      ].join("\n");
    case "logic-blueprint":
      return [
        "Use the logic architecture parent skill.",
        "Resolve source authority before extracting formulas, lookup tables, branch logic, applicability limits, and conflicts.",
        "Emit the Calculation Logic Blueprint and related inventories before coding.",
      ].join("\n");
    case "implementation-handoff":
      return [
        "Generate or review handoff/implementation_handoff.yaml and handoff/coding_go_no_go.md.",
        "Treat unresolved source gaps, missing traceability, and blocked go/no-go state as coding blockers.",
      ].join("\n");
    case "implementation":
      return [
        "Use the calculation book parent skill and implementation child skills.",
        "Keep official formulas inside reusable calculation modules and route calculations through run_book(BookInput) -> BookResult.",
        "Keep UI, reports, batch scripts, and review apps as thin consumers of trusted results.",
      ].join("\n");
    case "interfaces":
      return [
        "Use Skill 12 and the 12a/12b/12c split for reports, frontend/review, and batch/package interfaces.",
        "Preserve warnings, limitations, traceability, import/export manifests, and report status semantics.",
      ].join("\n");
    case "verification":
      return [
        "Use Skill 13 for regression, branch, lookup, traceability, interface, package, and smoke verification.",
        "Do not mark the system complete until validation artifacts and tests support the claim.",
      ].join("\n");
    case "release":
      return [
        "Use Skill 14 for local runnable and Linux-cloud deployable release paths.",
        "Include environment configuration, health checks, deployment files, release checklist, and smoke evidence.",
      ].join("\n");
    case "orchestration":
      return orchestrationGuidance();
    case "router":
    default:
      return [
        "Start with SKILL.md, then skills/00-engineering-calculation-router.skill.md.",
        "For non-trivial tasks, load shared/execution-discipline.md and produce route/gate/artifact/validation cards.",
        "Let the router choose one parent orchestrator and only the child skills needed for the task.",
      ].join("\n");
  }
}

export function gateSummary(): string {
  return [
    "Hard gates:",
    "- Use shared/execution-discipline.md for route card, gate card, artifact contract, and validation evidence.",
    "- Use shared/completion-evidence.md before completion, production, deployable, web-complete, verified, or bug-fixed claims.",
    "- Use shared/systematic-debugging.md before bug fixes and repair the lowest correct layer.",
    "- Do not invent engineering formulas, lookup rules, units, coefficients, branch logic, or pass/fail criteria.",
    "- Do not start production implementation unless implementation_handoff.yaml and coding_go_no_go.md allow it.",
    "- Keep formulas out of UI, report templates, frontend JavaScript, notebooks, batch scripts, and input files.",
    "- Route official calculations through run_book(BookInput) -> BookResult.",
    "- Run scripts/validate_artifacts.py before calling the package or generated project complete.",
  ].join("\n");
}

export function orchestrationLoadOrder(skillRoot: string): string {
  return [
    "Orchestration load order:",
    `1. ${skillRoot}/shared/multi-agent-orchestration.md`,
    `2. ${skillRoot}/templates/orchestration/parallel_work_plan.yaml`,
    `3. ${skillRoot}/templates/orchestration/task_brief.md`,
    `4. ${skillRoot}/templates/orchestration/agent_result_packet.yaml`,
    `5. ${skillRoot}/templates/orchestration/task_review.md`,
    `6. ${skillRoot}/templates/orchestration/merge_review.md`,
    `7. ${skillRoot}/templates/orchestration/progress_ledger.md`,
  ].join("\n");
}

export function supervisorOnlyDecisions(): string {
  return [
    "Supervisor-only decisions:",
    "- lifecycle routing when material state is unclear",
    "- evidence gate status",
    "- source authority priority and conflict resolution",
    "- ID namespace allocation after downstream references exist",
    "- coding gate status",
    "- implementation_handoff.yaml and coding_go_no_go.md freeze",
    "- BookInput -> run_book() -> BookResult contract changes",
    "- final report, production, and release readiness labels",
  ].join("\n");
}

export function workerOwnershipRules(): string {
  return [
    "Worker ownership rules:",
    "- assign disjoint owned_paths before parallel work starts",
    "- workers write only inside owned_paths",
    "- shared registries, handoff files, root README files, release files, and public API contracts stay supervisor-owned unless explicitly assigned",
    "- workers return agent_result_packet.yaml fields",
    "- supervisor accepts output only after task_review.md and merge_review.md checks",
    "- long or compacted work resumes from .engineering-calc/work/progress.md",
  ].join("\n");
}

export function orchestrationGuidance(): string {
  return [
    "Use orchestration only when the user explicitly requests multiple agents, subagents, delegation, or parallel work.",
    "Create a parallel work plan and task brief before splitting work, give every worker read-only inputs and disjoint owned_paths, and merge through task review plus supervisor review.",
    supervisorOnlyDecisions(),
    workerOwnershipRules(),
  ].join("\n\n");
}

export function compactionOrchestrationContext(): string {
  return [
    "Preserve orchestration state when present:",
    "- active plan_id and phase",
    "- worker task IDs, roles, owned_paths, and read-only inputs",
    "- result packet status, changed paths, IDs touched, assumptions, open questions, and validation result",
    "- progress ledger route/gate/evidence state",
    "- merge conflicts, requested shared-file changes, supervisor actions, and merge decision",
    "- evidence/coding gate decisions, source authority decisions, ID allocation, public runner contract status, and final acceptance state",
  ].join("\n");
}

function yamlScalar(value: string | undefined, fallback: string): string {
  const text = value?.trim() || fallback;
  if (/^[A-Za-z0-9_.:/ -]+$/.test(text)) return text;
  return JSON.stringify(text);
}

function yamlList(values: string[] | undefined, fallback: string[] = []): string {
  const items = values && values.length > 0 ? values : fallback;
  if (items.length === 0) return "[]";
  return items.map((item) => `  - ${yamlScalar(item, "to_be_defined")}`).join("\n");
}

export interface OrchestrationDraftArgs {
  artifact: OrchestrationArtifact;
  phase: OrchestrationPhase;
  objective?: string;
  taskId?: string;
  role?: string;
  readOnlyInputs?: string[];
  ownedPaths?: string[];
  expectedArtifacts?: string[];
  validationCommands?: string[];
}

export function renderOrchestrationDraft(args: OrchestrationDraftArgs): string {
  switch (args.artifact) {
    case "task_brief":
      return renderTaskBrief(args);
    case "agent_result_packet":
      return renderAgentResultPacket(args);
    case "task_review":
      return renderTaskReview(args);
    case "merge_review":
      return renderMergeReview(args);
    case "progress_ledger":
      return renderProgressLedger(args);
    case "parallel_work_plan":
    default:
      return renderParallelWorkPlan(args);
  }
}

function renderParallelWorkPlan(args: OrchestrationDraftArgs): string {
  const createdAt = new Date().toISOString().slice(0, 10);
  const taskId = args.taskId?.trim() || "TASK-001";
  const role = args.role?.trim() || defaultWorkerRole(args.phase);
  const objective = args.objective?.trim() || "to_be_defined";

  return [
    "```yaml",
    "plan_id: PWP-001",
    "project_or_book: to_be_defined",
    `created_at: ${createdAt}`,
    "status: draft # draft | active | merging | complete | blocked",
    "supervisor:",
    "  owner: supervisor",
    "  responsibilities:",
    "    - route lifecycle phase",
    "    - assign disjoint owned paths",
    "    - preserve IDs and public contracts",
    "    - merge worker outputs",
    "    - run validation",
    `phase: ${args.phase}`,
    "gate_context:",
    "  evidence_gate: to_be_defined",
    "  coding_gate: to_be_defined",
    "  handoff_status: to_be_defined",
    "work_directory: .engineering-calc/work/",
    "progress_ledger: .engineering-calc/work/progress.md",
    "read_only_inputs:",
    yamlList(args.readOnlyInputs, defaultReadOnlyInputs(args.phase)),
    "shared_outputs:",
    "  - templates/orchestration/merge_review.md",
    "agent_roles:",
    "  - role: supervisor",
    "    may_delegate: true",
    "    owns_gate_decisions: true",
    `  - role: ${yamlScalar(role, "worker")}`,
    "    may_delegate: false",
    "    owns_gate_decisions: false",
    "tasks:",
    `  - task_id: ${yamlScalar(taskId, "TASK-001")}`,
    `    role: ${yamlScalar(role, "worker")}`,
    `    task_brief: .engineering-calc/work/task-${yamlScalar(taskId, "TASK-001")}-brief.md`,
    `    objective: ${yamlScalar(objective, "to_be_defined")}`,
    "    read_only_inputs:",
    indentList(args.readOnlyInputs, defaultReadOnlyInputs(args.phase), 6),
    "    owned_paths:",
    indentList(args.ownedPaths, ["to_be_defined/"], 6),
    "    expected_artifacts:",
    indentList(args.expectedArtifacts, ["agent result packet"], 6),
    "    blocked_by: []",
    "    merge_point: merge_review",
    "    validation_commands:",
    indentList(args.validationCommands, defaultValidationCommands(args.phase), 6),
    "merge_points:",
    "  - merge_id: merge_review",
    "    reviewer: supervisor",
    "    task_review_template: templates/orchestration/task_review.md",
    "    checklist: templates/orchestration/merge_review.md",
    "    review_package: .engineering-calc/work/review-BASE..HEAD.diff",
    "validation_commands:",
    indentList(args.validationCommands, defaultValidationCommands(args.phase), 2),
    "notes:",
    "  - This draft is generated by the OpenCode plugin as text only; write it intentionally if accepted.",
    "```",
  ].join("\n");
}

function renderTaskBrief(args: OrchestrationDraftArgs): string {
  const taskId = args.taskId?.trim() || "TASK-001";
  return [
    "# Task Brief",
    "",
    `task_id: ${taskId}`,
    `phase: ${args.phase}`,
    `role: ${args.role?.trim() || defaultWorkerRole(args.phase)}`,
    "",
    "## Route Card",
    "",
    "```text",
    "task_type:",
    "material_state:",
    "required_skill_path:",
    "delivery_mode:",
    "parallel_suitability:",
    "immediate_next_action:",
    "```",
    "",
    "## Gate Card",
    "",
    "```text",
    "evidence_gate:",
    "coding_gate:",
    "handoff_status:",
    "blocking_gaps:",
    "```",
    "",
    "## Requirements",
    "",
    "- Read-only inputs:",
    ...indentMarkdownList(args.readOnlyInputs, defaultReadOnlyInputs(args.phase)),
    "- Owned paths:",
    ...indentMarkdownList(args.ownedPaths, ["to_be_defined/"]),
    "- Expected artifacts:",
    ...indentMarkdownList(args.expectedArtifacts, ["agent result packet"]),
    "- Validation commands:",
    ...indentMarkdownList(args.validationCommands, defaultValidationCommands(args.phase)),
    "",
    "## Boundaries",
    "",
    "- Do not edit paths outside owned paths.",
    "- Do not make evidence, coding, production, release, source authority, ID namespace, or final acceptance decisions.",
    "- Request shared file changes in the result packet instead of editing supervisor-owned files.",
  ].join("\n");
}

function renderAgentResultPacket(args: OrchestrationDraftArgs): string {
  const today = new Date().toISOString().slice(0, 10);
  return [
    "```yaml",
    "packet_id: ARP-001",
    "plan_id: PWP-001",
    `task_id: ${yamlScalar(args.taskId, "TASK-001")}`,
    "agent_id: agent-001",
    `role: ${yamlScalar(args.role, defaultWorkerRole(args.phase))}`,
    "status: partial # complete | partial | blocked | not_started",
    `started_at: ${today}`,
    "completed_at: null",
    "changed_paths: []",
    "artifacts_created:",
    yamlList(args.expectedArtifacts),
    "ids_touched:",
    "  source_ids: []",
    "  node_ids: []",
    "  formula_ids: []",
    "  lookup_ids: []",
    "  branch_ids: []",
    "  module_ids: []",
    "  result_paths: []",
    "assumptions: []",
    "open_questions: []",
    "validation_run:",
    "  commands:",
    indentList(args.validationCommands, [], 4),
    "  status: not_run # passed | failed | not_run | blocked",
    "  notes: []",
    "review_verdicts:",
    "  spec_compliance: not_reviewed # pass | issues | block | not_reviewed",
    "  engineering_quality: not_reviewed # pass | issues | block | not_reviewed",
    "completion_evidence:",
    "  category: \"\"",
    "  artifact_paths: []",
    "  validation_commands: []",
    "  notes: []",
    "merge_notes:",
    "  requested_shared_file_changes: []",
    "  conflicts: []",
    "  supervisor_actions_needed: []",
    "```",
  ].join("\n");
}

function renderTaskReview(args: OrchestrationDraftArgs): string {
  return [
    "# Task Review",
    "",
    `task_id: ${args.taskId?.trim() || "TASK-001"}`,
    "review_status: draft # draft | accepted | needs_changes | rejected",
    "",
    "## Inputs",
    "",
    "- task_brief:",
    "- worker_report:",
    "- review_package:",
    "- completion_evidence_category:",
    "",
    "## Spec Compliance Verdict",
    "",
    "- [ ] Required artifacts were produced.",
    "- [ ] Owned paths were respected.",
    "- [ ] Source, gate, ID, and public contract boundaries were respected.",
    "- [ ] Official calculations still flow through `run_book(BookInput) -> BookResult`.",
    "- [ ] No formulas moved into UI, report templates, batch scripts, CSV/XLSX inputs, or static HTML.",
    "",
    "Verdict: draft # accepted | needs_changes | rejected",
    "",
    "## Engineering Quality Verdict",
    "",
    "- [ ] Tests or blockers are recorded.",
    "- [ ] Formula traces and source references are stable where applicable.",
    "- [ ] Report/UI/batch layers are thin and traceable.",
    "- [ ] Validation evidence is fresh and matches `shared/completion-evidence.md`.",
    "",
    "Verdict: draft # accepted | needs_changes | rejected",
    "",
    "## Findings",
    "",
    "- Critical:",
    "- Important:",
    "- Minor:",
  ].join("\n");
}

function renderMergeReview(args: OrchestrationDraftArgs): string {
  return [
    "# Merge Review",
    "",
    "## Context",
    "",
    "| Item | Value |",
    "| --- | --- |",
    "| Plan ID | PWP-001 |",
    `| Task ID | ${args.taskId?.trim() || "TASK-001"} |`,
    `| Worker role | ${args.role?.trim() || defaultWorkerRole(args.phase)} |`,
    `| Task brief | .engineering-calc/work/task-${args.taskId?.trim() || "TASK-001"}-brief.md |`,
    "| Worker report | templates/orchestration/agent_result_packet.yaml |",
    "| Review package | .engineering-calc/work/review-BASE..HEAD.diff |",
    "| Reviewer | supervisor |",
    "| Review status | draft / accepted / needs_changes / rejected |",
    "",
    "## Spec Compliance",
    "",
    "- [ ] Worker only changed declared owned paths.",
    "- [ ] Result packet is present and complete.",
    "- [ ] No worker made final evidence, coding, production, or release gate decisions.",
    "- [ ] No worker changed source IDs, formula IDs, lookup IDs, branch IDs, module IDs, or result paths outside its assignment.",
    "- [ ] No engineering formulas were added to UI, report templates, batch scripts, CSV/XLSX input files, or presentation-only code.",
    "- [ ] Official calculation flow still uses `run_book(BookInput) -> BookResult`.",
    "- [ ] Source references and formula traces are stable.",
    "- [ ] Requested shared file changes are listed for supervisor action instead of applied out of scope.",
    "",
    "Spec verdict: draft # pass | issues | block",
    "",
    "## Engineering Quality",
    "",
    "- [ ] Tests, validation commands, or blockers are recorded.",
    "- [ ] Implementation is local to the assigned layer.",
    "- [ ] Shared contracts and public interfaces remain coherent.",
    "- [ ] Validation evidence is fresh enough to support the claimed completion category.",
    "",
    "Engineering verdict: draft # pass | issues | block",
    "",
    "## Merge Decision",
    "",
    "Decision: draft # accepted | needs_changes | rejected",
    "",
    "Reviewer notes:",
    "",
    "- to_be_defined",
  ].join("\n");
}

function renderProgressLedger(args: OrchestrationDraftArgs): string {
  return [
    "# Progress Ledger",
    "",
    "Use this ledger in `.engineering-calc/work/progress.md` or an equivalent project-local scratch location.",
    "It is the recovery map after context compaction.",
    "",
    "```text",
    "Task ID | Status | Route | Gate | Evidence | Commits | Notes",
    `${args.taskId?.trim() || "TASK-001"} | pending | ${args.phase} |  |  |  | ${args.objective?.trim() || ""}`,
    "```",
    "",
    "Statuses: `pending`, `in_progress`, `complete`, `blocked`, `needs_review`, `rejected`.",
    "",
    "Resume from the first task not marked `complete`. Trust the ledger and git history over chat memory.",
  ].join("\n");
}

function indentList(values: string[] | undefined, fallback: string[], spaces: number): string {
  const prefix = " ".repeat(spaces);
  const items = values && values.length > 0 ? values : fallback;
  if (items.length === 0) return `${prefix}[]`;
  return items.map((item) => `${prefix}- ${yamlScalar(item, "to_be_defined")}`).join("\n");
}

function indentMarkdownList(values: string[] | undefined, fallback: string[]): string[] {
  const items = values && values.length > 0 ? values : fallback;
  return items.map((item) => `  - ${item}`);
}

function defaultWorkerRole(phase: OrchestrationPhase): string {
  switch (phase) {
    case "acquisition":
      return "reference-acquirer";
    case "analysis":
      return "logic-extractor";
    case "verification":
      return "verification-worker";
    case "release":
      return "verification-worker";
    case "implementation":
    default:
      return "module-worker";
  }
}

function defaultReadOnlyInputs(phase: OrchestrationPhase): string[] {
  switch (phase) {
    case "acquisition":
      return ["references/acquisition/reference_gap_assessment.md"];
    case "analysis":
      return ["references/source_registry.yaml"];
    case "verification":
      return ["handoff/implementation_handoff.yaml", "tests/"];
    case "release":
      return ["release/release_checklist.md", "deploy/"];
    case "implementation":
    default:
      return ["handoff/implementation_handoff.yaml"];
  }
}

function defaultValidationCommands(phase: OrchestrationPhase): string[] {
  if (phase === "implementation" || phase === "verification" || phase === "release") {
    return ["pytest"];
  }
  return ["python scripts/validate_artifacts.py --package-root . --profile core"];
}
