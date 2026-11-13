"""Web compatibility surface over the UI-independent input/output adapter.

Mapping logic lives in pkg.interfaces.input_mapping so CLI, golden-case replay,
and report-only projects do not depend on a web application package.
"""

from pkg.interfaces.input_mapping import (
    _default_check_payload,
    _opt,
    _plain,
    _sanitize_json,
    _to_dict,
    book_input_to_form,
    build_case_input_from_form,
    case_result_to_ui,
)

__all__ = ["book_input_to_form", "build_case_input_from_form", "case_result_to_ui"]
