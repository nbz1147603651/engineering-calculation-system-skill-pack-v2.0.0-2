from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Literal

from .latex_renderer import detect_latex_toolchain


ReportFormat = Literal["latex_pdf", "html_a4"]


@dataclass(frozen=True)
class ReportRenderDecision:
    output_format: ReportFormat
    reason: str
    latex_available: bool
    latex_tool: str | None = None
    latex_path: str | None = None

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def select_report_output() -> ReportRenderDecision:
    """Choose the strictest available calculation-book renderer for this host."""
    toolchain = detect_latex_toolchain()
    if toolchain["available"]:
        return ReportRenderDecision(
            output_format="latex_pdf",
            reason="Local LaTeX compiler detected; final report must compile without errors.",
            latex_available=True,
            latex_tool=toolchain["tool"],
            latex_path=toolchain["path"],
        )

    return ReportRenderDecision(
        output_format="html_a4",
        reason="No local LaTeX compiler detected; use rigorous A4 HTML calculation report.",
        latex_available=False,
    )
