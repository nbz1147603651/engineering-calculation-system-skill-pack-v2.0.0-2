import { useState } from "react";
import Icon from "./Icon";
import { agentCatalog, platformDetails, platformMethod } from "./platformCatalog";
import type { ProductCopy, ProductLanguage } from "./content";

export default function AgentPlatforms({
  copy,
  language,
  selected,
  onSelect,
}: {
  copy: ProductCopy;
  language: ProductLanguage;
  selected: string;
  onSelect: (value: string) => void;
}) {
  const [expanded, setExpanded] = useState(false);
  const platform = platformDetails(selected);
  const visibleAgents = expanded ? agentCatalog : agentCatalog.filter((agent, index) => index < 3 || agent.id === selected);
  return (
    <section className="container agents-section" id="platforms">
      <div className="section-heading">
        <h2>{copy.platforms}</h2>
        <p>{copy.platformsIntro}</p>
      </div>
      <div className="agents-layout">
        <div className={expanded ? "agent-selector is-expanded" : "agent-selector"}>
        <div id="agent-options" className={expanded ? "agent-list expanded" : "agent-list"} role="group" aria-label={copy.nav[2]}>
          {visibleAgents.map((agent) => (
            <button
              className={
                selected === agent.id ? "agent-row selected" : "agent-row"
              }
              key={agent.id}
              aria-label={agent.name}
              aria-pressed={selected === agent.id}
              onClick={() => onSelect(agent.id)}
            >
                <img
                  src={agent.logo}
                  width="32"
                  height="32"
                  alt=""
                  loading="lazy"
                  className="agent-logo"
                />
              <strong>{agent.name}</strong>
              <Icon name="chevron" size={18} />
            </button>
          ))}
        </div>
          <button
            className="agent-row more-platforms"
            onClick={() => setExpanded((value) => !value)}
            aria-expanded={expanded}
            aria-controls="agent-options"
          >
            <Icon name="flow" size={27} />
            <span>{expanded ? copy.less : copy.more}</span>
            <span className={expanded ? "rotate-up" : "rotate-down"}>
              <Icon name="chevron" size={18} />
            </span>
          </button>
        </div>
        <div className="agent-detail" aria-live="polite" aria-atomic="true">
          <div className="agent-detail-heading">
            <img className="agent-logo" src={platform.logo} width="44" height="44" alt="" />
            <span>{language === "zh" ? "工程技能 · 平台接入" : "ENGINEERING SKILLS · PLATFORM SETUP"}</span>
          </div>
          <h3>{platform.name}</h3>
          <p className="agent-method">
            {language === "zh"
              ? "用熟悉的工具，完成更可靠的工程计算。"
              : "Reliable engineering, with the tools you know."}
          </p>
          <p className="agent-summary">
            {language === "zh"
              ? `将 Nimo 工程技能接入 ${platform.name}，从整理参考资料、梳理计算方法到校核结果，延续你已有的工作习惯。`
              : `Connect Nimo engineering skills to ${platform.name}. Organize references, work through calculation methods and verify results within your existing workflow.`}
          </p>
          <dl>
            <div>
              <dt>{copy.method}</dt>
              <dd>
                {platformMethod(selected, language)}
              </dd>
            </div>
            <div>
              <dt>{copy.location}</dt>
              <dd>
                {language === "zh"
                  ? "工程资料、计算分析与成果校核"
                  : "Engineering sources, calculation and review"}
              </dd>
            </div>
          </dl>
          <ol className="agent-setup-steps">
            {copy.steps.map((step, index) => <li key={step}><span>0{index + 1}</span>{step}</li>)}
          </ol>
          <a className="button button-primary" href="#install">
            {copy.details}
            <Icon name="arrow" />
          </a>
        </div>
      </div>
      <p className="compatibility">
        {copy.compatibility} Qoder · QoderCN · QoderWorkCN · WorkBuddy · Trae ·
        ZCode · MiniMaxCode
      </p>
    </section>
  );
}
