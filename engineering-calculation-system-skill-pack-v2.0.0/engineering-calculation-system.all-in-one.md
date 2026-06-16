# Engineering Calculation System - All-in-One Skill Pack
Version: 2.1.1

This merged file combines the root entrypoint, parent skills, child skills, shared contracts, key templates, validation schema, and scaffold files.


---

## adapters/agent-entrypoints.md

# Agent Entrypoints

Use this file when the target agent cannot automatically discover the root `SKILL.md`.

## Codex

Install the package as a skill folder when possible. The root `SKILL.md` is the primary entrypoint. For a single-file import, use `engineering-calculation-system.all-in-one.md`.

## Qoder / Trae / opencode

Register the package root as project instructions or a reusable prompt bundle. Use this routing prompt:

```text
Use the Engineering Calculation System skill pack.
Start with skills/00-engineering-calculation-router.skill.md.
Do not load all child skills at once. Load only the parent and child skills selected by the router.
During 02-reference-discovery-and-acquisition, use available internet search/browser tools actively for missing or insufficient references, and log searches in references/acquisition/search_log.csv.
Use templates/ for output artifacts and scripts/validate_artifacts.py before considering the work complete.
```

## Generic Agent

If the platform only accepts one instruction file, load `engineering-calculation-system.all-in-one.md`.

If the platform accepts multiple files, expose these directories:

```text
parent/
skills/
shared/
templates/
schemas/
scripts/
project_template/
```


---

## parent/engineering-calculation-book.skill.md

---
name: engineering-calculation-book
description: Parent/orchestrator skill for building, refactoring, extending, reviewing, testing, or packaging reusable engineering calculation book software from a validated Implementation Handoff Contract. Use for typed inputs/results, separated formula modules, official book runners, report contexts, unified production frontends, Marimo module review apps, import/export packages, batch workflows, traceability, and regression tests.
---

# Engineering Calculation Book — Parent Orchestrator

Use this parent skill after a valid implementation handoff exists, or when the user explicitly requests a prototype with clearly recorded assumptions.

This skill builds engineering calculation books as reusable, auditable software systems, not disposable scripts.

## Core Principle

Correctness and traceability come first. Reuse comes second. Presentation comes third.

Never place engineering formulas in:

```text
UI code
frontend code
review apps
report templates
batch scripts
CSV/Excel input files
presentation-only code
```

All official calculation paths must call:

```python
def run_book(book_input: BookInput) -> BookResult:
    ...
```

Operational interfaces should use the shared layout pattern from Skill 12:

```text
top bar for case/status/import/export/report preview
left panel for grouped BookInput forms
right workbench for governing summary, warnings/errors, results, charts, and traces
modal/drawer for report preview, imported report comparison, source trace, formula trace, and package validation
status strip for hashes, versions, package id, and timestamp
```

## Child Skills to Use

Use these child skills in order:

```text
08-calculation-book-architecture
09-core-and-data-models
10-reusable-calculation-modules
11-book-runner-and-governing-summary
12-report-review-batch-interfaces
13-verification-regression-traceability
```

If implementation handoff is missing, incomplete, or not source-backed, route upstream:

```text
01 -> 02 -> 03 -> 04 -> 05 -> 06 -> 07
```

## Dependency Direction

Use only this direction:

```text
presentation / report / review / batch / API
  -> books
    -> libraries
      -> core
```

Forbidden reverse dependencies:

```text
core imports libraries/books/UI/report
libraries import books/UI/report/batch
books import UI pages or report templates
reports/templates recalculate engineering results
batch runner implements separate formula logic
```

## Required Implementation Flow

1. Read `handoff/implementation_handoff.yaml` and `handoff/coding_go_no_go.md`.
2. Classify requested features by layer.
3. Define project structure and dependency rules.
4. Define core statuses, errors, metadata, units, validators, hash and serialization utilities.
5. Define typed `BookInput`, `BookResult`, module input/result models, and result paths.
6. Implement reusable calculation modules with formula traces.
7. Implement official `run_book()` orchestration.
8. Implement governing summary and warnings/errors aggregation.
9. Build report context, unified frontend, Marimo module review app, API, CLI, import/export package flow, or batch only as thin interfaces over `run_book()`.
10. Add unit, branch, lookup, regression, integration, and smoke tests.
11. Record acceptance status.

## Required Final Output

For new calculation book systems, provide:

```text
feature classification table
project structure
input schemas and typed models
unit system and status semantics
reusable module interfaces
book runner design
governing summary design
result path registry
report context design when needed
unified review/frontend/batch flow when needed
Marimo review app design when needed
data package import/export contract when needed
test plan and skeletons
run commands
acceptance checklist
```


---

## parent/engineering-calculation-logic-architecture.skill.md

---
name: engineering-calculation-logic-architecture
description: Parent/orchestrator skill for transforming a local engineering evidence library or user-provided engineering references into an implementation-ready Calculation Logic Blueprint and Implementation Handoff Contract. Use before coding when analyzing engineering codes, manuals, PDFs, spreadsheets, reports, design notes, test reports, soil reports, existing scripts, or legacy calculation books.
---

# Engineering Calculation Logic Architecture — Parent Orchestrator

Use this parent skill after the evidence gate has enough material to analyze. If no material exists or the source basis is too weak, route upstream to `engineering-calculation-reference-acquisition` first.

This skill does not primarily write production code. It orchestrates child skills that turn references into a traceable, implementation-ready calculation architecture.

## Core Principle

Mermaid diagrams are views, not the product.

The product is a reviewable, traceable, implementation-ready `Calculation Logic Blueprint`, followed by a formal `Implementation Handoff Contract`.

Required transformation:

```text
local evidence library / user references
-> source inventory and authority ranking
-> engineering concept map
-> normalized calculation logic
-> formula / lookup / branch inventory
-> Mermaid views
-> software module mapping
-> verification plan
-> implementation_handoff.yaml
```

## Child Skills to Use

Use these child skills in order:

```text
04-source-intake-and-authority
05-engineering-logic-blueprint
06-formula-lookup-branch-extraction
07-implementation-handoff-contract
```

If `references/acquisition/acquisition_handoff.yaml` does not exist and source sufficiency is doubtful, run:

```text
01-reference-adequacy-and-gap-assessment
02-reference-discovery-and-acquisition
03-reference-persistence-and-local-library
```

before this analysis sequence.

## Required Artifact Flow

```text
references/source_registry.yaml
references/evidence_library_manifest.yaml
analysis/01_source_inventory/
analysis/02_logic_blueprint/
analysis/03_logic_details/
analysis/04_diagrams/
analysis/05_risks_and_questions/
handoff/
```

## Workflow

1. Confirm that sources are available and adequate enough for analysis.
2. Run source intake and authority classification.
3. Build engineering concept map and normalized calculation node inventory.
4. Extract formulas, lookup tables, interpolation rules, branch logic, unit/sign conventions, assumptions, and applicability limits.
5. Generate Mermaid views from the normalized logic, not from raw prose.
6. Map nodes to future software modules, input models, result models, report context, and tests.
7. Create `implementation_handoff.yaml`, `artifact_index.yaml`, and `coding_go_no_go.md`.
8. Stop before production coding unless the user explicitly asks for implementation and the handoff gate allows it.

## Required Final Output

For substantial analysis tasks, provide:

```text
1. Evidence basis and source sufficiency status
2. Source summary and authority ranking
3. Engineering concept map
4. Calculation logic summary
5. Normalized calculation node inventory
6. Formula / method / lookup / branch inventory
7. Mermaid global flowchart
8. Mermaid data flow diagram when useful
9. Mermaid branch logic diagram when useful
10. Mermaid module dependency diagram when useful
11. Input, intermediate, and output inventories
12. Software module mapping
13. Suggested data model groups
14. Validation rules
15. Verification plan
16. Risks, ambiguities, assumptions, and open questions
17. Implementation handoff package
18. Coding gate recommendation
```

## Quality Gate

Before handoff, verify:

```text
source IDs are stable
source authority is explicit
conflicts are recorded
major concepts are identified
major formulas and lookup rules are traced
branch logic is explicit
unit and sign conventions are recorded
inputs and outputs are model-ready
risks are not hidden
open questions are classified by coding impact
handoff status is explicit: no_go, prototype_allowed, or production_allowed
```


---

## parent/engineering-calculation-reference-acquisition.skill.md

---
name: engineering-calculation-reference-acquisition
description: Parent/orchestrator skill for finding, screening, acquiring, and locally persisting engineering references before analysis. Use when the user has no materials, insufficient materials, stale or conflicting materials, unclear code basis, or asks the model to find references for an engineering calculation workflow before building a Calculation Logic Blueprint or software implementation.
---

# Engineering Calculation Reference Acquisition — Parent Orchestrator

Use this parent skill before reference analysis when source materials are missing, incomplete, stale, contradictory, or not authoritative enough.

This skill does not extract all formulas and does not implement code. It creates a local evidence library that downstream analysis can trust and cite.

## Core Principle

Do not invent engineering calculation rules when references are missing.

When web search or browser/search tools are available, the acquisition phase must use them. Missing, incomplete, stale, or jurisdiction-specific references require active internet search, source opening/inspection where possible, authority screening, and logged search evidence before analysis proceeds.

Required transformation:

```text
user intent / sparse description
-> reference adequacy assessment
-> gap list and acquisition plan
-> source discovery and authority screening
-> local persistence of allowed materials and source cards
-> acquisition_handoff.yaml
-> downstream source intake and analysis
```

## Child Skills to Use

Use these child skills in order:

```text
01-reference-adequacy-and-gap-assessment
02-reference-discovery-and-acquisition
03-reference-persistence-and-local-library
```

## When to Use

Use when:

```text
no reference materials are provided
only a short user description is provided
uploaded materials omit code basis, equations, tables, examples, or units
provided materials conflict or are obsolete
source authority is unclear
user asks to find design codes, manuals, examples, or calculation references
implementation request arrives without a valid source basis or handoff
```

## Required Artifact Flow

```text
references/acquisition/reference_gap_assessment.md
references/acquisition/acquisition_plan.yaml
references/acquisition/search_log.csv
references/acquisition/candidate_sources.csv
references/acquisition/source_coverage_matrix.csv
references/acquisition/retrieval_decisions.csv
references/raw/
references/source_cards/
references/extracted/
references/source_registry.yaml
references/evidence_library_manifest.yaml
references/acquisition/acquisition_handoff.yaml
```

## Copyright and Access Rules

Never bypass paywalls, login walls, subscription systems, robots restrictions, or license controls.

Persist raw full documents only when they are:

```text
user-provided
explicitly authorized by the user
openly downloadable from an official or public source with acceptable use
public-domain or clearly permissively licensed
```

For copyrighted standards, codes, manuals, papers, or textbooks, prefer:

```text
source cards
bibliographic metadata
clause/table/equation identifiers
short compliant excerpts
paraphrased notes
page references
links or access instructions
```

Do not store long copyrighted passages simply to make downstream work easier.

## Quality Gate

Before handing off to analysis, verify:

```text
minimum source basis is identified
source coverage is mapped to calculation needs
source IDs are stable
search attempts are logged
candidate sources are ranked
retrieval decisions are recorded
local file paths or source cards exist
uncovered gaps remain explicit
evidence gate is stated: evidence_no_go, search_required, partial_analysis_allowed, or analysis_allowed
```

## Required Final Output

Provide:

```text
reference adequacy summary
gaps found
sources searched
candidate sources selected or rejected
local persistence summary
coverage matrix summary
remaining missing evidence
recommended next skill path
acquisition_handoff.yaml summary
```


---

## project_template/engineering_calc_project/pyproject.toml

[project]
name = "engineering-calc-project"
version = "0.1.0"
description = "Scaffold for source-backed engineering calculation book software."
requires-python = ">=3.9"

[project.optional-dependencies]
web = [
    "flask>=3.0",
    "gunicorn>=21.2",
]
review = [
    "marimo>=0.8",
    "pandas>=2.0",
]
dev = [
    "pytest>=7.0",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]


---

## project_template/engineering_calc_project/README.md

# Engineering Calculation Project Scaffold

This scaffold supports the full v2 lifecycle:

```text
references -> analysis -> handoff -> implementation -> src -> tests -> outputs
```

Start with `references/acquisition/` when materials are missing or insufficient.

## Validate

From this directory:

```bash
python3 -m pytest -q
```

From the skill pack root:

```bash
python3 scripts/validate_artifacts.py --package-root . --project project_template/engineering_calc_project
```


---

## project_template/engineering_calc_project/src/pkg/__init__.py

"""Engineering calculation package scaffold."""


---

## project_template/engineering_calc_project/src/pkg/books/__init__.py

"""Calculation book packages."""


---

## project_template/engineering_calc_project/src/pkg/books/book_name/__init__.py

"""Example calculation book scaffold."""

from .book_runner import run_book

__all__ = ["run_book"]


---

## project_template/engineering_calc_project/src/pkg/books/book_name/book_models.py

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from pkg.core.checks import CheckResult
from pkg.core.enums import Status


@dataclass(frozen=True)
class ProjectInfo:
    project_id: str
    case_id: str
    title: str


@dataclass(frozen=True)
class BookInput:
    project: ProjectInfo
    design_options: dict[str, Any] = field(default_factory=dict)
    inputs: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class GoverningSummary:
    overall_status: Status
    governing_check_id: str | None = None
    governing_check_name: str | None = None
    governing_utilization_or_margin: float | None = None
    governing_limit: float | None = None
    critical_load_case_or_combination: str | None = None
    warnings_count: int = 0
    errors_count: int = 0


@dataclass(frozen=True)
class BookResult:
    project: ProjectInfo
    governing: GoverningSummary
    checks: list[CheckResult]
    intermediate_values: dict[str, Any] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


---

## project_template/engineering_calc_project/src/pkg/books/book_name/book_runner.py

from __future__ import annotations

from .book_models import BookInput, BookResult, GoverningSummary
from pkg.core.enums import Status


def run_book(book_input: BookInput) -> BookResult:
    """Official calculation entry point. Interfaces, reports, and batch must call this."""
    checks = []
    governing = GoverningSummary(
        overall_status=Status.NOT_EVALUATED,
        warnings_count=0,
        errors_count=0,
    )
    return BookResult(project=book_input.project, governing=governing, checks=checks)


---

## project_template/engineering_calc_project/src/pkg/books/book_name/report_context.py

from __future__ import annotations

from .book_models import BookResult


def build_report_context(result: BookResult) -> dict:
    """Build presentation data from BookResult without recalculating engineering logic."""
    return {
        "project": result.project,
        "governing": result.governing,
        "checks": result.checks,
        "warnings": result.warnings,
        "errors": result.errors,
    }


---

## project_template/engineering_calc_project/src/pkg/books/book_name/templates/.gitkeep




---

## project_template/engineering_calc_project/src/pkg/core/.gitkeep




---

## project_template/engineering_calc_project/src/pkg/core/__init__.py

"""Core status, trace, validation, and serialization utilities."""


---

## project_template/engineering_calc_project/src/pkg/core/checks.py

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .enums import Status


@dataclass(frozen=True)
class FormulaTrace:
    formula_id: str
    formula_name: str
    source_reference: str
    inputs: dict[str, Any]
    intermediates: dict[str, Any]
    result_symbol: str
    result_value: Any
    unit: str | None = None
    notes: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class CheckResult:
    check_id: str
    name: str
    status: Status
    demand: float | None = None
    capacity: float | None = None
    utilization: float | None = None
    limit: float | None = None
    unit: str | None = None
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    formula_traces: list[FormulaTrace] = field(default_factory=list)


---

## project_template/engineering_calc_project/src/pkg/core/enums.py

from enum import Enum


