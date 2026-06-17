# Engineering Calculation System - All-in-One Skill Pack
Version: 2.2.0

This merged file combines the root entrypoint, parent skills, child skills, shared contracts, key templates, validation schema, and scaffold files.


---

## adapters/agent-entrypoints.md

# Agent Entrypoints

Use this file when the target agent cannot automatically discover the root `SKILL.md`.

## Codex

Install the package as a skill folder when possible. The root `SKILL.md` is the primary entrypoint. For a single-file import, use `engineering-calculation-system.all-in-one.md`.

## Qoder

Use the included `.qoder/agents/engineering-calc-system.md` or `.qoder/skills/engineering-calc-system/SKILL.md` when the environment supports Qoder-style agents or skills.

## Trae

Use `.trae/rules/engineering-calc-system.md` as project rules when the environment supports repository-level rule files. If the environment only supports manual instructions, paste the routing prompt below.

## Trae / opencode / Generic Rules Agents

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
description: Parent/orchestrator skill for building, refactoring, extending, reviewing, testing, packaging, or deploying reusable engineering calculation book software from a validated Implementation Handoff Contract. Use for typed inputs/results, decoupled reusable formula modules, module asset accumulation, official book runners, report contexts, unified production frontends, Marimo module review apps, import/export packages, batch workflows, traceability, regression tests, local runnable web clients, and Linux cloud deployment.
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
12a-report-context-and-rendering when reports or report previews are needed
12b-frontend-and-review-interfaces when production UI, API, charts, i18n, or Marimo review is needed
12c-batch-import-export-packages when import/export, upload packages, or batch execution is needed
13-verification-regression-traceability
14-cloud-web-release-deployment when the result must be a runnable local or Linux-cloud deployable web calculator
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
9. Use Skill 12 to select required interface subskills, then build report context, unified frontend, Marimo module review app, API, CLI, import/export package flow, or batch only as thin interfaces over `run_book()`.
10. Add unit, branch, lookup, regression, integration, and smoke tests.
11. Package local and cloud Linux web release artifacts when final delivery is expected.
12. Record acceptance status.

## Required Final Output

For new calculation book systems, provide:

```text
feature classification table
project structure
input schemas and typed models
unit system and status semantics
reusable module interfaces
module asset registry
book runner design
governing summary design
result path registry
report context design when needed
unified review/frontend/batch flow when needed
Marimo review app design when needed
data package import/export contract when needed
test plan and skeletons
run commands
local and cloud Linux deployment commands when final delivery is expected
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

## project_template/engineering_calc_project/deploy/docker-compose.yml

services:
  engineering-calc-web:
    build:
      context: ..
      dockerfile: deploy/Dockerfile
    env_file:
      - env.example
    ports:
      - "5000:5000"
    volumes:
      - ../data:/app/data
      - ../outputs:/app/outputs
    restart: unless-stopped


---

## project_template/engineering_calc_project/deploy/Dockerfile

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src
ENV APP_HOST=0.0.0.0
ENV APP_PORT=5000
ENV FLASK_DEBUG=0

WORKDIR /app

COPY pyproject.toml README.md ./
RUN pip install --no-cache-dir "flask>=3.0" "gunicorn>=21.2"

COPY src ./src
COPY webapp ./webapp

EXPOSE 5000

CMD ["gunicorn", "webapp.app:create_app()", "--bind", "0.0.0.0:5000", "--workers", "2"]


---

## project_template/engineering_calc_project/deploy/env.example

APP_HOST=0.0.0.0
APP_PORT=5000
FLASK_DEBUG=0
SECRET_KEY=change-me-on-server
DATA_DIR=/var/lib/engineering-calc/data
OUTPUT_DIR=/var/lib/engineering-calc/outputs


---

## project_template/engineering_calc_project/deploy/nginx/engineering-calc.conf

server {
    listen 80;
    server_name example.com;

    client_max_body_size 25m;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}


---

## project_template/engineering_calc_project/deploy/systemd/engineering-calc.service

[Unit]
Description=Engineering Calculation Web Application
After=network.target

[Service]
Type=simple
WorkingDirectory=/opt/engineering-calc
EnvironmentFile=/opt/engineering-calc/deploy/env.example
Environment=PYTHONPATH=/opt/engineering-calc/src
ExecStart=/opt/engineering-calc/.venv/bin/gunicorn "webapp.app:create_app()" --bind 127.0.0.1:5000 --workers 2
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target


---

## project_template/engineering_calc_project/implementation/02_modules/module_asset_registry.csv

module_id,domain,category,module_name,public_function,input_model,options_model,result_model,source_references,formula_trace_path,unit_tests,regression_tests,reuse_status,asset_owner,notes


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
references -> analysis -> handoff -> implementation -> src -> tests -> deploy -> release
```

Start with `references/acquisition/` when materials are missing or insufficient.

## Validate

From this directory:

```bash
python3 -m pytest -q
```

## Run Locally

```bash
python3 -m pip install "flask>=3.0" "gunicorn>=21.2"
python3 -m webapp.app
```

Health check:

```bash
curl -fsS http://127.0.0.1:5000/health
```

## Deploy on Linux

Docker path:

```bash
docker compose -f deploy/docker-compose.yml up --build
```

systemd/gunicorn path:

```bash
gunicorn "webapp.app:create_app()" --bind 127.0.0.1:5000 --workers 2
```

From the skill pack root:

```bash
python3 scripts/validate_artifacts.py --package-root . --project project_template/engineering_calc_project
```


---

## project_template/engineering_calc_project/release/release_checklist.md

# Release Checklist

- [ ] Source basis and implementation handoff are recorded.
- [ ] Calculation modules are decoupled and listed in `implementation/02_modules/module_asset_registry.csv`.
- [ ] Official calculation path is `run_book(BookInput) -> BookResult`.
- [ ] Web/API/report/batch layers do not implement formulas.
- [ ] Unit, regression, integration, interface, and smoke tests pass or blockers are recorded.
- [ ] Local run command is tested: `python -m webapp.app`.
- [ ] Cloud Linux deployment files are present under `deploy/`.
- [ ] `/health` endpoint passes.
- [ ] `POST /api/calculate` smoke test passes with known input.
- [ ] Production debug mode is disabled.
- [ ] Secrets are environment-based and not committed.
- [ ] Data and output persistence paths are documented.


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

## project_template/engineering_calc_project/src/pkg/core/sanitize.py

"""Numeric sanitization utilities for JSON serialization.

Engineering calculations frequently produce non-finite floats
(Infinity from division by zero, NaN from invalid parameters).
These values break JSON serialization and frontend rendering.

Usage:
    from pkg.core.sanitize import sanitize_for_json
    cleaned, warnings = sanitize_for_json(result_dict)
"""

from __future__ import annotations

import math
from typing import Any


def sanitize_for_json(
    obj: Any,
    _path: str = "",
) -> tuple[Any, list[dict[str, str]]]:
    """Recursively replace non-finite floats with None.

    Walks dicts, lists, and tuples. Replaces float('inf'), float('-inf'),
    and float('nan') with None. Records each replacement as a warning.

    Args:
        obj: The object to sanitize (dict, list, scalar, etc.).
        _path: Internal field path tracker for warning messages.

    Returns:
        Tuple of (sanitized_object, list_of_warnings).
        Each warning is a dict with keys: field, reason.
    """
    warnings: list[dict[str, str]] = []

    if isinstance(obj, float):
        if math.isfinite(obj):
            return obj, warnings
        reason = "Infinity" if math.isinf(obj) else "NaN"
        warnings.append({"field": _path or "value", "reason": reason})
        return None, warnings

    if isinstance(obj, dict):
        result = {}
        for k, v in obj.items():
            child_path = f"{_path}.{k}" if _path else k
            sanitized, child_warnings = sanitize_for_json(v, child_path)
            result[k] = sanitized
            warnings.extend(child_warnings)
        return result, warnings

    if isinstance(obj, (list, tuple)):
        result = []
        for i, v in enumerate(obj):
            child_path = f"{_path}[{i}]"
            sanitized, child_warnings = sanitize_for_json(v, child_path)
            result.append(sanitized)
            warnings.extend(child_warnings)
        return result, warnings

    return obj, warnings


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

## project_template/engineering_calc_project/tests/smoke/example_input.json

{
  "project": {
    "project_id": "EXAMPLE_001",
    "case_id": "CASE_001",
    "title": "Example Project"
  },
  "options": {},
  "inputs": {}
}


---

## project_template/engineering_calc_project/tests/unit/.gitkeep




---

## project_template/engineering_calc_project/webapp/.gitkeep

unified production frontend lives here


---

## project_template/engineering_calc_project/webapp/__init__.py

"""Engineering calculation web application package."""


---

## project_template/engineering_calc_project/webapp/app.py

"""Application factory and local entrypoint for the engineering calculation web app."""

from __future__ import annotations

import sys

from flask import Flask, jsonify

from . import config as cfg

if str(cfg.SRC_DIR) not in sys.path:
    sys.path.insert(0, str(cfg.SRC_DIR))

from .routes import bp


def create_app() -> Flask:
    """Create the Flask application used by local runs and gunicorn."""
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.secret_key = cfg.SECRET_KEY
    app.config["DEBUG"] = cfg.DEBUG
    app.register_blueprint(bp)

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    return app


def main() -> None:
    app = create_app()
    app.run(host=cfg.HOST, port=cfg.PORT, debug=cfg.DEBUG)


if __name__ == "__main__":
    main()


---

## project_template/engineering_calc_project/webapp/config.py

"""Flask application configuration.

Scaffold: customize DEFAULTS and settings for each project.
"""

from __future__ import annotations

import os
from pathlib import Path

# Project root: one level up from webapp/
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = PROJECT_ROOT / "src"
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "outputs"

# Flask settings
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-key-change-in-production")
DEBUG = os.environ.get("FLASK_DEBUG", "0") == "1"

# Server settings
HOST = os.environ.get("APP_HOST", "0.0.0.0")
PORT = int(os.environ.get("APP_PORT", "5000"))

# Persistent runtime paths
DATA_DIR = Path(os.environ.get("DATA_DIR", DATA_DIR))
OUTPUT_DIR = Path(os.environ.get("OUTPUT_DIR", OUTPUT_DIR))

# Default calculation parameters — served on page load so the user
# can calculate immediately without filling every field.
# Customize these defaults for each engineering calculation book.
DEFAULTS: dict = {
    "project": {
        "project_id": "EXAMPLE_001",
        "project_name": "Example Project",
    },
    "foundation": {
        # Add book-specific geometry fields here.
        # e.g. "B_m": 1.0, "L_m": 1.0, "D_m": 1.2,
    },
    "loads": {
        # Add book-specific load fields here.
        # e.g. "Fx_kN": 0.0, "Fy_kN": 0.0, "Fz_kN": 100.0,
    },
    "options": {
        # Add book-specific design options here.
        # e.g. "fos_bearing": 3.0,
    },
    # Add soil_layers, water_table, or other book-specific sections as needed.
}


---

## project_template/engineering_calc_project/webapp/form_utils.py

"""Form data ↔ BookInput builder and BookResult → UI dict converter.

Scaffold: customize for each calculation book's BookInput / BookResult models.

This module is the SINGLE source of truth for form ↔ model mapping.
Never put mapping logic in route handlers or template renderers.
"""

from __future__ import annotations

import math
from typing import Any, Optional

from pkg.books.book_name.book_models import BookInput, BookResult, ProjectInfo
from pkg.core.enums import Status


# ---------------------------------------------------------------------------
# JSON Sanitization
# ---------------------------------------------------------------------------

