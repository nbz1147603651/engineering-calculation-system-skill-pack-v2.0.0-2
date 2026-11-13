/**
 * i18n.js — Language toggle and bilingual content management.
 *
 * Uses the same pattern as the reference signboard foundation app:
 * server-side key -> (English, Chinese) dictionary, /api/i18n/<lang>,
 * data-i18n bindings, persisted operator preference, and bilingual chart
 * visibility through .bi-en / .bi-zh classes.
 */

var currentLang = "en";
var translations = {};

const I18n = (function () {
    const STORAGE_KEY = "engineering_calc_lang";
    const SUPPORTED_LANGS = ["en", "zh"];

    let _translations = {};
    let _currentLang = localStorage.getItem(STORAGE_KEY) || "en";
    if (!SUPPORTED_LANGS.includes(_currentLang)) {
        _currentLang = "en";
    }

    async function loadTranslations(lang) {
        const resp = await fetch(`/api/i18n/${lang}`);
        if (!resp.ok) {
            throw new Error(`Failed to load translations for ${lang}`);
        }
        _translations = await resp.json();
        publishGlobals();
        return _translations;
    }

    function publishGlobals() {
        currentLang = _currentLang;
        translations = _translations;
        window.currentLang = _currentLang;
        window.translations = _translations;
    }

    function t(key, fallback) {
        return _translations[key] || fallback || key;
    }

    function translateTextBindings() {
        document.querySelectorAll("[data-i18n]").forEach(el => {
            const key = el.getAttribute("data-i18n");
            const text = t(key);
            if (text !== key) {
                el.textContent = text;
            }
        });

        document.querySelectorAll("[data-i18n-html]").forEach(el => {
            const key = el.getAttribute("data-i18n-html");
            const text = t(key);
            if (text !== key) {
                el.innerHTML = text;
            }
        });

        document.querySelectorAll("[data-i18n-placeholder]").forEach(el => {
            const key = el.getAttribute("data-i18n-placeholder");
            const text = t(key);
            if (text !== key) {
                el.placeholder = text;
            }
        });

        document.querySelectorAll("[data-i18n-title]").forEach(el => {
            const key = el.getAttribute("data-i18n-title");
            const text = t(key);
            if (text !== key) {
                el.title = text;
                el.setAttribute("aria-label", text);
            }
        });
    }

    function updateLanguageShell() {
        document.documentElement.lang = _currentLang === "zh" ? "zh-CN" : "en";
        document.documentElement.setAttribute("data-lang", _currentLang);

        document.querySelectorAll("#langToggle .btn").forEach(btn => {
            const active = btn.getAttribute("data-lang") === _currentLang;
            btn.classList.toggle("active", active);
            btn.setAttribute("aria-pressed", active ? "true" : "false");
        });

        document.querySelectorAll(".bi-zh, .bi-en").forEach(el => {
            el.style.display = el.classList.contains(`bi-${_currentLang}`) ? "" : "none";
        });
    }

    function applyTranslations() {
        translateTextBindings();
        updateLanguageShell();
    }

    async function setLanguage(lang, options = {}) {
        if (!SUPPORTED_LANGS.includes(lang)) {
            lang = "en";
        }
        if (!options.force && lang === _currentLang && Object.keys(_translations).length > 0) {
            applyTranslations();
            return;
        }

        _currentLang = lang;
        localStorage.setItem(STORAGE_KEY, lang);
        await loadTranslations(lang);
        applyTranslations();

        document.dispatchEvent(new CustomEvent("languagechange", {
            detail: {lang: _currentLang, translations: _translations},
        }));
    }

    function getLang() {
        return _currentLang;
    }

    async function init() {
        document.querySelectorAll("#langToggle .btn").forEach(btn => {
            btn.addEventListener("click", () => setLanguage(btn.getAttribute("data-lang")));
        });
        await setLanguage(_currentLang, {force: true});
    }

    publishGlobals();
    return {init, setLanguage, switchLanguage: setLanguage, getLang, t, applyTranslations};
})();

window.I18n = I18n;
window.switchLanguage = I18n.setLanguage;

document.addEventListener("DOMContentLoaded", () => {
    I18n.init().catch(e => console.warn("Failed to initialize i18n:", e));
});
