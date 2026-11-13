# DeepSeek Harness Plugin Adapter

This adapter maps the Engineering Calculation System skill pack onto DeepSeek
Harness. Read it before the router when the pack is loaded through the
`@engineering-calculation-system/dsh-plugin` bundle.

## How the pack is loaded

The bundle registers one DeepSeek Harness skill named
`engineering-calculation-system`. A session sees the name and description in its
skill catalog and loads the body with the `skill` tool. The loaded result
carries a resource base:

```text
<skill_resources>
Base directory for this skill: <the installed package directory>/skills/engineering-calculation-system
</skill_resources>
```

Resolve every relative path in this pack — `skills/00-engineering-calculation-router.skill.md`,
`shared/lifecycle.md`, `templates/`, `scripts/validate_artifacts.py` — against
that base directory and read the file with an absolute path. The loaded result
does not enumerate the bundle, so read exactly the files the router or a parent
names. Reading outside the session workspace is permitted; writing there is not.

## Tool mapping

| This pack asks for | DeepSeek Harness tool |
|---|---|
| Read a skill file, source extract, or produced artifact | `read` |
| Create or overwrite an artifact | `write` |
| Apply a targeted change to an existing file | `edit` |
| Find files or search text | `glob`, `grep` |
| Run a validator, build, test, or generator | `pwsh` on Windows, `bash` elsewhere |
| Track multi-step implementation work | `todo_write` |
| Delegate a bounded package | `subagent` or `subagent_fork` |
| Continue, inspect, or stop a delegated child | `send_message`, `list_agents`, `interrupt_agent` |
| Run a long command without blocking the turn | `pwsh` with `run_in_background`, then `job_list`, `job_output`, `job_kill` |
| Fetch a standard, manual, datasheet, or vendor page | `web_fetch`, `web_search` |
| Ask the user a blocking question | `ask_user_question` |
| Hand the user a produced deliverable | `present` |
| Request approval for the plan before implementation | `exit_plan_mode` |

## Shell and platform

- Windows sessions run `pwsh`; the `bash` tool is absent there. POSIX sessions
  run `bash`.
- Every shell call is a fresh process. Directory changes, exported variables,
  and activated virtual environments do not survive into the next call, so use
  absolute paths and set everything a command needs inside that one call.
- `python3` may not exist on Windows. Use `python` or `py`, quote paths that
  contain spaces, and keep the invocation identical to the one recorded in the
  evidence you report.

## Workspace, sandbox, and approval

- A session starts in `workspace-write` with approval `ask` unless the
  deployment states otherwise. Writes are confined to the session workspace and
  the platform temporary directory; reads are not confined.
- A denied write or command reports `[sandbox: file access denied under
  <mode> mode]` with a one-call escalation hint. Escalating widens file effects
  for that call only and asks the user; it is never a way to skip a gate.
- Generate the project scaffold, sources, reports, and validation output inside
  the session workspace. Treat a tool failure as a lifecycle failure, not as a
  reason to rerun the same call with a wider mode.

## Evidence and the session log

- Every model-visible input is reconstructable from the session log, which
  lives under `$DSH_HOME/sessions`. Session evidence is therefore the record of
  what actually ran.
- Report the commands you ran and their real output. Do not restate a gate as
  passed from memory, and do not present a summary the log cannot support.
- `shared/completion-evidence.md` remains the single source for the
  claim-to-evidence mapping; this adapter adds no weaker path to a
  completion, production, deployable, or web-complete claim.

## Delegation boundaries

`subagent` delegates a bounded task to a child that may select its own model;
`subagent_fork` inherits the parent route and history. Both create a separate
session with its own transcript, and `send_message`, `list_agents`, and
`interrupt_agent` continue or inspect the children a parent starts.

Pass a complete brief — source paths, owned files, artifact paths, the
acceptance criterion, and the exact command that proves it — because a child
sees neither this session's reasoning nor its unstated context. The
non-delegable decisions stay in the parent session: lifecycle routing,
evidence-gate decisions, source-authority ranking, ID-namespace control,
handoff freeze, `run_book()` public-contract changes, and final acceptance.

## Planning and user-facing output

- In plan mode, submit the plan through `exit_plan_mode` and wait for approval
  before implementing. Use `todo_write` for implementation tracking only.
- `present` hands a produced file or report to the user; it does not replace
  the artifact contract in `shared/delivery-contract.md`.
- Client-facing copy belongs to the client's locale dictionaries; generated web
  calculation systems keep their own i18n layer as the templates specify.

## What stays platform-neutral

The lifecycle router, parent skills, child skills, shared engineering
contracts, artifact templates, project scaffold, `run_book(BookInput) ->
BookResult` contract, and validation scripts are unchanged. This adapter maps
only how those instructions reach tools and how results are proven.
