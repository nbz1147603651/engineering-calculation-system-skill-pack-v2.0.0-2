/**
 * i18n.js — Language toggle and bilingual content management.
 *
 * Replaces text content of elements with data-i18n attributes
 * and toggles bilingual chart visibility on language switch.
 */

let currentLang = "en";
let translations = {};

async function switchLanguage(lang) {
    if (lang === currentLang) return;

    try {
        const resp = await fetch(`/api/i18n/${lang}`);
        if (!resp.ok) return;
        translations = await resp.json();
        currentLang = lang;
    } catch (e) {
        console.warn("Failed to load translations for", lang, e);
        return;
    }

    // Replace text content of all data-i18n elements
    document.querySelectorAll("[data-i18n]").forEach(el => {
        const key = el.getAttribute("data-i18n");
        if (translations[key] !== undefined) {
            el.textContent = translations[key];
        }
    });

    // Replace placeholder attributes
    document.querySelectorAll("[data-i18n-placeholder]").forEach(el => {
        const key = el.getAttribute("data-i18n-placeholder");
        if (translations[key] !== undefined) {
            el.placeholder = translations[key];
        }
    });

    // Toggle bilingual chart visibility
    document.querySelectorAll(".bi-zh, .bi-en").forEach(el => {
        el.style.display = el.classList.contains(`bi-${lang}`) ? "" : "none";
    });

    // Update language toggle button states
    document.querySelectorAll("#langToggle .btn").forEach(btn => {
        btn.classList.toggle("active", btn.dataset.lang === lang);
    });
}

// Initialize language toggle on page load
document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("#langToggle .btn").forEach(btn => {
        btn.addEventListener("click", () => switchLanguage(btn.dataset.lang));
    });
    // Load default language translations
    switchLanguage("en").then(() => { currentLang = "en"; });
});
