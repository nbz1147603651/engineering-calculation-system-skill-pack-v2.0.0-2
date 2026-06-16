/**
 * main.js — Event binding, API calls, and orchestration.
 *
 * This is the central coordinator that ties forms, results, and i18n together.
 */

document.addEventListener("DOMContentLoaded", () => {

    // ── Load defaults on page load ────────────────────────────────────
    fetch("/api/defaults")
        .then(r => r.json())
        .then(data => populateForm(data))
        .catch(e => console.warn("Could not load defaults", e));

    // ── Calculate button ──────────────────────────────────────────────
    const btnCalc = document.getElementById("btnCalculate");
    if (btnCalc) {
        btnCalc.addEventListener("click", async () => {
            btnCalc.disabled = true;
            btnCalc.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span>Calculating...';
            try {
                const data = collectFormData();
                data.lang = currentLang;

                const resp = await fetch("/api/calculate", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify(data),
                });

                const result = await resp.json();
                renderResults(result);

            } catch (e) {
                showError(e.message || "Network error");
            } finally {
                btnCalc.disabled = false;
                btnCalc.innerHTML = `<i class="bi bi-play-fill me-1"></i><span data-i18n="btn_calculate">${translations.btn_calculate || "Run Calculation"}</span>`;
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
                data.lang = currentLang;

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
                frame.srcdoc = `<p style="padding:2rem;color:red">Report preview failed.</p>`;
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
                data.lang = currentLang;

                const resp = await fetch("/api/report/html", {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify(data),
                });

                if (!resp.ok) throw new Error("Report download failed");
                const blob = await resp.blob();
                const url = URL.createObjectURL(blob);
                const a = document.createElement("a");
                a.href = url;
                a.download = "report.html";
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
                    alert(result.message || "Import failed");
                }
            } catch (e) {
                alert("Import failed: " + e.message);
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
                if (!resp.ok) throw new Error("Export failed");
                const blob = await resp.blob();
                const url = URL.createObjectURL(blob);
                const a = document.createElement("a");
                a.href = url;
                a.download = "config.json";
                a.click();
                URL.revokeObjectURL(url);
            } catch (e) {
                alert("Export failed: " + e.message);
            }
        });
    }

    // ── Reset button ──────────────────────────────────────────────────
    const btnReset = document.getElementById("btnReset");
    if (btnReset) {
        btnReset.addEventListener("click", resetToDefaults);
    }

});
