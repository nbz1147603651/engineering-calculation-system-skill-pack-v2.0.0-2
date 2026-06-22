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

    from pkg.review.bridge import append_review_decision, list_review_sessions, read_review_session, review_root

    return append_review_decision, json, list_review_sessions, mo, read_review_session, review_root


@app.cell
def __(list_review_sessions, mo, review_root):
    sessions = list_review_sessions()
    session_ids = [item["session_id"] for item in sessions] or ["no_session"]
    session_select = mo.ui.dropdown(
        options=session_ids,
        value=session_ids[0],
        label="Review session",
    )
    mo.vstack([
        mo.md(
            f"""
            # Calculation Review

            Python-native Marimo review for frontend-created calculation sessions,
            including BookResult checks and FormulaTrace records.

            **Review root:** `{review_root()}`

            Use `marimo edit` during engineering development when reviewers need to modify
            Python cells for draft investigation. Use `marimo run` behind `/admin/review/`
            for controlled review.
            """
        ),
        session_select,
    ])
    return session_select, sessions


@app.cell
def __(mo, read_review_session, session_select):
    session_id = session_select.value
    if session_id == "no_session":
        session = {}
        mo.callout("No frontend review sessions have been created yet.", kind="warn")
    else:
        session = read_review_session(session_id)
        state = session["state"]
        result = session["result"]
        governing = result.get("governing", {})
        mo.md(
            f"""
            ## Session `{session_id}`

            **Status:** `{state.get("status")}`  
            **Review decision:** `{state.get("review_decision")}`  
            **Overall status:** `{governing.get("overall_status")}`  
            **Governing check:** `{governing.get("governing_check_id") or "-"}`
            """
        )
    return session, session_id


@app.cell
def __(mo, session):
    result = session.get("result", {})
    checks = result.get("checks", []) if isinstance(result, dict) else []
    if not checks:
        mo.md("No checks recorded in this session.")
    else:
        rows = [
            "| Check | Name | Status | Utilization | Source formulas |",
            "| --- | --- | --- | --- | --- |",
        ]
        for check in checks:
            traces = check.get("formula_traces") or []
            formula_ids = ", ".join(trace.get("formula_id", "-") for trace in traces)
            rows.append(
                "| {check_id} | {name} | {status} | {utilization} | {formula_ids} |".format(
                    check_id=check.get("check_id", "-"),
                    name=check.get("name", "-"),
                    status=check.get("status", "-"),
                    utilization=check.get("utilization", "-"),
                    formula_ids=formula_ids or "-",
                )
            )
        mo.md("\n".join(rows))
    return checks


@app.cell
def __(checks, mo):
    trace_options = []
    for check in checks:
        for trace in check.get("formula_traces", []) or []:
            trace_options.append(f"{check.get('check_id')}::{trace.get('formula_id')}")
    if not trace_options:
        trace_select = mo.ui.dropdown(options=["no_trace"], value="no_trace", label="Formula trace")
    else:
        trace_select = mo.ui.dropdown(options=trace_options, value=trace_options[0], label="Formula trace")
    trace_select
    return trace_select


@app.cell
def __(checks, mo, trace_select):
    selected = trace_select.value
    selected_trace = None
    selected_check = None
    if selected != "no_trace":
        check_id, formula_id = selected.split("::", 1)
        for check in checks:
            if str(check.get("check_id")) != check_id:
                continue
            for trace in check.get("formula_traces", []) or []:
                if str(trace.get("formula_id")) == formula_id:
                    selected_check = check
                    selected_trace = trace
                    break
    if not selected_trace:
        mo.md("No formula trace selected.")
    else:
        expression = selected_trace.get("expression_tex") or selected_trace.get("expression_plain") or "not recorded"
        mo.md(
            f"""
            ### {selected_trace.get("formula_id")} - {selected_trace.get("formula_name")}

            **Check:** `{selected_check.get("check_id")}`  
            **Source:** `{selected_trace.get("source_reference")}`  
            **Result path:** `{selected_trace.get("result_path") or "-"}`

            {selected_trace.get("engineering_explanation") or ""}

            $${expression}$$

            ```json
            {selected_trace}
            ```
            """
        )
    return selected_check, selected_trace


@app.cell
def __(mo, session_id):
    decision = mo.ui.dropdown(
        options=["accepted", "needs_change", "rejected"],
        value="needs_change",
        label="Decision",
    )
    reviewer = mo.ui.text(value="reviewer", label="Reviewer")
    notes = mo.ui.text_area(value="", label="Review notes", rows=4)
    save_decision = mo.ui.run_button(
        label="Save review decision",
        disabled=session_id == "no_session",
    )
    mo.vstack([decision, reviewer, notes, save_decision])
    return decision, notes, reviewer, save_decision


@app.cell
def __(append_review_decision, decision, mo, notes, reviewer, save_decision, session_id):
    if save_decision.value and session_id != "no_session":
        state = append_review_decision(
            session_id,
            reviewer=reviewer.value,
            decision=decision.value,
            notes=notes.value,
        )
        mo.callout(
            f"Saved review decision `{state['review_decision']}` for session `{session_id}`.",
            kind="success",
        )
    else:
        mo.md("Review decisions are appended to `outputs/review/review_decisions.jsonl`.")
    return


if __name__ == "__main__":
    app.run()
