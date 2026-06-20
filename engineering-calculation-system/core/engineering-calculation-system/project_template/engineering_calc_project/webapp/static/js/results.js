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
    renderCharts(data.charts || []);
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

function chartValue(chart, series, index) {
    const values = Array.isArray(series.values) ? series.values : [];
    return index < values.length ? values[index] : null;
}

function chartUnit(chart, series) {
    const axis = chart && chart.y_axis ? chart.y_axis : {};
    return series.unit || axis.unit || "";
}

function finiteNumber(value) {
    const number = Number(value);
    return Number.isFinite(number) ? number : null;
}

function chartMaxValue(chart) {
    const values = [];
    (chart.series || []).forEach(series => {
        (series.values || []).forEach(value => {
            const number = finiteNumber(value);
            if (number !== null) values.push(Math.abs(number));
        });
    });
    (chart.thresholds || []).forEach(threshold => {
        const number = finiteNumber(threshold.value);
        if (number !== null) values.push(Math.abs(number));
    });
    return values.length ? Math.max(...values) : 1;
}

function renderChartSvg(chart) {
    const categories = chart.categories || [];
    const seriesList = chart.series || [];
    if (!categories.length || !seriesList.length) return "";

    const palette = ["#2563eb", "#16a34a", "#dc2626", "#9333ea", "#f59e0b"];
    const left = 185;
    const top = 40;
    const plotWidth = 430;
    const barHeight = 12;
    const seriesGap = 5;
    const rowGap = 18;
    const seriesCount = Math.max(1, seriesList.length);
    const rowHeight = seriesCount * (barHeight + seriesGap) + rowGap;
    const width = 680;
    const height = top + categories.length * rowHeight + 38;
    const scale = plotWidth / chartMaxValue(chart);
    const axisLabel = escapeHtml((chart.y_axis && chart.y_axis.label) || "Value");

    let svg = `
        <svg class="chart-svg" viewBox="0 0 ${width} ${height}" role="img" aria-label="${escapeHtml(chart.title || "Chart")}">
            <line x1="${left}" y1="${top - 8}" x2="${left}" y2="${height - 30}" stroke="#94a3b8" stroke-width="1"></line>
            <line x1="${left}" y1="${height - 30}" x2="${left + plotWidth}" y2="${height - 30}" stroke="#94a3b8" stroke-width="1"></line>
    `;

    (chart.thresholds || []).forEach(threshold => {
        const value = finiteNumber(threshold.value);
        if (value === null) return;
        const x = left + Math.min(Math.abs(value) * scale, plotWidth);
        svg += `
            <line x1="${x.toFixed(2)}" y1="${top - 12}" x2="${x.toFixed(2)}" y2="${height - 30}" stroke="#ef4444" stroke-width="1.5" stroke-dasharray="4 3"></line>
            <text x="${(x + 4).toFixed(2)}" y="${top - 18}" font-size="10" fill="#991b1b">${escapeHtml(threshold.label || "Threshold")}: ${escapeHtml(threshold.value)}</text>
        `;
    });

    seriesList.forEach((series, index) => {
        const color = series.color || palette[index % palette.length];
        const x = left + index * 120;
        svg += `
            <rect x="${x}" y="8" width="10" height="10" fill="${escapeHtml(color)}"></rect>
            <text x="${x + 15}" y="17" font-size="10" fill="#334155">${escapeHtml(series.label || "Series")}</text>
        `;
    });

    categories.forEach((category, categoryIndex) => {
        const y0 = top + categoryIndex * rowHeight;
        const labelY = y0 + (seriesCount * (barHeight + seriesGap)) / 2;
        svg += `<text x="8" y="${labelY.toFixed(2)}" font-size="10" fill="#334155">${escapeHtml(category)}</text>`;

        seriesList.forEach((series, seriesIndex) => {
            const value = finiteNumber(chartValue(chart, series, categoryIndex));
            if (value === null) return;
            const color = series.color || palette[seriesIndex % palette.length];
            const y = y0 + seriesIndex * (barHeight + seriesGap);
            const barWidth = Math.min(Math.abs(value) * scale, plotWidth);
            svg += `
                <rect x="${left}" y="${y.toFixed(2)}" width="${barWidth.toFixed(2)}" height="${barHeight}" rx="2" fill="${escapeHtml(color)}"></rect>
                <text x="${(left + barWidth + 5).toFixed(2)}" y="${(y + 10).toFixed(2)}" font-size="10" fill="#334155">${escapeHtml(value)} ${escapeHtml(chartUnit(chart, series))}</text>
            `;
        });
    });

    svg += `
            <text x="${(left + plotWidth / 2).toFixed(2)}" y="${height - 8}" font-size="10" text-anchor="middle" fill="#475569">${axisLabel}</text>
        </svg>
    `;
    return svg;
}

