import { useState } from "react";
import Icon from "./Icon";
import type { ProductCopy, ProductLanguage } from "./content";
import siteLinks from "@/data/siteLinks.json";

export function ProductHeader({
  copy,
  language,
  onLanguageChange,
}: {
  copy: ProductCopy;
  language: ProductLanguage;
  onLanguageChange: (value: ProductLanguage) => void;
}) {
  const [open, setOpen] = useState(false);
  return (
    <header className="product-header">
      <div className="container header-inner">
        <a href="#top" className="brand" aria-label="NIMO Engineering">
          <img src="./nimo-mascot.png" alt="" width="40" height="54" />
          <span>NIMO</span>
        </a>
        <nav
          className={open ? "header-nav is-open" : "header-nav"}
          aria-label={language === "zh" ? "主导航" : "Main navigation"}
        >
          <a className="brand-home-link" href={siteLinks[0].url}>NIMO Software <Icon name="arrow" size={14} /></a>
          {["#overview", "#workflow", "#platforms"].map((href, index) => (
            <a key={href} href={href} onClick={() => setOpen(false)}>
              {copy.nav[index]}
            </a>
          ))}
        </nav>
        <div className="header-actions">
          <button
            className="language-button"
            onClick={() => onLanguageChange(language === "zh" ? "en" : "zh")}
            aria-label={language === "zh" ? "Switch to English" : "切换到中文"}
          >
            {language === "zh" ? "EN" : "中文"}
          </button>
          <a className="button button-primary header-download" href="#install">
            {copy.download}
          </a>
          <button
            className="mobile-menu"
            aria-label={copy.menu}
            aria-expanded={open}
            onClick={() => setOpen(!open)}
          >
            <Icon name="menu" />
          </button>
        </div>
      </div>
    </header>
  );
}

function ClientPreview({ copy }: { copy: ProductCopy }) {
  return (
    <figure className="client-preview">
      <figcaption>{copy.preview}</figcaption>
      <div className="preview-window">
        <div className="preview-sidebar">
          <strong>
            NIMO
            <br />
            Engineering
          </strong>
          <div className="preview-nav">
            <span className="active">
              <Icon name="home" />
              {copy.nav[0]}
            </span>
            <span>
              <Icon name="plug" />
              {copy.nav[2]}
            </span>
            <span>
              <Icon name="flow" />
              {copy.nav[1]}
            </span>
            <span>
              <Icon name="log" />
              {copy.guide}
            </span>
          </div>
        </div>
        <div className="preview-main">
          <div className="preview-titlebar">
            <i />
            <i />
            <i />
          </div>
          <div className="preview-content">
            <h2>{copy.connect}</h2>
            <p>{copy.shared}</p>
            <div className="preview-table">
              {["Codex", "OpenCode", "DeepSeek Harness"].map((name, index) => (
                <div key={name}>
                  <span
                    className={
                      index !== 1 ? "preview-check checked" : "preview-check"
                    }
                  >
                    {index !== 1 && <Icon name="check" size={13} />}
                  </span>
                  <strong>{name}</strong>
                  <span className="preview-state">{copy.previewState}</span>
                </div>
              ))}
            </div>
          </div>
          <div className="preview-note">
            <img src="./nimo-mascot.png" width="54" height="76" alt="Nimo" />
            <strong>{copy.previewNote}</strong>
          </div>
        </div>
      </div>
    </figure>
  );
}

export function ProductHero({ copy }: { copy: ProductCopy }) {
  return (
    <>
      <section className="container product-hero" id="top">
        <div className="hero-copy">
          <h1>
            {copy.heading[0]}
            <br />
            <span>{copy.heading[1]}</span>
          </h1>
          <p className="hero-intro">{copy.intro}</p>
          <div className="hero-actions">
            <a href="#install" className="button button-primary">
              {copy.download}
            </a>
            <a href="#workflow" className="text-link">
              {copy.explore}
              <Icon name="arrow" />
            </a>
          </div>
          <p className="runtime-note">{copy.runtime}</p>
        </div>
        <ClientPreview copy={copy} />
      </section>
      <div className="container">
        <div className="platform-rail">
          <strong>{copy.rail}</strong>
          <div>
            {[
              "Codex",
              "OpenCode",
              "Qoder",
              "DeepSeek Harness",
              "ZCode",
              "MiniMax Code",
            ].map((name) => (
              <span key={name}>{name}</span>
            ))}
          </div>
        </div>
      </div>
      <section className="container overview-section" id="overview">
        <h2>{copy.overview}</h2>
        <div className="pillars">
          {copy.pillars.map(([title, text], index) => (
            <article key={title}>
              <h3>
                <span>0{index + 1}</span>
                {title}
              </h3>
              <p>{text}</p>
            </article>
          ))}
        </div>
      </section>
    </>
  );
}

export function ProductFooter({
  copy,
  version,
}: {
  copy: ProductCopy;
  version: string;
}) {
  return (
    <footer className="container product-footer">
      <a className="footer-wordmark" href="#top">
        NIMO<span>Engineering</span>
      </a>
      <p>{copy.footer}</p>
      <nav className="related-sites" aria-label="NIMO Software">
        {siteLinks.filter((site) => site.id !== "nimo-engineering").map((site) => <a href={site.url} key={site.id}>{site.name}</a>)}
      </nav>
      <span>
        © {new Date().getFullYear()} {copy.rights} · v{version}
      </span>
    </footer>
  );
}
