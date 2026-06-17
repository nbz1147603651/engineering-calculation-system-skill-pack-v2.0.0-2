/**
 * forms.js — Form interaction, dynamic lists, and validation feedback.
 *
 * Customize for each calculation book's input structure.
 */

/**
 * Collect all form data into a JSON-compatible dictionary.
 * Called before POST /api/calculate.
 */
function collectFormData() {
    const data = {};

    // Project info
    data.project = {
        project_id: document.getElementById("project_id")?.value || "",
        project_name: document.getElementById("project_name")?.value || "",
        case_id: document.getElementById("case_id")?.value || "",
    };

    // Scaffold: collect book-specific form sections.
    // data.foundation = { B_m: parseFloat(...), ... };
    // data.loads = { Fx_kN: parseFloat(...), ... };
    // data.options = { ... };

    return data;
}

/**
 * Populate form fields from a data dictionary (e.g. from defaults or import).
 */
function populateForm(data) {
    if (data.project) {
        _setVal("project_id", data.project.project_id);
        _setVal("project_name", data.project.project_name);
        _setVal("case_id", data.project.case_id);
    }

    // Scaffold: populate book-specific sections.
    // if (data.foundation) { _setVal("B_m", data.foundation.B_m); ... }
    // if (data.loads) { _setVal("Fx_kN", data.loads.Fx_kN); ... }
}

/**
 * Reset form to server defaults.
 */
async function resetToDefaults() {
    try {
        const resp = await fetch("/api/defaults");
        const defaults = await resp.json();
        populateForm(defaults);
        clearResults();
    } catch (e) {
        console.error("Failed to load defaults", e);
    }
}

// ── Helpers ──────────────────────────────────────────────────────────

function _setVal(id, value) {
    const el = document.getElementById(id);
    if (el && value !== undefined && value !== null) {
        el.value = value;
    }
}