class Status(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    WARNING = "WARNING"
    ERROR = "ERROR"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    NEEDS_CONFIRMATION = "NEEDS_CONFIRMATION"
    NOT_EVALUATED = "NOT_EVALUATED"


---

## project_template/engineering_calc_project/src/pkg/interfaces/.gitkeep




---

## project_template/engineering_calc_project/src/pkg/interfaces/__init__.py

"""Thin CLI, API, and batch interfaces over book runners."""


---

## project_template/engineering_calc_project/src/pkg/libraries/__init__.py

"""Reusable engineering calculation libraries."""


---

## project_template/engineering_calc_project/src/pkg/libraries/geotech/__init__.py

"""Geotechnical calculation libraries."""


---

## project_template/engineering_calc_project/src/pkg/libraries/geotech/shallow_foundation/.gitkeep




---

## project_template/engineering_calc_project/src/pkg/libraries/geotech/shallow_foundation/__init__.py

"""Shallow foundation reusable module namespace."""


---

## project_template/engineering_calc_project/src/pkg/report/.gitkeep




---

## project_template/engineering_calc_project/src/pkg/report/__init__.py

"""Report rendering helpers that consume BookResult or ReportContext."""


---

## project_template/engineering_calc_project/tests/conftest.py

from pathlib import Path
import sys


SRC = Path(__file__).resolve().parents[1] / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


---

## project_template/engineering_calc_project/tests/integration/.gitkeep




---

## project_template/engineering_calc_project/tests/integration/test_book_runner.py

from pkg.books.book_name.book_models import BookInput, ProjectInfo
from pkg.books.book_name.book_runner import run_book


def test_run_book_returns_result():
    book_input = BookInput(project=ProjectInfo(project_id="P001", case_id="C001", title="Example"))
    result = run_book(book_input)
    assert result.project.case_id == "C001"
    assert result.governing is not None


---

## project_template/engineering_calc_project/tests/regression/.gitkeep




---

## project_template/engineering_calc_project/tests/smoke/.gitkeep




---

## project_template/engineering_calc_project/tests/unit/.gitkeep




---

## README.md

# Engineering Calculation System Skill Pack v2.1.1

This package organizes engineering calculation software development into a full three-stage lifecycle:

```text
reference acquisition and local persistence
-> reference analysis and calculation logic blueprint
-> implementation, reporting, batch execution, verification, and traceability
```

The implementation stage now includes a unified interface pattern:

```text
polished frontend with left-side inputs and right-side review results
Marimo review pages for module-level inspection and draft edits
managed data/report import and uploadable calculation packages
```

## Why v2.0 exists

The earlier architecture handled two mature stages:

```text
analyze available references
-> create an implementation-ready handoff
-> build reusable engineering calculation book software
```

v2.0 adds the missing upstream layer for cases where the user has no references, incomplete references, or references that are not authoritative enough:

```text
assess reference gaps
-> discover candidate sources
-> actively use available internet search / browser / retrieval tools
-> screen authority and relevance
-> persist a local evidence library
-> hand off to source intake and analysis
```

## Core lifecycle

```text
00 router
01 reference adequacy and gap assessment
02 reference discovery and acquisition
03 reference persistence and local library
04 source intake and authority
05 engineering logic blueprint
06 formula lookup branch extraction
07 implementation handoff contract
08 calculation book architecture
09 core and data models
10 reusable calculation modules
11 book runner and governing summary
12 report review batch interfaces, unified UI, Marimo review, and data packages
13 verification regression traceability
```

## Parent skills

```text
parent/engineering-calculation-reference-acquisition.skill.md
parent/engineering-calculation-logic-architecture.skill.md
parent/engineering-calculation-book.skill.md
```

## Agent entrypoints

Use `SKILL.md` as the root skill entrypoint for Codex-compatible environments. For other agents, see:

```text
adapters/agent-entrypoints.md
```

If the target environment cannot coordinate multiple files, load:

```text
engineering-calculation-system.all-in-one.md
```

## Key handoff artifacts

```text
references/acquisition/acquisition_handoff.yaml
references/source_registry.yaml
analysis/02_logic_blueprint/calculation_blueprint.md
handoff/implementation_handoff.yaml
handoff/artifact_index.yaml
handoff/coding_go_no_go.md
```

## Copyright and access rule

Do not bypass paywalls, login walls, licensing restrictions, or access controls. Persist full raw documents only when user-provided, explicitly authorized, or openly downloadable with acceptable use. For copyrighted standards, codes, manuals, papers, and textbooks, prefer source cards, citations, clause identifiers, short compliant excerpts, and paraphrased notes.

## Validation

Validate the package itself:

```bash
python3 scripts/validate_artifacts.py --package-root .
```

Validate the included scaffold:

```bash
python3 scripts/validate_artifacts.py --package-root . --project project_template/engineering_calc_project
```

Run the scaffold smoke test:

```bash
cd project_template/engineering_calc_project
python3 -m pytest -q
```


---

## README.zh-CN.md

# 工程计算系统技能包 v2.1.1

本包把工程计算软件工作流升级为三段式闭环：

```text
资料获取与本地持久化
→ 资料分析与计算逻辑蓝图
→ 编程实现与验证追溯
```

适用场景：

```text
没有资料，但用户想建立工程计算程序
资料不足，无法安全抽取公式/分支/查表
已有资料，需要分析成 Calculation Logic Blueprint
已有 Blueprint / handoff，需要架构编程
已有代码，需要重构、测试、报告、批量计算
```

## v2.0 的核心变化

v1.0 已经解决了：

```text
资料分析
→ Calculation Logic Blueprint
→ Implementation Handoff Contract
→ Calculation Book Implementation
```

v2.0 新增前置层：

```text
Reference Adequacy Assessment
→ Reference Discovery and Acquisition
→ Reference Persistence and Local Evidence Library
```

这意味着当没有资料或资料不足时，模型不应该直接编造公式，也不应该勉强编码，而应该先：

```text
判断资料缺口
制定检索计划
充分调用可用的上网搜索 / 浏览 / 检索工具寻找权威资料
筛选候选来源
把可保存内容、来源卡片、摘录、检索日志、覆盖矩阵持久化到本地
再进入资料分析
```

## 推荐主流程

```text
00-router
→ 01-reference-adequacy-and-gap-assessment
→ 02-reference-discovery-and-acquisition
→ 03-reference-persistence-and-local-library
→ 04-source-intake-and-authority
→ 05-engineering-logic-blueprint
→ 06-formula-lookup-branch-extraction
→ 07-implementation-handoff-contract
→ 08-calculation-book-architecture
→ 09-core-and-data-models
→ 10-reusable-calculation-modules
→ 11-book-runner-and-governing-summary
→ 12-report-review-batch-interfaces
→ 13-verification-regression-traceability
```

## 三个父级编排技能

```text
parent/engineering-calculation-reference-acquisition.skill.md
parent/engineering-calculation-logic-architecture.skill.md
parent/engineering-calculation-book.skill.md
```

父级技能只负责编排，子技能负责具体任务。这样既避免两个巨型技能过重，也避免碎片化失控。

## Agent 入口

Codex 兼容环境优先使用根目录：

```text
SKILL.md
```

Qoder / Trae / opencode 等环境可参考：

```text
adapters/agent-entrypoints.md
```

如果目标环境不适合加载多个文件，使用单文件版本：

```text
engineering-calculation-system.all-in-one.md
```

## 最关键的接口文件

```text
references/acquisition/acquisition_handoff.yaml
references/source_registry.yaml
analysis/02_logic_blueprint/calculation_blueprint.md
analysis/03_logic_details/formula_inventory.csv
handoff/implementation_handoff.yaml
handoff/artifact_index.yaml
handoff/coding_go_no_go.md
```

其中：

```text
acquisition_handoff.yaml
```

连接“找资料”与“分析资料”；

```text
implementation_handoff.yaml
```

连接“分析资料”与“架构编程”。

## 本地持久化原则

```text
用户上传或授权保存的原始资料 → references/raw/
公开可下载且允许保存的资料 → references/raw/
不能或不应完整保存的资料 → references/source_cards/ + references/extracted/notes/
检索过程 → references/acquisition/search_log.csv
候选资料 → references/acquisition/candidate_sources.csv
资料覆盖情况 → references/acquisition/source_coverage_matrix.csv
资料注册表 → references/source_registry.yaml
```

不要绕过付费墙、登录限制、版权限制或访问控制。对于标准、规范、教材、论文等受版权保护内容，应优先保存来源卡片、短摘录、条款编号、页码、摘要和引用信息，而不是保存大段原文。

## 安装建议

复制以下目录到你的技能环境：

```text
SKILL.md
parent/
skills/
shared/
templates/
schemas/
scripts/
```

如果你的环境不适合加载多个技能，可以使用：

```text
engineering-calculation-system.all-in-one.md
```

## 校验

校验技能包：

```bash
python3 scripts/validate_artifacts.py --package-root .
```

校验内置工程骨架：

```bash
python3 scripts/validate_artifacts.py --package-root . --project project_template/engineering_calc_project
```

运行骨架最小测试：

```bash
cd project_template/engineering_calc_project
python3 -m pytest -q
```

## 版本

```text
version: 2.1.1
created_at: 2026-06-16
status: complete_packaged_release
```


---

## schemas/artifact_contracts.json

{
  "version": "2.1.1",
  "package_required_paths": [
    "SKILL.md",
    "agents/openai.yaml",
    "adapters/agent-entrypoints.md",
    "skills/00-engineering-calculation-router.skill.md",
    "parent/engineering-calculation-reference-acquisition.skill.md",
    "parent/engineering-calculation-logic-architecture.skill.md",
    "parent/engineering-calculation-book.skill.md",
    "shared/quality-gates.md",
    "templates/acquisition/open_reference_questions.md",
    "templates/acquisition/acquisition_notes.md",
    "templates/analysis/source_intake_notes.md",
    "templates/analysis/unit_and_sign_conventions.md",
    "templates/handoff/implementation_handoff.md",
    "templates/implementation/project_structure.md",
    "templates/implementation/dependency_rules.md",
    "templates/implementation/package_layout.md",
    "templates/implementation/core_model_plan.md",
    "templates/implementation/status_semantics.md",
    "templates/implementation/unit_system.md",
    "templates/implementation/formula_trace_spec.md",
    "templates/implementation/lookup_module_spec.md",
    "templates/implementation/governing_summary_spec.md",
    "templates/implementation/input_mapping_spec.md",
    "templates/implementation/ui_layout_spec.md",
    "templates/implementation/import_export_contract.md",
    "templates/implementation/marimo_review_spec.md",
    "templates/implementation/review_readability_checklist.md",
    "templates/implementation/data_package_manifest.yaml",
    "schemas/artifact_contracts.json",
    "scripts/validate_artifacts.py",
    "scripts/build_package_index.py"
  ],
  "skill_files": [
    "SKILL.md",
    "skills/00-engineering-calculation-router.skill.md",
    "skills/01-reference-adequacy-and-gap-assessment.skill.md",
    "skills/02-reference-discovery-and-acquisition.skill.md",
    "skills/03-reference-persistence-and-local-library.skill.md",
    "skills/04-source-intake-and-authority.skill.md",
    "skills/05-engineering-logic-blueprint.skill.md",
    "skills/06-formula-lookup-branch-extraction.skill.md",
    "skills/07-implementation-handoff-contract.skill.md",
    "skills/08-calculation-book-architecture.skill.md",
    "skills/09-core-and-data-models.skill.md",
    "skills/10-reusable-calculation-modules.skill.md",
    "skills/11-book-runner-and-governing-summary.skill.md",
    "skills/12-report-review-batch-interfaces.skill.md",
    "skills/13-verification-regression-traceability.skill.md",
    "parent/engineering-calculation-reference-acquisition.skill.md",
    "parent/engineering-calculation-logic-architecture.skill.md",
    "parent/engineering-calculation-book.skill.md"
  ],
  "csv_headers": {
    "templates/acquisition/candidate_sources.csv": "candidate_id,title,publisher,source_type,version_or_date,jurisdiction,url_or_location,access_date,authority_level,relevance_score,gaps_covered,recommended_action,limitations,license_or_access_notes",
    "templates/acquisition/local_persistence_log.csv": "entry_id,source_id,file_role,path,sha256,created_at,notes",
    "templates/acquisition/retrieval_decisions.csv": "decision_id,candidate_id,decision,reason,local_target,raw_allowed,source_card_required,extraction_required,follow_up",
    "templates/acquisition/search_log.csv": "search_id,gap_id,query,tool_or_location,date,results_reviewed,candidates_selected,notes",
    "templates/acquisition/source_coverage_matrix.csv": "requirement_id,requirement,importance,covered,current_source_id,gap,needed_source_type,blocks_analysis,blocks_coding",
    "templates/analysis/applicability_limits.csv": "limit_id,assumption_or_limit,applies_to,source_reference,program_handling,risk_level",
    "templates/analysis/assumption_register.csv": "assumption_id,assumption,source_reference,reason,program_handling,blocks_production",
    "templates/analysis/branch_inventory.csv": "branch_id,condition,engineering_meaning,source_reference,path_if_true,path_if_false,not_applicable_behavior,program_representation,required_tests,risk_level",
    "templates/analysis/calculation_nodes.csv": "node_id,node_type,node_name,engineering_meaning,inputs,outputs,units,formula_or_method,source_reference,branch_condition,applicability,assumptions,module_candidate,result_visibility,report_visibility,test_requirement,risk_level",
    "templates/analysis/concept_map.csv": "concept,meaning,role_in_calculation,source_id,notes",
    "templates/analysis/formula_inventory.csv": "formula_id,name,purpose,inputs,outputs,units,source_reference,applicability,branch_dependencies,lookup_dependencies,implementation_note,test_requirement,risk_level",
    "templates/analysis/input_inventory.csv": "field,symbol,unit,source_id,required,default,validation_rule,module",
    "templates/analysis/intermediate_inventory.csv": "value,symbol,unit,derived_from,used_by,should_be_reported",
    "templates/analysis/lookup_inventory.csv": "lookup_id,name,inputs,outputs,source_reference,interpolation_rule,out_of_range_behavior,implementation_note,test_requirement,risk_level",
    "templates/analysis/open_questions.csv": "question_id,question,severity,affected_artifact,blocks_analysis,blocks_coding,recommended_resolution",
    "templates/analysis/output_inventory.csv": "output,symbol,unit,meaning,status_logic,report_section",
    "templates/analysis/risk_register.csv": "risk_id,risk,cause,impact,mitigation,owner,status",
    "templates/analysis/source_authority_table.csv": "source_id,source,source_type,version_or_date,role,priority,authority_level,notes",
    "templates/analysis/source_conflicts.csv": "conflict_id,affected_item,source_a,source_a_method,source_b,source_b_method,engineering_consequence,recommended_resolution,blocks_analysis,blocks_coding",
    "templates/implementation/feature_classification.csv": "feature,layer,existing_module,new_module_needed,reusable,location,notes",
    "templates/implementation/frontend_fields.csv": "field_path,label,unit,group,editable,source,notes",
    "templates/implementation/module_review_log.csv": "module_review_id,module_id,review_scope,input_source,edited_fields,runner_or_function,result_status,decision,output_path,notes",
    "templates/implementation/result_path_registry.csv": "result_path,meaning,unit,source_module,report_visibility,regression_check",
    "templates/implementation/review_schema.csv": "field_path,label,unit,input_type,required,validation,help_text",
    "templates/verification/test_matrix.csv": "test_id,target,type,reference_basis,input_case,expected_result,tolerance,priority,notes"
  },
  "yaml_required_keys": {
    "templates/acquisition/acquisition_handoff.yaml": [
      "acquisition_handoff_id",
      "project_or_calculation_name",
      "status",
      "source_ids",
      "coverage_summary",
      "recommended_next_skill_path"
    ],
    "templates/acquisition/acquisition_plan.yaml": [
      "plan_id",
      "project_or_calculation_name",
      "status",
      "gaps"
    ],
    "templates/acquisition/evidence_library_manifest.yaml": [
      "manifest_id",
      "status",
      "files",
      "coverage_summary"
    ],
    "templates/acquisition/source_registry.yaml": [
      "sources"
    ],
    "templates/handoff/implementation_handoff.yaml": [
      "handoff_id",
      "book_name",
      "status",
      "source_basis",
      "calculation_scope",
      "runner_sequence",
      "module_candidates",
      "coding_gate"
    ],
    "templates/handoff/artifact_index.yaml": [
      "artifact_index_id",
      "project_or_book",
      "references",
      "analysis",
      "handoff",
      "implementation",
      "verification"
    ],
    "templates/implementation/data_package_manifest.yaml": [
      "package_id",
      "schema_version",
      "created_at",
      "project_or_book",
      "package_status",
      "inputs",
      "results",
      "files",
      "hashes",
      "versions",
      "validation"
    ]
  },
  "text_required_phrases": {
    "skills/12-report-review-batch-interfaces.skill.md": [
      "Report Production Decision Protocol",
      "Report Status",
      "Production Report Minimum",
      "Unified Frontend Layout",
      "Marimo Module Review Pattern",
      "Import, Report Import, and Upload Packages"
    ],
    "templates/implementation/ui_layout_spec.md": [
      "Standard Page Zones",
      "Left input panel",
      "Right review workbench"
    ],
    "templates/implementation/import_export_contract.md": [
      "Upload Package Flow",
      "Report Import Rules",
      "Export Package Contents"
    ],
    "templates/implementation/marimo_review_spec.md": [
      "marimo edit",
      "marimo run",
      "Module Review Rules"
    ],
    "templates/implementation/review_readability_checklist.md": [
      "Governing result is visible",
      "Imported reports are labeled",
      "Marimo exploratory edits"
    ],
    "templates/implementation/report_context_spec.md": [
      "Report Production Decision Record",
      "Production Eligibility",
      "Traceability",
      "Template Boundaries"
    ],
    "templates/verification/acceptance_checklist.md": [
      "Report production decision is recorded",
      "Report status is explicit"
    ],
    "shared/quality-gates.md": [
      "Report production gate",
      "report production decision recorded"
    ]
  },
  "project_required_paths": [
    "README.md",
    "pyproject.toml",
    "tests/conftest.py",
    "webapp/.gitkeep",
    "apps/review/.gitkeep",
    "data/input/.gitkeep",
    "data/imported/reports/.gitkeep",
    "data/imported/references/.gitkeep",
    "data/staging/.gitkeep",
    "data/normalized/cases/.gitkeep",
    "data/packages/.gitkeep",
    "outputs/results_json/.gitkeep",
    "outputs/reports_html/.gitkeep",
    "outputs/reports_pdf/.gitkeep",
    "outputs/reports_docx/.gitkeep",
    "outputs/upload_packages/.gitkeep",
    "outputs/logs/.gitkeep",
    "src/pkg/__init__.py",
    "src/pkg/core/__init__.py",
    "src/pkg/books/__init__.py",
    "src/pkg/books/book_name/__init__.py",
    "src/pkg/books/book_name/book_runner.py",
    "src/pkg/books/book_name/book_models.py",
    "src/pkg/books/book_name/report_context.py",
    "src/pkg/interfaces/__init__.py",
    "src/pkg/report/__init__.py",
    "tests/integration/test_book_runner.py"
  ],
  "project_csv_headers": {
    "references/acquisition/candidate_sources.csv": "candidate_id,title,publisher,source_type,version_or_date,jurisdiction,url_or_location,access_date,authority_level,relevance_score,gaps_covered,recommended_action,limitations,license_or_access_notes",
    "references/acquisition/search_log.csv": "search_id,gap_id,query,tool_or_location,date,results_reviewed,candidates_selected,notes",
    "references/acquisition/source_coverage_matrix.csv": "requirement_id,requirement,importance,covered,current_source_id,gap,needed_source_type,blocks_analysis,blocks_coding"
  }
}


---

## scripts/validate_artifacts.py

#!/usr/bin/env python3
"""Validate the engineering calculation skill pack and generated project artifacts."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path


FRONTMATTER_RE = re.compile(r"^---\n(?P<body>.*?)\n---\n", re.DOTALL)
YAML_KEY_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*):")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_contract(package_root: Path) -> dict:
    path = package_root / "schemas" / "artifact_contracts.json"
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def check_exists(root: Path, rel_path: str, errors: list[str]) -> None:
    if not (root / rel_path).exists():
        errors.append(f"missing required path: {rel_path}")


def first_csv_line(path: Path) -> str:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        row = next(reader, [])
    return ",".join(row)


def check_csv_headers(root: Path, headers: dict[str, str], errors: list[str]) -> None:
    for rel_path, expected in headers.items():
        path = root / rel_path
        if not path.exists():
            errors.append(f"missing CSV template: {rel_path}")
            continue
        actual = first_csv_line(path)
        if actual != expected:
            errors.append(f"CSV header mismatch in {rel_path}: expected {expected!r}, got {actual!r}")


def simple_yaml_top_keys(text: str) -> set[str]:
    keys: set[str] = set()
    for line in text.splitlines():
        match = YAML_KEY_RE.match(line)
        if match:
            keys.add(match.group(1))
    return keys


def check_yaml_required_keys(root: Path, required: dict[str, list[str]], errors: list[str]) -> None:
    for rel_path, keys in required.items():
        path = root / rel_path
        if not path.exists():
            errors.append(f"missing YAML template: {rel_path}")
            continue
        present = simple_yaml_top_keys(read_text(path))
        for key in keys:
            if key not in present:
                errors.append(f"missing top-level key {key!r} in {rel_path}")


def check_text_required_phrases(root: Path, required: dict[str, list[str]], errors: list[str]) -> None:
    for rel_path, phrases in required.items():
        path = root / rel_path
        if not path.exists():
            errors.append(f"missing text artifact: {rel_path}")
            continue
        text = read_text(path)
        for phrase in phrases:
            if phrase not in text:
                errors.append(f"missing required phrase {phrase!r} in {rel_path}")


def check_skill_frontmatter(root: Path, rel_path: str, errors: list[str]) -> None:
    path = root / rel_path
    if not path.exists():
        errors.append(f"missing skill file: {rel_path}")
        return
    text = read_text(path)
    match = FRONTMATTER_RE.match(text)
    if not match:
        errors.append(f"missing YAML frontmatter in {rel_path}")
        return
    body = match.group("body")
    if not re.search(r"^name:\s*\S+", body, re.MULTILINE):
        errors.append(f"missing frontmatter name in {rel_path}")
    if not re.search(r"^description:\s*.+", body, re.MULTILINE):
        errors.append(f"missing frontmatter description in {rel_path}")


def validate_package(package_root: Path, contract: dict) -> list[str]:
    errors: list[str] = []
    for rel_path in contract["package_required_paths"]:
        check_exists(package_root, rel_path, errors)
    for rel_path in contract["skill_files"]:
        check_skill_frontmatter(package_root, rel_path, errors)
    check_csv_headers(package_root, contract["csv_headers"], errors)
    check_yaml_required_keys(package_root, contract["yaml_required_keys"], errors)
    check_text_required_phrases(package_root, contract.get("text_required_phrases", {}), errors)
    return errors


def validate_project(project_root: Path, contract: dict) -> list[str]:
    errors: list[str] = []
    for rel_path in contract["project_required_paths"]:
        check_exists(project_root, rel_path, errors)
    check_csv_headers(project_root, contract["project_csv_headers"], errors)
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package-root", default=".", help="Skill pack root directory")
    parser.add_argument("--project", help="Generated engineering calculation project root")
    args = parser.parse_args(argv)

    package_root = Path(args.package_root).resolve()
    contract = load_contract(package_root)
    errors = validate_package(package_root, contract)

    if args.project:
        errors.extend(validate_project(Path(args.project).resolve(), contract))

    if errors:
        print("Artifact validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("Artifact validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


---

## shared/artifact-index-template.yaml

artifact_index_id: A001
project_or_book: example_book
version: 0.1.0
created_at: 2026-06-16

references:
  acquisition_handoff: references/acquisition/acquisition_handoff.yaml
  source_registry: references/source_registry.yaml
  evidence_library_manifest: references/evidence_library_manifest.yaml

analysis:
  source_inventory: analysis/01_source_inventory/source_inventory.yaml
  calculation_blueprint: analysis/02_logic_blueprint/calculation_blueprint.md
  calculation_nodes: analysis/02_logic_blueprint/calculation_nodes.csv
  formula_inventory: analysis/03_logic_details/formula_inventory.csv
  lookup_inventory: analysis/03_logic_details/lookup_inventory.csv
  branch_inventory: analysis/03_logic_details/branch_inventory.csv
  risk_register: analysis/05_risks_and_questions/risk_register.csv
  open_questions: analysis/05_risks_and_questions/open_questions.csv

handoff:
  implementation_handoff: handoff/implementation_handoff.yaml
  coding_go_no_go: handoff/coding_go_no_go.md

implementation:
  architecture: implementation/00_architecture/project_structure.md
  models: implementation/01_core_models/data_model_spec.md
  modules: implementation/02_modules/module_interface_spec.md
  runner: implementation/03_book_runner/runner_sequence.md
  interfaces: implementation/04_interfaces/report_context_spec.md

verification:
  test_matrix: verification/test_matrix.csv
  tolerance_policy: verification/tolerance_policy.md
  acceptance_checklist: verification/acceptance_checklist.md


---

## shared/contracts.md

# Shared Lifecycle Contracts

## Full lifecycle

```text
user request
-> material state classification
-> reference adequacy assessment
-> reference discovery and acquisition
-> local evidence library
-> source intake and authority
-> calculation logic blueprint
-> formula / lookup / branch extraction
-> implementation handoff contract
-> calculation book architecture
-> core and data models
-> reusable calculation modules
-> book runner and governing summary
-> report / review / batch interfaces
-> verification / regression / traceability
```

## Hard handoffs

```text
references/acquisition/acquisition_handoff.yaml
```

connects acquisition to analysis.

```text
handoff/implementation_handoff.yaml
```

connects analysis to implementation.

## Source principle

A calculation rule is not implementation-ready until its source, applicability, units, branch behavior, and test requirement are explicit or its uncertainty is recorded.

## Software principle

Engineering formulas belong in reusable calculation modules and official book runners only. Interfaces and reports consume results; they do not calculate.


---

## shared/copyright-and-access-policy.md

# Copyright and Access Policy for Reference Acquisition

## Allowed persistence

Persist full raw material only when:

```text
user uploaded it
user explicitly authorized storing it
it is openly downloadable with acceptable use
it is public-domain or permissively licensed
```

## Restricted persistence

For copyrighted standards, codes, manuals, papers, textbooks, or paid sources, store:

```text
source card
bibliographic metadata
URL or access location
access date
clause/table/equation/page references
short compliant excerpts when necessary
paraphrased technical notes
coverage tags
limitations
```

Do not store long passages or complete copyrighted works unless authorized.

## Prohibited behavior

```text
bypassing paywalls
using unauthorized copies
removing access controls
copying full standards into local notes
using unverified AI summaries as governing sources
```


---

## shared/file-naming-convention.md

# File Naming Convention

## Source files

```text
S01_<short_source_name>.<ext>
S02_<short_source_name>.<ext>
CODE-01_<code_name>.<ext>
MANUAL-01_<manual_name>.<ext>
EXAMPLE-01_<worked_example>.<ext>
```

Use lowercase snake_case for generated artifacts.

## Analysis files

```text
source_inventory.yaml
calculation_blueprint.md
calculation_nodes.csv
formula_inventory.csv
lookup_inventory.csv
branch_inventory.csv
implementation_handoff.yaml
```

## Implementation files

```text
book_models.py
book_runner.py
governing.py
report_context.py
input_mapping.py
```

## Rule

Once a file path is referenced by `artifact_index.yaml`, do not rename it without updating the index.


---

## shared/handoff-contract-template.yaml

handoff_id: H001
book_name: example_book
version: 0.1.0
status: prototype_allowed # no_go | prototype_allowed | production_allowed

source_basis:
  acquisition_handoff: references/acquisition/acquisition_handoff.yaml
  source_registry: references/source_registry.yaml
  governing_sources:
    - source_id: S01
      role: governing_code
      priority: 1
  example_sources:
    - source_id: S02
      role: regression_reference

evidence_library_status:
  status: analysis_allowed
  remaining_gaps:
    - gap_id: G001
      description: example remaining gap
      blocks_production: true

calculation_scope:
  domain: geotechnical
  object: shallow_foundation
  checks:
    - bearing_capacity
    - settlement

input_model_groups:
  - ProjectInfo
  - DesignBasis
  - GeometryInput
  - LoadInput
  - MaterialOrSoilInput
  - DesignOptions

result_model_groups:
  - ModuleResult
  - CheckResult
  - GoverningSummary
  - BookResult

runner_sequence:
  - validate_input
  - normalize_units
  - select_method
  - compute_module_results
  - check_utilization
  - summarize_governing
  - build_report_context

module_candidates:
  - module: libraries.domain.category.module_name
    responsibility: compute source-backed engineering result
    source_nodes: [N001]
    formulas: [F001]
    lookups: []

formula_inventory_refs:
  - F001

lookup_inventory_refs: []

branch_inventory_refs: []

validation_rules:
  - rule_id: V001
    severity: error
    description: required input must be present
    related_inputs: []

test_requirements:
  - test_id: T001
    type: regression
    basis: S02 worked example
    tolerance: to_be_defined

report_sections:
  - section_id: R001
    title: Input summary
    result_paths: []

traceability_requirements:
  - input_hash
  - result_hash
  - formula_traces
  - source_references

open_questions:
  - question_id: Q001
    severity: high
    blocks_production: true
    description: unresolved source issue

coding_gate:
  status: prototype_allowed
  allowed_work:
    - scaffold typed models
    - implement formulas with needs_confirmation markers
  blocked_work:
    - production release
    - final report certification


---

## shared/id-convention.md

# ID Convention

## Source and acquisition IDs

```text
S01, S02, S03                 source IDs
CAND-001, CAND-002           candidate source IDs
GAP-001, GAP-002             reference gaps
SEARCH-001, SEARCH-002       search attempts
DEC-001, DEC-002             retrieval decisions
COV-001, COV-002             coverage items
```

## Analysis IDs

```text
N001, N002                   calculation nodes
F001, F002                   formulas
L001, L002                   lookup tables/charts
B001, B002                   branches
A001, A002                   assumptions
V001, V002                   validation rules
RISK-001, RISK-002           risks
Q001, Q002                   open questions
```

## Implementation IDs

```text
MOD-001, MOD-002             modules
PATH-001, PATH-002           result paths
T001, T002                   tests
```

Do not recycle IDs after downstream artifacts reference them.


---

## shared/local-persistence-contract.md

# Local Persistence Contract

## Purpose

Make retrieved or user-provided sources durable, auditable, and reusable by downstream skills.

## Raw storage rules

Store full raw files only when:

```text
user provided the file
user explicitly authorized saving
the source is openly downloadable with acceptable use
the source is public-domain or permissively licensed
```

Otherwise store a source card and limited notes.

## Required directories

```text
references/raw/
references/source_cards/
references/extracted/
references/acquisition/
references/snapshots/
```

## Required registries

```text
references/source_registry.yaml
references/evidence_library_manifest.yaml
references/acquisition/acquisition_handoff.yaml
```

## Source card required fields

```text
source_id
title
publisher_or_author
source_type
version_or_date
jurisdiction
url_or_location
access_date
raw_file_path
extracted_file_path
authority_level
coverage_tags
relevance_to_calculation
key_clauses_tables_equations_pages
short_excerpts
paraphrased_notes
limitations
license_or_access_notes
recommended_downstream_use
```

## Hashing

Use SHA256 where practical for raw and extracted files. Record hashes in `evidence_library_manifest.yaml`.


---

## shared/quality-gates.md

# Quality Gates

## Evidence gate

```text
evidence_no_go
search_required
partial_analysis_allowed
analysis_allowed
```

`analysis_allowed` requires:

```text
minimum governing or reference basis exists
source IDs are stable
coverage matrix exists
major unresolved gaps are recorded
copyright/access limitations are recorded
```

## Handoff gate

```text
no_go
prototype_allowed
production_allowed
```

`production_allowed` requires:

```text
critical formulas source-backed
critical lookup/interpolation rules defined
major branch rules defined
unit and sign conventions defined
source conflicts resolved or explicitly handled
test requirements defined
```

## Implementation gate

Before release:

```text
formulas only in calculation modules/books
one official run_book()
typed input/result models
unit conversion only at boundaries
warnings/errors preserved
result paths stable
UI and review apps follow the unified layout when present
upload/import packages have manifests and hashes when present
unit, branch, lookup, regression, integration, and smoke tests pass
traceability metadata saved
```

## Report production gate

Before labeling any report or export as final or production-ready:

```text
report production decision recorded
report status explicit
source basis and coding gate allow production
report generated from saved final input or trusted saved BookResult
ReportContext includes source basis, assumptions, limitations, warnings, errors, and traceability metadata
unified UI layout is documented when frontend exists
Marimo review app is documented when module review exists
data package manifest exists when import/export packages exist
templates, UI, Marimo apps, and batch flows do not calculate or override status
renderer/export smoke test passes
run command documented
```

If any item is missing, use a non-final status such as `draft`, `review`, `prototype`, or `not_for_construction`.


---

## shared/result-path-convention.md

# Result Path Convention

Use stable result paths for reports, tests, and regression checks.

Examples:

```text
bearing.status
bearing.utilization
bearing.capacity_kN
settlement.maximum_settlement_mm
governing.overall_status
governing.governing_check_id
warnings.count
errors.count
```

Report templates should reference result paths; they should not recalculate results.


---

## shared/source-acquisition-contract.md

# Source Acquisition Contract

## Purpose

Standardize how missing engineering references are searched, screened, and prepared for downstream analysis.

## Minimum acquisition outputs

```text
reference_gap_assessment.md
acquisition_plan.yaml
search_log.csv
candidate_sources.csv
retrieval_decisions.csv
source_coverage_matrix.csv
source_registry.yaml
evidence_library_manifest.yaml
acquisition_handoff.yaml
```

## Source decision statuses

```text
persist_raw
persist_source_card_only
use_for_background_only
reject
needs_user_access
needs_purchase_or_license
needs_confirmation
```

## Search log requirement

Every meaningful search attempt should be logged with:

```text
search_id
gap_id
query
tool_or_location
date
results_reviewed
candidates_selected
notes
```

## Internet search tool requirement

When an agent has access to internet search, browser, or retrieval tools, reference discovery must use them for missing, incomplete, stale, or jurisdiction-specific source bases.

Minimum behavior:

```text
search each critical/high gap with multiple targeted queries
prefer primary and official sources over summaries
inspect promising results when opening pages/files is possible
cross-check version/year, jurisdiction, publisher, and applicability
log the tool used in tool_or_location
record both accepted and rejected candidates
state explicitly when search tools are unavailable or blocked
```

## Candidate source requirement

Each candidate source must have:

```text
candidate_id
title
publisher
source_type
version_or_date
jurisdiction
url_or_location
access_date
authority_level
relevance_score
gaps_covered
recommended_action
limitations
license_or_access_notes
```


---

## shared/status-semantics.md

# Status Semantics

Recommended statuses:

```text
PASS
FAIL
WARNING
ERROR
NOT_APPLICABLE
NEEDS_CONFIRMATION
NOT_EVALUATED
```

Suggested comparison rule:

```text
PASS: utilization <= limit + tolerance
FAIL: utilization > limit + tolerance
NOT_APPLICABLE: check does not apply to this case
ERROR: required calculation could not be completed
WARNING: result exists but inputs or assumptions require attention
NEEDS_CONFIRMATION: source or assumption must be confirmed before production use
```


---

## shared/unit-convention.md

# Unit Convention

Default internal units:

```text
length: m
area: m2
volume: m3
force: kN
stress/pressure: kPa
unit_weight: kN/m3
moment: kNm
settlement/displacement: mm
angle_input: degree
angle_internal: radian
```

Rules:

```text
convert units at input boundaries
use internal units inside calculation modules
format units only at presentation boundaries
store unit metadata in public input/result models
reject ambiguous dimensional values
avoid mixing degree and radian fields
```


---

## SKILL.md

---
name: engineering-calculation-system
description: Full lifecycle workflow for engineering calculation software. Use when Codex or another coding agent must assess missing engineering references, acquire and persist source evidence, transform references into a Calculation Logic Blueprint, create an implementation handoff, build auditable calculation book software, or verify formulas, reports, batch flows, and traceability.
---

# Engineering Calculation System

Start with `skills/00-engineering-calculation-router.skill.md` for any non-trivial request. The router decides whether the task belongs to reference acquisition, source analysis, implementation, interface work, or verification.

## Load Order

Use progressive disclosure:

1. Read the router.
2. Read one parent orchestrator when the task spans a phase:
   - `parent/engineering-calculation-reference-acquisition.skill.md`
   - `parent/engineering-calculation-logic-architecture.skill.md`
   - `parent/engineering-calculation-book.skill.md`
3. Read only the child skill files named by the router or parent.
4. Use templates from `templates/` and shared contracts from `shared/` only when generating or validating artifacts.

For environments that cannot load multiple files reliably, use `engineering-calculation-system.all-in-one.md`.

## Non-Negotiable Gates

Do not invent engineering formulas, lookup rules, units, coefficients, or branch logic when the source basis is missing.

Do not start production implementation unless `handoff/implementation_handoff.yaml` and `handoff/coding_go_no_go.md` allow it.

Keep formulas out of UI, report templates, CSV/Excel inputs, batch scripts, and presentation-only code. Official calculations must flow through `run_book(BookInput) -> BookResult`.

## Artifact Validation

When this package is available on disk, run:

```bash
python3 scripts/validate_artifacts.py --package-root .
```

For generated engineering calculation projects, also run:

```bash
python3 scripts/validate_artifacts.py --package-root <skill-pack-root> --project <project-root>
```

Treat validation failures as blocking unless the user explicitly asks for a draft or prototype.


---

## skills/00-engineering-calculation-router.skill.md

---
name: engineering-calculation-router
description: Route engineering calculation tasks to the correct reference acquisition, reference analysis, handoff, implementation, reporting, batch, or verification skill. Use whenever the user request spans multiple stages, lacks source materials, has unclear source sufficiency, or when it is unclear whether to find references, analyze references, write code, refactor, generate reports, or test.
---

# Engineering Calculation Router

Use this skill to decide which engineering calculation skill path should handle the task.

## Routing Principle

Do not jump into analysis or coding when the source basis is missing or insufficient.

Do not jump into coding when raw references exist but no implementation handoff exists.

Do not analyze references again when a valid source-backed `implementation_handoff.yaml` already exists and the user asks for implementation.

Do not put formulas in report, UI, frontend, batch, or CSV/Excel input work.

## Source State Classification

Classify the material state first:

| State | Meaning | Route |
| --- | --- | --- |
| `no_materials` | User describes a desired calculator but provides no references | 01 -> 02 -> 03 |
| `insufficient_materials` | Some materials exist but formula, code basis, units, coefficients, examples, or branches are missing | 01 -> 02 -> 03 |
| `materials_available_untrusted` | Materials exist but authority/version/conflicts are unclear | 04, and maybe 01 -> 02 -> 03 |
| `local_evidence_library_available` | Source registry, source cards, raw/extracted references, and acquisition handoff exist | 04 -> 05 -> 06 -> 07 |
| `analysis_handoff_available` | Implementation handoff and coding gate exist | 08 -> 09 -> 10 -> 11 -> 13, plus 12 if interfaces needed |
| `codebase_available` | Existing implementation exists | classify bug/feature by layer, then route to 08-13 |

## Task Classification

| User intent | Route |
| --- | --- |
| Find资料, search references, gather standards/manuals/examples | 01 -> 02 -> 03 |
| Decide if provided资料足够 | 01 |
| Persist gathered references locally | 03 |
| Analyze standards, PDFs, Excel, reports, scripts, soil reports, or manual calculations | 04 -> 05 -> 06 -> 07 |
| Create Calculation Logic Blueprint | 05, with 04 first |
| Extract formulas, lookup tables, branch rules, units, assumptions | 06 |
| Prepare downstream coding guidance | 07 |
| Build or refactor engineering calculation software | 08 -> 09 -> 10 -> 11 -> 13, plus 12 if needed |
| Build typed models only | 09 |
| Build reusable formula/calculation module | 10, plus 13 |
| Build official calculation book runner | 11, plus 13 |
| Build report, review UI, CLI, API, or batch flow | 12, plus 13 smoke tests |
| Add tests, regression, traceability, hash, quality gates | 13 |
| Fix bug | Identify lowest correct layer, then route there |

## Gate Statuses

Use evidence gate statuses before analysis:

```text
evidence_no_go: cannot analyze or code because source basis is absent or unreliable
search_required: references must be found before analysis
partial_analysis_allowed: enough for outline, not enough for implementation handoff
analysis_allowed: enough to produce a traceable blueprint
```

Use coding gate statuses before implementation:

```text
no_go: do not code except scaffolding or non-formula architecture notes
prototype_allowed: code only with explicit assumptions and needs_confirmation markers
production_allowed: implementation can proceed with tests and traceability
```

## Required Checks Before Routing

Ask or infer:

```text
Is this reference acquisition, reference analysis, or implementation?
Are there any user-provided sources?
Is there a local evidence library?
Is there a valid acquisition_handoff.yaml?
Is there a valid implementation_handoff.yaml?
Does the task require current or jurisdiction-specific information?
Does the task involve formulas, lookup rules, branch logic, or units?
Does the task involve only presentation/report/UI/batch?
Are there source conflicts or missing design-code bases?
```

## Output

Provide a short routing decision:

```text
Task type:
Material state:
Required skill path:
Required input artifacts:
Expected output artifacts:
Gate status:
Immediate next action:
```


---

## skills/01-reference-adequacy-and-gap-assessment.skill.md

---
name: reference-adequacy-and-gap-assessment
description: Assess whether available engineering materials are sufficient for calculation logic extraction or software implementation. Use when no materials are provided, materials look incomplete, source authority is unclear, the user asks whether資料足够, or before deciding whether to search for additional references.
---

# Reference Adequacy and Gap Assessment

Use this skill before searching, analyzing, or coding when source sufficiency is unclear.

## Goal

Determine whether the available references are enough to support:

```text
conceptual outline
traceable calculation blueprint
implementation handoff
prototype code
production-grade calculation book software
```

## Do Not

Do not invent missing formulas, factors, units, load combinations, coefficients, or branch rules.

Do not treat a user description as a governing source unless it is explicitly a project assumption.

Do not send work to coding if the source basis is not sufficient for formulas, units, and checks.

## Inputs to Inspect

```text
user request
uploaded documents
local evidence library if present
references/source_registry.yaml if present
references/acquisition/acquisition_handoff.yaml if present
handoff/implementation_handoff.yaml if present
```

## Adequacy Dimensions

Evaluate coverage for:

```text
engineering domain and calculation object
governing code / standard / manual
jurisdiction and version/year
project-specific design basis
load cases and load combinations
geometry definitions
material / soil / hydraulic / structural parameters
formula sources
lookup tables / charts / interpolation rules
branch and applicability rules
unit and sign conventions
safety factors / partial factors / resistance factors
worked examples or regression references
reporting requirements
review / approval requirements
```

## Required Output Artifacts

```text
references/acquisition/reference_gap_assessment.md
references/acquisition/source_coverage_matrix.csv
references/acquisition/acquisition_plan.yaml
references/acquisition/open_reference_questions.md
```

## Coverage Matrix

Use this structure:

| Requirement ID | Requirement | Importance | Covered? | Current Source ID | Gap | Needed Source Type | Blocks Analysis? | Blocks Coding? |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

Importance values:

```text
critical
high
medium
low
```

Coverage values:

```text
covered
partially_covered
not_covered
conflicting
unknown
```

## Acquisition Plan

For each gap, define:

```text
gap_id
needed_information
why_it_matters
preferred_source_type
authority_priority
target_jurisdiction_or_standard
search_keywords
candidate_domains_or_publishers
minimum_acceptance_criteria
fallback_if_not_found
```

## Gate Decision

Return one evidence gate status:

```text
evidence_no_go
search_required
partial_analysis_allowed
analysis_allowed
```

Default decisions:

```text
No governing source and formulas needed -> search_required
No formulas, lookup rules, or units -> search_required
Enough for rough structure only -> partial_analysis_allowed
Enough for traceable blueprint but not tests -> analysis_allowed
```

If the user asks for implementation, also state whether the downstream coding gate is likely `no_go`, `prototype_allowed`, or `production_allowed`, but do not use coding gate statuses as the evidence gate result.

## Required Final Response

Provide:

```text
material sufficiency judgment
blocking gaps
non-blocking gaps
recommended sources to find
whether web/file-library/user upload search should be used
local artifacts to create
next skill path
```


---

## skills/02-reference-discovery-and-acquisition.skill.md

---
name: reference-discovery-and-acquisition
description: Discover, search, screen, and select candidate engineering references to fill gaps identified by the reference adequacy assessment. Use when materials are absent or insufficient and the model should find authoritative codes, manuals, examples, tables, public guidance, or project-relevant references before analysis.
---

# Reference Discovery and Acquisition

Use this skill after `01-reference-adequacy-and-gap-assessment` identifies gaps.

## Goal

Find candidate references that can support a traceable engineering calculation analysis.

Required transformation:

```text
acquisition_plan.yaml
-> search strategy
-> search log
-> candidate source list
-> authority and relevance screening
-> retrieval decisions
-> updated source coverage matrix
```

## Source Priority

Prefer sources in this order unless the user states a different authority hierarchy:

```text
1. project-specific contractual requirements and design basis
2. governing codes, standards, national annexes, client standards
3. official code commentaries or recognized agency design manuals
4. official technical guidance from ministries, agencies, institutes, or standards bodies
5. approved historical calculation books or verified legacy spreadsheets
6. published worked examples from reliable technical sources
7. textbooks, peer-reviewed papers, university notes, manufacturer technical manuals
8. independent hand calculations
9. internal design notes
10. unverified web pages, forums, AI summaries, or unknown sources
```

## Search Strategy

For each gap, define:

```text
search objective
required facts or tables
jurisdiction and language
preferred publisher or authority
essential keywords
alternative keywords
source acceptance criteria
rejection criteria
```

## Web Search Tool Requirement

When an internet search or browser/search tool is available, use it actively for this stage. Do not rely only on model memory, embedded knowledge, or the user's short description when references are absent, incomplete, stale, jurisdiction-specific, or version-sensitive.

For each critical or high-importance gap:

```text
run targeted web searches
try multiple query formulations
prefer official domains, standards bodies, agencies, ministries, publishers, or recognized technical institutions
open and inspect promising primary sources when the tool supports it
cross-check candidate authority, version/year, jurisdiction, and applicability
record every meaningful search in search_log.csv
record selected and rejected candidates in candidate_sources.csv
record retrieval decisions before persistence
```

If the internet search tool is unavailable, explicitly state that limitation, use only local/user-provided materials, and keep the evidence gate at `search_required` or `partial_analysis_allowed` unless the local evidence is already sufficient.

Prefer targeted queries such as:

```text
<engineering object> <check> design manual pdf official
<standard/code name> <clause/table/equation> <topic>
<agency/ministry> <topic> design guide
<calculation type> worked example <code/version>
```

Use iterative search. After finding a candidate source, search again by its title, publisher, clause/table/equation identifiers, version/year, and related official manuals to find better primary sources or worked examples.

## Screening Criteria

For each candidate source, record:

```text
candidate_id
title
publisher / author
source_type
url_or_location
access_date
version_or_date
jurisdiction
relevance_score
authority_level
coverage_tags
gaps_covered
limitations
license_or_access_notes
recommended_action
```

Recommended actions:

```text
persist_raw
persist_source_card_only
use_for_background_only
reject
needs_user_access
needs_purchase_or_license
needs_confirmation
```

## Copyright and Access Rules

Do not bypass paywalls, login requirements, copy protection, subscription systems, or licensing restrictions.

Do not save full copyrighted standards, textbooks, or papers unless the user provides them or explicitly confirms authorization.

For restricted sources, save only:

```text
bibliographic information
source card
short compliant excerpt if needed
clause/table/equation identifiers
summary of relevance
access instructions
```

## Required Output Artifacts

```text
references/acquisition/search_log.csv
references/acquisition/candidate_sources.csv
references/acquisition/retrieval_decisions.csv
references/acquisition/source_coverage_matrix.csv
references/acquisition/acquisition_notes.md
```

## Search Log Columns

```text
search_id,gap_id,query,tool_or_location,date,results_reviewed,candidates_selected,notes
```

## Candidate Source Columns

```text
candidate_id,title,publisher,source_type,version_or_date,jurisdiction,url_or_location,access_date,authority_level,relevance_score,gaps_covered,recommended_action,limitations,license_or_access_notes
```

## Retrieval Decision Columns

```text
decision_id,candidate_id,decision,reason,local_target,raw_allowed,source_card_required,extraction_required,follow_up
```

## Required Final Response

Provide:

```text
searches performed
best sources found
sources rejected and why
which gaps are now covered
which gaps remain
what will be persisted locally
whether analysis can proceed
```


---

## skills/03-reference-persistence-and-local-library.skill.md

---
name: reference-persistence-and-local-library
description: Persist acquired engineering references, source cards, metadata, search logs, extracted notes, coverage matrices, and acquisition handoff files into a local evidence library. Use after reference discovery or whenever found資料 must be made durable and traceable for downstream analysis.
---

# Reference Persistence and Local Library

Use this skill after candidate sources have been selected or when the user asks to save found references locally.

## Goal

Convert ephemeral search results and user-provided files into a stable local evidence library.

Required transformation:

```text
candidate_sources.csv + retrieval_decisions.csv + acquired files
-> stable source IDs
-> raw files where allowed
-> source cards where raw persistence is not allowed
-> extracted notes / text where appropriate
-> source_registry.yaml
-> evidence_library_manifest.yaml
-> acquisition_handoff.yaml
```

## Directory Contract

Use this structure:

```text
references/
  acquisition/
    reference_gap_assessment.md
    acquisition_plan.yaml
    search_log.csv
    candidate_sources.csv
    retrieval_decisions.csv
    source_coverage_matrix.csv
    acquisition_notes.md
    acquisition_handoff.yaml
  raw/
    S01_<short_source_name>.pdf
    S02_<short_source_name>.xlsx
  extracted/
    S01_text.md
    S01_tables/
    S02_workbook_formula_map.md
    notes/
      S01_source_notes.md
  source_cards/
    S01_source_card.md
    S02_source_card.md
  snapshots/
    README.md
  source_registry.yaml
  evidence_library_manifest.yaml
```

## Stable Source IDs

Assign source IDs such as:

```text
S01, S02, S03
CODE-01
MANUAL-01
EXAMPLE-01
EXCEL-01
REPORT-01
```

Do not change existing IDs once downstream analysis has started.

## Raw Persistence Rules

Save raw files only when:

```text
the user uploaded the file
the user explicitly authorized saving it
it is openly downloadable and permitted for local use
it is public-domain or permissively licensed
```

If raw saving is not allowed or uncertain, create a source card instead.

## Source Card Contract

Every source should have a source card, even when raw is saved.

Each source card should include:

```text
source_id
title
publisher / author
source_type
version_or_date
jurisdiction
url_or_location
access_date
raw_file_path if any
extracted_file_path if any
authority_level
coverage_tags
relevance_to_calculation
key clauses / tables / equations / pages
short compliant excerpts if necessary
paraphrased notes
limitations
license_or_access_notes
recommended downstream use
```

## Extraction Rules

When extracting text, tables, or workbook logic:

```text
record extraction date
record extraction tool or method if relevant
record page/sheet/range references
record uncertainty and OCR risks
preserve table identifiers
avoid long copyrighted passages
prefer structured summaries and identifiers
```

For spreadsheets, record:

```text
workbook name
sheet names
named ranges
visible/hidden sheets
formula map if available
input cells
output cells
important intermediate cells
external links/macros if present
```

## Hash and Manifest

For every local raw or extracted file, record where practical:

```text
path
sha256
created_at
source_id
file_role
notes
```

## Acquisition Handoff

Create:

```text
references/acquisition/acquisition_handoff.yaml
```

It should include:

```text
project_or_calculation_name
acquisition_status
source_ids
coverage_summary
remaining_gaps
recommended_analysis_path
sources_to_use_as_governing
sources_to_use_as_examples
sources_to_use_as_background
copyright_or_access_limitations
```

## Required Final Response

Provide:

```text
local evidence library summary
files persisted
source cards created
coverage status
remaining gaps
next skill path: 04-source-intake-and-authority or back to 02-reference-discovery-and-acquisition
```


---

## skills/04-source-intake-and-authority.skill.md

---
name: source-intake-and-authority
description: Intake engineering source materials or a local evidence library, assign stable source IDs, classify authority, record source conflicts, and prepare source inventory for calculation logic analysis. Use after reference persistence or when user-provided materials are already available.
---

# Source Intake and Authority

Use this skill as the first analysis-stage skill after evidence acquisition or direct user upload.

## Goal

Turn references into a reliable source inventory that downstream logic extraction can cite.

## Inputs

Prefer reading these artifacts if available:

```text
references/source_registry.yaml
references/evidence_library_manifest.yaml
references/acquisition/acquisition_handoff.yaml
references/raw/
references/extracted/
references/source_cards/
```

If no local evidence library exists, use uploaded materials directly and create equivalent source inventory artifacts.

## Source Inventory Contract

Assign or verify stable source IDs:

```text
S01, S02, S03
CODE-01
MANUAL-01
EXCEL-01
REPORT-01
NOTE-01
```

For each source, record:

```text
source_id
source_name
source_type
version_or_date
jurisdiction_or_project
role_in_analysis
priority
authority_level
reliability_notes
scope_of_applicability
known_limitations
local_path_or_source_card
```

## Authority Hierarchy

Default priority order:

```text
1. project-specific contractual requirement
2. governing design code or standard
3. official code commentary or nationally recognized design manual
4. project-approved calculation basis
5. published worked example from reliable source
6. verified historical calculation report
7. legacy spreadsheet
8. internal design note
9. engineering assumption
10. unknown source or unverified material
```

If the user specifies a different order, follow it.

## Conflict Inventory

When sources conflict, record:

```text
conflict_id
affected formula, coefficient, branch, or assumption
source A method
source B method
engineering consequence
recommended resolution
whether it blocks analysis or coding
```

## Required Output Artifacts

```text
analysis/01_source_inventory/source_inventory.yaml
analysis/01_source_inventory/source_authority_table.csv
analysis/01_source_inventory/source_conflicts.csv
analysis/01_source_inventory/source_intake_notes.md
```

## Quality Gate

Before passing to logic blueprint, verify:

```text
sources are identified
source IDs are stable
version/year and jurisdiction are captured where available
authority ranking is explicit
project-specific sources are distinguished from generic sources
source cards or local paths are available
conflicts and gaps are visible
```

## Required Final Response

Provide:

```text
source inventory summary
authority ranking
conflicts found
gaps remaining
whether logic blueprint can proceed
```


---

## skills/05-engineering-logic-blueprint.skill.md

---
name: engineering-logic-blueprint
description: Transform source-inventoried engineering references into a normalized Calculation Logic Blueprint with concept map, calculation nodes, input/intermediate/output inventories, diagrams, module candidates, validation needs, and traceability anchors.
---

# Engineering Logic Blueprint

Use this skill after source intake and authority classification.

## Core Principle

Do not treat Mermaid as the final product. Mermaid diagrams are views of the deeper calculation logic model.

The core deliverable is:

```text
analysis/02_logic_blueprint/calculation_blueprint.md
```

## Required Transformation

```text
source inventory
-> engineering concept map
-> calculation stages
-> normalized calculation node model
-> input / intermediate / output inventories
-> Mermaid views
-> software module candidates
```

## Engineering Concept Layer

Extract concepts such as:

```text
calculation object
design situation
limit state
load case
load combination
material model
soil model
water or environmental condition
geometry model
boundary condition
design method
checking method
safety format
failure mode
serviceability criterion
ultimate criterion
special condition
governing result
report output
```

## Normalized Node Model

Each node should include:

```text
node_id
node_type
node_name
engineering_meaning
inputs
outputs
units
formula_or_method
source_reference
branch_condition
applicability
assumptions
module_candidate
result_visibility
report_visibility
test_requirement
risk_level
```

Allowed node types:

```text
Input
Validate
Normalize
SelectMethod
Lookup
Compute
Branch
Check
Aggregate
Output
Report
Warning
Error
Redesign
```

## Required Output Artifacts

```text
analysis/02_logic_blueprint/calculation_blueprint.md
analysis/02_logic_blueprint/concept_map.csv
analysis/02_logic_blueprint/calculation_nodes.csv
analysis/02_logic_blueprint/input_inventory.csv
analysis/02_logic_blueprint/intermediate_inventory.csv
analysis/02_logic_blueprint/output_inventory.csv
analysis/04_diagrams/global_flowchart.mmd
analysis/04_diagrams/data_flow.mmd
analysis/04_diagrams/branch_logic.mmd
analysis/04_diagrams/module_dependency.mmd
```

## Software Mapping Orientation

Every important node should map to at least one future artifact:

```text
input model field
validator
normalizer
lookup library
calculation module function
book runner step
CheckResult
GoverningSummary
BookResult field
ReportContext field
test target
```

## Required Final Response

Provide:

```text
scope and purpose
concept map summary
calculation logic summary
node inventory summary
input/intermediate/output inventory summary
Mermaid diagrams
module candidates
open issues for detailed formula extraction
```


---

## skills/06-formula-lookup-branch-extraction.skill.md

---
name: formula-lookup-branch-extraction
description: Extract and normalize engineering formulas, design methods, lookup tables, charts, interpolation rules, branch conditions, unit/sign conventions, assumptions, applicability limits, warnings, errors, and test requirements from inventoried sources and the Calculation Logic Blueprint.
---

# Formula, Lookup, and Branch Extraction

Use this skill after the high-level Calculation Logic Blueprint exists.

## Goal

Freeze the high-risk calculation details that software implementation must not reinterpret later.

## Required Extraction Targets

```text
formulas and named methods
coefficients and factors
lookup tables and charts
interpolation and out-of-range rules
branch conditions and method selection rules
applicability limits
unit and sign conventions
safety formats
status rules
warnings and errors
assumptions and engineering judgment
```

## Formula Inventory

For each formula/method record:

```text
formula_id
name
purpose
inputs
outputs
units
source_reference
applicability
branch_dependencies
lookup_dependencies
implementation_note
test_requirement
risk_level
```

Classify source type:

```text
code-defined
manual-defined
spreadsheet-derived
empirical
project-specific
engineering assumption
needs confirmation
```

## Lookup Inventory

For each table/chart/nomogram record:

```text
lookup_id
name
inputs
outputs
source_reference
interpolation_rule
out_of_range_behavior
implementation_note
test_requirement
risk_level
```

Lookup behaviors:

```text
exact lookup
range lookup
linear interpolation
bilinear interpolation
log interpolation
nearest conservative value
chart digitization
manual selection
not specified / needs confirmation
```

## Branch Inventory

For each decision record:

```text
branch_id
condition
engineering_meaning
source_reference
path_if_true
path_if_false
not_applicable_behavior
program_representation
required_tests
risk_level
```

## Unit and Sign Rules

Record:

```text
input units
internal units
output units
angle units
force/moment sign conventions
coordinate directions
pressure/stress conventions
settlement/displacement sign conventions
```

Mark unclear items as `needs confirmation`.

## Required Output Artifacts

```text
analysis/03_logic_details/formula_inventory.csv
analysis/03_logic_details/lookup_inventory.csv
analysis/03_logic_details/branch_inventory.csv
analysis/03_logic_details/applicability_limits.csv
analysis/03_logic_details/unit_and_sign_conventions.md
analysis/03_logic_details/assumption_register.csv
analysis/05_risks_and_questions/risk_register.csv
analysis/05_risks_and_questions/open_questions.csv
```

## Required Final Response

Provide:

```text
formula inventory summary
lookup and interpolation summary
branch logic summary
unit and sign convention summary
applicability limits
high-risk uncertainties
test requirements
whether implementation handoff can proceed
```


---

## skills/07-implementation-handoff-contract.skill.md

---
name: implementation-handoff-contract
description: Convert the source-backed Calculation Logic Blueprint, formula/lookup/branch inventories, validation rules, risk register, and test requirements into a formal Implementation Handoff Contract for downstream engineering calculation book software.
---

# Implementation Handoff Contract

Use this skill after the analysis artifacts are complete enough to guide implementation.

## Goal

Create a hard interface between reference analysis and coding.

The downstream implementation skill should not need to reinterpret raw references to understand the intended software architecture.

## Required Inputs

```text
references/acquisition/acquisition_handoff.yaml
analysis/01_source_inventory/source_inventory.yaml
analysis/02_logic_blueprint/calculation_blueprint.md
analysis/02_logic_blueprint/calculation_nodes.csv
analysis/03_logic_details/formula_inventory.csv
analysis/03_logic_details/lookup_inventory.csv
analysis/03_logic_details/branch_inventory.csv
analysis/03_logic_details/applicability_limits.csv
analysis/03_logic_details/unit_and_sign_conventions.md
analysis/05_risks_and_questions/risk_register.csv
analysis/05_risks_and_questions/open_questions.csv
```

## Required Outputs

```text
handoff/implementation_handoff.yaml
handoff/implementation_handoff.md
handoff/artifact_index.yaml
handoff/coding_go_no_go.md
handoff/unresolved_items_before_coding.md
```

## Contract Sections

The YAML contract should include:

```text
handoff_id
book_name
version
status
source_basis
evidence_library_status
calculation_scope
input_model_groups
result_model_groups
runner_sequence
module_candidates
formula_inventory_refs
lookup_inventory_refs
branch_inventory_refs
validation_rules
test_requirements
report_sections
traceability_requirements
open_questions
coding_gate
```

## Coding Gate

Use one of:

```text
no_go
prototype_allowed
production_allowed
```

Default gate rules:

```text
critical formula missing -> no_go
critical lookup rule missing -> no_go
governing code basis missing -> no_go
unit system unclear -> no_go
major source conflict unresolved -> no_go
missing regression references but formulas are clear -> prototype_allowed
all critical formulas, units, branches, and tests defined -> production_allowed
```

## Required Final Response

Provide:

```text
handoff status
what implementation may start
what implementation must not start
required modules
runner sequence
model groups
report sections
test requirements
remaining blockers
next skill path
```


---

## skills/08-calculation-book-architecture.skill.md

---
name: calculation-book-architecture
description: Design the project and package architecture for a reusable engineering calculation book system from a validated implementation handoff, including feature classification, dependency rules, package layout, and file placement.
---

# Calculation Book Architecture

Use this skill as the first implementation-stage skill.

## Goal

Design the software architecture before writing formulas or interfaces.

## Required Inputs

```text
handoff/implementation_handoff.yaml
handoff/coding_go_no_go.md
```

If the gate is `no_go`, produce only scaffold or architecture notes; do not implement production formulas.

## Dependency Direction

```text
presentation / report / review / batch / API
  -> books
    -> libraries
      -> core
```

## Feature Classification

Before implementation, classify every feature:

| Feature | Layer | Existing module? | New module needed? | Reusable? | Location | Notes |
| --- | --- | --- | --- | --- | --- | --- |

Layers:

```text
core platform
reusable engineering library
calculation book runner
report context / renderer
review/frontend
batch / CLI / API
verification
```

## Default Project Structure

```text
engineering_calc_project/
  references/
  analysis/
  handoff/
  data/
    input/
    imported/
      reports/
      references/
    staging/
    normalized/
      cases/
    packages/
  implementation/
  src/<pkg>/
    core/
    libraries/
    books/<book_name>/
    interfaces/
    report/
  webapp/
  apps/
    review/
  outputs/
    results_json/
    reports_html/
    reports_pdf/
    reports_docx/
    upload_packages/
    logs/
  tests/
  verification/
```

## Required Output Artifacts

```text
implementation/00_architecture/project_structure.md
implementation/00_architecture/feature_classification.csv
implementation/00_architecture/dependency_rules.md
implementation/00_architecture/package_layout.md
```

## Required Final Response

Provide:

```text
architecture decision
feature classification
project tree
layer placement
forbidden dependencies
implementation order
```


---

## skills/09-core-and-data-models.skill.md

---
name: core-and-data-models
description: Define core platform utilities and typed data models for engineering calculation books, including statuses, errors, units, validators, metadata, hashing, serialization, BookInput, BookResult, module inputs/results, formula traces, and report context models.
---

# Core and Data Models

Use this skill after the calculation book architecture is defined.

## Goal

Create stable typed contracts before implementing calculation modules.

## Core Platform Responsibilities

```text
status enums
CheckResult
FormulaTrace
RunMetadata
errors and warnings
validators
unit helpers
hashing
serialization
result path utilities
```

Core must not contain:

```text
domain formulas
book-specific runner logic
UI code
report rendering
batch workflow
```

## Data Models

Recommended public models:

```text
ProjectInfo
DesignBasis
DesignOptions
Assumption
BookInput
BookResult
ModuleInput
ModuleResult
CheckResult
GoverningSummary
ReportContext
```

Every public result should expose where applicable:

```text
status
demand
capacity
utilization
limit
unit
warnings
errors
intermediate_values
formula_traces
code_references
governing_reason
```

## Unit Contract

Define one internal unit system:

```text
length: m
force: kN
stress/pressure: kPa
unit_weight: kN/m3
moment: kNm
settlement/displacement: mm
angle_input: degree
angle_internal: radian
```

Convert units only at input/output boundaries.

## Required Output Artifacts

```text
implementation/01_core_models/core_model_plan.md
implementation/01_core_models/data_model_spec.md
implementation/01_core_models/status_semantics.md
implementation/01_core_models/unit_system.md
src/<pkg>/core/
src/<pkg>/books/<book_name>/book_models.py
```

## Required Final Response

Provide:

```text
core model plan
data model specification
status semantics
unit policy
result path plan
serialization and hash plan
```


---

## skills/10-reusable-calculation-modules.skill.md

---
name: reusable-calculation-modules
description: Implement or design reusable engineering calculation modules from the implementation handoff, with typed inputs/outputs, formula traces, lookup behavior, warnings/errors, no file I/O, no UI/report dependency, and unit/regression tests.
---

# Reusable Calculation Modules

Use this skill to implement domain formulas and lookup logic.

## Goal

Build reusable, independently testable engineering modules.

## Module Rules

Every reusable module must:

```text
have typed input
have typed output
expose one stable public function
avoid hidden global state
avoid file I/O
avoid UI dependencies
avoid report dependencies
avoid batch-specific behavior
validate module-specific assumptions
return intermediate values needed for audit
return warnings instead of silently clipping values
be independently testable
```

## Forbidden

Do not read CSV, render reports, access UI state, write batch summaries, or call a book runner from a reusable formula module.

## Example Interface

```python
def check_bearing_capacity(
    input_data: BearingInput,
    options: BearingOptions,
) -> BearingResult:
    ...
```

## Required Output Artifacts

```text
implementation/02_modules/module_interface_spec.md
implementation/02_modules/formula_trace_spec.md
implementation/02_modules/lookup_module_spec.md
src/<pkg>/libraries/<domain>/<category>/
tests/unit/test_<module>.py
tests/regression/test_<module>_<reference>.py
```

## Required Final Response

Provide:

```text
module location
input/options/result models
public function signatures
formula and source references
intermediate values returned
warning/error behavior
unit tests
regression tests if references exist
example usage
```


---

## skills/11-book-runner-and-governing-summary.skill.md

---
name: book-runner-and-governing-summary
description: Build the official engineering calculation book runner, orchestration sequence, shared state preparation, module calls, warnings/errors aggregation, BookResult, governing summary, result paths, and integration tests.
---

# Book Runner and Governing Summary

Use this skill after core models and reusable modules exist or have been designed.

## Goal

Create exactly one official calculation path for a formal engineering calculation book.

## Official Runner

Every calculation book must define:

```python
def run_book(book_input: BookInput) -> BookResult:
    ...
```

The runner must:

```text
validate book-level input
prepare shared state
apply design options and assumptions
call reusable calculation modules
collect module results
preserve warnings and errors
summarize governing checks
create run metadata
return structured BookResult
```

The runner must not:

```text
render reports
read raw CSV files
manage UI state
write batch summaries
contain report-template logic
```

## Governing Summary

Expose:

```text
overall_status
governing_check_id
governing_check_name
governing_utilization_or_margin
governing_limit
critical_load_case or combination
controlling location/member/foundation if applicable
warnings_count
errors_count
```

## Required Output Artifacts

```text
implementation/03_book_runner/runner_sequence.md
implementation/03_book_runner/governing_summary_spec.md
implementation/03_book_runner/result_path_registry.csv
src/<pkg>/books/<book_name>/book_runner.py
src/<pkg>/books/<book_name>/governing.py
tests/integration/test_<book_name>_runner.py
```

## Required Final Response

Provide:

```text
runner sequence
module call order
shared state plan
BookResult structure
governing summary logic
warnings/errors behavior
integration test
```


---

## skills/12-report-review-batch-interfaces.skill.md

---
name: report-review-batch-interfaces
description: Build polished, review-readable report, frontend, Marimo review, CLI, API, import/export, upload-package, and batch interfaces over a trusted engineering calculation book runner and BookResult. Use when creating production web UIs, module review notebooks, data/report import flows, uploadable calculation packages, report previews, or batch summaries, while keeping formulas and independent pass/fail logic out of presentation layers.
---

# Report, Review, Batch, and Interface Layer

Use this skill after `run_book()` and `BookResult` exist or are specified.

## Goal

Create user-facing, reviewer-facing, and batch-facing interfaces that consume `BookInput`, `BookResult`, or `ReportContext` without implementing engineering calculations.

Interfaces must be:

```text
thin over run_book()
review-readable
consistent across projects
pleasant enough for daily engineering use
able to import/export managed data packages
able to preview or import prior reports for review and comparison
```

This skill is domain-neutral about engineering discipline, but not layout-neutral. Use the unified operational layout below unless the user or existing app gives a stronger local design system.

## Interface Families

Select one or more interface families and record the choice.

```text
production frontend: polished browser UI for daily input, calculation, report preview, import/export, and batch operation
Marimo review app: reactive reviewer page for module-by-module inspection, editing, trace checks, and what-if exploration
report renderer: HTML/PDF/DOCX/XLSX/JSON generated from ReportContext
CLI/API/batch: automation layer for repeatable runs and package processing
```

Use Marimo for interactive engineering review when a Python-native reactive page is useful. Author with `marimo edit`; publish a read-only review app with `marimo run`. Marimo pages may use file upload, file browser, and data editor widgets for managed review workflows, but they must still call trusted modules or `run_book()`.

## Unified Frontend Layout

Use a stable layout so every calculation book is easy to reproduce and manage:

```text
top bar:
  book/project title, case selector, report status, import package, export package, report preview, language switch if needed

left input panel:
  collapsible input cards grouped by BookInput model groups
  compact labels, units, required markers, validation feedback
  sticky run/validate/save controls at the bottom

right review workbench:
  governing summary first
  warnings/errors/unresolved assumptions near the top
  result cards ordered by engineering review sequence
  tables, charts, source traces, formula traces, and report preview links

modal or drawer:
  report preview, imported report preview, source trace, formula trace, data package validation, input/result diff

status strip:
  input hash, result hash, runner version, report template version, data package id, timestamp
```

This layout mirrors a repeatable engineering dashboard pattern: inputs stay on the left, conclusions and audit evidence stay on the right, and import/export/report actions stay in a predictable top-level location.

## Review Readability Contract

A review UI is not complete unless a checker can answer these questions quickly:

```text
What is the overall result?
Which check governs?
What input and source basis produced it?
What warnings, errors, or assumptions block final status?
Which formulas, lookup tables, and branch decisions were used?
What changed from the saved final input, previous result, or imported report?
Can the reviewer export the exact input/result package that generated this view?
```

Required readability rules:

```text
show conclusion before detail
show source basis and design code/version near the top
never hide warnings, errors, unresolved assumptions, or prototype status
use tables for comparable checks and cards only for distinct result groups
make every editable field map to a BookInput path
make every displayed result map to a BookResult or ReportContext path
show units with fields and values
provide trace expansion for critical formulas, lookups, and branch decisions
mark exploratory Marimo edits as draft/prototype until saved and verified
```

## Report Production Decision Protocol

Before designing or rendering a report, decide and record:

```text
report purpose
intended audience
review depth
report status
required output formats
governing source basis
required inputs and saved result source
required traceability metadata
required report sections derived from user needs and BookResult
renderer choice and reason
frontend layout choice and reason
Marimo review app choice if used
data package import/export requirements
verification method
known limitations
```

The agent may choose an appropriate rendering stack, but must preserve the unified frontend layout for operational UIs unless an existing product design overrides it. The choice must be justified by the requested deliverable, environment, review requirements, and data already present in `BookResult` or `ReportContext`.

## Report Status

Use explicit report status labels:

```text
draft
review
final
superseded
prototype
not_for_construction
```

Do not label a report `final` or production-ready unless the coding gate allows production work, the source basis is sufficient, the report is generated from saved final input or a trusted saved `BookResult`, and verification has passed.

## Allowed Responsibilities

Interfaces may:

```text
parse CSV / JSON / YAML / XLSX / ZIP / API input
import prior reports as review artifacts
map fields to BookInput
validate input before runner call
call run_book()
call trusted reusable modules for module-level Marimo review
display inputs and results
build ReportContext from BookResult
render reports
run batch cases
save normalized input JSON
save BookResult JSON
write batch summaries
write data package manifests and hashes
export uploadable calculation packages
```

## Forbidden Responsibilities

Interfaces must not:

```text
implement engineering formulas
perform unit conversion for official calculations except at input/output boundaries
calculate capacity, settlement, reinforcement, hydraulic results, or load combinations independently
recalculate pass/fail status
hide warnings/errors
treat imported reports as calculation truth unless converted through a source-backed BookInput/BookResult path
overwrite final inputs or results from exploratory UI edits without an explicit save, hash, and verification step
```

## Import, Report Import, and Upload Packages

Use a managed data area:

```text
data/input/                  user-provided source inputs
data/imported/reports/       prior HTML/PDF/DOCX/XLSX/context reports used for review or comparison
data/imported/references/    project-provided reference files allowed by access rules
data/staging/                uploaded but not yet accepted files
data/normalized/cases/       normalized BookInput JSON per case
data/packages/               unpacked upload/export packages with manifest
outputs/results_json/        trusted BookResult JSON
outputs/reports_html/        generated HTML reports
outputs/reports_pdf/         generated PDF reports
outputs/reports_docx/        generated DOCX reports
outputs/upload_packages/     ZIP or folder packages ready to share/upload
```

Upload package flow:

```text
upload ZIP or files
-> store in data/staging/
-> compute hashes and inspect manifest
-> classify inputs, reports, references, and outputs
-> normalize accepted inputs into BookInput JSON
-> show validation and diff summary
-> run_book only after user selects case or batch
-> save BookResult and export package
```

Imported reports are review artifacts. They may support visual comparison, regression evidence, or client review, but must not inject formulas or override official status.

## Marimo Module Review Pattern

Create Marimo apps under:

```text
apps/review/<book_name>_review.py
apps/review/modules/<module_name>_review.py
```

Each Marimo review page should include:

```text
case/package loader
module selector
editable module input fields or data editor
run selected module or full run_book()
governing result and warnings/errors
input/result diff from saved final or imported reference
formula traces and source references
review notes and decision
save draft input, module review log, or export package
```

Marimo review pages may use sliders and editable tables for what-if exploration. Label all such results as `draft`, `review`, or `prototype` until the exact input is saved, re-run through the official path, and verified.

## Report Flow

```text
final_input.json
-> run_book()
-> BookResult
-> save BookResult JSON
-> build_report_context()
-> template/render function
-> report
-> optional upload package
```

## Report Context Contract

Build `ReportContext` as a presentation contract over computed results. It should expose enough structured data for the chosen renderer without forcing a fixed report layout.

Include when applicable:

```text
report production decision
project and case metadata
report status and output target
design basis and source references
input summary
assumptions and limitations
module summaries
governing summary
checks and result paths
intermediate values selected for audit
warnings and errors
formula traces or source trace references
imported report comparison metadata
data package metadata
appendix data
traceability metadata
```

Report sections should be derived from:

```text
user-requested deliverable
calculation scope
BookResult result paths
required review questions
source-backed reporting requirements
warnings, errors, and unresolved assumptions
```

Templates may contain value references, loops, conditionals, formatting filters, section visibility logic, unit display formatting, and cross-references. Templates must not contain engineering formulas, independent unit conversion for official calculations, optimization logic, load-combination generation, or independent pass/fail logic.

## Batch Flow

```text
read batch_control.csv or uploaded package manifest
-> load case input
-> validate
-> run_book()
-> save normalized input JSON
-> save BookResult JSON
-> render report if requested
-> write batch summary CSV/HTML
-> export upload package if requested
-> write logs
```

Batch workflows must preserve per-case report status, warnings, errors, result paths, hashes, and traceability metadata. A batch summary may summarize outcomes, but it must not recalculate or override case-level engineering status.

## Production Report Minimum

A production report workflow must have:

```text
recorded report production decision
explicit report status
saved final input or trusted saved BookResult
clear source basis and limitations
structured ReportContext
unified UI layout spec when frontend exists
Marimo review spec when review notebooks exist
data package manifest when import/export packages exist
renderer or export path selected for the requested deliverable
proof that templates/UI/Marimo/batch do not calculate
warnings and errors preserved in the report output
traceability metadata preserved
smoke test for each report renderer or export path
documented run command
```

If any item is missing, state the report as draft, review, prototype, or blocked according to the gap. Do not silently downgrade production requirements.

## Required Output Artifacts

```text
implementation/04_interfaces/input_mapping_spec.md
implementation/04_interfaces/ui_layout_spec.md
implementation/04_interfaces/import_export_contract.md
implementation/04_interfaces/marimo_review_spec.md
implementation/04_interfaces/report_context_spec.md
implementation/04_interfaces/review_readability_checklist.md
implementation/04_interfaces/review_schema.csv
implementation/04_interfaces/frontend_fields.csv
implementation/04_interfaces/module_review_log.csv
implementation/04_interfaces/data_package_manifest.yaml
implementation/04_interfaces/batch_flow.md
src/<pkg>/books/<book_name>/input_mapping.py
src/<pkg>/books/<book_name>/report_context.py
src/<pkg>/interfaces/
src/<pkg>/report/
webapp/ or src/<pkg>/interfaces/webapp/
apps/review/ when Marimo review is requested
tests/smoke/test_<report_or_interface>.py
```

## Required Final Response

Provide:

```text
which BookInput or BookResult is consumed
which runner is called
unified UI layout summary
field mapping or display schema
import/export and upload package flow
Marimo review pages and module editing scope if used
report context fields
template or UI flow
report production decision and status
proof that formulas are not in template/UI/Marimo/batch
smoke test
run command
```


---

## skills/13-verification-regression-traceability.skill.md

---
name: verification-regression-traceability
description: Design and implement verification, regression tests, tolerance policy, formula trace checks, input/result hashes, report smoke tests, Marimo review smoke tests, upload package checks, batch summary checks, and acceptance gates for engineering calculation book systems.
---

# Verification, Regression, and Traceability

Use this skill throughout implementation and before release.

## Goal

Verify formulas, lookups, branches, book orchestration, report context, interfaces, and traceability.

## Test Categories

```text
unit tests for isolated formulas
lookup tests for tables and interpolation
branch tests for method selection
edge case tests for boundary conditions
invalid input tests
regression tests against references
integration tests for complete run_book workflows
report smoke tests
Marimo review smoke tests
upload/import package manifest and hash tests
batch smoke tests
serialization and hash tests
```

## Regression Reference Priority

```text
design code examples
published design manual examples
approved historical reports
verified legacy spreadsheets
independent hand calculations
synthetic edge cases
```

## Traceability Metadata

For production results, include where feasible:

```text
book_type
book_name
case_id
project_id
design_code and version
run_timestamp
package version
input_hash
result_hash
python_version
git_commit if available
formula registry version if used
runner version
report template version
```

## Required Output Artifacts

```text
verification/test_matrix.csv
verification/regression_references.md
verification/tolerance_policy.md
verification/acceptance_checklist.md
tests/unit/
tests/regression/
tests/integration/
tests/smoke/
```

## Acceptance Checklist

Verify:

```text
source basis is recorded
features are classified into layers
formulas live only in reusable calculation modules
book runner is the official calculation entry point
CSV/JSON/frontend/API inputs map to the same BookInput
unit conversions happen only at input/output boundaries
templates do not calculate
frontend/review does not calculate
Marimo review pages do not calculate outside trusted modules or run_book
upload packages preserve manifests, hashes, normalized inputs, and trusted results
batch does not calculate independently
units are explicit
result objects include intermediate values
warnings and errors are preserved
status semantics are defined
governing summary exists
tests cover reusable modules
book integration test exists
report rendering smoke test exists when reports exist
traceability metadata exists for production outputs
run commands are documented
```

## Required Final Response

Provide:

```text
test matrix summary
regression references
tolerance policy
traceability plan
acceptance result
remaining verification risks
```


---

## templates/acquisition/acquisition_handoff.yaml

acquisition_handoff_id: ACQ-HANDOFF-001
project_or_calculation_name: example
created_at: 2026-06-16
status: analysis_allowed # evidence_no_go | search_required | partial_analysis_allowed | analysis_allowed

source_registry: references/source_registry.yaml
evidence_library_manifest: references/evidence_library_manifest.yaml
coverage_matrix: references/acquisition/source_coverage_matrix.csv

source_ids:
  - S01

coverage_summary:
  critical_requirements_total: 0
  critical_requirements_covered: 0
  partially_covered: []
  remaining_gaps: []

governing_sources:
  - source_id: S01
    role: governing_or_primary_reference
    priority: 1

example_or_regression_sources: []
background_sources: []

copyright_or_access_limitations:
  - source_id: S01
    limitation: source card only unless authorized

recommended_next_skill_path:
  - 04-source-intake-and-authority
  - 05-engineering-logic-blueprint
  - 06-formula-lookup-branch-extraction
  - 07-implementation-handoff-contract


---

## templates/acquisition/acquisition_notes.md

# Acquisition Notes

## Search Scope

Record jurisdictions, standards, source types, languages, and date/version constraints used during discovery.

## Web Search Tool Use

Record which internet search, browser, database, library, or local search tools were used. If no internet search tool was available, state that explicitly and identify what evidence limitations remain.

## Screening Notes

Summarize why selected candidates were accepted and why rejected candidates were not suitable.

## Access And Copyright Notes

Record access limits, paywall/license constraints, user authorization, and source-card-only decisions.

## Remaining Work

List gaps that require another search pass or user-provided material.


---

## templates/acquisition/acquisition_plan.yaml

plan_id: ACQ-PLAN-001
project_or_calculation_name: example
created_at: 2026-06-16
status: draft

gaps:
  - gap_id: GAP-001
    needed_information: governing design method and formulas
    why_it_matters: blocks source-backed calculation implementation
    preferred_source_type: governing code or official design manual
    authority_priority: high
    target_jurisdiction_or_standard: to_be_defined
    search_keywords:
      - example calculation design manual official pdf
    candidate_domains_or_publishers: []
    minimum_acceptance_criteria:
      - source has publisher, date/version, and usable formula or method reference
    fallback_if_not_found: ask user to provide governing source or allow prototype only


---

## templates/acquisition/candidate_sources.csv

candidate_id,title,publisher,source_type,version_or_date,jurisdiction,url_or_location,access_date,authority_level,relevance_score,gaps_covered,recommended_action,limitations,license_or_access_notes


---

## templates/acquisition/evidence_library_manifest.yaml

manifest_id: EVIDENCE-001
created_at: 2026-06-16
status: draft

files:
  - source_id: S01
    path: references/source_cards/S01_source_card.md
    file_role: source_card
    sha256: to_be_computed
    notes: metadata and short notes only

coverage_summary:
  critical_requirements_total: 0
  critical_requirements_covered: 0
  remaining_blockers: []


---

## templates/acquisition/local_persistence_log.csv

entry_id,source_id,file_role,path,sha256,created_at,notes


---

## templates/acquisition/open_reference_questions.md

# Open Reference Questions

| Question ID | Question | Severity | Needed From | Blocks Analysis? | Blocks Coding? | Recommended Resolution |
| --- | --- | --- | --- | --- | --- | --- |
| QREF-001 | to_be_defined | high | user_or_source | true | true | identify governing reference or mark prototype only |


---

## templates/acquisition/reference_gap_assessment.md

# Reference Gap Assessment

## Calculation intent

- Domain:
- Calculation object:
- Intended software output:

## Material state

```text
no_materials | insufficient_materials | materials_available_untrusted | local_evidence_library_available
```

## Sufficiency judgment

```text
evidence_no_go | search_required | partial_analysis_allowed | analysis_allowed
```

## Blocking gaps

| Gap ID | Missing information | Why it matters | Blocks analysis? | Blocks coding? | Needed source type |
| --- | --- | --- | --- | --- | --- |

## Non-blocking gaps

| Gap ID | Missing information | Impact | Recommended follow-up |
| --- | --- | --- | --- |


---

## templates/acquisition/retrieval_decisions.csv

decision_id,candidate_id,decision,reason,local_target,raw_allowed,source_card_required,extraction_required,follow_up


---

## templates/acquisition/search_log.csv

search_id,gap_id,query,tool_or_location,date,results_reviewed,candidates_selected,notes


---

## templates/acquisition/source_card_template.md

# Source Card: SXX

## Metadata

- Source ID:
- Title:
- Publisher / Author:
- Source type:
- Version / Date:
- Jurisdiction:
- URL or location:
- Access date:
- Raw file path:
- Extracted file path:

## Authority and relevance

- Authority level:
- Priority:
- Coverage tags:
- Gaps covered:
- Recommended downstream use:

## Key references

| Clause/Table/Figure/Page | Topic | Notes |
| --- | --- | --- |

## Short compliant excerpts if necessary

Keep excerpts short and only when needed.

## Paraphrased notes

- 

## Limitations and access notes

- License/access notes:
- Known limitations:


---

## templates/acquisition/source_coverage_matrix.csv

requirement_id,requirement,importance,covered,current_source_id,gap,needed_source_type,blocks_analysis,blocks_coding


---

## templates/acquisition/source_registry.yaml

sources:
  - source_id: S01
    title: example source
    source_type: official_manual
    publisher_or_author: example publisher
    version_or_date: 2026
    jurisdiction: to_be_defined
    role_in_analysis: governing_source
    authority_level: high
    priority: 1
    raw_file_path: null
    source_card_path: references/source_cards/S01_source_card.md
    extracted_paths: []
    coverage_tags: []
    limitations: []
    license_or_access_notes: source card only unless authorized


---

## templates/analysis/applicability_limits.csv

limit_id,assumption_or_limit,applies_to,source_reference,program_handling,risk_level


---

## templates/analysis/assumption_register.csv

assumption_id,assumption,source_reference,reason,program_handling,blocks_production


---

## templates/analysis/branch_inventory.csv

branch_id,condition,engineering_meaning,source_reference,path_if_true,path_if_false,not_applicable_behavior,program_representation,required_tests,risk_level


---

## templates/analysis/calculation_blueprint.md

# Calculation Logic Blueprint

## Scope and purpose

## Source basis

## Engineering concept map summary

## Calculation stages

```text
input
-> validation
-> normalization
-> method selection
-> calculation
-> special-condition handling
-> check
-> governing summary
-> output
```

## Node inventory summary

## Input / intermediate / output model mapping

## Module candidates

## Diagrams

## Verification targets

## Open questions


---

## templates/analysis/calculation_nodes.csv

node_id,node_type,node_name,engineering_meaning,inputs,outputs,units,formula_or_method,source_reference,branch_condition,applicability,assumptions,module_candidate,result_visibility,report_visibility,test_requirement,risk_level


---

## templates/analysis/concept_map.csv

concept,meaning,role_in_calculation,source_id,notes


---

## templates/analysis/formula_inventory.csv

formula_id,name,purpose,inputs,outputs,units,source_reference,applicability,branch_dependencies,lookup_dependencies,implementation_note,test_requirement,risk_level


---

## templates/analysis/global_flowchart.mmd

flowchart TD
    A[Collect inputs] --> B[Validate inputs]
    B --> C{Inputs valid?}
    C -- No --> E[Stop with validation error]
    C -- Yes --> D[Run calculation modules]
    D --> F[Summarize governing results]
    F --> G[Build structured outputs]


---

## templates/analysis/input_inventory.csv

field,symbol,unit,source_id,required,default,validation_rule,module


---

## templates/analysis/intermediate_inventory.csv

value,symbol,unit,derived_from,used_by,should_be_reported


---

## templates/analysis/lookup_inventory.csv

lookup_id,name,inputs,outputs,source_reference,interpolation_rule,out_of_range_behavior,implementation_note,test_requirement,risk_level


---

## templates/analysis/open_questions.csv

question_id,question,severity,affected_artifact,blocks_analysis,blocks_coding,recommended_resolution


---

## templates/analysis/output_inventory.csv

output,symbol,unit,meaning,status_logic,report_section


---

## templates/analysis/risk_register.csv

risk_id,risk,cause,impact,mitigation,owner,status


---

## templates/analysis/source_authority_table.csv

source_id,source,source_type,version_or_date,role,priority,authority_level,notes


---

## templates/analysis/source_conflicts.csv

conflict_id,affected_item,source_a,source_a_method,source_b,source_b_method,engineering_consequence,recommended_resolution,blocks_analysis,blocks_coding


---

## templates/analysis/source_intake_notes.md

# Source Intake Notes

## Intake Summary

Record which raw files, source cards, extracted notes, spreadsheets, reports, or user-provided assumptions were reviewed.

## Authority Decisions

Explain priority ordering and any deviations from the default authority hierarchy.

## Conflicts And Gaps

Reference `source_conflicts.csv` and list source gaps that affect later extraction.

## Downstream Readiness

State whether `05-engineering-logic-blueprint` can proceed and what must be treated as uncertain.


---

## templates/analysis/source_inventory.yaml

sources:
  - source_id: S01
    source_name: example source
    source_type: official_manual
    version_or_date: 2026
    jurisdiction_or_project: to_be_defined
    role_in_analysis: governing_source
    priority: 1
    authority_level: high
    reliability_notes: []
    scope_of_applicability: []
    known_limitations: []
    local_path_or_source_card: references/source_cards/S01_source_card.md


---

## templates/analysis/unit_and_sign_conventions.md

# Unit And Sign Conventions

## Internal Unit System

| Quantity | Internal Unit | Input Unit Handling | Output Unit Handling |
| --- | --- | --- | --- |
| length | m | convert at boundary | convert at boundary |
| force | kN | convert at boundary | convert at boundary |
| stress_or_pressure | kPa | convert at boundary | convert at boundary |
| moment | kNm | convert at boundary | convert at boundary |
| displacement | mm | convert at boundary | convert at boundary |
| angle | radian | degrees allowed at input boundary | report as requested |

## Sign Conventions

| Quantity | Positive Direction Or Meaning | Source Reference | Program Handling |
| --- | --- | --- | --- |
| to_be_defined | to_be_defined | to_be_defined | needs_confirmation |

## Unresolved Items

List unclear units, signs, coordinate conventions, or reporting transformations.


---

## templates/handoff/artifact_index.yaml

artifact_index_id: A001
project_or_book: example_book
version: 0.1.0
created_at: 2026-06-16

references:
  acquisition_handoff: references/acquisition/acquisition_handoff.yaml
  source_registry: references/source_registry.yaml
  evidence_library_manifest: references/evidence_library_manifest.yaml

analysis:
  source_inventory: analysis/01_source_inventory/source_inventory.yaml
  calculation_blueprint: analysis/02_logic_blueprint/calculation_blueprint.md
  calculation_nodes: analysis/02_logic_blueprint/calculation_nodes.csv
  formula_inventory: analysis/03_logic_details/formula_inventory.csv
  lookup_inventory: analysis/03_logic_details/lookup_inventory.csv
  branch_inventory: analysis/03_logic_details/branch_inventory.csv
  risk_register: analysis/05_risks_and_questions/risk_register.csv
  open_questions: analysis/05_risks_and_questions/open_questions.csv

handoff:
  implementation_handoff: handoff/implementation_handoff.yaml
  coding_go_no_go: handoff/coding_go_no_go.md

implementation:
  architecture: implementation/00_architecture/project_structure.md
  models: implementation/01_core_models/data_model_spec.md
  modules: implementation/02_modules/module_interface_spec.md
  runner: implementation/03_book_runner/runner_sequence.md
  interfaces: implementation/04_interfaces/report_context_spec.md

verification:
  test_matrix: verification/test_matrix.csv
  tolerance_policy: verification/tolerance_policy.md
  acceptance_checklist: verification/acceptance_checklist.md


---

## templates/handoff/coding_go_no_go.md

# Coding Go / No-Go

## Gate status

```text
no_go | prototype_allowed | production_allowed
```

## Allowed work

- 

## Blocked work

- 

## Blocking issues

| Issue ID | Issue | Affected module | Required resolution |
| --- | --- | --- | --- |

## Notes

Do not implement production formulas when source basis, units, branch rules, or safety factors are unresolved.


---

## templates/handoff/implementation_handoff.md

# Implementation Handoff

## Handoff Status

Summarize `handoff/implementation_handoff.yaml` and the current coding gate.

## Source Basis

List governing, example, background, and assumption sources by stable source ID.

## Calculation Scope

State included checks, excluded checks, applicability limits, and major assumptions.

## Model Groups

Summarize input model groups, result model groups, validation rules, and result paths.

## Module And Runner Plan

Summarize module candidates, formula references, lookup references, branch references, and runner sequence.

## Verification Requirements

Summarize required unit, lookup, branch, regression, integration, smoke, and traceability tests.

## Blockers

List unresolved items that block prototype or production work.


---

## templates/handoff/implementation_handoff.yaml

handoff_id: H001
book_name: example_book
version: 0.1.0
status: prototype_allowed # no_go | prototype_allowed | production_allowed

source_basis:
  acquisition_handoff: references/acquisition/acquisition_handoff.yaml
  source_registry: references/source_registry.yaml
  governing_sources:
    - source_id: S01
      role: governing_code
      priority: 1
  example_sources:
    - source_id: S02
      role: regression_reference

evidence_library_status:
  status: analysis_allowed
  remaining_gaps:
    - gap_id: G001
      description: example remaining gap
      blocks_production: true

calculation_scope:
  domain: geotechnical
  object: shallow_foundation
  checks:
    - bearing_capacity
    - settlement

input_model_groups:
  - ProjectInfo
  - DesignBasis
  - GeometryInput
  - LoadInput
  - MaterialOrSoilInput
  - DesignOptions

result_model_groups:
  - ModuleResult
  - CheckResult
  - GoverningSummary
  - BookResult

runner_sequence:
  - validate_input
  - normalize_units
  - select_method
  - compute_module_results
  - check_utilization
  - summarize_governing
  - build_report_context

module_candidates:
  - module: libraries.domain.category.module_name
    responsibility: compute source-backed engineering result
    source_nodes: [N001]
    formulas: [F001]
    lookups: []

formula_inventory_refs:
  - F001

lookup_inventory_refs: []

branch_inventory_refs: []

validation_rules:
  - rule_id: V001
    severity: error
    description: required input must be present
    related_inputs: []

test_requirements:
  - test_id: T001
    type: regression
    basis: S02 worked example
    tolerance: to_be_defined

report_sections:
  - section_id: R001
    title: Input summary
    result_paths: []

traceability_requirements:
  - input_hash
  - result_hash
  - formula_traces
  - source_references

open_questions:
  - question_id: Q001
    severity: high
    blocks_production: true
    description: unresolved source issue

coding_gate:
  status: prototype_allowed
  allowed_work:
    - scaffold typed models
    - implement formulas with needs_confirmation markers
  blocked_work:
    - production release
    - final report certification


---

## templates/handoff/unresolved_items_before_coding.md

# Unresolved Items Before Coding

| ID | Item | Severity | Blocks production? | Recommended resolution |
| --- | --- | --- | --- |


---

## templates/implementation/batch_flow.md

# Batch Flow

```text
read batch_control -> load input -> run_book -> save result JSON -> render report -> summary CSV
```


---

## templates/implementation/core_model_plan.md

# Core Model Plan

## Core Responsibilities

Define status enums, check results, formula traces, warnings/errors, metadata, hashing, serialization, and unit boundary helpers.

## Out Of Scope

Core must not contain domain formulas, book-specific orchestration, UI logic, report rendering, or batch workflow behavior.

## Planned Files

| File | Responsibility |
| --- | --- |
| src/<pkg>/core/enums.py | status and severity enums |
| src/<pkg>/core/checks.py | CheckResult and FormulaTrace |
| src/<pkg>/core/units.py | boundary conversions |
| src/<pkg>/core/hashing.py | stable input/result hashes |


---

## templates/implementation/data_model_spec.md

# Data Model Specification

## BookInput

## Module inputs/results

## BookResult

## ReportContext


---

## templates/implementation/data_package_manifest.yaml

package_id: to_be_defined
schema_version: 0.1.0
created_at: to_be_defined
created_by: to_be_defined
project_or_book: to_be_defined
package_status: draft # draft | review | final | imported | superseded
source_basis:
  design_code: to_be_defined
  design_code_version: to_be_defined
  source_ids: []
inputs:
  final_input_json: null
  draft_input_json: null
  batch_control: null
results:
  book_result_json: null
  report_context_json: null
reports:
  html: []
  pdf: []
  docx: []
  xlsx: []
imported_reports:
  - report_import_id: RPT-IMPORT-001
    original_filename: to_be_defined
    role: comparison # comparison | regression_reference | client_report | prior_version
    local_path: to_be_defined
    sha256: to_be_defined
    trust_level: untrusted # untrusted | reference | approved
files:
  - path: to_be_defined
    role: input
    sha256: to_be_defined
    size_bytes: 0
hashes:
  input_hash: to_be_defined
  result_hash: to_be_defined
versions:
  package_version: to_be_defined
  runner_version: to_be_defined
  report_template_version: to_be_defined
validation:
  normalized_inputs: false
  run_book_executed: false
  verification_passed: false
  notes: []


---

## templates/implementation/dependency_rules.md

# Dependency Rules

Allowed direction:

```text
presentation / report / review / batch / API
  -> books
    -> libraries
      -> core
```

Forbidden reverse dependencies:

```text
core -> libraries/books/UI/report
libraries -> books/UI/report/batch
books -> UI pages or report templates
reports/templates -> engineering formulas
batch -> separate formula logic
```


---

## templates/implementation/feature_classification.csv

feature,layer,existing_module,new_module_needed,reusable,location,notes


---

## templates/implementation/formula_trace_spec.md

# Formula Trace Specification

Each source-backed formula result should expose:

| Field | Meaning |
| --- | --- |
| formula_id | stable ID from `formula_inventory.csv` |
| formula_name | human-readable formula or method name |
| source_reference | source ID plus clause/table/equation/page |
| inputs | values used by the formula |
| intermediates | audit values needed for review |
| result_symbol | engineering symbol |
| result_value | computed value |
| unit | result unit |
| notes | warnings, assumptions, or implementation comments |


---

## templates/implementation/frontend_fields.csv

field_path,label,unit,group,editable,source,notes


---

## templates/implementation/governing_summary_spec.md

# Governing Summary Specification

## Required Fields

| Field | Meaning |
| --- | --- |
| overall_status | aggregate PASS/FAIL/WARNING/ERROR state |
| governing_check_id | controlling check ID |
| governing_check_name | controlling check name |
| governing_utilization_or_margin | utilization, margin, or equivalent measure |
| governing_limit | criterion used for governing selection |
| critical_load_case_or_combination | controlling load case if applicable |
| warnings_count | number of preserved warnings |
| errors_count | number of preserved errors |

## Selection Rule

Document how governing checks are ranked when multiple checks are near or beyond limits.


---

## templates/implementation/import_export_contract.md

# Import, Report Import, and Export Contract

Use this template for data import, prior report import, upload packages, and repeatable exports.

## Managed Data Directories

```text
data/input/
data/imported/reports/
data/imported/references/
data/staging/
data/normalized/cases/
data/packages/
outputs/results_json/
outputs/reports_html/
outputs/reports_pdf/
outputs/reports_docx/
outputs/upload_packages/
outputs/logs/
```

## Accepted Imports

| Import type | Formats | Destination | Normalization target | Allowed use |
| --- | --- | --- | --- | --- |
| case input | JSON / YAML / CSV / XLSX | data/input or data/staging | BookInput JSON | official calculation after validation |
| batch control | CSV / XLSX / YAML | data/input | batch_control.csv | batch orchestration |
| prior report | HTML / PDF / DOCX / XLSX / context.json | data/imported/reports | report_import record | review/comparison only |
| reference file | PDF / image / document / spreadsheet | data/imported/references | source card or registry entry | source-backed review only |
| upload package | ZIP / folder | data/packages | manifest + normalized inputs | repeatable import/export |

## Upload Package Flow

```text
receive package
-> store in data/staging/
-> compute file hashes
-> read data_package_manifest.yaml if present
-> classify files by role
-> validate schema and allowed extensions
-> preview case list and imported report list
-> normalize accepted case inputs
-> run selected case or batch through run_book()
-> write BookResult JSON, reports, and package manifest
```

## Report Import Rules

- Imported reports are evidence or comparison artifacts, not official calculation truth.
- Imported report metadata must include original filename, hash, import date, role, and trust level.
- If an imported report is used as a regression reference, record the expected result paths and tolerances in verification artifacts.
- If an imported report contains values that must become official inputs, convert them into BookInput fields with provenance and reviewer confirmation.

## Export Package Contents

| Path | Required | Notes |
| --- | --- | --- |
| data_package_manifest.yaml | true | Package inventory and hashes. |
| inputs/final_input.json | true for final | Exact normalized BookInput. |
| inputs/draft_input.json | optional | Exploratory or review input. |
| results/book_result.json | true when calculated | Exact BookResult. |
| reports/ | optional | HTML/PDF/DOCX/XLSX outputs. |
| traces/ | optional | Formula/source trace exports. |
| logs/ | optional | Run logs and validation summaries. |

## Validation Summary

| Check | Status | Evidence | Notes |
| --- | --- | --- | --- |
| manifest present or generated | to_be_defined | data_package_manifest.yaml |  |
| file hashes recorded | to_be_defined | manifest |  |
| inputs normalized to BookInput | to_be_defined | normalized cases |  |
| imported reports classified | to_be_defined | report import records |  |
| no formulas in imported UI/report files | to_be_defined | review |  |


---

## templates/implementation/input_mapping_spec.md

# Input Mapping Specification

## Flow

```text
CSV / JSON / API / UI input
-> parse external fields
-> validate shape and units
-> build BookInput
-> run_book(BookInput)
```

## Mapping Table

| External Field | BookInput Path | Unit | Required | Default | Validation | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| to_be_defined | to_be_defined | to_be_defined | true | none | to_be_defined | to_be_defined |


---

## templates/implementation/lookup_module_spec.md

# Lookup Module Specification

## Lookup Ownership

Lookup tables, charts, interpolation rules, and out-of-range behavior belong in reusable calculation modules or lookup helpers, not UI/report/batch code.

## Required Fields

| Lookup ID | Source Reference | Inputs | Output | Interpolation | Out Of Range Behavior | Tests |
| --- | --- | --- | --- | --- | --- | --- |
| L001 | to_be_defined | to_be_defined | to_be_defined | needs_confirmation | error_or_warning | test_lookup_L001 |


---

## templates/implementation/marimo_review_spec.md

# Marimo Review Specification

Use Marimo for Python-native, reactive engineering review pages when module-level checking, editable inputs, or exploratory scenarios are useful.

## App Locations

```text
apps/review/<book_name>_review.py
apps/review/modules/<module_name>_review.py
```

## Launch Commands

```bash
marimo edit apps/review/<book_name>_review.py
marimo run apps/review/<book_name>_review.py
```

Use `marimo edit` for authoring and engineering development. Use `marimo run` for a read-only review app.

## Standard Review Page

| Section | Required content |
| --- | --- |
| Header | project, case, package id, report status, source basis, runner version |
| Package loader | file upload or file browser for data packages and final inputs |
| Module selector | module list from handoff/module registry |
| Editable input | BookInput group or module input model using form controls or data editor |
| Run cell | call selected trusted module or run_book() |
| Result summary | status, governing value, warnings/errors |
| Trace review | formula ids, source references, lookup ids, branch decisions |
| Diff review | current draft vs final input/result/imported report |
| Notes and decision | reviewer notes, accepted/rejected/needs change |
| Save/export | draft input, review log row, BookResult JSON, upload package |

## Module Review Rules

- Each editable field must map to a typed input field.
- Each result value must map to a module result path or BookResult path.
- Exploratory edits must be labeled draft/review/prototype.
- Saving an edit must write a new draft input or review artifact; do not overwrite final input silently.
- Module pages may call reusable modules directly for review, but official report generation must use `run_book()`.
- The page must display warnings/errors and traceability before export.

## Suggested Widgets

Use the available Marimo UI widgets that fit the project:

```text
file upload for local user-provided packages
file browser for server-side package selection
data editor for tabular module inputs
dropdown or tabs for module selection
forms and sliders for scenario exploration
tables/dataframes for check summaries and diffs
download controls for JSON/report/package artifacts
```

## Review Log

Write review decisions to:

```text
implementation/04_interfaces/module_review_log.csv
outputs/logs/module_review_log.csv
```

Do not use the review log as calculation input. It is an audit record.


---

## templates/implementation/module_interface_spec.md

# Module Interface Specification

## Public functions

## Input models

## Result models

## Formula traces

## Warning/error behavior


---

## templates/implementation/module_review_log.csv

module_review_id,module_id,review_scope,input_source,edited_fields,runner_or_function,result_status,decision,output_path,notes


---

## templates/implementation/package_layout.md

# Package Layout

| Package Or File | Layer | Responsibility | May Import | Must Not Import |
| --- | --- | --- | --- | --- |
| src/<pkg>/core/ | core platform | statuses, checks, traces, units, hashes | standard library | domain formulas |
| src/<pkg>/libraries/ | reusable engineering library | formulas, lookups, branch-local checks | core | books, UI, reports |
| src/<pkg>/books/<book_name>/ | book runner | official orchestration and BookResult | core, libraries | UI pages |
| src/<pkg>/interfaces/ | interface layer | CLI/API/batch adapters | books | formulas |
| src/<pkg>/report/ | report layer | render from ReportContext | books or report context | formulas |
| webapp/ or src/<pkg>/interfaces/webapp/ | production frontend | unified left-input/right-review UI, import/export, report preview | books/API/report context | formulas |
| apps/review/ | Marimo review apps | module review, editable draft inputs, traces, what-if exploration | books, libraries, report context | formulas not already in trusted modules |
| data/ | managed input area | input, imported reports, references, staging, normalized cases, packages | none | generated results |
| outputs/ | generated output area | BookResult JSON, reports, packages, logs | none | source inputs |


---

## templates/implementation/project_structure.md

# Project Structure

```text
engineering_calc_project/
  references/
  analysis/
  handoff/
  data/
    input/
    imported/
      reports/
      references/
    staging/
    normalized/
      cases/
    packages/
  implementation/
  src/<pkg>/
    core/
    libraries/
    books/<book_name>/
    interfaces/
    report/
  webapp/
  apps/
    review/
  tests/
  verification/
  outputs/
    results_json/
    reports_html/
    reports_pdf/
    reports_docx/
    upload_packages/
    logs/
```

## Placement Rules

Record where each feature class belongs and which files own formulas, runner orchestration, reports, interfaces, and tests.

Use `webapp/` or `src/<pkg>/interfaces/webapp/` for the unified production frontend. Use `apps/review/` for Marimo review apps. Use `data/` for user-provided, imported, staging, normalized, and package-managed data. Use `outputs/` only for generated artifacts.


---

## templates/implementation/report_context_spec.md

# Report Context Specification

Use this template to define how a report, review page, export, or batch artifact consumes already-computed results. Keep it domain-neutral. Do not prescribe a fixed report layout unless the user, source basis, client requirement, or implementation handoff requires one.

## Report Production Decision Record

| Decision item | Selected value | Reason | Source or artifact |
| --- | --- | --- | --- |
| Report purpose | to_be_defined | to_be_defined | user request / handoff |
| Intended audience | to_be_defined | to_be_defined | user request / handoff |
| Review depth | draft / review / final / prototype | to_be_defined | coding gate |
| Report status | draft / review / final / superseded / prototype / not_for_construction | to_be_defined | coding gate |
| Output format | html / pdf / docx / xlsx / json / other | to_be_defined | user request |
| Renderer or export path | to_be_defined | to_be_defined | environment |
| Saved input source | final_input.json / other | to_be_defined | output registry |
| Saved result source | BookResult JSON / trusted BookResult | to_be_defined | output registry |
| Verification method | smoke / regression / visual / manual review | to_be_defined | verification plan |

## Production Eligibility

| Requirement | Status | Evidence | Notes |
| --- | --- | --- | --- |
| Coding gate allows production | to_be_defined | handoff/coding_go_no_go.md |  |
| Source basis is sufficient | to_be_defined | references/source_registry.yaml |  |
| Report uses saved final input or trusted BookResult | to_be_defined | output path |  |
| Templates do not calculate | to_be_defined | review or test |  |
| Warnings and errors are preserved | to_be_defined | smoke test |  |
| Traceability metadata is preserved | to_be_defined | result/report metadata |  |
| Renderer smoke test exists | to_be_defined | tests/smoke |  |

If any production requirement is not satisfied, the report status must not be `final`.

## Inputs

List external or saved inputs displayed in the report. These are presentation fields only; official calculations must already be represented in `BookInput` and `BookResult`.

| Report field | BookInput or BookResult path | Unit | Display rule | Source | Notes |
| --- | --- | --- | --- | --- | --- |
| to_be_defined | to_be_defined | to_be_defined | to_be_defined | to_be_defined | to_be_defined |

## Report Sections

Derive sections from the user request, calculation scope, result paths, review needs, and source-backed reporting requirements.

| Section ID | Section title | Purpose | Required data paths | Visibility rule | Notes |
| --- | --- | --- | --- | --- | --- |
| R001 | to_be_defined | to_be_defined | to_be_defined | to_be_defined | to_be_defined |

## Module summaries

| Module or check | Result paths | Values to display | Formula trace visibility | Notes |
| --- | --- | --- | --- | --- |
| to_be_defined | to_be_defined | to_be_defined | summary / detailed / appendix / hidden | to_be_defined |

## Governing summary

| Field | BookResult path | Display rule | Notes |
| --- | --- | --- | --- |
| overall_status | governing.overall_status | to_be_defined |  |
| governing_check_id | governing.governing_check_id | to_be_defined |  |
| governing_utilization_or_margin | governing.governing_utilization_or_margin | to_be_defined |  |
| warnings_count | governing.warnings_count | to_be_defined |  |
| errors_count | governing.errors_count | to_be_defined |  |

## Warnings/errors

| Source path | Severity | Display location | Must appear in final report | Notes |
| --- | --- | --- | --- | --- |
| warnings | warning | to_be_defined | true |  |
| errors | error | to_be_defined | true |  |

## Assumptions And Limitations

| Item ID | Text or reference | Source | Blocks final report | Display rule |
| --- | --- | --- | --- | --- |
| to_be_defined | to_be_defined | to_be_defined | to_be_defined | to_be_defined |

## Traceability

| Metadata item | Source path | Required for production | Notes |
| --- | --- | --- | --- |
| report_status | ReportContext metadata | true |  |
| input_hash | BookResult metadata or saved input | true |  |
| result_hash | BookResult metadata or saved result | true |  |
| source_references | BookResult / traces | true |  |
| runner_version | BookResult metadata | true |  |
| report_template_version | renderer metadata | true when templated |  |
| data_package_id | package manifest | true when packages exist |  |
| imported_report_ids | import records | true when imported reports are used |  |

## Imported Reports and Packages

| Item | Source | Display rule | Final report impact |
| --- | --- | --- | --- |
| imported reports | data/imported/reports or package manifest | label as comparison/reference/client/prior version | never override official result |
| package manifest | data_package_manifest.yaml | show package id, status, hashes, and validation | required when package export is used |
| input/result diff | saved final input/result or imported report context | show changed paths and review note | blocks final only when unresolved |

## Template Boundaries

Allowed in templates:

```text
value references
loops
conditionals
section visibility logic
formatting filters
unit display formatting
cross-references
```

Forbidden in templates:

```text
engineering formulas
capacity/demand/status recalculation
lookup table selection
load-combination generation
optimization logic
official unit conversion
warning/error suppression
```


---

## templates/implementation/result_path_registry.csv

result_path,meaning,unit,source_module,report_visibility,regression_check


---

## templates/implementation/review_readability_checklist.md

# Review Readability Checklist

- [ ] Governing result is visible before detailed results.
- [ ] Report status is visible as text, not color alone.
- [ ] Source basis, design code/version, and source IDs are visible near the top.
- [ ] Warnings, errors, unresolved assumptions, and prototype status are never hidden.
- [ ] Inputs are grouped by engineering meaning and BookInput model groups.
- [ ] Every editable field has unit, validation rule, and BookInput path.
- [ ] Result cards follow engineering review order, not implementation order.
- [ ] Critical formulas, lookup tables, and branch choices can be expanded from the result.
- [ ] Current input/result can be compared with saved final input/result or imported report where applicable.
- [ ] Imported reports are labeled as review/reference artifacts.
- [ ] Exported reports and packages include input hash, result hash, runner version, and template version.
- [ ] Marimo exploratory edits are labeled draft/review/prototype until saved and verified.
- [ ] UI, Marimo, report templates, and batch summaries do not calculate or override status.


---

## templates/implementation/review_schema.csv

field_path,label,unit,input_type,required,validation,help_text


---

## templates/implementation/runner_sequence.md

# Runner Sequence

```text
validate_input -> normalize_units -> call_modules -> summarize_governing -> return_BookResult
```


---

## templates/implementation/status_semantics.md

# Status Semantics

| Status | Meaning | Typical Handling |
| --- | --- | --- |
| PASS | check satisfies the stated criterion | report normally |
| FAIL | check does not satisfy the criterion | expose as governing or blocking |
| WARNING | result exists but requires attention | preserve and report |
| ERROR | required calculation could not complete | block dependent result |
| NOT_APPLICABLE | check does not apply | omit from governing failure selection |
| NEEDS_CONFIRMATION | source or assumption must be confirmed | prototype only unless resolved |
| NOT_EVALUATED | calculation was not run | expose reason |


---

## templates/implementation/ui_layout_spec.md

# Unified UI Layout Specification

Use this template for production frontend, review UI, or app-like engineering calculation interfaces.

## Layout Decision

| Item | Selected value | Reason | Evidence |
| --- | --- | --- | --- |
| Interface family | production frontend / Marimo review / report preview / batch dashboard | to_be_defined | user request |
| Primary user | engineer / checker / approver / batch operator | to_be_defined | workflow |
| Data source | uploaded package / final_input.json / API / batch_control | to_be_defined | import contract |
| Calculation path | run_book(BookInput) -> BookResult | required | code |
| Report preview path | HTML / PDF / DOCX / other | to_be_defined | report context |

## Standard Page Zones

| Zone | Required content | Notes |
| --- | --- | --- |
| Top bar | project/book title, case selector, status, import, export, report preview | Keep actions predictable across projects. |
| Left input panel | collapsible BookInput groups, units, validation, sticky run/save controls | Do not place result logic here. |
| Right review workbench | governing summary, warnings/errors, result cards, charts, traces | Conclusion first, details below. |
| Modal/drawer | report preview, imported report preview, source trace, formula trace, package validation, diff | Use for deep review without losing context. |
| Status strip | input hash, result hash, runner version, report template version, package id, timestamp | Required for production review. |

## Input Card Pattern

| Card ID | BookInput group | Fields | Validation feedback | Conditional visibility | Notes |
| --- | --- | --- | --- | --- | --- |
| to_be_defined | to_be_defined | to_be_defined | inline / summary | to_be_defined |  |

## Result Card Pattern

| Card ID | BookResult path | Purpose | Displays | Trace expansion | Report visibility |
| --- | --- | --- | --- | --- | --- |
| governing | governing | conclusion first | status, governing check, utilization/margin | true | summary |
| warnings_errors | warnings/errors | review blockers | warnings, errors, unresolved assumptions | true | summary |

## Interaction States

| State | Required UI behavior |
| --- | --- |
| no_input | Show import/create options and disabled report export. |
| draft_input | Allow run, save draft, export draft package. |
| validation_error | Show field-level errors and keep run disabled or blocked. |
| calculation_error | Preserve input, show error, do not emit final output. |
| review_result | Show traces, warnings, export review package. |
| final_result | Require saved final input, trusted BookResult, verification evidence. |

## Visual Rules

- Keep the interface dense and work-focused.
- Put inputs on the left and results on the right for desktop layouts.
- On mobile, stack input first, then governing summary, then result details.
- Use clear status text in addition to color.
- Keep formulas and long traces behind expandable detail sections.
- Use tables for comparable engineering checks and compact metric boxes for headline values.
- Provide chart containers only when figures improve engineering review.


---

## templates/implementation/unit_system.md

# Unit System

## Policy

Use one internal unit system. Convert units only at input and output boundaries.

| Quantity | Internal Unit |
| --- | --- |
| length | m |
| force | kN |
| stress_or_pressure | kPa |
| unit_weight | kN/m3 |
| moment | kNm |
| settlement_or_displacement | mm |
| angle_internal | radian |

## Boundary Conversion

Document accepted input units, output units, and where conversion functions live.


---

## templates/verification/acceptance_checklist.md

# Acceptance Checklist

- [ ] Source basis recorded
- [ ] Acquisition handoff exists when sources were searched
- [ ] Implementation handoff exists
- [ ] Report production decision is recorded when a report/export is produced
- [ ] Report status is explicit and matches evidence/coding gate state
- [ ] Formulas are only in calculation modules/books
- [ ] One official run_book() exists
- [ ] Typed BookInput and BookResult exist
- [ ] Unit policy is explicit
- [ ] Report/UI/batch do not calculate
- [ ] UI follows the unified layout when a frontend exists
- [ ] Marimo review pages do not calculate outside trusted modules or run_book
- [ ] Upload/import packages have manifests and hashes when present
- [ ] Imported reports are labeled as review/reference artifacts
- [ ] Reports are generated from saved final input or trusted BookResult
- [ ] ReportContext preserves source basis, limitations, warnings/errors, and traceability metadata
- [ ] Unit tests exist
- [ ] Regression tests exist when references exist
- [ ] Integration test exists
- [ ] Smoke tests exist for reports/interfaces
- [ ] Report renderer/export path has a documented run command
- [ ] Traceability metadata exists for production outputs


---

## templates/verification/regression_references.md

# Regression References

| Ref ID | Source ID | Case | Expected outputs | Notes |
| --- | --- | --- | --- | --- |


---

## templates/verification/test_matrix.csv

test_id,target,type,reference_basis,input_case,expected_result,tolerance,priority,notes


---

## templates/verification/tolerance_policy.md

# Tolerance Policy

Define absolute/relative tolerances per formula, lookup, and integration result.


---

## workflow_diagrams/full_lifecycle.mmd

flowchart TD
    A[User request] --> B{Materials available?}
    B -- No or insufficient --> C[01 Reference adequacy assessment]
    C --> D[02 Reference discovery and acquisition]
    D --> E[03 Local evidence library persistence]
    E --> F[04 Source intake and authority]
    B -- Yes --> F
    F --> G[05 Calculation Logic Blueprint]
    G --> H[06 Formula / lookup / branch extraction]
    H --> I[07 Implementation handoff contract]
    I --> J{Coding gate}
    J -- no_go --> K[Resolve source or logic gaps]
    K --> C
    J -- prototype_allowed or production_allowed --> L[08 Architecture]
    L --> M[09 Core and data models]
    M --> N[10 Reusable calculation modules]
    N --> O[11 Book runner and governing summary]
    O --> P[12 Report / review / batch interfaces]
    O --> Q[13 Verification / regression / traceability]
    P --> Q
    Q --> R[Release package]
