from __future__ import annotations

try:
    import marimo
except ModuleNotFoundError:
    marimo = None


class _MissingMarimoApp:
    def __init__(self) -> None:
        self.message = "Marimo is not installed. Install with: python -m pip install marimo"

    def cell(self, func=None):
        if func is None:
            return lambda wrapped: wrapped
        return func

    def run(self) -> None:
        raise RuntimeError(self.message)


__generated_with = "0.8.0"
app = marimo.App(width="full") if marimo is not None else _MissingMarimoApp()


@app.cell
def __():
    import json
    import marimo as mo

    from pkg.core.formula_registry import (
        active_registry_metadata,
        active_versions_path,
        publish_formula_rule,
        read_json_yaml,
        registry_root,
        run_book_smoke_check,
        validate_formula_rule,
    )

    return (
        active_registry_metadata,
        active_versions_path,
        json,
        mo,
        publish_formula_rule,
        read_json_yaml,
        registry_root,
        run_book_smoke_check,
        validate_formula_rule,
    )


@app.cell
def __(active_registry_metadata, active_versions_path, mo, registry_root):
    root = registry_root()
    metadata = active_registry_metadata(root)
    mo.md(
        f"""
        # Formula Review Admin

        Edit declaration-based formula rules, validate them, and publish a tested
        active version for the production web calculator.

        **Registry root:** `{root}`

        **Active registry:** `{active_versions_path(root)}`

        **Current version:** `{metadata["formula_registry_version"]}`

        **Current hash:** `{metadata["formula_hash"] or "untracked"}`
        """
    )
    return metadata, root


@app.cell
def __(mo, read_json_yaml, root):
    active_data = read_json_yaml(root / "active_versions.yaml")
    active_modules = sorted((active_data.get("active") or {}).keys())
    if not active_modules:
        active_modules = ["example_module"]
    module_select = mo.ui.dropdown(
        options=active_modules,
        value=active_modules[0],
        label="Module",
    )
    module_select
    return active_data, active_modules, module_select


@app.cell
def __(active_data, json, module_select, read_json_yaml, root):
    module_id = module_select.value
    module_ref = (active_data.get("active") or {}).get(module_id, {})
    current_path = root / module_ref.get(
        "path", f"modules/{module_id}/versions/example_v1.yaml"
    )
    current_rule = read_json_yaml(current_path)
    current_text = json.dumps(current_rule, indent=2, ensure_ascii=False)
    return current_path, current_rule, current_text, module_id


@app.cell
def __(current_path, mo, module_id):
    mo.md(
        f"""
        ## Review `{module_id}`

        Active rule file: `{current_path}`

        The editor below accepts JSON-compatible YAML. Publishing creates a new
        version file, runs declared tests and a `run_book()` smoke test, writes
        a publish log, and updates `active_versions.yaml` only after validation
        passes.
        """
    )
    return


@app.cell
def __(current_text, mo):
    rule_editor = mo.ui.text_area(
        value=current_text,
        label="Formula rule declaration",
        full_width=True,
        rows=28,
    )
    rule_editor
    return (rule_editor,)


@app.cell
def __(json, mo, rule_editor, run_book_smoke_check, validate_formula_rule):
    try:
        draft_rule = json.loads(rule_editor.value)
        validation_errors = validate_formula_rule(draft_rule)
        if not validation_errors:
            validation_errors.extend(run_book_smoke_check())
    except Exception as exc:
        draft_rule = {}
        validation_errors = [str(exc)]

    if validation_errors:
        mo.callout(
            "\n".join(f"- {item}" for item in validation_errors),
            kind="danger",
        )
    else:
        mo.callout("Draft formula rule is valid, smoke-tested, and ready to publish.", kind="success")
    return draft_rule, validation_errors


@app.cell
def __(mo, validation_errors):
    admin_name = mo.ui.text(value="admin", label="Admin name")
    publish_notes = mo.ui.text_area(value="", label="Publish notes", rows=3)
    publish_button = mo.ui.run_button(
        label="Validate and publish active version",
        disabled=bool(validation_errors),
    )
    mo.vstack([admin_name, publish_notes, publish_button])
    return admin_name, publish_button, publish_notes


@app.cell
def __(admin_name, draft_rule, mo, publish_button, publish_formula_rule, publish_notes):
    if publish_button.value:
        result = publish_formula_rule(
            draft_rule,
            admin=admin_name.value or "admin",
            notes=publish_notes.value or "",
        )
        if result["status"] == "published":
            mo.callout(
                f"Published `{result['path']}` with sha256 `{result['sha256']}`.",
                kind="success",
            )
        else:
            mo.callout("\n".join(result["errors"]), kind="danger")
    else:
        mo.md("Click publish after reviewing the declaration and validation result.")
    return


@app.cell
def __(metadata, mo):
    mo.md(
        f"""
        ## Production effect

        After a successful publish, the next request to `/api/calculate` loads the
        active formula registry version. The browser UI and report templates do not
        contain engineering formulas.

        Current active modules: `{", ".join(metadata["active_modules"]) or "none"}`
        """
    )
    return


if __name__ == "__main__":
    app.run()
