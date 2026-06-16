# Internationalization (i18n) Pattern

Use this template to document the i18n strategy for multilingual engineering calculation interfaces.

## i18n Architecture Decision

| Item | Selected value | Notes |
| --- | --- | --- |
| Dictionary format | `key -> (english, chinese)` tuple | Single master dictionary |
| Delivery method | `/api/i18n/<lang>` REST endpoint | Loaded on toggle, cached client-side |
| HTML binding | `data-i18n="key"` attribute | JS replaces `textContent` on toggle |
| Chart i18n | Bilingual SVG generation | CSS class toggle: `.bi-zh` / `.bi-en` |
| Report i18n | `lang` parameter passed to renderer | Report generated in selected language |
| Storage | `webapp/i18n.py` | Master dictionary + helper functions |

## Dictionary Categories

| Category | Example keys | Count estimate |
| --- | --- | --- |
| Navigation and layout | `app_title`, `app_subtitle`, `nav_calculate` | ~10 |
| Section titles | `section_project`, `section_soil`, `section_results` | ~8 |
| Form field labels | `fdn_width_b`, `soil_phi`, `load_Fz` | ~40 |
| Form help text | `load_Fz_help`, `opt_drainage` | ~10 |
| Button labels | `btn_calculate`, `btn_add_layer`, `btn_optimize` | ~12 |
| Result display labels | `result_bearing`, `result_settlement`, `result_governing` | ~30 |
| Status text | `result_status_ok`, `result_status_ng` | ~6 |
| Error messages | `error_calc_failed`, `error_invalid_input` | ~6 |
| Warning messages | `warn_invalid_values`, `warn_infinite` | ~4 |
| Report sections | `bearing_detail`, `conclusion` | ~10 |

## Implementation Pattern

```python
# webapp/i18n.py
I18N: dict[str, tuple[str, str]] = {
    "key": ("English text", "中文文本"),
    ...
}

def get_translations(lang: str = "en") -> dict[str, str]:
    idx = 0 if lang == "en" else 1
    return {k: v[idx] for k, v in I18N.items()}

def t(key: str, lang: str = "en") -> str:
    entry = I18N.get(key)
    if entry is None:
        return key
    return entry[0] if lang == "en" else entry[1]
```

## Frontend JS Pattern

```javascript
// webapp/static/js/i18n.js
let currentLang = "en";
let translations = {};

async function switchLanguage(lang) {
    const resp = await fetch(`/api/i18n/${lang}`);
    translations = await resp.json();
    currentLang = lang;
    document.querySelectorAll("[data-i18n]").forEach(el => {
        const key = el.getAttribute("data-i18n");
        if (translations[key]) el.textContent = translations[key];
    });
    // Toggle bilingual chart visibility
    document.querySelectorAll(".bi-zh, .bi-en").forEach(el => {
        el.style.display = el.classList.contains(`bi-${lang}`) ? "" : "none";
    });
}
```

## HTML Binding Pattern

```html
<span data-i18n="btn_calculate">Run Calculation</span>
<button data-i18n="btn_add_layer">Add Layer</button>
```

## Rules

```text
never hard-code display text in HTML templates — always use data-i18n keys
add new keys to the master dictionary before using them in templates
test both languages render correctly for every page
keep chart labels bilingual — generate two SVG variants
report renderer should accept lang parameter and use the same dictionary
```
