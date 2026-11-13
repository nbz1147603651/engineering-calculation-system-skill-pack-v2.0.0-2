"""Evidence-first workflow routes shared by the desktop and headless service.

This module plans work; it never approves engineering evidence or runs formulas.
The canonical lifecycle remains the authority for each stage's exit criteria.
"""

from __future__ import annotations

GROUPS = (
    {"id": "evidence", "title": "资料与依据", "stages": ["01", "02", "03"], "gate": "analysis_allowed", "description": "核实资料缺口、权威来源与本地证据，不重复获取已有可用资料。"},
    {"id": "blueprint", "title": "分析与交接", "stages": ["04", "05", "06", "07"], "gate": "production_allowed", "description": "冻结适用范围、单位、公式分支及可验证的实施交接。"},
    {"id": "calculation", "title": "计算内核", "stages": ["08", "09", "10", "11"], "gate": "runner_verified", "description": "统一 BookInput → run_book → BookResult，公式只驻留在计算层。"},
    {"id": "delivery", "title": "报告与交互", "stages": ["12a", "12b", "12c"], "gate": "interfaces_verified", "description": "界面、A4 计算书与批处理复用同一结果契约。"},
    {"id": "verification", "title": "验证与交付", "stages": ["13", "14"], "gate": "delivery_verified", "description": "用黄金算例、追溯、运行冒烟及部署证据验收声明的范围。"},
)
MODES = ("core-only", "report-only", "prototype-web", "web-complete")
LAYER_STAGES = {
    "source": tuple(stage for group in GROUPS for stage in group["stages"]),
    "formula": ("05", "06", "07", "10", "11", "13"),
    "model": ("09", "10", "11", "13"),
    "runner": ("10", "11", "13"),
    "report": ("12a", "13"),
    "ui": ("12b", "13"),
    "batch": ("12c", "13"),
    "deployment": ("13", "14"),
}
ORDER = tuple(stage for group in GROUPS for stage in group["stages"])


def overview() -> list[dict]:
    return [{**group, "stages": list(group["stages"])} for group in GROUPS]


def route(
    task_type: str = "new-system",
    delivery_mode: str = "web-complete",
    evidence_gate: str = "search_required",
    coding_gate: str = "no_go",
    changed_layers: tuple[str, ...] = (),
    baseline_verified: bool = False,
) -> dict:
    if delivery_mode not in MODES:
        raise ValueError(f"Unknown delivery mode: {delivery_mode}")
    if task_type not in ("new-system", "change", "analysis", "acquisition"):
        raise ValueError(f"Unknown task type: {task_type}")
    if evidence_gate not in ("evidence_no_go", "search_required", "partial_analysis_allowed", "analysis_allowed"):
        raise ValueError(f"Unknown evidence gate: {evidence_gate}")
    if coding_gate not in ("no_go", "prototype_allowed", "production_allowed"):
        raise ValueError(f"Unknown coding gate: {coding_gate}")
    unknown = set(changed_layers) - LAYER_STAGES.keys()
    if unknown:
        raise ValueError(f"Unknown changed layers: {', '.join(sorted(unknown))}")
    incremental = task_type == "change" and baseline_verified and bool(changed_layers)
    if incremental:
        required = {stage for layer in changed_layers for stage in LAYER_STAGES[layer]}
    else:
        required = set(ORDER)
        if delivery_mode == "core-only":
            required -= {"12a", "12b", "12c", "14"}
        elif delivery_mode == "report-only":
            required -= {"12b", "12c", "14"}
        elif delivery_mode == "prototype-web":
            required -= {"14"}
    if task_type == "acquisition":
        required &= {"01", "02", "03"}
    elif task_type == "analysis":
        required &= {"01", "02", "03", "04", "05", "06", "07"}
    if evidence_gate != "analysis_allowed":
        required.update(("01", "02", "03"))
    implementation = task_type not in ("analysis", "acquisition")
    coding_blocked = coding_gate == "no_go" or (coding_gate != "production_allowed" and delivery_mode != "prototype-web")
    if coding_blocked and implementation:
        required.update(("04", "05", "06", "07"))
    if evidence_gate == "evidence_no_go":
        status, next_action = "blocked", "Resolve source authority/access blockers before calculation work"
    elif evidence_gate != "analysis_allowed":
        status, next_action = "evidence_required", "Close the evidence gap; no production calculation claims"
    elif coding_blocked and implementation:
        status, next_action = "handoff_required", "Validate the implementation handoff and coding gate"
    else:
        status, next_action = "planned", "Execute the selected stages and collect fresh validation evidence"
    return {"task_type": task_type, "delivery_mode": delivery_mode, "incremental": incremental,
            "stages": [stage for stage in ORDER if stage in required], "status": status,
            "next_action": next_action, "evidence_gate": evidence_gate, "coding_gate": coding_gate,
            "completion_verified": False}
