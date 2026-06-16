/**
 * results.js — Render calculation results, status badges, and traces.
 *
 * Customize for each calculation book's result structure.
 */

/**
 * Render the full result panel from the API response dict.
 */
function renderResults(data) {
    if (data.status === "error") {
        showError(data.message);
        return;
    }

    hidePlaceholder();

    // Governing summary
    renderGoverning(data.governing);

    // Warnings banner
    if (data.warnings && data.warnings.length > 0) {
        showWarnings(data.warnings);
    }

    // Errors
    if (data.errors && data.errors.length > 0) {
        showErrors(data.errors);
    }

    // Scaffold: render book-specific result sections.
    // if (data.bearing) renderBearingCard(data.bearing);
    // if (data.settlement) renderSettlementCard(data.settlement);
    // if (data.checks) renderChecksTable(data.checks);

    // Enable report preview button
    const btnPreview = document.getElementById("btnPreviewReport");
    if (btnPreview) btnPreview.disabled = false;
}

/**
 * Render the governing status box at the top of the results panel.
 */
function renderGoverning(gov) {
    const box = document.getElementById("governingBox");
    if (!box || !gov) return;

    box.classList.remove("d-none", "alert-success", "alert-danger", "alert-warning");

    const isOk = gov.status === "PASS" || gov.status === "OK";
    box.classList.add(isOk ? "alert-success" : "alert-danger");

    const statusText = isOk
        ? (translations.result_all_pass || "All checks PASS")
        : (translations.result_has_fail || "Some checks FAILED");

    const utilText = gov.utilization !== null && gov.utilization !== undefined
        ? ` | ${translations.result_utilization || "Utilization"}: ${(gov.utilization * 100).toFixed(1)}%`
        : "";

    box.innerHTML = `
        <strong>${statusText}</strong>
        <br>${translations.result_governing || "Governing"}: ${gov.check}${utilText}
    `;
}

/**
 * Format a numeric value for display. Returns '--' for null/undefined.
 */
function fmt(val, decimals = 3) {
    if (val === null || val === undefined) return "—";
    return Number(val).toFixed(decimals);
}

/**
 * Create a status badge HTML element.
 */
function statusBadge(status) {
    const isOk = status === "PASS" || status === "OK";
    const cls = isOk ? "bg-success" : "bg-danger";
    const text = isOk
        ? (translations.result_status_ok || "PASS")
        : (translations.result_status_ng || "FAIL");
    return `<span class="badge ${cls}">${text}</span>`;
}

/**
 * Clear results and show placeholder.
 */
function clearResults() {
    showPlaceholder();
    const box = document.getElementById("governingBox");
    if (box) box.classList.add("d-none");
    const btnPreview = document.getElementById("btnPreviewReport");
    if (btnPreview) btnPreview.disabled = true;
    hideWarnings();
    hideErrors();
}

// ── Placeholder / Warning / Error helpers ────────────────────────────

function hidePlaceholder() {
    const el = document.getElementById("resultsPlaceholder");
    if (el) el.classList.add("d-none");
}

function showPlaceholder() {
    const el = document.getElementById("resultsPlaceholder");
    if (el) el.classList.remove("d-none");
}

function showWarnings(warnings) {
    // Scaffold: render warning banner
    console.warn("Calculation warnings:", warnings);
}

function hideWarnings() {}

function showErrors(errors) {
    console.error("Calculation errors:", errors);
}

function hideErrors() {}

function showError(message) {
    const box = document.getElementById("governingBox");
    if (box) {
        box.classList.remove("d-none", "alert-success");
        box.classList.add("alert-danger");
        box.innerHTML = `<strong>Error:</strong> ${message}`;
    }
}
