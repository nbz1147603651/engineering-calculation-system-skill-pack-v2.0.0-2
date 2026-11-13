#!/usr/bin/env python3
"""Select delivery scope from explicit deliverables, independently of host/UI."""

from __future__ import annotations

import argparse
import json

DELIVERABLE_MODES = {
    "module": "core-only", "library": "core-only", "batch": "core-only", "cli": "core-only",
    "report": "report-only", "calculation-book": "report-only",
    "prototype": "prototype-web", "mockup": "prototype-web",
    "web": "web-complete", "online-calculator": "web-complete", "deployable-system": "web-complete",
}
MODES = {"core-only", "report-only", "prototype-web", "web-complete"}


def select_delivery(deliverables: list[str] | tuple[str, ...], explicit_mode: str | None = None) -> str:
    """Use the requested product; an unspecified task retains the full-system default.

    A named delivery mode is authoritative. Web+prototype means a prototype web
    surface unless a deployable/online product was also explicitly requested.
    A report may include a core batch flow without adding a web deployment.
    """
    if explicit_mode is not None:
        if explicit_mode not in MODES:
            raise ValueError(f"Unknown delivery mode: {explicit_mode}")
        return explicit_mode
    unknown = set(deliverables) - DELIVERABLE_MODES.keys()
    if unknown:
        raise ValueError(f"Unknown deliverables: {', '.join(sorted(unknown))}")
    requested = set(deliverables)
    if requested & {"deployable-system", "online-calculator"}:
        return "web-complete"
    if requested & {"prototype", "mockup"}:
        return "prototype-web"
    if "web" in requested:
        return "web-complete"
    if requested & {"report", "calculation-book"}:
        return "report-only"
    return "core-only" if requested else "web-complete"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deliverable", choices=sorted(DELIVERABLE_MODES), action="append", default=[])
    parser.add_argument("--delivery", choices=sorted(MODES))
    args = parser.parse_args(argv)
    mode = select_delivery(args.deliverable, args.delivery)
    print(json.dumps({"delivery_mode": mode, "deliverables": args.deliverable,
                      "production_verified": False, "requires_web": mode in {"prototype-web", "web-complete"}}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
