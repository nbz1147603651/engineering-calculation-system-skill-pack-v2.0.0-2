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
