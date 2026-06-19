/**
 * results.js - render calculation results, capability status, and traces.
 *
 * This layer displays trusted API data only. It must not calculate engineering
 * results, override pass/fail status, or perform unit conversion for official
 * values.
 */

function normalizeStatus(status) {
    return String(status || "NOT_EVALUATED").replace(/^Status\./, "");
}

function escapeHtml(value) {
    return String(value ?? "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#39;");
}

function renderResults(data) {
    if (data.status === "error") {
        showError(data.message);
        return;
    }

    hidePlaceholder();
    renderGoverning(data.governing);
    renderFormulaRegistry(data.formula_registry);
    renderChecksTable(data.checks || []);
    renderFormulaTraces(data.checks || []);
    renderWarningsErrors(data.warnings || [], data.errors || []);

    const btnPreview = document.getElementById("btnPreviewReport");
    if (btnPreview) btnPreview.disabled = false;
    const btnLatex = document.getElementById("btnDownloadLatex");
    if (btnLatex) btnLatex.disabled = false;
}

function renderGoverning(gov) {
    const box = document.getElementById("governingBox");
    if (!box || !gov) return;

    const status = normalizeStatus(gov.status);
    box.classList.remove("d-none", "alert-success", "alert-danger", "alert-warning", "alert-secondary");

    const isOk = status === "PASS" || status === "OK";
    const isProblem = status === "FAIL" || status === "ERROR";
    const alertClass = isOk ? "alert-success" : isProblem ? "alert-danger" : "alert-warning";
    box.classList.add(alertClass);

    const statusText = isOk
        ? (translations.result_all_pass || "All checks PASS")
        : isProblem
            ? (translations.result_has_fail || "Some checks FAILED")
            : `Status: ${status}`;

    const utilText = gov.utilization !== null && gov.utilization !== undefined
        ? ` | ${translations.result_utilization || "Utilization"}: ${(gov.utilization * 100).toFixed(1)}%`
        : "";

    box.innerHTML = `
        <strong>${escapeHtml(statusText)}</strong>
        <br>${escapeHtml(translations.result_governing || "Governing")}: ${escapeHtml(gov.check || "-")}${escapeHtml(utilText)}
    `;
}

function fmt(val, decimals = 3) {
    if (val === null || val === undefined || val === "") return "-";
    const num = Number(val);
    return Number.isFinite(num) ? num.toFixed(decimals) : escapeHtml(val);
}

function statusBadge(status) {
    const normalized = normalizeStatus(status);
    const cls = normalized === "PASS" || normalized === "OK"
        ? "bg-success"
        : normalized === "FAIL" || normalized === "ERROR"
            ? "bg-danger"
            : "bg-warning text-dark";
    return `<span class="badge ${cls}">${escapeHtml(normalized)}</span>`;
}

function renderChecksTable(checks) {
    const section = document.getElementById("checksSection");
    const body = document.getElementById("checksTableBody");
    if (!section || !body) return;

    section.classList.remove("d-none");
    if (!checks.length) {
        body.innerHTML = `<tr><td colspan="8" class="text-muted">No checks recorded by BookResult.</td></tr>`;
        return;
    }

    body.innerHTML = checks.map(check => `
        <tr>
            <td>${escapeHtml(check.check_id || "-")}</td>
            <td>${escapeHtml(check.name || "-")}</td>
            <td>${statusBadge(check.status)}</td>
            <td>${fmt(check.demand)}</td>
            <td>${fmt(check.capacity)}</td>
            <td>${fmt(check.utilization, 4)}</td>
            <td>${fmt(check.limit, 4)}</td>
            <td>${escapeHtml(check.unit || "-")}</td>
        </tr>
    `).join("");
}

function renderFormulaTraces(checks) {
    const section = document.getElementById("traceSection");
    const body = document.getElementById("traceBody");
    if (!section || !body) return;

    const traces = [];
    checks.forEach(check => {
        (check.formula_traces || []).forEach(trace => traces.push({check, trace}));
    });

    section.classList.remove("d-none");
    if (!traces.length) {
        body.innerHTML = `<p class="text-muted mb-0">No formula traces were recorded for this scaffold result.</p>`;
        return;
    }

    body.innerHTML = traces.map(({check, trace}) => `
        <div class="border-start border-primary ps-3 mb-3">
            <div class="fw-bold">${escapeHtml(trace.formula_id || "-")} - ${escapeHtml(trace.formula_name || "-")}</div>
            <div class="small text-muted">Check: ${escapeHtml(check.check_id || "-")} | Source: ${escapeHtml(trace.source_reference || "-")}</div>
            <div class="small">Inputs: ${escapeHtml(JSON.stringify(trace.inputs || {}))}</div>
            <div class="small">Intermediates: ${escapeHtml(JSON.stringify(trace.intermediates || {}))}</div>
            <div class="small">Result: ${escapeHtml(trace.result_symbol || "-")} = ${escapeHtml(trace.result_value ?? "-")} ${escapeHtml(trace.unit || "")}</div>
        </div>
    `).join("");
}