function renderChartDataTable(chart) {
    const categories = chart.categories || [];
    const rows = [];
    categories.forEach((category, categoryIndex) => {
        (chart.series || []).forEach(series => {
            const paths = series.result_paths || [];
            rows.push(`
                <tr>
                    <td>${escapeHtml(category)}</td>
                    <td>${escapeHtml(series.label || "-")}</td>
                    <td>${fmt(chartValue(chart, series, categoryIndex))}</td>
                    <td>${escapeHtml(chartUnit(chart, series) || "-")}</td>
                    <td><code>${escapeHtml(paths[categoryIndex] || "-")}</code></td>
                </tr>
            `);
        });
    });

    return `
        <div class="table-responsive">
            <table class="table table-sm align-middle mb-0 chart-data-table">
                <thead><tr><th>Category</th><th>Series</th><th>Value</th><th>Unit</th><th>Result Path</th></tr></thead>
                <tbody>${rows.join("") || '<tr><td colspan="5" class="text-muted">No chart data recorded.</td></tr>'}</tbody>
            </table>
        </div>
    `;
}

function renderCharts(charts) {
    const section = document.getElementById("chartsSection");
    const body = document.getElementById("chartsBody");
    if (!section || !body) return;

    if (!charts.length) {
        section.classList.add("d-none");
        body.innerHTML = "";
        return;
    }

    section.classList.remove("d-none");
    body.innerHTML = charts.map(chart => {
        const notes = (chart.notes || []).map(note => `<li>${escapeHtml(note)}</li>`).join("");
        const paths = (chart.source_result_paths || []).map(path => `<code>${escapeHtml(path)}</code>`).join(", ") || "-";
        return `
            <article class="chart-panel">
                <div class="d-flex flex-wrap justify-content-between gap-2">
                    <div>
                        <h6 class="mb-1">${escapeHtml(chart.title || "Chart")}</h6>
                        <p class="text-muted small mb-2">${escapeHtml(chart.purpose || "")}</p>
                    </div>
                    <span class="badge bg-light text-dark border">${escapeHtml(chart.chart_type || "chart")}</span>
                </div>
                ${renderChartSvg(chart)}
                ${renderChartDataTable(chart)}
                <div class="small text-muted mt-2">
                    Source result paths: ${paths}<br>
                    Placement: report=${escapeHtml(chart.recommended_report_location || "-")};
                    UI=${escapeHtml(chart.recommended_ui_location || "-")}
                </div>
                ${notes ? `<ul class="small text-muted mt-2 mb-0">${notes}</ul>` : ""}
            </article>
        `;
    }).join("");
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
    ["governingBox", "formulaRegistryStrip", "chartsSection", "checksSection", "traceSection", "warningsBox", "errorsBox"].forEach(id => {
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

    link.classList.remove("disabled");
    link.setAttribute("href", marimoReview.shell_url || "/admin/review/");
    link.setAttribute("title", marimoReview.message || "Open review admin setup.");
    if (note) {
        note.textContent = status === "available"
            ? "Marimo installed; review token/service setup needed."
            : `Review setup needed. Install with: ${marimoReview.install_command || "python -m pip install marimo"}`;
    }
}
