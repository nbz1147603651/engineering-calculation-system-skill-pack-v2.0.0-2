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

    data.inputs = {
        checks: [
            {
                check_id: "DEMO-001",
                name: document.getElementById("check_name")?.value || "Template demand/capacity check",
                demand: _numVal("check_demand", 45),
                capacity: _numVal("check_capacity", 90),
                limit: _numVal("check_limit", 1),
                unit: document.getElementById("check_unit")?.value || "kN",
                source_reference: "S01",
            },
        ],
    };

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

    const check = data.inputs?.checks?.[0] || data.checks?.[0] || {};
    _setVal("check_name", check.name);
    _setVal("check_demand", check.demand);
    _setVal("check_capacity", check.capacity);
    _setVal("check_limit", check.limit);
    _setVal("check_unit", check.unit);
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

function _numVal(id, fallback) {
    const value = document.getElementById(id)?.value;
    const number = Number.parseFloat(value);
    return Number.isFinite(number) ? number : fallback;
}