function renderWarningsErrors(warnings, errors) {
    renderListAlert("warningsBox", warnings, "warning", "Warnings");
    renderListAlert("errorsBox", errors, "danger", "Errors");
}

function renderListAlert(id, items, kind, title) {
    const box = document.getElementById(id);
    if (!box) return;
    if (!items.length) {
        box.classList.add("d-none");
        box.innerHTML = "";
        return;
    }
    box.className = `alert alert-${kind} mb-3`;
    box.innerHTML = `<strong>${escapeHtml(title)}</strong><ul class="mb-0">${items.map(item => `<li>${escapeHtml(item)}</li>`).join("")}</ul>`;
}

function clearResults() {
    showPlaceholder();
    ["governingBox", "formulaRegistryStrip", "checksSection", "traceSection", "warningsBox", "errorsBox"].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.classList.add("d-none");
    });
    const btnPreview = document.getElementById("btnPreviewReport");
    if (btnPreview) btnPreview.disabled = true;
    const btnLatex = document.getElementById("btnDownloadLatex");
    if (btnLatex) btnLatex.disabled = true;
}

function hidePlaceholder() {
    const el = document.getElementById("resultsPlaceholder");
    if (el) el.classList.add("d-none");
}

function showPlaceholder() {
    const el = document.getElementById("resultsPlaceholder");
    if (el) el.classList.remove("d-none");
}

function showError(message) {
    const box = document.getElementById("governingBox");
    if (box) {
        box.classList.remove("d-none", "alert-success", "alert-warning");
        box.classList.add("alert-danger");
        box.innerHTML = `<strong>Error:</strong> ${escapeHtml(message)}`;
    }
}

function renderFormulaRegistry(registry) {
    const strip = document.getElementById("formulaRegistryStrip");
    if (!strip || !registry) return;

    const hash = registry.hash ? registry.hash.substring(0, 12) : "untracked";
    const published = registry.published_at || "not published";
    strip.classList.remove("d-none");
    strip.innerHTML = `
        <span><strong>Formula version:</strong> ${escapeHtml(registry.version || "unversioned")}</span>
        <span><strong>Hash:</strong> ${escapeHtml(hash)}</span>
        <span><strong>Published:</strong> ${escapeHtml(published)}</span>
    `;
}

function renderCapabilities(payload) {
    const strip = document.getElementById("capabilityStrip");
    if (!strip || !payload || !payload.capabilities) return;
    const caps = payload.capabilities;
    const marimoReview = caps.marimo_review || {};
    const latex = caps.latex || {};
    const python = caps.python || {};

    strip.classList.remove("d-none");
    strip.innerHTML = `
        <span><strong>Python:</strong> ${escapeHtml(python.version || "unknown")}</span>
        <span><strong>Marimo review:</strong> ${escapeHtml(marimoReview.status || "missing")}</span>
        <span><strong>Report output:</strong> ${escapeHtml(latex.available ? "latex/pdf available" : "html_a4 fallback")}</span>
    `;

    configureReviewAdmin(marimoReview);
}

function configureReviewAdmin(marimoReview) {
    const link = document.getElementById("btnAdminReview");
    const note = document.getElementById("adminReviewStatus");
    if (!link) return;

    const status = marimoReview.status || "missing";
    if (status === "configured") {
        link.classList.remove("disabled");
        link.setAttribute("href", marimoReview.admin_url || "/admin/review/");
        link.setAttribute("title", "Open Marimo review admin");
        if (note) note.textContent = "";
        return;
    }

    link.classList.add("disabled");
    link.removeAttribute("href");
    link.setAttribute("title", marimoReview.message || "Marimo review is not enabled.");
    if (note) {
        note.textContent = `Marimo review is not enabled. Install with: ${marimoReview.install_command || "python -m pip install marimo"}`;
    }
}
