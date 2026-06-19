/**
 * main.js — Event binding, API calls, and orchestration.
 *
 * This is the central coordinator that ties forms, results, and i18n together.
 */

function getCurrentLang() {
    if (window.I18n && typeof window.I18n.getLang === "function") {
        return window.I18n.getLang();
    }
    return window.currentLang || document.documentElement.getAttribute("data-lang") || "en";
}

function uiText(key, fallback) {
    if (window.I18n && typeof window.I18n.t === "function") {
        return window.I18n.t(key, fallback);
    }
    return (window.translations && window.translations[key]) || fallback || key;
}

function getSelectedLatexTemplateId() {
    const select = document.getElementById("latexTemplateSelect");
    return select && select.value ? select.value : "default_engineering_calcbook";
}

function restoreCalculateButton(btnCalc) {
    btnCalc.innerHTML = `<i class="bi bi-play-fill me-1"></i><span data-i18n="btn_calculate">${uiText("btn_calculate", "Run Calculation")}</span>`;
}

document.addEventListener("DOMContentLoaded", () => {

    // ── Load defaults on page load ────────────────────────────────────
    fetch("/api/defaults")
        .then(r => r.json())
        .then(data => populateForm(data))
        .catch(e => console.warn("Could not load defaults", e));

    fetch("/api/capabilities")
        .then(r => r.json())
        .then(data => renderCapabilities(data))
        .catch(e => console.warn("Could not load capabilities", e));

    // ── Load LaTeX template options. Empty or missing user choice falls back server-side.
    const latexTemplateSelect = document.getElementById("latexTemplateSelect");
    if (latexTemplateSelect) {
        fetch("/api/report/templates")
            .then(r => r.json())
            .then(payload => {
                const templates = payload.templates || [];
                latexTemplateSelect.innerHTML = "";
                if (templates.length === 0) {
                    const option = document.createElement("option");
                    option.value = payload.default_template_id || "default_engineering_calcbook";
                    option.textContent = uiText("latex_template_default", "Default template");
                    latexTemplateSelect.appendChild(option);
                    return;
                }

                templates.forEach(template => {
                    const option = document.createElement("option");
                    option.value = template.id;
                    option.textContent = template.is_default
                        ? uiText("latex_template_default", "Default template")
                        : template.label;
                    option.selected = Boolean(template.is_default);
                    latexTemplateSelect.appendChild(option);
                });
            })
            .catch(e => console.warn("Could not load LaTeX templates", e));
    }

    // ── Calculate button ──────────────────────────────────────────────
    const btnCalc = document.getElementById("btnCalculate");
    if (btnCalc) {
        btnCalc.addEventListener("click", async () => {
            btnCalc.disabled = true;
            btnCalc.innerHTML = `<span class="spinner-border spinner-border-sm me-1"></span>${uiText("status_calculating", "Calculating...")}`;
            try {
                const data = collectFormData();
                data.lang = getCurrentLang();

                const resp = await fetch("/api/calculate", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify(data),
                });

                const result = await resp.json();
                renderResults(result);
                if (window.I18n) window.I18n.applyTranslations();

            } catch (e) {
                showError(e.message || uiText("error_network", "Network error"));
            } finally {
                btnCalc.disabled = false;
                restoreCalculateButton(btnCalc);
            }
        });
    }

    // ── Report preview button ─────────────────────────────────────────
    const btnPreview = document.getElementById("btnPreviewReport");
    if (btnPreview) {
        btnPreview.addEventListener("click", async () => {
            const modal = document.getElementById("reportModal");
            const frame = document.getElementById("reportFrame");
            const loading = document.getElementById("reportLoading");

            if (!modal || !frame) return;

            // Show modal with loading state
            const bsModal = new bootstrap.Modal(modal);
            bsModal.show();
            if (loading) loading.classList.remove("d-none");
            frame.src = "about:blank";

            try {
                const data = collectFormData();
                data.lang = getCurrentLang();

                const resp = await fetch("/api/report/preview", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify(data),
                });

                const result = await resp.json();
                if (result.status === "ok") {
                    frame.srcdoc = result.html;
                } else {
                    frame.srcdoc = `<p style="padding:2rem;color:red">${result.message}</p>`;
                }
            } catch (e) {
                frame.srcdoc = `<p style="padding:2rem;color:red">${uiText("error_report_preview_failed", "Report preview failed.")}</p>`;
            } finally {
                if (loading) loading.classList.add("d-none");
            }
        });
    }

    // ── Report download button ────────────────────────────────────────
    const btnDownload = document.getElementById("btnDownloadReport");
    if (btnDownload) {
        btnDownload.addEventListener("click", async () => {
            try {
                const data = collectFormData();
                data.lang = getCurrentLang();
                data.latex_template_id = getSelectedLatexTemplateId();

                const resp = await fetch("/api/report/final", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify(data),
                });

                if (!resp.ok) throw new Error(uiText("error_report_download_failed", "Report download failed."));
                const blob = await resp.blob();
                const contentType = resp.headers.get("Content-Type") || "";
                const url = URL.createObjectURL(blob);
                const a = document.createElement("a");
                a.href = url;
                a.download = contentType.includes("application/pdf") ? "calculation_report.pdf" : "calculation_report.html";
                a.click();
                URL.revokeObjectURL(url);

            } catch (e) {
                alert(e.message);
            }
        });
    }

    // ── LaTeX / Overleaf package download button ──────────────────────
    const btnLatex = document.getElementById("btnDownloadLatex");
    if (btnLatex) {
        btnLatex.addEventListener("click", async () => {
            try {
                const data = collectFormData();
                data.lang = getCurrentLang();
                data.latex_template_id = getSelectedLatexTemplateId();

                const resp = await fetch("/api/report/latex", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify(data),
                });

                if (!resp.ok) throw new Error(uiText("error_latex_download_failed", "LaTeX export failed."));
                const blob = await resp.blob();
                const url = URL.createObjectURL(blob);
                const a = document.createElement("a");
                a.href = url;
                a.download = "latex_report.zip";
                a.click();
                URL.revokeObjectURL(url);

            } catch (e) {
                alert(e.message);
            }
        });
    }

    // ── Import JSON button ────────────────────────────────────────────
    const btnImport = document.getElementById("btnImportJson");
    const fileInput = document.getElementById("fileImport");

    if (btnImport && fileInput) {
        btnImport.addEventListener("click", () => fileInput.click());

        fileInput.addEventListener("change", async () => {
            const file = fileInput.files[0];
            if (!file) return;

            const formData = new FormData();
            formData.append("file", file);

            try {
                const resp = await fetch("/api/import/json", {
                    method: "POST",
                    body: formData,
                });
                const result = await resp.json();
                if (result.status === "ok") {
                    populateForm(result.data);
                    clearResults();
                } else {
                    alert(result.message || uiText("error_import_failed", "Import failed."));
                }
            } catch (e) {
                alert(`${uiText("error_import_failed", "Import failed.")}: ${e.message}`);
            }

            fileInput.value = "";  // Reset for re-import
        });
    }

    // ── Export JSON button ────────────────────────────────────────────
    const btnExport = document.getElementById("btnExportJson");
    if (btnExport) {
        btnExport.addEventListener("click", async () => {
            try {
                const data = collectFormData();
                const resp = await fetch("/api/export/json", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify(data),
                });
                if (!resp.ok) throw new Error(uiText("error_export_failed", "Export failed."));
                const blob = await resp.blob();
                const url = URL.createObjectURL(blob);
                const a = document.createElement("a");
                a.href = url;
                a.download = "config.json";
                a.click();
                URL.revokeObjectURL(url);
            } catch (e) {
                alert(`${uiText("error_export_failed", "Export failed.")}: ${e.message}`);
            }
        });
    }

    // ── Reset button ──────────────────────────────────────────────────
    const btnReset = document.getElementById("btnReset");
    if (btnReset) {
        btnReset.addEventListener("click", resetToDefaults);
    }

});