def _sanitize_json(obj: Any, _path: str = "") -> tuple[Any, list[dict]]:
    """Recursively replace non-finite floats (inf, -inf, nan) with None.

    Python's float('inf') serializes as ``Infinity`` which is not valid JSON
    and causes ``JSON.parse`` to throw on the browser side.

    Returns:
        Tuple of (sanitized_object, list_of_warnings).
    """
    warnings: list[dict] = []

    if isinstance(obj, float):
        if math.isfinite(obj):
            return obj, warnings
        reason = "Infinity" if math.isinf(obj) else "NaN"
        warnings.append({"field": _path or "value", "reason": reason})
        return None, warnings

    if isinstance(obj, dict):
        result = {}
        for k, v in obj.items():
            child_path = f"{_path}.{k}" if _path else k
            sanitized, child_warnings = _sanitize_json(v, child_path)
            result[k] = sanitized
            warnings.extend(child_warnings)
        return result, warnings

    if isinstance(obj, (list, tuple)):
        result = []
        for i, v in enumerate(obj):
            child_path = f"{_path}[{i}]"
            sanitized, child_warnings = _sanitize_json(v, child_path)
            result.append(sanitized)
            warnings.extend(child_warnings)
        return result, warnings

    return obj, warnings


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _opt(val: Any, default: Optional[float] = None) -> Optional[float]:
    """Convert to float or return default."""
    if val is None or val == "" or val == "null":
        return default
    try:
        return float(val)
    except (ValueError, TypeError):
        return default


# ---------------------------------------------------------------------------
# Form → BookInput
# ---------------------------------------------------------------------------

def build_case_input_from_form(data: dict) -> BookInput:
    """Build a BookInput from web form JSON data.

    Customize this function for each calculation book.
    Use explicit field-by-field conversion — no reflection or magic.
    """
    proj = data.get("project", {})

    project = ProjectInfo(
        project_id=proj.get("project_id", "UNKNOWN"),
        case_id=proj.get("case_id", "CASE_001"),
        title=proj.get("title", "Untitled Project"),
    )

    # Scaffold: add book-specific input groups here.
    # foundation = Foundation(...)
    # load_case = LoadCase(...)
    # options = DesignOptions(...)

    return BookInput(
        project=project,
        design_options=data.get("options", {}),
        inputs=data.get("inputs", {}),
    )


# ---------------------------------------------------------------------------
# BookInput → Form (for import/export)
# ---------------------------------------------------------------------------

def book_input_to_form(bi: BookInput) -> dict:
    """Convert a BookInput back to the web form structure.

    Used for JSON export and populating forms after import.
    """
    return {
        "project": {
            "project_id": bi.project.project_id,
            "case_id": bi.project.case_id,
            "title": bi.project.title,
        },
        "design_options": bi.design_options,
        "inputs": bi.inputs,
    }


# ---------------------------------------------------------------------------
# BookResult → UI dict
# ---------------------------------------------------------------------------

def case_result_to_ui(r: BookResult, bi: BookInput) -> dict:
    """Convert BookResult to a UI-friendly dictionary.

    Customize for each calculation book's result structure.

    Rules:
    - round all floats to display precision (3-4 decimals)
    - convert enums to strings for JSON serialization
    - include governing status, utilization, and status badge text
    - embed SVG charts inline when available (bilingual if i18n active)
    - sanitize NaN/Infinity before returning
    """
    out: dict[str, Any] = {"status": "ok"}

    # Governing summary
    g = r.governing
    out["governing"] = {
        "check": g.governing_check_name or "—",
        "utilization": round(g.governing_utilization_or_margin, 4) if g.governing_utilization_or_margin is not None else None,
        "status": str(g.overall_status),
    }

    # Scaffold: add book-specific result sections here.
    # e.g. out["bearing"] = { ... }
    # e.g. out["settlement"] = { ... }
    # e.g. out["sliding"] = { ... }

    # Checks
    out["checks"] = [
        {
            "check_id": c.check_id,
            "name": c.name,
            "status": str(c.status),
            "demand": round(c.demand, 3) if c.demand is not None else None,
            "capacity": round(c.capacity, 3) if c.capacity is not None else None,
            "utilization": round(c.utilization, 4) if c.utilization is not None else None,
            "unit": c.unit,
            "warnings": c.warnings,
            "errors": c.errors,
        }
        for c in r.checks
    ]

    # Warnings and errors
    out["warnings"] = r.warnings
    out["errors"] = r.errors

    # Sanitize non-finite floats
    sanitized, sanitize_warnings = _sanitize_json(out)
    if sanitize_warnings:
        existing = sanitized.get("warnings") or []
        existing.extend(
            f"Sanitized {w['field']}: {w['reason']}" for w in sanitize_warnings
        )
        sanitized["warnings"] = existing

    return sanitized


---

## project_template/engineering_calc_project/webapp/i18n.py

"""Internationalization (i18n) system for the web UI.

Scaffold: add book-specific translations while keeping the common patterns.
Master dictionary: key -> (english, chinese).
"""

from __future__ import annotations

# Master i18n dictionary — common keys shared across all calculation books.
# Add book-specific entries below the common section.
I18N: dict[str, tuple[str, str]] = {
    # ── Navigation & Layout ──────────────────────────────────────────
    "app_title": ("Engineering Calculator", "工程计算系统"),
    "app_subtitle": ("Source-Backed Calculation Book", "有据可查的计算书"),
    "nav_calculate": ("Calculate", "执行计算"),
    "nav_export_report": ("Export Report", "导出报告"),
    "nav_import": ("Import JSON", "导入配置"),
    "nav_export": ("Export JSON", "导出配置"),
    "nav_language": ("Language", "语言"),
    "nav_preview": ("Preview Report", "预览报告"),
    "nav_download": ("Download Report", "下载报告"),

    # ── Section titles ───────────────────────────────────────────────
    "section_project": ("Project Information", "工程信息"),
    "section_options": ("Design Options", "设计参数"),
    "section_results": ("Calculation Results", "计算结果"),

    # ── Project form ─────────────────────────────────────────────────
    "project_id": ("Project ID", "项目编号"),
    "project_name": ("Project Name", "项目名称"),
    "case_id": ("Case ID", "工况编号"),

    # ── Buttons ──────────────────────────────────────────────────────
    "btn_calculate": ("Run Calculation", "执行计算"),
    "btn_import_json": ("Import JSON Config", "导入 JSON 配置"),
    "btn_export_json": ("Export Config", "导出配置"),
    "btn_preview_report": ("Preview Report", "预览报告"),
    "btn_download_report": ("Download Report", "下载报告"),
    "btn_close": ("Close", "关闭"),
    "btn_reset": ("Reset to Defaults", "恢复默认值"),

    # ── Results display ──────────────────────────────────────────────
    "result_title": ("Calculation Results", "计算结果"),
    "result_placeholder": ("Click \"Run Calculation\" to see results.", "点击「执行计算」查看结果。"),
    "result_governing": ("Governing Check", "控制性验算"),
    "result_all_pass": ("All checks PASS", "所有验算通过"),
    "result_has_fail": ("Some checks FAILED", "部分验算未通过"),
    "result_utilization": ("Utilization", "利用率"),
    "result_status_ok": ("PASS", "满足要求"),
    "result_status_ng": ("FAIL", "不满足要求"),

    # ── Error messages ───────────────────────────────────────────────
    "error_calc_failed": ("Calculation failed. Please check your inputs.", "计算失败，请检查输入参数。"),
    "error_invalid_input": ("Invalid input value", "输入值无效"),
    "error_missing_field": ("Required field missing", "必填字段缺失"),
    "error_import_failed": ("Failed to import configuration.", "导入配置失败。"),
    "error_no_result": ("Please run calculation first.", "请先执行计算。"),

    # ── Warning messages ─────────────────────────────────────────────
    "warn_invalid_values": (
        "Some computed values are invalid (Infinity/NaN) and have been replaced.",
        "部分计算结果无效(无穷大/非数值)，已替换。请检查输入参数。",
    ),

    # ── Report preview ───────────────────────────────────────────────
    "report_title": ("Calculation Report", "计算报告"),
    "report_generating": ("Generating report...", "正在生成报告..."),

    # ── Book-specific entries ────────────────────────────────────────
    # Add domain-specific translations below. Examples:
    # "section_soil": ("Soil Profile", "地基土层"),
    # "section_foundation": ("Foundation Geometry", "基础几何参数"),
    # "section_loads": ("Load Case", "荷载工况"),
    # "result_bearing": ("Bearing Capacity", "地基承载力"),
    # "result_settlement": ("Settlement", "沉降"),
}


def get_translations(lang: str = "en") -> dict[str, str]:
    """Return a flat dictionary of {key: translated_text} for the given language."""
    idx = 0 if lang == "en" else 1
    return {k: v[idx] for k, v in I18N.items()}


def t(key: str, lang: str = "en") -> str:
    """Get a single translated text."""
    entry = I18N.get(key)
    if entry is None:
        return key
    return entry[0] if lang == "en" else entry[1]


---

## project_template/engineering_calc_project/webapp/routes.py

"""Flask route handlers for the engineering calculation web app.

Scaffold: customize routes for each calculation book.
All route handlers are thin: parse → build model → call runner → convert → return.
"""

from __future__ import annotations

import json
import traceback
from io import BytesIO

from flask import (
    Blueprint, jsonify, render_template, request,
    Response, send_file,
)

from . import config as cfg
from .form_utils import build_case_input_from_form, case_result_to_ui
from .i18n import get_translations

bp = Blueprint("main", __name__)


# ---------------------------------------------------------------------------
# Page routes
# ---------------------------------------------------------------------------

@bp.route("/")
def index():
    """Serve the main single-page application."""
    return render_template("index.html")


# ---------------------------------------------------------------------------
# API routes
# ---------------------------------------------------------------------------

@bp.route("/api/defaults")
def api_defaults():
    """Return default calculation parameters."""
    return jsonify(cfg.DEFAULTS)


@bp.route("/api/i18n/<lang>")
def api_i18n(lang: str):
    """Return i18n translations for the given language (en or zh)."""
    if lang not in ("en", "zh"):
        lang = "en"
    return jsonify(get_translations(lang))


@bp.route("/api/calculate", methods=["POST"])
def api_calculate():
    """Run engineering calculation and return structured results.

    Flow: form JSON → BookInput → run_book() → BookResult → UI dict
    """
    try:
        data = request.get_json(force=True)
        book_input = build_case_input_from_form(data)

        # Import the book runner — the ONLY official calculation path.
        # Replace with the actual import for your calculation book.
        from pkg.books.book_name.book_runner import run_book
        result = run_book(book_input)

        ui_data = case_result_to_ui(result, book_input)
        return jsonify(ui_data)

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e) if cfg.DEBUG else "Calculation failed. Please check your inputs.",
        }), 400


@bp.route("/api/report/html", methods=["POST"])
def api_report_html():
    """Generate and download an HTML calculation report."""
    try:
        data = request.get_json(force=True)
        lang = data.pop("lang", "en")
        book_input = build_case_input_from_form(data)

        from pkg.books.book_name.book_runner import run_book
        result = run_book(book_input)

        # Replace with your actual report generator.
        # from pkg.report.html import generate_html_report
        # html = generate_html_report(book_input, result, lang=lang)
        html = f"<h1>Report placeholder for {book_input.project.project_id}</h1>"

        return Response(
            html,
            mimetype="text/html",
            headers={
                "Content-Disposition": f"attachment; filename=report_{book_input.project.project_id}.html"
            },
        )

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e) if cfg.DEBUG else "Report generation failed.",
        }), 400


@bp.route("/api/report/preview", methods=["POST"])
def api_report_preview():
    """Generate HTML report and return it as a string for inline preview."""
    try:
        data = request.get_json(force=True)
        lang = data.pop("lang", "en")
        book_input = build_case_input_from_form(data)

        from pkg.books.book_name.book_runner import run_book
        result = run_book(book_input)

        # Replace with your actual report generator.
        html = f"<h1>Report preview for {book_input.project.project_id}</h1>"

        return jsonify({"status": "ok", "html": html})

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e) if cfg.DEBUG else "Report preview failed.",
        }), 400


@bp.route("/api/import/json", methods=["POST"])
def api_import_json():
    """Import a BookInput JSON configuration file."""
    try:
        if "file" in request.files:
            f = request.files["file"]
            raw = f.read().decode("utf-8")
        else:
            raw = request.get_data(as_text=True)

        data = json.loads(raw)
        book_input = build_case_input_from_form(data)

        # Convert BookInput back to the web form structure.
        from .form_utils import book_input_to_form
        form_data = book_input_to_form(book_input)
        return jsonify({"status": "ok", "data": form_data})

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
        }), 400


