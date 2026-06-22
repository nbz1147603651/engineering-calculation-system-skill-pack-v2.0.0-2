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


def select_report_output(preferred_format: ReportFormat | None = None) -> ReportRenderDecision:
    """Choose the default calculation-book renderer for this host.

    Print-ready A4 HTML is the primary default because it is easy to review,
    archive, and print from a browser. LaTeX remains available as an explicit
    export/compile path when a PDF or Overleaf package is requested.
    """
    toolchain = detect_latex_toolchain()
    if preferred_format == "latex_pdf" and toolchain["available"]:
        return ReportRenderDecision(
            output_format="latex_pdf",
            reason="LaTeX PDF was explicitly requested and a local compiler was detected.",
            latex_available=True,
            latex_tool=toolchain["tool"],
            latex_path=toolchain["path"],
        )

    return ReportRenderDecision(
        output_format="html_a4",
        reason=(
            "Default calculation-book output is print-ready A4 HTML; "
            "LaTeX/Overleaf export remains available when explicitly requested."
        ),
        latex_available=bool(toolchain["available"]),
        latex_tool=toolchain["tool"],
        latex_path=toolchain["path"],
    )