@bp.route("/api/export/json")
def api_export_json():
    """Export current configuration as JSON file."""
    try:
        data = request.get_json(silent=True)
        if data is None:
            data = cfg.DEFAULTS

        book_input = build_case_input_from_form(data)

        # Replace with your actual serialization.
        from .form_utils import book_input_to_form
        json_data = book_input_to_form(book_input)

        return Response(
            json.dumps(json_data, indent=2, ensure_ascii=False),
            mimetype="application/json",
            headers={
                "Content-Disposition": f"attachment; filename=config_{book_input.project.project_id}.json"
            },
        )

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


# ---------------------------------------------------------------------------
# Error handlers
# ---------------------------------------------------------------------------

@bp.app_errorhandler(404)
def not_found(e):
    return jsonify({"status": "error", "message": "Not found"}), 404


@bp.app_errorhandler(500)
def server_error(e):
    return jsonify({"status": "error", "message": "Internal server error"}), 500


---

## project_template/engineering_calc_project/webapp/static/css/style.css

/* style.css — Minimal styles for the unified engineering calculator layout.
 *
 * Customize colors, spacing, and component styles for each project.
 */

/* ── Gradient navbar ─────────────────────────────────────────────── */
.bg-primary-gradient {
    background: linear-gradient(135deg, #1a5276 0%, #2e86c1 100%);
}

/* ── Input panel ──────────────────────────────────────────────────── */
.input-panel {
    max-height: calc(100vh - 80px);
    overflow-y: auto;
    padding-right: 0.5rem;
}

.sticky-bottom {
    position: sticky;
    bottom: 0;
    z-index: 10;
    border-radius: 0.375rem;
}

/* ── Result cards ─────────────────────────────────────────────────── */
.result-card .card-header {
    cursor: pointer;
    user-select: none;
}

.result-card .card-header:hover {
    background-color: rgba(0, 0, 0, 0.03);
}

.result-card .card-body table {
    font-size: 0.875rem;
}

/* ── Status colors ────────────────────────────────────────────────── */
.status-pass { color: #198754; }
.status-fail { color: #dc3545; }
.status-warn { color: #ffc107; }

/* ── Utilization bar ──────────────────────────────────────────────── */
.util-bar {
    height: 8px;
    border-radius: 4px;
    background-color: #e9ecef;
    overflow: hidden;
}

.util-bar-fill {
    height: 100%;
    border-radius: 4px;
    transition: width 0.3s ease;
}

.util-bar-fill.safe   { background-color: #198754; }
.util-bar-fill.caution { background-color: #ffc107; }
.util-bar-fill.fail   { background-color: #dc3545; }

/* ── Chart containers ─────────────────────────────────────────────── */
.chart-container {
    margin: 0.75rem 0;
    text-align: center;
}

.chart-container svg {
    max-width: 100%;
    height: auto;
}

/* ── Responsive ───────────────────────────────────────────────────── */
@media (max-width: 991px) {
    .input-panel {
        max-height: none;
        overflow-y: visible;
    }
}

/* ── Form compactness ─────────────────────────────────────────────── */
.form-label {
    margin-bottom: 0.15rem;
    font-weight: 500;
}

.form-control-sm {
    font-size: 0.8125rem;
}

/* ── Results icon placeholder ─────────────────────────────────────── */
.results-icon {
    opacity: 0.3;
}


---

## project_template/engineering_calc_project/webapp/static/js/forms.js

/**
 * forms.js — Form interaction, dynamic lists, and validation feedback.
 *
 * Customize for each calculation book's input structure.
 */

/**
 * Collect all form data into a JSON-compatible dictionary.
 * Called before POST /api/calculate.
 */
function collectFormData() {
    const data = {};

    // Project info
    data.project = {
        project_id: document.getElementById("project_id")?.value || "",
        project_name: document.getElementById("project_name")?.value || "",
        case_id: document.getElementById("case_id")?.value || "",
    };

    // Scaffold: collect book-specific form sections.
    // data.foundation = { B_m: parseFloat(...), ... };
    // data.loads = { Fx_kN: parseFloat(...), ... };
    // data.options = { ... };

    return data;
}

/**
 * Populate form fields from a data dictionary (e.g. from defaults or import).
 */
function populateForm(data) {
    if (data.project) {
        _setVal("project_id", data.project.project_id);
        _setVal("project_name", data.project.project_name);
        _setVal("case_id", data.project.case_id);
    }

    // Scaffold: populate book-specific sections.
    // if (data.foundation) { _setVal("B_m", data.foundation.B_m); ... }
    // if (data.loads) { _setVal("Fx_kN", data.loads.Fx_kN); ... }
}

/**
 * Reset form to server defaults.
 */
async function resetToDefaults() {
    try {
        const resp = await fetch("/api/defaults");
        const defaults = await resp.json();
        populateForm(defaults);
        clearResults();
    } catch (e) {
        console.error("Failed to load defaults", e);
    }
}

// ── Helpers ──────────────────────────────────────────────────────────

function _setVal(id, value) {
    const el = document.getElementById(id);
    if (el && value !== undefined && value !== null) {
        el.value = value;
    }
}


---

## project_template/engineering_calc_project/webapp/static/js/i18n.js

/**
 * i18n.js — Language toggle and bilingual content management.
 *
 * Replaces text content of elements with data-i18n attributes
 * and toggles bilingual chart visibility on language switch.
 */

let currentLang = "en";
let translations = {};

async function switchLanguage(lang) {
    if (lang === currentLang) return;

    try {
        const resp = await fetch(`/api/i18n/${lang}`);
        if (!resp.ok) return;
        translations = await resp.json();
        currentLang = lang;
    } catch (e) {
        console.warn("Failed to load translations for", lang, e);
        return;
    }

    // Replace text content of all data-i18n elements
    document.querySelectorAll("[data-i18n]").forEach(el => {
        const key = el.getAttribute("data-i18n");
        if (translations[key] !== undefined) {
            el.textContent = translations[key];
        }
    });

    // Replace placeholder attributes
    document.querySelectorAll("[data-i18n-placeholder]").forEach(el => {
        const key = el.getAttribute("data-i18n-placeholder");
        if (translations[key] !== undefined) {
            el.placeholder = translations[key];
        }
    });

    // Toggle bilingual chart visibility
    document.querySelectorAll(".bi-zh, .bi-en").forEach(el => {
        el.style.display = el.classList.contains(`bi-${lang}`) ? "" : "none";
    });

    // Update language toggle button states
    document.querySelectorAll("#langToggle .btn").forEach(btn => {
        btn.classList.toggle("active", btn.dataset.lang === lang);
    });
}

// Initialize language toggle on page load
document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("#langToggle .btn").forEach(btn => {
        btn.addEventListener("click", () => switchLanguage(btn.dataset.lang));
    });
    // Load default language translations
    switchLanguage("en").then(() => { currentLang = "en"; });
});


---

## project_template/engineering_calc_project/webapp/static/js/main.js

/**
 * main.js — Event binding, API calls, and orchestration.
 *
 * This is the central coordinator that ties forms, results, and i18n together.
 */

document.addEventListener("DOMContentLoaded", () => {

    // ── Load defaults on page load ────────────────────────────────────
    fetch("/api/defaults")
        .then(r => r.json())
        .then(data => populateForm(data))
        .catch(e => console.warn("Could not load defaults", e));

    // ── Calculate button ──────────────────────────────────────────────
    const btnCalc = document.getElementById("btnCalculate");
    if (btnCalc) {
        btnCalc.addEventListener("click", async () => {
            btnCalc.disabled = true;
            btnCalc.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span>Calculating...';
            try {
                const data = collectFormData();
                data.lang = currentLang;

                const resp = await fetch("/api/calculate", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify(data),
                });

                const result = await resp.json();
                renderResults(result);

            } catch (e) {
                showError(e.message || "Network error");
            } finally {
                btnCalc.disabled = false;
                btnCalc.innerHTML = `<i class="bi bi-play-fill me-1"></i><span data-i18n="btn_calculate">${translations.btn_calculate || "Run Calculation"}</span>`;
            }
        });
    }

    // ── Report preview button ─────────────────────────────────────────
    const btnPreview = document.getElementById("btnPreviewReport");
    if (btnPreview) {
        btnPreview.addEventListener("click", async () => {
            const modal = document.getElementById("reportModal");
            const frame = document.getElementById("reportFrame");
            const loading = document.getElementById("reportLoading");

            if (!modal || !frame) return;

            // Show modal with loading state
            const bsModal = new bootstrap.Modal(modal);
            bsModal.show();
            if (loading) loading.classList.remove("d-none");
            frame.src = "about:blank";

            try {
                const data = collectFormData();
                data.lang = currentLang;

                const resp = await fetch("/api/report/preview", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify(data),
                });

                const result = await resp.json();
                if (result.status === "ok") {
                    frame.srcdoc = result.html;
                } else {
                    frame.srcdoc = `<p style="padding:2rem;color:red">${result.message}</p>`;
                }
            } catch (e) {
                frame.srcdoc = `<p style="padding:2rem;color:red">Report preview failed.</p>`;
            } finally {
                if (loading) loading.classList.add("d-none");
            }
        });
    }

    // ── Report download button ────────────────────────────────────────
    const btnDownload = document.getElementById("btnDownloadReport");
    if (btnDownload) {
        btnDownload.addEventListener("click", async () => {
            try {
                const data = collectFormData();
                data.lang = currentLang;

                const resp = await fetch("/api/report/html", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify(data),
                });

                if (!resp.ok) throw new Error("Report download failed");
                const blob = await resp.blob();
                const url = URL.createObjectURL(blob);
                const a = document.createElement("a");
                a.href = url;
                a.download = "report.html";
                a.click();
                URL.revokeObjectURL(url);

            } catch (e) {
                alert(e.message);
            }
        });
    }

    // ── Import JSON button ────────────────────────────────────────────
    const btnImport = document.getElementById("btnImportJson");
    const fileInput = document.getElementById("fileImport");

    if (btnImport && fileInput) {
        btnImport.addEventListener("click", () => fileInput.click());

        fileInput.addEventListener("change", async () => {
            const file = fileInput.files[0];
            if (!file) return;

            const formData = new FormData();
            formData.append("file", file);

            try {
                const resp = await fetch("/api/import/json", {
                    method: "POST",
                    body: formData,
                });
                const result = await resp.json();
                if (result.status === "ok") {
                    populateForm(result.data);
                    clearResults();
                } else {
                    alert(result.message || "Import failed");
                }
            } catch (e) {
                alert("Import failed: " + e.message);
            }

            fileInput.value = "";  // Reset for re-import
        });
    }

    // ── Export JSON button ────────────────────────────────────────────
    const btnExport = document.getElementById("btnExportJson");
    if (btnExport) {
        btnExport.addEventListener("click", async () => {
            try {
                const data = collectFormData();
                const resp = await fetch("/api/export/json", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify(data),
                });
                if (!resp.ok) throw new Error("Export failed");
                const blob = await resp.blob();
                const url = URL.createObjectURL(blob);
                const a = document.createElement("a");
                a.href = url;
                a.download = "config.json";
                a.click();
                URL.revokeObjectURL(url);
            } catch (e) {
                alert("Export failed: " + e.message);
            }
        });
    }

    // ── Reset button ──────────────────────────────────────────────────
    const btnReset = document.getElementById("btnReset");
    if (btnReset) {
        btnReset.addEventListener("click", resetToDefaults);
    }

});


---

## project_template/engineering_calc_project/webapp/static/js/results.js

/**
 * results.js — Render calculation results, status badges, and traces.
 *
 * Customize for each calculation book's result structure.
 */

/**
 * Render the full result panel from the API response dict.
 */
function renderResults(data) {
    if (data.status === "error") {
        showError(data.message);
        return;
    }

    hidePlaceholder();

    // Governing summary
    renderGoverning(data.governing);

    // Warnings banner
    if (data.warnings && data.warnings.length > 0) {
        showWarnings(data.warnings);
    }

    // Errors
    if (data.errors && data.errors.length > 0) {
        showErrors(data.errors);
    }

    // Scaffold: render book-specific result sections.
    // if (data.bearing) renderBearingCard(data.bearing);
    // if (data.settlement) renderSettlementCard(data.settlement);
    // if (data.checks) renderChecksTable(data.checks);

    // Enable report preview button
    const btnPreview = document.getElementById("btnPreviewReport");
    if (btnPreview) btnPreview.disabled = false;
}

/**
 * Render the governing status box at the top of the results panel.
 */
function renderGoverning(gov) {
    const box = document.getElementById("governingBox");
    if (!box || !gov) return;

    box.classList.remove("d-none", "alert-success", "alert-danger", "alert-warning");

    const isOk = gov.status === "PASS" || gov.status === "OK";
    box.classList.add(isOk ? "alert-success" : "alert-danger");

    const statusText = isOk
        ? (translations.result_all_pass || "All checks PASS")
        : (translations.result_has_fail || "Some checks FAILED");

    const utilText = gov.utilization !== null && gov.utilization !== undefined
        ? ` | ${translations.result_utilization || "Utilization"}: ${(gov.utilization * 100).toFixed(1)}%`
        : "";

    box.innerHTML = `
        <strong>${statusText}</strong>
        <br>${translations.result_governing || "Governing"}: ${gov.check}${utilText}
    `;
}

/**
 * Format a numeric value for display. Returns '--' for null/undefined.
 */
function fmt(val, decimals = 3) {
    if (val === null || val === undefined) return "—";
    return Number(val).toFixed(decimals);
}

/**
 * Create a status badge HTML element.
 */
function statusBadge(status) {
    const isOk = status === "PASS" || status === "OK";
    const cls = isOk ? "bg-success" : "bg-danger";
    const text = isOk
        ? (translations.result_status_ok || "PASS")
        : (translations.result_status_ng || "FAIL");
    return `<span class="badge ${cls}">${text}</span>`;
}

/**
 * Clear results and show placeholder.
 */
function clearResults() {
    showPlaceholder();
    const box = document.getElementById("governingBox");
    if (box) box.classList.add("d-none");
    const btnPreview = document.getElementById("btnPreviewReport");
    if (btnPreview) btnPreview.disabled = true;
    hideWarnings();
    hideErrors();
}

// ── Placeholder / Warning / Error helpers ────────────────────────────

function hidePlaceholder() {
    const el = document.getElementById("resultsPlaceholder");
    if (el) el.classList.add("d-none");
}

function showPlaceholder() {
    const el = document.getElementById("resultsPlaceholder");
    if (el) el.classList.remove("d-none");
}

function showWarnings(warnings) {
    // Scaffold: render warning banner
    console.warn("Calculation warnings:", warnings);
}

function hideWarnings() {}

function showErrors(errors) {
    console.error("Calculation errors:", errors);
}

function hideErrors() {}

function showError(message) {
    const box = document.getElementById("governingBox");
    if (box) {
        box.classList.remove("d-none", "alert-success");
        box.classList.add("alert-danger");
        box.innerHTML = `<strong>Error:</strong> ${message}`;
    }
}


---

## project_template/engineering_calc_project/webapp/templates/base.html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title data-i18n="app_title">Engineering Calculator</title>
    <!-- Bootstrap 5 CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css" rel="stylesheet">
    <!-- KaTeX for formula rendering (optional) -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
    <!-- Custom styles -->
    <link rel="stylesheet" href="static/css/style.css">
    {% block head %}{% endblock %}
</head>
<body>
    <!-- ─── Navbar (Top Bar) ────────────────────────────────────────── -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary-gradient sticky-top shadow-sm">
        <div class="container-fluid">
            <a class="navbar-brand d-flex align-items-center" href="./">
                <i class="bi bi-calculator me-2"></i>
                <span class="fw-bold" data-i18n="app_title">Engineering Calculator</span>
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarContent">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarContent">
                <ul class="navbar-nav me-auto">
                    <li class="nav-item">
                        <button class="btn btn-outline-light btn-sm me-2 mt-1" id="btnImportJson" data-i18n="nav_import">
                            Import JSON
                        </button>
                    </li>
                    <li class="nav-item">
                        <button class="btn btn-outline-light btn-sm me-2 mt-1" id="btnExportJson" data-i18n="nav_export">
                            Export JSON
                        </button>
                    </li>
                </ul>
                <div class="d-flex align-items-center gap-2">
                    <!-- Language toggle -->
                    <div class="btn-group btn-group-sm" role="group" id="langToggle">
                        <button type="button" class="btn btn-outline-light active" data-lang="en">EN</button>
                        <button type="button" class="btn btn-outline-light" data-lang="zh">中文</button>
                    </div>
                    <!-- Report preview button -->
                    <button class="btn btn-warning btn-sm fw-bold" id="btnPreviewReport" disabled>
                        <i class="bi bi-file-earmark-text me-1"></i>
                        <span data-i18n="nav_preview">Preview Report</span>
                    </button>
                </div>
            </div>
        </div>
    </nav>

    <!-- ─── Main content ────────────────────────────────────────────── -->
    <main class="container-fluid py-3">
        {% block content %}{% endblock %}
    </main>

    <!-- ─── Report Preview Modal ────────────────────────────────────── -->
    <div class="modal fade" id="reportModal" tabindex="-1">
        <div class="modal-dialog modal-xl modal-dialog-scrollable">
            <div class="modal-content">
                <div class="modal-header bg-light">
                    <h5 class="modal-title" data-i18n="report_title">Calculation Report</h5>
                    <div class="d-flex gap-2">
                        <button class="btn btn-primary btn-sm" id="btnDownloadReport">
                            <i class="bi bi-download me-1"></i>
                            <span data-i18n="btn_download_report">Download</span>
                        </button>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                </div>
                <div class="modal-body p-0">
                    <div id="reportLoading" class="text-center py-5 d-none">
                        <div class="spinner-border text-primary" role="status"></div>
                        <p class="mt-2 text-muted" data-i18n="report_generating">Generating report...</p>
                    </div>
                    <iframe id="reportFrame" class="w-100 border-0" style="min-height: 80vh;"></iframe>
                </div>
            </div>
        </div>
    </div>

    <!-- Hidden file input for JSON import -->
    <input type="file" id="fileImport" accept=".json" class="d-none">

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
    <!-- App JS modules (order matters: i18n first, then forms, results, main) -->
    <script src="static/js/i18n.js"></script>
    <script src="static/js/forms.js"></script>
    <script src="static/js/results.js"></script>
    <script src="static/js/main.js"></script>
    {% block scripts %}{% endblock %}
</body>
</html>


---

## project_template/engineering_calc_project/webapp/templates/index.html

{% extends "base.html" %}

{% block content %}
<div class="row g-3">
    <!-- ─── LEFT PANEL: Input Forms ─────────────────────────────── -->
    <div class="col-lg-4 col-xl-3">
        <div class="input-panel">
            <!-- Project Info -->
            <div class="card mb-3 shadow-sm">
                <div class="card-header"><h6 class="mb-0" data-i18n="section_project">Project Information</h6></div>
                <div class="card-body">
                    <div class="mb-2">
                        <label class="form-label small" data-i18n="project_id">Project ID</label>
                        <input type="text" class="form-control form-control-sm" id="project_id" value="EXAMPLE_001">
                    </div>
                    <div class="mb-2">
                        <label class="form-label small" data-i18n="project_name">Project Name</label>
                        <input type="text" class="form-control form-control-sm" id="project_name" value="">
                    </div>
                    <div class="mb-2">
                        <label class="form-label small" data-i18n="case_id">Case ID</label>
                        <input type="text" class="form-control form-control-sm" id="case_id" value="CASE_001">
                    </div>
                    <!-- Scaffold: add book-specific input cards here -->
                </div>
            </div>

            <!-- Scaffold: add more input cards (foundation, loads, options, etc.) -->

            <!-- Calculate button (sticky bottom) -->
            <div class="sticky-bottom bg-white border-top p-3 mt-3">
                <button class="btn btn-primary btn-lg w-100 fw-bold shadow-sm" id="btnCalculate">
                    <i class="bi bi-play-fill me-1"></i>
                    <span data-i18n="btn_calculate">Run Calculation</span>
                </button>
            </div>
        </div>
    </div>

    <!-- ─── RIGHT PANEL: Results ────────────────────────────────── -->
    <div class="col-lg-8 col-xl-9">
        <div id="resultsPanel" class="results-panel">
            <!-- Placeholder -->
            <div id="resultsPlaceholder" class="text-center py-5">
                <div class="mb-3">
                    <i class="bi bi-clipboard2-data display-1 text-muted"></i>
                </div>
                <h4 class="text-muted" data-i18n="result_placeholder">Click "Run Calculation" to see results.</h4>
            </div>

            <!-- Governing status box (hidden until calculated) -->
            <div id="governingBox" class="alert d-none mb-3" role="alert"></div>

            <!-- Scaffold: add book-specific result cards here -->
            <!-- Each card follows the pattern:
            <div id="xxxSection" class="card result-card mb-3 shadow-sm d-none">
                <div class="card-header result-card-header" data-bs-toggle="collapse" data-bs-target="#collapseXxx">
                    <h6 class="mb-0">
                        <i class="bi bi-icon me-2"></i>
                        <span data-i18n="result_xxx">Section Title</span>
                        <span class="float-end" id="xxxStatusBadge"></span>
                    </h6>
                </div>
                <div id="collapseXxx" class="collapse show">
                    <div class="card-body py-2" id="xxxBody"></div>
                </div>
            </div>
            -->
        </div>
    </div>
</div>
{% endblock %}


---

## README.md

# Engineering Calculation System Skill Pack v2.2.0

This package organizes engineering calculation software development into a full delivery lifecycle:

```text
reference acquisition and local persistence
-> reference analysis and calculation logic blueprint
-> implementation, reporting, batch execution, verification, traceability, release, and Linux cloud deployment
```

The implementation stage now includes a unified interface pattern:

```text
polished frontend with left-side inputs and right-side review results
Marimo review pages for module-level inspection and draft edits
managed data/report import and uploadable calculation packages
runnable local web client and Linux-cloud deployable web service
```

v2.2.0 splits the interface layer into a lightweight router plus three focused subskills:

```text
12  report/review/batch interface router
12a report context and rendering
12b frontend and review interfaces
12c batch, import/export, and upload packages
14  cloud web release and Linux deployment
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
12 report review batch interface router
12a report context and rendering
12b frontend and review interfaces
12c batch import/export packages
13 verification regression traceability
14 cloud web release deployment
```

## Parent skills

```text
parent/engineering-calculation-reference-acquisition.skill.md
parent/engineering-calculation-logic-architecture.skill.md
parent/engineering-calculation-book.skill.md
```

## Agent entrypoints

Use `SKILL.md` as the root skill entrypoint for Codex-compatible environments. Qoder-compatible files are included under `.qoder/`. Trae-compatible project rules are included under `.trae/rules/`. For other agents, see:

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
implementation/02_modules/module_asset_registry.csv
deploy/
release/release_checklist.md
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

# 工程计算系统技能包 v2.2.0

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
→ 12-report-review-batch-interfaces（接口层路由）
→ 12a-report-context-and-rendering（报告上下文与渲染）
→ 12b-frontend-and-review-interfaces（前端与审查界面）
→ 12c-batch-import-export-packages（批量、导入导出、上传包）
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

其中 Qoder 适配文件位于 `.qoder/`，Trae 项目规则入口位于 `.trae/rules/engineering-calc-system.md`。

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
agents/
adapters/
parent/
skills/
shared/
templates/
schemas/
scripts/
```

跨 Agent 可选目录：

```text
.qoder/
.trae/
project_template/
examples/
workflow_diagrams/
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
version: 2.2.0
created_at: 2026-06-16
status: complete_packaged_release
```


---

## schemas/artifact_contracts.json

{
  "version": "2.2.0",
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
    "templates/implementation/module_asset_registry.csv",
    "templates/implementation/data_package_manifest.yaml",
    "templates/deployment/cloud_linux_deployment.md",
    "templates/deployment/release_checklist.md",
    "templates/deployment/runtime_env.example",
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
    "skills/12a-report-context-and-rendering.skill.md",
    "skills/12b-frontend-and-review-interfaces.skill.md",
    "skills/12c-batch-import-export-packages.skill.md",
    "skills/13-verification-regression-traceability.skill.md",
    "skills/14-cloud-web-release-deployment.skill.md",
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
    "templates/implementation/module_asset_registry.csv": "module_id,domain,category,module_name,public_function,input_model,options_model,result_model,source_references,formula_trace_path,unit_tests,regression_tests,reuse_status,asset_owner,notes",
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
      "Interface Subskills",
      "Required Interface Decision Record",
      "Report Status Labels"
    ],
    "skills/12a-report-context-and-rendering.skill.md": [
      "Report Production Decision",
      "Report Status",
      "Production Minimum",
      "Template Boundaries"
    ],
    "skills/12b-frontend-and-review-interfaces.skill.md": [
      "Unified Frontend Layout",
      "Form and API Contract",
      "Marimo Review Apps"
    ],
    "skills/12c-batch-import-export-packages.skill.md": [
      "Managed Data Area",
      "Upload Package Flow",
      "Batch Flow"
    ],
    "skills/14-cloud-web-release-deployment.skill.md": [
      "Release Targets",
      "Production Web Minimum",
      "Linux Deployment Rules"
    ],
    "templates/implementation/ui_layout_spec.md": [
      "Standard Page Zones",
      "Left input panel",
      "Right review workbench",
      "Deployment Entry"
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
    "templates/deployment/cloud_linux_deployment.md": [
      "Runtime Target",
      "Deployment Sequence",
      "Health and Smoke Tests"
    ],
    "templates/deployment/release_checklist.md": [
      "Required Gates",
      "Release Artifacts",
      "Smoke Test Record"
    ],
    "templates/implementation/report_context_spec.md": [
      "Report Production Decision Record",
      "Production Eligibility",
      "Traceability",
      "Template Boundaries"
    ],
    "templates/verification/acceptance_checklist.md": [
      "Report production decision is recorded",
      "Report status is explicit",
      "module_asset_registry.csv",
      "Cloud Linux deployment path"
    ],
    "shared/quality-gates.md": [
      "Report production gate",
      "report production decision recorded",
      "Release and deployment gate"
    ]
  },
  "project_required_paths": [
    "README.md",
    "pyproject.toml",
    "tests/conftest.py",
    "implementation/02_modules/module_asset_registry.csv",
    "deploy/env.example",
    "deploy/Dockerfile",
    "deploy/docker-compose.yml",
    "deploy/systemd/engineering-calc.service",
    "deploy/nginx/engineering-calc.conf",
    "release/release_checklist.md",
    "tests/smoke/example_input.json",
    "webapp/__init__.py",
    "webapp/app.py",
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
    "implementation/02_modules/module_asset_registry.csv": "module_id,domain,category,module_name,public_function,input_model,options_model,result_model,source_references,formula_trace_path,unit_tests,regression_tests,reuse_status,asset_owner,notes",
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
reusable modules are decoupled and registered as assets
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

## Release and deployment gate

Before labeling an online web calculation program as complete, production-ready, or deployable:

```text
local web client run command documented and smoke-tested
cloud Linux deployment path documented
web app exposes a health endpoint
production server entrypoint exists
environment variables control secrets, debug mode, host, port, data, and output paths
Dockerfile or systemd service exists when cloud deployment is required
nginx or platform proxy guidance exists when the app is internet-facing
calculation modules remain independent from web, report, batch, and deployment layers
module_asset_registry.csv records reusable calculation assets
release checklist records smoke tests and remaining assumptions
```

If any release item is missing, use `review`, `deployment_blocked`, or `not_production_ready`.


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
description: Full lifecycle workflow for engineering calculation software. Use when Codex or another coding agent must assess missing engineering references, acquire and persist source evidence, transform references into a Calculation Logic Blueprint, create an implementation handoff, build decoupled reusable calculation modules, build auditable web calculation software, verify formulas, reports, batch flows, and traceability, or package a runnable local and Linux-cloud deployable online calculator.
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

Do not label a system complete unless reusable calculation modules are decoupled, traceable, independently testable, and recorded for future reuse.

Do not label a web calculation system production-ready unless it has local run instructions, a Linux cloud deployment path, environment-based configuration, smoke tests, and release artifacts.

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
description: Route engineering calculation tasks to the correct reference acquisition, reference analysis, handoff, implementation, reporting, batch, verification, reusable-module, or cloud-web release skill. Use whenever the user request spans multiple stages, lacks source materials, has unclear source sufficiency, or when it is unclear whether to find references, analyze references, write code, refactor, generate reports, test, package, or deploy a runnable online calculator.
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
| `analysis_handoff_available` | Implementation handoff and coding gate exist | 08 -> 09 -> 10 -> 11 -> 13, plus 12 if interfaces needed, plus 14 for deployable web delivery |
| `codebase_available` | Existing implementation exists | classify bug/feature by layer, then route to 08-14 |

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
| Build or refactor engineering calculation software | 08 -> 09 -> 10 -> 11 -> 13, plus 12 if needed, plus 14 when final delivery is expected |
| Build reusable or asset-ready calculation modules | 08 -> 10 -> 13, record module assets |
| Build typed models only | 09 |
| Build reusable formula/calculation module | 10, plus 13 |
| Build official calculation book runner | 11, plus 13 |
| Build report, review UI, CLI, API, or batch flow | 12, then 12a/12b/12c as needed, plus 13 smoke tests |
| Add tests, regression, traceability, hash, quality gates | 13 |
| Package, release, run locally, deploy to cloud/Linux, Docker, systemd, nginx, online web calculator | 14, after 12b and 13 when web UI/API exists |
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
Does the final output need to be a runnable online web calculation program?
Does deployment target Linux, Docker, systemd, nginx, or another cloud runtime?
Do calculation modules need to become reusable assets for later projects?
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
description: Design the project and package architecture for a reusable engineering calculation book system from a validated implementation handoff, including feature classification, dependency rules, decoupled reusable module boundaries, module asset registry, package layout, deployment layout, and file placement.
---

# Calculation Book Architecture

Use this skill as the first implementation-stage skill.

## Goal

Design the software architecture before writing formulas or interfaces.

Plan reusable modules as long-lived assets, not book-local helpers.

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
release / deployment
```

## Reusable Module Boundaries

Before coding, define which engineering logic belongs in reusable libraries and which orchestration belongs in book runners.

Reusable library modules must:

```text
be independent from a specific web page, report, batch job, database, or file layout
expose typed input/options/result models
own source-backed formulas, lookup behavior, and intermediate values
return warnings/errors instead of hiding assumptions
be registered in module_asset_registry.csv
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
  deploy/
    nginx/
    systemd/
  release/
  tests/
  verification/
```

## Required Output Artifacts

```text
implementation/00_architecture/project_structure.md
implementation/00_architecture/feature_classification.csv
implementation/00_architecture/dependency_rules.md
implementation/00_architecture/package_layout.md
implementation/02_modules/module_asset_registry.csv
```

## Required Final Response

Provide:

```text
architecture decision
feature classification
project tree
layer placement
forbidden dependencies
module asset boundaries
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
description: Implement or design decoupled reusable engineering calculation modules from the implementation handoff, with typed inputs/outputs, stable public functions, module asset registration, formula traces, lookup behavior, warnings/errors, no file I/O, no UI/report/deployment dependency, and unit/regression tests.
---

# Reusable Calculation Modules

Use this skill to implement domain formulas and lookup logic.

## Goal

Build reusable, independently testable engineering modules.

Treat each module as an accumulating engineering asset that can be reused by later books, web apps, batch jobs, and reports through the same public interface.

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
be recorded in module_asset_registry.csv
```

## Forbidden

Do not read CSV, render reports, access UI state, write batch summaries, call a book runner, open deployment files, read environment variables, or depend on a web framework from a reusable formula module.

## Asset Registry

Record every reusable module with:

```text
module_id
domain and category
module name
stable public function
input/options/result models
source references
formula trace path
unit and regression test paths
reuse status: draft / reviewed / stable / deprecated
asset owner or maintainer
```

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
implementation/02_modules/module_asset_registry.csv
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
asset registry row
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
description: Route and govern report, frontend, review, API, import/export, upload-package, batch, and deployable-web interface work over a trusted engineering calculation book runner and BookResult. Use when the task needs presentation, review, report rendering, operational UI, data package, API, CLI, batch workflows, or a final runnable online web calculator while keeping formulas and independent pass/fail logic out of interface layers.
---

# Report, Review, Batch, and Interface Router

Use this skill after `run_book()` and `BookResult` exist or are specified.

This skill selects the correct interface subskill and enforces the shared interface rules. Load only the subskill needed by the user request.

When the interface must become a deployable online web calculator, route to Skill 14 after frontend/API verification.

## Core Principle

Interfaces consume trusted calculation outputs. They do not become calculation engines.

Never place engineering formulas, lookup rules, branch decisions, load-combination logic, or independent pass/fail decisions in:

```text
UI code
frontend JavaScript
review notebooks
report templates
batch scripts
CSV/XLSX input files
presentation-only code
```

All official paths must call:

```python
run_book(BookInput) -> BookResult
```

## Interface Subskills

Select one or more:

```text
12a-report-context-and-rendering
  Use for ReportContext design, report production decisions, renderer choice, templates, preview, HTML/PDF/DOCX/XLSX/JSON exports, report status, and template boundaries.

12b-frontend-and-review-interfaces
  Use for production web UI, form-to-model mapping, API route shape, frontend JavaScript structure, i18n, charts, numeric sanitization, and Marimo review apps.

12c-batch-import-export-packages
  Use for managed data areas, report import, upload packages, import/export manifests, hashes, package validation, CLI/API batch runs, and batch summaries.

14-cloud-web-release-deployment
  Use after 12b and 13 when the user expects a runnable local and cloud-deployable online web calculator.
```

If the request spans all three families, read them in this order:

```text
12a -> 12b -> 12c -> 13 -> 14 when final web release is expected
```

## Shared Interface Contract

Every interface family must preserve:

```text
BookInput path mapping
BookResult or ReportContext result paths
source basis and limitations
warnings, errors, assumptions, and prototype status
input hash and result hash when persisted
runner version and report/template version when available
stable export paths
smoke tests for each user-facing path
```

## Report Status Labels

Use explicit status:

```text
draft
review
final
superseded
prototype
not_for_construction
```

Do not label a report or interface output `final` unless the coding gate allows production work, the source basis is sufficient, the output is generated from saved final input or trusted saved `BookResult`, and verification has passed.

## Required Interface Decision Record

Before implementation, record:

```text
requested interface family
consumed BookInput / BookResult / ReportContext
runner entrypoint
source of saved input/result
report or interface status
chosen templates or UI pattern
import/export or batch scope
release/deployment scope when final web delivery is expected
verification method
known limitations
selected subskills
```

Use templates from:

```text
templates/implementation/input_mapping_spec.md
templates/implementation/ui_layout_spec.md
templates/implementation/report_context_spec.md
templates/implementation/import_export_contract.md
templates/implementation/marimo_review_spec.md
templates/implementation/batch_flow.md
templates/implementation/data_package_manifest.yaml
templates/deployment/cloud_linux_deployment.md
templates/deployment/release_checklist.md
```

## Required Final Response

Provide:

```text
selected interface subskills
which runner is called
which BookInput, BookResult, or ReportContext is consumed
status and production eligibility
proof that formulas are not in UI/report/Marimo/batch
created or updated artifact paths
smoke test or validation command
release/deployment command when final web delivery is expected
remaining limitations
```


---

## skills/12a-report-context-and-rendering.skill.md

---
name: report-context-and-rendering
description: Design and implement source-backed engineering calculation report context, report production decisions, renderer choices, report templates, report preview, and HTML/PDF/DOCX/XLSX/JSON exports over trusted BookResult data. Use when building reports or report previews while keeping templates free of engineering formulas and independent pass/fail logic.
---

# Report Context and Rendering

Use this skill for report production after `run_book()` and `BookResult` exist or are specified.

## Goal

Create reports from a structured `ReportContext` that wraps trusted calculation results without recalculating engineering outcomes.

Required flow:

```text
saved final input or trusted saved BookResult
-> build_report_context()
-> renderer/template
-> report output
-> optional preview or package export
```

## Report Production Decision

Before rendering, record:

```text
report purpose
intended audience
review depth
report status
required output formats
governing source basis
saved input/result source
required traceability metadata
renderer choice and reason
required report sections
verification method
known limitations
```

Use `templates/implementation/report_context_spec.md`.

## Report Status

Use explicit report status labels from Skill 12. Do not mark reports `final` until source basis, coding gate, saved input/result, and verification state all support production use.

## ReportContext Contents

Include when applicable:

```text
project and case metadata
report production decision
report status and output target
design basis and source references
input summary
assumptions and limitations
module summaries
governing summary
checks and stable result paths
intermediate values selected for audit
warnings and errors
formula traces or source trace references
imported report comparison metadata
data package metadata
appendix data
traceability metadata
```

## Template Boundaries

Templates may contain:

```text
value references
loops and conditionals
formatting filters
section visibility logic
unit display formatting
cross-references
```

Templates must not contain:

```text
engineering formulas
lookup rules
load-combination generation
optimization logic
independent unit conversion for official calculations
independent pass/fail logic
```

## Renderer Choice

Choose the simplest renderer that satisfies the output requirement:

```text
HTML for preview and browser-native review
PDF for frozen deliverables
DOCX for editable client/report workflows
XLSX for tabular export or audit appendices
JSON for machine-readable packages
```

The chosen renderer must preserve warnings, limitations, source basis, report status, and traceability metadata.

## Production Minimum

A production report workflow must have:

```text
recorded report production decision
explicit report status
saved final input or trusted saved BookResult
clear source basis and limitations
structured ReportContext
template boundary proof
warnings and errors preserved in output
traceability metadata preserved
smoke test for each renderer or export path
documented run command
```

If any item is missing, label the report `draft`, `review`, `prototype`, or `not_for_construction`.

## Required Final Response

Provide:

```text
ReportContext fields
renderer choice and reason
report status
saved input/result source
template boundary proof
output paths
smoke test
remaining limitations
```


---

## skills/12b-frontend-and-review-interfaces.skill.md

---
name: frontend-and-review-interfaces
description: Build production web UIs, API routes, form-to-model mapping, frontend JavaScript modules, i18n, charts, numeric sanitization, and Marimo review apps for engineering calculation books. Use when creating operational review interfaces over run_book(), BookInput, BookResult, and ReportContext while keeping formulas out of presentation and review layers.
---

# Frontend and Review Interfaces

Use this skill when the user needs an operational UI, API, review notebook, or module review surface.

## Goal

Create interfaces that make engineering review efficient while remaining thin over trusted calculation modules.

Recommended interface families:

```text
production frontend: browser UI for inputs, calculation, report preview, import/export, and review
Marimo review app: Python-native module inspection, draft edits, traces, and what-if review
API route layer: thin parse -> model -> run_book -> UI/result conversion endpoints
```

## Deployment-Ready Web App Minimum

For production web delivery, include:

```text
webapp/app.py or equivalent application factory
create_app() entrypoint for gunicorn or platform runtime
GET /health endpoint for deployment smoke tests
environment-based host, port, secret, debug, data, and output paths
local run command such as python -m webapp.app
production run command such as gunicorn "webapp.app:create_app()"
```

## Unified Frontend Layout

Use this layout unless an existing product design overrides it:

```text
top bar:
  book/project title, case selector, report status, import/export, report preview, language switch

left input panel:
  grouped BookInput forms, units, validation feedback, sticky run/save controls

right review workbench:
  governing summary, warnings/errors, result tables/cards, charts, source traces, formula traces

modal or drawer:
  report preview, imported report comparison, source trace, formula trace, package validation, input/result diff

status strip:
  input hash, result hash, runner version, report template version, package id, timestamp
```

Use `templates/implementation/ui_layout_spec.md`.

## Form and API Contract

Create explicit conversion functions:

```text
form_to_model(data: dict) -> BookInput
model_to_form(model: BookInput) -> dict
result_to_ui(result: BookResult) -> dict
```

Rules:

```text
place conversion in a dedicated mapping module
keep route handlers thin
use explicit field-by-field mapping
validate required fields before runner calls
sanitize NaN and Infinity before JSON responses
preserve unit conversion at input/output boundaries only
record mapping decisions in form_mapping_spec.md
```

Use `templates/implementation/form_mapping_spec.md` and `templates/implementation/api_route_skeleton.md`.

## Frontend JavaScript

Keep JavaScript focused:

```text
forms.js: collect, populate, reset, validate, dynamic lists
results.js: render summaries, status badges, utilization bars, trace expansion
i18n.js: language switching and data-i18n replacement
main.js: API calls, event binding, loading states, orchestration
```

Do not calculate engineering results in JavaScript.

## i18n, Sanitization, and Charts

Use i18n when the project serves multilingual engineers or clients:

```text
single translation dictionary
data-i18n attributes
/api/i18n/<lang> endpoint
bilingual chart variants when needed
```

Use a recursive sanitizer for non-finite numeric values. Display sanitized values as `--` or `N/A` and preserve warnings.

Generate charts from already-computed `BookResult` values. Charts visualize; they do not calculate.

Use:

```text
templates/implementation/i18n_pattern.md
templates/implementation/chart_integration.md
src/<pkg>/core/sanitize.py or equivalent
```

## Marimo Review Apps

Use Marimo when reviewers need interactive module-level inspection.

Create apps under:

```text
apps/review/<book_name>_review.py
apps/review/modules/<module_name>_review.py
```

Each review app should expose:

```text
case/package loader
module selector
editable draft inputs
run selected module or full run_book()
governing result and warnings/errors
input/result diff
formula traces and source references
review notes and decision
save draft input or module review log
```

Label exploratory edits as `draft`, `review`, or `prototype` until saved, rerun through the official path, and verified.

Use `templates/implementation/marimo_review_spec.md`.

## Required Final Response

Provide:

```text
layout summary
mapping module and functions
API route table
frontend module breakdown
i18n/sanitization/chart decisions
Marimo review scope if used
proof that UI and review layers do not calculate
smoke test
run command
deployment-ready entrypoint when final delivery is expected
```


---

## skills/12c-batch-import-export-packages.skill.md

---
name: batch-import-export-packages
description: Design and implement managed import/export, uploaded calculation packages, prior report import, hashes, manifests, CLI/API batch execution, saved normalized inputs, saved BookResult JSON, report exports, and batch summaries for engineering calculation books. Use when building repeatable package, data exchange, or batch workflows over trusted run_book() results.
---

# Batch, Import/Export, and Upload Packages

Use this skill when the task involves data packages, imported reports, export bundles, batch runs, or automated case processing.

## Goal

Make engineering calculation inputs, results, reports, and review artifacts portable and repeatable without moving formulas into data files or batch scripts.

## Managed Data Area

Use a predictable data layout:

```text
data/input/                  user-provided input files
data/imported/reports/       prior reports used for review or comparison
data/imported/references/    allowed project reference files
data/staging/                uploaded but not yet accepted files
data/normalized/cases/       normalized BookInput JSON per case
data/packages/               unpacked upload/export packages
outputs/results_json/        trusted BookResult JSON
outputs/reports_html/        generated HTML reports
outputs/reports_pdf/         generated PDF reports
outputs/reports_docx/        generated DOCX reports
outputs/upload_packages/     ZIP or folder packages ready to share/upload
outputs/logs/                run and validation logs
```

Use `templates/implementation/import_export_contract.md` and `templates/implementation/data_package_manifest.yaml`.

## Upload Package Flow

Required flow:

```text
upload ZIP or files
-> store in data/staging/
-> compute hashes and inspect manifest
-> classify inputs, reports, references, and outputs
-> normalize accepted inputs into BookInput JSON
-> show validation and diff summary
-> run_book only after case selection or batch approval
-> save BookResult JSON
-> render requested reports
-> export package with manifest and hashes
```

Imported reports are review artifacts. They may support comparison or regression evidence, but they must not inject formulas or override official status.

## Batch Flow

Use this sequence:

```text
read batch_control.csv or package manifest
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

Use `templates/implementation/batch_flow.md`.

## Manifest and Hash Rules

Every package should record:

```text
package id
schema version
created timestamp
project/book name
input files and hashes
result files and hashes
report files and hashes
runner version
template version
source basis references
validation status
known limitations
```

Do not accept a package as trusted if required hashes, runner version, source basis, or validation status are missing.

## CLI/API Rules

Batch CLI and API endpoints may:

```text
load package manifests
validate files and hashes
normalize BookInput JSON
call run_book()
save BookResult JSON
render reports
write summaries
export packages
```

They must not:

```text
implement formulas
recalculate pass/fail status
silently override saved final inputs
hide warnings/errors
treat imported reports as source of truth
```

## Required Final Response

Provide:

```text
managed data paths
package manifest fields
import/export flow
batch sequence
hash and trust rules
created or updated artifacts
proof that batch/import layers do not calculate
smoke test
run command
```


---

## skills/13-verification-regression-traceability.skill.md

---
name: verification-regression-traceability
description: Design and implement verification, regression tests, tolerance policy, formula trace checks, module asset checks, input/result hashes, report smoke tests, web/API smoke tests, Marimo review smoke tests, upload package checks, batch summary checks, deployment smoke tests, and acceptance gates for engineering calculation book systems.
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
web/API smoke tests
Marimo review smoke tests
upload/import package manifest and hash tests
batch smoke tests
serialization and hash tests
deployment smoke tests for local and Linux cloud release paths
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
release/release_checklist.md when final delivery is expected
```

## Acceptance Checklist

Verify:

```text
source basis is recorded
features are classified into layers
formulas live only in reusable calculation modules
reusable modules are listed in module_asset_registry.csv
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
web app health and calculate API smoke tests exist when frontend/API exists
deployment smoke tests or explicit deployment blockers are recorded when final delivery is expected
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

## skills/14-cloud-web-release-deployment.skill.md

---
name: cloud-web-release-deployment
description: Package and verify a production-ready engineering calculation web application for local operation and Linux cloud deployment. Use after implementation and verification, or when the user asks for a runnable online calculator, cloud deployment, Linux server deployment, Docker/systemd/nginx packaging, release artifacts, operations runbook, local client package, or final deployable delivery.
---

# Cloud Web Release and Deployment

Use this skill as the final delivery stage for engineering calculation software.

## Goal

Produce a runnable, traceable, reviewable, modifiable, and Linux-deployable web calculation program.

The release is not complete until a fresh operator can run the app locally, inspect traces and source basis, modify decoupled calculation modules, and deploy the same calculation path to a Linux server.

## Required Inputs

```text
handoff/implementation_handoff.yaml
implementation/00_architecture/dependency_rules.md
implementation/02_modules/module_asset_registry.csv
verification/acceptance_checklist.md
webapp/ or src/<pkg>/interfaces/webapp/
tests/
```

Do not package as production-ready if verification failed, source basis is missing, or the web/API layer calculates outside `run_book()`.

## Release Targets

Provide both targets unless the user explicitly narrows scope:

```text
local web client: runs on the user's machine and opens in a browser
cloud Linux web service: runs behind gunicorn on a Linux server, optionally with nginx, systemd, or Docker
```

For a desktop installer, add Electron, Tauri, PyInstaller, or a native wrapper only when the user requests a true desktop client. Otherwise the local client is the same browser UI served locally.

## Production Web Minimum

The application must include:

```text
application factory such as create_app()
health endpoint for deployment smoke tests
thin API routes that call run_book()
explicit form_to_model and result_to_ui mapping
static/templates or SPA bundle needed by the browser UI
environment-based configuration
non-debug production defaults
structured error responses that preserve server logs
```

## Deployment Package Contents

Create or update:

```text
deploy/env.example
deploy/Dockerfile or deploy/systemd/*.service
deploy/nginx/*.conf when reverse proxy is expected
deploy/docker-compose.yml when Docker is used
release/release_checklist.md
release/runbook.md when operational handoff is needed
```

The release package must document:

```text
local run command
Linux production run command
required environment variables
port and host binding
data/output persistence paths
log location
backup/export strategy for inputs, results, reports, and packages
health check command
rollback or stop command
```

## Module Asset Requirements

Before release, confirm reusable calculation modules are asset-ready:

```text
each module has stable module_id and public function
inputs/options/results are typed
module owns formulas and lookup behavior only
module has no web, report, batch, file-system, or database dependency
source references and formula traces are recorded
unit and regression tests cover the module
reuse status is recorded in module_asset_registry.csv
```

## Linux Deployment Rules

For Linux server deployment:

```text
run with gunicorn or an equivalent production WSGI/ASGI server
bind the app service to an internal host/port unless intentionally exposed
put TLS, compression, and public routing in nginx or the platform proxy
read secrets from environment variables or server secret storage
write generated outputs only to configured data/output directories
make logs visible to journald, container logs, or configured log files
disable debug mode
```

## Smoke Tests

Run or define smoke tests for:

```text
python -m webapp.app or equivalent local start
GET /health
GET /
POST /api/calculate with a known input
report preview or export when present
Docker build/run or systemd command syntax when provided
artifact validation script
```

If the current environment cannot start Docker, systemd, or nginx, still validate file presence, command syntax where possible, and provide the exact unrun command plus the reason it was not executed.

## Required Final Response

Provide:

```text
release targets produced
local run command
cloud Linux deployment command
deployment files created or updated
module asset registry status
traceability and review evidence
smoke test results
remaining deployment assumptions
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

## templates/deployment/cloud_linux_deployment.md

# Cloud Linux Deployment Plan

Use this template for production deployment of an engineering calculation web application.

## Runtime Target

| Item | Selected Value | Notes |
| --- | --- | --- |
| Application entrypoint | `webapp.app:create_app()` | Must call the same `run_book()` path as local/API/batch. |
| Server | gunicorn / uvicorn / platform WSGI-ASGI server | Use production server, not Flask debug server. |
| Reverse proxy | nginx / platform proxy / none | Required when exposing to public internet. |
| Host binding | `127.0.0.1` behind proxy or `0.0.0.0` in container | Avoid unintended exposure. |
| Port | to_be_defined | Record firewall and proxy routing. |
| OS | Linux | Record distro/version when known. |

## Required Files

```text
deploy/env.example
deploy/Dockerfile or deploy/systemd/<service>.service
deploy/nginx/<site>.conf when nginx is used
deploy/docker-compose.yml when Docker is used
release/release_checklist.md
```

## Environment Variables

| Variable | Required | Example | Purpose |
| --- | --- | --- | --- |
| `APP_HOST` | true | `0.0.0.0` | Service bind host. |
| `APP_PORT` | true | `5000` | Service bind port. |
| `FLASK_DEBUG` | true | `0` | Must be `0` in production. |
| `SECRET_KEY` | true | server secret | Never commit real production secret. |
| `DATA_DIR` | false | `/var/lib/engineering-calc/data` | Persistent inputs/imports. |
| `OUTPUT_DIR` | false | `/var/lib/engineering-calc/outputs` | Persistent results/reports/packages. |

## Deployment Sequence

```text
prepare Linux host or container runtime
copy release package or pull repository
create virtualenv or build container image
install dependencies
configure environment variables
start gunicorn service
configure nginx or platform proxy when public
run health check
run known POST /api/calculate smoke case
record release status
```

## Health and Smoke Tests

```text
curl -fsS http://127.0.0.1:5000/health
curl -fsS http://127.0.0.1:5000/
curl -fsS -X POST http://127.0.0.1:5000/api/calculate \
  -H "Content-Type: application/json" \
  --data @tests/smoke/example_input.json
```

## Production Rules

```text
debug mode disabled
secrets not committed
logs routed to journald, container logs, or configured log path
generated outputs written to configured persistent directory
calculation modules remain independent from web/deploy layers
deployment smoke test result recorded in release/release_checklist.md
```


---

## templates/deployment/release_checklist.md

# Release Checklist

## Release Identity

| Item | Value |
| --- | --- |
| Release ID | to_be_defined |
| Project/book | to_be_defined |
| Version | to_be_defined |
| Git commit or source snapshot | to_be_defined |
| Release status | draft / review / production_ready / blocked |

## Required Gates

- [ ] Source basis and implementation handoff are recorded.
- [ ] Calculation modules are decoupled and listed in `module_asset_registry.csv`.
- [ ] Official calculation path is `run_book(BookInput) -> BookResult`.
- [ ] Web/API/report/batch layers do not implement formulas or independent pass/fail logic.
- [ ] Unit, regression, integration, interface, and smoke tests pass or blockers are recorded.
- [ ] Traceability metadata includes source basis, input hash, result hash, runner version, and report/template version when present.
- [ ] Local web client run command is documented and tested.
- [ ] Cloud Linux deployment files are present.
- [ ] `/health` endpoint passes.
- [ ] `POST /api/calculate` smoke test passes with known input.
- [ ] Production debug mode is disabled.
- [ ] Secrets are environment-based and not committed.
- [ ] Data and output persistence paths are documented.

## Release Artifacts

| Artifact | Path | Required | Status |
| --- | --- | --- | --- |
| Local run instructions | README.md | true | to_be_defined |
| Environment example | deploy/env.example | true | to_be_defined |
| Dockerfile | deploy/Dockerfile | Docker path | to_be_defined |
| systemd service | deploy/systemd/*.service | systemd path | to_be_defined |
| nginx site config | deploy/nginx/*.conf | public Linux path | to_be_defined |
| Release runbook | release/runbook.md | when operational handoff needed | to_be_defined |
| Acceptance checklist | verification/acceptance_checklist.md | true | to_be_defined |

## Smoke Test Record

| Test | Command | Result | Notes |
| --- | --- | --- | --- |
| Local app start | `python -m webapp.app` | to_be_defined |  |
| Health | `curl -fsS http://127.0.0.1:5000/health` | to_be_defined |  |
| Main page | `curl -fsS http://127.0.0.1:5000/` | to_be_defined |  |
| Calculate API | `curl -fsS -X POST ... /api/calculate` | to_be_defined |  |
| Docker build | `docker build -f deploy/Dockerfile .` | to_be_defined |  |

## Remaining Assumptions

| Assumption | Risk | Owner | Resolution |
| --- | --- | --- | --- |
| to_be_defined | to_be_defined | to_be_defined | to_be_defined |


---

## templates/deployment/runtime_env.example

# Copy to a server-managed environment file and replace values.
# Do not commit production secrets.

APP_HOST=0.0.0.0
APP_PORT=5000
FLASK_DEBUG=0
SECRET_KEY=change-me-on-server
DATA_DIR=/var/lib/engineering-calc/data
OUTPUT_DIR=/var/lib/engineering-calc/outputs


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

## templates/implementation/api_route_skeleton.md

# API Route Skeleton

Use this template to document the API endpoint architecture for engineering calculation web applications.

## Technology Stack

| Item | Selected value | Notes |
| --- | --- | --- |
| Framework | Flask / FastAPI | Flask with Blueprint pattern |
| Server | gunicorn (production) / flask dev (development) | — |
| Serialization | `flask.jsonify` | Structured JSON responses |
| Error format | `{"status": "error", "message": "..."}` | Consistent error contract |

## Endpoint Registry

| Method | Path | Purpose | Input | Output | Auth |
| --- | --- | --- | --- | --- | --- |
| GET | `/health` | Deployment health check | none | JSON `{status: "ok"}` | none |
| GET | `/` | Serve main SPA page | — | HTML | none |
| GET | `/api/defaults` | Return default parameters | — | JSON (form defaults) | none |
| GET | `/api/i18n/<lang>` | Return i18n translations | lang: "en" or "zh" | JSON (key→text) | none |
| POST | `/api/calculate` | Run calculation | JSON (form data) | JSON (result UI dict) | none |
| POST | `/api/report/html` | Generate downloadable report | JSON (form data + lang) | HTML file download | none |
| POST | `/api/report/preview` | Generate report for inline preview | JSON (form data + lang) | JSON `{status, html}` | none |
| POST | `/api/import/json` | Import configuration | file upload or JSON body | JSON `{status, data}` | none |
| GET | `/api/export/json` | Export configuration | JSON (form data) | JSON file download | none |
| POST | `/api/optimize` | Auto-optimize parameters | JSON (form data + lang) | JSON (optimal result) | none |

## Handler Pattern

```python
@bp.route("/api/calculate", methods=["POST"])
def api_calculate():
    """Thin handler: parse → build model → call runner → convert → return."""
    try:
        data = request.get_json(force=True)
        ci = build_case_input_from_form(data)        # form_utils.py
        result = run_case(ci)                         # runner.py (the only calculation path)
        ui_data = case_result_to_ui(result, ci)       # form_utils.py
        return jsonify(ui_data)
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e) if DEBUG else "Calculation failed.",
        }), 400
```

## Error Handling Strategy

| HTTP code | Trigger | Response body |
| --- | --- | --- |
| 400 | Bad input, validation error, calculation failure | `{"status": "error", "message": "details"}` |
| 404 | Missing resource | `{"status": "error", "message": "Not found"}` |
| 500 | Unexpected server error | `{"status": "error", "message": "Internal server error"}` |

```text
in DEBUG mode: include full traceback in message field
in production: log traceback server-side, return generic message to client
frontend: show error in dismissible alert banner, preserve user input
```

## Application Factory Pattern

```python
# webapp/app.py
def create_app() -> Flask:
    app = Flask(__name__, template_folder="...", static_folder="...")
    app.secret_key = cfg.SECRET_KEY
    app.config["DEBUG"] = cfg.DEBUG
    from .routes import bp
    app.register_blueprint(bp)
    return app

# Development:
#   python -m webapp.app
# Production:
#   gunicorn "webapp.app:create_app()" --bind 0.0.0.0:5000 --workers 2
```

Production delivery must use the same application factory locally, in Docker, and on Linux servers.

## Rules

```text
route handlers must be thin — no business logic, no formula calls
all model building and result conversion lives in form_utils.py
all calculation lives behind run_book() / run_case() — never in routes
download responses must include Content-Disposition header
import endpoints should accept both file upload and raw JSON body
debug mode controlled by environment variable, not hard-coded
```


---

## templates/implementation/batch_flow.md

# Batch Flow

```text
read batch_control -> load input -> run_book -> save result JSON -> render report -> summary CSV
```


---

## templates/implementation/chart_integration.md

# Chart and Visualization Integration

Use this template to document the chart generation strategy for engineering calculation interfaces.

## Chart Generation Architecture

| Item | Selected value | Notes |
| --- | --- | --- |
| Chart library | matplotlib / plotly / D3.js | Server-side SVG generation |
| Output format | SVG string | Inline embeddable in HTML |
| i18n support | Bilingual SVG per chart | `{zh: svg_zh, en: svg_en}` dict |
| Delivery | Embedded in API response JSON | Via `result_to_ui()` converter |
| Frontend toggle | CSS class `.bi-zh` / `.bi-en` | JS hides/shows on language switch |

## Chart Inventory

| Chart ID | Name | Type | Data source | Trigger |
| --- | --- | --- | --- | --- |
| `chart_breakdown` | Result breakdown | horizontal bar | `BookResult.checks` | when > 1 check |
| `chart_stress` | Stress distribution | line (depth vs stress) | `SettlementResult.stress_profile` | when settlement exists |
| `chart_iz` | Influence factor Iz | line (depth vs Iz) | `SettlementResult.iz_profile` | when Iz method used |
| `chart_consol` | Consolidation curve | line (time vs U) | `ConsolidationResult` | when consolidation exists |
| `chart_soil` | Soil profile schematic | custom schematic | `SoilProfile.layers` | always available |
| `chart_util` | Utilization summary | horizontal bar | `BookResult.checks[*].utilization` | when > 1 check |
| to_be_defined | to_be_defined | to_be_defined | to_be_defined | to_be_defined |

## Chart Generation Pattern

```python
# src/<pkg>/report/charts.py
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend
import matplotlib.pyplot as plt
from io import BytesIO

def figure_to_svg(fig) -> str:
    buf = BytesIO()
    fig.savefig(buf, format="svg", bbox_inches="tight", dpi=150)
    plt.close(fig)
    return buf.getvalue().decode("utf-8")

def plot_result_breakdown(checks: list, lang: str = "en") -> plt.Figure:
    """Horizontal bar chart of utilization for all checks."""
    fig, ax = plt.subplots(figsize=(8, 3))
    # ... plot logic using BookResult values only ...
    ax.set_xlabel("Utilization" if lang == "en" else "利用率")
    return fig
```

## Bilingual Chart Helper

```python
def _bilingual_svg(plot_fn, *args, **kwargs) -> dict | None:
    """Generate chart in both languages for i18n toggle."""
    try:
        fig_zh = plot_fn(*args, lang="zh", **kwargs)
        svg_zh = figure_to_svg(fig_zh)
        fig_en = plot_fn(*args, lang="en", **kwargs)
        svg_en = figure_to_svg(fig_en)
        return {"zh": svg_zh, "en": svg_en}
    except Exception:
        return None
```

## Frontend Rendering Pattern

```html
<!-- In results.js or result template -->
<div class="chart-container">
    <div class="bi-zh" style="display:none">{{ chart_svg_zh | safe }}</div>
    <div class="bi-en">{{ chart_svg_en | safe }}</div>
</div>
```

## Color and Style Conventions

| Element | Color | Notes |
| --- | --- | --- |
| PASS status | `#198754` (Bootstrap success green) | Utilization < 1.0 |
| FAIL status | `#dc3545` (Bootstrap danger red) | Utilization >= 1.0 |
| WARNING | `#ffc107` (Bootstrap warning amber) | Near limit |
| Utilization bar < 0.7 | green fill | Safe |
| Utilization bar 0.7–1.0 | amber fill | Caution |
| Utilization bar >= 1.0 | red fill | Fail |

## Rules

```text
charts visualize BookResult values — they must not compute engineering results
label all axes with units
keep SVG output under 50KB per chart
use matplotlib Agg backend for server-side rendering
close all figures after SVG export to prevent memory leaks
provide chart data as structured dicts alongside SVG for accessibility and testing
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

deployment / release scripts
  -> app entrypoint
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
deployment -> engineering formulas or module internals
```

Reusable modules must stay asset-ready:

```text
libraries cannot import books, webapp, report, batch, deploy, release, or tests
libraries cannot read environment variables or deployment files
libraries cannot depend on Flask/FastAPI, templates, HTTP requests, or browser state
```


---

## templates/implementation/feature_classification.csv

feature,layer,existing_module,new_module_needed,reusable,location,notes


---

## templates/implementation/form_mapping_spec.md

# Form ↔ Model Bidirectional Mapping Specification

Use this template to document the conversion layer between web forms and typed calculation models.

## Mapping Functions

| Function | Direction | Input | Output | Module |
| --- | --- | --- | --- | --- |
| `build_case_input_from_form` | form → model | web form JSON dict | `BookInput` | `webapp/form_utils.py` |
| `case_input_to_form` | model → form | `BookInput` | web form JSON dict | `webapp/form_utils.py` |
| `case_result_to_ui` | result → UI | `BookResult` | UI display dict | `webapp/form_utils.py` |

## Form → Model Field Mapping

| Form field path | Model field | Type | Required | Default | Validation |
| --- | --- | --- | --- | --- | --- |
| `project.project_id` | `BookInput.project.project_id` | str | yes | `"UNKNOWN"` | non-empty |
| `foundation.B_m` | `BookInput.foundation.B_m` | float | yes | `1.0` | > 0 |
| `loads.Fz_kN` | `BookInput.load_case.Fz_kN` | float | yes | `0.0` | any |
| `soil_layers[i].thickness_m` | `SoilProfile.layers[i].thickness_m` | float | yes | `1.0` | > 0 |
| to_be_defined | to_be_defined | to_be_defined | to_be_defined | to_be_defined | to_be_defined |

## Model → Form Reverse Mapping

| Model field | Form field path | Notes |
| --- | --- | --- |
| `BookInput.project` | `project` | Direct dict conversion via dataclass fields |
| `BookInput.foundation` | `foundation` | Preserve all geometry fields |
| to_be_defined | to_be_defined | to_be_defined |

## Result → UI Display Mapping

| BookResult path | UI key | Display format | Unit | Status badge |
| --- | --- | --- | --- | --- |
| `governing.governing_check` | `governing.check` | string | — | — |
| `governing.utilization` | `governing.utilization` | `round(x, 4)` | — | color-coded |
| `bearing.check.status` | `bearing.status` | enum → string | — | PASS/FAIL badge |
| `settlement.total_mm` | `settlement.total_mm` | `round(x, 3)` | mm | OK/NG |
| to_be_defined | to_be_defined | to_be_defined | to_be_defined | to_be_defined |

## Sanitization Rules

| Condition | Action | Warning message |
| --- | --- | --- |
| `float('inf')` | replace with `null` | "Infinity (division by zero or overflow)" |
| `float('-inf')` | replace with `null` | "Infinity (overflow)" |
| `float('nan')` | replace with `null` | "NaN (not a number)" |

## Dynamic List Handling

| List | Add button | Delete button | Min items | Max items |
| --- | --- | --- | --- | --- |
| `soil_layers` | "Add Layer" | per-row delete | 1 | unlimited |
| to_be_defined | to_be_defined | to_be_defined | to_be_defined | to_be_defined |

## Validation Strategy

```text
required fields: reject with field-level error before runner call
numeric range: reject negative thickness, zero width, etc.
enum values: validate against allowed literals (e.g. "compression" | "tension")
cross-field: validate Fz sign matches limit_state (positive for compression)
```

## Notes

- Keep this mapping in sync with `BookInput` / `BookResult` model definitions.
- When adding a new model field, update this spec, the form template, and the JS rendering.


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
project.name,Project Name,,project,true,user_input,
project.code,Project Code,,project,true,user_input,
project.location,Location,,project,true,user_input,
inputs.param_example_1,Parameter 1,kN,loads,true,user_input,Edit label/unit per BookInput field
inputs.param_example_2,Parameter 2,m,geometry,true,user_input,
intermediate.value_1,Intermediate 1,kPa,results,false,computed,Read-only display from BookResult
checks.check_1,Check 1,,results,false,computed,Status badge + utilization bar


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

## templates/implementation/i18n_pattern.md

# Internationalization (i18n) Pattern

Use this template to document the i18n strategy for multilingual engineering calculation interfaces.

## i18n Architecture Decision

| Item | Selected value | Notes |
| --- | --- | --- |
| Dictionary format | `key -> (english, chinese)` tuple | Single master dictionary |
| Delivery method | `/api/i18n/<lang>` REST endpoint | Loaded on toggle, cached client-side |
| HTML binding | `data-i18n="key"` attribute | JS replaces `textContent` on toggle |
| Chart i18n | Bilingual SVG generation | CSS class toggle: `.bi-zh` / `.bi-en` |
| Report i18n | `lang` parameter passed to renderer | Report generated in selected language |
| Storage | `webapp/i18n.py` | Master dictionary + helper functions |

## Dictionary Categories

| Category | Example keys | Count estimate |
| --- | --- | --- |
| Navigation and layout | `app_title`, `app_subtitle`, `nav_calculate` | ~10 |
| Section titles | `section_project`, `section_soil`, `section_results` | ~8 |
| Form field labels | `fdn_width_b`, `soil_phi`, `load_Fz` | ~40 |
| Form help text | `load_Fz_help`, `opt_drainage` | ~10 |
| Button labels | `btn_calculate`, `btn_add_layer`, `btn_optimize` | ~12 |
| Result display labels | `result_bearing`, `result_settlement`, `result_governing` | ~30 |
| Status text | `result_status_ok`, `result_status_ng` | ~6 |
| Error messages | `error_calc_failed`, `error_invalid_input` | ~6 |
| Warning messages | `warn_invalid_values`, `warn_infinite` | ~4 |
| Report sections | `bearing_detail`, `conclusion` | ~10 |

## Implementation Pattern

```python
# webapp/i18n.py
I18N: dict[str, tuple[str, str]] = {
    "key": ("English text", "中文文本"),
    ...
}

def get_translations(lang: str = "en") -> dict[str, str]:
    idx = 0 if lang == "en" else 1
    return {k: v[idx] for k, v in I18N.items()}

def t(key: str, lang: str = "en") -> str:
    entry = I18N.get(key)
    if entry is None:
        return key
    return entry[0] if lang == "en" else entry[1]
```

## Frontend JS Pattern

```javascript
// webapp/static/js/i18n.js
let currentLang = "en";
let translations = {};

async function switchLanguage(lang) {
    const resp = await fetch(`/api/i18n/${lang}`);
    translations = await resp.json();
    currentLang = lang;
    document.querySelectorAll("[data-i18n]").forEach(el => {
        const key = el.getAttribute("data-i18n");
        if (translations[key]) el.textContent = translations[key];
    });
    // Toggle bilingual chart visibility
    document.querySelectorAll(".bi-zh, .bi-en").forEach(el => {
        el.style.display = el.classList.contains(`bi-${lang}`) ? "" : "none";
    });
}
```

## HTML Binding Pattern

```html
<span data-i18n="btn_calculate">Run Calculation</span>
<button data-i18n="btn_add_layer">Add Layer</button>
```

## Rules

```text
never hard-code display text in HTML templates — always use data-i18n keys
add new keys to the master dictionary before using them in templates
test both languages render correctly for every page
keep chart labels bilingual — generate two SVG variants
report renderer should accept lang parameter and use the same dictionary
```


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

## templates/implementation/module_asset_registry.csv

module_id,domain,category,module_name,public_function,input_model,options_model,result_model,source_references,formula_trace_path,unit_tests,regression_tests,reuse_status,asset_owner,notes


---

## templates/implementation/module_interface_spec.md

# Module Interface Specification

Use this template for decoupled reusable calculation modules that can become long-lived engineering assets.

## Module identity

| Item | Value |
| --- | --- |
| module_id | to_be_defined |
| domain | to_be_defined |
| category | to_be_defined |
| reuse_status | draft / reviewed / stable / deprecated |

## Public functions

## Input models

## Options models

## Result models

## Formula traces

## Warning/error behavior

## Dependency boundary

```text
no UI dependency
no report dependency
no batch-specific dependency
no deployment dependency
no file I/O unless explicitly classified as a lookup-data loader
```

## Asset registry row

Record this module in `module_asset_registry.csv`.


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
| deploy/ | deployment layer | Dockerfile, systemd service, nginx config, runtime env examples | app entrypoint only by command | formulas, reusable module internals |
| release/ | release handoff | release checklist, runbook, smoke records | none | formulas |


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
  deploy/
    nginx/
    systemd/
  release/
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

Use `webapp/` or `src/<pkg>/interfaces/webapp/` for the unified production frontend. Use `apps/review/` for Marimo review apps. Use `data/` for user-provided, imported, staging, normalized, and package-managed data. Use `outputs/` only for generated artifacts. Use `deploy/` for Linux/cloud runtime files and `release/` for final delivery checklists or runbooks.

Reusable calculation assets belong under `src/<pkg>/libraries/` and must be registered in `implementation/02_modules/module_asset_registry.csv`.


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

## Frontend Stack Decision

| Item | Selected value | Reason |
| --- | --- | --- |
| Template engine | Jinja2 / React / Vue | to_be_defined | server-rendered vs SPA |
| CSS framework | Bootstrap 5 / Tailwind / custom | to_be_defined | rapid prototyping |
| JS architecture | vanilla modules / React hooks | to_be_defined | see `api_route_skeleton.md` |
| i18n strategy | data-i18n + API endpoint | to_be_defined | see `i18n_pattern.md` |
| Chart library | matplotlib SVG / plotly / D3 | to_be_defined | see `chart_integration.md` |
| Formula rendering | KaTeX / MathJax / none | to_be_defined | for report preview |

## Deployment Entry

| Item | Selected value | Reason |
| --- | --- | --- |
| App factory | `webapp.app:create_app()` / other | Required for cloud runtime |
| Health endpoint | `/health` | Required for deployment smoke tests |
| Local run command | `python -m webapp.app` / other | Required for local client |
| Production run command | `gunicorn "webapp.app:create_app()" --bind 0.0.0.0:5000` / other | Required for Linux cloud |

## Related Templates

```text
form_mapping_spec.md    — form ↔ model bidirectional mapping
i18n_pattern.md         — internationalization strategy
chart_integration.md    — chart generation and embedding
api_route_skeleton.md   — Flask/FastAPI route architecture
```


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
- [ ] Reusable calculation modules are decoupled and registered in module_asset_registry.csv
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
- [ ] Web app exposes /health when frontend/API exists
- [ ] Local run command is documented and smoke-tested when frontend/API exists
- [ ] Cloud Linux deployment path is documented when final delivery is expected
- [ ] Release checklist records deployment smoke tests and remaining assumptions when final delivery is expected
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
    Q --> R[14 Cloud web release and deployment]
    R --> S[Runnable online web calculation program]
